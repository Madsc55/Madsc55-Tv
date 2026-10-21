"""Preserve explicit IBO device results independently from automated tests."""
from __future__ import annotations

def classify_channel(technical_status: str, ibo_result: str = "UNKNOWN") -> dict:
    if ibo_result not in ("UNKNOWN", "WORKING", "NOT_WORKING"):
        raise ValueError("Invalid IBO result")
    if technical_status not in ("UNTESTED", "PRELIMINARY_PASS", "NEEDS_REVIEW"):
        raise ValueError("Invalid technical status")
    return {
        "technical_status": technical_status,
        "ibo_result": ibo_result,
        "protected_working": ibo_result == "WORKING",
        "technical_failure_overrides_ibo": False,
        "delete_allowed": False,
        "backup_write_allowed": False,
        "production_change_allowed": False,
    }
