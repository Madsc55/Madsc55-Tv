"""Offline isolated five-stage fixture gate; no live acceptance."""
import json
from madsc.core import CATEGORIES, execute
from madsc.maintenance import verify_fixture_evidence


def assess_all(executor=None):
    executor = execute if executor is None else executor
    reports = []
    errors = {}
    for category in CATEGORIES:
        try:
            checks = executor(category)
            valid = isinstance(checks, dict) and bool(checks) and all(value is True for value in checks.values())
            if not valid:
                errors[category] = "invalid_fixture_evidence"
            reports.append({"category": category, "status": "success" if valid else "failure",
                            "production_writes": False, "fixture_checks": checks})
        except Exception as exc:
            errors[category] = type(exc).__name__
            reports.append({"category": category, "status": "failure",
                            "production_writes": False, "fixture_checks": {}})
    summary = verify_fixture_evidence(reports)
    required = set(CATEGORIES)
    if len(CATEGORIES) != 5 or len(required) != 5 or required != {"k1", "k2", "k3", "k4", "k5"}:
        errors["inventory"] = "invalid_five_stage_inventory"
    return {"categories_checked": len(reports),
            "categories": {item["category"]: item["status"] for item in reports},
            "fixture_gate_passed": not errors and summary["fixture_evidence_verified"],
            "errors": errors, "production_ready": False, "production_writes": False,
            "legacy_92_behavioral_acceptance": 0, "runtime_security_26_acceptance": 0}


def main():
    result = assess_all()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["fixture_gate_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
