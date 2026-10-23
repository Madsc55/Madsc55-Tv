"""Import channels from M3U/M3U8 text into a read-only candidate inventory."""
from __future__ import annotations
from pathlib import Path
import re
from madsc.discovery import classify_candidates

def extract_candidates(source: Path, known_urls: set[str] | None = None) -> dict:
    source = Path(source)
    if source.suffix.lower() not in (".m3u", ".m3u8"):
        raise ValueError("Only M3U and M3U8 playlists are supported")
    if source.is_symlink() or not source.is_file():
        raise ValueError("Invalid source file")
    import os
    import stat
    if not hasattr(os, "O_NOFOLLOW") or any(parent.is_symlink() for parent in source.absolute().parents):
        raise ValueError("Unsafe source path")
    fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_NONBLOCK", 0))
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > 16 * 1024 * 1024:
            raise ValueError("Invalid or oversized source file")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            raw = stream.read(16 * 1024 * 1024 + 1)
        if len(raw) > 16 * 1024 * 1024:
            raise ValueError("Source exceeds 16 MiB safety limit")
    finally:
        os.close(fd)
    lines = [x.strip() for x in raw.decode("utf-8-sig").splitlines() if x.strip()]
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
            if attrs.count('"') % 2:
                raise ValueError("Unbalanced EXTINF attribute quotes")
            # M3U metadata attributes must be unique case-insensitively. Picking
            # the first duplicate silently can bind a channel to the wrong EPG ID
            # or logo, so reject ambiguous rows before extracting any values.
            attr_names = re.findall(r'(?:^|\s)([\w-]+)="[^"]*"', attrs)
            folded_names = [name.casefold() for name in attr_names]
            if len(folded_names) != len(set(folded_names)):
                raise ValueError("Duplicate metadata attribute")
            match = re.search(r'(?:^|\s)tvg-id="([^"]*)"', attrs, flags=re.IGNORECASE)
            logo = re.search(r'(?:^|\s)tvg-logo="([^"]*)"', attrs, flags=re.IGNORECASE)
            group = re.search(r'(?:^|\s)group-title="([^"]*)"', attrs, flags=re.IGNORECASE)
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
    result["source_rows"] = rows
    result["source_format"] = source.suffix.lower()
    result["source_channel_count"] = len(rows)
    result["accepted_channel_count"] = len(result["candidates"])
    result["duplicate_channel_count"] = len(result["duplicates"])
    result["rejected_channel_count"] = len(result["rejected"])
    result["production_playlist_modified"] = False
    return result
