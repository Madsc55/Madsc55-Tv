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
    # The restore acceptance gate requires an exact file inventory, not just
    # matching hashes for a caller-selected subset. Reject unexpected files,
    # symlinks and extra directories in any of the three sandbox trees.
    expected_files = set(names)
    expected_dirs = {
        str(parent).replace("\\\\", "/")
        for name in names
        for parent in Path(name).parents
        if str(parent) != "."
    }
    inventory_matches = True
    for root in (Path(source), Path(backup), Path(restored)):
        actual_files = set()
        actual_dirs = set()
        for item in root.rglob("*"):
            relative = item.relative_to(root).as_posix()
            if item.is_symlink():
                inventory_matches = False
                break
            if item.is_dir():
                actual_dirs.add(relative)
            elif item.is_file():
                actual_files.add(relative)
            else:
                inventory_matches = False
                break
        if actual_files != expected_files or actual_dirs != expected_dirs:
            inventory_matches = False
    accepted = result["independent_sandbox_restore_matches"] is True and inventory_matches
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
