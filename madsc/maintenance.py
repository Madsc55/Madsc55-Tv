"""Pure functions for aggregate status and bounded retry decisions."""
from __future__ import annotations

def retry_decision(consecutive_failures: int, limit: int = 3) -> dict:
    if type(consecutive_failures) is not int or consecutive_failures < 0 or type(limit) is not int or not 1 <= limit <= 10:
        raise ValueError("Invalid failure count or retry limit")
    blocked = consecutive_failures >= limit
    return {"blocked": blocked, "next_action": "HALT_AND_REPORT" if blocked else "RETRY_LATER",
            "production_writes": False, "state_persisted": False}

def aggregate(reports: list[dict]) -> dict:
    if not isinstance(reports, list) or any(not isinstance(r, dict) for r in reports):
        raise ValueError("Invalid batch reports")
    categories = {report.get("category") for report in reports if isinstance(report.get("category"), str)}
    expected = {"k1", "k2", "k3", "k4", "k5"}
    complete = categories == expected and len(reports) == 5
    safe = complete and all(report.get("production_writes") is False for report in reports)
    successful = safe and all(report.get("status") == "success" for report in reports)
    return {"all_five_present": complete, "all_read_only": safe,
            "all_five_successful": successful,
            "all_reports_explicitly_read_only": safe,
            "production_ready": False, "runtime_evidence_verified": False}


def summarize_batch(reports: list[dict]) -> dict:
    """Read-only per-category failure summary for coordinated maintenance."""
    if not isinstance(reports, list) or any(not isinstance(r, dict) for r in reports):
        raise ValueError("Invalid batch reports")
    base = aggregate(reports)
    expected = {"k1", "k2", "k3", "k4", "k5"}
    failures = sorted(str(r.get("category", "unknown")) for r in reports
                      if r.get("status") != "success" or (not isinstance(r.get("category"), str) or r.get("category") not in expected))
    missing = sorted(expected - {r.get("category") for r in reports if isinstance(r.get("category"), str)})
    counts = {category: sum(r.get("category") == category for r in reports) for category in expected}
    duplicates = sorted(category for category, count in counts.items() if count > 1)
    unexpected = sum(not isinstance(r.get("category"), str) or r.get("category") not in expected for r in reports)
    unsafe = sorted(str(r.get("category", "unknown")) for r in reports
                    if r.get("production_writes") is not False)
    return {**base, "failed_categories": failures, "missing_categories": missing,
            "duplicate_categories": duplicates, "unexpected_category_count": unexpected,
            "unsafe_or_unverified_write_categories": unsafe,
            "requires_review": bool(failures) or bool(missing) or bool(duplicates) or bool(unexpected) or not base["all_read_only"],
            "production_writes": False}


def verify_fixture_evidence(reports: list[dict]) -> dict:
    """Require explicit, true fixture checks without claiming production validation."""
    summary = summarize_batch(reports)
    missing_evidence = []
    failed_checks = []
    for report in reports:
        category = str(report.get("category", "unknown"))
        checks = report.get("fixture_checks")
        if not isinstance(checks, dict) or not checks:
            missing_evidence.append(category)
        elif any(value is not True for value in checks.values()):
            failed_checks.append(category)
    return {**summary, "missing_fixture_evidence": sorted(missing_evidence),
            "failed_fixture_checks": sorted(failed_checks),
            "fixture_evidence_verified": not summary["requires_review"]
            and not missing_evidence and not failed_checks,
            "production_ready": False, "runtime_evidence_verified": False}


def review_candidate_batch(coordination: dict, backup_evidence: dict) -> dict:
    """K5 cross-check K2/K3 candidate decisions and K4 restore evidence.

    This is a read-only review package, never an authorization to modify lists.
    """
    if not isinstance(coordination, dict) or not isinstance(backup_evidence, dict):
        raise ValueError("Invalid cross-system evidence")
    candidates = coordination.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError("Missing K2/K3 candidates")
    seen = set()
    for item in candidates:
        if not isinstance(item, dict):
            raise ValueError("Malformed candidate evidence")
        digest = item.get("url_sha256")
        if (not isinstance(digest, str) or len(digest) != 64
                or any(c not in "0123456789abcdef" for c in digest) or digest in seen):
            raise ValueError("Invalid or repeated candidate identity")
        seen.add(digest)
        if (item.get("production_change_allowed") is not False
                or item.get("delete_allowed") is not False
                or type(item.get("hold")) is not bool
                or type(item.get("protected_working")) is not bool):
            raise ValueError("Unsafe candidate decision evidence")
    if (coordination.get("production_writes") is not False
            or coordination.get("production_ready") is not False
            or coordination.get("network_probed") is not False):
        raise ValueError("Unverified or unsafe coordination evidence")
    if (backup_evidence.get("production_writes") is not False
            or backup_evidence.get("production_restore_verified") is not False
            or backup_evidence.get("external_storage_proven") is not False):
        raise ValueError("Unsafe or overstated backup evidence")
    restore_matches = backup_evidence.get("independent_sandbox_restore_matches") is True
    return {
        "candidate_count": len(candidates),
        "held_count": sum(item["hold"] for item in candidates),
        "protected_ibo_working_count": sum(item["protected_working"] for item in candidates),
        "k4_independent_sandbox_restore_matches": restore_matches,
        "review_evidence_complete": restore_matches and bool(candidates),
        "production_ready": False, "production_writes": False,
        "device_verified": False, "external_storage_proven": False,
        "legacy_behavioral_equivalence_verified": False,
    }
