"""Fail-closed, read-only VOD/archive manifest equivalence; no filesystem writes."""
from __future__ import annotations

import re
import unicodedata

_DIGEST = re.compile(r"[0-9a-f]{64}\Z")


def _normalized_entries(manifest: object) -> dict[str, tuple[int, str, str, str]]:
    if type(manifest) is not dict or set(manifest) != {"entries"}:
        raise ValueError("Invalid VOD manifest")
    entries = manifest["entries"]
    if type(entries) is not list or not 1 <= len(entries) <= 10000:
        raise ValueError("Invalid VOD inventory size")
    result = {}
    portable = set()
    for item in entries:
        if type(item) is not dict or set(item) != {"path", "bytes", "sha256", "retention", "access"}:
            raise ValueError("Invalid VOD entry")
        path = item["path"]
        if (type(path) is not str or not 1 <= len(path) <= 4096 or
                path.startswith(("/", "~")) or "\\" in path or ":" in path or
                any(segment in ("", ".", "..") for segment in path.split("/")) or
                any(ord(ch) < 32 or ord(ch) == 127 or
                    unicodedata.category(ch) in ("Cf", "Cs") for ch in path)):
            raise ValueError("Unsafe VOD path")
        key = unicodedata.normalize("NFKC", path).casefold()
        if key in portable:
            raise ValueError("Duplicate or aliased VOD path")
        portable.add(key)
        size, digest = item["bytes"], item["sha256"]
        if type(size) is not int or size < 0 or type(digest) is not str or not _DIGEST.fullmatch(digest):
            raise ValueError("Invalid VOD hash or size")
        retention, access = item["retention"], item["access"]
        if (type(retention) is not str or not retention or len(retention) > 256 or
                type(access) is not str or not access or len(access) > 256):
            raise ValueError("Invalid VOD policy metadata")
        result[path] = (size, digest, retention, access)
    return result


def compare_vod_manifests(source: object, copy: object) -> dict:
    """Compare approved, precomputed manifests; never claim production acceptance."""
    left = _normalized_entries(source)
    right = _normalized_entries(copy)
    missing = sorted(set(left) - set(right))
    extra = sorted(set(right) - set(left))
    changed = sorted(path for path in left.keys() & right.keys() if left[path] != right[path])
    return {
        "equivalent": not (missing or extra or changed),
        "files_checked": len(left),
        "missing": missing,
        "extra": extra,
        "changed": changed,
        "production_vod_verified": False,
        "production_writes": False,
    }
