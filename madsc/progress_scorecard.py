"""Evidence-linked K1-K5 progress; historical 47/53 is not a live metric."""
import argparse
import json
from pathlib import Path
from madsc.write_path_audit import enforce_local_output_path

BASELINE = {"overall_reference_completed_percent": 47, "overall_reference_remaining_percent": 53}
INVENTORY = {"legacy_yaml_source_review": {"done": 99, "total": 99},
             "legacy_python_source_inventory": {"done": 130, "total": 130},
             "legacy_python_test_inventory": {"done": 68, "total": 68}}
STAGES = ("K1", "K2", "K3", "K4", "K5")


def task_summary(tasks):
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("Nonempty task ledger required")
    ids = set()
    stages = {name: {"completed": 0, "in_progress": 0, "pending": 0, "total": 0} for name in STAGES}
    in_progress = 0
    completed = 0
    for task in tasks:
        if not isinstance(task, dict) or not isinstance(task.get("id"), str) or not task["id"] or task["id"] in ids:
            raise ValueError("Invalid or duplicate task ID")
        ids.add(task["id"])
        stage, status = task.get("stage"), task.get("status")
        if stage not in stages or status not in ("pending", "in_progress", "completed"):
            raise ValueError("Invalid stage or status")
        evidence = task.get("evidence", [])
        if not isinstance(evidence, list) or any(not isinstance(x, str) or not x.strip() for x in evidence):
            raise ValueError("Invalid evidence")
        if status == "completed" and not evidence:
            raise ValueError("Completed task requires evidence")
        stages[stage]["total"] += 1
        if status == "completed":
            completed += 1
            stages[stage]["completed"] += 1
        elif status == "in_progress":
            in_progress += 1
            stages[stage]["in_progress"] += 1
        else:
            stages[stage]["pending"] += 1
    total = len(tasks)
    return {"completed": completed, "in_progress": in_progress,
            "pending": total - completed - in_progress,
            "remaining": total - completed, "total": total,
            "completed_percent": round(100 * completed / total, 2),
            "remaining_percent": round(100 * (total - completed) / total, 2),
            "by_stage": stages, "scope": "Only explicitly enumerated, evidence-linked tasks"}


def scorecard(accepted_behaviors=0, accepted_security=0, verified_ci=False, tasks=None):
    if (type(accepted_behaviors) is not int or type(accepted_security) is not int
            or not 0 <= accepted_behaviors <= 92 or not 0 <= accepted_security <= 26
            or type(verified_ci) is not bool):
        raise ValueError("Invalid progress evidence")
    task_progress = task_summary(tasks) if tasks is not None else None
    return {
        "schema": "madsc-evidence-scorecard-v2",
        "reference": dict(BASELINE),
        "source_inventory": INVENTORY,
        "acceptance": {
            "legacy_behavioral_equivalence": {"accepted": accepted_behaviors, "total": 92},
            "runtime_security_rules": {"accepted": accepted_security, "total": 26}},
        "measured_progress": {
            "legacy_yaml_initial_review_percent": 100.0,
            "legacy_python_source_inventory_percent": 100.0,
            "legacy_python_test_inventory_percent": 100.0,
            "legacy_behavioral_acceptance_percent": round(100 * accepted_behaviors / 92, 2),
            "runtime_security_acceptance_percent": round(100 * accepted_security / 26, 2),
            "combined_acceptance_percent": round(100 * (accepted_behaviors + accepted_security) / 118, 2),
            "combined_acceptance_denominator": 118,
            "scope": "Only 92 behavioral and 26 runtime security acceptances; not overall project completion"},
        "five_system_ci": {"last_run_success_verified": verified_ci,
                           "scope": "offline workflow integration, not production acceptance"},
        "task_progress": task_progress,
        "calculated_overall_percent": task_progress["completed_percent"] if task_progress else None,
        "reason": "Measured against supplied task ledger only" if task_progress else "No verified full task ledger supplied",
        "production_ready": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--tasks", type=Path, help="K1-K5 task evidence JSON list")
    parser.add_argument("--verified-ci", action="store_true")
    args = parser.parse_args()
    enforce_local_output_path(args.output.absolute())
    default_ledger = Path(__file__).resolve().parent.parent / "docs" / "K1_K5_KANITLI_GOREV_DEFTERI.json"
    ledger = args.tasks if args.tasks is not None else default_ledger
    tasks = json.loads(ledger.read_text(encoding="utf-8")) if ledger.is_file() else None
    report = scorecard(verified_ci=args.verified_ci, tasks=tasks)
    if args.output.exists() or args.output.is_symlink():
        raise FileExistsError("Progress evidence cannot overwrite existing data")
    if not args.output.parent.is_dir() or args.output.parent.is_symlink():
        raise ValueError("Output parent must be an existing real directory")
    with args.output.open("x", encoding="utf-8") as out:
        json.dump(report, out, indent=2, sort_keys=True, ensure_ascii=False)
        out.write("\n")


if __name__ == "__main__":
    main()
