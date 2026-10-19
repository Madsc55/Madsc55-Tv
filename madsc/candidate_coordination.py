"""Read-only candidate evidence coordination; no production changes."""
from __future__ import annotations

from madsc.discovery import classify_candidates
from madsc.channel_test import evaluate_probe
from madsc.maintenance import retry_decision


def coordinate(rows: list[dict], probes: dict, attempts: dict) -> dict:
    """Classify supplied evidence by URL fingerprint; never mutate playlists."""
    discovery = classify_candidates(rows)
    result = []
    for candidate in discovery["candidates"]:
        digest = candidate["url_sha256"]
        probe = probes.get(digest)
        if probe is not None and probe.get("url_sha256") != digest:
            raise ValueError("Probe fingerprint mismatch")
        status = evaluate_probe(probe)["technical_status"] if probe else "UNTESTED"
        failures = attempts.get(digest, 0)
        retry = retry_decision(failures)
        result.append({"url_sha256": digest, "technical_status": status,
                       "score": max(0, (50 if status == "PRELIMINARY_PASS" else 0) - 5 * failures),
                       "hold": status != "PRELIMINARY_PASS" or retry["blocked"],
                       "next_action": retry["next_action"], "production_change_allowed": False})
    return {"candidates": sorted(result, key=lambda x: (-x["score"], x["url_sha256"])),
            "duplicates": discovery["duplicates"], "rejected": discovery["rejected"],
            "production_writes": False, "production_ready": False}
