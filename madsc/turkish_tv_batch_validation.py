"""Single-run multi-source discovery and bounded video/audio validation. No playlist writes."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path

from madsc.legacy_multisource_discovery import SOURCES, scan, RADIO
from madsc.k3_turkish_tv_video_pilot import verify_av, category

MAX_PROBES = min(1000, max(1, int(os.environ.get("MADSC_MAX_PROBES", "1000"))))
TURKISH_FEEDS = ("-TR", "TURKCE", "TURKIYE", "TURK_KANAL", "iptv-turk")
def eligible_source(name):
    return any(term in name.upper() for term in ("-TR", "TURKCE", "TURKIYE")) or name == "iptv-turk-tr"

def run():
    found = {}
    sources_ok = 0
    total = 0
    source_by_digest = {}
    source_errors = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for name, entries, error in pool.map(scan, SOURCES.items()):
            if error is None:
                sources_ok += 1
            else:
                source_errors[name] = "source_scan_failed"
            if not eligible_source(name) or error is not None:
                continue
            for title, url in entries:
                total += 1
                if any(w in title.casefold() for w in RADIO):
                    continue
                if not url.startswith("https://"):
                    continue
                key = hashlib.sha256(url.encode()).hexdigest()
                found.setdefault(key, (title, url))
                source_by_digest.setdefault(key, set()).add(name)
    chosen = sorted(found.items(), key=lambda item: item[0])[:MAX_PROBES]
    discovery_fingerprint = hashlib.sha256("\n".join(sorted(found)).encode("ascii")).hexdigest()
    by_digest = dict(chosen)
    def test(item):
        digest, (title, url) = item
        try:
            video, audio, reason = verify_av(url)
        except Exception:
            video, audio, reason = False, False, "blocked_or_unreachable"
        return {"name": title[:100], "sha256": digest,
                "source_names": sorted(source_by_digest[digest]),
                "video": video, "reason": reason,
                "audio": audio, "turkish_audio": "not_verified"}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(test, chosen))
    reasons = {k: sum(x["reason"] == k for x in results) for k in sorted(set(x["reason"] for x in results))}
    report = {"stage": "BATCH_DISCOVER_VALIDATE",
              "selection_policy": "sha256_ascending_stable",
              "discovery_fingerprint_sha256": discovery_fingerprint,
              "selected_candidate_sha256": [digest for digest, _ in chosen],
              "source_provenance_declared_only": True, "sources_checked": len(SOURCES),
              "sources_ok": sources_ok, "source_failures": source_errors,
              "source_failures_count": len(source_errors),
              "entries_in_turkish_feeds": total,
              "unique_https_nonradio_candidates": len(found), "tested": len(results),
              "video_verified": sum(x["video"] for x in results),
              "video_and_audio_verified": sum(x["video"] and x["audio"] for x in results),
              "audio_verified": sum(x["audio"] for x in results), "turkish_audio_verified": 0,
              "playlist_modified": False, "reason_counts": reasons, "results": results}
    # Export only public-source candidates with both A/V codecs for manual playback.
    # This is NOT the production playlist and does NOT certify spoken Turkish.
    playlist = ["#EXTM3U"]
    exported = 0
    for result in results:
        if not (result["video"] and result["audio"]):
            continue
        title, url = by_digest[result["sha256"]]
        safe_title = title.replace("\\r", " ").replace("\\n", " ").replace('"', "'")[:100]
        group = category(safe_title)
        if not group:
            continue
        playlist.append(f'#EXTINF:-1 group-title="{group}",{safe_title}')
        playlist.append(url)
        exported += 1
    playlist_out = Path("reports/MADSC55_TURKCE_TV_ADAY_DENEME.m3u8")
    playlist_out.parent.mkdir(parents=True, exist_ok=True)
    playlist_out.write_text("\n".join(playlist) + "\n", encoding="utf-8")
    report["test_playlist_candidates"] = exported
    report["production_approved"] = False
    report["three_stage_six_hour_verified"] = False
    report["device_verified"] = False
    report["test_playlist_language_status"] = "unverified"
    out = Path("reports/turkish-tv-batch-validation.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k != "results"}, ensure_ascii=False))

if __name__ == "__main__":
    run()
