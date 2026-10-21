"""Read-only CLI for independently verified K2 history source.

No fixture fallback and no writes to production history or playlists.
"""
import argparse
import json
import os
from pathlib import Path
from madsc.write_path_audit import enforce_local_output_path

from madsc.github_history_client import verify_live_github_origin
from madsc.history_source_gate import load_verified_source


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-folder", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--current-sha", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workflow", default=".github/workflows/madsc-05-bakim.yml")
    args = parser.parse_args()
    enforce_local_output_path(args.output.absolute())
    if args.output.is_symlink():
        raise ValueError("Symlinked report output")
    if args.manifest.is_symlink() or not args.manifest.is_file():
        raise ValueError("Missing source manifest")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("Invalid source manifest")
    # Check local file bytes and manifest contract before calling GitHub.
    load_verified_source(args.source_folder, args.manifest,
                         run_id=manifest.get("source_run_id"),
                         commit_sha=manifest.get("source_commit_sha"))
    verified = verify_live_github_origin(
        manifest, repository="Madsc55/Madsc55-Tv", branch="main",
        workflow_path=args.workflow, current_sha=args.current_sha,
        token=os.environ.get("GITHUB_TOKEN"))
    # Only a successful independent check produces an isolated report.
    result = {"schema": "madsc-verified-history-origin-v1",
              **verified, "read_only": True, "production_ready": False}
    enforce_local_output_path(args.output.absolute())
    with args.output.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, sort_keys=True) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
