"""Read-only K1-K5 installation inventory; no tests, Actions or production writes."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import ast
import hashlib

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
    ledger_bytes = ledger.read_bytes()
    ledger_sha256 = hashlib.sha256(ledger_bytes).hexdigest()
    tasks = json.loads(ledger_bytes)
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
    source_fingerprints = {}
    for module in sorted((root / "madsc").glob("*.py")):
        if module.is_symlink():
            raise ValueError("Symlinked Python source")
        source_bytes = module.read_bytes()
        source_fingerprints[module.relative_to(root).as_posix()] = hashlib.sha256(source_bytes).hexdigest()
        tree = ast.parse(source_bytes, filename=str(module))
        parents = {child: parent for parent in ast.walk(tree)
                   for child in ast.iter_child_nodes(parent)}

        def enclosing_scope(node):
            current = node
            while current in parents:
                current = parents[current]
                if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Module)):
                    return current
            return tree

        def assigned_value(name, call):
            scope = enclosing_scope(call)
            assignments = []
            for candidate in ast.walk(scope):
                if (candidate is scope
                        or enclosing_scope(candidate) is not scope
                        or getattr(candidate, "lineno", call.lineno) >= call.lineno):
                    continue
                if isinstance(candidate, ast.Assign):
                    if any(isinstance(target, ast.Name) and target.id == name
                           for target in candidate.targets):
                        assignments.append(candidate)
                elif (isinstance(candidate, ast.AnnAssign)
                      and isinstance(candidate.target, ast.Name)
                      and candidate.target.id == name):
                    assignments.append(candidate)
            if not assignments:
                return None
            latest = max(assignments, key=lambda item: item.lineno)
            return latest.value

        def flag_names(node, call, resolving=frozenset()):
            if node is None:
                return set()
            names = {part.attr for part in ast.walk(node)
                     if isinstance(part, ast.Attribute)}
            if isinstance(node, ast.Name) and node.id not in resolving:
                value = assigned_value(node.id, call)
                if value is not None:
                    names |= flag_names(value, call, resolving | {node.id})
            return names

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                target = node.func
                name = target.attr if isinstance(target, ast.Attribute) else (target.id if isinstance(target, ast.Name) else "")
                operations = {"write_text", "write_bytes", "replace", "mkdir",
                              "NamedTemporaryFile", "TemporaryFile", "mkstemp", "unlink",
                              "rename", "copyfile", "copy2", "copy", "move", "rmtree",
                              "makedirs", "remove", "rmdir", "touch", "chmod",
                              "symlink_to", "hardlink_to", "link", "truncate", "writelines",
                              "write", "dump", "dumps_to_file", "to_csv", "to_json"}
                if name == "open" and isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "os":
                    # os.open(path, flags) is a file-descriptor writer when flags include
                    # O_WRONLY/O_RDWR/O_CREAT/O_TRUNC/O_APPEND. Dynamic flags need review.
                    flag_node = node.args[1] if len(node.args) >= 2 else next(
                        (kw.value for kw in node.keywords if kw.arg == "flags"), None)
                    resolved_flag_names = flag_names(flag_node, node)
                    classification = ("write" if resolved_flag_names & {
                        "O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND"}
                        else "dynamic_mode_review")
                elif name in ("open", "fdopen"):
                    mode_node = next((kw.value for kw in node.keywords if kw.arg == "mode"), None)
                    if mode_node is None:
                        if name == "fdopen" and len(node.args) >= 2:
                            mode_node = node.args[1]
                        elif isinstance(target, ast.Name) and len(node.args) >= 2:
                            mode_node = node.args[1]
                        elif isinstance(target, ast.Attribute) and node.args:
                            mode_node = node.args[0]
                    if mode_node is None:
                        if name == "fdopen":
                            classification = "dynamic_mode_review"
                        else:
                            continue  # Default open() is read-only.
                    elif not isinstance(mode_node, ast.Constant) or not isinstance(mode_node.value, str):
                        classification = "dynamic_mode_review"
                    elif any(flag in mode_node.value for flag in "wax+"):
                        classification = "write"
                    else:
                        continue
                elif name == "Popen" or name in ("run", "call", "check_call", "check_output", "system"):
                    classification = "dynamic_mode_review"
                elif name in operations:
                    classification = "write"
                else:
                    continue
                writer_calls.append({"file": module.relative_to(root).as_posix(),
                                     "line": node.lineno, "operation": name,
                                     "classification": classification})
                continue
    writer_calls.sort(key=lambda row: (row["file"], row["line"], row["operation"]))
    writer_by_module = {}
    for row in writer_calls:
        writer_by_module.setdefault(row["file"], {"write": 0, "dynamic_mode_review": 0})
        writer_by_module[row["file"]][row["classification"]] += 1
    # Never follow workflow symlinks when constructing the trusted inventory.
    workflow_entries = list(workflows.iterdir())
    if any(p.is_symlink() for p in workflow_entries):
        raise ValueError("Symlinked workflow entry")
    files = sorted(p.name for p in workflow_entries
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
        "ledger_sha256": ledger_sha256,
        "source_modules_inspected": len(source_fingerprints),
        "evidence_requirements_missing_tasks": evidence["requirements_missing_tasks"],
        "external_evidence_required_tasks": evidence["requires_external_evidence_tasks"],
        "writer_callsite_candidates": writer_calls,
        "writer_source_sha256": source_fingerprints,
        "writer_callsite_candidates_count": len(writer_calls),
        "writer_callsite_modules": writer_by_module,
        "writer_dynamic_mode_review_count": sum(row["classification"] == "dynamic_mode_review" for row in writer_calls),
        "all_writer_callsites_manually_verified": False,
        "writer_inventory_limitations": [
            "Static AST only; aliases, wrappers, subprocesses and dynamic calls require runtime review",
            "Source hashes bind the report to inspected Python bytes, not production behavior",
        ],
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
