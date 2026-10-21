"""K4 isolated restore evidence gate, composed with K1 source safety.

Only inspects three already-existing independent directories. Never restores files.
"""
from __future__ import annotations

from pathlib import Path

from madsc.backup import verify_independent_restore


def audit_k4_restore(source: Path, backup: Path, restored: Path,
                     names: list[str]) -> dict:
    """Require matching backup/restore bytes before reporting sandbox success."""
    result = verify_independent_restore(source, backup, restored, names)
    accepted = result["independent_sandbox_restore_matches"] is True
    return {
        "stage": "K4_ARCHIVE_RESTORE",
        "k1_source_path_checks_applied": True,
        "sandbox_restore_accepted": accepted,
        "external_storage_proven": False,
        "production_restore_approved": False,
        "production_writes": False,
        "files_checked": result["files_checked"],
        "backup_matches_source": result["backup_verified_against_source"],
        "restore_matches_backup": result["restore_verified_against_backup"],
        "next_action": "SANDBOX_AUDIT_PASSED_ONLY" if accepted else "HALT_AND_INVESTIGATE",
    }
