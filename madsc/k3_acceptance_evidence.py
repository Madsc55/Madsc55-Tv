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
        stamp = datetime.fromisoformat(data["measured_at_utc"])
        if stamp.tzinfo is None or stamp.utcoffset() is None:
            raise ValueError("Timezone required")
        rows = data.get("results")
        if (data.get("stage") != "K3_REAL_NETWORK_MANIFEST_PILOT" or
                data.get("production_playlist_modified") is not False or
                data.get("candidate_limit") != 75 or
                data.get("candidate_shortfall") != 0 or
                data.get("probed") != 75 or not isinstance(rows, list) or len(rows) != 75):
            raise ValueError("Invalid K3 75-candidate snapshot")
        ids = [r.get("url_sha256") for r in rows]
        if any(not isinstance(h, str) or len(h) != 64 or
               any(ch not in "0123456789abcdef" for ch in h) for h in ids):
            raise ValueError("Invalid hashed channel identity")
        if len(set(ids)) != 75:
            raise ValueError("Duplicate channel identities")
        count = sum(r.get("hls_manifest_seen") is True for r in rows)
        if data.get("manifest_seen") != count:
            raise ValueError("Manifest count mismatch")
        snapshots.append((stamp.astimezone(timezone.utc), set(ids), count))
    snapshots.sort(key=lambda s: s[0])
    elapsed = (snapshots[-1][0] - snapshots[0][0]).total_seconds()
    same = len(set.intersection(*(s[1] for s in snapshots))) == 75
    passed = elapsed >= 21600 and same and all(s[2] == 75 for s in snapshots)
    return {"stage": "K3_THREE_STAGE_MANIFEST_ACCEPTANCE", "elapsed_seconds": elapsed,
            "minimum_six_hours_met": elapsed >= 21600, "same_75_candidates": same,
            "manifest_seen_each": [s[2] for s in snapshots],
            "audio_video_verified": False, "manifest_acceptance": passed,
            "full_k3_acceptance": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshots", nargs=3)
    print(json.dumps(assess(parser.parse_args().snapshots), indent=2))
