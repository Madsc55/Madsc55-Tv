"""Bounded real HTTPS HLS reachability pilot; no playlist mutation or redirects."""
import hashlib
import ipaddress
import json
from pathlib import Path
from madsc.fixture_report_writer import write_fixture_report
import socket
import subprocess
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from madsc.probe_target_gate import validate_probe_target, validate_resolved_addresses

SOURCE = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u"
LIMIT = 12


def candidates(source_evidence=None):
    with urlopen(Request(SOURCE, headers={"User-Agent": "Madsc55-Tv-K3-pilot"}), timeout=15) as r:
        raw = r.read(300_001)
    if len(raw) > 300_000 or not raw.startswith(b"#EXTM3U"):
        raise ValueError("Unexpected source size or format")
    if source_evidence is not None:
        source_evidence["source_sha256"] = hashlib.sha256(raw).hexdigest()
        source_evidence["source_bytes"] = len(raw)
    from madsc.remote_m3u_parser import parse_remote_m3u
    for row in parse_remote_m3u(raw, max_bytes=300_000):
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
    result = subprocess.run(command, capture_output=True, timeout=11, check=False)
    body = result.stdout[:65536]
    is_manifest = result.returncode == 0 and body.lstrip().startswith(b"#EXTM3U")
    return {"url_sha256": gate["url_sha256"], "https_reachable": result.returncode == 0,
            "hls_manifest_seen": is_manifest, "audio_video_verified": False,
            "response_bytes": len(body), "curl_exit_code": result.returncode}


def run():
    results = []
    source_evidence = {}
    for name, url in candidates(source_evidence):
        if len(results) >= LIMIT:
            break
        try:
            result = probe(url)
            result["status"] = "manifest_only" if result["hls_manifest_seen"] else "unverified"
        except (ValueError, PermissionError, OSError, subprocess.TimeoutExpired) as exc:
            result = {"url_sha256": hashlib.sha256(url.encode()).hexdigest(),
                      "status": "blocked_or_unreachable", "error_type": type(exc).__name__,
                      "audio_video_verified": False}
        results.append(result)
    report = {"stage": "K3_REAL_NETWORK_MANIFEST_PILOT", "source": SOURCE,
              **source_evidence,
              "probed": len(results), "manifest_seen": sum(x.get("hls_manifest_seen", False) for x in results),
              "audio_video_verified": 0, "production_playlist_modified": False,
              "results": results}
    out = Path("reports/k3-real-manifest-pilot.json")
    write_fixture_report(Path.cwd(), out.as_posix(), json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "results"}))


if __name__ == "__main__":
    run()
