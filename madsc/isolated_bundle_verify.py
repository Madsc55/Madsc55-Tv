"""Verify isolated K5 M3U artifacts against their SHA-256 manifest."""
from __future__ import annotations
import argparse
import hashlib
import json
import stat
from pathlib import Path
from madsc.playlist_previews import BUCKETS

EXPECTED = frozenset(bucket + ".m3u" for bucket in BUCKETS)
MAX_FILE_BYTES = 16_000_000


def _regular_file(path: Path) -> bool:
    if path.is_symlink():
        return False
    try:
        mode = path.lstat()
    except OSError:
        return False
    return stat.S_ISREG(mode.st_mode) and mode.st_nlink == 1


def verify_bundle(directory: Path) -> dict:
    directory = Path(directory)
    errors = []
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError("Invalid isolated bundle directory")
    for ancestor in (directory, *directory.parents):
        if ancestor.is_symlink():
            raise ValueError("Symlinked bundle ancestor")
    manifest_path = directory / "manifest.json"
    if not _regular_file(manifest_path) or manifest_path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError("Invalid manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (not isinstance(manifest, dict) or manifest.get("production_ready") is not False
            or manifest.get("production_writes") is not False
            or manifest.get("preview_only") is not True):
        raise ValueError("Manifest must explicitly forbid production acceptance")
    files = manifest.get("files")
    if not isinstance(files, dict) or set(files) != EXPECTED:
        raise ValueError("Unexpected manifest file set")
    if set(x.name for x in directory.iterdir()) != EXPECTED | {"manifest.json"}:
        errors.append("unexpected_directory_entries")
    counts = manifest.get("counts")
    if not isinstance(counts, dict) or set(counts) != set(BUCKETS):
        raise ValueError("Invalid manifest counts")
    for name in sorted(EXPECTED):
        meta = files[name]
        path = directory / name
        if not isinstance(meta, dict) or not _regular_file(path):
            errors.append(name + ":invalid_file")
            continue
        size = path.stat().st_size
        if size > MAX_FILE_BYTES or size != meta.get("bytes"):
            errors.append(name + ":size_mismatch")
            continue
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != meta.get("sha256"):
            errors.append(name + ":digest_mismatch")
        if not data.startswith(b"#EXTM3U\\n"):
            errors.append(name + ":invalid_header")
        bucket = name[:-4]
        if meta.get("channels") != counts[bucket] or type(meta.get("channels")) is not int:
            errors.append(name + ":count_mismatch")
        if data.count(b"#EXTINF:") != meta.get("channels"):
            errors.append(name + ":playlist_count_mismatch")
    return {"verified": not errors, "errors": errors, "files_checked": len(EXPECTED),
            "production_ready": False, "production_writes": False}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Verify isolated K5 playlist bundle")
    parser.add_argument("directory", type=Path)
    args = parser.parse_args(argv)
    result = verify_bundle(args.directory)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
