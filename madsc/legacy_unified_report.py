"""Read-only compatibility view of the legacy unified candidate report.

Input rows are already-parsed CSV dictionaries. No URLs are fetched or written.
"""
from __future__ import annotations
from madsc.legacy_scoring import legacy_approval_decision

FIELDS = ("KANAL", "PUAN", "TEKNIK_DURUM", "24_SAAT_KARARLI", "DURUM",
          "IBO_ONAYI", "KULLANICI_ONAYI", "ANA_LISTEYE_EKLE", "YAYIN_URL", "KAYNAK")


def legacy_unified_rows(scores: list[dict], stability: list[dict]) -> dict:
    if not isinstance(scores, list) or not isinstance(stability, list):
        raise ValueError("Invalid legacy CSV rows")
    if any(not isinstance(r, dict) for r in scores + stability):
        raise ValueError("Invalid legacy CSV row")
    stable_by_url = {}
    for row in stability:
        url = row.get("YAYIN_URL")
        if not isinstance(url, str) or not url:
            raise ValueError("Invalid stability URL")
        if url in stable_by_url:
            raise ValueError("Duplicate stability URL")
        stable_by_url[url] = row
    results = []
    for row in scores:
        url = row.get("YAYIN_URL")
        if not isinstance(url, str) or not url:
            raise ValueError("Invalid candidate URL")
        try:
            score = int(row.get("PUAN") or 0)
        except (ValueError, TypeError, OverflowError) as exc:
            raise ValueError("Invalid legacy candidate score") from exc
        if str(score) != str(row.get("PUAN") or "0") or score < 0:
            raise ValueError("Invalid legacy candidate score")
        stable = stable_by_url.get(url, {}).get("24_SAAT_KARARLI") == "EVET"
        technical = row.get("TEKNIK_KANIT", "")
        if not isinstance(technical, str):
            raise ValueError("Invalid technical evidence")
        decision = legacy_approval_decision(score, technical, stable)
        results.append({"KANAL": row.get("KANAL", ""), "PUAN": decision["score"],
                        "TEKNIK_DURUM": technical,
                        "24_SAAT_KARARLI": "EVET" if stable else "HAYIR",
                        "DURUM": decision["status"], "IBO_ONAYI": "YOK",
                        "KULLANICI_ONAYI": "YOK", "ANA_LISTEYE_EKLE": "HAYIR",
                        "YAYIN_URL": url, "KAYNAK": row.get("KAYNAK", "")})
    results.sort(key=lambda row: (-row["PUAN"], row["KANAL"]))
    return {"fields": list(FIELDS), "rows": results, "production_writes": False,
            "historical_stability_verified": False, "ibo_device_verified": False}
