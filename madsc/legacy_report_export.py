"""Explicit opt-in legacy CSV compatibility artifact writer.

Reads two supplied CSV files; writes only to a newly created empty report
directory. Never writes to playlist, EPG, logo, or production paths.
"""
from __future__ import annotations
import csv
import json
from collections import Counter
from pathlib import Path
from madsc.legacy_unified_report import legacy_unified_rows

OUTPUT_CSV = "BIRLESIK_ADAY_ONAY_RAPORU.csv"
OUTPUT_JSON = "BIRLESIK_ADAY_OZET.json"


def export_legacy_report(scores_csv: str, stability_csv: str, output_dir: str) -> dict:
    sources = [Path(scores_csv).resolve(strict=True), Path(stability_csv).resolve(strict=True)]
    if not all(path.is_file() and path.suffix.lower() == ".csv" for path in sources):
        raise ValueError("Both sources must be CSV files")
    dest = Path(output_dir).resolve()
    if dest.exists() or dest == Path.cwd().resolve() or dest in sources:
        raise ValueError("Output must be a new report directory")
    if dest.is_relative_to(Path.cwd().resolve()):
        raise ValueError("Output directory must be outside the repository checkout")
    if any(dest == src.parent or dest in src.parents for src in sources):
        raise ValueError("Output overlaps input files")
    def load(path):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or "YAYIN_URL" not in reader.fieldnames:
                raise ValueError("Missing YAYIN_URL header")
            return list(reader)
    scores, stability = [load(path) for path in sources]
    report = legacy_unified_rows(scores, stability)
    summary = {"toplam_aday": len(report["rows"]),
               "durumlar": dict(Counter(row["DURUM"] for row in report["rows"])),
               "kullanici_onayi_olmadan_eklenen": 0,
               "uyari": "Teknik puanlama kimlik veya IBO oynatma onayi degildir. Bu is akisinin liste yazma izni yoktur."}
    dest.mkdir(parents=False, exist_ok=False)
    with (dest / OUTPUT_CSV).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=report["fields"])
        writer.writeheader()
        writer.writerows(report["rows"])
    (dest / OUTPUT_JSON).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"output_directory": str(dest), "candidate_count": len(report["rows"]),
            "production_writes": False, "runtime_probe_performed": False}
