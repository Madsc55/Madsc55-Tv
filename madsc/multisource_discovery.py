"""K2 offline multi-source discovery registry: metadata only, no network or writes.

A public watch page is NOT permission to redistribute a stream.
"""
from __future__ import annotations

from hashlib import sha256
from urllib.parse import urlsplit
from madsc.discovery import normalize_url

SOURCE_KINDS = frozenset({"official_broadcaster", "licensed_m3u", "tv_directory",
                          "official_youtube", "licensed_free_platform"})
MAX_RECORDS = 20000


def evaluate_discovery(records: list[dict], existing_urls: set[str] | None = None) -> dict:
    """Return a review-only report. Never claim playback, resolution or licensing."""
    if type(records) is not list or len(records) > MAX_RECORDS:
        raise ValueError("Invalid discovery records")
    if existing_urls is not None and (not isinstance(existing_urls, (set, frozenset))
                                      or len(existing_urls) > MAX_RECORDS):
        raise ValueError("Invalid existing URL inventory")
    try:
        existing = {normalize_url(url) for url in (existing_urls or set())}
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid existing URL inventory") from exc
    seen: set[str] = set()
    proposals, duplicates, rejected = [], [], []
    for index, item in enumerate(records):
        try:
            if type(item) is not dict:
                raise ValueError("Record must be an object")
            name, kind, page = item["name"], item["source_kind"], item["source_page"]
            if type(name) is not str or not name.strip() or len(name) > 256:
                raise ValueError("Invalid channel name")
            if any(ord(c) < 32 or ord(c) == 127 or 0xD800 <= ord(c) <= 0xDFFF for c in name):
                raise ValueError("Invalid channel name")
            if type(kind) is not str or kind not in SOURCE_KINDS:
                raise ValueError("Unknown source category")
            page = normalize_url(page)
            if urlsplit(page).scheme != "https":
                raise ValueError("Evidence page must use HTTPS")
            # Source pages are evidence references, not playable media endpoints.
            raw_stream = item.get("stream_url")
            stream = normalize_url(raw_stream) if raw_stream is not None else None
            license_reference = item.get("license_reference")
            if license_reference is not None:
                license_reference = normalize_url(license_reference)
                if urlsplit(license_reference).scheme != "https":
                    raise ValueError("License reference must use HTTPS")
            rights_verified = item.get("redistribution_permission_verified", False)
            if type(rights_verified) is not bool:
                raise ValueError("Invalid rights verification flag")
            # A boolean assertion alone never upgrades evidence to verified rights.
            fingerprint = sha256((stream or page).encode("utf-8")).hexdigest()
            if fingerprint in seen or (stream is not None and stream in existing):
                duplicates.append({"index": index, "fingerprint": fingerprint,
                                   "reason": "duplicate_or_existing"})
                continue
            seen.add(fingerprint)
            proposals.append({
                "index": index, "name": name.strip(), "source_kind": kind,
                "source_page": page, "url_sha256": fingerprint,
                "stream_url": stream,
                "license_reference": license_reference,
                "redistribution_permission_claimed": rights_verified,
                "license_verified": False, "operator_independence_verified": False,
                "live_verified": False, "resolution_verified": False,
                "codec_verified": False, "drm_checked": False,
                "production_ready": False, "auto_add_allowed": False,
                "status": "REVIEW_REQUIRED",
            })
        except (KeyError, TypeError, ValueError) as exc:
            rejected.append({"index": index, "reason": str(exc)[:120]})
    return {"report_type": "offline_multisource_discovery",
            "candidates": proposals, "duplicates": duplicates,
            "rejected": rejected, "network_probed": False,
            "production_writes": False, "production_ready": False}
