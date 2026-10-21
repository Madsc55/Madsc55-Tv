"""Restricted writer for isolated fixture reports; not a repository-wide write gate."""
from pathlib import Path
from madsc.write_path_audit import enforce_write_paths, enforce_local_output_path


def write_fixture_report(root: Path, relative_path: str, content: str) -> dict:
    if not isinstance(relative_path, str) or not relative_path.startswith("reports/"):
        raise PermissionError("Only isolated reports are permitted")
    if not isinstance(content, str):
        raise TypeError("Report content must be text")
    enforce_write_paths([relative_path])
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise PermissionError("Invalid fixture root")
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
    destination.parent.mkdir(parents=True, exist_ok=True)
    enforce_local_output_path(destination, allowed_root=root)
    with destination.open("x", encoding="utf-8") as handle:
        handle.write(content)
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
