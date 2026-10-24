"""Offline K2 daily evidence runner. Never fetches sources or changes production data."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from hashlib import sha256

from madsc.k2_daily_evidence import build_daily_evidence, verify_daily_evidence


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--day", required=True)
    parser.add_argument("--previous")
    args = parser.parse_args()
    registry = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    if not isinstance(registry, list):
        raise ValueError("Registry must be a list")
    previous = []
    if args.previous:
        prior = json.loads(Path(args.previous).read_text(encoding="utf-8"))
        if not verify_daily_evidence(prior):
            raise ValueError("Previous artifact integrity verification failed")
        previous = prior["candidate_fingerprints"]
    commit = os.environ.get("GITHUB_SHA", "")
    artifact = build_daily_evidence(registry, day=args.day, source_commit=commit,
                                    previous_fingerprints=previous)
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    run_attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "")
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    artifact["runner_context"] = {
        "repository": repository,
        "run_id": run_id,
        "run_attempt": run_attempt,
        "workflow_ref": os.environ.get("GITHUB_WORKFLOW_REF", ""),
    }
    # Runner-provided metadata is a claim, not a signed attestation.
    payload = {k: v for k, v in artifact.items() if k != "artifact_sha256"}
    artifact["artifact_sha256"] = sha256(json.dumps(
        payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
        allow_nan=False).encode("utf-8")).hexdigest()
    if not verify_daily_evidence(artifact):
        raise RuntimeError("K2 artifact self-check failed")
    destination = Path(args.output)
    if destination.is_symlink() or (destination.exists() and not destination.is_file()):
        raise ValueError("Output must be a regular file, not a symlink")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(artifact, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                           encoding="utf-8")


if __name__ == "__main__":
    main()
