"""K2 read-only verification of independently collected execution artifacts.

Never fetches URLs or certifies behavioral parity. Callers must independently
bind each file to a verified GitHub run and artifact ID.
"""
from __future__ import annotations

import hashlib
from pathlib import Path


def verify_artifact_bytes(path: str | Path, expected_sha256: str, *, max_bytes: int = 64_000_000) -> dict:
    """Hash a bounded regular artifact without following symlinks."""
    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64 or any(
        c not in "0123456789abcdef" for c in expected_sha256
    ):
        raise ValueError("Expected SHA-256 must be 64 lowercase hex characters")
    if type(max_bytes) is not int or not 1 <= max_bytes <= 64_000_000:
        raise ValueError("Invalid artifact byte limit")
    import os
    import stat
    target = Path(path)
    # Lexical parent traversal can bypass the ancestor symlink check.
    if ".." in target.parts:
        raise ValueError("Artifact paths must not contain parent traversal")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    # Reject symlinked parent directories as well as a symlinked leaf.
    for parent in target.absolute().parents:
        if parent.is_symlink():
            raise ValueError("Artifact path has a symlinked ancestor")
    fd = os.open(target, flags)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError("Artifact must be an unaliased regular file")
        if info.st_size > max_bytes:
            raise ValueError("Artifact exceeds bounded size")
        digest = hashlib.sha256()
        total = 0
        with os.fdopen(os.dup(fd), "rb") as stream:
            while True:
                block = stream.read(min(65536, max_bytes - total + 1))
                if not block:
                    break
                total += len(block)
                if total > max_bytes:
                    raise ValueError("Artifact exceeds bounded size")
                digest.update(block)
        after = os.fstat(fd)
        if (after.st_dev, after.st_size, after.st_mtime_ns, after.st_ctime_ns, after.st_ino) != (
            info.st_dev, info.st_size, info.st_mtime_ns, info.st_ctime_ns, info.st_ino
        ):
            raise ValueError("Artifact changed during verification")
        # Reject a path replaced while its original inode remained open.
        current = os.stat(target, follow_symlinks=False)
        if (current.st_dev, current.st_ino, current.st_size, current.st_mtime_ns, current.st_ctime_ns) != (
            info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns
        ):
            raise ValueError("Artifact path changed during verification")
    finally:
        os.close(fd)
    actual = digest.hexdigest()
    return {
        "sha256": actual,
        "bytes": total,
        "digest_matches": actual == expected_sha256,
        "execution_origin_verified": False,
        "behavioral_parity_accepted": False,
        "production_writes": False,
    }


def compare_artifact_pair(legacy_path: str | Path, replacement_path: str | Path,
                          legacy_sha256: str, replacement_sha256: str,
                          *, max_bytes: int = 64_000_000) -> dict:
    """Compare two local artifact files, without asserting independent run origin.

    Both supplied expected hashes must match actual bytes. No path may be reused.
    This is an integrity prerequisite, NOT behavioral equivalence approval.
    """
    import os
    if os.path.samefile(legacy_path, replacement_path):
        raise ValueError("Legacy and replacement artifacts must be distinct files")
    legacy = verify_artifact_bytes(legacy_path, legacy_sha256, max_bytes=max_bytes)
    replacement = verify_artifact_bytes(
        replacement_path, replacement_sha256, max_bytes=max_bytes
    )
    if not legacy["digest_matches"] or not replacement["digest_matches"]:
        raise ValueError("At least one artifact does not match its expected SHA-256")
    return {
        "legacy": legacy,
        "replacement": replacement,
        "artifact_bytes_match": legacy["sha256"] == replacement["sha256"],
        "independent_origin_api_verified": False,
        "behavioral_parity_accepted": False,
        "production_ready": False,
    }
