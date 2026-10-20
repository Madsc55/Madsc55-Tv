"""Restricted writer for isolated fixture reports; not a repository-wide write gate."""
from pathlib import Path
from madsc.write_path_audit import enforce_write_paths


def write_fixture_report(root: Path, relative_path: str, content: str) -> dict:
    if not isinstance(relative_path, str) or not relative_path.startswith("reports/"):
        raise PermissionError("Only isolated reports are permitted")
    enforce_write_paths([relative_path])
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise PermissionError("Invalid fixture root")
    destination = root.joinpath(*relative_path.split("/"))
    if destination.exists() and not destination.is_file():
        raise PermissionError("Report target must be a regular file")
    if destination.is_symlink() or destination.parent.is_symlink():
        raise PermissionError("Symlink target forbidden")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.parent.resolve().is_relative_to(root.resolve()):
        raise PermissionError("Escaping fixture root")
    if destination.exists():
        raise FileExistsError("Refusing to overwrite existing report evidence")
    with destination.open("x", encoding="utf-8") as handle:
        handle.write(content)
    return {"isolated_report_written": True, "production_write_allowed": False}
