"""Read-only legacy category snapshot and quarantine routing for new discoveries."""
from __future__ import annotations

import json
from pathlib import Path

SNAPSHOT = Path(__file__).resolve().parent.parent / "config" / "legacy_category_order_snapshot.json"
EXPECTED = {"CALISANLAR.m3u": 1039, "YABANCI_KANALLAR.m3u": 740,
            "YENILER.m3u": 58, "CALISMAYANLAR.txt": 97}


def load_historical_categories(path: str | Path = SNAPSHOT) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Historical snapshot must be an object")
    if data.get("schema") != "madsc55-legacy-order-v1":
        raise ValueError("Unexpected historical snapshot schema")
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise ValueError("Historical entries must be a list")
    if any(not isinstance(row, dict) for row in entries):
        raise ValueError("Historical entries must contain objects")
    if any(row.get("file") not in EXPECTED for row in entries):
        raise ValueError("Unknown historical source file")
    sources = data.get("source_files")
    if not isinstance(sources, list) or len(sources) != len(EXPECTED):
        raise ValueError("Historical source manifest missing or incomplete")
    source_map = {item.get("file"): item for item in sources if isinstance(item, dict)}
    if len(source_map) != len(EXPECTED) or set(source_map) != set(EXPECTED):
        raise ValueError("Historical source manifest mismatch")
    for filename, count in EXPECTED.items():
        source = source_map[filename]
        if source.get("count") != count or not isinstance(source.get("sha"), str) or len(source["sha"]) != 40 or any(ch not in "0123456789abcdef" for ch in source["sha"]):
            raise ValueError("Historical source manifest count or SHA invalid: " + filename)

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

def audit_historical_metadata(path: str | Path = SNAPSHOT) -> dict:
    """Read-only metadata quality audit; never silently repair approved channel data."""
    data = load_historical_categories(path)
    issues = []
    for row in data["entries"]:
        name = row.get("name")
        if not isinstance(name, str) or not name.strip():
            issues.append({"file": row["file"], "order": row["order"], "issue": "blank_name"})
        elif "tvg-logo=" in name or "group-title=" in name:
            issues.append({"file": row["file"], "order": row["order"], "issue": "embedded_m3u_attributes_in_name"})
    return {"records_checked": len(data["entries"]), "issues": issues,
            "production_writes": False, "auto_repairs": False}
