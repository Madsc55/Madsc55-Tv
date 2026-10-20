"""Read-only K2 live discovery pilot from one allowlisted public playlist."""
import hashlib
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

from madsc.discovery import classify_candidates

SOURCE = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u"
MAX_BYTES = 2_000_000
MAX_ROWS = 100


def run():
    request = Request(SOURCE, headers={"User-Agent": "Madsc55-Tv-readonly-pilot/1.0"})
    with urlopen(request, timeout=20) as response:
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Source exceeds pilot byte limit")
    text = data.decode("utf-8-sig")
    if not text.lstrip().startswith("#EXTM3U"):
        raise ValueError("Invalid source M3U")
    rows = []
    name = None
    for line in text.splitlines()[1:]:
        line = line.strip()
        if line.startswith("#EXTINF:"):
            name = line.split(",", 1)[-1].strip() if "," in line else None
        elif line and not line.startswith("#"):
            if name:
                rows.append({"name": name, "url": line})
            name = None
    selected = rows[:MAX_ROWS]
    result = classify_candidates(selected)
    report = {
        "mode": "REAL_REMOTE_SOURCE_READ_ONLY",
        "source": SOURCE,
        "source_sha256": hashlib.sha256(data).hexdigest(),
        "source_bytes": len(data),
        "parsed_total": len(rows),
        "pilot_evaluated": len(selected),
        "accepted": len(result["candidates"]),
        "duplicates": len(result["duplicates"]),
        "rejected": len(result["rejected"]),
        "candidate_hashes": [x["url_sha256"] for x in result["candidates"]],
        "stream_reachability_tested": False,
        "device_verified": False,
        "production_playlist_modified": False,
        "note": "Live source ingestion only; no playback or stream verification",
    }
    out = Path("reports/k2-live-pilot.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "candidate_hashes"}))


if __name__ == "__main__":
    run()
