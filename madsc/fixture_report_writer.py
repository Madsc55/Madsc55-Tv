"""Restricted writers for isolated evidence; not a repository-wide write gate."""
import os
import stat
from pathlib import Path
from madsc.write_path_audit import (enforce_write_paths, enforce_local_output_path,
                                    enforce_local_turkish_tv_test_playlist)


_TURKISH_TV_PLAYLIST = "reports/MADSC55_TURKCE_TV_ADAY_DENEME.m3u8"


def _prepare_fixture_root(root: Path) -> Path:
    root = Path(root).absolute()
    if root.is_symlink() or not root.is_dir() or root.resolve(strict=True) != root:
        raise PermissionError("Fixture root and its ancestors must be real, nonsymlink directories")
    reports = root / "reports"
    if reports.is_symlink() or (reports.exists() and not reports.is_dir()):
        raise PermissionError("Invalid reports directory")
    if not reports.exists():
        reports.mkdir()
    return root


def _exclusive_bytes(destination: Path, payload: bytes) -> None:
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if not isinstance(nofollow, int):
        raise PermissionError("Secure exclusive output is unavailable without O_NOFOLLOW")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow
    descriptor = os.open(destination, flags, 0o600)
    completed = False
    created_identity = None
    try:
        metadata = os.fstat(descriptor)
        created_identity = metadata
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise PermissionError("Evidence output must be an independent regular file")
        with os.fdopen(descriptor, "wb", closefd=False) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        completed = True
    finally:
        os.close(descriptor)
        if not completed:
            # A concurrent replacement must never be deleted by cleanup.
            try:
                current = destination.lstat()
            except FileNotFoundError:
                pass
            else:
                if (created_identity is not None and
                        (current.st_dev, current.st_ino, current.st_size,
                         current.st_mtime_ns, current.st_ctime_ns) ==
                        (created_identity.st_dev, created_identity.st_ino,
                         created_identity.st_size, created_identity.st_mtime_ns,
                         created_identity.st_ctime_ns)):
                    destination.unlink(missing_ok=True)



# Rollback identity includes timestamps and size as well as inode to avoid
# deleting a concurrent replacement if the filesystem reuses an inode.

def prepare_turkish_tv_test_bundle(root: Path) -> tuple[Path, Path, Path]:
    """Create only the reports directory and preflight both fixed outputs."""
    root = _prepare_fixture_root(root)
    playlist_path = root / _TURKISH_TV_PLAYLIST
    report_path = root / "reports/turkish-tv-batch-validation.json"
    enforce_write_paths(["reports/turkish-tv-batch-validation.json"])
    enforce_local_turkish_tv_test_playlist(playlist_path, allowed_root=root)
    enforce_local_output_path(report_path, allowed_root=root)
    return root, playlist_path, report_path


def write_turkish_tv_test_bundle(root: Path, playlist: bytes, report: str) -> dict:
    """Write the fixed, opt-in K3 test playlist and its JSON evidence once.

    The general M3U/M3U8 write prohibition remains unchanged.  This narrowly
    scoped writer can only create the named reports artifact and its companion
    JSON evidence under an isolated root.
    """
    if not isinstance(playlist, bytes) or not isinstance(report, str):
        raise TypeError("Playlist must be bytes and report must be text")
    root, playlist_path, report_path = prepare_turkish_tv_test_bundle(root)
    # The JSON side still passes the ordinary K1 policy.  The M3U8 exception is
    # exact-name only and receives the same local path/symlink/overwrite checks.
    for destination in (playlist_path, report_path):
        if destination.exists() or destination.is_symlink():
            raise FileExistsError("Refusing to overwrite existing report evidence")
        if destination.parent != root / "reports":
            raise PermissionError("Evidence output outside reports directory")
    created = []
    try:
        _exclusive_bytes(playlist_path, playlist)
        created.append((playlist_path, playlist_path.lstat()))
        _exclusive_bytes(report_path, report.encode("utf-8"))
        created.append((report_path, report_path.lstat()))
    except Exception:
        # Roll back only the exact inodes this call created. A concurrent
        # replacement must not be removed as if it were our own evidence.
        for path, identity in reversed(created):
            try:
                current = path.lstat()
            except FileNotFoundError:
                continue
            if (current.st_dev, current.st_ino, current.st_size,\n                    current.st_mtime_ns, current.st_ctime_ns) == (\n                    identity.st_dev, identity.st_ino, identity.st_size,\n                    identity.st_mtime_ns, identity.st_ctime_ns):
                path.unlink(missing_ok=True)
        raise
    return {
        "isolated_bundle_written": True,
        "playlist_path": _TURKISH_TV_PLAYLIST,
        "report_path": "reports/turkish-tv-batch-validation.json",
        "production_write_allowed": False,
    }


def write_fixture_report(root: Path, relative_path: str, content: str) -> dict:
    if not isinstance(relative_path, str) or not relative_path.startswith("reports/"):
        raise PermissionError("Only isolated reports are permitted")
    if not isinstance(content, str):
        raise TypeError("Report content must be text")
    enforce_write_paths([relative_path])
    root = Path(root).absolute()
    if root.is_symlink() or not root.is_dir() or root.resolve(strict=True) != root:
        raise PermissionError("Fixture root and its ancestors must be real, nonsymlink directories")
    destination = root.joinpath(*relative_path.split("/"))
    if destination.exists() and not destination.is_file():
        raise PermissionError("Report target must be a regular file")
    if destination.is_symlink() or destination.parent.is_symlink():
        raise PermissionError("Symlink target forbidden")
    # Check every existing ancestor before mkdir: an intermediate symlink
    # must not create directories outside the isolated fixture root.
    base = root.resolve(strict=True)
    cursor = root
    for part in relative_path.split("/")[:-1]:
        cursor = cursor / part
        if cursor.is_symlink():
            raise PermissionError("Symlink ancestor forbidden")
        if cursor.exists() and not cursor.is_dir():
            raise PermissionError("Report ancestor must be a directory")
    if not destination.parent.resolve().is_relative_to(base):
        raise PermissionError("Escaping fixture root")
    # Reject protected ancestors before even creating a reports directory.
    enforce_write_paths([destination.relative_to(destination.anchor).as_posix()])
    first_new = destination
    while not first_new.parent.exists():
        first_new = first_new.parent
    if not first_new.exists():
        enforce_local_output_path(first_new, allowed_root=root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError("Refusing to overwrite existing report evidence")
    enforce_local_output_path(destination, allowed_root=root)
    _exclusive_bytes(destination, content.encode("utf-8"))
    return {"isolated_report_written": True, "production_write_allowed": False}


def write_stage_report(root: Path, stage: str, report: dict) -> dict:
    """K3/K4/K5 isolated JSON handoff via the shared K1 write gate."""
    import json
    if stage not in ("k3", "k4", "k5") or not isinstance(report, dict):
        raise ValueError("Invalid stage report")
    if report.get("category") != stage or report.get("production_writes") is not False:
        raise ValueError("Report must match stage and explicitly forbid production writes")
    if report.get("production_ready") is not False:
        raise ValueError("Isolated evidence must explicitly deny production readiness")
    relative_path = f"reports/{stage}-isolated-evidence.json"
    result = write_fixture_report(root, relative_path,
                                  json.dumps(report, sort_keys=True, ensure_ascii=False) + "\n")
    return {**result, "stage": stage, "relative_path": relative_path}
