"""K5 checks K3 linked channel evidence without mistaking fixtures for live proof."""
import argparse
import json
from pathlib import Path
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
    if any(item.get("actual_network_measurements_verified") is True or
           item.get("network_probed") is True or
           item.get("production_ready") is True for item in results):
        raise ValueError("Unexpected live approval in offline evidence")
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
    if args.k3.is_symlink() or not args.k3.is_file() or args.k3.stat().st_size > 1024 * 1024:
        raise ValueError("Invalid K3 input")
    report = json.loads(args.k3.read_text(encoding="utf-8"), object_pairs_hook=_unique_json_pairs)
    if args.k2.is_symlink() or not args.k2.is_file() or args.k2.stat().st_size > 16 * 1024 * 1024:
        raise ValueError("Invalid K2 input")
    k2 = json.loads(args.k2.read_text(encoding="utf-8"), object_pairs_hook=_unique_json_pairs)
    result = evaluate_k3_evidence(report, k2, args.run_id, args.commit_sha)
    if args.output.is_symlink() or args.output.exists():
        raise FileExistsError("Refusing to overwrite K5 safety evidence")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as f:
        f.write(json.dumps(result, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
