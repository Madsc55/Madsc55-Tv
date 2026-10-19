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
    categories = {report.get("category") for report in reports}
    expected = {"k1", "k2", "k3", "k4", "k5"}
    complete = categories == expected and len(reports) == 5
    safe = complete and all(report.get("production_writes") is False for report in reports)
    return {"all_five_present": complete, "all_read_only": safe,
            "production_ready": False, "runtime_evidence_verified": False}


def summarize_batch(reports: list[dict]) -> dict:
    """Read-only per-category failure summary for coordinated maintenance."""
    if not isinstance(reports, list) or any(not isinstance(r, dict) for r in reports):
        raise ValueError("Invalid batch reports")
    base = aggregate(reports)
    expected = {"k1", "k2", "k3", "k4", "k5"}
    failures = sorted(str(r.get("category", "unknown")) for r in reports
                      if r.get("status") != "success" or r.get("category") not in expected)
    missing = sorted(expected - {r.get("category") for r in reports if isinstance(r.get("category"), str)})
    counts = {category: sum(r.get("category") == category for r in reports) for category in expected}
    duplicates = sorted(category for category, count in counts.items() if count > 1)
    unexpected = sum(r.get("category") not in expected for r in reports)
    return {**base, "failed_categories": failures, "missing_categories": missing,
            "duplicate_categories": duplicates, "unexpected_category_count": unexpected,
            "requires_review": bool(failures) or bool(missing) or bool(duplicates) or bool(unexpected) or not base["all_read_only"],
            "production_writes": False}
