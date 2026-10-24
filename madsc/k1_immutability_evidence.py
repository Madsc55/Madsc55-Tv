"""Read-only K1 protected-file snapshot comparison.

This does not enforce immutability; it measures before/after evidence.
"""
from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def _snapshot_one(root: Path, rel: str) -> dict:
    if not isinstance(rel, str) or not rel or rel.startswith("/") or "\\" in rel:
        raise ValueError("Invalid protected path")
    parts = Path(rel).parts
    if any(p in (".", "..") for p in parts):
        raise ValueError("Unsafe protected path")
    target = root.joinpath(*parts)
    if not target.is_relative_to(root):
        raise ValueError("Path escapes root")
    for item in (root, *(root.joinpath(*parts[:i]) for i in range(1, len(parts) + 1))):
        if item.is_symlink():
            raise ValueError("Protected path includes symlink")
    info = target.lstat()
    if not stat.S_ISREG(info.st_mode):
        raise ValueError("Protected path is not a regular file")
    with target.open("rb") as handle:
        before = os.fstat(handle.fileno())
        if not stat.S_ISREG(before.st_mode) or (before.st_dev, before.st_ino) != (info.st_dev, info.st_ino):
            raise ValueError("Protected file changed during opening")
        digest = hashlib.sha256()
        while True:
            block = handle.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
        after = os.fstat(handle.fileno())
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
            after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns
        ):
            raise ValueError("Protected file changed during hashing")
    return {"path": rel, "sha256": digest.hexdigest(), "size": after.st_size,
            "mode": stat.S_IMODE(after.st_mode), "device": after.st_dev,
            "inode": after.st_ino, "mtime_ns": after.st_mtime_ns}


def snapshot(root: str | Path, protected_paths: list[str]) -> dict:
    supplied_root = Path(root)
    if supplied_root.is_symlink():
        raise ValueError("Root must not be a symlink")
    root = supplied_root.resolve(strict=True)
    if not root.is_dir() or not isinstance(protected_paths, list) or not protected_paths:
        raise ValueError("Root and nonempty protected file list required")
    if len(protected_paths) > 10000 or len(protected_paths) != len(set(protected_paths)):
        raise ValueError("Duplicate or excessive protected paths")
    return {"schema": "k1_protected_snapshot_v1", "root": str(root),
            "files": [_snapshot_one(root, rel) for rel in sorted(protected_paths)]}


def compare(before: dict, after: dict) -> dict:
    if before.get("schema") != "k1_protected_snapshot_v1" or after.get("schema") != before["schema"]:
        raise ValueError("Invalid snapshot schema")
    if before.get("root") != after.get("root"):
        raise ValueError("Snapshot root changed")
    a, b = before.get("files"), after.get("files")
    if not isinstance(a, list) or not isinstance(b, list) or not a or not b:
        raise ValueError("Missing protected-file evidence")
    if any(not isinstance(x, dict) or not isinstance(x.get("path"), str) for x in a + b):
        raise ValueError("Malformed protected-file evidence")
    if len({x["path"] for x in a}) != len(a) or len({x["path"] for x in b}) != len(b):
        raise ValueError("Duplicate protected-file evidence")
    unchanged = a == b
    return {"unchanged": unchanged, "files_checked": len(a), "before": a,
            "after": b, "production_acceptance": False}


def write_report(path: str | Path, result: dict) -> None:
    path = Path(path)
    if path.is_symlink():
        raise ValueError("Report destination is a symlink")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
