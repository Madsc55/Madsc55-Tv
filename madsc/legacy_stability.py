"""Validate supplied historical media observations without retiming them.

Pure compatibility check; does not perform a network probe or persist history.
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone


def _time(value: str, now: datetime) -> datetime:
    if not isinstance(value, str):
        raise ValueError("Missing measurement time")
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Invalid measurement time") from exc
    if stamp.tzinfo is None:
        raise ValueError("Measurement time must include timezone")
    stamp = stamp.astimezone(timezone.utc)
    if stamp > now + timedelta(minutes=5):
        raise ValueError("Future measurement time")
    return stamp


def evaluate_legacy_stability(observations: list[dict], now: datetime) -> dict:
    if not isinstance(now, datetime) or now.tzinfo is None:
        raise ValueError("Invalid current time")
    now = now.astimezone(timezone.utc)
    if not isinstance(observations, list) or len(observations) > 20000:
        raise ValueError("Invalid history")
    by_time = {}
    for row in observations:
        if not isinstance(row, dict) or not isinstance(row.get("state"), str) or not row["state"]:
            raise ValueError("Invalid historical observation")
        if row["state"] == "TEST_EDILMEDI":
            raise ValueError("Untested media state is not a measurement")
        if not isinstance(row.get("at"), str) or not row["at"]:
            raise ValueError("Measurement timestamp is required")
        stamp = _time(row.get("at"), now)
        if stamp in by_time and by_time[stamp] != row["state"]:
            raise ValueError("Conflicting measurements at the same time")
        by_time[stamp] = row["state"]
    window = [(t, state) for t, state in by_time.items()
              if timedelta(0) <= now - t <= timedelta(days=7)]
    window.sort()
    good = [t for t, state in window if state == "VIDEO_SES_VAR"]
    span = (good[-1] - good[0]).total_seconds() / 3600 if len(good) >= 2 else 0
    fresh = bool(window) and now - window[-1][0] <= timedelta(hours=24)
    stable = len(good) >= 2 and span >= 24 and fresh and all(
        state == "VIDEO_SES_VAR" for _, state in window)
    return {"24_SAAT_KARARLI": "EVET" if stable else "HAYIR",
            "GOZLEM_SAYISI": len(window),
            "BASARILI_VIDEO_SES_GOZLEMI": len(good),
            "BASARILI_ARALIK_SAAT": round(span, 1),
            "SON_DURUM": window[-1][1] if window else "GUNCEL_GOZLEM_YOK",
            "measurement_history_supplied_only": True,
            "network_probed": False, "ibo_device_verified": False,
            "production_writes": False}
