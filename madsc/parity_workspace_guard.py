"""Identity-only workspace side-effect boundary for opt-in parity children."""
from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path, PurePosixPath

from madsc.write_path_audit import ProtectedWriteRejected


MAX_WORKSPACE_ENTRIES = 20_000
RECEIPT_PATH = "reports/parity-workspace-effects.json"


def _identity(metadata, *, kind: str, target: str = "") -> tuple:
    return (kind, metadata.st_mode, metadata.st_uid, metadata.st_gid,
            metadata.st_dev, metadata.st_ino, metadata.st_nlink,
            metadata.st_size, metadata.st_mtime_ns, metadata.st_ctime_ns,
            target)


def _directory_flags() -> int:
    return (os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))


def _walk_directory(descriptor: int, relative: PurePosixPath,
                    result: dict[str, tuple]) -> None:
    before = os.fstat(descriptor)
    if not stat.S_ISDIR(before.st_mode):
        raise ProtectedWriteRejected("Parity workspace entry is not a directory")
    try:
        with os.scandir(descriptor) as iterator:
            entries = sorted(iterator, key=lambda entry: entry.name)
    except OSError as exc:
        raise ProtectedWriteRejected("Cannot enumerate parity workspace") from exc
    for entry in entries:
        if (not entry.name or entry.name in {".", ".."}
                or "/" in entry.name or "\x00" in entry.name):
            raise ProtectedWriteRejected("Unsafe parity workspace entry name")
        child_relative = relative / entry.name
        label = child_relative.as_posix()
        if len(result) >= MAX_WORKSPACE_ENTRIES:
            raise ProtectedWriteRejected("Parity workspace entry limit exceeded")
        try:
            metadata = entry.stat(follow_symlinks=False)
        except OSError as exc:
            raise ProtectedWriteRejected("Cannot identify parity workspace entry") from exc
        if stat.S_ISDIR(metadata.st_mode):
            try:
                # This descriptor is provably read-only; no caller-supplied flags
                # can turn the inventory walk into a mutation.
                child = os.open(entry.name, os.O_RDONLY
                                | getattr(os, "O_DIRECTORY", 0)
                                | getattr(os, "O_NOFOLLOW", 0)
                                | getattr(os, "O_NONBLOCK", 0),
                                dir_fd=descriptor)
            except OSError as exc:
                raise ProtectedWriteRejected("Cannot open parity workspace directory") from exc
            try:
                opened = os.fstat(child)
                if ((metadata.st_dev, metadata.st_ino)
                        != (opened.st_dev, opened.st_ino)):
                    raise ProtectedWriteRejected("Parity workspace directory changed")
                _walk_directory(child, child_relative, result)
                after = os.fstat(child)
            finally:
                os.close(child)
            if _identity(opened, kind="directory") != _identity(after, kind="directory"):
                raise ProtectedWriteRejected("Parity workspace changed during inventory")
            result[label] = _identity(after, kind="directory")
        elif stat.S_ISREG(metadata.st_mode):
            result[label] = _identity(metadata, kind="regular")
        elif stat.S_ISLNK(metadata.st_mode):
            try:
                target = os.readlink(entry.name, dir_fd=descriptor)
                current = entry.stat(follow_symlinks=False)
            except OSError as exc:
                raise ProtectedWriteRejected("Cannot identify parity workspace symlink") from exc
            if _identity(metadata, kind="symlink", target=target) != _identity(
                    current, kind="symlink", target=target):
                raise ProtectedWriteRejected("Parity workspace symlink changed")
            result[label] = _identity(current, kind="symlink", target=target)
        else:
            raise ProtectedWriteRejected("Unsupported special entry in parity workspace")
    after = os.fstat(descriptor)
    if _identity(before, kind="directory") != _identity(after, kind="directory"):
        raise ProtectedWriteRejected("Parity workspace changed during inventory")


