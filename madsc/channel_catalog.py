"""K2-K3 read-only bridge: discovery, supplied measurements, logos and IBO."""
from __future__ import annotations

from madsc.discovery import classify_candidates
from madsc.channel_presentation import present_channel
from madsc.channel_test import evaluate_probe
from madsc.k3_three_stage_gate import assess_three_stage_probes


def prepare_channel_catalog(rows: list[dict], measurements: dict | None = None,
                            logos: dict | None = None, ibo_results: dict | None = None,
                            probes: dict | None = None,
                            three_stage: dict | None = None) -> dict:
    """Inputs are externally supplied evidence keyed by stream SHA256.

    Does not fetch logos, probe streams, certify devices, or write playlists.
    """
    measurements = {} if measurements is None else measurements
    logos = {} if logos is None else logos
    ibo_results = {} if ibo_results is None else ibo_results
    probes = {} if probes is None else probes
    three_stage = {} if three_stage is None else three_stage
    if any(not isinstance(x, dict) for x in (measurements, logos, ibo_results, probes, three_stage)):
        raise ValueError("Evidence maps must be dictionaries")
    discovery = classify_candidates(rows)
    digests = {c["url_sha256"] for c in discovery["candidates"]}
    for evidence in (measurements, logos, ibo_results, probes, three_stage):
        if set(evidence) - digests:
            raise ValueError("Evidence for unknown channel fingerprint")
    entries = []
    for candidate in discovery["candidates"]:
        digest = candidate["url_sha256"]
        source = rows[candidate["source_index"]]
        probe = probes.get(digest)
        if digest in probes:
            if not isinstance(probe, dict) or probe.get("url_sha256") != digest:
                raise ValueError("Probe fingerprint mismatch")
            status = evaluate_probe(probe)["technical_status"]
        else:
            status = "UNTESTED"
        staged = three_stage.get(digest)
        staged_result = None
        if digest in three_stage:
            staged_result = assess_three_stage_probes(staged)
            if staged_result["url_sha256"] != digest:
                raise ValueError("Three-stage fingerprint mismatch")
        if staged_result is not None and staged_result["three_stage_preliminary_pass"]:
            if probe is not None and status != "PRELIMINARY_PASS":
                raise ValueError("Three-stage pass conflicts with current technical probe")
        if staged_result is not None and probe is None:
            # Historical stage evidence does not substitute for a current probe.
            status = "UNTESTED"
        supplied_measurement = measurements.get(digest, {})
        if not isinstance(supplied_measurement, dict):
            raise ValueError("Invalid measurement")
        # Technical classification must come from validated probe evidence, not a caller claim.
        measurement = {**supplied_measurement, "technical_status": status}
        presentation = present_channel(
            {**candidate, "foreign": source.get("foreign") is True},
            measurement=measurement,
            logo_evidence=logos.get(digest),
            ibo_result=ibo_results.get(digest, "UNKNOWN"))
        entries.append({"url_sha256": digest, "source_index": candidate["source_index"],
                        "technical_status": status,
                        "three_stage_preliminary_pass": (staged_result["three_stage_preliminary_pass"]
                                                         if staged_result is not None else False),
                        "three_stage_evidence_supplied": staged_result is not None,
                        **presentation})
    buckets = {}
    for entry in entries:
        bucket = entry["bucket"]
        buckets[bucket] = buckets.get(bucket, 0) + 1
    return {"summary": {
                "candidate_count": len(entries),
                "duplicate_count": len(discovery["duplicates"]),
                "rejected_count": len(discovery["rejected"]),
                "buckets": buckets,
                "three_stage_evidence_count": sum(
                    entry["three_stage_evidence_supplied"] for entry in entries),
                "technical_probe_count": sum(
                    entry["technical_status"] != "UNTESTED" for entry in entries),
                "device_acceptance_proven": False,
            },
            "channels": entries, "duplicates": discovery["duplicates"],
            "rejected": discovery["rejected"], "category_order": list(dict.fromkeys(
                entry["group_title"] for entry in entries)),
            "device_verified_by_this_function": False,
            "network_probed": False, "production_writes": False,
            "production_ready": False}
