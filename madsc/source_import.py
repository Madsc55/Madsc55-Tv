"""Import channels from M3U/M3U8 text into a read-only candidate inventory."""
from __future__ import annotations
from pathlib import Path
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
            pending = line.rsplit(",", 1)[-1].strip()
        elif line.startswith("#"):
            continue
        else:
            if pending is None:
                raise ValueError("Channel URL without metadata")
            rows.append({"name": pending, "url": line})
            pending = None
    if pending is not None:
        raise ValueError("Missing channel URL")
    result = classify_candidates(rows, known_urls)
    result["source_format"] = source.suffix.lower()
    result["production_playlist_modified"] = False
    return result
