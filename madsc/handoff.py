"""Read-only K2 to K3 handoff; no network or playlist writes."""
from __future__ import annotations
from madsc.channel_test import evaluate_probe

def assess_candidates(discovery: dict, probes: dict[str, dict]) -> dict:
    assessed = []
    for candidate in discovery["candidates"]:
        digest = candidate["url_sha256"]
        probe = probes.get(digest)
        if probe is None:
            status = "UNTESTED"
        else:
            if probe.get("url_sha256") != digest:
                raise ValueError("Probe fingerprint mismatch")
            status = evaluate_probe(probe)["technical_status"]
        assessed.append({"url_sha256": digest, "technical_status": status,
                         "ibo_device_verified": False, "production_change_allowed": False})
    return {"assessed": assessed, "candidate_count": len(assessed),
            "production_playlist_modified": False, "network_probed": False}
