"""Read-only playlist/XMLTV tvg-id matching validation."""
from __future__ import annotations
import re
import xml.etree.ElementTree as ET
from pathlib import Path

TVG_ID = re.compile(r'\btvg-id="([^"]*)"')


def check_epg_mapping(playlist: Path, xmltv: Path) -> dict:
    """Validate playlist channel IDs against XMLTV channels and programme references.

    This is a structural/mapping check only; it does not prove that a player
    downloads or displays the EPG, nor does it modify either input.
    """
    raw = playlist.read_bytes()
    text = raw.decode("utf-8-sig")
    if not text.lstrip().startswith("#EXTM3U"):
        raise ValueError("Invalid M3U8 playlist")
    ids = []
    for line in text.splitlines():
        if line.startswith("#EXTINF:"):
            matches = TVG_ID.findall(line)
            if len(matches) > 1:
                raise ValueError("Duplicate M3U tvg-id attribute")
            ids.append(matches[0].strip() if matches else "")

    root = ET.fromstring(xmltv.read_bytes())
    if root.tag != "tv":
        raise ValueError("Expected XMLTV tv root")
    raw_channel_ids = [node.attrib.get("id", "").strip() for node in root.findall("channel")]
    if any(not channel_id for channel_id in raw_channel_ids):
        raise ValueError("XMLTV channel is missing a nonempty id")
    if len(raw_channel_ids) != len(set(raw_channel_ids)):
        raise ValueError("Duplicate XMLTV channel id")
    channel_ids = set(raw_channel_ids)

    program_ids = set()
    for programme in root.findall("programme"):
        channel_id = programme.attrib.get("channel", "").strip()
        if not channel_id:
            raise ValueError("XMLTV programme is missing a nonempty channel")
        program_ids.add(channel_id)

    missing = sorted(set(ids) - channel_ids - {""})
    unmatched_programmes = sorted(program_id for program_id in program_ids if program_id not in channel_ids)
    return {
        "playlist_channels": len(ids),
        "missing_tvg_id": sum(not channel_id for channel_id in ids),
        "xmltv_channels": len(channel_ids),
        "unmatched_playlist_ids": missing,
        "unmatched_programme_ids": unmatched_programmes,
        "matching_verified": bool(ids) and not any(not channel_id for channel_id in ids)
            and not missing and not unmatched_programmes,
        "device_verified": False,
        "read_only": True,
    }
