"""Read-only K2 to K3 handoff; no network or playlist writes."""
from __future__ import annotations
from madsc.channel_test import evaluate_probe, evaluate_three_stage_continuity
from madsc.ibo_policy import classify_channel

def assess_candidates(discovery: dict, probes: dict[str, dict], ibo_results: dict[str, str] | None = None,
                      continuity_samples: dict[str, list[dict]] | None = None) -> dict:
    if not isinstance(probes, dict):
        raise ValueError("Probe evidence must be a dictionary")
    if len(probes) > 20000:
        raise ValueError("Too many probe evidence records")
    if not isinstance(discovery, dict) or not isinstance(discovery.get("candidates"), list):
        raise ValueError("Invalid discovery evidence")
    if len(discovery["candidates"]) > 20000:
        raise ValueError("Too many candidates in discovery")
    assessed = []
    seen = set()
    alternative_map = {}
    alternatives = discovery.get("alternatives", [])
    if not isinstance(alternatives, list):
        raise ValueError("Invalid alternative evidence")
    if len(alternatives) > 20000:
        raise ValueError("Too many alternatives in discovery")
    for alternative in alternatives:
        if not isinstance(alternative, dict):
            raise ValueError("Invalid alternative evidence")
        digest = alternative.get("url_sha256")
        parent = alternative.get("alternative_to_sha256")
        if (not isinstance(digest, str) or not isinstance(parent, str)
                or any(len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value)
                       for value in (digest, parent))
                or digest == parent or digest in alternative_map):
            raise ValueError("Invalid alternative mapping")
        alternative_map[digest] = parent
    if continuity_samples is not None and not isinstance(continuity_samples, dict):
        raise ValueError("Invalid continuity evidence")
    continuity_samples = continuity_samples or {}
    if len(continuity_samples) > 20000:
        raise ValueError("Too many continuity evidence records")
    identity_primary = {}
    if ibo_results is not None and not isinstance(ibo_results, dict):
        raise ValueError("Invalid IBO evidence")
    ibo_results = ibo_results or {}
    if len(ibo_results) > 20000:
        raise ValueError("Too many IBO evidence records")
    for evidence in (probes, continuity_samples, ibo_results):
        if any(not isinstance(key, str) or len(key) != 64
               or any(ch not in "0123456789abcdef" for ch in key)
               for key in evidence):
            raise ValueError("Invalid evidence fingerprint key")
    for candidate in discovery["candidates"]:
        if not isinstance(candidate, dict) or not isinstance(candidate.get("url_sha256"), str):
            raise ValueError("Invalid candidate fingerprint")
        digest = candidate["url_sha256"]
        if len(digest) != 64 or not all(char in "0123456789abcdef" for char in digest):
            raise ValueError("Invalid candidate fingerprint")
        if digest in seen:
            raise ValueError("Duplicate candidate fingerprint")
        seen.add(digest)
        tvg_id = candidate.get("tvg_id", "")
        if not isinstance(tvg_id, str):
            raise ValueError("Invalid candidate tvg-id")
        if tvg_id != tvg_id.strip() or any(ord(ch) < 32 or ord(ch) == 127 or ch == "\\" for ch in tvg_id):
            raise ValueError("Unsafe candidate tvg-id")
        name = candidate.get("name", "")
        logo = candidate.get("tvg_logo", "")
        group = candidate.get("group_title", "")
        if any(not isinstance(value, str) for value in (name, logo, group)):
            raise ValueError("Invalid candidate display metadata")
        if (not name.strip() or any(value != value.strip() for value in (name, logo, group))
                or any(ord(ch) < 32 or ord(ch) == 127 or ch == "\\" for value in (name, logo, group) for ch in value)):
            raise ValueError("Unsafe candidate display metadata")
        probe = probes.get(digest)
        if probe is None:
            status = "UNTESTED"
        else:
            if not isinstance(probe, dict):
                raise ValueError("Invalid probe record")
            if probe.get("url_sha256") != digest:
                raise ValueError("Probe fingerprint mismatch")
            status = evaluate_probe(probe)["technical_status"]
        identity = ("tvg_id", tvg_id.casefold()) if tvg_id else ("name_group", name.casefold(), group.casefold())
        alternative_to = identity_primary.get(identity)
        if alternative_to is None:
            identity_primary[identity] = digest
        continuity = (evaluate_three_stage_continuity(continuity_samples[digest])
                      if digest in continuity_samples else None)
        if continuity is not None and continuity["url_sha256"] != digest:
            raise ValueError("Continuity fingerprint mismatch")
        decision = classify_channel(status, ibo_results.get(digest, "UNKNOWN"))
        assessed.append({"url_sha256": digest, "name": name, "tvg_id": tvg_id,
                         "alternative_to_sha256": alternative_map.get(digest, alternative_to),
                         "continuity": continuity,
                         "tvg_logo": logo, "group_title": group, **decision,
                         "ibo_device_verified": False,
                         "ibo_result_supplied": decision["ibo_result"] != "UNKNOWN"})
    by_digest = {item["url_sha256"]: item for item in assessed}
    for key, parent in alternative_map.items():
        if key not in seen or parent not in seen:
            raise ValueError("Unlinked alternative fingerprint")
        child = by_digest[key]
        primary = by_digest[parent]
        child_identity = (("tvg_id", child["tvg_id"].casefold()) if child["tvg_id"]
                          else ("name_group", child["name"].casefold(), child["group_title"].casefold()))
        primary_identity = (("tvg_id", primary["tvg_id"].casefold()) if primary["tvg_id"]
                            else ("name_group", primary["name"].casefold(), primary["group_title"].casefold()))
        if (child_identity != primary_identity or child["alternative_to_sha256"] != parent
                or identity_primary.get(child_identity) != parent
                or primary["alternative_to_sha256"] is not None):
            raise ValueError("Conflicting alternative channel identity")
    if any(key not in seen for key in continuity_samples):
        raise ValueError("Unlinked continuity evidence fingerprint")
    if any(key not in seen for key in probes) or any(key not in seen for key in ibo_results):
        raise ValueError("Unlinked handoff evidence fingerprint")
    return {"assessed": assessed, "candidate_count": len(assessed),
            "production_playlist_modified": False, "network_probed": False}
