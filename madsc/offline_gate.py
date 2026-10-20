"""Offline K1-K5 smoke gate; no GitHub Actions, network, secrets or billing.

Run from repository root: python -m madsc.offline_gate
"""
import json
import subprocess
import sys
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent.parent
    cmd = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
    result = subprocess.run(cmd, cwd=root, capture_output=True, text=True,
                            timeout=180, check=False)
    report = {
        "mode": "offline_local",
        "scope": "unit_regression_only",
        "production_acceptance": False,
        "legacy_92_behavioral_acceptance": 0,
        "runtime_security_26_acceptance": 0,
        "test_exit_code": result.returncode,
        "tests_passed": result.returncode == 0,
        "note": "Offline unit tests cannot certify live K1-K5 or production.",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if result.returncode:
        print(result.stdout[-12000:], file=sys.stderr)
        print(result.stderr[-12000:], file=sys.stderr)
    return 0 if result.returncode == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
