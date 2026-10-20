"""Fail-closed read-only validation of independently supplied K2 history.

No fixture generation and no writes to production histories.
"""
import argparse
import json
from pathlib import Path

from madsc.history_pair_bridge import import_legacy_pair
from madsc.history_pair_store import KEYS


def publish_source(folder, output):
    folder, output = Path(folder), Path(output)
    if folder.is_symlink() or not folder.is_dir() or output.is_symlink():
        raise ValueError("Real source folder required; symlinks rejected")
    for name in KEYS:
        source = folder / name
        if source.is_symlink() or not source.is_file():
            raise ValueError("UNVERIFIED: missing independent history document")
        if source.stat().st_size > 8 * 1024 * 1024:
            raise ValueError("Oversized history document")
    # Verify structure before writing any evidence.
    pair = import_legacy_pair(folder)
    if output.exists():
        raise ValueError("Refusing to overwrite source evidence")
    output.mkdir(parents=True, exist_ok=False)
    for name in KEYS:
        with (output / name).open("xb") as handle:
            handle.write((folder / name).read_bytes())
    return {"source_files": list(KEYS), "production_writes": False,
            "real_source_independently_authenticated": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    print(json.dumps(publish_source(args.folder, args.output), sort_keys=True))


if __name__ == "__main__":
    main()
