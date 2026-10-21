"""One offline entry point for K2 discovery, K3 evidence and K5 drafts.

K1 production isolation is inherent: this function performs no filesystem writes.
K4 backup/restore is intentionally not invoked by preview generation.
"""
from __future__ import annotations

from madsc.channel_catalog import prepare_channel_catalog
from madsc.playlist_previews import render_playlist_previews


def build_offline_channel_previews(rows: list[dict], *, probes: dict | None = None,
                                   measurements: dict | None = None,
                                   logos: dict | None = None,
                                   ibo_results: dict | None = None,
                                   three_stage: dict | None = None) -> dict:
    """Build candidate-only previews without network or GitHub Actions."""
    catalog = prepare_channel_catalog(rows, probes=probes, measurements=measurements,
                                      logos=logos, ibo_results=ibo_results,
                                      three_stage=three_stage)
    previews = render_playlist_previews(catalog, rows)
    return {
        "catalog": catalog,
        "previews": previews["drafts"],
        "counts": previews["counts"],
        "automation_count": 5,
        "executed_stages": ["K2_DISCOVERY", "K3_SUPPLIED_EVIDENCE", "K5_PREVIEW"],
        "k1_policy": "NO_PRODUCTION_WRITES",
        "k4_backup_invoked": False,
        "network_probed": False,
        "ibo_device_test_executed": False,
        "production_writes": False,
        "production_ready": False,
    }
