"""CLI for read-only fixture K2 to K3 Actions artifact transport."""
import argparse
import json
from madsc.batch_acceptance import _unique_json_pairs
from pathlib import Path
from madsc.artifact_handoff import pack, unpack
from madsc.discovery import classify_candidates
from madsc.handoff import assess_candidates

def main():
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=["produce", "consume"])
    p.add_argument("--path", type=Path, required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--commit-sha", required=True)
    p.add_argument("--source", type=Path, help="Optional read-only M3U/M3U8 source")
    args = p.parse_args()
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
        envelope = json.loads(args.path.read_text(encoding="utf-8"), object_pairs_hook=_unique_json_pairs)
        discovery = unpack(envelope, args.run_id, args.commit_sha)
        result = assess_candidates(discovery, {})
        if result["network_probed"] or result["production_playlist_modified"]:
            raise ValueError("Read-only invariant failed")
    if args.mode == "produce":
        args.path.parent.mkdir(parents=True, exist_ok=True)
        args.path.write_text(json.dumps(result, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"mode": args.mode, "fixture_only": args.source is None if args.mode == "produce" else False, "verified": True}))
if __name__ == "__main__":
    main()
