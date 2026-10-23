"""K5 fail-closed acceptance gate for offline migration artifacts.

Integrity is not evidence of real channel identity or playback. This module
cannot approve production writes or device rollout.
"""
from collections.abc import Mapping

from madsc.isolated_ibo_archive_verify import verify_6115_archive_preview
from madsc.isolated_ibo_test_pool_verify import verify_isolated_test_pool


def assess_k5_acceptance(urls, archive_manifest, records, pool):
    """Validate both isolated artifacts; report blockers without any I/O."""
    archive = verify_6115_archive_preview(urls, archive_manifest)
    isolated = verify_isolated_test_pool(records, pool)
    if archive["position_count"] != isolated["entry_count"]:
        raise ValueError("K5 archive and pool sizes disagree")
    blockers = [
        "source_identity_not_verified",
        "legacy_logo_history_not_verified",
        "playback_not_verified",
        "device_not_verified",
        "production_release_not_authorized",
    ]
    return {
        "archive_integrity_verified": archive["verified"],
        "pool_integrity_verified": isolated["verified"],
        "entry_count": isolated["entry_count"],
        "preview_only": True,
        "production_writes": False,
        "production_ready": False,
        "blockers": blockers,
    }
