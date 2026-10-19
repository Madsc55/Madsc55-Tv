"""Read-only XMLTV channel and programme inventory for isolated EPG checks."""
from __future__ import annotations
from pathlib import Path
from xml.etree import ElementTree as ET


def inspect_xmltv(path: Path, playlist_ids: set[str]) -> dict:
    """Compare XMLTV channel IDs with explicitly supplied playlist IDs."""
    if not isinstance(playlist_ids, set) or any(not isinstance(x, str) for x in playlist_ids):
        raise ValueError("Invalid playlist channel IDs")
    root = ET.parse(path).getroot()
    if root.tag != "tv":
        raise ValueError("Not an XMLTV document")
    ids = [node.get("id") for node in root.findall("channel")]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError("Invalid or duplicate XMLTV channel ID")
    channels = set(ids)
    programmes = root.findall("programme")
    orphaned = sum(1 for item in programmes if item.get("channel") not in channels)
    return {"xmltv_channels": len(channels), "programmes": len(programmes),
            "matched_playlist_ids": len(channels & playlist_ids),
            "unmatched_playlist_ids": sorted(playlist_ids - channels),
            "orphaned_programmes": orphaned, "device_verified": False,
            "production_writes": False}
