"""Fail-closed aggregation of five isolated GitHub Actions category artifacts."""
from __future__ import annotations
import json
from pathlib import Path
from madsc.maintenance import verify_fixture_evidence

CATEGORIES = ("k1", "k2", "k3", "k4", "k5")
MODULES = {"k1": "security", "k2": "discovery", "k3": "channel_testing",
           "k4": "backup", "k5": "maintenance"}

def _unique_json_pairs(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON evidence key: {key}")
        result[key] = value
    return result


def collect(root: Path) -> dict:
    root = Path(root)
    if not root.is_dir() or root.is_symlink():
        raise ValueError("Evidence root must be a real directory")
    reports = {}
    evidence_reports = []
    expected_names = {key + ".json" for key in CATEGORIES}
    unexpected_json = sorted(str(path.relative_to(root)) for path in root.rglob("*.json")
                             if path.name not in expected_names)
    if unexpected_json:
        raise ValueError(f"Unexpected JSON evidence: {unexpected_json}")
    allowed_dirs = {f"madsc-batch-{key}" for key in CATEGORIES}
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Symlink evidence is forbidden: {path}")
        relative = path.relative_to(root)
        if (len(relative.parts) > 2 or relative.parts[0] not in allowed_dirs
                or (len(relative.parts) == 1 and not path.is_dir())
                or (len(relative.parts) == 2 and
                    (path.is_dir() or relative.name != relative.parts[0].removeprefix("madsc-batch-") + ".json"))):
            raise ValueError(f"Unexpected evidence package entry: {relative}")
    for key in CATEGORIES:
        matches = list(root.rglob(key + ".json"))
        if len(matches) != 1:
            raise ValueError(f"Expected exactly one report for {key}; got {len(matches)}")
        if (matches[0].parent.name != f"madsc-batch-{key}"
                or matches[0].is_symlink() or not matches[0].is_file()):
            raise ValueError(f"Invalid evidence file: {key}")
        data = json.loads(matches[0].read_text(encoding="utf-8"),
                          object_pairs_hook=_unique_json_pairs)
        if not isinstance(data, dict):
            raise ValueError(f"Invalid report object: {key}")
        if (data.get("category") != key
            or data.get("module") != MODULES[key]
            or data.get("mode") != "isolated_read_only"
            or data.get("production_writes") is not False
            or data.get("legacy_workflows_executed") is not False
            or data.get("status") != "isolated_fixture_checks_passed_not_production_verified"
            or not isinstance(data.get("fixture_checks"), dict)
            or not data["fixture_checks"]
            or not all(isinstance(k, str) and k and v is True
                       for k, v in data["fixture_checks"].items())
            or not isinstance(data.get("checks"), dict)
            or data["checks"].get("isolation") is not True
            or data["checks"].get("runtime_rule_evidence") is not False
            or data.get("checks", {}).get("legacy_behavioral_equivalence") is not False):
            raise ValueError(f"Invalid or unverified evidence: {key}")
        evidence_reports.append({"category": key, "status": "success",
                                 "production_writes": data["production_writes"],
                                 "fixture_checks": data["fixture_checks"]})
        reports[key] = {"status": data["status"], "module": MODULES[key],
                        "fixture_checks": len(data["fixture_checks"]),
                        "fixture_check_names": sorted(data["fixture_checks"])}
    verification = verify_fixture_evidence(evidence_reports)
    if not verification["fixture_evidence_verified"]:
        raise ValueError("K1-K5 fixture evidence verification failed")
    return {"category_order": list(CATEGORIES), "categories": reports,
            "k5_fixture_evidence_verified": verification["fixture_evidence_verified"],
            "five_isolated_reports_valid": True, "runtime_rules_verified": False,
            "legacy_92_behavioral_equivalence_verified": False,
            "ibo_device_verified": False, "external_restore_verified": False,
            "production_ready": False, "automatic_schedule_enabled": False}

def main() -> None:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--reports", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    result = collect(a.reports)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
