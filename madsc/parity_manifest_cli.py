"""Opt-in CLI for producing a replacement parity manifest from real files."""
import argparse
import json
import os
import stat
from pathlib import Path

from madsc.legacy_parity_cli import unique_pairs
from madsc.parity_manifest_writer import (MAX_INPUT_BYTES,
                                          write_replacement_parity_manifest)


MAX_SNAPSHOT_BYTES = 1024 * 1024


def _read_regular_file(path, limit):
    path = Path(path)
    if path.is_symlink():
        raise PermissionError("Symlink parity input is forbidden")
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags)
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > limit:
            raise PermissionError("Parity input must be a bounded regular file")
        chunks = []
        remaining = limit + 1
        while remaining:
            chunk = os.read(descriptor, min(65536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        payload = b"".join(chunks)
        if not payload or len(payload) > limit:
            raise ValueError("Invalid parity input size")
        return payload
    finally:
        os.close(descriptor)


def produce_from_files(*, input_path, snapshot_path, output_root, repository,
                       branch, workflow_path, run_id, head_sha):
    """Read real input/snapshot files and write one isolated v1 manifest."""
    input_payload = _read_regular_file(input_path, MAX_INPUT_BYTES)
    raw_snapshot = _read_regular_file(snapshot_path, MAX_SNAPSHOT_BYTES)
    try:
        snapshot = json.loads(raw_snapshot.decode("utf-8"), object_pairs_hook=unique_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid parity snapshot JSON") from exc
    execution = {
        "repository": repository,
        "branch": branch,
        "workflow_path": workflow_path,
        "run_id": run_id,
        "head_sha": head_sha,
        "snapshot": snapshot,
    }
    return write_replacement_parity_manifest(Path(output_root), execution, input_payload)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--output-root", default=".")
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY"))
    parser.add_argument("--branch", default=os.environ.get("GITHUB_REF_NAME"))
    parser.add_argument("--workflow-path", required=True)
    parser.add_argument("--run-id", default=os.environ.get("GITHUB_RUN_ID"))
    parser.add_argument("--head-sha", default=os.environ.get("GITHUB_SHA"))
    args = parser.parse_args(argv)
    try:
        run_id = int(args.run_id)
    except (TypeError, ValueError) as exc:
        raise ValueError("Missing or invalid GitHub run id") from exc
    result = produce_from_files(
        input_path=args.input, snapshot_path=args.snapshot,
        output_root=Path(args.output_root).absolute(), repository=args.repository,
        branch=args.branch, workflow_path=args.workflow_path,
        run_id=run_id, head_sha=args.head_sha)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
