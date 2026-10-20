"""Fail-closed K2 candidate to K3 offline probe linkage; no network or playlist writes."""
from madsc.artifact_handoff import unpack
from madsc.channel_test import summarize_offline_probe_evidence


def link_candidate_probes(envelope: dict, records: list[dict], run_id: str, commit_sha: str) -> dict:
    discovery = unpack(envelope, run_id, commit_sha)
    candidates = discovery["candidates"]
    fingerprints = {item["url_sha256"] for item in candidates}
    if len(fingerprints) != len(candidates):
        raise ValueError("Duplicate K2 candidate")
    summary = summarize_offline_probe_evidence(records)
    reported = {item["url_sha256"] for item in summary["results"]}
    if not reported.issubset(fingerprints):
        raise ValueError("K3 probe is not linked to the verified K2 candidate set")
    return {
        "schema": "madsc-k2-k3-offline-link-v1",
        "run_id": run_id, "commit_sha": commit_sha,
        "source_digest": envelope["digest"],
        "candidate_count": len(candidates),
        "probed_candidates": len(reported),
        "untested_candidates": len(fingerprints - reported),
        "preliminary_passes": summary["preliminary_passes"],
        "needs_review": summary["needs_review"],
        "network_probed": False, "ibo_device_verified": False,
        "production_writes": False, "production_ready": False,
        "results": summary["results"],
    }
