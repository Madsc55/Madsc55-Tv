"""Isolated manifest checks: never overwrite or restore production files."""
from __future__ import annotations
import hashlib
import os
import stat
from pathlib import Path
from madsc.write_path_audit import enforce_local_output_path


def _open_relative_file_nofollow(root: Path, parts: tuple[str, ...]) -> int:
    """Open a relative file beneath root without following symlinks in any component."""
    if (not parts or any(not isinstance(part, str) or part in ("", ".", "..")
                         or "/" in part or "\\" in part for part in parts)):
        raise ValueError("Unsafe backup source path components")
    # Never silently drop no-follow/dir-fd protection on unsupported platforms.
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if (type(nofollow) is not int or type(directory) is not int
            or os.open not in os.supports_dir_fd):
        raise ValueError("Secure no-follow backup opening is unavailable")
    directory_flags = os.O_RDONLY | directory | nofollow
    file_flags = os.O_RDONLY | nofollow | getattr(os, "O_NONBLOCK", 0)
    opened_dirs: list[int] = []
    try:
        current = os.open(root, directory_flags)
        opened_dirs.append(current)
        for component in parts[:-1]:
            current = os.open(component, directory_flags, dir_fd=current)
            opened_dirs.append(current)
        return os.open(parts[-1], file_flags, dir_fd=current)
    finally:
        for descriptor in reversed(opened_dirs):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _create_relative_file_nofollow(root: Path, parts: tuple[str, ...],
                                   expected_root_identity: tuple[int, int] | None = None) -> int:
    """Exclusively create a file beneath root using directory descriptors only."""
    if (not parts or any(not isinstance(part, str) or part in ("", ".", "..")
                         or "/" in part or "\\" in part for part in parts)):
        raise ValueError("Unsafe sandbox destination path")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if (type(nofollow) is not int or type(directory) is not int
            or os.open not in os.supports_dir_fd or os.mkdir not in os.supports_dir_fd):
        raise ValueError("Secure no-follow destination creation is unavailable")
    directory_flags = os.O_RDONLY | directory | nofollow
    opened_dirs: list[int] = []
    try:
        current = os.open(root, directory_flags)
        opened_dirs.append(current)
        root_stat = os.fstat(current)
        if (expected_root_identity is not None and
                (root_stat.st_dev, root_stat.st_ino) != expected_root_identity):
            raise ValueError("Sandbox destination root changed during copy")
        for component in parts[:-1]:
            try:
                os.mkdir(component, mode=0o700, dir_fd=current)
            except FileExistsError:
                pass
            child = os.open(component, directory_flags, dir_fd=current)
            opened_dirs.append(child)
            current = child
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow
        return os.open(parts[-1], flags, 0o600, dir_fd=current)
    finally:
        for descriptor in reversed(opened_dirs):
            try:
                os.close(descriptor)
            except OSError:
                pass


def snapshot_manifest(root: Path, paths: list[str]) -> dict:
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError("Backup root must be a real directory")
    # A real leaf reached through a symlinked ancestor is still an aliased root.
    # Reject it before resolving or reading any manifest member.
    if any(ancestor.is_symlink() for ancestor in (root, *root.parents)):
        raise ValueError("Backup root ancestors must not be symlinks")
    base = root.resolve(strict=True)
    if base != root.absolute():
        raise ValueError("Backup root must resolve to its canonical absolute path")
    if (not isinstance(paths, list) or any(not isinstance(name, str) or not name for name in paths)
            or len(set(paths)) != len(paths)):
        raise ValueError("Backup paths must be unique nonempty strings")
    # Enforce the same resource bounds on creation as on verification.
    if len(paths) > 10000:
        raise ValueError("Backup source exceeds bounded entry limit")
    if any(len(name) > 4096 for name in paths):
        raise ValueError("Backup source path exceeds bounded length")
    entries = []
    for name in sorted(paths):
        if (any(ord(c) < 32 or ord(c) == 127
                or 0xD800 <= ord(c) <= 0xDFFF for c in name)
                or ":" in name or name.startswith("~")):
            raise ValueError("Unsafe backup source path")
        requested = Path(name)
        if (requested.is_absolute() or "\\" in name or
                any(part in ("", ".", "..") for part in name.split("/"))):
            raise ValueError("Unsafe backup source path")
        candidate = base / requested
        for parent in (base, *(base / Path(*requested.parts[:i]) for i in range(1, len(requested.parts) + 1))):
            if parent.is_symlink():
                raise ValueError("Symlink in backup source path is not permitted")
        digest = hashlib.sha256()
        size = 0
        try:
            descriptor = _open_relative_file_nofollow(base, requested.parts)
        except OSError as exc:
            raise ValueError("Backup source path changed or contains a symlink") from exc
        with os.fdopen(descriptor, "rb") as source:
            metadata = os.fstat(source.fileno())
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
                raise ValueError("Backup source must be a singly linked regular file")
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
                size += len(chunk)
            # A checksum of bytes read during concurrent modification is not
            # necessarily a consistent source snapshot. Fail closed when the
            # descriptor's identity, size or timestamps changed mid-read.
            after = os.fstat(source.fileno())
            if (metadata.st_dev, metadata.st_ino, metadata.st_size,
                    metadata.st_mtime_ns, metadata.st_ctime_ns) != (
                    after.st_dev, after.st_ino, after.st_size,
                    after.st_mtime_ns, after.st_ctime_ns) or size != after.st_size:
                raise ValueError("Backup source changed during manifest read")
        entries.append({"path": requested.as_posix(),
                        "bytes": size, "sha256": digest.hexdigest()})
    return {"entries": entries, "mode": "manifest_only", "external_backup_verified": False,
            "restore_verified": False, "production_writes": False}

