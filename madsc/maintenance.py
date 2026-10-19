"""Pure functions for aggregate status and bounded retry decisions."""
from __future__ import annotations

def retry_decision(consecutive_failures: int, limit: int = 3) -> dict:
    if type(consecutive_failures) is not int or consecutive_failures < 0 or type(limit) is not int or not 1 <= limit <= 10:
        raise ValueError("Invalid failure count or retry limit")
    blocked = consecutive_failures >= limit
    return {"blocked": blocked, "next_action": "HALT_AND_REPORT" if blocked else "RETRY_LATER",
            "production_writes": False, "state_persisted": False}

def aggregate(reports: list[dict]) -> dict:
    categories = {report.get("category") for report in reports}
    expected = {"k1", "k2", "k3", "k4", "k5"}
    complete = categories == expected and len(reports) == 5
    safe = complete and all(report.get("production_writes") is False for report in reports)
    return {"all_five_present": complete, "all_read_only": safe,
            "production_ready": False, "runtime_evidence_verified": False}
