"""Strict bounded parser shared by read-only K2 and K3 online pilots."""
from __future__ import annotations
import re


def parse_remote_m3u(raw: bytes, *, max_bytes: int) -> list[dict]:
    if not isinstance(raw, bytes) or len(raw) > max_bytes:
        raise ValueError("Remote playlist exceeds byte limit")
    text = raw.decode("utf-8-sig")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "#EXTM3U":
        raise ValueError("Invalid remote playlist header")
    rows = []
    pending = None
    for line in lines[1:]:
        line = line.strip()
        if line.startswith("#EXTINF:"):
            if pending is not None:
                raise ValueError("Unpaired channel metadata")
            parts = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', line, maxsplit=1)
            if len(parts) != 2 or not parts[1].strip():
                raise ValueError("Invalid EXTINF channel name")
            pending = parts[1].strip()
        elif line.startswith("#") or not line:
            continue
        else:
            if pending is None:
                raise ValueError("Stream URL without EXTINF")
            rows.append({"name": pending, "url": line})
            pending = None
    if pending is not None:
        raise ValueError("Unpaired channel metadata")
    return rows
