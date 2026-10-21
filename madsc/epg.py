"""Read-only playlist/XMLTV tvg-id matching validation."""
from __future__ import annotations
import re
import xml.etree.ElementTree as ET
from pathlib import Path

TVG_ID = re.compile(r'\btvg-id="([^"]*)"')

def check_epg_mapping(playlist: Path, xmltv: Path) -> dict:
    raw = playlist.read_bytes()
    text = raw.decode("utf-8-sig")
    if not text.lstrip().startswith("#EXTM3U"):
        raise ValueError("Invalid M3U8 playlist")
    ids = []
    for line in text.splitlines():
        if line.startswith("#EXTINF:"):
            match = TVG_ID.search(line)
            ids.append(match.group(1) if match else "")
    root = ET.fromstring(xmltv.read_bytes())
    if root.tag != "tv":
        raise ValueError("Expected XMLTV tv root")
    channel_ids = {node.attrib["id"] for node in root.findall("channel") if "id" in node.attrib}
    program_ids = {node.attrib["channel"] for node in root.findall("programme") if "channel" in node.attrib}
    missing = sorted(set(ids) - channel_ids - {""})
    return {"playlist_channels": len(ids), "missing_tvg_id": sum(not x for x in ids),
            "xmltv_channels": len(channel_ids), "unmatched_playlist_ids": missing,
            "unmatched_programme_ids": sorted(program_ids - channel_ids),
            "matching_verified": not missing and all(ids) and not (program_ids - channel_ids),
            "device_verified": False, "read_only": True}
