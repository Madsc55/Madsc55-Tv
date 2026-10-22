"""MADSC55-TV: fail-closed protection for isolated automation output."""
from __future__ import annotations
import argparse
import json
import os
import stat
import unicodedata
from pathlib import Path
from madsc.write_path_audit import audit_write_paths

PROTECTED = {"calisanlar.m3u", "yeniler", "yedekler", "hepsi", "favoriler", "epg", "logolar", "arsiv", "playlist.m3u8", "xmltv.xml", "yeni̇ler"}
def safe_relative_path(raw: str) -> bool:
    if not isinstance(raw, str) or not raw or any(ord(ch) < 32 or ord(ch) == 127 for ch in raw):
        return False
    if "\\" in raw:
        return False
    p = Path(raw)
    if p.is_absolute() or not p.parts or ".." in p.parts or any(part in ("", ".") for part in p.parts):
        return False
    parts = [x.casefold() for x in p.parts]
    if ":" in raw or raw.startswith(("//", "\\\\")):
        return False
    if audit_write_paths([raw])["blocked"]:
        return False
    return not any(any(token in part for token in PROTECTED) for part in parts)

def validate_manifest(manifest: dict) -> None:
    if not isinstance(manifest, dict):
        raise ValueError("Manifest must be an object")
    if manifest.get("production_write") is not False:
        raise ValueError("production writes are prohibited")
    paths = manifest.get("output_paths")
    if not isinstance(paths, list) or not paths:
        raise ValueError("explicit nonempty output_paths required")
    if not all(isinstance(p, str) for p in paths):
        raise ValueError("Output paths must be strings")
    normalized = [unicodedata.normalize("NFKC", p).casefold() for p in paths]
    if len(normalized) != len(set(normalized)):
        raise ValueError("Duplicate output paths")
    if any(not isinstance(p, str) or not safe_relative_path(p) or not p.replace("\\", "/").startswith("artifacts/") for p in paths):
        raise ValueError("outputs must stay under artifacts/ and outside protected paths")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    # Open once without following a final-component symlink. Inspect and read
    # the same descriptor to avoid a path-swap between validation and reading.
    try:
        fd = os.open(args.manifest, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
        with os.fdopen(fd, "rb") as stream:
            metadata = os.fstat(stream.fileno())
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > 1024 * 1024:
                parser.error("Manifest must be a regular file no larger than 1 MiB")
            payload = stream.read(1024 * 1024 + 1)
            if len(payload) > 1024 * 1024:
                parser.error("Manifest exceeds 1 MiB limit")
    except OSError as exc:
        parser.error(f"Cannot safely open manifest: {exc.strerror}")
    try:
        manifest = json.loads(payload.decode("utf-8"))
        validate_manifest(manifest)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        parser.error(f"Invalid or unsafe manifest: {exc}")
    print("K1 read-only output gate: PASS")

if __name__ == "__main__":
    main()
