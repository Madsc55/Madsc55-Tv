"""Read-only K3 three-stage manifest acceptance gate."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path


def assess(paths):
    if len(paths) != 3 or len({str(Path(p).resolve()) for p in paths}) != 3:
        raise ValueError("Three distinct snapshot files required")
    snapshots = []
    for path in paths:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Invalid K3 snapshot object")
        if not isinstance(data.get("measured_at_utc"), str):
            raise ValueError("Invalid K3 snapshot timestamp")
        try:
            stamp = datetime.fromisoformat(data["measured_at_utc"])
        except ValueError as exc:
            raise ValueError("Invalid K3 snapshot timestamp") from exc
        if stamp.tzinfo is None or stamp.utcoffset() is None:
            raise ValueError("Timezone required")
        rows = data.get("results")
        if (data.get("stage") != "K3_REAL_NETWORK_MANIFEST_PILOT" or
                data.get("production_playlist_modified") is not False or
                data.get("candidate_limit") != 75 or
                data.get("candidate_shortfall") != 0 or
                data.get("probed") != 75 or not isinstance(rows, list) or len(rows) != 75):
            raise ValueError("Invalid K3 75-candidate snapshot")
        # A manifest-only snapshot must never claim decoded audio/video.
        if type(data.get("audio_video_verified", 0)) is not int or data.get("audio_video_verified", 0) != 0:
            raise ValueError("Manifest-only snapshot claims audio/video verification")
        if any(not isinstance(r, dict) for r in rows):
            raise ValueError("Invalid K3 result row")
        if any(r.get("audio_video_verified", False) is not False for r in rows):
            raise ValueError("Manifest-only row claims audio/video verification")
        ids = [r.get("url_sha256") for r in rows]
        if any(not isinstance(h, str) or len(h) != 64 or
               any(ch not in "0123456789abcdef" for ch in h) for h in ids):
            raise ValueError("Invalid hashed channel identity")
        if len(set(ids)) != 75:
            raise ValueError("Duplicate channel identities")
        count = sum(r.get("hls_manifest_seen") is True for r in rows)
        if type(data.get("manifest_seen")) is not int or data.get("manifest_seen") != count:
            raise ValueError("Manifest count mismatch")
        for row in rows:
            if row.get("hls_manifest_seen") not in (True, False, None):
                raise ValueError("Invalid manifest observation type")
            if row.get("hls_manifest_seen") is True:
                if row.get("status") != "manifest_only" or row.get("https_reachable") is not True:
                    raise ValueError("Inconsistent successful probe evidence")
            elif row.get("status") == "manifest_only":
                raise ValueError("Unverified probe marked as manifest-only")
        snapshots.append((stamp.astimezone(timezone.utc), set(ids), count))
    snapshots.sort(key=lambda s: s[0])
    elapsed = (snapshots[-1][0] - snapshots[0][0]).total_seconds()
    adjacent_intervals = [(snapshots[i + 1][0] - snapshots[i][0]).total_seconds()
                          for i in range(2)]
    intervals_met = all(seconds >= 21600 for seconds in adjacent_intervals)
    same = len(set.intersection(*(s[1] for s in snapshots))) == 75
    passed = intervals_met and same and all(s[2] == 75 for s in snapshots)
    return {"stage": "K3_THREE_STAGE_MANIFEST_ACCEPTANCE", "elapsed_seconds": elapsed,
            "minimum_six_hours_met": intervals_met,
            "adjacent_interval_seconds": adjacent_intervals, "same_75_candidates": same,
            "manifest_seen_each": [s[2] for s in snapshots],
            "audio_video_verified": False, "manifest_acceptance": passed,
            "full_k3_acceptance": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshots", nargs=3)
    print(json.dumps(assess(parser.parse_args().snapshots), indent=2))
