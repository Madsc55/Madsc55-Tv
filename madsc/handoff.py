"""Read-only K2 to K3 handoff; no network or playlist writes."""
from __future__ import annotations
from madsc.channel_test import evaluate_probe
from madsc.ibo_policy import classify_channel

def assess_candidates(discovery: dict, probes: dict[str, dict], ibo_results: dict[str, str] | None = None) -> dict:
    if not isinstance(probes, dict):
        raise ValueError("Probe evidence must be a dictionary")
    if not isinstance(discovery, dict) or not isinstance(discovery.get("candidates"), list):
        raise ValueError("Invalid discovery evidence")
    assessed = []
    seen = set()
    if ibo_results is not None and not isinstance(ibo_results, dict):
        raise ValueError("Invalid IBO evidence")
    ibo_results = ibo_results or {}
    for candidate in discovery["candidates"]:
        if not isinstance(candidate, dict) or not isinstance(candidate.get("url_sha256"), str):
            raise ValueError("Invalid candidate fingerprint")
        digest = candidate["url_sha256"]
        if len(digest) != 64 or not all(char in "0123456789abcdef" for char in digest):
            raise ValueError("Invalid candidate fingerprint")
        if digest in seen:
            raise ValueError("Duplicate candidate fingerprint")
        seen.add(digest)
        tvg_id = candidate.get("tvg_id", "")
        if not isinstance(tvg_id, str):
            raise ValueError("Invalid candidate tvg-id")
        name = candidate.get("name", "")
        logo = candidate.get("tvg_logo", "")
        group = candidate.get("group_title", "")
        if any(not isinstance(value, str) for value in (name, logo, group)):
            raise ValueError("Invalid candidate display metadata")
        probe = probes.get(digest)
        if probe is None:
            status = "UNTESTED"
        else:
            if not isinstance(probe, dict):
                raise ValueError("Invalid probe record")
            if probe.get("url_sha256") != digest:
                raise ValueError("Probe fingerprint mismatch")
            status = evaluate_probe(probe)["technical_status"]
        decision = classify_channel(status, ibo_results.get(digest, "UNKNOWN"))
        assessed.append({"url_sha256": digest, "name": name, "tvg_id": tvg_id,
                         "tvg_logo": logo, "group_title": group, **decision,
                         "ibo_device_verified": False,
                         "ibo_result_supplied": decision["ibo_result"] != "UNKNOWN"})
    return {"assessed": assessed, "candidate_count": len(assessed),
            "production_playlist_modified": False, "network_probed": False}
