"""Read-only legacy scoring merge contract; no CSV or playlist writes."""
from __future__ import annotations
from collections import Counter
from .legacy_scoring import legacy_technical_score

FIELDS = ("KANAL", "ADAY_TURU", "PUAN", "DURUM", "TEKNIK_KANIT",
          "COZUNURLUK", "SES_IZI", "LOGO_ADAY_URL", "YAYIN_URL", "KAYNAK",
          "KIMLIK_DOGRULANDI", "KARARLILIK_DOGRULANDI", "ANA_LISTEYE_EKLENEBILIR")
EVIDENCE_STEMS = frozenset(("ONCELIKLI_KANAL_TEK_NIK_RAPOR",
                            "ONCELIKLI_KANAL_TEK_NIK_RAPORU",
                            "GENEL_ADAY_GERCEK_MEDYA_RAPORU"))

def _value(row, *keys):
    return next((str(row.get(k) or "").strip() for k in keys
                 if str(row.get(k) or "").strip()), "")

def merge_legacy_candidate_rows(inputs):
    """inputs: ordered (CSV filename stem, parsed DictReader rows) pairs."""
    if not isinstance(inputs, list) or len(inputs) > 200:
        raise ValueError("Invalid candidate input")
    checked = []
    for stem, rows in inputs:
        if not isinstance(stem, str) or not isinstance(rows, list) or len(rows) > 20000 or any(
                not isinstance(row, dict) for row in rows):
            raise ValueError("Invalid CSV evidence")
        checked.append((stem, rows))
    evidence = {}
    for stem, rows in checked:
        if stem not in EVIDENCE_STEMS:
            continue
        for row in rows:
            url = _value(row, "YAYIN_URL")
            if url and (url not in evidence or row.get("TEKNIK_MEDYA") == "VIDEO_SES_VAR"):
                evidence[url] = row
    candidates = {}
    for _, rows in checked:
        for original in rows:
            url = _value(original, "YAYIN_URL")
            if not url.startswith(("https://", "http://")):
                continue
            row = dict(original)
            if url in evidence:
                row.update({k: v for k, v in evidence[url].items()
                            if v and k in ("TEKNIK_MEDYA", "COZUNURLUK", "SES_IZI")})
            technical = _value(row, "TEKNIK_MEDYA", "MEDYA_TEST", "TEKNIK_TEST")
            result = legacy_technical_score(technical, _value(row, "SES_IZI"),
                                            _value(row, "COZUNURLUK"),
                                            _value(row, "LOGO_ADAY_URL"))
            item = {"KANAL": _value(row, "KANAL"),
                    "ADAY_TURU": _value(row, "ADAY_TURU", "GRUP"),
                    "PUAN": result["score"], "DURUM": result["status"],
                    "TEKNIK_KANIT": technical, "COZUNURLUK": _value(row, "COZUNURLUK"),
                    "SES_IZI": _value(row, "SES_IZI"),
                    "LOGO_ADAY_URL": _value(row, "LOGO_ADAY_URL"),
                    "YAYIN_URL": url, "KAYNAK": _value(row, "KAYNAK"),
                    "KIMLIK_DOGRULANDI": "HAYIR",
                    "KARARLILIK_DOGRULANDI": "HAYIR",
                    "ANA_LISTEYE_EKLENEBILIR": "HAYIR"}
            if url not in candidates or item["PUAN"] > candidates[url]["PUAN"]:
                candidates[url] = item
    ordered = sorted(candidates.values(), key=lambda r: (-r["PUAN"], r["KANAL"]))
    counts = Counter(r["DURUM"] for r in ordered)
    summary = {"aday_sayisi": len(ordered), "durumlar": dict(counts),
               "en_yuksek_puan": max((r["PUAN"] for r in ordered), default=0),
               "eslesen_teknik_kanit": sum(url in evidence for url in candidates),
               "network_probed": False, "production_change_allowed": False}
    return {"fields": list(FIELDS), "rows": ordered, "summary": summary}
