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
