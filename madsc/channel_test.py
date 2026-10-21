"""Offline channel test result evaluation; network probes require separate opt-in."""
from __future__ import annotations
import math

def evaluate_probe(probe: dict) -> dict:
    """Classify supplied ffprobe-like evidence without assuming IBO approval."""
    required = {"url_sha256", "http_status", "video", "audio", "duration_seconds"}
    if not isinstance(probe, dict) or not required.issubset(probe):
        raise ValueError("Missing probe evidence")
    digest = probe["url_sha256"]
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise ValueError("Invalid URL fingerprint")
    status = probe["http_status"]
    duration = probe["duration_seconds"]
    if type(status) is not int or type(duration) not in (int, float) or not math.isfinite(duration) or duration < 0:
        raise ValueError("Invalid probe measurements")
    if type(probe["video"]) is not bool or type(probe["audio"]) is not bool:
        raise ValueError("Invalid video/audio evidence")
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


def evaluate_ffprobe_json(payload: dict, url_sha256: str, http_status: int = 200) -> dict:
    """Translate captured ffprobe JSON into conservative preliminary evidence.

    A single ffprobe sample does not prove 30 seconds of live continuity.
    """
    if not isinstance(payload, dict) or not isinstance(payload.get("streams"), list):
        raise ValueError("Invalid ffprobe JSON")
    streams = payload["streams"]
    if any(not isinstance(stream, dict) for stream in streams):
        raise ValueError("Invalid ffprobe stream")
    video = any(stream.get("codec_type") == "video" for stream in streams)
    audio = any(stream.get("codec_type") == "audio" for stream in streams)
    fmt = payload.get("format", {})
    if not isinstance(fmt, dict):
        raise ValueError("Invalid ffprobe format")
    try:
        duration = float(fmt.get("duration", 0))
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("Invalid ffprobe duration") from exc
    if not math.isfinite(duration) or duration < 0:
        raise ValueError("Invalid ffprobe duration")
    report = evaluate_probe({"url_sha256": url_sha256, "http_status": http_status,
                             "video": video, "audio": audio, "duration_seconds": duration})
    return {**report, "ffprobe_json_parsed": True,
            "live_probe_executed_by_this_function": False,
            "single_sample_only": True}


def summarize_offline_probe_evidence(records: list[dict]) -> dict:
    """Summarize supplied ffprobe-style measurements without probing any URLs."""
    if not isinstance(records, list):
        raise ValueError("Probe records must be a list")
    results = []
    seen = set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Invalid probe record")
        result = evaluate_ffprobe_json(record.get("ffprobe"), record.get("url_sha256"),
                                       record.get("http_status", 200))
        digest = result["url_sha256"]
        if digest in seen:
            raise ValueError("Duplicate channel evidence")
        seen.add(digest)
        results.append(result)
    return {"schema": "madsc-offline-probe-summary-v1", "channel_count": len(results),
            "preliminary_passes": sum(x["technical_status"] == "PRELIMINARY_PASS" for x in results),
            "needs_review": sum(x["technical_status"] == "NEEDS_REVIEW" for x in results),
            "network_probed": False, "ibo_device_verified": False,
            "production_ready": False, "results": results}


def evaluate_three_stage_continuity(samples: list[dict], minimum_hours: float = 6) -> dict:
    """Evaluate three chronological offline samples, never certify their provenance."""
    from datetime import datetime, timezone
    if (not isinstance(samples, list) or len(samples) < 3
            or type(minimum_hours) not in (int, float)
            or not math.isfinite(minimum_hours) or minimum_hours < 6):
        raise ValueError("Three stages and at least six hours are required")
    parsed = []
    for sample in samples:
        if not isinstance(sample, dict) or not isinstance(sample.get("observed_at"), str):
            raise ValueError("Timestamped sample required")
        stamp = sample["observed_at"]
        try:
            instant = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("Invalid observation time") from exc
        if instant.tzinfo is None or instant.utcoffset() is None:
            raise ValueError("Timezone-aware observation required")
        parsed.append((instant.astimezone(timezone.utc), evaluate_probe(sample)))
    if any(a[0] >= b[0] for a, b in zip(parsed, parsed[1:])):
        raise ValueError("Samples must be strictly chronological")
    fingerprints = {item[1]["url_sha256"] for item in parsed}
    if len(fingerprints) != 1:
        raise ValueError("Mixed channel fingerprints")
    elapsed = (parsed[-1][0] - parsed[0][0]).total_seconds() / 3600
    passes = sum(item[1]["technical_status"] == "PRELIMINARY_PASS" for item in parsed)
    return {
        "url_sha256": parsed[0][1]["url_sha256"],
        "stages_observed": len(parsed),
        "elapsed_hours": round(elapsed, 6),
        "preliminary_passes": passes,
        "three_stage_six_hour_preliminary": elapsed >= minimum_hours and passes == len(parsed),
        "observation_provenance_verified": False,
        "actual_network_measurements_verified": False,
        "stream_continuity_verified": False,
        "ibo_device_verified": False,
        "production_change_allowed": False,
    }
