"""Deterministic, side-effect-free candidate deduplication and classification."""
from __future__ import annotations
from hashlib import sha256
from urllib.parse import urlsplit, urlunsplit

def normalize_url(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Candidate URL must be text")
    if any(ord(ch) < 32 or ord(ch) == 127 or 0xD800 <= ord(ch) <= 0xDFFF for ch in value) or "\\" in value:
        raise ValueError("Control characters or backslash escapes are forbidden in candidate URLs")
    value = value.strip()
    parts = urlsplit(value)
    if parts.scheme.lower() not in ("http", "https") or not parts.netloc or parts.username or parts.password:
        raise ValueError("Candidate must use HTTP(S) without embedded credentials")
    try:
        host = parts.hostname
        port = parts.port
    except ValueError as exc:
        raise ValueError("Invalid candidate host or port") from exc
    if not host or any(ch.isspace() for ch in parts.netloc) or port == 0:
        raise ValueError("Invalid candidate host or port")
    if parts.fragment:
        raise ValueError("URL fragments are not accepted")
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path or "/", parts.query, ""))

def classify_candidates(rows: list[dict], known_urls: set[str] | None = None) -> dict:
    if not isinstance(rows, list):
        raise ValueError("Candidate rows must be a list")
    if len(rows) > 20000:
        raise ValueError("Too many candidate rows")
    if known_urls is not None and not isinstance(known_urls, (set, frozenset)):
        raise ValueError("Known URLs must be a set")
    if known_urls is not None and len(known_urls) > 20000:
        raise ValueError("Too many known URLs")
    known = {normalize_url(x) for x in (known_urls or set())}
    seen = set()
    accepted, duplicates, rejected, alternatives = [], [], [], []
    identities = {}
    for index, item in enumerate(rows):
        try:
            url = normalize_url(item["url"])
            name = item["name"]
            if not isinstance(name, str) or any(ord(ch) < 32 or ord(ch) == 127 or 0xD800 <= ord(ch) <= 0xDFFF for ch in name):
                raise ValueError("Candidate name must be safe text")
            if "\\" in name:
                raise ValueError("Backslash escapes in channel names are forbidden")
            name = name.strip()
            if not name:
                raise ValueError("Empty name")
            key = sha256(url.encode("utf-8")).hexdigest()
            tvg_id = item.get("tvg_id", "")
            if not isinstance(tvg_id, str):
                raise ValueError("Invalid tvg-id")
            logo = item.get("tvg_logo", "")
            group = item.get("group_title", "")
            if not isinstance(logo, str) or not isinstance(group, str):
                raise ValueError("Invalid logo or group metadata")
            if any(ord(ch) < 32 or ord(ch) == 127 or 0xD800 <= ord(ch) <= 0xDFFF or ch == "\\" for value in (tvg_id, logo, group)
                   for ch in value):
                raise ValueError("Control characters in channel metadata")
            entry = {"name": name, "tvg_id": tvg_id.strip(), "tvg_logo": logo.strip(),
                     "group_title": group.strip(), "url_sha256": key,
                     "source_index": index, "status": "candidate_only"}
            if url in seen or url in known:
                duplicates.append({**entry, "duplicate_reason": "already_known" if url in known else "same_batch"})
            else:
                seen.add(url)
                identity = ("tvg_id", entry["tvg_id"].casefold()) if entry["tvg_id"] else ("name_group", entry["name"].casefold(), entry["group_title"].casefold())
                if identity in identities:
                    alternatives.append({**entry, "alternative_to_sha256": identities[identity]})
                else:
                    identities[identity] = key
                accepted.append(entry)
        except (KeyError, TypeError, ValueError, AttributeError) as exc:
            rejected.append({"source_index": index, "reason": str(exc)})
    return {"candidates": accepted, "duplicates": duplicates, "alternatives": alternatives, "rejected": rejected,
            "production_playlist_modified": False, "device_verified": False}
