"""Read-only Turkish television K3 video verification, no radio or playlist writes."""
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path
from madsc.fixture_report_writer import write_fixture_report
from urllib.parse import urljoin, urlsplit

from madsc.k3_live_manifest_pilot import candidates, probe
from madsc.probe_target_gate import validate_probe_target

LIMIT = 12
MAX_SOURCE_ROWS = 120  # Bound source scanning even when every row is radio.
MAX_SEGMENT = 1_500_000
CATEGORIES = ("🇹🇷 ULUSAL", "📺 HABER", "⚽ SPOR", "🌍 BELGESEL", "🧸 ÇOCUK", "🎧 MÜZİK", "📍 YEREL", "🕌 DİNİ", "⭐ FAVORİLER", "🔄 ALTERNATİF", "⭐ YENİLER", "📦 YEDEKLER")


def category(name):
    n = name.casefold()
    if any(x in n for x in ("radyo", "radio", "fm ", " fm", "music radio")):
        return None
    if any(x in n for x in ("haber", "news", "ntv", "cnn", "a haber", "trt haber")):
        return CATEGORIES[1]
    if any(x in n for x in ("spor", "sport", "futbol")):
        return CATEGORIES[2]
    if any(x in n for x in ("belgesel", "documentary")):
        return CATEGORIES[3]
    if any(x in n for x in ("çocuk", "kids", "çizgi")):
        return CATEGORIES[4]
    if any(x in n for x in ("müzik", "music", "kral pop")):
        return CATEGORIES[5]
    if any(x in n for x in ("diyanet", "kur'an", "kuran")):
        return CATEGORIES[7]
    return CATEGORIES[0]


def safe_curl(url, limit):
    validate_probe_target(url, authorized=True)
    # Use a fixed public HTTPS domain only for the first independent playback pilot.
    # Reject redirecting and untrusted nested media URLs; do not follow redirects.
    from madsc.k3_live_manifest_pilot import socket, validate_resolved_addresses
    p = urlsplit(url)
    ips = validate_resolved_addresses([a[4][0] for a in socket.getaddrinfo(p.hostname, 443, type=socket.SOCK_STREAM)])
    pin = ips[0]
    resolver = f"{p.hostname}:443:{'[' + pin + ']' if ':' in pin else pin}"
    cmd = ["curl", "-q", "-fsS", "--noproxy", "*", "--proto", "=https", "--max-time", "9",
           "--connect-timeout", "4", "--max-filesize", str(limit), "--resolve", resolver, url]
    result = subprocess.run(cmd, capture_output=True, timeout=11,
                            stdin=subprocess.DEVNULL)
    return result.stdout if result.returncode == 0 and len(result.stdout) <= limit else None


def same_origin_https(parent, child):
    """Reject scheme downgrade, credentials, nonstandard ports and cross-origin HLS URLs."""
    a, b = urlsplit(parent), urlsplit(child)
    try:
        return (a.scheme == b.scheme == "https" and a.hostname == b.hostname
                and a.port in (None, 443) and b.port in (None, 443)
                and not a.username and not a.password and not b.username and not b.password)
    except ValueError:
        return False


