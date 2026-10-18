"""Execute actual isolated category checks against bundled nonproduction fixtures."""
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from madsc.backup import snapshot_manifest, verify_manifest
from madsc.channel_test import evaluate_probe
from madsc.discovery import classify_candidates
from madsc.maintenance import aggregate, retry_decision
from madsc.playlist import compare_snapshots, inspect_playlist

CATEGORIES = {"k1": "security", "k2": "discovery", "k3": "channel_testing", "k4": "backup", "k5": "maintenance"}
PROTECTED = ("CALISANLAR.m3u", "YENILER", "YEDEKLER", "HEPSI", "FAVORILER", "epg/", "logolar/")

def execute(category: str) -> dict:
    if category == "k1":
        with TemporaryDirectory() as d:
            p = Path(d) / "sample.m3u"
            p.write_text("#EXTM3U\n#EXTINF:-1,Sample\nhttps://example.org/live\n", encoding="utf-8")
            original = p.read_bytes()
            before = inspect_playlist(p)
            after = inspect_playlist(p)
            evidence = {"valid_playlist": before["channel_count"] == 1,
                        "no_playlist_mutation": original == p.read_bytes(),
                        "integrity_comparison": compare_snapshots(before, after)["identical"]}
    elif category == "k2":
        result = classify_candidates([
            {"name": "Sample", "url": "https://example.org/live"},
            {"name": "Duplicate", "url": "https://example.org/live"},
            {"name": "Invalid", "url": "file:///invalid"},
        ])
        evidence = {"unique_candidates": len(result["candidates"]) == 1,
                    "duplicates_separated": len(result["duplicates"]) == 1,
                    "invalid_rejected": len(result["rejected"]) == 1}
    elif category == "k3":
        result = evaluate_probe({"url_sha256": "a" * 64, "http_status": 200,
                                 "video": True, "audio": True, "duration_seconds": 40})
        evidence = {"preliminary_classification": result["technical_status"] == "PRELIMINARY_PASS",
                    "no_device_approval": not result["ibo_device_verified"],
                    "no_production_approval": not result["production_change_allowed"]}
    elif category == "k4":
        with TemporaryDirectory() as d:
            p = Path(d) / "sample.txt"
            p.write_text("fixture", encoding="utf-8")
            manifest = snapshot_manifest(Path(d), ["sample.txt"])
            evidence = {"manifest_integrity": verify_manifest(Path(d), manifest),
                        "external_backup_not_claimed": not manifest["external_backup_verified"],
                        "restore_not_claimed": not manifest["restore_verified"]}
    elif category == "k5":
        reports = [{"category": k, "production_writes": False} for k in CATEGORIES]
        result = aggregate(reports)
        evidence = {"five_categories": result["all_five_present"],
                    "read_only": result["all_read_only"],
                    "failure_limit": retry_decision(3)["blocked"],
                    "production_not_approved": not result["production_ready"]}
    else:
        raise ValueError("Unknown category")
    return evidence

def run(category: str, output: Path) -> dict:
    if category not in CATEGORIES:
        raise ValueError("Unknown category")
    evidence = execute(category)
    if not all(evidence.values()):
        raise RuntimeError("Isolated check failed; fail closed")
    report = {
        "category": category, "module": CATEGORIES[category],
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "isolated_read_only", "production_writes": False,
        "legacy_workflows_executed": False,
        "status": "isolated_fixture_checks_passed_not_production_verified",
        "protected_targets": list(PROTECTED), "fixture_checks": evidence,
        "checks": {"isolation": True, "runtime_rule_evidence": False,
                   "legacy_behavioral_equivalence": False},
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