def verify_manifest(root: Path, manifest: dict) -> bool:
    if not isinstance(manifest, dict) or not isinstance(manifest.get("entries"), list):
        raise ValueError("Invalid backup manifest")
    # Local manifests cannot be relabeled as an externally verified backup.
    if "mode" in manifest and (type(manifest["mode"]) is not str
                               or manifest["mode"] != "manifest_only"):
        raise ValueError("Unsupported backup manifest mode")
    # A local checksum manifest is never evidence of external backup or
    # production restoration. Do not accept forged positive attestations.
    for claim in ("external_backup_verified", "restore_verified", "production_writes"):
        if claim in manifest and manifest[claim] is not False:
            raise ValueError("Unverified backup manifest attestation")
    if not manifest["entries"]:
        return False
    # Bound untrusted manifests before iterating or opening filesystem paths.
    if len(manifest["entries"]) > 10000:
        raise ValueError("Backup manifest exceeds bounded entry limit")
    if any(not isinstance(entry, dict) or not isinstance(entry.get("path"), str)
           or type(entry.get("bytes")) is not int or entry["bytes"] < 0
           or not isinstance(entry.get("sha256"), str) or len(entry["sha256"]) != 64
           or any(c not in "0123456789abcdef" for c in entry["sha256"])
           for entry in manifest["entries"]):
        raise ValueError("Invalid backup manifest entry")
    paths = [entry["path"] for entry in manifest["entries"]]
    # Reject pathological names before sorting, hashing, or filesystem access.
    if any(len(path) > 4096 for path in paths):
        raise ValueError("Backup manifest path exceeds bounded length")
    # Reject malformed Unicode and control bytes before filesystem operations.
    if any(any(ord(char) < 32 or ord(char) == 127
               or 0xD800 <= ord(char) <= 0xDFFF for char in path)
           for path in paths):
        raise ValueError("Unsafe backup manifest path characters")
    if len(set(paths)) != len(paths):
        raise ValueError("Duplicate backup manifest paths")
    # A manifest is a canonical snapshot, not an arbitrary subset or reordered list.
    if paths != sorted(paths):
        return False
    if not paths:
        return False
    current = snapshot_manifest(root, paths)
    return current["entries"] == manifest["entries"]


def _secure_regular_file_identity(root: Path, name: str) -> tuple[int, int]:
    """Read inode identity via no-follow descriptors, never a re-opened path stat."""
    descriptor = _open_relative_file_nofollow(root, Path(name).parts)
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise ValueError("Copy audit requires singly linked regular files")
        return metadata.st_dev, metadata.st_ino
    finally:
        os.close(descriptor)


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
    first = snapshot_manifest(source, names)
    second = snapshot_manifest(destination, names)
    # Only access inode metadata after source paths passed manifest validation.
    for entry in first["entries"]:
        name = entry["path"]
        left = _secure_regular_file_identity(resolved[0], name)
        right = _secure_regular_file_identity(resolved[1], name)
        if left == right:
            raise ValueError("Copy audit requires physically independent files")
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
    # Validate all requested paths before checking inode identity.
    original = snapshot_manifest(source, names)
    backed_up = snapshot_manifest(backup, names)
    recovered = snapshot_manifest(restored, names)
    for entry in original["entries"]:
        name = entry["path"]
        identities = [_secure_regular_file_identity(root, name) for root in locations]
        if len(set(identities)) != 3:
            raise ValueError("Independent restore trees must not share hard-linked files")
    valid = original["entries"] == backed_up["entries"] == recovered["entries"]
    return {"independent_sandbox_restore_matches": valid,
            "files_checked": len(original["entries"]),
            "backup_verified_against_source": original["entries"] == backed_up["entries"],
            "restore_verified_against_backup": backed_up["entries"] == recovered["entries"],
            "external_storage_proven": False, "production_restore_verified": False,
            "production_writes": False}



def _remove_created_tree_if_same(destination: Path, identity: tuple[int, int]) -> None:
    """Rollback only the exact directory inode created by this operation."""
    try:
        current = destination.lstat()
    except FileNotFoundError:
        return
    if (not stat.S_ISDIR(current.st_mode) or stat.S_ISLNK(current.st_mode)
            or (current.st_dev, current.st_ino) != identity):
        return
    import shutil
    shutil.rmtree(destination)

