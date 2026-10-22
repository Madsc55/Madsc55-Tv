"""Opt-in real history GitHub Actions entry point; no fixture fallback."""
import argparse
import json
import os
from pathlib import Path

from madsc.history_verified_pipeline import produce_verified_history, SOURCE_WORKFLOWS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-workflow", choices=SOURCE_WORKFLOWS,
                        default=SOURCE_WORKFLOWS[0])
    args = parser.parse_args()
    if not args.manifest.is_file() or args.manifest.is_symlink():
        raise ValueError("Real history manifest absent; no verified source")
    run_id = os.environ.get("GITHUB_RUN_ID")
    sha = os.environ.get("GITHUB_SHA")
    if not run_id or not sha:
        raise ValueError("Missing GitHub run identity")
    result = produce_verified_history(
        args.manifest, args.output, current_sha=sha, run_id=run_id,
        token=os.environ.get("GITHUB_TOKEN"), source_workflow_path=args.source_workflow)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
