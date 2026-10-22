"""Offline channel test result evaluation; network probes require separate opt-in."""
from __future__ import annotations
import math
import re

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
    if not isinstance(probes, list) or not probes or len(probes) > 20000 or type(minimum_passes) is not int or not 2 <= minimum_passes <= 20000:
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
    if not isinstance(records, list) or len(records) > 20000:
        raise ValueError("Probe records must be a bounded list")
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
    if len(samples) > 20000:
        raise ValueError("Too many continuity samples")
    parsed = []
    for sample in samples:
        if not isinstance(sample, dict) or not isinstance(sample.get("observed_at"), str):
            raise ValueError("Timestamped sample required")
        stamp = sample["observed_at"]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})", stamp):
            raise ValueError("Observation must use RFC3339 timestamp")
        try:
            instant = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("Invalid observation time") from exc
        if instant.tzinfo is None or instant.utcoffset() is None:
            raise ValueError("Timezone-aware observation required")
        now = datetime.now(timezone.utc)
        if instant.astimezone(timezone.utc) > now:
            raise ValueError("Future-dated continuity evidence is invalid")
        if instant.year < 2020:
            raise ValueError("Implausibly old continuity evidence is invalid")
        parsed.append((instant.astimezone(timezone.utc), evaluate_probe(sample)))
    if any(a[0] >= b[0] for a, b in zip(parsed, parsed[1:])):
        raise ValueError("Samples must be strictly chronological")
    fingerprints = {item[1]["url_sha256"] for item in parsed}
    if len(fingerprints) != 1:
        raise ValueError("Mixed channel fingerprints")
    spacing_ok = all((b[0] - a[0]).total_seconds() / 3600 >= minimum_hours
                     for a, b in zip(parsed, parsed[1:]))
    elapsed = (parsed[-1][0] - parsed[0][0]).total_seconds() / 3600
    passes = sum(item[1]["technical_status"] == "PRELIMINARY_PASS" for item in parsed)
    return {
        "url_sha256": parsed[0][1]["url_sha256"],
        "stages_observed": len(parsed),
        "elapsed_hours": round(elapsed, 6),
        "preliminary_passes": passes,
        "three_stage_six_hour_preliminary": spacing_ok and passes == len(parsed),
        "observation_provenance_verified": False,
        "actual_network_measurements_verified": False,
        "stream_continuity_verified": False,
        "ibo_device_verified": False,
        "production_change_allowed": False,
    }


def summarize_candidate_continuity(candidate_fingerprints: list[str],
                                   measurements: dict[str, list[dict]]) -> dict:
    """Batch-evaluate real-shaped evidence without inventing missing measurements."""
    if (not isinstance(candidate_fingerprints, list) or len(candidate_fingerprints) > 20000
            or not isinstance(measurements, dict) or len(measurements) > 20000):
        raise ValueError("Invalid continuity batch")
    if any(not isinstance(key, str) for key in candidate_fingerprints):
        raise ValueError("Invalid candidate fingerprint")
    if len(set(candidate_fingerprints)) != len(candidate_fingerprints):
        raise ValueError("Duplicate candidate fingerprint")
    if any(not isinstance(key, str) or len(key) != 64
           or any(ch not in "0123456789abcdef" for ch in key)
           for key in candidate_fingerprints):
        raise ValueError("Invalid candidate fingerprint")
    if any(not isinstance(key, str) or len(key) != 64 or any(ch not in "0123456789abcdef" for ch in key) for key in measurements):
        raise ValueError("Invalid measurement fingerprint")
    if any(key not in candidate_fingerprints for key in measurements):
        raise ValueError("Orphan continuity measurements")
    results = {}
    for key in candidate_fingerprints:
        if key not in measurements:
            results[key] = {"status": "MISSING_MEASUREMENTS"}
            continue
        report = evaluate_three_stage_continuity(measurements[key])
        if report["url_sha256"] != key:
            raise ValueError("Continuity fingerprint mismatch")
        results[key] = {"status": ("PRELIMINARY_WINDOW_PASS"
                                    if report["three_stage_six_hour_preliminary"]
                                    else "NEEDS_REVIEW"), "evidence": report}
    return {
        "candidate_count": len(candidate_fingerprints),
        "measured_count": len(measurements),
        "missing_count": len(candidate_fingerprints) - len(measurements),
        "preliminary_window_passes": sum(
            x["status"] == "PRELIMINARY_WINDOW_PASS" for x in results.values()),
        "results": results,
        "actual_network_measurements_verified": False,
        "production_change_allowed": False,
    }
