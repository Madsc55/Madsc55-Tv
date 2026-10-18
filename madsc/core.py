"""Isolated read-only runner for five MADSC categories."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

CATEGORIES = {"k1": "security", "k2": "discovery", "k3": "channel_testing", "k4": "backup", "k5": "maintenance"}
PROTECTED = ("CALISANLAR.m3u", "YENILER", "YEDEKLER", "HEPSI", "FAVORILER", "epg/", "logolar/")

def run(category: str, output: Path) -> dict:
    if category not in CATEGORIES:
        raise ValueError("Unknown category")
    report = {
        "category": category,
        "module": CATEGORIES[category],
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "isolated_read_only",
        "production_writes": False,
        "legacy_workflows_executed": False,
        "status": "scaffold_only_not_behaviorally_verified",
        "protected_targets": list(PROTECTED),
        "checks": {"isolation": True, "runtime_rule_evidence": False, "legacy_behavioral_equivalence": False},
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", choices=sorted(CATEGORIES), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.category, args.output), ensure_ascii=False))

if __name__ == "__main__":
    main()
