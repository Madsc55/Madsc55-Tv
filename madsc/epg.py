"""Read-only playlist/XMLTV tvg-id matching validation."""
from __future__ import annotations
import re
import xml.etree.ElementTree as ET
from pathlib import Path

M3U_ATTRIBUTE = re.compile(r'(?:^|\s)([A-Za-z][\w-]*)="([^"]*)"(?=\s|$)')


def check_epg_mapping(playlist: Path, xmltv: Path) -> dict:
    """Validate playlist channel IDs against XMLTV channels and programme references.

    This is a structural/mapping check only; it does not prove that a player
    downloads or displays the EPG, nor does it modify either input.
    """
    raw = playlist.read_bytes()
    text = raw.decode("utf-8-sig")
    if "\x00" in text:
        raise ValueError("NUL byte in M3U8 playlist")
    if any(char in text for char in ("\u0085", "\u2028", "\u2029")):
        raise ValueError("Nonstandard line separator in M3U8 playlist")
    header = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if header != "#EXTM3U" and not header.startswith("#EXTM3U "):
        raise ValueError("Invalid M3U8 playlist")
    ids = []
    pending_stream = False
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("#EXTINF:"):
            if pending_stream:
                raise ValueError("M3U EXTINF missing stream URI")
            pending_stream = True
            # The channel-name separator is the first comma outside quoted attributes.
            quoted = False
            separator = None
            for position, char in enumerate(line):
                if char == '"':
                    quoted = not quoted
                elif char == "," and not quoted:
                    separator = position
                    break
            if separator is None or quoted:
                raise ValueError("Malformed M3U EXTINF: missing channel-name separator")
            if not line[separator + 1:].strip():
                raise ValueError("Malformed M3U EXTINF: empty channel name")
            attribute_text = line[:separator]
            if attribute_text.count('"') % 2:
                raise ValueError("Malformed M3U EXTINF: unbalanced quoted attribute")
            matches = [match.group(2) for match in M3U_ATTRIBUTE.finditer(attribute_text)
                       if match.group(1) == "tvg-id"
                       and attribute_text[:match.start(1)].count('"') % 2 == 0]
            declared = [match for match in re.finditer(r'(?:^|\s)tvg-id(?=\s|=)', attribute_text)
                        if attribute_text[:match.start()].count('"') % 2 == 0]
            if len(declared) != len(matches):
                raise ValueError("Malformed M3U tvg-id attribute")
            if len(matches) > 1:
                raise ValueError("Duplicate M3U tvg-id attribute")
            ids.append(matches[0].strip() if matches else "")
        elif pending_stream and line and not line.startswith("#"):
            if not line.startswith(("https://", "http://")):
                raise ValueError("M3U EXTINF invalid stream URI")
            pending_stream = False
    if pending_stream:
        raise ValueError("M3U EXTINF missing stream URI")
    if any(line.strip().startswith("#EXTINF") and not line.strip().startswith("#EXTINF:") for line in text.splitlines()):
        raise ValueError("Malformed M3U EXTINF directive")

    xmltv_raw = xmltv.read_bytes()
    if b"\x00" in xmltv_raw:
        raise ValueError("NUL byte in XMLTV")
    xmltv_upper = xmltv_raw.upper()
    if b"<!DOCTYPE" in xmltv_upper or b"<!ENTITY" in xmltv_upper:
        raise ValueError("XMLTV DTD and entity declarations are not allowed")
    root = ET.fromstring(xmltv_raw)
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

    seen_playlist_ids = set()
    duplicate_playlist_ids = set()
    for channel_id in ids:
        if not channel_id:
            continue
        if channel_id in seen_playlist_ids:
            duplicate_playlist_ids.add(channel_id)
        seen_playlist_ids.add(channel_id)
    duplicate_playlist_ids = sorted(duplicate_playlist_ids)
    missing = sorted(set(ids) - channel_ids - {""})
    unmatched_programmes = sorted(program_id for program_id in program_ids if program_id not in channel_ids)
    return {
        "playlist_channels": len(ids),
        "missing_tvg_id": sum(not channel_id for channel_id in ids),
        "xmltv_channels": len(channel_ids),
        "unmatched_playlist_ids": missing,
        "duplicate_playlist_ids": duplicate_playlist_ids,
        "unmatched_programme_ids": unmatched_programmes,
        "matching_verified": bool(ids) and not any(not channel_id for channel_id in ids)
            and not missing and not duplicate_playlist_ids and not unmatched_programmes,
        "device_verified": False,
        "read_only": True,
    }
