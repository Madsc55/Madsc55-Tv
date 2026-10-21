"""Fail-closed evidence requirements for all 22 K1-K5 tasks.

This module does not probe streams, run tests, launch Actions or alter the ledger.
"""
from __future__ import annotations

import json
from pathlib import Path

REQUIREMENTS = {
    "K1-01": ("runtime_rule_26_evidence",),
    "K1-02": ("production_file_before_after_hashes",),
    "K1-03": ("all_writer_callsite_inventory", "runtime_guard_enforcement"),
    "K1-04": ("security_task_18_of_18_evidence",),
    "K2-05": ("source_license_review", "source_reconciliation"),
    "K2-06": ("daily_trigger_equivalence", "discovery_output_provenance"),
    "K2-07": ("independent_artifact_sha256", "artifact_origin"),
    "K2-08": ("candidate_duplicate_alternative_differential",),
    "K3-09": ("75_candidate_timed_retests",),
    "K3-10": ("three_independent_samples_six_hours_apart", "continuity_measurements"),
    "K3-11": ("real_ffprobe_ffmpeg_evidence",),
    "K3-12": ("ibo_real_device_user_acceptance",),
    "K3-13": ("xmltv_tvg_id_live_pages_chain",),
    "K3-14": ("logo_visual_channel_identity",),
    "K4-15": ("independent_external_backup_receipt",),
    "K4-16": ("external_backup_isolated_restore",),
    "K4-17": ("vod_archive_behavioral_parity",),
    "K4-18": ("first_and_fifteenth_backup_trigger_parity",),
    "K5-19": ("92_of_92_behavioral_evidence",),
    "K5-20": ("real_end_to_end_evidence_chain",),
    "K5-21": ("timeout_retry_failure_artifact_parity",),
    "K5-22": ("turkish_final_acceptance_report",),
}
EXTERNAL_EVIDENCE = frozenset({
    "K1-02", "K2-05", "K2-06", "K2-07", "K3-09", "K3-10",
    "K3-11", "K3-12", "K3-13", "K3-14", "K4-15", "K4-16",
    "K4-17", "K4-18", "K5-19", "K5-20",
})


def assess_task_evidence(tasks: list[dict], verified: dict | None = None) -> dict:
    """Only independently verified evidence may satisfy a required key.

    verified maps task IDs to evidence-key -> literal True. A caller assertion
    is NOT independent verification, so this is a readiness checklist only.
    """
    if not isinstance(tasks, list) or len(tasks) != len(REQUIREMENTS):
        raise ValueError("Expected complete 22-task ledger")
    if verified is None:
        verified = {}
    if not isinstance(verified, dict) or set(verified) - REQUIREMENTS.keys():
        raise ValueError("Unknown evidence task")
    by_stage = {stage: [] for stage in ("K1", "K2", "K3", "K4", "K5")}
    seen = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("Invalid task")
        tid = task.get("id")
        if tid not in REQUIREMENTS or tid in seen or task.get("stage") != tid[:2]:
            raise ValueError("Unknown, duplicate or mismatched task")
        seen.add(tid)
        if task.get("status") not in ("pending", "in_progress", "completed"):
            raise ValueError("Invalid task status")
        supplied = verified.get(tid, {})
        if not isinstance(supplied, dict) or any(type(value) is not bool for value in supplied.values()):
            raise ValueError("Invalid evidence claims")
        if set(supplied) - set(REQUIREMENTS[tid]):
            raise ValueError("Unknown evidence requirement")
        missing = [key for key in REQUIREMENTS[tid] if supplied.get(key) is not True]
        by_stage[tid[:2]].append({
            "id": tid, "title": task.get("title"),
            "ledger_status": task["status"],
            "requires_external_evidence": tid in EXTERNAL_EVIDENCE,
            "missing_evidence": missing,
            "evidence_checklist_complete": not missing,
            "production_acceptance_proven_by_this_report": False,
        })
    if seen != REQUIREMENTS.keys():
        raise ValueError("Incomplete task ledger")
    rows = [row for group in by_stage.values() for row in group]
    return {
        "schema": "madsc-k1-k5-evidence-requirements-v1",
        "tasks": by_stage,
        "total": len(rows),
        "pending_in_ledger": sum(row["ledger_status"] == "pending" for row in rows),
        "in_progress_in_ledger": sum(row["ledger_status"] == "in_progress" for row in rows),
        "completed_in_ledger": sum(row["ledger_status"] == "completed" for row in rows),
        "requirements_missing_tasks": sum(bool(row["missing_evidence"]) for row in rows),
        "requires_external_evidence_tasks": sum(row["requires_external_evidence"] for row in rows),
        "production_ready": False,
        "github_actions_triggered": False,
        "tests_executed": False,
        "production_writes": False,
    }


def main() -> None:
    path = Path(__file__).resolve().parent.parent / "docs" / "K1_K5_KANITLI_GOREV_DEFTERI.json"
    tasks = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(assess_task_evidence(tasks), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
