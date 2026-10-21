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
        if any(ord(c) < 32 or ord(c) == 127 for c in name) or ":" in name or name.startswith("~"):
            raise ValueError("Unsafe backup source path")
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
        digest = hashlib.sha256()
        size = 0
        with candidate.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
                size += len(chunk)
        entries.append({"path": candidate.relative_to(base).as_posix(),
                        "bytes": size, "sha256": digest.hexdigest()})
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
    paths = [entry["path"] for entry in manifest["entries"]]
    if len(set(paths)) != len(paths):
        raise ValueError("Duplicate backup manifest paths")
    # A manifest is a canonical snapshot, not an arbitrary subset or reordered list.
    if paths != sorted(paths):
        return False
    if not paths:
        return False
    current = snapshot_manifest(root, paths)
    return current["entries"] == manifest["entries"]


def compare_copy(source: Path, destination: Path, names: list[str]) -> bool:
    """Check independent sandbox copies without changing either directory."""
    if not isinstance(names, list) or not names:
        raise ValueError("Copy audit requires a nonempty file list")
    roots = [Path(source), Path(destination)]
    if any(root.is_symlink() or not root.is_dir() for root in roots):
        raise ValueError("Copy audit requires real directories")
    resolved = [root.resolve(strict=True) for root in roots]
    if (resolved[0] == resolved[1] or
            resolved[0].is_relative_to(resolved[1]) or
            resolved[1].is_relative_to(resolved[0])):
        raise ValueError("Copy audit requires independent nonnested directories")
    # Separate directories are insufficient if their files share inodes.
    for name in names:
        left = (resolved[0] / name).stat()
        right = (resolved[1] / name).stat()
        if (left.st_dev, left.st_ino) == (right.st_dev, right.st_ino):
            raise ValueError("Copy audit requires physically independent files")
    first = snapshot_manifest(source, names)
    second = snapshot_manifest(destination, names)
    return first["entries"] == second["entries"]


def verify_sandbox_restore(source: Path, restored: Path, names: list[str]) -> dict:
    """Audit an already restored sandbox tree; never write to either tree."""
    if not isinstance(names, list) or not names:
        raise ValueError("Sandbox restore audit requires named files")
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
    # Distinct directories may still share inode-backed files via hard links.
    # A backup must not be able to change when the source is modified.
    for name in names:
        stats = [(root / name).stat() for root in locations]
        identities = [(item.st_dev, item.st_ino) for item in stats]
        if len(set(identities)) != 3:
            raise ValueError("Independent restore trees must not share hard-linked files")
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


def restore_to_new_sandbox(backup: Path, destination: Path, names: list[str]) -> dict:
    """Restore a verified backup into a newly created sandbox, never production.

    The destination must not exist. A failed copy removes only this new tree.
    """
    import shutil

    backup = Path(backup)
    destination = Path(destination)
    if not isinstance(names, list) or not names:
        raise ValueError("Sandbox restore requires a nonempty file list")
    original = snapshot_manifest(backup, names)
    if destination.is_symlink() or destination.exists():
        raise ValueError("Restore destination must not exist")
    parent = destination.parent
    if parent.is_symlink() or not parent.is_dir():
        raise ValueError("Restore parent must be a real directory")
    source_root = backup.resolve(strict=True)
    target_root = destination.resolve(strict=False)
    if target_root == source_root or target_root.is_relative_to(source_root):
        raise ValueError("Restore destination must be outside backup tree")
    if source_root.is_relative_to(target_root):
        raise ValueError("Restore destination must not contain backup tree")
    destination.mkdir()
    try:
        for entry in original["entries"]:
            relative = Path(entry["path"])
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with (backup / relative).open("rb") as reader, target.open("xb") as writer:
                shutil.copyfileobj(reader, writer, length=1024 * 1024)
        if not verify_manifest(backup, original) or not verify_manifest(destination, original):
            raise ValueError("Backup changed or sandbox restore failed integrity verification")
    except BaseException:
        shutil.rmtree(destination)
        raise
    return {"sandbox_restore_matches": True, "files_restored": len(original["entries"]),
            "external_storage_proven": False, "production_restore_verified": False,
            "production_writes": False}
