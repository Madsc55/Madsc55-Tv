"""Offline K1-K5 smoke gate; no GitHub Actions, network, secrets or billing.

Run from repository root: python -m madsc.offline_gate
"""
import json
import re
import subprocess
import sys
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent.parent
    cmd = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
    try:
        result = subprocess.run(cmd, cwd=root, capture_output=True, text=True,
                                timeout=180, check=False)
        exit_code = result.returncode
        stdout, stderr = result.stdout or "", result.stderr or ""
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        exit_code = 124
        timed_out = True
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
    # unittest can exit 0 after discovering zero tests: never accept that as green.
    matches = re.findall(r"Ran (\d+) tests? in", stderr + "\n" + stdout)
    test_count = int(matches[-1]) if matches else 0
    unittest_passed = exit_code == 0 and test_count > 0 and not timed_out
    if exit_code == 0 and test_count == 0:
        exit_code = 2
    # Require the real K1-K5 isolated executors, not only passing unit tests.
    from madsc.offline_five_gate import assess_all
    try:
        five_stage = assess_all()
        expected = {"k1", "k2", "k3", "k4", "k5"}
        categories = five_stage.get("categories")
        five_stage_passed = (five_stage.get("fixture_gate_passed") is True
                             and five_stage.get("categories_checked") == 5
                             and isinstance(categories, dict)
                             and set(categories) == expected
                             and all(categories[key] == "success" for key in expected)
                             and five_stage.get("production_ready") is False
                             and five_stage.get("production_writes") is False)
    except Exception as exc:
        five_stage = {"fixture_gate_passed": False, "errors": {"orchestration": type(exc).__name__}}
        five_stage_passed = False
    if not five_stage_passed and exit_code == 0:
        exit_code = 3
    # A green fixture is not enough: inventory all 15 manual workflows and
    # all 22 ledger tasks in the SAME offline invocation, fail closed on drift.
    try:
        from madsc.workflow_consolidation import consolidation_plan
        from madsc.k1_k5_acceptance_requirements import assess_task_evidence
        from madsc.legacy_parity_evidence import reconcile_legacy_scope
        legacy_scope = reconcile_legacy_scope(json.loads(
            (root / "docs" / "LEGACY_SOURCE_SCOPE.json").read_text(encoding="utf-8")))
        workflow_plan = consolidation_plan(root)
        ledger = json.loads((root / "docs" / "K1_K5_KANITLI_GOREV_DEFTERI.json").read_text(encoding="utf-8"))
        acceptance_plan = assess_task_evidence(ledger)
        inventory_passed = (workflow_plan["auxiliary_count"] == 10
                            and len(workflow_plan["main_workflows"]) == 5
                            and workflow_plan["commands_integrated_in_main"] == 10
                            and workflow_plan["all_ten_commands_integrated_in_main"] is True
                            and legacy_scope["legacy_behavior_workflows"] == 92
                            and len(legacy_scope["excluded_from_92"]) == 7
                            and acceptance_plan["total"] == 22
                            and acceptance_plan["production_ready"] is False)
    except Exception as exc:
        legacy_scope = {}
        workflow_plan = {"error": type(exc).__name__}
        acceptance_plan = {"error": type(exc).__name__}
        inventory_passed = False
    if not inventory_passed and exit_code == 0:
        exit_code = 4
    # The latest read-only installation inventory is a mandatory part of this gate.
    # This validates wiring and evidence gaps, never production acceptance.
    try:
        from madsc.five_stage_installation import assess_installation
        installation = assess_installation(root)
        installation_passed = (
            set(installation["stages"]) == {"K1", "K2", "K3", "K4", "K5"}
            and installation["main_workflows_installed"] == 5
            and installation["auxiliary_commands_integrated"] == 10
            and installation["legacy_behavior_workflows"] == 92
            and installation["task_count"] == 22
            and installation["production_ready"] is False
            and installation["github_actions_triggered"] is False
            and installation["production_writes"] is False
            and all(not stage["runtime_verified"] and not stage["production_accepted"]
                    for stage in installation["stages"].values()))
    except Exception as exc:
        installation = {"error": type(exc).__name__}
        installation_passed = False
    if not installation_passed and exit_code == 0:
        exit_code = 6
    # Verify actual report serialization and K5 consumption in the same gate.
    from madsc.offline_five_gate import assess_report_roundtrip
    try:
        roundtrip = assess_report_roundtrip()
        roundtrip_passed = (roundtrip.get("passed") is True
                            and roundtrip.get("reports_written") == 5
                            and roundtrip.get("consumer_preserved_report_bytes") is True
                            and roundtrip.get("production_ready") is False)
    except Exception as exc:
        roundtrip = {"error": type(exc).__name__}
        roundtrip_passed = False
    if not roundtrip_passed and exit_code == 0:
        exit_code = 5
    report = {
        "mode": "offline_local",
        "scope": "unit_regression_and_isolated_five_stage_fixture",
        "production_acceptance": False,
        "legacy_92_behavioral_acceptance": 0,
        "runtime_security_26_acceptance": 0,
        "test_exit_code": exit_code,
        "timed_out": timed_out,
        "tests_discovered": test_count,
        "tests_passed": unittest_passed,
        "five_stage_fixture_gate_passed": five_stage_passed,
        "all_offline_gates_passed": unittest_passed and five_stage_passed and inventory_passed and roundtrip_passed and installation_passed,
        "five_stage_installation_inventory_passed": installation_passed,\n        "five_stage_installation_inventory_error": installation.get("error"),
        "five_report_roundtrip_passed": roundtrip_passed,
        "five_report_roundtrip": roundtrip,
        "workflow_and_task_inventory_passed": inventory_passed,
        "auxiliary_workflows_mapped": workflow_plan.get("auxiliary_count"),
        "auxiliary_commands_integrated_in_main": workflow_plan.get("commands_integrated_in_main"),
        "task_requirements_inventoried": acceptance_plan.get("total"),
        "legacy_scope_source_workflows": legacy_scope.get("source_workflows"),
        "legacy_scope_behavior_workflows": legacy_scope.get("legacy_behavior_workflows"),
        "legacy_scope_excluded": legacy_scope.get("excluded_from_92"),
        "workflow_inventory_error": workflow_plan.get("error"),
        "task_inventory_error": acceptance_plan.get("error"),
        "five_stage_fixture_categories": five_stage.get("categories", {}),
        "five_stage_fixture_errors": five_stage.get("errors", {}),
        "note": "Unit tests AND real isolated K1-K5 fixture gate required; never production certification.",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if exit_code:
        print(stdout[-12000:], file=sys.stderr)
        print(stderr[-12000:], file=sys.stderr)
    return 0 if exit_code == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
