"""Execute actual isolated category checks against bundled nonproduction fixtures."""
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from madsc.backup import snapshot_manifest, verify_manifest, compare_copy, verify_sandbox_restore, verify_independent_restore
from madsc.channel_test import evaluate_probe, evaluate_repeated_probes, evaluate_ffprobe_json
from madsc.discovery import classify_candidates
from madsc.dependencies import validate_batch, plan_task
from madsc.maintenance import aggregate, retry_decision, summarize_batch, review_candidate_batch, assess_failure_history
from madsc.playlist import compare_snapshots, inspect_playlist
from madsc.source_import import extract_candidates
from madsc.handoff import assess_candidates
from madsc.epg_inventory import inspect_xmltv
from madsc.legacy_epg_logo import join_pilot
from madsc.legacy_retest_390 import evaluate_entries, parse_entries
from madsc.candidate_coordination import coordinate
from madsc.write_path_audit import audit_write_paths, enforce_local_output_path
from madsc.fixture_report_writer import write_fixture_report, write_stage_report
from madsc.history_pair_bridge import bridge_legacy_pair, merge_into_envelope
from madsc.history_pair_store import decode_pair
from madsc.legacy_workflow_safety import assess_workflow_source
from madsc.legacy_parity_evidence import compare_provenance_bound_batch

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
            audit = audit_write_paths(["CALISANLAR.m3u", "epg/sample.xml", "reports/fixture.json"])
            safe_report = write_fixture_report(Path(d), "reports/k1.json", '{"isolated":true}')
            try:
                write_fixture_report(Path(d), "CALISANLAR.m3u", "blocked")
                denied = False
            except PermissionError:
                denied = True
            guard_verified = (safe_report["isolated_report_written"]
                              and not safe_report["production_write_allowed"]
                              and denied and not (Path(d) / "CALISANLAR.m3u").exists())
            metadata_denied = True
            for name in ("reports/favorites.json", "reports/HEPSI.txt", "reports/cache/logos/logo.png"):
                try:
                    write_fixture_report(Path(d), name, "blocked")
                    metadata_denied = False
                except PermissionError:
                    metadata_denied = metadata_denied and not (Path(d) / name).exists()
            evidence = {"fixture_report_write_guard": guard_verified,
                        "favorite_metadata_and_nested_logo_write_denied": metadata_denied,
                        "protected_write_paths_identified": audit["blocked"] and len(audit["rejected"]) == 2,
                        "audit_does_not_claim_runtime_gate": not audit["runtime_gate_enforced"],
                        "valid_playlist": before["channel_count"] == 1,
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
            legacy = Path(d) / "legacy_history"
            legacy.mkdir()
            first = {"gecmis.json": {"history": {"fixture": {"last_test": "2026-10-19T12:00:00Z", "runs": 1, "last_result": "PASS", "decision": "MANUAL_ONLY"}}},
                     "ana_liste_test_gecmisi.json": {"channels": {"fixture": {"last_test": "2026-10-19T12:00:00Z", "runs": 1, "last_result": "PASS", "decision": "MANUAL_ONLY"}}}}
            for name, doc in first.items():
                (legacy / name).write_text(json.dumps(doc), encoding="utf-8")
            original_history = {name: (legacy / name).read_bytes() for name in first}
            envelope = Path(d) / "history-pair.json"
            bridge_legacy_pair(legacy, envelope)
            incoming = {name: {key: {"fixture": {"last_test": "2026-10-20T12:00:00Z", "runs": 2, "last_result": "FAIL"}}}
                        for name, key in (("gecmis.json", "history"), ("ana_liste_test_gecmisi.json", "channels"))}
            merge_into_envelope(envelope, incoming)
            stored = decode_pair(envelope.read_text(encoding="utf-8"))
            history_bridge_ok = all(stored[name][key]["fixture"]["last_result"] == "FAIL"
                                    and stored[name][key]["fixture"]["decision"] == "MANUAL_ONLY"
                                    and (legacy / name).read_bytes() == original_history[name]
                                    for name, key in (("gecmis.json", "history"), ("ana_liste_test_gecmisi.json", "channels")))
            evidence = {
                "legacy_history_bridge_isolated": history_bridge_ok,
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
        repeated = evaluate_repeated_probes([{"url_sha256": "a" * 64, "http_status": 200,
                 "video": True, "audio": True, "duration_seconds": 40}] * 2)
        parsed = evaluate_ffprobe_json({"streams": [{"codec_type": "video"}, {"codec_type": "audio"}],
                                        "format": {"duration": "40"}}, "a" * 64)
        evidence = {"ffprobe_json_fixture_not_live": parsed["ffprobe_json_parsed"] and not parsed["live_probe_executed_by_this_function"],
                    "repeated_measurements_fixture_only": repeated["stable_preliminary"] and not repeated["actual_network_measurements_verified"],
                    "preliminary_classification": result["technical_status"] == "PRELIMINARY_PASS",
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
            xml = Path(d) / "epg.xml"
            xml.write_text('<tv><channel id="sample.tv"/><programme channel="sample.tv"/></tv>', encoding="utf-8")
            epg = inspect_xmltv(xml, {"sample.tv"})
            evidence["xmltv_id_matching"] = epg["matched_playlist_ids"] == 1 and epg["orphaned_programmes"] == 0 and not epg["device_verified"]
            evidence["ibo_report_not_device_verified"] = (decision["ibo_result_supplied"]
                and not decision["ibo_device_verified"] and decision["protected_working"])
            evidence["ibo_fixture_not_live_device_evidence"] = (
                not protected["network_probed"] and not protected["production_playlist_modified"])
            pilot = Path(d) / "pilot.xml"
            pilot.write_text('<tv><channel id="fixture.tv"/><programme channel="fixture.tv"/></tv>', encoding="utf-8")
            pilot_original = pilot.read_bytes()
            joined = join_pilot(
                [{"channel": "Fixture", "channel_id": "fixture.tv", "stream_sha256": digest}],
                [{"stream_sha256": digest, "status": "PREPARED", "visual_match": "NOT_VERIFIED"}], pilot)
            item = joined["candidate_results"][0]
            evidence["legacy_epg_logo_pilot_join"] = (
                item["epg_pilot_status"] == "PILOT_MATCH_WITH_PROGRAMMES"
                and item["logo_status"] == "PREPARED"
                and not item["playlist_approved"] and not item["ready_for_playlist"]
                and not joined["production_ready"] and pilot_original == pilot.read_bytes())
            from types import SimpleNamespace
            def offline_runner(args, **kwargs):
                return SimpleNamespace(returncode=0, stderr="",
                                       stdout="video\\naudio\\n" if args[0] == "ffprobe" else "")
            retest = evaluate_entries(parse_entries(
                '#EXTM3U\\n#EXTINF:-1,Fixture\\nhttps://example.invalid/fixture\\n'.replace('\\n', '\n')),
                runner=offline_runner, workers=2)
            evidence["legacy_390_offline_decode_contract"] = (
                retest["technical_pass_count"] == 1
                and "TEKNIK_VIDEO_SES_20SN" in retest["csv_text"]
                and not retest["identity_verified"] and not retest["production_ready"]
                and not retest["production_writes"])

    elif category == "k4":
        with TemporaryDirectory() as d:
            p = Path(d) / "sample.txt"
            p.write_text("fixture", encoding="utf-8")
            manifest = snapshot_manifest(Path(d), ["sample.txt"])
            with TemporaryDirectory() as copy_dir:
                (Path(copy_dir) / "sample.txt").write_bytes(p.read_bytes())
                copy_ok = compare_copy(Path(d), Path(copy_dir), ["sample.txt"])
                restore_audit = verify_sandbox_restore(Path(d), Path(copy_dir), ["sample.txt"])
                with TemporaryDirectory() as third_dir:
                    (Path(third_dir) / "sample.txt").write_bytes(p.read_bytes())
                    independent = verify_independent_restore(Path(d), Path(copy_dir), Path(third_dir), ["sample.txt"])
            evidence = {"three_tree_restore_fixture": independent["independent_sandbox_restore_matches"] and not independent["external_storage_proven"],
                        "independent_restore_reports_no_production_proof": (
                            independent["backup_verified_against_source"]
                            and independent["restore_verified_against_backup"]
                            and independent["files_checked"] == 1
                            and independent["production_restore_verified"] is False
                            and independent["production_writes"] is False),
                        "sandbox_restore_audit": restore_audit["sandbox_restore_matches"] and not restore_audit["production_restore_verified"],
                        "sandbox_copy_integrity": copy_ok,
                        "manifest_integrity": verify_manifest(Path(d), manifest),
                        "external_backup_not_claimed": not manifest["external_backup_verified"],
                        "restore_not_claimed": not manifest["restore_verified"]}
    elif category == "k5":
        source_catalog = json.loads((Path(__file__).resolve().parents[1] /
                                    "docs/LEGACY_SOURCE_SCOPE.json").read_text(encoding="utf-8"))
        pair_preparation = compare_provenance_bound_batch(source_catalog, {},
            replacement_workflow_root=Path(__file__).resolve().parents[1])
        history_rows = [{"id": i, "head_branch": "fixture", "created_at": "2026-10-22T00:00:00Z",
                         "status": "in_progress" if i == 104 else "completed",
                         "conclusion": None if i == 104 else "failure"} for i in range(104, 4, -1)]
        old_failures = [{"id": i, "head_branch": "fixture", "created_at": "2026-10-22T00:00:00Z",
                         "status": "completed", "conclusion": "failure"} for i in (4, 3, 2)]
        history_result = assess_failure_history([
            {"total_count": 103, "workflow_runs": history_rows},
            {"total_count": 103, "workflow_runs": old_failures}], current_run_id=104, branch="fixture")
        source_scope = assess_workflow_source("jobs:\n  check:\n    steps:\n"
            "      - run: python3 tools/workflow_failure_gate.py\n"
            "  writer:\n    steps:\n      - run: git push origin main\n")
        reports = [{"category": k, "production_writes": False} for k in CATEGORIES]
        result = aggregate([{**r, "status": "success"} for r in reports])
        summary = summarize_batch([{**r, "status": "success"} for r in reports])
        coordination = validate_batch(["candidate_discovery", "channel_assessment", "backup_restore", "schedule_collision"])
        fixture_rows = [{"name": "Fixture", "url": "https://example.org/fixture.m3u8",
                         "tvg_id": "fixture.tv"}]
        fixture_digest = classify_candidates(fixture_rows)["candidates"][0]["url_sha256"]
        candidate_report = coordinate(
            fixture_rows,
            {fixture_digest: {"url_sha256": fixture_digest, "http_status": 200,
                              "video": True, "audio": True, "duration_seconds": 40}},
            {}, {"fixture.tv"}, {"fixture.tv"})
        candidate_item = candidate_report["candidates"][0]
        handoff_report = assess_candidates(classify_candidates(fixture_rows),
            {fixture_digest: {"url_sha256": fixture_digest, "http_status": 200,
                              "video": True, "audio": True, "duration_seconds": 40}})
        handoff_item = handoff_report["assessed"][0]
        with TemporaryDirectory() as source_dir, TemporaryDirectory() as backup_dir, TemporaryDirectory() as restored_dir:
            for directory in (source_dir, backup_dir, restored_dir):
                (Path(directory) / "fixture.txt").write_text("isolated-k4", encoding="utf-8")
            k4_review = verify_independent_restore(
                Path(source_dir), Path(backup_dir), Path(restored_dir), ["fixture.txt"])
            (Path(restored_dir) / "fixture.txt").write_text("corrupted-restore", encoding="utf-8")
            k4_corrupt_review = verify_independent_restore(
                Path(source_dir), Path(backup_dir), Path(restored_dir), ["fixture.txt"])
        cross_system_review = review_candidate_batch(candidate_report, k4_review)
        corrupted_cross_review = review_candidate_batch(candidate_report, k4_corrupt_review)
        with TemporaryDirectory() as evidence_dir:
            k5_payload = {"category": "k5", "production_writes": False,
                          "production_ready": False, "review": cross_system_review}
            guarded_report = write_stage_report(Path(evidence_dir), "k5", k5_payload)
            saved_report = json.loads(
                (Path(evidence_dir) / guarded_report["relative_path"]).read_text(encoding="utf-8"))
            try:
                write_stage_report(Path(evidence_dir), "k5",
                                   {"category": "k5", "production_writes": True,
                                    "production_ready": False})
                rejected_unsafe = False
            except ValueError:
                rejected_unsafe = True
            try:
                write_stage_report(Path(evidence_dir), "k5", k5_payload)
                rejected_overwrite = False
            except FileExistsError:
                rejected_overwrite = True
        guarded_handoff_ok = (saved_report == k5_payload and rejected_unsafe
                              and rejected_overwrite and guarded_report["production_write_allowed"] is False)
        evidence = {"k1_guards_k5_report_write": guarded_handoff_ok,
                    "all_92_pair_requirements_bound_without_acceptance": (
                        pair_preparation["pair_preparation_rows"] == 92
                        and pair_preparation["replacement_contract_catalog_checked"]
                        and pair_preparation["replacement_contract_catalog"]["workflow_count"] == 5
                        and pair_preparation["missing_pairs"] == 92
                        and pair_preparation["behavioral_parity_accepted"] == 0
                        and all(row["pair_preparation"]["catalog_identity_bound"]
                                and row["pair_preparation"]["independent_evidence_missing"]
                                for row in pair_preparation["rows"])),
                    "paginated_failure_history_blocks_retry": history_result["blocked"] and not history_result["runtime_history_origin_verified"],
                    "separate_job_gate_not_false_writer_clearance": source_scope["mutation_signal_count"] == 1 and not source_scope["runtime_verified"],
                    "k4_corruption_blocks_k5_review": (
                        not k4_corrupt_review["independent_sandbox_restore_matches"]
                        and not corrupted_cross_review["review_evidence_complete"]
                        and not corrupted_cross_review["production_ready"]),
                    "k2_k3_k4_k5_candidate_restore_review": (
                        cross_system_review["review_evidence_complete"]
                        and cross_system_review["candidate_count"] == 1
                        and cross_system_review["held_count"] == 1
                        and not cross_system_review["production_ready"]
                        and not cross_system_review["production_writes"]),
                    "candidate_k2_k3_k5_consistent": (
                        handoff_item["url_sha256"] == candidate_item["url_sha256"]
                        and handoff_item["technical_status"] == candidate_item["technical_status"]
                        and handoff_item["tvg_id"] == candidate_item["tvg_id"]
                        and not handoff_item["production_change_allowed"]
                        and not handoff_report["production_playlist_modified"]),
                    "candidate_k2_k3_k5_join": candidate_item["score"] == 80 and candidate_item["hold"] and candidate_item["ibo_review_required"],
                    "candidate_metadata_counts": candidate_report["epg_matched"] == 1 and candidate_report["logo_matched"] == 1,
                    "candidate_report_read_only": candidate_report["production_writes"] is False and candidate_report["production_ready"] is False,
                    "batch_failure_summary": not summary["requires_review"] and not summary["failed_categories"],
                    "five_categories": result["all_five_present"],
                    "five_fixture_reports_successful": result["all_five_successful"],
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
    # Fail closed: never overwrite evidence or follow a symlinked output path.
    output = Path(output).absolute()
    if output.parent.name == "reports" and not output.parent.exists():
        if output.parent.parent.is_symlink() or not output.parent.parent.is_dir():
            raise PermissionError("Unsafe reports root")
        output.parent.mkdir()
    enforce_local_output_path(output)
    with output.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", choices=sorted(CATEGORIES), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.category, args.output), ensure_ascii=False))

if __name__ == "__main__":
    main()
