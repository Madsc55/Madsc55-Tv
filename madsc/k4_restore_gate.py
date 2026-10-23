"""K4 isolated restore evidence gate, composed with K1 source safety.

Only inspects three already-existing independent directories. Never restores files.
"""
from __future__ import annotations

from pathlib import Path

from madsc.backup import verify_independent_restore


def audit_k4_restore(source: Path, backup: Path, restored: Path,
                     names: list[str]) -> dict:
    """Require matching backup/restore bytes before reporting sandbox success."""
    # An aliased ancestor can redirect a seemingly independent sandbox tree.
    # Fail before reading any content through that path.
    for root in (Path(source), Path(backup), Path(restored)):
        if any(ancestor.is_symlink() for ancestor in (root, *root.parents)):
            raise ValueError("Restore audit paths must not contain symlink ancestors")
    # Reject ambiguous aliases before any hashing or inventory traversal.
    roots = [Path(source), Path(backup), Path(restored)]
    if any(not root.is_absolute() or str(root) != str(root.absolute())
           or any(part in ('.', '..') for part in root.parts)
           for root in roots):
        raise ValueError('Restore audit roots must be canonical absolute paths')
    # Reject oversized declared inventories before performing any file hashing.
    # Directory entries also count toward the bounded traversal budget.
    if not isinstance(names, list) or any(not isinstance(name, str) for name in names):
        raise ValueError("Restore audit names must be a list of paths")
    if not names:
        raise ValueError("Restore audit requires at least one declared file")
    if len(names) > 10000:
        raise ValueError("Restore audit exceeds manifest entry limit")
    import unicodedata
    declared_dirs = set()
    seen_names = set()
    seen_portable_names = set()
    for name in names:
        if len(name) > 4096:
            raise ValueError("Restore audit path exceeds bounded length")
        if name in seen_names:
            raise ValueError("Duplicate restore audit path")
        portable_name = unicodedata.normalize('NFKC', name).casefold()
        if portable_name in seen_portable_names:
            raise ValueError("Ambiguous restore audit path alias")
        seen_names.add(name)
        seen_portable_names.add(portable_name)
        if (not name or name.startswith("~") or ":" in name or chr(92) in name
                or any(ord(character) < 32 or ord(character) == 127
                       or 0xD800 <= ord(character) <= 0xDFFF
                       or unicodedata.category(character) == 'Cf'
                       for character in name)
                or Path(name).is_absolute()
                or any(part in ("", ".", "..") for part in name.split("/"))):
            raise ValueError("Unsafe restore audit path")
        for parent in Path(name).parents:
            if str(parent) != ".":
                declared_dirs.add(parent.as_posix())
                if len(names) + len(declared_dirs) > 20000:
                    raise ValueError("Restore audit inventory exceeds safe entry limit")
    if seen_names.intersection(declared_dirs):
        raise ValueError('Restore audit file conflicts with declared directory')
    # Check directory aliases too: distinct file names may share a portable
    # directory name after Unicode normalization and case folding.
    portable_dirs = {}
    for directory_name in declared_dirs:
        portable_directory = unicodedata.normalize('NFKC', directory_name).casefold()
        previous = portable_dirs.setdefault(portable_directory, directory_name)
        if previous != directory_name:
            raise ValueError('Ambiguous restore audit directory alias')
        if portable_directory in seen_portable_names:
            raise ValueError('Restore audit portable file-directory collision')
    result = verify_independent_restore(source, backup, restored, names)
    # The restore acceptance gate requires an exact file inventory, not just
    # matching hashes for a caller-selected subset. Reject unexpected files,
    # symlinks and extra directories in any of the three sandbox trees.
    expected_files = set(names)
    expected_dirs = declared_dirs
    inventory_matches = True
    for root in (Path(source), Path(backup), Path(restored)):
        actual_files = set()
        actual_dirs = set()
        inspected = 0
        try:
            for item in root.rglob("*"):
                inspected += 1
                if inspected > 20000:
                    inventory_matches = False
                    break
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
        except OSError:
            # Unreadable or disappearing entries cannot establish a complete inventory.
            inventory_matches = False
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
