"""Deterministic, side-effect-free candidate deduplication and classification."""
from __future__ import annotations
from hashlib import sha256
from urllib.parse import urlsplit, urlunsplit

def normalize_url(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Candidate URL must be text")
    value = value.strip()
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        raise ValueError("Control characters are forbidden in candidate URLs")
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
    known = {normalize_url(x) for x in (known_urls or set())}
    seen = set()
    accepted, duplicates, rejected = [], [], []
    if not isinstance(rows, list):
        raise ValueError("Candidate rows must be a list")
    for index, item in enumerate(rows):
        try:
            url = normalize_url(item["url"])
            name = item["name"]
            if not isinstance(name, str):
                raise ValueError("Candidate name must be text")
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
            entry = {"name": name, "tvg_id": tvg_id.strip(), "tvg_logo": logo.strip(),
                     "group_title": group.strip(), "url_sha256": key,
                     "source_index": index, "status": "candidate_only"}
            if url in seen or url in known:
                duplicates.append(entry)
            else:
                seen.add(url)
                accepted.append(entry)
        except (KeyError, TypeError, ValueError, AttributeError) as exc:
            rejected.append({"source_index": index, "reason": str(exc)})
    return {"candidates": accepted, "duplicates": duplicates, "rejected": rejected,
            "production_playlist_modified": False, "device_verified": False}
