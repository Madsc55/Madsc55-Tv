"""Offline channel test result evaluation; network probes require separate opt-in."""
from __future__ import annotations
import math

def evaluate_probe(probe: dict) -> dict:
    """Classify supplied ffprobe-like evidence without assuming IBO approval."""
    required = {"url_sha256", "http_status", "video", "audio", "duration_seconds"}
    if not required.issubset(probe):
        raise ValueError("Missing probe evidence")
    digest = probe["url_sha256"]
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise ValueError("Invalid URL fingerprint")
    status = probe["http_status"]
    duration = probe["duration_seconds"]
    if type(status) is not int or type(duration) not in (int, float) or not math.isfinite(duration) or duration < 0:
        raise ValueError("Invalid probe measurements")
    technical = (200 <= status < 300 and probe["video"] is True
                 and probe["audio"] is True and duration >= 30)
    return {
        "url_sha256": digest,
        "technical_status": "PRELIMINARY_PASS" if technical else "NEEDS_REVIEW",
        "stream_continuity_verified": False,
        "channel_identity_verified": False,
        "ibo_device_verified": False,
        "production_change_allowed": False,
    }


def evaluate_repeated_probes(probes: list[dict], minimum_passes: int = 2) -> dict:
    """Evaluate independently supplied measurements, without claiming a live run."""
    if not isinstance(probes, list) or not probes or type(minimum_passes) is not int or minimum_passes < 2:
        raise ValueError("Invalid repeated-probe evidence")
    if len(probes) < minimum_passes:
        raise ValueError("Insufficient independent samples")
    evaluated = [evaluate_probe(probe) for probe in probes]
    digests = {item["url_sha256"] for item in evaluated}
    if len(digests) != 1:
        raise ValueError("Mixed channel fingerprints")
    passes = sum(item["technical_status"] == "PRELIMINARY_PASS" for item in evaluated)
    return {"url_sha256": evaluated[0]["url_sha256"],
            "samples": len(evaluated), "preliminary_passes": passes,
            "stable_preliminary": passes >= minimum_passes and passes == len(evaluated),
            "actual_network_measurements_verified": False,
            "stream_continuity_verified": False, "ibo_device_verified": False,
            "production_change_allowed": False}
