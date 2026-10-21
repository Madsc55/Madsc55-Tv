"""K2-K3 read-only bridge: discovery, supplied measurements, logos and IBO."""
from __future__ import annotations

from madsc.discovery import classify_candidates
from madsc.channel_presentation import present_channel


def prepare_channel_catalog(rows: list[dict], measurements: dict | None = None,
                            logos: dict | None = None, ibo_results: dict | None = None) -> dict:
    """Inputs are externally supplied evidence keyed by stream SHA256.

    Does not fetch logos, probe streams, certify devices, or write playlists.
    """
    measurements = {} if measurements is None else measurements
    logos = {} if logos is None else logos
    ibo_results = {} if ibo_results is None else ibo_results
    if any(not isinstance(x, dict) for x in (measurements, logos, ibo_results)):
        raise ValueError("Evidence maps must be dictionaries")
    discovery = classify_candidates(rows)
    digests = {c["url_sha256"] for c in discovery["candidates"]}
    for evidence in (measurements, logos, ibo_results):
        if set(evidence) - digests:
            raise ValueError("Evidence for unknown channel fingerprint")
    entries = []
    for candidate in discovery["candidates"]:
        digest = candidate["url_sha256"]
        source = rows[candidate["source_index"]]
        presentation = present_channel(
            {**candidate, "foreign": source.get("foreign") is True},
            measurement=measurements.get(digest),
            logo_evidence=logos.get(digest),
            ibo_result=ibo_results.get(digest, "UNKNOWN"))
        entries.append({"url_sha256": digest, "source_index": candidate["source_index"],
                        **presentation})
    return {"channels": entries, "duplicates": discovery["duplicates"],
            "rejected": discovery["rejected"], "category_order": list(dict.fromkeys(
                entry["group_title"] for entry in entries)),
            "device_verified_by_this_function": False,
            "network_probed": False, "production_writes": False,
            "production_ready": False}
