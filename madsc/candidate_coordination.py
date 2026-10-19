"""Read-only candidate evidence coordination; no production changes."""
from __future__ import annotations

from madsc.discovery import classify_candidates
from madsc.channel_test import evaluate_probe
from madsc.maintenance import retry_decision
from madsc.ibo_policy import classify_channel


def coordinate(rows: list[dict], probes: dict, attempts: dict,
               epg_ids: set[str] | None = None, logo_ids: set[str] | None = None,
               ibo_results: dict | None = None) -> dict:
    """Classify supplied evidence by URL fingerprint; never mutate playlists."""
    if not isinstance(probes, dict) or not isinstance(attempts, dict):
        raise ValueError("Invalid evidence mapping")
    if epg_ids is not None and (not isinstance(epg_ids, set) or any(not isinstance(x, str) for x in epg_ids)):
        raise ValueError("Invalid EPG identifiers")
    if logo_ids is not None and (not isinstance(logo_ids, set) or any(not isinstance(x, str) for x in logo_ids)):
        raise ValueError("Invalid logo identifiers")
    if ibo_results is not None and not isinstance(ibo_results, dict):
        raise ValueError("Invalid IBO evidence")
    discovery = classify_candidates(rows)
    result = []
    for candidate in discovery["candidates"]:
        digest = candidate["url_sha256"]
        probe = probes.get(digest)
        if probe is not None and not isinstance(probe, dict):
            raise ValueError("Invalid probe evidence")
        if probe is not None and probe.get("url_sha256") != digest:
            raise ValueError("Probe fingerprint mismatch")
        status = evaluate_probe(probe)["technical_status"] if probe is not None else "UNTESTED"
        failures = attempts.get(digest, 0)
        if type(failures) is not int or failures < 0:
            raise ValueError("Invalid retry count")
        retry = retry_decision(failures)
        channel_id = candidate["tvg_id"]
        epg_match = channel_id in epg_ids if epg_ids is not None and channel_id else False
        logo_match = channel_id in logo_ids if logo_ids is not None and channel_id else False
        ibo = classify_channel(status, (ibo_results or {}).get(digest, "UNKNOWN"))
        metadata_hold = (epg_ids is not None and not epg_match) or (logo_ids is not None and not logo_match)
        ibo_review = ibo["ibo_result"] != "WORKING"
        protected_working = ibo["protected_working"]
        score = max(0, (50 if status == "PRELIMINARY_PASS" else 0) + (20 if epg_match else 0)
                    + (10 if logo_match else 0) - 5 * failures)
        result.append({"url_sha256": digest, "technical_status": status,
                       "tvg_id": channel_id, "epg_match": epg_match, "logo_match": logo_match,
                       "ibo_result": ibo["ibo_result"], "protected_working": protected_working,
                       "score": score,
                       "hold": status != "PRELIMINARY_PASS" or retry["blocked"] or metadata_hold or ibo_review,
                       "ibo_review_required": ibo_review,
                       "next_action": ("PRESERVE_IBO_WORKING_AND_REVIEW" if protected_working and
                                       (status != "PRELIMINARY_PASS" or retry["blocked"] or metadata_hold) else
                                       "HALT_AND_REPORT" if retry["blocked"] else
                                       "MANUAL_METADATA_REVIEW" if metadata_hold else
                                       "MANUAL_IBO_REVIEW" if ibo_review else retry["next_action"]),
                       "production_change_allowed": False, "delete_allowed": False})
    return {"candidates": sorted(result, key=lambda x: (-x["score"], x["url_sha256"])),
            "duplicates": discovery["duplicates"], "rejected": discovery["rejected"],
            "held_count": sum(x["hold"] for x in result),
            "epg_matched": sum(x["epg_match"] for x in result),
            "logo_matched": sum(x["logo_match"] for x in result),
            "report_type": "supplied_evidence_only", "ibo_device_verified": False,
            "network_probed": False, "production_writes": False, "production_ready": False}
