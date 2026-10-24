"""Offline isolated five-stage fixture gate; no live acceptance."""
import json
import os
import stat
import tempfile
from pathlib import Path

from madsc.core import CATEGORIES, execute
from madsc.maintenance import verify_fixture_evidence
from madsc.write_path_audit import ProtectedWriteRejected


def enforce_offline_package_path(root: Path, category: str) -> Path:
    """Allow one absent fixed package below the gate's system temp root."""
    if category not in CATEGORIES:
        raise ProtectedWriteRejected("Unknown offline package category")
    root = Path(root)
    system_temp = Path(tempfile.gettempdir()).resolve(strict=True)
    if (not root.is_absolute() or root.is_symlink() or not root.is_dir()
            or root.resolve(strict=True) != root or root.parent != system_temp
            or not root.name.startswith("madsc-offline-")):
        raise ProtectedWriteRejected("Invalid offline package root")
    destination = root / f"madsc-batch-{category}"
    if destination.exists() or destination.is_symlink():
        raise ProtectedWriteRejected("Offline package already exists")
    return destination


def create_offline_package(root: Path, category: str) -> Path:
    """Create one fixed package with a no-follow root descriptor."""
    enforce_offline_package_path(root, category)
    root = Path(root)
    destination = root / f"madsc-batch-{category}"
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory_flag = getattr(os, "O_DIRECTORY", None)
    if not isinstance(nofollow, int) or not isinstance(directory_flag, int):
        raise PermissionError("Secure offline package creation is unavailable")
    descriptor = os.open(root, os.O_RDONLY | directory_flag | nofollow)
    try:
        opened = os.fstat(descriptor)
        current = root.lstat()
        if ((opened.st_dev, opened.st_ino) !=
                (current.st_dev, current.st_ino)):
            raise PermissionError("Offline package root changed before creation")
        os.mkdir(destination.name, mode=0o700, dir_fd=descriptor)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    metadata = destination.lstat()
    if destination.is_symlink() or not stat.S_ISDIR(metadata.st_mode):
        raise PermissionError("Offline package creation produced an unsafe path")
    return destination


def assess_all(executor=None):
    executor = execute if executor is None else executor
    reports = []
    errors = {}
    for category in CATEGORIES:
        try:
            checks = executor(category)
            valid = isinstance(checks, dict) and bool(checks) and all(value is True for value in checks.values())
            if not valid:
                errors[category] = "invalid_fixture_evidence"
            reports.append({"category": category, "status": "success" if valid else "failure",
                            "production_writes": False, "fixture_checks": checks})
        except Exception as exc:
            errors[category] = type(exc).__name__
            reports.append({"category": category, "status": "failure",
                            "production_writes": False, "fixture_checks": {}})
    summary = verify_fixture_evidence(reports)
    required = set(CATEGORIES)
    if len(CATEGORIES) != 5 or len(required) != 5 or required != {"k1", "k2", "k3", "k4", "k5"}:
        errors["inventory"] = "invalid_five_stage_inventory"
    return {"categories_checked": len(reports),
            "categories": {item["category"]: item["status"] for item in reports},
            "fixture_gate_passed": not errors and summary["fixture_evidence_verified"],
            "errors": errors, "production_ready": False, "production_writes": False,
            "legacy_92_behavioral_acceptance": 0, "runtime_security_26_acceptance": 0}


def main():
    result = assess_all()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["fixture_gate_passed"] else 1


def assess_report_roundtrip():
    """Run all actual isolated producers through the on-disk K5 consumer.

    Temporary files are fixture evidence, never independent Actions artifacts.
    """
    import hashlib
    from tempfile import TemporaryDirectory
    from madsc.core import run
    from madsc.batch_acceptance import collect

    with TemporaryDirectory(prefix="madsc-offline-") as directory:
        root = Path(directory)
        before = {}
        for category in CATEGORIES:
            package = create_offline_package(root, category)
            path = package / f"{category}.json"
            run(category, path)
            before[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        acceptance = collect(root)
        after = {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in before}
        passed = (acceptance["five_isolated_reports_valid"] is True
                  and acceptance["k5_fixture_evidence_verified"] is True
                  and acceptance["production_ready"] is False and before == after
                  and len(before) == 5)
        return {"passed": passed, "reports_written": len(before),
                "reports_sha256": before, "consumer_preserved_report_bytes": before == after,
                "acceptance": acceptance, "independent_execution_evidence": False,
                "production_ready": False}


if __name__ == "__main__":
    raise SystemExit(main())
