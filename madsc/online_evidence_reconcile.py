"""Read-only reconciliation of K2 discovery and K3 manifest evidence.

Evidence never implies playback, device approval or production readiness.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def reconcile(k2: dict, k3: dict) -> dict:
    if not isinstance(k2, dict) or not isinstance(k3, dict):
        raise ValueError("K2 and K3 reports must be objects")
    if k2.get("production_playlist_modified") is not False or k3.get("production_playlist_modified") is not False:
        raise ValueError("Reports must explicitly forbid production mutation")
    if k2.get("mode") != "REAL_REMOTE_SOURCE_READ_ONLY" or k3.get("stage") != "K3_REAL_NETWORK_MANIFEST_PILOT":
        raise ValueError("Unexpected K2/K3 evidence type")
    source = k2.get("source")
    if not isinstance(source, str) or source != k3.get("source"):
        raise ValueError("K2 and K3 must use the same declared source")
    source_sha = k2.get("source_sha256")
    k3_source_sha = k3.get("source_sha256")
    if (not isinstance(source_sha, str) or len(source_sha) != 64
            or any(ch not in "0123456789abcdef" for ch in source_sha)
            or source_sha != k3_source_sha):
        raise ValueError("K2/K3 remote source bytes do not match")
    source_bytes = k2.get("source_bytes")
    if (type(source_bytes) is not int or not 0 < source_bytes <= 2_000_000
            or type(k3.get("source_bytes")) is not int
            or source_bytes != k3["source_bytes"]):
        raise ValueError("K2/K3 source byte counts do not match")
    hashes = k2.get("candidate_hashes")
    results = k3.get("results")
    if not isinstance(hashes, list) or not isinstance(results, list):
        raise ValueError("Missing candidate hashes or probe results")
    if any(not isinstance(x, str) or len(x) != 64 or
           any(ch not in "0123456789abcdef" for ch in x) for x in hashes):
        raise ValueError("Invalid K2 candidate digest")
    if len(hashes) != len(set(hashes)):
        raise ValueError("Duplicate K2 candidate digest")
    if len(hashes) > 100 or len(results) > 12:
        raise ValueError("K2/K3 evidence exceeds pilot limits")
    if type(k3.get("probed")) is not int or k3["probed"] != len(results):
        raise ValueError("K3 reported probe count does not match results")
    if type(k3.get("manifest_seen")) is not int or k3["manifest_seen"] != sum(
            item.get("hls_manifest_seen") is True for item in results if isinstance(item, dict)):
        raise ValueError("K3 reported manifest count does not match results")
    if k2.get("stream_reachability_tested") is not False or k2.get("device_verified") is not False:
        raise ValueError("K2 discovery must not claim stream or device verification")
    if k3.get("audio_video_verified") != 0:
        raise ValueError("K3 manifest pilot must not claim audio/video verification")
    observed = []
    for item in results:
        if not isinstance(item, dict):
            raise ValueError("Invalid K3 probe entry")
        digest = item.get("url_sha256")
        if not isinstance(digest, str) or len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise ValueError("Invalid K3 digest")
        observed.append(digest)
    if len(observed) != len(set(observed)):
        raise ValueError("Duplicate K3 probe")
    matched = set(hashes).intersection(observed)
    manifests = [r["url_sha256"] for r in results if r["url_sha256"] in matched
                 and r.get("hls_manifest_seen") is True]
    return {"source": source, "source_sha256": source_sha, "k2_candidates": len(hashes), "k3_probed": len(results),
            "matched_by_digest": len(matched), "matched_manifest_seen": len(manifests),
            "manifest_hashes": sorted(manifests), "audio_video_verified": False,
            "device_verified": False, "production_ready": False,
            "production_writes": False, "evidence_only": True}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Read-only K2/K3 evidence correlation")
    parser.add_argument("k2", type=Path)
    parser.add_argument("k3", type=Path)
    args = parser.parse_args(argv)
    for path in (args.k2, args.k3):
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 2_000_000:
            raise ValueError("Invalid evidence input")
    result = reconcile(json.loads(args.k2.read_text()), json.loads(args.k3.read_text()))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
