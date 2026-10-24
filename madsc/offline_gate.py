"""Offline K1-K5 smoke gate; no GitHub Actions, network, secrets or billing.

Run from repository root: python -m madsc.offline_gate
"""
import json
import re
import subprocess
import sys
from pathlib import Path


def enforce_offline_unittest_process(command, root: Path) -> None:
    """Fail closed unless the child is the fixed local unittest discovery."""
    expected = [sys.executable, "-B", "-m", "unittest", "discover",
                "-s", "tests", "-v"]
    repository = Path(__file__).resolve().parent.parent
    root = Path(root)
    tests = root / "tests"
    if (command != expected or not root.is_absolute() or root.is_symlink()
            or root.resolve(strict=True) != repository
            or tests.is_symlink() or not tests.is_dir()
            or tests.resolve(strict=True) != repository / "tests"):
        raise PermissionError("Unsafe offline unittest subprocess contract")

def main():
    root = Path(__file__).resolve().parent.parent
    cmd = [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"]
    enforce_offline_unittest_process(cmd, root)
    try:
        result = subprocess.run(cmd, cwd=root, capture_output=True, text=True,
                                timeout=180, check=False, stdin=subprocess.DEVNULL)
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
    except OSError as exc:
        exit_code = 125
        timed_out = False
        stdout = ""
        stderr = f"unittest launch failed: {type(exc).__name__}: {exc}"
    # unittest can exit 0 after discovering zero tests: never accept that as green.
    matches = re.findall(r"Ran (\d+) tests? in", stderr + "\n" + stdout)
    test_count = int(matches[-1]) if matches else 0
    unittest_passed = exit_code == 0 and test_count > 0 and not timed_out
    if exit_code == 0 and test_count == 0:
        exit_code = 2
    # Require the real K1-K5 isolated executors, not only passing unit tests.
    try:
        from madsc.offline_five_gate import assess_all
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
        from madsc.workflow_consolidation import consolidation_plan, contract_gate
        from madsc.k1_k5_acceptance_requirements import assess_task_evidence
        from madsc.legacy_parity_evidence import reconcile_legacy_scope
        legacy_scope = reconcile_legacy_scope(json.loads(
            (root / "docs" / "LEGACY_SOURCE_SCOPE.json").read_text(encoding="utf-8")))
        workflow_plan = consolidation_plan(root)
        operational_contract = contract_gate(root)
        ledger = json.loads((root / "docs" / "K1_K5_KANITLI_GOREV_DEFTERI.json").read_text(encoding="utf-8"))
        acceptance_plan = assess_task_evidence(ledger)
        inventory_passed = (operational_contract["pass"] is True
                            and workflow_plan["auxiliary_count"] == 10
                            and len(workflow_plan["main_workflows"]) == 5
                            and workflow_plan["commands_integrated_in_main"] == 10
                            and workflow_plan["all_ten_commands_integrated_in_main"] is True
                            and legacy_scope["legacy_behavior_workflows"] == 92
                            and len(legacy_scope["excluded_from_92"]) == 7
                            and acceptance_plan["total"] == 22
                            and acceptance_plan["production_ready"] is False)
    except Exception as exc:
        operational_contract = {"pass": False, "error": type(exc).__name__}
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
    try:
        from madsc.offline_five_gate import assess_report_roundtrip
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
    # Read-only K1 write-callsite inventory. Findings are review candidates,
    # not proof of enforcement; any parse failure blocks the offline gate.
    try:
        from madsc.write_callsite_audit import scan_python_tree
        write_callsite_inventory = scan_python_tree(root)
        write_callsite_audit_passed = write_callsite_inventory.get("schema") == "madsc-k1-write-callsite-inventory-v2"
    except Exception as exc:
        write_callsite_inventory = {"error": type(exc).__name__, "runtime_gate_enforced": False}
        write_callsite_audit_passed = False
    if not write_callsite_audit_passed and exit_code == 0:
        exit_code = 7
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
        "all_offline_gates_passed": unittest_passed and five_stage_passed and inventory_passed and roundtrip_passed and installation_passed and write_callsite_audit_passed,
        "five_stage_installation_inventory_passed": installation_passed,
        "five_stage_installation_inventory_error": installation.get("error"),
        "five_report_roundtrip_passed": roundtrip_passed,
        "five_report_roundtrip": roundtrip,
        "write_callsite_audit_passed": write_callsite_audit_passed,
        "write_callsite_files_scanned": write_callsite_inventory.get("files_scanned", 0),
        "write_callsite_candidate_count": write_callsite_inventory.get("candidate_callsite_count", 0),
        "write_callsite_inventory": write_callsite_inventory,
        "workflow_and_task_inventory_passed": inventory_passed,
        "operational_contract_gate": operational_contract,
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
