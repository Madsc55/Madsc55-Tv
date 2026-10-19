"""Execute actual isolated category checks against bundled nonproduction fixtures."""
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from madsc.backup import snapshot_manifest, verify_manifest, compare_copy
from madsc.channel_test import evaluate_probe
from madsc.discovery import classify_candidates
from madsc.dependencies import validate_batch, plan_task
from madsc.maintenance import aggregate, retry_decision
from madsc.playlist import compare_snapshots, inspect_playlist
from madsc.source_import import extract_candidates
from madsc.handoff import assess_candidates

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
        with TemporaryDirectory() as d:
            results = []
            for suffix in (".m3u", ".m3u8"):
                p = Path(d) / ("sample" + suffix)
                p.write_text("#EXTM3U\\n#EXTINF:-1,Sample\\nhttps://example.org/live.m3u8\\n#EXTINF:-1,Duplicate\\nhttps://example.org/live.m3u8\\n#EXTINF:-1,Invalid\\nfile:///invalid\\n".replace("\\n", "\n"), encoding="utf-8")
                before = p.read_bytes()
                result = extract_candidates(p)
                results.append((result, before == p.read_bytes()))
            evidence = {
                "both_m3u_and_m3u8": {r["source_format"] for r, _ in results} == {".m3u", ".m3u8"},
                "unique_candidates": all(len(r["candidates"]) == 1 for r, _ in results),
                "source_inventory_reconciled": all(r["source_channel_count"] == r["accepted_channel_count"] + r["duplicate_channel_count"] + r["rejected_channel_count"] for r, _ in results),
                "duplicates_separated": all(len(r["duplicates"]) == 1 for r, _ in results),
                "invalid_rejected": all(len(r["rejected"]) == 1 for r, _ in results),
                "sources_unchanged": all(ok for _, ok in results),
                "no_production_mutation": all(not r["production_playlist_modified"] for r, _ in results),
            }
    elif category == "k3":
        result = evaluate_probe({"url_sha256": "a" * 64, "http_status": 200,
                                 "video": True, "audio": True, "duration_seconds": 40})
        evidence = {"preliminary_classification": result["technical_status"] == "PRELIMINARY_PASS",
                    "no_device_approval": not result["ibo_device_verified"],
                    "no_production_approval": not result["production_change_allowed"]}
        with TemporaryDirectory() as d:
            p = Path(d) / "sample.m3u8"
            p.write_text("#EXTM3U\n#EXTINF:-1,Sample\nhttps://example.org/live.m3u8\n", encoding="utf-8")
            original = p.read_bytes()
            discovery = extract_candidates(p)
            digest = discovery["candidates"][0]["url_sha256"]
            handoff = assess_candidates(discovery, {digest: {"url_sha256": digest, "http_status": 200,
                                   "video": True, "audio": True, "duration_seconds": 40}})
            evidence["k2_to_k3_handoff"] = handoff["candidate_count"] == 1
            evidence["preliminary_not_approved"] = (handoff["assessed"][0]["technical_status"] == "PRELIMINARY_PASS"
                and not handoff["assessed"][0]["production_change_allowed"])
            evidence["handoff_read_only"] = original == p.read_bytes() and not handoff["production_playlist_modified"]
            failed = {"url_sha256": digest, "http_status": 503,
                      "video": False, "audio": False, "duration_seconds": 0}
            protected = assess_candidates(discovery, {digest: failed}, {digest: "WORKING"})
            decision = protected["assessed"][0]
            evidence["ibo_working_survives_technical_failure"] = (
                decision["technical_status"] == "NEEDS_REVIEW"
                and decision["ibo_result"] == "WORKING"
                and decision["protected_working"]
                and not decision["delete_allowed"]
                and not decision["production_change_allowed"])
            evidence["ibo_fixture_not_live_device_evidence"] = (
                not protected["network_probed"] and not protected["production_playlist_modified"])

    elif category == "k4":
        with TemporaryDirectory() as d:
            p = Path(d) / "sample.txt"
            p.write_text("fixture", encoding="utf-8")
            manifest = snapshot_manifest(Path(d), ["sample.txt"])
            with TemporaryDirectory() as copy_dir:
                (Path(copy_dir) / "sample.txt").write_bytes(p.read_bytes())
                copy_ok = compare_copy(Path(d), Path(copy_dir), ["sample.txt"])
            evidence = {"sandbox_copy_integrity": copy_ok,
                        "manifest_integrity": verify_manifest(Path(d), manifest),
                        "external_backup_not_claimed": not manifest["external_backup_verified"],
                        "restore_not_claimed": not manifest["restore_verified"]}
    elif category == "k5":
        reports = [{"category": k, "production_writes": False} for k in CATEGORIES]
        result = aggregate(reports)
        coordination = validate_batch(["candidate_discovery", "channel_assessment", "backup_restore", "schedule_collision"])
        evidence = {"five_categories": result["all_five_present"],
                    "read_only": result["all_read_only"],
                    "failure_limit": retry_decision(3)["blocked"],
                    "production_not_approved": not result["production_ready"],
                    "cross_category_handoff": plan_task("candidate_discovery")["involved_categories"] == ["k2", "k3", "k4", "k5"],
                    "single_batch_no_extra_triggers": coordination["independent_extra_triggers"] == 0,
                    "no_schedule_activation": all(not task["schedule_activation_allowed"] for task in coordination["tasks"]),
                    "no_legacy_shutdown": all(not task["legacy_workflows_disabled"] for task in coordination["tasks"])}
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
