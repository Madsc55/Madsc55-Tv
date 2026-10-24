"""K2 deterministic daily discovery evidence. Offline only; no URL fetching."""
from __future__ import annotations

import json
from datetime import date
from hashlib import sha256

from madsc.multisource_discovery import evaluate_discovery


def _digest(value: object) -> str:
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                             separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def build_daily_evidence(records: list[dict], *, day: str, source_commit: str,
                         previous_fingerprints: list[str] | None = None,
                         existing_urls: set[str] | None = None) -> dict:
    """Produce a hash-linked review artifact without making rights assertions."""
    try:
        if date.fromisoformat(day).isoformat() != day:
            raise ValueError
    except (TypeError, ValueError) as exc:
        raise ValueError("Day must be an ISO calendar date") from exc
    if not isinstance(source_commit, str) or len(source_commit) != 40 or any(
        ch not in "0123456789abcdef" for ch in source_commit
    ):
        raise ValueError("Source commit must be a full lowercase Git SHA")
    if previous_fingerprints is None:
        previous_fingerprints = []
    if not isinstance(previous_fingerprints, list) or len(previous_fingerprints) > 20000 or any(
        not isinstance(x, str) or len(x) != 64 or any(c not in "0123456789abcdef" for c in x)
        for x in previous_fingerprints
    ):
        raise ValueError("Invalid previous fingerprints")
    if len(previous_fingerprints) != len(set(previous_fingerprints)):
        raise ValueError("Duplicate previous fingerprints")
    report = evaluate_discovery(records, existing_urls)
    current = sorted(item["url_sha256"] for item in report["candidates"])
    old = set(previous_fingerprints)
    current_set = set(current)
    evidence = {
        "schema": "k2_daily_discovery_evidence_v1",
        "day": day,
        "source_commit": source_commit,
        "input_sha256": _digest(records),
        "previous_sha256": _digest(sorted(old)),
        "report_sha256": _digest(report),
        "candidate_fingerprints": current,
        "added": sorted(current_set - old),
        "missing_from_today": sorted(old - current_set),
        "source_identity_verified": False,
        "license_verified": False,
        "production_ready": False,
        "network_probed": False,
        "production_writes": False,
        "report": report,
    }
    return {**evidence, "artifact_sha256": _digest(evidence)}


def verify_daily_evidence(artifact: dict) -> bool:
    if not isinstance(artifact, dict) or "artifact_sha256" not in artifact:
        return False
    try:
        expected = artifact["artifact_sha256"]
        payload = {k: v for k, v in artifact.items() if k != "artifact_sha256"}
        return (isinstance(expected, str) and len(expected) == 64
                and expected == _digest(payload)
                and payload["report_sha256"] == _digest(payload["report"])
                and payload["candidate_fingerprints"] == sorted(
                    row["url_sha256"] for row in payload["report"]["candidates"])
                and payload["production_ready"] is False
                and payload["license_verified"] is False
                and payload["source_identity_verified"] is False
                and payload["network_probed"] is False
                and payload["production_writes"] is False)
    except (KeyError, TypeError, ValueError):
        return False
