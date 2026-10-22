"""K5 offline M3U previews from K2/K3 catalog; never write live playlists."""
from __future__ import annotations

from madsc.discovery import normalize_url
from hashlib import sha256

BUCKETS = ("IBO_ONAYLI_CALISAN", "CALISAN_ADAY", "CALISMAYAN_ADAY",
           "YABANCI", "TEST_BEKLIYOR")


def _attribute(value: str) -> str:
    if not isinstance(value, str) or any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        raise ValueError("Unsafe M3U metadata")
    return value.replace("&", "&amp;").replace('"', "&quot;")


def render_playlist_previews(catalog: dict, source_rows: list[dict]) -> dict:
    """Return separate in-memory drafts; never treat preliminary tests as acceptance."""
    if not isinstance(catalog, dict) or not isinstance(source_rows, list):
        raise ValueError("Invalid catalog or source rows")
    if catalog.get("production_writes") is not False or catalog.get("production_ready") is not False:
        raise ValueError("Playlist preview requires a read-only, non-production catalog")
    entries = catalog.get("channels")
    if not isinstance(entries, list):
        raise ValueError("Missing catalog channels")
    output = {bucket: ["#EXTM3U"] for bucket in BUCKETS}
    seen_indices = set()
    seen_digests = set()
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("bucket") not in output:
            raise ValueError("Unknown channel category")
        index = entry.get("source_index")
        if type(index) is not int or not 0 <= index < len(source_rows):
            raise ValueError("Invalid source reference")
        if index in seen_indices:
            raise ValueError("Duplicate catalog source reference")
        seen_indices.add(index)
        source = source_rows[index]
        if not isinstance(source, dict):
            raise ValueError("Invalid source row")
        url = normalize_url(source["url"])
        digest = sha256(url.encode("utf-8")).hexdigest()
        if digest != entry.get("url_sha256"):
            raise ValueError("Catalog and source fingerprint mismatch")
        if digest in seen_digests:
            raise ValueError("Duplicate stream in playlist preview")
        seen_digests.add(digest)
        for key in ("display_name", "tvg_id", "group_title"):
            if not isinstance(entry.get(key), str):
                raise ValueError("Invalid channel metadata")
        name = entry["display_name"]
        if not isinstance(name, str) or not name or any(ord(ch) < 32 or ord(ch) == 127 for ch in name):
            raise ValueError("Unsafe channel name")
        if "," in name or "\r" in name or "\n" in name:
            raise ValueError("Unsafe M3U channel delimiter")
        logo = entry.get("logo_url") or ""
        if logo and (entry.get("logo_verified") is not True or
                     not isinstance(logo, str) or not logo.startswith("https://")):
            raise ValueError("Unverified logo")
        attrs = (f'tvg-id="{_attribute(entry["tvg_id"])}" '
                 f'tvg-logo="{_attribute(logo)}" '
                 f'group-title="{_attribute(entry["group_title"])}"')
        output[entry["bucket"]].extend([f"#EXTINF:-1 {attrs},{name}", url])
    return {"drafts": {bucket: "\n".join(lines) + "\n" for bucket, lines in output.items()},
            "counts": {bucket: (len(lines) - 1) // 2 for bucket, lines in output.items()},
            "preview_only": True, "device_verified_by_this_function": False,
            "production_writes": False, "production_change_allowed": False}
