"""Bounded real HTTPS HLS reachability pilot; no playlist mutation or redirects."""
import argparse
import hashlib
import ipaddress
import json
from datetime import datetime, timezone
from pathlib import Path
from madsc.fixture_report_writer import write_fixture_report
import socket
import subprocess
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from madsc.probe_target_gate import validate_probe_target, validate_resolved_addresses
from madsc.discovery import normalize_url

SOURCE = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u"
LIMIT = 12
MAX_LIMIT = 75
SOURCE_MAX_BYTES = 2_000_000  # Same cap as K2 discovery


def candidates(source_evidence=None, source_file=None):
    if source_file is None:
        with urlopen(Request(SOURCE, headers={"User-Agent": "Madsc55-Tv-K3-pilot"}), timeout=15) as r:
            raw = r.read(SOURCE_MAX_BYTES + 1)
    else:
        source_path = Path(source_file)
        if source_path.is_symlink() or not source_path.is_file():
            raise ValueError("Invalid source snapshot")
        with source_path.open("rb") as source:
            raw = source.read(SOURCE_MAX_BYTES + 1)
    if len(raw) > SOURCE_MAX_BYTES or not raw.startswith(b"#EXTM3U"):
        raise ValueError("Unexpected source size or format")
    if source_evidence is not None:
        source_evidence["source_sha256"] = hashlib.sha256(raw).hexdigest()
        source_evidence["source_bytes"] = len(raw)
    from madsc.remote_m3u_parser import parse_remote_m3u
    for row in parse_remote_m3u(raw, max_bytes=SOURCE_MAX_BYTES):
        yield row["name"], row["url"]


def probe(url):
    gate = validate_probe_target(url, authorized=True)
    parts = urlsplit(url)
    addresses = validate_resolved_addresses(
        [a[4][0] for a in socket.getaddrinfo(parts.hostname, 443, type=socket.SOCK_STREAM)]
    )
    # Pin the checked IP at the TLS connection. No proxy, no redirects, no config,
    # no credentials in logs; bounded bytes and time.
    pinned = addresses[0]
    resolve = f"{parts.hostname}:443:{'[' + pinned + ']' if ':' in pinned else pinned}"
    command = [
        "curl", "-q", "--silent", "--show-error", "--fail", "--noproxy", "*",
        "--proto", "=https", "--max-time", "9", "--connect-timeout", "4",
        "--max-filesize", "65536", "--range", "0-65535",
        "--resolve", resolve, url,
    ]
    result = subprocess.run(command, capture_output=True, timeout=11, check=False,
                            stdin=subprocess.DEVNULL)
    body = result.stdout[:65536]
    is_manifest = result.returncode == 0 and body.lstrip().startswith(b"#EXTM3U")
    return {"url_sha256": gate["url_sha256"], "https_reachable": result.returncode == 0,
            "hls_manifest_seen": is_manifest, "audio_video_verified": False,
            "response_bytes": len(body), "curl_exit_code": result.returncode}


def run(source_file=None, limit=LIMIT):
    if not isinstance(limit, int) or not 1 <= limit <= MAX_LIMIT:
        raise ValueError("Candidate limit must be between 1 and 75")
    results = []
    seen_hashes = set()
    source_evidence = {}
    # Keep the first requested number of candidates while still exhausting the generator:
    # the source SHA-256 must describe the complete downloaded snapshot.
    for name, url in candidates(source_evidence, source_file):
        if len(results) >= limit:
            continue
        try:
            normalized_url = normalize_url(url)
        except ValueError:
            continue
        # This pilot only probes HTTPS; HTTP candidates remain K2-only evidence.
        if urlsplit(normalized_url).scheme != "https":
            continue
        digest = hashlib.sha256(normalized_url.encode()).hexdigest()
        if digest in seen_hashes:
            continue
        seen_hashes.add(digest)
        try:
            result = probe(normalized_url)
            result["status"] = "manifest_only" if result["hls_manifest_seen"] else "unverified"
        except (ValueError, PermissionError, OSError, subprocess.TimeoutExpired) as exc:
            result = {"url_sha256": digest,
                      "status": "blocked_or_unreachable", "error_type": type(exc).__name__,
                      "audio_video_verified": False}
        results.append(result)
    # Timestamp the completed observation, not the beginning of source discovery.
    measured_at_utc = datetime.now(timezone.utc).isoformat()
    report = {"stage": "K3_REAL_NETWORK_MANIFEST_PILOT", "source": SOURCE,
              "measured_at_utc": measured_at_utc, "candidate_limit": limit,
              "candidate_shortfall": max(0, limit - len(results)),
              **source_evidence,
              "probed": len(results), "manifest_seen": sum(x.get("hls_manifest_seen", False) for x in results),
              "audio_video_verified": 0, "production_playlist_modified": False,
              "results": results}
    out = Path("reports/k3-real-manifest-pilot.json")
    write_fixture_report(Path.cwd(), out.as_posix(), json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "results"}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bounded K3 HTTPS manifest pilot")
    parser.add_argument("--source-file", type=Path)
    parser.add_argument("--limit", type=int, default=LIMIT, help="HTTPS candidates to probe (1-75)")
    args = parser.parse_args()
    run(args.source_file, limit=args.limit)