def snapshot_workspace(root: Path) -> dict[str, tuple]:
    """Capture bounded lstat identities without reading repository file bytes."""
    root = Path(root)
    try:
        path_metadata = root.lstat()
    except OSError as exc:
        raise ProtectedWriteRejected("Missing parity workspace root") from exc
    if (not root.is_absolute() or root.is_symlink()
            or not stat.S_ISDIR(path_metadata.st_mode)
            or root.resolve(strict=True) != root):
        raise ProtectedWriteRejected("Unsafe parity workspace root")
    try:
        # Keep the full read-only expression visible for the K1 callsite audit.
        descriptor = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                             | getattr(os, "O_NOFOLLOW", 0)
                             | getattr(os, "O_NONBLOCK", 0))
    except OSError as exc:
        raise ProtectedWriteRejected("Cannot open parity workspace root") from exc
    try:
        opened = os.fstat(descriptor)
        if ((path_metadata.st_dev, path_metadata.st_ino)
                != (opened.st_dev, opened.st_ino)):
            raise ProtectedWriteRejected("Parity workspace root changed")
        result = {".": _identity(opened, kind="directory")}
        _walk_directory(descriptor, PurePosixPath(), result)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = root.lstat()
    if (_identity(opened, kind="directory") != _identity(after, kind="directory")
            or _identity(after, kind="directory")
            != _identity(current, kind="directory")):
        raise ProtectedWriteRejected("Parity workspace root changed during inventory")
    result["."] = _identity(after, kind="directory")
    return result


def enforce_workspace_effects(before: dict[str, tuple], after: dict[str, tuple],
                              *, expected_output: str | None) -> tuple[str, ...]:
    """Allow only creation of the consumer's one declared output file."""
    if not isinstance(before, dict) or not isinstance(after, dict):
        raise ProtectedWriteRejected("Invalid parity workspace inventory")
    changed = {name for name in set(before) | set(after)
               if before.get(name) != after.get(name)}
    allowed: set[str] = set()
    if expected_output is not None:
        relative = PurePosixPath(expected_output)
        if (relative.is_absolute() or not relative.parts
                or any(part in {"", ".", ".."} for part in relative.parts)):
            raise ProtectedWriteRejected("Unsafe expected parity output")
        label = relative.as_posix()
        parent = relative.parent.as_posix()
        allowed.update({label, parent})
        if label in before:
            raise ProtectedWriteRejected("Expected parity output already existed")
        if label in after:
            identity = after[label]
            if (identity[0] != "regular" or identity[6] != 1
                    or parent not in before or parent not in after
                    or before[parent][0] != "directory"
                    or after[parent][0] != "directory"
                    or before[parent][1:7] != after[parent][1:7]):
                raise ProtectedWriteRejected("Unsafe expected parity output effect")
    unexpected = sorted(changed - allowed)
    if unexpected:
        raise ProtectedWriteRejected(
            "Unexpected parity workspace effects: " + ", ".join(unexpected[:8]))
    return tuple(sorted(changed))


def build_workspace_effect_receipt(before: dict[str, tuple],
                                   after: dict[str, tuple], *, consumer: str,
                                   expected_output: str | None,
                                   observed_changes: tuple[str, ...]) -> bytes:
    """Serialize a hash-bound, non-accepting receipt for a successful child."""
    verified = enforce_workspace_effects(
        before, after, expected_output=expected_output)
    if verified != observed_changes or consumer not in {"k1", "k4", "k5"}:
        raise ProtectedWriteRejected("Invalid parity workspace effect receipt")

    def digest(inventory: dict[str, tuple]) -> str:
        encoded = json.dumps(inventory, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

    receipt = {
        "schema": "madsc-parity-workspace-effects-v1",
        "consumer": consumer,
        "scope": "repository_workspace_persistent_identity",
        "expected_output": expected_output,
        "observed_changes": list(observed_changes),
        "before_inventory_sha256": digest(before),
        "after_inventory_sha256": digest(after),
        "external_effects_verified": False,
        "independent_execution_verified": False,
        "behavioral_parity_accepted": False,
        "production_ready": False,
    }
    return (json.dumps(receipt, sort_keys=True, separators=(",", ":"))
            + "\n").encode("utf-8")
