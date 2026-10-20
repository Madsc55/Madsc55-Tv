"""Fail-closed K2 candidate to K3 offline probe linkage; no network or playlist writes."""
from madsc.artifact_handoff import unpack
from madsc.channel_test import summarize_offline_probe_evidence


def link_candidate_probes(envelope: dict, records: list[dict], run_id: str, commit_sha: str) -> dict:
    discovery = unpack(envelope, run_id, commit_sha)
    candidates = discovery["candidates"]
    fingerprints = {item["url_sha256"] for item in candidates}
    if len(fingerprints) != len(candidates):
        raise ValueError("Duplicate K2 candidate")
    summary = summarize_offline_probe_evidence(records)
    reported = {item["url_sha256"] for item in summary["results"]}
    if not reported.issubset(fingerprints):
        raise ValueError("K3 probe is not linked to the verified K2 candidate set")
    return {
        "schema": "madsc-k2-k3-offline-link-v1",
        "run_id": run_id, "commit_sha": commit_sha,
        "source_digest": envelope["digest"],
        "candidate_count": len(candidates),
        "probed_candidates": len(reported),
        "untested_candidates": len(fingerprints - reported),
        "preliminary_passes": summary["preliminary_passes"],
        "technical_samples_supplied": bool(reported),
        "live_continuity_verified": False,
        "candidate_identity_verified": False,
        "needs_review": summary["needs_review"],
        "network_probed": False, "ibo_device_verified": False,
        "production_writes": False, "production_ready": False,
        "results": summary["results"],
    }


def main():
    import argparse
    import json
    from pathlib import Path
    from madsc.batch_acceptance import _unique_json_pairs
    from madsc.fixture_report_writer import write_stage_report

    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--probes", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--commit-sha", required=True)
    parser.add_argument("--isolated-report-root", type=Path, required=True)
    args = parser.parse_args()
    def load(path):
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 16 * 1024 * 1024:
            raise ValueError("Invalid or oversized evidence")
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_json_pairs)
    linked = link_candidate_probes(load(args.candidates), load(args.probes),
                                  args.run_id, args.commit_sha)
    report = {"category": "k3", "production_writes": False,
              "production_ready": False, "evidence": linked}
    print(json.dumps(write_stage_report(args.isolated_report_root, "k3", report),
                     sort_keys=True))


if __name__ == "__main__":
    main()
