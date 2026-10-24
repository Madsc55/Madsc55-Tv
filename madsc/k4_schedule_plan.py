"""Offline K4 schedule planner; never triggers a backup or contacts a provider."""
from __future__ import annotations

import argparse
import datetime as dt
import json
from zoneinfo import ZoneInfo

ZONE = "Europe/Stockholm"
DAYS = (1, 15)


def planned_slots(year: int, month: int, hour: int = 3) -> list[dict]:
    """Return deterministic local slots and UTC instants for a single month.

    03:00 local is never ambiguous or skipped on Stockholm DST transition days
    (transitions happen on the last Sunday, not the 1st or 15th).
    """
    if type(year) is not int or not 2000 <= year <= 2100:
        raise ValueError("invalid year")
    if type(month) is not int or not 1 <= month <= 12:
        raise ValueError("invalid month")
    if type(hour) is not int or not 0 <= hour <= 23:
        raise ValueError("invalid hour")
    if DAYS != (1, 15):
        raise ValueError("K4 schedule days must remain the 1st and 15th")
    zone = ZoneInfo(ZONE)
    slots = []
    for day in DAYS:
        local = dt.datetime(year, month, day, hour, tzinfo=zone)
        # Both folds must agree; otherwise this wall clock is ambiguous or skipped.
        if local.utcoffset() != local.replace(fold=1).utcoffset():
            raise ValueError("ambiguous or nonexistent local time")
        utc = local.astimezone(dt.timezone.utc)
        if utc.astimezone(zone).replace(fold=0) != local:
            raise ValueError("ambiguous or nonexistent local time")
        slots.append({
            "idempotency_key": f"k4:{year:04d}-{month:02d}-{day:02d}:{hour:02d}:{ZONE}",
            "local": local.isoformat(),
            "utc": utc.isoformat().replace("+00:00", "Z"),
            "mode": "dry_run_only",
        })
    return slots


def main() -> None:
    parser = argparse.ArgumentParser(description="K4 offline schedule preview; no writes")
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--month", type=int, required=True)
    args = parser.parse_args()
    print(json.dumps({"production_writes": False, "scheduler_enabled": False,
                      "slots": planned_slots(args.year, args.month)}, sort_keys=True))


if __name__ == "__main__":
    main()
