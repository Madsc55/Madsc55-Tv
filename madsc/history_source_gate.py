"""Fail-closed real K2 history input gate.

Fixture mode is explicitly separate from verified source mode. No network or writes.
"""
import hashlib
import json
from pathlib import Path

from madsc.history_pair_bridge import import_legacy_pair
from madsc.history_pair_store import KEYS


def load_verified_source(folder, manifest_path, *, run_id, commit_sha):
    folder, manifest_path = Path(folder), Path(manifest_path)
    if folder.is_symlink() or manifest_path.is_symlink() or not manifest_path.is_file():
        raise ValueError("Missing or symlinked history source/manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or set(manifest) != {
            "schema", "mode", "source_run_id", "source_commit_sha", "hashes",
            "production_writes"}:
        raise ValueError("Invalid source manifest")
    if (manifest["schema"] != 1 or manifest["mode"] != "VERIFIED_SOURCE"
            or manifest["source_run_id"] != run_id
            or manifest["source_commit_sha"] != commit_sha
            or manifest["production_writes"] is not False
            or not isinstance(manifest["hashes"], dict)
            or set(manifest["hashes"]) != set(KEYS)):
        raise ValueError("Source provenance mismatch or fixture source")
    for name in KEYS:
        path = folder / name
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 8 * 1024 * 1024:
            raise ValueError("Unsafe history source file")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != manifest["hashes"][name]:
            raise ValueError("History source SHA256 mismatch")
    return import_legacy_pair(folder)
