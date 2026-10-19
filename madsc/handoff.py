"""Read-only K2 to K3 handoff; no network or playlist writes."""
from __future__ import annotations
from madsc.channel_test import evaluate_probe
from madsc.ibo_policy import classify_channel

def assess_candidates(discovery: dict, probes: dict[str, dict], ibo_results: dict[str, str] | None = None) -> dict:
    assessed = []
    ibo_results = ibo_results or {}
    for candidate in discovery["candidates"]:
        digest = candidate["url_sha256"]
        probe = probes.get(digest)
        if probe is None:
            status = "UNTESTED"
        else:
            if probe.get("url_sha256") != digest:
                raise ValueError("Probe fingerprint mismatch")
            status = evaluate_probe(probe)["technical_status"]
        decision = classify_channel(status, ibo_results.get(digest, "UNKNOWN"))
        assessed.append({"url_sha256": digest, **decision,
                         "ibo_device_verified": decision["ibo_result"] != "UNKNOWN"})
    return {"assessed": assessed, "candidate_count": len(assessed),
            "production_playlist_modified": False, "network_probed": False}
