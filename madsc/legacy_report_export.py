"""Explicit opt-in legacy CSV compatibility artifact writer.

Reads two supplied CSV files; writes only to a newly created empty report
directory. Never writes to playlist, EPG, logo, or production paths.
"""
from __future__ import annotations
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from madsc.legacy_unified_report import legacy_unified_rows

OUTPUT_CSV = "BIRLESIK_ADAY_ONAY_RAPORU.csv"
OUTPUT_JSON = "BIRLESIK_ADAY_OZET.json"


def export_legacy_report(scores_csv: str, stability_csv: str, output_dir: str, *,
                         history_json: str | None = None, now: datetime | None = None,
                         require_history: bool = False) -> dict:
    if type(require_history) is not bool or (require_history and history_json is None):
        raise ValueError("Historical measurements required for verified export")
    sources = [Path(scores_csv).resolve(strict=True), Path(stability_csv).resolve(strict=True)]
    if not all(path.is_file() and path.suffix.lower() == ".csv" for path in sources):
        raise ValueError("Both sources must be CSV files")
    if history_json is not None:
        history_path = Path(history_json).resolve(strict=True)
        if not history_path.is_file() or history_path.suffix.lower() != ".json":
            raise ValueError("History source must be JSON")
        sources.append(history_path)
        with history_path.open(encoding="utf-8") as handle:
            history = json.load(handle)
        if not isinstance(history, dict):
            raise ValueError("History must be a URL mapping")
        if now is None:
            now = datetime.now(timezone.utc)
    else:
        history = None
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
    scores, stability = [load(path) for path in sources[:2]]
    report = legacy_unified_rows(scores, stability, history=history, now=now)
    summary = {"toplam_aday": len(report["rows"]),
               "durumlar": dict(Counter(row["DURUM"] for row in report["rows"])),
               "kullanici_onayi_olmadan_eklenen": 0,
               "historical_evidence_source": report["historical_evidence_source"],
               "historical_evidence_supplied": history is not None,
               "history_required": require_history,
               "uyari": "Teknik puanlama kimlik veya IBO oynatma onayi degildir. Bu is akisinin liste yazma izni yoktur."}
    dest.mkdir(parents=False, exist_ok=False)
    with (dest / OUTPUT_CSV).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=report["fields"])
        writer.writeheader()
        writer.writerows(report["rows"])
    (dest / OUTPUT_JSON).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"output_directory": str(dest), "candidate_count": len(report["rows"]),
            "production_writes": False, "runtime_probe_performed": False}
