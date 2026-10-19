"""Isolated manifest checks: never overwrite or restore production files."""
from __future__ import annotations
import hashlib
from pathlib import Path

def snapshot_manifest(root: Path, paths: list[str]) -> dict:
    base = root.resolve(strict=True)
    entries = []
    for name in sorted(set(paths)):
        requested = Path(name)
        if requested.is_absolute() or ".." in requested.parts:
            raise ValueError("Unsafe backup source path")
        candidate = base / requested
        for parent in (base, *(base / Path(*requested.parts[:i]) for i in range(1, len(requested.parts) + 1))):
            if parent.is_symlink():
                raise ValueError("Symlink in backup source path is not permitted")
        candidate = candidate.resolve(strict=True)
        if not candidate.is_relative_to(base) or not candidate.is_file():
            raise ValueError("Backup source must be a regular file within root")
        raw = candidate.read_bytes()
        entries.append({"path": candidate.relative_to(base).as_posix(),
                        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    return {"entries": entries, "mode": "manifest_only", "external_backup_verified": False,
            "restore_verified": False, "production_writes": False}

def verify_manifest(root: Path, manifest: dict) -> bool:
    if not isinstance(manifest, dict) or not isinstance(manifest.get("entries"), list):
        raise ValueError("Invalid backup manifest")
    if any(not isinstance(entry, dict) or not isinstance(entry.get("path"), str) for entry in manifest["entries"]):
        raise ValueError("Invalid backup manifest entry")
    current = snapshot_manifest(root, [entry["path"] for entry in manifest["entries"]])
    return current["entries"] == manifest["entries"]
