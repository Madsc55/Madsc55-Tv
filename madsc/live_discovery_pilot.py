"""Read-only K2 live discovery pilot from one allowlisted public playlist."""
import hashlib
import json
import argparse
from pathlib import Path
from madsc.fixture_report_writer import write_fixture_report
from urllib.request import Request, urlopen

from madsc.discovery import classify_candidates

SOURCE = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u"
MAX_BYTES = 2_000_000
MAX_ROWS = 100


def run(source_file=None):
    if source_file is None:
        request = Request(SOURCE, headers={"User-Agent": "Madsc55-Tv-readonly-pilot/1.0"})
        with urlopen(request, timeout=20) as response:
            data = response.read(MAX_BYTES + 1)
    else:
        source_path = Path(source_file)
        if source_path.is_symlink() or not source_path.is_file():
            raise ValueError("Invalid source snapshot")
        with source_path.open("rb") as source:
            data = source.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Source exceeds pilot byte limit")
    from madsc.remote_m3u_parser import parse_remote_m3u
    rows = parse_remote_m3u(data, max_bytes=MAX_BYTES)
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
    write_fixture_report(Path.cwd(), out.as_posix(), json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "candidate_hashes"}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read-only K2 discovery")
    parser.add_argument("--source-file", type=Path)
    run(parser.parse_args().source_file)
