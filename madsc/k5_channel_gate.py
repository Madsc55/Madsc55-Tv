"""K5 checks K3 linked channel evidence without mistaking fixtures for live proof."""
import argparse
import json
from pathlib import Path
from madsc.batch_acceptance import _unique_json_pairs


def evaluate_k3_evidence(report: dict) -> dict:
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
    results = evidence.get("results")
    if not isinstance(results, list) or len(results) != evidence["probed_candidates"]:
        raise ValueError("Invalid K3 results")
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
    args = p.parse_args()
    if args.k3.is_symlink() or not args.k3.is_file() or args.k3.stat().st_size > 1024 * 1024:
        raise ValueError("Invalid K3 input")
    report = json.loads(args.k3.read_text(encoding="utf-8"), object_pairs_hook=_unique_json_pairs)
    result = evaluate_k3_evidence(report)
    if args.output.is_symlink() or args.output.exists():
        raise FileExistsError("Refusing to overwrite K5 safety evidence")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as f:
        f.write(json.dumps(result, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
