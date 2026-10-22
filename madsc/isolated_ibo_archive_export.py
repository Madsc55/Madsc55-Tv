"""K5 create-only offline IBO manifest export outside the source tree."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from madsc.isolated_ibo_archive_preview import build_6115_archive_preview
from madsc.write_path_audit import enforce_write_paths


def export_6115_archive_manifest(urls: list[str], destination: Path) -> dict:
    """Export one JSON preview to a fresh directory; no M3U or network writes."""
    manifest = build_6115_archive_preview(urls)
    raw = str(destination)
    if any(part in (".", "..") for part in raw.replace(chr(92), "/").split("/")):
        raise PermissionError("Ambiguous destination")
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
    target = destination / "ibo_6115_archive_preview.json"
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        fd = os.open(target, flags, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle, ensure_ascii=False, sort_keys=True, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        # Verify the persisted bytes before claiming a successful export.
        saved = target.read_bytes()
        if json.loads(saved) != manifest:
            raise OSError("Archive manifest readback mismatch")
        if hashlib.sha256(saved).digest() != hashlib.sha256(
            (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
        ).digest():
            raise OSError("Archive manifest byte integrity mismatch")
        return manifest
    except BaseException:
        target.unlink(missing_ok=True)
        destination.rmdir()
        raise
