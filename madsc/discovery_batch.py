"""Read-only K2 M3U candidate extraction and cross-source corroboration.

Never probes URLs, writes playlists or upgrades candidates to live channels.
"""
from __future__ import annotations

import re
from collections import defaultdict
from hashlib import sha256

from madsc.discovery import classify_candidates, normalize_url

ATTR = re.compile(r'([\w-]+)="([^"]*)"')


def parse_m3u(text: str, source: str, *, max_entries: int = 20000) -> dict:
    if not isinstance(text, str) or not isinstance(source, str) or not source.strip():
        raise ValueError("Source and M3U text are required")
    if not 1 <= max_entries <= 20000:
        raise ValueError("Invalid candidate limit")
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "#EXTM3U":
        raise ValueError("Missing M3U header")
    candidates, errors = [], []
    pending = None
    for number, raw in enumerate(lines[1:], 2):
        line = raw.strip()
        if line.startswith("#EXTINF:"):
            if pending is not None:
                errors.append({"line": number, "reason": "missing_url"})
            if "," not in line:
                pending = None
                errors.append({"line": number, "reason": "missing_channel_name"})
                continue
            meta, title = line.split(",", 1)
            attrs = dict(ATTR.findall(meta))
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
    if pending is not None:
        errors.append({"line": len(lines), "reason": "missing_url"})
    classified = classify_candidates(candidates)
    return {"source": source, "entries": len(candidates),
            "candidates": classified["candidates"],
            "duplicates": classified["duplicates"],
            "alternatives": classified["alternatives"],
            "rejected": classified["rejected"], "parse_errors": errors,
            "production_writes": False, "live_verified": False}


def corroborate_sources(sources: dict[str, str], known_urls: set[str] | None = None) -> dict:
    """Rank independent feed corroboration without treating it as playback proof."""
    if not isinstance(sources, dict) or not sources or len(sources) > 200:
        raise ValueError("Require 1-200 named M3U sources")
    known = {normalize_url(url) for url in (known_urls or set())}
    grouped = defaultdict(lambda: {"sources": set(), "urls": set(), "names": set()})
    reports = {}
    for source, text in sorted(sources.items()):
        report = parse_m3u(text, source)
        reports[source] = {"entries": report["entries"], "rejected": len(report["rejected"]),
                           "parse_errors": len(report["parse_errors"])}
        # Keep one vote per independent source, regardless of repeated entries.
        for entry in report["candidates"]:
            identity = ("tvg", entry["tvg_id"].casefold()) if entry["tvg_id"] else (
                "name", entry["name"].casefold(), entry["group_title"].casefold())
            row = grouped[identity]
            row["sources"].add(source)
            row["names"].add(entry["name"])
            row["urls"].add(entry["url_sha256"])
    output = []
    for identity, row in grouped.items():
        output.append({"identity_sha256": sha256(repr(identity).encode()).hexdigest(),
                       "source_count": len(row["sources"]),
                       "sources": sorted(row["sources"]),
                       "url_variants": len(row["urls"]),
                       "status": "REVIEW_REQUIRED_NOT_LIVE_VERIFIED"})
    output.sort(key=lambda x: (-x["source_count"], -x["url_variants"], x["identity_sha256"]))
    return {"sources_checked": len(reports), "source_reports": reports,
            "identity_candidates": output, "known_urls_supplied": len(known),
            "production_writes": False, "live_verified": False}
