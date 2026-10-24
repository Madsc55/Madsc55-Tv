"""Read-only contracts for legacy priority and retest schedule."""
from datetime import datetime, timedelta, timezone

PRIORITY_FIELDS = ("ONCELIK", "INCELEME_NOTU")
NOTE = "Kanal kimliği elle doğrulanmalı; otomatik ekleme yasak"


def priority_rows(rows):
    if not isinstance(rows, list) or len(rows) > 20000 or any(not isinstance(row, dict) for row in rows):
        raise ValueError("Invalid priority rows")
    def rank(row):
        verified = row.get("DURUM") == "TEKNIK_TEKRAR_DOGRULANDI_KIMLIK_BEKLIYOR"
        new = row.get("ADAY_TURU") == "YENI_KANAL_ADAYI"
        media = row.get("MEDYA_TEST") == "VIDEO_SES_VAR"
        return (0 if verified and new else 1 if verified else 2 if media and new
                else 3 if media else 4, row.get("KANAL", "").casefold())
    return [{**row, "ONCELIK": rank(row)[0] + 1, "INCELEME_NOTU": NOTE}
            for row in sorted(rows, key=rank)]


def retest_rows(records, now):
    if not isinstance(records, dict) or len(records) > 20000 or not isinstance(now, datetime) or now.tzinfo is None:
        raise ValueError("Invalid retest input")
    rows = []
    for url, record in sorted(records.items()):
        if not isinstance(record, dict):
            continue
        successes = record.get("successful_runs") or []
        last = record.get("last_seen") or record.get("first_seen")
        try:
            normalized_last = (last[:-1] + "+00:00"
                               if last.endswith("Z") else last)
            tested = (datetime.fromisoformat(normalized_last).astimezone(timezone.utc)
                      if last else now)
        except (ValueError, AttributeError):
            tested = now
        passed = record.get("technical") == "TEKNIK_AKIS_VAR" and record.get("media") == "VIDEO_SES_VAR"
        hours = 24 if passed and len(successes) >= 3 else 12 if passed and len(successes) >= 2 else 6 if passed else 2
        next_test = tested + timedelta(hours=hours)
        rows.append({"KANAL": record.get("name", ""), "YAYIN_URL": url,
                     "SON_TEST": tested.isoformat(timespec="seconds"),
                     "SONUC": "BASARILI" if passed else "TEKRAR_KONTROL",
                     "TEST_ARALIGI_SAAT": hours,
                     "SONRAKI_TEST": next_test.isoformat(timespec="seconds"),
                     "TEST_ZAMANI_GELDI": "EVET" if next_test <= now else "HAYIR"})
    return rows
