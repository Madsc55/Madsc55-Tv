"""Read-only legacy category snapshot and quarantine routing for new discoveries."""
from __future__ import annotations

import json
from pathlib import Path

SNAPSHOT = Path(__file__).resolve().parent.parent / "config" / "legacy_category_order_snapshot.json"
EXPECTED = {"CALISANLAR.m3u": 1039, "YABANCI_KANALLAR.m3u": 740,
            "YENILER.m3u": 58, "CALISMAYANLAR.txt": 97}


def load_historical_categories(path: str | Path = SNAPSHOT) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema") != "madsc55-legacy-order-v1":
        raise ValueError("Unexpected historical snapshot schema")
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise ValueError("Historical entries must be a list")
    if any(not isinstance(row, dict) for row in entries):
        raise ValueError("Historical entries must contain objects")
    if any(row.get("file") not in EXPECTED for row in entries):
        raise ValueError("Unknown historical source file")
    for filename, count in EXPECTED.items():
        selected = [row for row in entries if row.get("file") == filename]
        if len(selected) != count or [row.get("order") for row in selected] != list(range(count)):
            raise ValueError("Historical channel order or count changed: " + filename)
    if len(entries) != sum(EXPECTED.values()):
        raise ValueError("Unexpected historical records")
    return data


def route_discovered_candidates(candidates: list[dict]) -> dict:
    """New channels stay in an isolated queue, not in protected YENILER or YEDEKLER lists."""
    if not isinstance(candidates, list):
        raise ValueError("Candidates must be a list")
    queued = []
    for index, candidate in enumerate(candidates):
        if (not isinstance(candidate, dict) or not isinstance(candidate.get("name"), str)
                or not candidate["name"].strip()):
            raise ValueError("Invalid discovery candidate")
        queued.append({"discovery_order": index, "name": candidate["name"],
                       "destination": "IZOLE_ADAY_TEST_KUYRUGU",
                       "requires_k3_probe": True, "requires_user_ibo_decision": True,
                       "production_change_allowed": False})
    return {"queued": queued, "production_writes": False, "existing_order_modified": False}
