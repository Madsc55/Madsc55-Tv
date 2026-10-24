"""K5 create-only offline IBO manifest export outside the source tree."""
from __future__ import annotations

import hashlib
import json
import os
import unicodedata
from pathlib import Path

from madsc.isolated_ibo_archive_preview import build_6115_archive_preview
from madsc.write_path_audit import enforce_write_paths


def export_6115_archive_manifest(urls: list[str], destination: Path) -> dict:
    """Export one JSON preview to a fresh directory; no M3U or network writes."""
    raw = str(destination)
    slash_normalized = raw.translate({92: 47})
    if len(raw.encode("utf-8", "surrogatepass")) > 4096 or any(len(part.encode("utf-8", "surrogatepass")) > 255
                              for part in slash_normalized.split("/") if part):
        raise PermissionError("Oversized destination path")
    if any(part in (".", "..") for part in slash_normalized.split("/")):
        raise PermissionError("Ambiguous destination")
    if any(unicodedata.category(ch) in ('Cc', 'Cf', 'Cs', 'Zl', 'Zp')
           or 0xFDD0 <= ord(ch) <= 0xFDEF
           or (ord(ch) & 0xFFFE) == 0xFFFE for ch in raw):
        raise PermissionError("Unsafe destination characters")
    # Validate the untrusted destination before processing the full archive.
    manifest = build_6115_archive_preview(urls)
    destination = Path(destination).absolute()
    if destination.parent == destination:
        raise PermissionError('Root output forbidden')
    if destination.name in ('', '.', '..'):
        raise PermissionError('Invalid destination')
    if destination.exists() or destination.is_symlink():
        raise FileExistsError("Destination already exists")
    if not destination.parent.is_dir():
        raise PermissionError("Destination parent missing")
    for ancestor in (destination.parent, *destination.parent.parents):
        if ancestor.is_symlink():
            raise PermissionError("Symlinked destination ancestor")
    enforce_write_paths([destination.relative_to(destination.anchor).as_posix()])
    destination.mkdir(mode=0o700)
    try:
        destination.chmod(0o700)
    except BaseException:
        destination.rmdir()
        raise
    target = destination / "ibo_6115_archive_preview.json"
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        # Serialize once: json.dump and json.dumps may differ for values
        # containing non-ASCII data, so verify exactly what we intended to write.
        payload = (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
        fd = os.open(target, flags, 0o600)
        try:
            handle = os.fdopen(fd, "wb")
        except BaseException:
            os.close(fd)
            raise
        with handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        # Verify the persisted bytes before claiming a successful export.
        saved = target.read_bytes()
        if hashlib.sha256(saved).digest() != hashlib.sha256(payload).digest():
            raise OSError("Archive manifest byte integrity mismatch")
        if json.loads(saved) != manifest:
            raise OSError("Archive manifest readback mismatch")
        # Ensure the new directory entry is durable as well as the file bytes.
        if hasattr(os, "O_DIRECTORY"):
            directory_flags = os.O_RDONLY | os.O_DIRECTORY
            if hasattr(os, "O_NOFOLLOW"):
                directory_flags |= os.O_NOFOLLOW
            directory_fd = os.open(destination, directory_flags)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        return manifest
    except BaseException:
        target.unlink(missing_ok=True)
        destination.rmdir()
        raise
