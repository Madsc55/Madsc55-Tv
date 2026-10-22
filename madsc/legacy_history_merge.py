"""Read-only K2 history merge contract; never writes checkout or artifacts."""
import json
from datetime import datetime, timezone

FILES = {"gecmis.json": "history", "ana_liste_test_gecmisi.json": "channels"}
OBSERVATIONS = {"runs", "successful_runs", "last_test", "last_success", "last_result", "resolution"}


def stamp(value):
    if value is None:
        return datetime.min.replace(tzinfo=timezone.utc)
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Observation timestamp has no timezone")
    return parsed


def merge_pair(base, incoming):
    if not isinstance(base, dict) or not isinstance(incoming, dict):
        raise ValueError("Invalid history bundles")
    for bundle in (base, incoming):
        for filename, key in FILES.items():
            if (not isinstance(bundle.get(filename), dict)
                    or not isinstance(bundle[filename].get(key), dict)
                    or len(bundle[filename][key]) > 20000
                    or any(not isinstance(k, str) or not isinstance(v, dict)
                           for k, v in bundle[filename][key].items())):
                raise ValueError("Invalid history records")
    merged = json.loads(json.dumps(base))
    changes = {}
    for filename, key in FILES.items():
        records = merged[filename][key]
        added = updated = 0
        for identity, observation in incoming[filename][key].items():
            if identity not in records:
                records[identity] = observation.copy()
                added += 1
                continue
            old = records[identity]
            old_time, new_time = stamp(old.get("last_test")), stamp(observation.get("last_test"))
            if new_time > old_time:
                if observation.get("runs", old.get("runs", 0)) < old.get("runs", 0):
                    raise ValueError("Newer observation has a regressed run count")
                for field in OBSERVATIONS:
                    if field in observation:
                        old[field] = observation[field]
                updated += 1
            elif new_time == old_time and old_time != stamp(None):
                if any(old.get(field) != observation.get(field) for field in OBSERVATIONS):
                    raise ValueError("Conflicting observations at the same timestamp")
            if "source_history" in observation:
                old["source_history"] = sorted(set(old.get("source_history", []))
                                               | set(observation["source_history"]))
        changes[filename] = {"added": added, "updated": updated, "total": len(records)}
    return merged, changes
