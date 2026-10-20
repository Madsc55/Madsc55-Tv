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
    report = {
        "mode": "offline_local",
        "scope": "unit_regression_and_isolated_five_stage_fixture",
        "production_acceptance": False,
        "legacy_92_behavioral_acceptance": 0,
        "runtime_security_26_acceptance": 0,
        "test_exit_code": exit_code,
        "timed_out": timed_out,
        "tests_discovered": test_count,
        "tests_passed": test_count > 0 and not timed_out and exit_code in (0, 3),
        "five_stage_fixture_gate_passed": five_stage_passed,
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
