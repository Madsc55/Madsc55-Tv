"""K5: offline preview of an IBO archive manifest; never writes playlists.

The original positions are the sole keys. URL/playback validation is deliberately
outside this module and remains subject to final user device verification.
"""
from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from urllib.parse import urlsplit

from madsc.isolated_ibo_classification import classify_6115_positions


def build_6115_archive_preview(urls: Sequence[str]) -> dict:
    """Return JSON-safe metadata for a complete ordered fixture; no I/O.

    Refuse missing, duplicated, non-HTTPS or ambiguous URL entries to avoid
    silently accepting a shifted playlist. This is not a network probe.
    """
    if not isinstance(urls, (list, tuple)) or len(urls) != 6115:
        raise ValueError("Expected exactly 6115 ordered URL entries")
    seen: set[str] = set()
    for url in urls:
        if not isinstance(url, str):
            raise ValueError("Unsafe, missing or duplicate URL in ordered fixture")
        try:
            parsed = urlsplit(url)
            port = parsed.port  # Reject malformed or out-of-range explicit ports.
        except ValueError as exc:
            raise ValueError("Unsafe, missing or duplicate URL in ordered fixture") from exc
        if (parsed.scheme != "https" or not parsed.hostname or port == 0
                or parsed.username is not None or parsed.password is not None
                or parsed.fragment or url != url.strip()
                or any(ch.isspace() or ord(ch) < 32 or ord(ch) == 127 for ch in url)
                or url in seen):
            raise ValueError("Unsafe, missing or duplicate URL in ordered fixture")
        seen.add(url)
    decisions = classify_6115_positions(len(urls))
    archived = [d.original_position for d in decisions if d.action == "ARSIV_ONIZLEME"]
    retained = [d.original_position for d in decisions if d.action == "KALDI"]
    digest = hashlib.sha256(
        json.dumps(urls, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "preview_only": True,
        "production_writes": False,
        "production_ready": False,
        "device_verified": False,
        "source_count": len(urls),
        "source_order_sha256": digest,
        "archived_original_positions": archived,
        "retained_original_positions": retained,
        "archive_count": len(archived),
        "retained_count": len(retained),
    }
