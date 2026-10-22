"""K4 executable isolated backup and restore drill.

Copies only allowlisted files into temporary directories; source is never modified.
This is not proof of external storage or production restoration.
"""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from madsc.backup import (snapshot_manifest, verify_independent_restore,
                          backup_to_new_sandbox, restore_to_new_sandbox)
from madsc.fixture_report_writer import write_stage_report
from madsc.write_path_audit import enforce_local_output_path


def run_drill(source: Path, names: list[str]) -> dict:
    source = Path(source)
    baseline = snapshot_manifest(source, names)
    if not baseline["entries"]:
        raise ValueError("Restore drill requires nonempty file selection")
    with tempfile.TemporaryDirectory(prefix="madsc-k4-") as tmp:
        base = Path(tmp)
        backup, restored = base / "backup", base / "restored"
        backup_result = backup_to_new_sandbox(source, backup, names)
        restore_result = restore_to_new_sandbox(backup, restored, names)
        report = verify_independent_restore(source, backup, restored, names)
        if not report["independent_sandbox_restore_matches"]:
            raise ValueError("Backup and restore drill integrity mismatch")
        if snapshot_manifest(source, names)["entries"] != baseline["entries"]:
            raise ValueError("Source changed during restore drill")
        return {**report, "drill_executed": True,
                "sandbox_backup_matches": backup_result["sandbox_backup_matches"],
                "sandbox_restore_matches": restore_result["sandbox_restore_matches"],
                "temporary_backup_created": True,
                "temporary_restore_created": True, "source_unchanged": True,
                "external_storage_proven": False, "production_restore_verified": False}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--file", action="append", required=True, dest="names")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--isolated-report-root", type=Path)
    args = parser.parse_args()
    if args.isolated_report_root is not None:
        expected = args.isolated_report_root / "reports/k4-isolated-evidence.json"
        if args.output != expected:
            raise ValueError("K4 isolated output must use the protected reports path")
        enforce_local_output_path(expected)
    else:
        destination = args.output if args.output.is_absolute() else Path.cwd() / args.output
        enforce_local_output_path(destination)
    report = run_drill(args.source, args.names)
    if args.isolated_report_root is not None:
        write_stage_report(args.isolated_report_root, "k4",
                           {**report, "category": "k4", "production_ready": False})
        print(json.dumps(report, sort_keys=True))
        return
    destination = args.output if args.output.is_absolute() else Path.cwd() / args.output
    enforce_local_output_path(destination)
    with destination.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
