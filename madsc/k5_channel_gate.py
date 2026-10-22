"""K5 checks K3 linked channel evidence without mistaking fixtures for live proof."""
import argparse
import hashlib
import json
from pathlib import Path
from madsc.write_path_audit import enforce_local_output_path
from madsc.batch_acceptance import _unique_json_pairs
from madsc.artifact_handoff import unpack


def evaluate_k3_evidence(report: dict, k2_envelope: dict | None = None,
                         run_id: str | None = None, commit_sha: str | None = None) -> dict:
    if not isinstance(report, dict) or report.get("category") != "k3":
        raise ValueError("Invalid K3 report")
    if report.get("production_writes") is not False or report.get("production_ready") is not False:
        raise ValueError("Unsafe K3 production flags")
    evidence = report.get("evidence")
    if not isinstance(evidence, dict) or evidence.get("schema") != "madsc-k2-k3-offline-link-v1":
        raise ValueError("Missing linked K2-K3 evidence")
    for key in ("network_probed", "ibo_device_verified", "live_continuity_verified",
                "candidate_identity_verified", "production_writes", "production_ready"):
        if evidence.get(key) is not False:
            raise ValueError("Unproven K3 safety flag: " + key)
    if (type(evidence.get("candidate_count")) is not int or
            type(evidence.get("probed_candidates")) is not int or
            type(evidence.get("untested_candidates")) is not int or
            min(evidence["candidate_count"], evidence["probed_candidates"],
                evidence["untested_candidates"]) < 0 or
            evidence["probed_candidates"] + evidence["untested_candidates"] != evidence["candidate_count"]):
        raise ValueError("Inconsistent K3 candidate counts")
    if evidence.get("technical_samples_supplied") is not (evidence["probed_candidates"] > 0):
        raise ValueError("K3 sample flag does not match candidate counts")
    if (type(evidence.get("preliminary_passes")) is not int or
            type(evidence.get("needs_review")) is not int or
            evidence["preliminary_passes"] < 0 or evidence["needs_review"] < 0 or
            evidence["preliminary_passes"] + evidence["needs_review"] != evidence["probed_candidates"]):
        raise ValueError("K3 technical status counts do not match probes")
    results = evidence.get("results")
    if not isinstance(results, list) or len(results) != evidence["probed_candidates"]:
        raise ValueError("Invalid K3 results")
    fingerprints = [item.get("url_sha256") for item in results if isinstance(item, dict)]
    if (len(fingerprints) != len(results) or len(set(fingerprints)) != len(results) or
            any(not isinstance(d, str) or len(d) != 64 or
                any(c not in "0123456789abcdef" for c in d) for d in fingerprints)):
        raise ValueError("Invalid or repeated K3 channel fingerprints")
    # Offline evidence is a closed safety contract: reject *any* positive live claim,
    # including future fields that could otherwise bypass the three explicit checks.
    live_flags = ("actual_network_measurements_verified", "network_probed",
                  "live_continuity_verified", "stream_continuity_verified",
                  "candidate_identity_verified", "channel_identity_verified",
                  "ibo_device_verified", "production_writes", "production_ready",
                  "production_change_allowed")
    if any(evidence.get(key) is not False for key in live_flags if key in evidence):
        raise ValueError("Unexpected live approval in offline K3 envelope")
    if any(item.get(key) is not False for item in results for key in live_flags if key in item):
        raise ValueError("Unexpected live approval in offline K3 result")
    if any(item.get("technical_status") not in ("PRELIMINARY_PASS", "NEEDS_REVIEW") or
           item.get("stream_continuity_verified") is not False or
           item.get("channel_identity_verified") is not False or
           item.get("ibo_device_verified") is not False or
           item.get("production_change_allowed") is not False for item in results):
        raise ValueError("Unsafe K3 technical result")
    if sum(item["technical_status"] == "PRELIMINARY_PASS" for item in results) != evidence["preliminary_passes"]:
        raise ValueError("Inconsistent preliminary K3 pass count")
    if k2_envelope is not None:
        discovery = unpack(k2_envelope, run_id, commit_sha)
        fingerprints_k2 = {item["url_sha256"] for item in discovery["candidates"]}
        if (evidence.get("run_id") != run_id or evidence.get("commit_sha") != commit_sha or
                evidence.get("source_digest") != k2_envelope["digest"] or
                len(fingerprints_k2) != len(discovery["candidates"]) or
                evidence["candidate_count"] != len(fingerprints_k2) or
                not set(fingerprints).issubset(fingerprints_k2)):
            raise ValueError("K2-K3-K5 provenance or candidate fingerprint mismatch")
    return {"schema": "madsc-k5-k3-safety-gate-v1",
            "candidate_count": evidence["candidate_count"],
            "probed_candidates": evidence["probed_candidates"],
            "untested_candidates": evidence["untested_candidates"],
            "offline_fingerprint_link_verified": True,
            "actual_network_measurements_verified": False,
            "live_continuity_verified": False,
            "ibo_device_verified": False,
            "production_ready": False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--k3", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--k2", type=Path, required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--commit-sha", required=True)
    args = p.parse_args()
    enforce_local_output_path(args.output.absolute())
    if args.k3.is_symlink() or not args.k3.is_file() or args.k3.stat().st_size > 1024 * 1024:
        raise ValueError("Invalid K3 input")
    report = json.loads(args.k3.read_text(encoding="utf-8"), object_pairs_hook=_unique_json_pairs)
    if args.k2.is_symlink() or not args.k2.is_file() or args.k2.stat().st_size > 16 * 1024 * 1024:
        raise ValueError("Invalid K2 input")
    k2 = json.loads(args.k2.read_text(encoding="utf-8"), object_pairs_hook=_unique_json_pairs)
    result = evaluate_k3_evidence(report, k2, args.run_id, args.commit_sha)
    if args.output.is_symlink() or args.output.exists():
        raise FileExistsError("Refusing to overwrite K5 safety evidence")
    enforce_local_output_path(args.output.absolute())
    with args.output.open("x", encoding="utf-8") as f:
        f.write(json.dumps(result, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))



def evaluate_k3_head_observation(observation: dict, k2_envelope: dict,
                                 run_id: str, commit_sha: str) -> dict:
    """Separate HEAD transport evidence from offline K3 and live stream acceptance."""
    if not isinstance(observation, dict) or observation.get("schema") != "madsc-k3-https-head-observation-v1":
        raise ValueError("Invalid K3 HTTPS HEAD observation")
    discovery = unpack(k2_envelope, run_id, commit_sha)
    fingerprints = [item["url_sha256"] for item in discovery["candidates"]]
    digest = observation.get("url_sha256")
    if (not isinstance(digest, str) or len(digest) != 64 or
            any(c not in "0123456789abcdef" for c in digest) or
            fingerprints.count(digest) != 1 or
            observation.get("k2_source_digest") != k2_envelope["digest"] or
            observation.get("run_id") != run_id or
            observation.get("commit_sha") != commit_sha):
        raise ValueError("K2-K3 HEAD provenance mismatch")
    # This function validates a supplied report; it cannot attest that sockets
    # or TLS were actually used. Never promote caller claims to live acceptance.
    for key in ("tls_verified", "dns_pinned", "network_probed"):
        if observation.get(key) is not True:
            raise ValueError("Missing HEAD transport evidence: " + key)
    for key in ("redirects_followed", "stream_continuity_verified",
                "ibo_device_verified", "production_writes", "production_ready"):
        if observation.get(key) is not False:
            raise ValueError("Unsafe HEAD observation claim: " + key)
    # Explicitly reject approval-like extensions; a caller-supplied JSON report
    # must not smuggle a live/production claim through this review gate.
    approval_flags = ("actual_network_measurements_verified",
                      "actual_stream_measurements_verified",
                      "live_continuity_verified", "candidate_identity_verified",
                      "channel_identity_verified", "production_change_allowed",
                      "production_approved", "ibo_approved",
                      "head_transport_independently_verified")
    if any(observation.get(key) is not False
           for key in approval_flags if key in observation):
        raise ValueError("Untrusted live approval in HEAD observation")
    status = observation.get("http_status")
    if type(status) is not int or not 100 <= status <= 599 or 300 <= status < 400:
        raise ValueError("Invalid or redirected HTTP status")
    # Closed schema: unexpected fields may carry covert approvals or change
    # audit meaning. Require exactly the K3 producer's documented fields.
    expected_fields = {
        "schema", "url_sha256", "k2_source_digest", "run_id", "commit_sha",
        "http_status", "tls_verified", "dns_pinned", "redirects_followed",
        "network_probed", "stream_continuity_verified", "ibo_device_verified",
        "production_writes", "production_ready"}
    if set(observation) != expected_fields:
        raise ValueError("Unexpected or missing HEAD observation fields")
    # Stable digest binds the exact accepted report content for later audit.
    # It is NOT a signature or independent proof that a network request occurred.
    observation_digest = hashlib.sha256(
        json.dumps(observation, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=True, allow_nan=False).encode("utf-8")).hexdigest()
    return {"schema": "madsc-k5-k3-head-transport-review-v1",
            "url_sha256": digest, "http_status": status,
            "observation_sha256": observation_digest,
            "head_transport_claim_validated": True,
            "head_transport_independently_verified": False,
            "http_success_status": 200 <= status < 300,
            "actual_stream_measurements_verified": False,
            "live_continuity_verified": False, "ibo_device_verified": False,
            "production_ready": False}


if __name__ == "__main__":
    main()
