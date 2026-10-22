"""CLI for read-only fixture K2 to K3 Actions artifact transport."""
import argparse
import json
from madsc.batch_acceptance import _unique_json_pairs
from pathlib import Path
from madsc.artifact_handoff import pack, unpack
from madsc.discovery import classify_candidates
from madsc.handoff import assess_candidates
from madsc.write_path_audit import enforce_local_output_path, enforce_write_paths

def main():
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=["produce", "consume"])
    p.add_argument("--path", type=Path, required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--commit-sha", required=True)
    p.add_argument("--source", type=Path, help="Optional read-only M3U/M3U8 source")
    p.add_argument("--output", type=Path, help="Optional K3/K5 verification report")
    args = p.parse_args()
    if args.mode == "produce":
        enforce_local_output_path(args.path.absolute())
    elif args.output is not None:
        enforce_local_output_path(args.output.absolute())
    if args.mode == "produce":
        if args.source is not None:
            from madsc.source_import import extract_candidates
            if args.source.is_symlink() or not args.source.is_file():
                raise ValueError("Invalid read-only source")
            discovery = extract_candidates(args.source)
        else:
            discovery = classify_candidates([{"name": "Fixture only", "url": "https://example.org/fixture.m3u8", "tvg_id": "fixture.tv"}])
        result = pack(discovery, args.run_id, args.commit_sha)
    else:
        if args.path.is_symlink() or not args.path.is_file():
            raise ValueError("Invalid evidence file")
        if args.path.stat().st_size > 16 * 1024 * 1024:
            raise ValueError("Evidence exceeds 16 MiB safety limit")
        envelope = json.loads(args.path.read_text(encoding="utf-8"), object_pairs_hook=_unique_json_pairs)
        discovery = unpack(envelope, args.run_id, args.commit_sha)
        result = assess_candidates(discovery, {})
        if result["network_probed"] or result["production_playlist_modified"]:
            raise ValueError("Read-only invariant failed")
        if args.output is not None:
            if args.output.is_symlink():
                raise ValueError("Invalid report output")
            enforce_write_paths([args.output.name])
            enforce_local_output_path(args.output.absolute())
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(json.dumps({"schema": "madsc-handoff-verification-v1", "run_id": args.run_id,
                "commit_sha": args.commit_sha, "source_digest": envelope["digest"],
                "candidate_count": result["candidate_count"], "read_only": True,
                "network_probed": False, "production_ready": False}, sort_keys=True) + "\n")
    if args.mode == "produce":
        enforce_write_paths([args.path.name])
        enforce_local_output_path(args.path.absolute())
        with args.path.open("x", encoding="utf-8") as handle:
            handle.write(json.dumps(result, sort_keys=True) + "\n")
    print(json.dumps({"mode": args.mode, "source_mode": "read_only_m3u" if args.mode == "produce" and args.source is not None else ("synthetic_fixture" if args.mode == "produce" else "verified_artifact"), "production_ready": False, "verified": True}))
if __name__ == "__main__":
    main()
