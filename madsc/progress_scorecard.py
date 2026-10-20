"""Evidence-based project scorecard; never infer production acceptance from green CI."""
import argparse
import json
from pathlib import Path

BASELINE = {"overall_reference_completed_percent": 47,
            "overall_reference_remaining_percent": 53}
INVENTORY = {"legacy_yaml_source_review": {"done": 99, "total": 99},
             "legacy_python_source_inventory": {"done": 130, "total": 130},
             "legacy_python_test_inventory": {"done": 68, "total": 68}}
ACCEPTANCE = {"legacy_behavioral_equivalence": {"accepted": 0, "total": 92},
              "runtime_security_rules": {"accepted": 0, "total": 26}}


def scorecard(accepted_behaviors=0, accepted_security=0, verified_ci=False):
    if (type(accepted_behaviors) is not int or type(accepted_security) is not int
            or not 0 <= accepted_behaviors <= 92 or not 0 <= accepted_security <= 26
            or type(verified_ci) is not bool):
        raise ValueError("Invalid progress evidence")
    return {
        "schema": "madsc-evidence-scorecard-v1",
        "reference": dict(BASELINE),
        "source_inventory": INVENTORY,
        "acceptance": {
            "legacy_behavioral_equivalence": {"accepted": accepted_behaviors, "total": 92},
            "runtime_security_rules": {"accepted": accepted_security, "total": 26},
        },
        "five_system_ci": {"last_run_success_verified": verified_ci,
                           "scope": "offline workflow integration, not production acceptance"},
        "calculated_overall_percent": None,
        "reason": "No agreed weighted, verified end-to-end acceptance denominator exists",
        "production_ready": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verified-ci", action="store_true")
    args = parser.parse_args()
    if args.output.exists() or args.output.is_symlink():
        raise FileExistsError("Progress evidence cannot overwrite existing data")
    if args.output.parent.is_symlink():
        raise ValueError("Symlink output directory rejected")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as out:
        json.dump(scorecard(verified_ci=args.verified_ci), out, indent=2, sort_keys=True)
        out.write("\n")


if __name__ == "__main__":
    main()
