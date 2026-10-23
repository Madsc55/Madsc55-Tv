"""K5 offline, read-only channel history migration; never modifies source playlists."""
import hashlib
import json
from collections.abc import Mapping
from madsc.isolated_ibo_classification import classify_6115_positions

STATES = {"working", "broken", "pending", "unknown"}

def build_isolated_test_pool(records):
    """Return metadata-only isolated pool; records must be ordered 1..6115."""
    if not isinstance(records, (list, tuple)) or len(records) != 6115:
        raise ValueError("Expected 6115 records")
    entries = []
    for i, (r, decision) in enumerate(zip(records, classify_6115_positions()), 1):
        if not isinstance(r, Mapping) or type(r.get("position")) is not int or r["position"] != i:
            raise ValueError("Position mismatch")
        if set(r) - {"position", "source_sha256", "logo_sha256", "history", "playback"}:
            raise ValueError("Unexpected source metadata fields")
        digest = r.get("source_sha256")
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError("Invalid source hash")
        logo = r.get("logo_sha256")
        if logo is not None and (not isinstance(logo, str) or len(logo) != 64 or any(c not in "0123456789abcdef" for c in logo)):
            raise ValueError("Invalid logo hash")
        history = r.get("history", [])
        if not isinstance(history, (list, tuple)) or len(history) > 100:
            raise ValueError("Invalid history")
        clean = []
        for h in history:
            if not isinstance(h, Mapping) or set(h) != {"status", "evidence_id"}:
                raise ValueError("Invalid evidence")
            status, eid = h["status"], h["evidence_id"]
            if not isinstance(status, str) or status not in STATES or not isinstance(eid, str) or not 0 < len(eid) <= 256 or any(ord(c) < 32 or ord(c) == 127 or 0xD800 <= ord(c) <= 0xDFFF for c in eid):
                raise ValueError("Invalid evidence")
            if "://" in eid or "/" in eid or "\\" in eid or "@" in eid:
                raise ValueError("Evidence identifier may not contain URLs or paths")
            clean.append({"status": status, "evidence_id": eid})
        reported = r.get("playback", "unknown")
        if not isinstance(reported, str) or reported not in STATES:
            raise ValueError("Invalid playback")
        playback = reported if clean and clean[-1]["status"] == reported else "unknown"
        bucket = ("broken" if playback == "broken" else
                  "foreign" if decision.country == "YABANCI_KULLANICI_BILDIRIMI" else
                  "pending" if playback in ("pending", "unknown") else "retained")
        entries.append({"position": i, "source_sha256": digest,
                        "reported_country": decision.country, "playback": playback,
                        "bucket": bucket, "logo_sha256": logo, "history": clean})
    encoded = json.dumps(entries, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {"preview_only": True, "production_writes": False, "device_verified": False,
            "entry_count": 6115, "entries_sha256": hashlib.sha256(encoded).hexdigest(),
            "counts": {s: sum(e["bucket"] == s for e in entries)
                       for s in ("foreign", "broken", "pending", "retained")},
            "entries": entries}
