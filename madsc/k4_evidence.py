"""Fail-closed K4 isolated restore evidence verification for K5 acceptance."""
import argparse
import json
from pathlib import Path
from madsc.batch_acceptance import _unique_json_pairs
from madsc.write_path_audit import enforce_local_output_path

REQUIRED_TRUE = ("drill_executed", "temporary_backup_created",
                 "temporary_restore_created", "source_unchanged",
                 "independent_sandbox_restore_matches",
                 "backup_verified_against_source", "restore_verified_against_backup")
REQUIRED_FALSE = ("external_storage_proven", "production_restore_verified",
                  "production_writes")

def verify(report):
    if not isinstance(report, dict):
        raise ValueError("K4 evidence must be an object")
    if any(report.get(key) is not True for key in REQUIRED_TRUE):
        raise ValueError("K4 restore evidence incomplete or failed")
    if any(report.get(key) is not False for key in REQUIRED_FALSE):
        raise ValueError("K4 restore production safety claims invalid")
    if type(report.get("files_checked")) is not int or report["files_checked"] < 1:
        raise ValueError("K4 restore evidence requires nonempty verified files")
    return {"k4_isolated_restore_verified": True, "files_checked": report["files_checked"],
            "external_storage_proven": False, "production_ready": False}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.report.is_symlink() or not args.report.is_file() or args.report.stat().st_size > 1024 * 1024:
        raise ValueError("Invalid K4 evidence file")
    report = json.loads(args.report.read_text(encoding="utf-8"), object_pairs_hook=_unique_json_pairs)
    result = verify(report)
    destination = args.output if args.output.is_absolute() else Path.cwd() / args.output
    enforce_local_output_path(destination)
    with destination.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(result, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
