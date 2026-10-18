"""Read-only M3U inventory and integrity inspection, no network or writes."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

def inspect_playlist(path: Path) -> dict:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines or lines[0] != "#EXTM3U":
        raise ValueError("Invalid M3U header")
    channels = []
    pending = None
    for line in lines[1:]:
        if line.startswith("#EXTINF:"):
            if pending is not None:
                raise ValueError("EXTINF without URL")
            pending = line
        elif line.startswith("#"):
            continue
        else:
            if pending is None:
                raise ValueError("URL without EXTINF")
            channels.append({"metadata": pending, "url_sha256": hashlib.sha256(line.encode()).hexdigest()})
            pending = None
    if pending is not None:
        raise ValueError("Unpaired EXTINF")
    return {"sha256": hashlib.sha256(raw).hexdigest(), "channel_count": len(channels),
            "channels": channels, "read_only": True}

def compare_snapshots(before: dict, after: dict) -> dict:
    return {"identical": before["sha256"] == after["sha256"],
            "channel_count_unchanged": before["channel_count"] == after["channel_count"],
            "order_and_metadata_unchanged": before["channels"] == after["channels"]}
