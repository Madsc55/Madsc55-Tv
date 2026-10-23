"""Read-only legacy M3U8 migration preview; never alters old or production files."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from madsc.legacy_category_order import load_historical_categories

SOURCE_FILES = ("CALISANLAR.m3u", "YABANCI_KANALLAR.m3u", "YENILER.m3u")
MAX_BYTES = 2_000_000


def build_legacy_m3u8_preview(source_dir: Path, snapshot: Path | None = None) -> dict:
    """Join historical metadata to original M3U by source order, without probing URLs."""
    source_dir = Path(source_dir)
    if not source_dir.is_dir() or source_dir.is_symlink():
        raise ValueError("Source must be a regular directory")
    data = load_historical_categories() if snapshot is None else load_historical_categories(snapshot)
    manifests = {item["file"]: item for item in data["source_files"]}
    drafts = []
    counts = {}
    for filename in SOURCE_FILES:
        path = source_dir / filename
        if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_BYTES:
            raise ValueError("Missing, symlinked or oversized source: " + filename)
        raw = path.read_bytes()
        if len(raw) > MAX_BYTES or hashlib.sha1(raw).hexdigest() != manifests[filename]["sha"]:
            raise ValueError("Legacy source SHA mismatch: " + filename)
        content = raw.decode("utf-8-sig")
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        if not lines or not (lines[0] == "#EXTM3U" or lines[0].startswith("#EXTM3U ")):
            raise ValueError("Invalid M3U header: " + filename)
        if not drafts:\n            drafts.append(lines[0])\n        entries = []
        pending = None
        for line in lines[1:]:
            if line.startswith("#EXTINF:"):
                if pending is not None:
                    raise ValueError("Missing stream URL: " + filename)
                pending = line
            elif line.startswith("#"):
                continue
            else:
                if pending is None or not line.startswith(("https://", "http://")) or any(ord(c) < 32 for c in line):
                    raise ValueError("Invalid stream URL: " + filename)
                entries.append((pending, line))
                pending = None
        if pending is not None or len(entries) != manifests[filename]["count"]:
            raise ValueError("Legacy M3U count mismatch: " + filename)
        for row, (extinf, url) in zip((x for x in data["entries"] if x["file"] == filename), entries):
            # Keep the exact source EXTINF attributes and original URL; never invent a verified status.
            drafts.extend((extinf, url))
        counts[filename] = len(entries)
    return {"playlist_m3u8": "\n".join(drafts) + "\n",
            "counts": counts, "historical_only": True, "network_probed": False,
            "production_ready": False, "production_writes": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Print verified legacy M3U8 preview to stdout")
    parser.add_argument("source_dir", type=Path)
    args = parser.parse_args(argv)
    print(build_legacy_m3u8_preview(args.source_dir)["playlist_m3u8"], end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
