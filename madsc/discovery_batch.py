"""Read-only K2 M3U candidate extraction and cross-source corroboration.

Never probes URLs, writes playlists or upgrades candidates to live channels.
"""
from __future__ import annotations

import re
import unicodedata
from collections import defaultdict
from hashlib import sha256

from madsc.discovery import classify_candidates, normalize_url

ATTR = re.compile(r'([\w-]+)="([^"]*)"')


def _canonical_source_name(name: str) -> str:
    return unicodedata.normalize("NFKC", name.strip()).casefold()


def parse_m3u(text: str, source: str, *, max_entries: int = 20000) -> dict:
    if not isinstance(text, str) or not isinstance(source, str) or not source.strip() or len(text) > 8_000_000:
        raise ValueError("Source and M3U text are required")
    # Surrogate code points cannot be represented in UTF-8 output and must
    # fail at ingestion rather than during downstream hashing or rendering.
    try:
        text.encode("utf-8", errors="strict")
        source.encode("utf-8", errors="strict")
    except UnicodeEncodeError as exc:
        raise ValueError("M3U source and text must be valid UTF-8") from exc
    # Source names are provenance labels, not arbitrary control sequences.
    # Reject embedded controls before they can contaminate audit reports.
    if any(unicodedata.category(ch) in ("Cc", "Cf", "Zl", "Zp") for ch in source):
        raise ValueError("Source name contains control characters")
    if len(source) > 256:
        raise ValueError("Source name exceeds bounded length")
    if type(max_entries) is not int or not 1 <= max_entries <= 20000:
        raise ValueError("Invalid candidate limit")
    lines = text.removeprefix("\ufeff").splitlines()
    if not lines or lines[0] != "#EXTM3U":
        raise ValueError("Missing M3U header")
    # A URL may not be silently associated with a different EXTINF entry.
    # Malformed metadata consumes only its own following URL.
    candidates, errors = [], []
    pending = None
    discard_url_for_rejected_entry = False
    for number, raw in enumerate(lines[1:], 2):
        line = raw.strip()
        if discard_url_for_rejected_entry:
            if line.startswith("#EXTINF:"):
                # A new entry started before a URL; do not consume its metadata.
                discard_url_for_rejected_entry = False
            elif line and not line.startswith("#"):
                # The URL belonging to the rejected metadata row is consumed,
                # preventing a duplicate diagnostic for the same malformed entry.
                discard_url_for_rejected_entry = False
                continue
        if line.startswith("#EXTINF:"):
            if pending is not None:
                errors.append({"line": number, "reason": "missing_url"})
            # EXTINF attributes may contain commas inside quoted values.
            # Only the first comma outside quotes separates metadata from title.
            quoted = False
            separator = -1
            for offset, char in enumerate(line):
                if char == '"':
                    quoted = not quoted
                elif char == "," and not quoted:
                    separator = offset
                    break
            if separator < 0 or quoted:
                pending = None
                errors.append({"line": number, "reason": "missing_channel_name"})
                discard_url_for_rejected_entry = True
                continue
            meta, title = line[:separator], line[separator + 1:]
            if not title.strip():
                pending = None
                errors.append({"line": number, "reason": "empty_channel_name"})
                discard_url_for_rejected_entry = True
                continue
            if meta.count('"') % 2:
                pending = None
                errors.append({"line": number, "reason": "unbalanced_metadata_quotes"})
                discard_url_for_rejected_entry = True
                continue
            attr_pairs = ATTR.findall(meta)
            # Attributes must start at a whitespace boundary; otherwise a
            # quoted-looking substring inside an attribute name is ambiguous.
            if any(match.start() == 0 or not meta[match.start() - 1].isspace()
                   for match in ATTR.finditer(meta)):
                pending = None
                errors.append({"line": number, "reason": "invalid_metadata_attribute"})
                discard_url_for_rejected_entry = True
                continue
            identity_attributes = {"tvg-id", "tvg-logo", "group-title"}
            if any(name.casefold() not in identity_attributes
                   and any(identity in name.casefold() for identity in identity_attributes)
                   for name, _ in attr_pairs):
                pending = None
                errors.append({"line": number, "reason": "invalid_metadata_attribute"})
                discard_url_for_rejected_entry = True
                continue
            # Do not silently discard malformed identity-related attributes.
            # A bare or unquoted tvg-id could otherwise turn a channel into a
            # misleading name-only match instead of a rejected candidate.
            remainder = ATTR.sub("", meta)
            if re.search(r'(?i)(?:^|\s)(?:tvg-id|tvg-logo|group-title)\s*=', remainder):
                pending = None
                errors.append({"line": number, "reason": "invalid_metadata_attribute"})
                discard_url_for_rejected_entry = True
                continue
            attr_names = [name.casefold() for name, _ in attr_pairs]
            # Repeated attributes make channel identity ambiguous. Reject the
            # row instead of silently keeping the last value via dict().
            if len(attr_names) != len(set(attr_names)):
                pending = None
                errors.append({"line": number, "reason": "duplicate_metadata_attribute"})
                discard_url_for_rejected_entry = True
                continue
            attrs = {name.casefold(): value for name, value in attr_pairs}
            pending = {"name": title.strip(), "tvg_id": attrs.get("tvg-id", ""),
                       "tvg_logo": attrs.get("tvg-logo", ""),
                       "group_title": attrs.get("group-title", "")}
        elif line.startswith("#") or not line:
            continue
        elif pending is not None:
            if len(candidates) >= max_entries:
                raise ValueError("Source exceeds bounded candidate limit")
            candidates.append({**pending, "url": line, "source": source})
            pending = None
        else:
            errors.append({"line": number, "reason": "orphan_url"})
    if pending is not None:
        errors.append({"line": len(lines), "reason": "missing_url"})
    classified = classify_candidates(candidates)
    return {"source": source, "entries": len(candidates),
            "candidate_rows": [candidates[item["source_index"]] for item in classified["candidates"]],
            "candidates": classified["candidates"],
            "duplicates": classified["duplicates"],
            "alternatives": classified["alternatives"],
            "rejected": classified["rejected"], "parse_errors": errors,
            "production_writes": False, "live_verified": False}


