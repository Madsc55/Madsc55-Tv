"""Fail-closed K2 candidate to K3 offline probe linkage; no network or playlist writes."""
from madsc.artifact_handoff import unpack
from madsc.channel_test import summarize_offline_probe_evidence, summarize_candidate_continuity


def link_candidate_probes(envelope: dict, records: list[dict], run_id: str, commit_sha: str) -> dict:
    discovery = unpack(envelope, run_id, commit_sha)
    candidates = discovery["candidates"]
    if not isinstance(candidates, list) or len(candidates) > 20000:
        raise ValueError("Invalid K2 candidate list")
    fingerprints = []
    for item in candidates:
        if not isinstance(item, dict):
            raise ValueError("Invalid K2 candidate")
        digest = item.get("url_sha256")
        if (not isinstance(digest, str) or len(digest) != 64
                or any(ch not in "0123456789abcdef" for ch in digest)):
            raise ValueError("Invalid K2 candidate fingerprint")
        fingerprints.append(digest)
    fingerprints = set(fingerprints)
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



def link_candidate_continuity(envelope: dict, measurements: dict,
                              run_id: str, commit_sha: str) -> dict:
    """Join K2 candidates to K3 time-window evidence, without live approval.

    Supplied timestamps and measurements are untrusted offline claims.
    """
    discovery = unpack(envelope, run_id, commit_sha)
    candidates = discovery["candidates"]
    fingerprints = [item["url_sha256"] for item in candidates]
    summary = summarize_candidate_continuity(fingerprints, measurements)
    return {
        "schema": "madsc-k2-k3-continuity-link-v1",
        "run_id": run_id,
        "commit_sha": commit_sha,
        "source_digest": envelope["digest"],
        **summary,
        "observation_provenance_verified": False,
        "actual_network_measurements_verified": False,
        "ibo_device_verified": False,
        "production_ready": False,
        "production_writes": False,
    }


def load_evidence(path):
    """Read bounded JSON evidence without following path-component symlinks."""
    import json
    import os
    import stat
    from pathlib import Path
    from madsc.batch_acceptance import _unique_json_pairs

    if (not isinstance(getattr(os, "O_NOFOLLOW", None), int)
            or not isinstance(getattr(os, "O_DIRECTORY", None), int)
            or os.open not in os.supports_dir_fd):
        raise ValueError("Secure evidence opening is unavailable")

    path = Path(path).absolute()
    parts = path.parts
    descriptor = None
    try:
        descriptor = os.open(parts[0], os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        for component in parts[1:-1]:
            next_descriptor = os.open(
                component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=descriptor)
            os.close(descriptor)
            descriptor = next_descriptor
        file_descriptor = os.open(
            parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
            dir_fd=descriptor)
        with os.fdopen(file_descriptor, "rb") as handle:
            opened = os.fstat(handle.fileno())
            if not stat.S_ISREG(opened.st_mode) or opened.st_size > 16 * 1024 * 1024:
                raise ValueError("Evidence must be a bounded regular file")
            raw = handle.read(16 * 1024 * 1024 + 1)
    except OSError as exc:
        raise ValueError("Evidence path cannot be opened securely") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    if len(raw) > 16 * 1024 * 1024:
        raise ValueError("Invalid or oversized evidence")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_json_pairs)


def main():
    import argparse
    import json
    from pathlib import Path
    from madsc.batch_acceptance import _unique_json_pairs
    from madsc.fixture_report_writer import write_stage_report

    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    evidence_group = parser.add_mutually_exclusive_group(required=True)
    evidence_group.add_argument("--probes", type=Path)
    evidence_group.add_argument("--continuity", type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--commit-sha", required=True)
    parser.add_argument("--isolated-report-root", type=Path, required=True)
    args = parser.parse_args()
    candidates = load_evidence(args.candidates)
    if args.continuity is not None:
        linked = link_candidate_continuity(candidates, load_evidence(args.continuity),
                                           args.run_id, args.commit_sha)
    else:
        linked = link_candidate_probes(candidates, load_evidence(args.probes),
                                      args.run_id, args.commit_sha)
    report = {"category": "k3", "production_writes": False,
              "production_ready": False, "evidence": linked}
    print(json.dumps(write_stage_report(args.isolated_report_root, "k3", report),
                     sort_keys=True))


if __name__ == "__main__":
    main()
