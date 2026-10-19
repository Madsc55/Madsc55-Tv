import csv
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
