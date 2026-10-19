"""Isolated manifest checks: never overwrite or restore production files."""
from __future__ import annotations
import hashlib
from pathlib import Path

def snapshot_manifest(root: Path, paths: list[str]) -> dict:
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError("Backup root must be a real directory")
    base = root.resolve(strict=True)
    if (not isinstance(paths, list) or any(not isinstance(name, str) or not name for name in paths)
            or len(set(paths)) != len(paths)):
        raise ValueError("Backup paths must be unique nonempty strings")
    entries = []
    for name in sorted(paths):
        requested = Path(name)
        if (requested.is_absolute() or "\\" in name or
                any(part in ("", ".", "..") for part in name.split("/"))):
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
    if any(not isinstance(entry, dict) or not isinstance(entry.get("path"), str)
           or type(entry.get("bytes")) is not int or entry["bytes"] < 0
           or not isinstance(entry.get("sha256"), str) or len(entry["sha256"]) != 64
           or any(c not in "0123456789abcdef" for c in entry["sha256"])
           for entry in manifest["entries"]):
        raise ValueError("Invalid backup manifest entry")
    current = snapshot_manifest(root, [entry["path"] for entry in manifest["entries"]])
    return current["entries"] == manifest["entries"]


def compare_copy(source: Path, destination: Path, names: list[str]) -> bool:
    """Check independent sandbox copies without changing either directory."""
    first = snapshot_manifest(source, names)
    second = snapshot_manifest(destination, names)
    return first["entries"] == second["entries"]


def verify_sandbox_restore(source: Path, restored: Path, names: list[str]) -> dict:
    """Audit an already restored sandbox tree; never write to either tree."""
    valid = compare_copy(source, restored, names)
    return {"sandbox_restore_matches": valid, "files_checked": len(set(names)),
            "production_restore_verified": False, "production_writes": False}


def verify_independent_restore(source: Path, backup: Path, restored: Path,
                               names: list[str]) -> dict:
    """Compare three pre-existing independent trees; never perform restoration."""
    if (not isinstance(names, list) or not names or
            any(not isinstance(name, str) or not name for name in names) or
            len(set(names)) != len(names)):
        raise ValueError("Restore audit requires unique named files")
    if any(Path(path).is_symlink() or not Path(path).is_dir()
           for path in (source, backup, restored)):
        raise ValueError("Independent restore trees must be real directories")
    locations = [path.resolve(strict=True) for path in (source, backup, restored)]
    if len(set(locations)) != 3:
        raise ValueError("Source, backup and restored trees must be distinct")
    if any(a.is_relative_to(b) for a in locations for b in locations if a != b):
        raise ValueError("Nested trees are not independent")
    original = snapshot_manifest(source, names)
    backed_up = snapshot_manifest(backup, names)
    recovered = snapshot_manifest(restored, names)
    valid = original["entries"] == backed_up["entries"] == recovered["entries"]
    return {"independent_sandbox_restore_matches": valid,
            "files_checked": len(original["entries"]),
            "backup_verified_against_source": original["entries"] == backed_up["entries"],
            "restore_verified_against_backup": backed_up["entries"] == recovered["entries"],
            "external_storage_proven": False, "production_restore_verified": False,
            "production_writes": False}
