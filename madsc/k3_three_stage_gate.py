"""K3 read-only three-stage schedule evidence; never probe or schedule jobs."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import re

from madsc.channel_test import evaluate_probe


def assess_three_stage_probes(samples: list[dict]) -> dict:
    """Require three distinct UTC timestamps spaced at least six hours apart.

    Timestamps are caller-supplied and are NOT independently authenticated.
    """
    if not isinstance(samples, list) or len(samples) != 3:
        raise ValueError("Exactly three test samples required")
    records = []
    now = datetime.now(timezone.utc)
    for sample in samples:
        if not isinstance(sample, dict) or not isinstance(sample.get("captured_at"), str):
            raise ValueError("Timestamp required")
        stamp = sample["captured_at"]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z", stamp):
            raise ValueError("UTC RFC3339 timestamp required")
        try:
            when = datetime.fromisoformat(stamp[:-1] + "+00:00")
        except ValueError as exc:
            raise ValueError("Invalid timestamp") from exc
        if when.tzinfo is None or when.utcoffset() != timedelta(0):
            raise ValueError("UTC timestamps required")
        if when > now:
            raise ValueError("Future-dated test evidence is invalid")
        if when.year < 2020:
            raise ValueError("Implausibly old test evidence is invalid")
        evidence = evaluate_probe(sample.get("probe"))
        records.append((when.astimezone(timezone.utc), evidence))
    records.sort(key=lambda item: item[0])
    if any(records[i + 1][0] - records[i][0] < timedelta(hours=6) for i in range(2)):
        raise ValueError("Samples must be separated by at least six hours")
    digests = {item[1]["url_sha256"] for item in records}
    if len(digests) != 1:
        raise ValueError("Mixed channel fingerprints")
    passes = sum(item[1]["technical_status"] == "PRELIMINARY_PASS" for item in records)
    return {
        "url_sha256": records[0][1]["url_sha256"],
        "samples": 3,
        "minimum_spacing_hours": 6,
        "preliminary_passes": passes,
        "three_stage_preliminary_pass": passes == 3,
        "timestamps_independently_verified": False,
        "actual_network_measurements_verified": False,
        "ibo_device_verified": False,
        "production_change_allowed": False,
    }
