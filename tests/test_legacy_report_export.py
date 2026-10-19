import csv
from datetime import datetime, timedelta, timezone
import json
import tempfile
import unittest
from pathlib import Path
from madsc.legacy_report_export import export_legacy_report


class LegacyReportExportTests(unittest.TestCase):
    def test_exports_separate_legacy_artifacts(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            scores = base / "scores.csv"
            stable = base / "stable.csv"
            with scores.open("w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=["KANAL", "PUAN", "TEKNIK_KANIT", "YAYIN_URL"])
                w.writeheader()
                w.writerow({"KANAL": "Sample", "PUAN": "35", "TEKNIK_KANIT": "VIDEO_SES_VAR",
                            "YAYIN_URL": "https://example.org/live"})
            stable.write_text("YAYIN_URL,24_SAAT_KARARLI\nhttps://example.org/live,EVET\n", encoding="utf-8")
            dest = base / "isolated_reports"
            result = export_legacy_report(str(scores), str(stable), str(dest))
            self.assertEqual(result["candidate_count"], 1)
            with (dest / "BIRLESIK_ADAY_ONAY_RAPORU.csv").open(encoding="utf-8-sig", newline="") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(rows[0]["PUAN"], "65")
            self.assertEqual(rows[0]["ANA_LISTEYE_EKLE"], "HAYIR")
            summary = json.loads((dest / "BIRLESIK_ADAY_OZET.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["toplam_aday"], 1)
            self.assertEqual(summary["kullanici_onayi_olmadan_eklenen"], 0)
            with self.assertRaises(ValueError):
                export_legacy_report(str(scores), str(stable), str(dest))

    def test_rejects_missing_header_before_creating_destination(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            scores = base / "scores.csv"
            stable = base / "stable.csv"
            scores.write_text("KANAL,PUAN\nA,20\n", encoding="utf-8")
            stable.write_text("YAYIN_URL,24_SAAT_KARARLI\n", encoding="utf-8")
            dest = base / "report"
            with self.assertRaises(ValueError):
                export_legacy_report(str(scores), str(stable), str(dest))
            self.assertFalse(dest.exists())

    def test_export_history_corroborates_csv_claim(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            scores, stable, history = (base / "scores.csv", base / "stable.csv", base / "history.json")
            scores.write_text("KANAL,PUAN,TEKNIK_KANIT,YAYIN_URL\nA,35,VIDEO_SES_VAR,https://example.org/live\n", encoding="utf-8")
            stable.write_text("YAYIN_URL,24_SAAT_KARARLI\nhttps://example.org/live,EVET\n", encoding="utf-8")
            now = datetime(2026, 10, 19, 12, tzinfo=timezone.utc)
            url = "https://example.org/live"
            history.write_text(json.dumps({url: [{"at": (now - timedelta(hours=25)).isoformat(), "state": "VIDEO_SES_VAR"},
                                                 {"at": (now - timedelta(hours=1)).isoformat(), "state": "VIDEO_SES_VAR"}]}), encoding="utf-8")
            dest = base / "reports"
            export_legacy_report(str(scores), str(stable), str(dest), history_json=str(history), now=now, require_history=True)
            with (dest / "BIRLESIK_ADAY_ONAY_RAPORU.csv").open(encoding="utf-8-sig", newline="") as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(row["PUAN"], "65")
            summary = json.loads((dest / "BIRLESIK_ADAY_OZET.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["historical_evidence_source"], "supplied_history_only")
            history.write_text("{}", encoding="utf-8")
            dest2 = base / "reports_missing_history"
            export_legacy_report(str(scores), str(stable), str(dest2), history_json=str(history), now=now)
            with (dest2 / "BIRLESIK_ADAY_ONAY_RAPORU.csv").open(encoding="utf-8-sig", newline="") as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(row["PUAN"], "35")
            self.assertEqual(row["24_SAAT_KARARLI"], "HAYIR")

    def test_invalid_history_fails_before_output(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            scores, stable, history = (base / "scores.csv", base / "stable.csv", base / "history.json")
            scores.write_text("YAYIN_URL,PUAN\nhttps://example.org/live,10\n", encoding="utf-8")
            stable.write_text("YAYIN_URL,24_SAAT_KARARLI\n", encoding="utf-8")
            history.write_text("[]", encoding="utf-8")
            dest = base / "reports"
            with self.assertRaises(ValueError):
                export_legacy_report(str(scores), str(stable), str(dest), history_json=str(history))
            self.assertFalse(dest.exists())

    def test_required_history_rejects_csv_only_export(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            scores, stable = base / "scores.csv", base / "stable.csv"
            scores.write_text("YAYIN_URL,PUAN\nhttps://example.org/live,35\n", encoding="utf-8")
            stable.write_text("YAYIN_URL,24_SAAT_KARARLI\nhttps://example.org/live,EVET\n", encoding="utf-8")
            dest = base / "reports"
            with self.assertRaises(ValueError):
                export_legacy_report(str(scores), str(stable), str(dest), require_history=True)
            self.assertFalse(dest.exists())
