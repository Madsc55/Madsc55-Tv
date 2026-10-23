"""Offline K3 XMLTV audit. Does not write playlists or fetch network resources."""
import argparse
import json
from pathlib import Path

from madsc.trial_epg_matching import programme_coverage


def audit(playlist, xmltv):
    rows = programme_coverage(playlist, xmltv)
    counts = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    return {
        "total": len(rows),
        "empty_tvg_id": sum(not row["old_id"] for row in rows),
        "statuses": counts,
        "matched_with_programmes": sum(row["has_programmes"] for row in rows),
        "matched_without_programmes": sum(
            bool(row["matched_id"]) and not row["has_programmes"] for row in rows
        ),
        "channels": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--playlist", type=Path, required=True)
    parser.add_argument("--xmltv", type=Path, required=True)
    parser.add_argument("--max-bytes", type=int, default=50_000_000)
    args = parser.parse_args()
    if args.max_bytes <= 0:
        parser.error("--max-bytes must be positive")
    for path in (args.playlist, args.xmltv):
        if path.is_symlink() or not path.is_file():
            parser.error("inputs must be regular non-symlink files")
        if path.stat().st_size > args.max_bytes:
            parser.error("input exceeds size limit")
    result = audit(args.playlist.read_text(encoding="utf-8"),
                   args.xmltv.read_bytes())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
