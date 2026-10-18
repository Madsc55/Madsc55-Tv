"""MADSC55-TV: fail-closed protection for isolated automation output."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

PROTECTED = {"calisanlar.m3u", "yeniler", "yedekler", "hepsi", "favoriler", "epg", "logolar", "arsiv"}
def safe_relative_path(raw: str) -> bool:
    p = Path(raw.replace("\\", "/"))
    if p.is_absolute() or not p.parts or ".." in p.parts:
        return False
    parts = [x.casefold() for x in p.parts]
    return not any(any(token in part for token in PROTECTED) for part in parts)

def validate_manifest(manifest: dict) -> None:
    if manifest.get("production_write") is not False:
        raise ValueError("production writes are prohibited")
    paths = manifest.get("output_paths")
    if not isinstance(paths, list) or not paths:
        raise ValueError("explicit nonempty output_paths required")
    if any(not isinstance(p, str) or not safe_relative_path(p) or not p.startswith("artifacts/") for p in paths):
        raise ValueError("outputs must stay under artifacts/ and outside protected paths")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    validate_manifest(json.loads(args.manifest.read_text(encoding="utf-8")))
    print("K1 read-only output gate: PASS")

if __name__ == "__main__":
    main()