def corroborate_sources(sources: dict[str, str], known_urls: set[str] | None = None) -> dict:
    """Rank independent feed corroboration without treating it as playback proof."""
    if not isinstance(sources, dict) or not sources or len(sources) > 200:
        raise ValueError("Require 1-200 named M3U sources")
    if any(not isinstance(name, str) or not name.strip() for name in sources):
        raise ValueError("Invalid source name")
    if len({_canonical_source_name(name) for name in sources}) != len(sources):
        raise ValueError("Ambiguous duplicate source names")
    if any(len(name) > 256 for name in sources):
        raise ValueError("Source name exceeds bounded length")
    if known_urls is not None and not isinstance(known_urls, (set, frozenset)):
        raise ValueError("Known URLs must be a set")
    if known_urls is not None and len(known_urls) > 20000:
        raise ValueError("Too many known URLs")
    if known_urls is not None and any(not isinstance(url, str) for url in known_urls):
        raise ValueError("Known URLs must contain strings")
    if known_urls is not None and any(
        len(url) > 8192 or any(0xD800 <= ord(ch) <= 0xDFFF for ch in url)
        for url in known_urls
    ):
        raise ValueError("Known URLs contain oversized or invalid Unicode values")
    if known_urls is not None and any(
        any(unicodedata.category(ch) in ("Cc", "Cf", "Cs", "Zl", "Zp") for ch in url)
        for url in known_urls
    ):
        raise ValueError("Known URLs contain control characters")
    if any(any(unicodedata.category(ch) in ("Cc", "Cf", "Cs", "Zl", "Zp")
               for ch in source) for source in sources):
        raise ValueError("Invalid source name: control characters or UTF-8 surrogates")
    if any(not isinstance(body, str) for body in sources.values()):
        raise ValueError("M3U source bodies must be text")
    if sum(len(body) for body in sources.values()) > 8_000_000:
        raise ValueError("Combined source text exceeds bounded input limit")
    # Validate provenance labels before URL normalization and aggregation.
    # Avoid parsing each M3U twice just to reject malformed source names.
    if any(any(unicodedata.category(ch) in ("Cc", "Cf", "Cs", "Zl", "Zp")
               for ch in source) for source in sources):
        raise ValueError("Invalid source name: control characters or UTF-8 surrogates")
    known = {normalize_url(url) for url in (known_urls or set())}
    grouped = defaultdict(lambda: {"sources": set(), "source_fingerprints": set(),
                                    "urls": set(), "names": set()})
    reports = {}
    for source, text in sorted(sources.items()):
        report = parse_m3u(text, source)
        reports[source] = {"entries": report["entries"], "rejected": len(report["rejected"]),
                           "parse_errors": len(report["parse_errors"])}
        # Labels and serialization order do not prove independence. Fingerprint
        # the parsed channel inventory so transport formatting, comments, and
        # row ordering cannot manufacture corroboration votes.
        # Presentation-only changes (display name, logo, group for tvg-id
        # channels) cannot turn a mirrored inventory into a second vote.
        # Name/group remain identity fields when a tvg-id is absent.
        semantic_rows = sorted(
            (
                entry["url_sha256"],
                ("tvg", entry["tvg_id"].casefold()) if entry["tvg_id"] else
                ("name", entry["name"].casefold(), entry["group_title"].casefold()),
            )
            for entry, original in zip(report["candidates"], report["candidate_rows"])
            if normalize_url(original["url"]) not in known
        )
        source_fingerprint = sha256(repr(semantic_rows).encode("utf-8")).hexdigest()
        for entry, original in zip(report["candidates"], report["candidate_rows"]):
            if normalize_url(original["url"]) in known:
                continue
            identity = ("tvg", entry["tvg_id"].casefold()) if entry["tvg_id"] else (
                "name", entry["name"].casefold(), entry["group_title"].casefold())
            row = grouped[identity]
            row["sources"].add(source)
            row["source_fingerprints"].add(source_fingerprint)
            row["names"].add(entry["name"])
            row["urls"].add(entry["url_sha256"])
    output = []
    for identity, row in grouped.items():
        output.append({"identity_sha256": sha256(repr(identity).encode()).hexdigest(),
                       "source_count": len(row["source_fingerprints"]),
                       "sources": sorted(row["sources"]),
                       "url_variants": len(row["urls"]),
                       # A distinct feed inventory is not proof of an
                       # independently operated/licensed source. Keep this
                       # explicit so downstream consumers cannot promote the
                       # count into a verified-source claim.
                       "source_independence_verified": False,
                       "status": "REVIEW_REQUIRED_NOT_LIVE_VERIFIED"})
    output.sort(key=lambda x: (-x["source_count"], -x["url_variants"], x["identity_sha256"]))
    return {"sources_checked": len(reports), "source_reports": reports,
            "identity_candidates": output, "known_urls_supplied": len(known),
            "source_count_semantics": "distinct_semantic_feed_inventories_not_verified_origins",
            "source_independence_verified": False,
            "production_writes": False, "live_verified": False}


