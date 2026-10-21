"""Read-only K1-K5 installation inventory; no tests, Actions or production writes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import ast

from madsc.k1_k5_acceptance_requirements import REQUIREMENTS, assess_task_evidence

MAIN = {
    "K1": "madsc-01-guvenlik.yml",
    "K2": "madsc-02-kesif.yml",
    "K3": "madsc-03-kanal-test.yml",
    "K4": "madsc-04-yedek.yml",
    "K5": "madsc-05-bakim.yml",
}
STATUSES = {"pending", "in_progress", "completed"}


def inspect_installation(root: Path) -> dict:
    """Inventory wiring and task ledger without running a workflow or test."""
    root = Path(root)
    workflows = root / ".github" / "workflows"
    ledger = root / "docs" / "K1_K5_KANITLI_GOREV_DEFTERI.json"
    if not workflows.is_dir() or not ledger.is_file() or ledger.is_symlink():
        raise ValueError("Missing workflow directory or task ledger")
    tasks = json.loads(ledger.read_text(encoding="utf-8"))
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("Invalid task ledger")
    ids = set()
    counts = {stage: {"completed": 0, "in_progress": 0, "pending": 0} for stage in MAIN}
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("Invalid task")
        identifier, stage, status = task.get("id"), task.get("stage"), task.get("status")
        if (not isinstance(identifier, str) or identifier in ids
                or stage not in MAIN or status not in STATUSES
                or not identifier.startswith(stage + "-")):
            raise ValueError("Invalid or duplicate task stage/status/id")
        ids.add(identifier)
        counts[stage][status] += 1
    if ids != set(REQUIREMENTS):
        raise ValueError("Incomplete or unexpected K1-K5 task ledger")
    evidence = assess_task_evidence(tasks)
    writer_calls = []
    for module in sorted((root / "madsc").glob("*.py")):
        if module.is_symlink():
            raise ValueError("Symlinked Python source")
        tree = ast.parse(module.read_text(encoding="utf-8"), filename=str(module))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                target = node.func
                name = target.attr if isinstance(target, ast.Attribute) else (target.id if isinstance(target, ast.Name) else "")
                operations = {"write_text", "write_bytes", "replace", "mkdir",
                              "NamedTemporaryFile", "mkstemp", "unlink", "rename", "copyfile", "copy2"}
                if name == "open":
                    mode_node = next((kw.value for kw in node.keywords if kw.arg == "mode"), None)
                    if mode_node is None and len(node.args) >= (2 if isinstance(target, ast.Name) else 1):
                        mode_node = node.args[1] if isinstance(target, ast.Name) else node.args[0]
                    if mode_node is None:
                        continue  # Default open() is read-only.
                    if not isinstance(mode_node, ast.Constant) or not isinstance(mode_node.value, str):
                        classification = "dynamic_mode_review"
                    elif any(flag in mode_node.value for flag in "wax+"):
                        classification = "write"
                    else:
                        continue
                elif name in operations:
                    classification = "write"
                else:
                    continue
                writer_calls.append({"file": module.relative_to(root).as_posix(),
                                     "line": node.lineno, "operation": name,
                                     "classification": classification})
    files = sorted(p.name for p in workflows.iterdir()
                   if p.is_file() and p.suffix in (".yml", ".yaml"))
    missing = [name for name in MAIN.values() if name not in files]
    additional = [name for name in files if name not in MAIN.values()]
    return {
        "mode": "read_only_installation_inventory",
        "five_main_workflows": dict(MAIN),
        "main_workflows_present": not missing,
        "missing_main_workflows": missing,
        "additional_workflows_requiring_consolidation_review": additional,
        "total_workflow_files": len(files),
        "task_counts": counts,
        "evidence_requirements_missing_tasks": evidence["requirements_missing_tasks"],
        "external_evidence_required_tasks": evidence["requires_external_evidence_tasks"],
        "writer_callsite_candidates": writer_calls,
        "writer_callsite_candidates_count": len(writer_calls),
        "all_writer_callsites_manually_verified": False,
        "tasks_total": len(tasks),
        "tasks_completed": sum(x["completed"] for x in counts.values()),
        "tasks_in_progress": sum(x["in_progress"] for x in counts.values()),
        "tasks_pending": sum(x["pending"] for x in counts.values()),
        "full_five_workflow_consolidation_proven": not missing and not additional,
        "tests_executed": False,
        "github_actions_triggered": False,
        "production_writes": False,
        "production_ready": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    print(json.dumps(inspect_installation(args.root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