def verify_av(url):
    """Verify codec streams from an HLS segment; audio language is not inferred."""
    manifest = safe_curl(url, 65536)
    if not manifest or not manifest.lstrip().startswith(b"#EXTM3U") or len(manifest) > 65536:
        return False, False, "no_manifest"
    text = manifest.decode("utf-8-sig", errors="replace")
    if any(line.strip().startswith("#EXT-X-STREAM-INF:") for line in text.splitlines()):
        lines = [line.strip() for line in text.splitlines()]
        variants = [lines[i + 1] for i, line in enumerate(lines[:-1])
                    if line.startswith("#EXT-X-STREAM-INF") and lines[i + 1]
                    and not lines[i + 1].startswith("#")]
        if not variants:
            return False, False, "no_variant"
        nested = urljoin(url, variants[0])
        if not same_origin_https(url, nested):
            return False, False, "cross_host_variant"
        url = nested
        manifest = safe_curl(url, 65536)
        if not manifest:
            return False, False, "variant_unreachable"
        if not manifest.lstrip().startswith(b"#EXTM3U") or len(manifest) > 65536:
            return False, False, "invalid_variant_manifest"
        text = manifest.decode("utf-8-sig", errors="replace")
    if any(line.lstrip().startswith('#EXT-X-STREAM-INF') for line in text.splitlines()):
        return False, False, 'nested_master_manifest'
    if any(line.lstrip().startswith(('#EXT-X-KEY:', '#EXT-X-SESSION-KEY:'))
           for line in text.splitlines()):
        return False, False, 'encrypted_hls_unsupported'
    if any(line.lstrip().startswith(("#EXT-X-MEDIA:", "#EXT-X-SESSION-DATA:"))
           for line in text.splitlines()):
        return False, False, "alternate_media_unsupported"
    if any(line.lstrip().startswith(("#EXT-X-MAP:", "#EXT-X-I-FRAME-STREAM-INF:"))
           for line in text.splitlines()):
        return False, False, "unsupported_hls_media_layout"
    if any(line.lstrip().startswith(("#EXT-X-BYTERANGE:", "#EXT-X-PART:", "#EXT-X-PRELOAD-HINT:",
                                     "#EXT-X-SKIP:", "#EXT-X-RENDITION-REPORT:",
                                     "#EXT-X-DISCONTINUITY", "#EXT-X-GAP"))
           for line in text.splitlines()):
        return False, False, "unsupported_hls_segment_layout"
    segments = [line.strip() for line in text.splitlines()
                if line.strip() and not line.lstrip().startswith("#")]
    if not segments:
        return False, False, "no_segments"
    segment_url = urljoin(url, segments[0])
    if not same_origin_https(url, segment_url):
        return False, False, "cross_host_segment"
    payload = safe_curl(segment_url, MAX_SEGMENT)
    if not payload or len(payload) < 188 or len(payload) > MAX_SEGMENT:
        return False, False, "segment_unreachable"
    with tempfile.TemporaryDirectory() as folder:
        segment = Path(folder) / "sample.ts"
        segment.write_bytes(payload)
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
                 "-of", "json", str(segment)], capture_output=True, timeout=8,
                stdin=subprocess.DEVNULL)
            if result.returncode != 0:
                return False, False, "probe_error"
            decoded = json.loads(result.stdout or b"{}")
            if not isinstance(decoded, dict) or not isinstance(decoded.get("streams", []), list):
                return False, False, "probe_error"
            streams = decoded.get("streams", [])
            if any(not isinstance(stream, dict) for stream in streams):
                return False, False, "probe_error"
        except (subprocess.TimeoutExpired, ValueError, OSError):
            return False, False, "probe_error"
    video = any(stream.get("codec_type") == "video" for stream in streams)
    audio = any(stream.get("codec_type") == "audio" for stream in streams)
    return video, audio, "video_audio_detected" if video and audio else (
        "video_detected" if video else "audio_only" if audio else "no_av")


def verify_video(url):
    video, _audio, reason = verify_av(url)
    return video, reason


def run():
    results = []
    verified = []
    tv_tested = 0
    source_rows = 0
    seen_tv_urls = set()
    from itertools import islice
    for name, url in islice(candidates(), MAX_SOURCE_ROWS):
        if tv_tested >= LIMIT:
            break
        source_rows += 1
        cat = category(name)
        digest = hashlib.sha256(url.encode()).hexdigest()
        if not cat:
            results.append({"sha256": digest, "status": "radio_excluded"})
            continue
        if digest in seen_tv_urls:
            results.append({"sha256": digest, "status": "duplicate_excluded"})
            continue
        seen_tv_urls.add(digest)
        tv_tested += 1
        try:
            ok, reason = verify_video(url)
        except (ValueError, OSError, subprocess.TimeoutExpired):
            ok, reason = False, "blocked_or_unreachable"
        results.append({"sha256": digest, "status": reason, "video_verified": ok})
        if ok:
            verified.append({"name": name, "category": cat, "sha256": digest})
    report = {"stage": "K3_REAL_TURKISH_TV_VIDEO_PILOT", "tested": tv_tested,
              "source_rows_scanned": min(source_rows, MAX_SOURCE_ROWS),
              "source_scan_limit": MAX_SOURCE_ROWS,
              "video_verified": len(verified), "radio_excluded": sum(x["status"] == "radio_excluded" for x in results),
              "playlist_modified": False, "language_confirmed_by_audio": False,
              "results": results, "verified_metadata": verified}
    out = Path("reports/k3-turkish-tv-video-pilot.json")
    report["reason_counts"] = {reason: sum(x["status"] == reason for x in results) for reason in sorted({x["status"] for x in results})}
    write_fixture_report(Path.cwd(), out.as_posix(), json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ("results", "verified_metadata")}))


if __name__ == "__main__":
    run()