def build_m3u8_preview(sources: dict[str, str]) -> dict:
    """K2 -> K3 -> K5: in-memory UTF-8 M3U8 draft, all channels untested."""
    from madsc.channel_catalog import prepare_channel_catalog
    from madsc.playlist_previews import render_playlist_previews

    if not isinstance(sources, dict) or not sources or len(sources) > 200:
        raise ValueError("Require 1-200 named M3U sources")
    if len({_canonical_source_name(name) for name in sources if isinstance(name, str)}) != len(sources):
        raise ValueError("Ambiguous duplicate source names")
    if any(isinstance(name, str) and len(name) > 256 for name in sources):
        raise ValueError("Source name exceeds bounded length")
    rows = []
    rejected_count = 0
    # Downstream classification is bounded to 20,000 rows in total.
    max_total_candidates = 20000
    if any(not isinstance(source, str) or not source.strip() for source in sources):
        raise ValueError("Invalid source name")
    if any(not isinstance(body, str) for body in sources.values()):
        raise ValueError("M3U source bodies must be text")
    # Bound total input size before parsing any feed; each feed is already
    # individually limited, but 200 feeds could otherwise amplify memory use.
    if sum(len(body) for body in sources.values()) > 8_000_000:
        raise ValueError("Combined source text exceeds bounded input limit")
    for source, body in sorted(sources.items()):
        parsed = parse_m3u(body, source)
        if len(rows) + len(parsed["candidate_rows"]) > max_total_candidates:
            raise ValueError("Combined sources exceed bounded candidate limit")
        rows.extend(parsed["candidate_rows"])
        rejected_count += len(parsed["rejected"]) + len(parsed["parse_errors"])
    catalog = prepare_channel_catalog(rows)
    previews = render_playlist_previews(catalog, rows)
    draft = previews["drafts"]["TEST_BEKLIYOR"]
    if not draft.startswith("#EXTM3U\n"):
        raise ValueError("Invalid M3U8 preview")
    draft.encode("utf-8", errors="strict")
    return {"filename": "playlist.m3u8", "content": draft,
            "channel_count": previews["counts"]["TEST_BEKLIYOR"],
            "duplicates": len(catalog["duplicates"]),
            "rejected": rejected_count + len(catalog["rejected"]),
            "status": "SANDBOX_PREVIEW_ONLY",
            "production_writes": False, "production_ready": False,
            "ibo_device_verified": False}