def restore_to_new_sandbox(backup: Path, destination: Path, names: list[str]) -> dict:
    """Restore a verified backup into a newly created sandbox, never production.

    The destination must not exist. A failed copy removes only this new tree.
    """
    import shutil

    backup = Path(backup)
    destination = Path(destination)
    if not isinstance(names, list) or not names:
        raise ValueError("Sandbox restore requires a nonempty file list")
    if destination.is_symlink() or destination.exists():
        raise ValueError("Restore destination must not exist")
    parent = destination.parent
    if parent.is_symlink() or not parent.is_dir():
        raise ValueError("Restore parent must be a real directory")
    # Never traverse an aliased ancestor (e.g. a symlinked sandbox parent).
    for ancestor in (parent, *parent.parents):
        if ancestor.is_symlink():
            raise ValueError("Restore destination ancestors must not be symlinks")
    if not backup.is_dir() or backup.is_symlink():
        raise ValueError("Restore source must be a real directory")
    if any(ancestor.is_symlink() for ancestor in (backup, *backup.parents)):
        raise ValueError("Restore source ancestors must not be symlinks")
    source_root = backup.resolve(strict=True)
    target_root = destination.resolve(strict=False)
    if target_root == source_root or target_root.is_relative_to(source_root):
        raise ValueError("Restore destination must be outside backup tree")
    if source_root.is_relative_to(target_root):
        raise ValueError("Restore destination must not contain backup tree")
    enforce_local_output_path(destination.absolute())
    original = snapshot_manifest(backup, names)
    enforce_local_output_path(destination.absolute())
    destination.mkdir()
    created = destination.lstat()
    created_identity = (created.st_dev, created.st_ino)
    try:
        for entry in original["entries"]:
            relative = Path(entry["path"])
            descriptor = _open_relative_file_nofollow(backup, relative.parts)
            try:
                target_descriptor = _create_relative_file_nofollow(destination, relative.parts, created_identity)
            except BaseException:
                os.close(descriptor)
                raise
            with os.fdopen(descriptor, "rb") as reader, os.fdopen(target_descriptor, "wb") as writer:
                metadata = os.fstat(reader.fileno())
                if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
                    raise ValueError("Sandbox copy source must be an independent regular file")
                shutil.copyfileobj(reader, writer, length=1024 * 1024)
        if not verify_manifest(backup, original) or not verify_manifest(destination, original):
            raise ValueError("Backup changed or sandbox restore failed integrity verification")
    except BaseException:
        _remove_created_tree_if_same(destination, created_identity)
        raise
    return {"sandbox_restore_matches": True, "files_restored": len(original["entries"]),
            "external_storage_proven": False, "production_restore_verified": False,
            "production_writes": False}


def backup_to_new_sandbox(source: Path, destination: Path, names: list[str]) -> dict:
    """Create a fresh, integrity-checked sandbox backup; never write to source."""
    import shutil

    source = Path(source)
    destination = Path(destination)
    if not isinstance(names, list) or not names:
        raise ValueError("Sandbox backup requires a nonempty file list")
    if destination.is_symlink() or destination.exists():
        raise ValueError("Backup destination must not exist")
    if not source.is_dir() or source.is_symlink():
        raise ValueError("Backup source must be a real directory")
    if any(ancestor.is_symlink() for ancestor in (source, *source.parents)):
        raise ValueError("Backup source ancestors must not be symlinks")
    parent = destination.parent
    if not parent.is_dir() or any(item.is_symlink() for item in (parent, *parent.parents)):
        raise ValueError("Backup destination parent must be a real unaliased directory")
    source_root = source.resolve(strict=True)
    target_root = destination.resolve(strict=False)
    if (target_root == source_root or target_root.is_relative_to(source_root)
            or source_root.is_relative_to(target_root)):
        raise ValueError("Backup destination must be independent from source")
    enforce_local_output_path(destination.absolute())
    original = snapshot_manifest(source, names)
    enforce_local_output_path(destination.absolute())
    destination.mkdir()
    created = destination.lstat()
    created_identity = (created.st_dev, created.st_ino)
    try:
        for entry in original["entries"]:
            relative = Path(entry["path"])
            descriptor = _open_relative_file_nofollow(source, relative.parts)
            try:
                target_descriptor = _create_relative_file_nofollow(destination, relative.parts, created_identity)
            except BaseException:
                os.close(descriptor)
                raise
            with os.fdopen(descriptor, "rb") as reader, os.fdopen(target_descriptor, "wb") as writer:
                metadata = os.fstat(reader.fileno())
                if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
                    raise ValueError("Sandbox copy source must be an independent regular file")
                shutil.copyfileobj(reader, writer, length=1024 * 1024)
        if not verify_manifest(source, original) or not verify_manifest(destination, original):
            raise ValueError("Source changed or sandbox backup failed integrity verification")
    except BaseException:
        _remove_created_tree_if_same(destination, created_identity)
        raise
    return {"sandbox_backup_matches": True, "files_backed_up": len(original["entries"]),
            "external_storage_proven": False, "production_writes": False}
