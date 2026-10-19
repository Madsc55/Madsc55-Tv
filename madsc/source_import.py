"""Import channels from M3U/M3U8 text into a read-only candidate inventory."""
from __future__ import annotations
from pathlib import Path
import re
from madsc.discovery import classify_candidates

def extract_candidates(source: Path, known_urls: set[str] | None = None) -> dict:
    if source.suffix.lower() not in (".m3u", ".m3u8"):
        raise ValueError("Only M3U and M3U8 playlists are supported")
    lines = [x.strip() for x in source.read_text(encoding="utf-8-sig").splitlines() if x.strip()]
    if not lines or lines[0] != "#EXTM3U":
        raise ValueError("Invalid playlist header")
    rows = []
    pending = None
    for line in lines[1:]:
        if line.startswith("#EXTINF:"):
            if pending is not None:
                raise ValueError("Unpaired channel metadata")
            parts = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', line, maxsplit=1)
            if len(parts) != 2:
                raise ValueError("Invalid EXTINF metadata")
            attrs, channel_name = parts[0], parts[1].strip()
            match = re.search(r'(?:^|\s)tvg-id="([^"]*)"', attrs)
            logo = re.search(r'(?:^|\s)tvg-logo="([^"]*)"', attrs)
            group = re.search(r'(?:^|\s)group-title="([^"]*)"', attrs)
            pending = {"name": channel_name, "tvg_id": match.group(1) if match else "",
                       "tvg_logo": logo.group(1) if logo else "",
                       "group_title": group.group(1) if group else ""}
            if not channel_name:
                raise ValueError("Empty channel name")
        elif line.startswith("#"):
            continue
        else:
            if pending is None:
                raise ValueError("Channel URL without metadata")
            rows.append({**pending, "url": line})
            pending = None
    if pending is not None:
        raise ValueError("Missing channel URL")
    result = classify_candidates(rows, known_urls)
    result["source_format"] = source.suffix.lower()
    result["source_channel_count"] = len(rows)
    result["accepted_channel_count"] = len(result["candidates"])
    result["duplicate_channel_count"] = len(result["duplicates"])
    result["rejected_channel_count"] = len(result["rejected"])
    result["production_playlist_modified"] = False
    return result
