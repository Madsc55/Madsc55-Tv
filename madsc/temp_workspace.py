"""K1-guarded system-temp workspaces for isolated local operations."""
from __future__ import annotations

import stat
import tempfile
from contextlib import contextmanager
from pathlib import Path

from madsc.write_path_audit import ProtectedWriteRejected


_ALLOWED_PREFIXES = {"madsc-k3-video-", "madsc-k4-"}


def enforce_local_temporary_root(root: Path, prefix: str) -> None:
    """Validate the real system temp root before a workspace is created."""
    if prefix not in _ALLOWED_PREFIXES:
        raise ProtectedWriteRejected("Unapproved temporary workspace prefix")
    root = Path(root)
    if (not root.is_absolute() or root.is_symlink() or not root.is_dir()
            or root.resolve(strict=True) != root):
        raise ProtectedWriteRejected("System temporary root must be a real directory")
    metadata = root.lstat()
    if not stat.S_ISDIR(metadata.st_mode) or metadata.st_nlink < 1:
        raise ProtectedWriteRejected("Invalid system temporary root identity")


def _verify_workspace(path: Path, root: Path, root_identity: tuple[int, int],
                      prefix: str, expected: tuple[int, int] | None = None
                      ) -> tuple[int, int]:
    root_metadata = root.lstat()
    if ((root_metadata.st_dev, root_metadata.st_ino) != root_identity
            or not stat.S_ISDIR(root_metadata.st_mode) or root.is_symlink()
            or path.parent != root or not path.name.startswith(prefix)
            or path.is_symlink()):
        raise ProtectedWriteRejected("Temporary workspace escaped its verified root")
    metadata = path.lstat()
    identity = (metadata.st_dev, metadata.st_ino)
    if (not stat.S_ISDIR(metadata.st_mode) or metadata.st_nlink < 1
            or path.resolve(strict=True) != path
            or expected is not None and identity != expected):
        raise ProtectedWriteRejected("Temporary workspace identity changed")
    return identity


@contextmanager
def guarded_temporary_directory(prefix: str):
    """Yield one identity-bound workspace and clean only that same directory."""
    root = Path(tempfile.gettempdir())
    enforce_local_temporary_root(root, prefix)
    root_metadata = root.lstat()
    root_identity = (root_metadata.st_dev, root_metadata.st_ino)
    manager = tempfile.TemporaryDirectory(prefix=prefix, dir=root, delete=False)
    workspace = Path(manager.name)
    identity = _verify_workspace(workspace, root, root_identity, prefix)
    try:
        yield workspace
    finally:
        # Never let cleanup follow or remove a replacement at the same name.
        _verify_workspace(workspace, root, root_identity, prefix, identity)
        manager.cleanup()
        if workspace.exists() or workspace.is_symlink():
            raise ProtectedWriteRejected("Temporary workspace cleanup failed")
