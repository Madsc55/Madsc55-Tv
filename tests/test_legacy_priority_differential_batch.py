"""Batch executable old/new priority report differential in disposable directory.

The pinned old script is a fixture; this does not establish full workflow parity.
"""
import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from madsc.legacy_priority_retest import priority_rows

LEGACY = Path(__file__).parent / "fixtures" / "legacy_aday_oncelik_raporu.py"
FIELDS = ["KANAL", "DURUM", "YAYIN_URL", "ADAY_TURU", "MEDYA_TEST"]


class LegacyPriorityDifferentialBatch(unittest.TestCase):
    def test_legacy_input_fields_can_override_computed_priority(self):
        """Record a genuine old/new discrepancy instead of hiding it."""
        fields = FIELDS + ["ONCELIK", "INCELEME_NOTU"]
        row = {"KANAL": "Injected", "DURUM": "", "YAYIN_URL": "https://example.invalid/x",
               "ADAY_TURU": "", "MEDYA_TEST": "", "ONCELIK": "999",
               "INCELEME_NOTU": "untrusted user approval"}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "aday_bekletme"
            folder.mkdir()
            with (folder / "ADAY_DURUM_RAPORU.csv").open(
                    "w", newline="", encoding="utf-8-sig") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerow(row)
            (root / "legacy.py").write_bytes(LEGACY.read_bytes())
            old = subprocess.run([sys.executable, "legacy.py"], cwd=root,
                                 capture_output=True, text=True, timeout=10)
            self.assertEqual(old.returncode, 0, old.stderr)
            with (folder / "ADAY_ONCELIK_RAPORU.csv").open(
                    encoding="utf-8-sig", newline="") as stream:
                actual = list(csv.DictReader(stream))[0]
            new = priority_rows([row])[0]
            self.assertEqual(actual["ONCELIK"], "999")
            self.assertEqual(actual["INCELEME_NOTU"], "untrusted user approval")
            self.assertEqual(new["ONCELIK"], 5)
            self.assertNotEqual(new["INCELEME_NOTU"], actual["INCELEME_NOTU"])
            self.assertFalse((root / "CALISANLAR.m3u").exists())

    def test_all_five_priority_tiers_and_tie_breaking(self):
        rows = [
            {"KANAL": "Z", "DURUM": "", "YAYIN_URL": "https://example.invalid/0",
             "ADAY_TURU": "", "MEDYA_TEST": ""},
            {"KANAL": "b", "DURUM": "TEKNIK_TEKRAR_DOGRULANDI_KIMLIK_BEKLIYOR",
             "YAYIN_URL": "https://example.invalid/1", "ADAY_TURU": "YENI_KANAL_ADAYI",
             "MEDYA_TEST": ""},
            {"KANAL": "A", "DURUM": "TEKNIK_TEKRAR_DOGRULANDI_KIMLIK_BEKLIYOR",
             "YAYIN_URL": "https://example.invalid/2", "ADAY_TURU": "YENI_KANAL_ADAYI",
             "MEDYA_TEST": ""},
            {"KANAL": "C", "DURUM": "TEKNIK_TEKRAR_DOGRULANDI_KIMLIK_BEKLIYOR",
             "YAYIN_URL": "https://example.invalid/3", "ADAY_TURU": "", "MEDYA_TEST": ""},
            {"KANAL": "D", "DURUM": "", "YAYIN_URL": "https://example.invalid/4",
             "ADAY_TURU": "YENI_KANAL_ADAYI", "MEDYA_TEST": "VIDEO_SES_VAR"},
            {"KANAL": "E", "DURUM": "", "YAYIN_URL": "https://example.invalid/5",
             "ADAY_TURU": "", "MEDYA_TEST": "VIDEO_SES_VAR"},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "aday_bekletme"
            folder.mkdir()
            with (folder / "ADAY_DURUM_RAPORU.csv").open(
                    "w", newline="", encoding="utf-8-sig") as stream:
                writer = csv.DictWriter(stream, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            (root / "legacy.py").write_bytes(LEGACY.read_bytes())
            old = subprocess.run([sys.executable, "legacy.py"], cwd=root,
                                 capture_output=True, text=True, timeout=10)
            self.assertEqual(old.returncode, 0, old.stderr)
            with (folder / "ADAY_ONCELIK_RAPORU.csv").open(
                    encoding="utf-8-sig", newline="") as stream:
                actual = list(csv.DictReader(stream))
            expected = priority_rows(rows)
            self.assertEqual(len(actual), 6)
            self.assertEqual([row["KANAL"] for row in actual],
                             [row["KANAL"] for row in expected])
            self.assertEqual([int(row["ONCELIK"]) for row in actual],
                             [row["ONCELIK"] for row in expected])
            self.assertEqual([row["INCELEME_NOTU"] for row in actual],
                             [row["INCELEME_NOTU"] for row in expected])
            self.assertEqual([int(row["ONCELIK"]) for row in actual],
                             [1, 1, 2, 3, 4, 5])
            self.assertFalse((root / "CALISANLAR.m3u").exists())


if __name__ == "__main__":
    unittest.main()
