"""Narrow descriptor writer for bundled K1-K5 fixtures in system temp roots."""
from __future__ import annotations

import os
import stat
import tempfile
from pathlib import Path, PurePosixPath

from madsc.write_path_audit import ProtectedWriteRejected


_ALLOWED_FILES = frozenset({
    "sample.m3u",
    "sample.m3u8",
    "legacy_history/gecmis.json",
    "legacy_history/ana_liste_test_gecmisi.json",
    "epg.xml",
    "pilot.xml",
    "sample.txt",
    "fixture.txt",
})


def enforce_core_fixture_path(root: Path, relative_path: str, *, overwrite: bool) -> Path:
    """Permit only fixed offline fixtures below a fresh system temp directory."""
    if type(overwrite) is not bool or not isinstance(relative_path, str):
        raise ProtectedWriteRejected("Invalid core fixture policy")
    if (relative_path not in _ALLOWED_FILES
            or PurePosixPath(relative_path).as_posix() != relative_path):
        raise ProtectedWriteRejected("Unrecognized core fixture path")
    root = Path(root)
    if (not root.is_absolute() or root.is_symlink() or not root.is_dir()
            or root.resolve(strict=True) != root):
        raise ProtectedWriteRejected("Core fixture root must be a real absolute directory")
    system_temp = Path(tempfile.gettempdir()).resolve(strict=True)
    if root.parent != system_temp or not root.name.startswith("tmp"):
        raise ProtectedWriteRejected("Core fixtures require a direct system temp root")
    destination = root.joinpath(*relative_path.split("/"))
    if destination.is_symlink() or destination.parent.is_symlink():
        raise ProtectedWriteRejected("Symlinked core fixture path")
    if overwrite:
        if not destination.is_file():
            raise ProtectedWriteRejected("Core fixture overwrite target must exist")
        metadata = destination.lstat()
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise ProtectedWriteRejected("Unsafe core fixture overwrite target")
    elif destination.exists():
        raise ProtectedWriteRejected("Core fixture already exists")
    return destination


def write_core_fixture(root: Path, relative_path: str, payload: bytes, *,
                       overwrite: bool = False) -> Path:
    """Write one allowlisted offline fixture through no-follow descriptors."""
    if not isinstance(payload, bytes):
        raise TypeError("Core fixture payload must be bytes")
    enforce_core_fixture_path(root, relative_path, overwrite=overwrite)
    destination = Path(root).joinpath(*relative_path.split("/"))
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory_flag = getattr(os, "O_DIRECTORY", None)
    if not isinstance(nofollow, int) or not isinstance(directory_flag, int):
        raise PermissionError("Secure core fixture descriptors are unavailable")
    root = Path(root)
    directory_flags = os.O_RDONLY | directory_flag | nofollow
    root_fd = os.open(root, directory_flags)
    parent_fd = root_fd
    descriptor = None
    created_identity = None
    completed = False
    try:
        root_metadata = os.fstat(root_fd)
        path_metadata = root.lstat()
        if ((root_metadata.st_dev, root_metadata.st_ino) !=
                (path_metadata.st_dev, path_metadata.st_ino)):
            raise PermissionError("Core fixture root changed before write")
        parts = relative_path.split("/")
        if len(parts) == 2:
            try:
                os.mkdir(parts[0], mode=0o700, dir_fd=root_fd)
            except FileExistsError:
                pass
            parent_fd = os.open(parts[0], directory_flags, dir_fd=root_fd)
        # O_NONBLOCK prevents a swapped FIFO from hanging the writer before
        # fstat can reject its non-regular descriptor.
        nonblock = getattr(os, "O_NONBLOCK", None)
        if not isinstance(nonblock, int):
            raise PermissionError("Nonblocking secure fixture open is unavailable")
        flags = os.O_WRONLY | nofollow | nonblock | (0 if overwrite
                                                     else os.O_CREAT | os.O_EXCL)
        descriptor = os.open(parts[-1], flags, 0o600, dir_fd=parent_fd)
        metadata = os.fstat(descriptor)
        if not overwrite:
            created_identity = (metadata.st_dev, metadata.st_ino)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise PermissionError("Core fixture must be an independent regular file")
        if overwrite:
            current = destination.lstat()
            if ((metadata.st_dev, metadata.st_ino) !=
                    (current.st_dev, current.st_ino)):
                raise PermissionError("Core fixture changed before overwrite")
            os.ftruncate(descriptor, 0)
        with os.fdopen(descriptor, "wb", closefd=False) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        # Persist the directory entry as well as the file contents before
        # reporting success. This is required for durable fixture evidence.
        os.fsync(parent_fd)
        completed = True
    finally:
        if not completed and created_identity is not None:
            # Never unlink a different inode swapped into the fixture path.
            try:
                current = os.stat(parts[-1], dir_fd=parent_fd,
                                  follow_symlinks=False)
                if (current.st_dev, current.st_ino) == created_identity:
                    os.unlink(parts[-1], dir_fd=parent_fd)
                    os.fsync(parent_fd)
            except OSError:
                pass
        if descriptor is not None:
            os.close(descriptor)
        if parent_fd != root_fd:
            os.close(parent_fd)
        os.close(root_fd)
    return destination
