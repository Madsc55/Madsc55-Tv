#!/usr/bin/env python3
"""K3 read-only, bounded ffprobe audit. Never edits playlists or candidate input."""
import argparse
import csv
import datetime as dt
import hashlib
import json
import subprocess
import time
from pathlib import Path
from urllib.parse import urlsplit

def candidates(path, limit):
    seen = set()
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            url = (row.get("YAYIN_URL") or "").strip()
            try:
                p = urlsplit(url)
                valid = p.scheme in ("http", "https") and bool(p.hostname) and not p.username and not p.password and not p.fragment and not any(c.isspace() for c in url) and "\\\\" not in url
            except ValueError:
                valid = False
            if not valid or url in seen:
                continue
            seen.add(url)
            yield {"name": (row.get("KANAL") or "")[:100], "url": url, "id": hashlib.sha256(url.encode()).hexdigest()[:16]}
            if len(seen) >= limit:
                return

def probe(item, timeout):
    cmd = ["ffprobe", "-v", "error", "-rw_timeout", str(timeout * 1000000),
           "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate",
           "-of", "json", item["url"]]
    try:
        p = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True,
                           text=True, timeout=timeout + 5, check=False)
        if p.returncode:
            return {"status": "probe_failed", "video": False, "audio": False}
        streams = json.loads(p.stdout).get("streams", [])
        return {"status": "ok" if any(s.get("codec_type") == "video" for s in streams) and any(s.get("codec_type") == "audio" for s in streams) else "incomplete",
                "video": any(s.get("codec_type") == "video" for s in streams),
                "audio": any(s.get("codec_type") == "audio" for s in streams),
                "codecs": sorted({s.get("codec_name", "") for s in streams if s.get("codec_name")}),
                "video_details": [{"width": s.get("width"), "height": s.get("height"), "fps": s.get("r_frame_rate")} for s in streams if s.get("codec_type") == "video"]}
    except (subprocess.TimeoutExpired, OSError, ValueError, json.JSONDecodeError):
        return {"status": "probe_error", "video": False, "audio": False}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--limit", type=int, default=75)
    ap.add_argument("--hours", type=float, default=6)
    ap.add_argument("--interval-minutes", type=float, default=60)
    ap.add_argument("--timeout", type=int, default=12)
    args = ap.parse_args()
    if not (1 <= args.limit <= 75 and 0 <= args.hours <= 24 and args.interval_minutes > 0 and 1 <= args.timeout <= 30):
        ap.error("invalid bounded test parameters")
    if args.candidates.resolve() == args.output.resolve():
        ap.error("output cannot overwrite input")
    items = list(candidates(args.candidates, args.limit))
    if len(items) != args.limit:
        ap.error(f"only {len(items)} unique valid candidates; requested {args.limit}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    end = start + args.hours * 3600
    index = 0
    with args.output.open("x", encoding="utf-8") as out:
        while True:
            for item in items:
                result = probe(item, args.timeout)
                record = {"timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                          "round": index, "candidate_id": item["id"], "channel": item["name"], **result}
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                out.flush()
            index += 1
            if args.hours == 0 or time.monotonic() >= end:
                break
            wait = start + index * args.interval_minutes * 60 - time.monotonic()
            if wait > 0:
                time.sleep(min(wait, max(0, end - time.monotonic())))
            if time.monotonic() >= end:
                break
    print(f"Completed {index} round(s) for {len(items)} candidates; inspect {args.output}. Device acceptance not included.")

if __name__ == "__main__":
    main()
