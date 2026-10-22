"""K5 isolated M3U export: create-only output outside the source directory."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path

from madsc.playlist_previews import BUCKETS, preview_imported_m3u


def export_isolated_previews(source: Path, destination: Path) -> dict:
    """Write five drafts and a manifest into a new empty, isolated directory.

    Never overwrite existing data, follow output symlinks, or promote to production.
    """
    source = Path(source).absolute()
    destination = Path(destination).absolute()
    if destination == source.parent or destination.is_relative_to(source.parent):
        raise PermissionError("Output must be outside the source directory tree")
    if destination.exists() or destination.is_symlink():
        raise FileExistsError("Isolated output must be a fresh directory")
    if not destination.parent.is_dir() or destination.parent.is_symlink():
        raise PermissionError("Output parent must be an existing regular directory")
    for ancestor in (destination.parent, *destination.parent.parents):
        if ancestor.is_symlink():
            raise PermissionError("Symlinked output ancestor")
    report = preview_imported_m3u(source)
    destination.mkdir(mode=0o700)
    created = []
    try:
        manifest = {"preview_only": True, "production_ready": False,
                    "production_writes": False, "source_channel_count": report["source_channel_count"],
                    "counts": report["counts"], "files": {}}
        for bucket in BUCKETS:
            name = bucket + ".m3u"
            content = report["drafts"][bucket].encode("utf-8")
            path = destination / name
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            fd = os.open(path, flags, 0o600)
            created.append(path)
            with os.fdopen(fd, "wb") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            manifest["files"][name] = {"sha256": hashlib.sha256(content).hexdigest(),
                                       "bytes": len(content), "channels": report["counts"][bucket]}
        path = destination / "manifest.json"
        with path.open("x", encoding="utf-8") as handle:
            json.dump(manifest, handle, ensure_ascii=False, sort_keys=True, indent=2)
            handle.write("\n")
        created.append(path)
        return manifest
    except Exception:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        destination.rmdir()
        raise
