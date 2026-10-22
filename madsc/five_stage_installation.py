"""Single read-only K1–K5 installation, task and parity inventory.

No Actions, network, protected playlist reads or production writes.
"""
from __future__ import annotations

import json
from pathlib import Path

from madsc.workflow_consolidation import consolidation_plan
from madsc.k1_k5_acceptance_requirements import assess_task_evidence
from madsc.legacy_parity_evidence import reconcile_legacy_scope
from madsc.parity_workflow_readiness import audit_parity_workflow_readiness


def assess_installation(root: str | Path) -> dict:
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Repository root must be a directory")
    plan = consolidation_plan(root)
    ledger = json.loads((root / "docs/K1_K5_KANITLI_GOREV_DEFTERI.json").read_text(encoding="utf-8"))
    tasks = assess_task_evidence(ledger)
    scope = reconcile_legacy_scope(json.loads(
        (root / "docs/LEGACY_SOURCE_SCOPE.json").read_text(encoding="utf-8")))
    readiness = audit_parity_workflow_readiness(root)
    if (len(plan["main_workflows"]) != 5
            or plan["auxiliary_count"] != 10
            or readiness["workflow_count"] != 5
            or tasks["total"] != 22
            or scope["legacy_behavior_workflows"] != 92
            or len(scope["excluded_from_92"]) != 7):
        raise ValueError("K1-K5 inventory drift")
    by_stage = {}
    for stage, workflow in plan["main_workflows"].items():
        rows = tasks["tasks"][stage]
        by_stage[stage] = {
            "workflow": ".github/workflows/" + workflow,
            "installed_static": True,
            "task_count": len(rows),
            "ledger_in_progress": sum(r["ledger_status"] == "in_progress" for r in rows),
            "ledger_pending": sum(r["ledger_status"] == "pending" for r in rows),
            "missing_evidence_task_ids": [r["id"] for r in rows if r["missing_evidence"]],
            "external_evidence_task_ids": [r["id"] for r in rows if r["requires_external_evidence"]],
            "runtime_verified": False,
            "production_accepted": False,
        }
    return {
        "schema": "madsc-five-stage-installation-inventory-v1",
        "stages": by_stage,
        "main_workflows_installed": 5,
        "auxiliary_commands_integrated": plan["commands_integrated_in_main"],
        "auxiliary_commands_expected": 10,
        "parity_static_markers_complete": readiness["marker_contract_complete"],
        "parity_static_file_bindings_complete": readiness["static_file_bindings_complete"],
        "external_live_input_blockers": readiness["external_or_live_input_blockers"],
        "legacy_source_workflows": scope["source_workflows"],
        "legacy_behavior_workflows": scope["legacy_behavior_workflows"],
        "legacy_behavior_accepted": 0,
        "task_count": tasks["total"],
        "tasks_with_missing_evidence": tasks["requirements_missing_tasks"],
        "runtime_security_rules_accepted": 0,
        "previous_project_progress_estimate_percent": 60,
        "current_project_progress_verified_percent": None,
        "all_stages_operationally_verified": False,
        "production_ready": False,
        "github_actions_triggered": False,
        "production_writes": False,
        "note": "Installed static workflows are not independently executed production behavior.",
    }


def main():
    root = Path(__file__).resolve().parent.parent
    print(json.dumps(assess_installation(root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
