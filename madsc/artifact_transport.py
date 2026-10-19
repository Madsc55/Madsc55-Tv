"""CLI for read-only fixture K2 to K3 Actions artifact transport."""
import argparse
import json
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
    args = p.parse_args()
    if args.mode == "produce":
        discovery = classify_candidates([{"name": "Fixture only", "url": "https://example.org/fixture.m3u8", "tvg_id": "fixture.tv"}])
        result = pack(discovery, args.run_id, args.commit_sha)
    else:
        envelope = json.loads(args.path.read_text(encoding="utf-8"))
        discovery = unpack(envelope, args.run_id, args.commit_sha)
        result = assess_candidates(discovery, {})
        if result["network_probed"] or result["production_playlist_modified"]:
            raise ValueError("Read-only invariant failed")
    if args.mode == "produce":
        args.path.parent.mkdir(parents=True, exist_ok=True)
        args.path.write_text(json.dumps(result, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"mode": args.mode, "fixture_only": True, "verified": True}))
if __name__ == "__main__":
    main()
