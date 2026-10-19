"""Execute pinned priority script and import pinned retest planner on fixtures."""
import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from madsc.legacy_priority_retest import priority_rows, retest_rows

FIXTURES = Path(__file__).parent / "fixtures"


class PriorityRetestDifferentialTests(unittest.TestCase):
    def test_priority_all_five_tiers_and_casefold_tiebreak(self):
        rows = [
            {"KANAL": "Zulu", "DURUM": "UNKNOWN", "ADAY_TURU": "OLD", "MEDYA_TEST": ""},
            {"KANAL": "beta", "DURUM": "TEKNIK_TEKRAR_DOGRULANDI_KIMLIK_BEKLIYOR",
             "ADAY_TURU": "YENI_KANAL_ADAYI", "MEDYA_TEST": ""},
            {"KANAL": "Alpha", "DURUM": "TEKNIK_TEKRAR_DOGRULANDI_KIMLIK_BEKLIYOR",
             "ADAY_TURU": "YENI_KANAL_ADAYI", "MEDYA_TEST": ""},
            {"KANAL": "Older", "DURUM": "TEKNIK_TEKRAR_DOGRULANDI_KIMLIK_BEKLIYOR",
             "ADAY_TURU": "OLD", "MEDYA_TEST": ""},
            {"KANAL": "MediaNew", "DURUM": "UNKNOWN", "ADAY_TURU": "YENI_KANAL_ADAYI",
             "MEDYA_TEST": "VIDEO_SES_VAR"},
            {"KANAL": "MediaOld", "DURUM": "UNKNOWN", "ADAY_TURU": "OLD",
             "MEDYA_TEST": "VIDEO_SES_VAR"},
        ]
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "aday_bekletme").mkdir()
            source = root / "aday_bekletme" / "ADAY_DURUM_RAPORU.csv"
            with source.open("w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            script = root / "aday_oncelik_raporu.py"
            script.write_bytes((FIXTURES / "legacy_aday_oncelik_raporu.py").read_bytes())
            run = subprocess.run([sys.executable, str(script)], cwd=root,
                                 capture_output=True, text=True, timeout=10)
            self.assertEqual(run.returncode, 0, run.stderr)
            with (root / "aday_bekletme" / "ADAY_ONCELIK_RAPORU.csv").open(
                    encoding="utf-8-sig", newline="") as f:
                actual = list(csv.DictReader(f))
            expected = [{k: str(v) for k, v in row.items()} for row in priority_rows(rows)]
            self.assertEqual(actual, expected)
            self.assertEqual([int(x["ONCELIK"]) for x in actual], [1, 1, 2, 3, 4, 5])
            self.assertEqual([x["KANAL"] for x in actual[:2]], ["Alpha", "beta"])

    def test_retest_boundaries_and_success_counts(self):
        spec = importlib.util.spec_from_file_location(
            "pinned_legacy_retest_plan", FIXTURES / "legacy_akilli_tekrar_test_takvimi.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        now = datetime(2026, 10, 20, 12, 0, tzinfo=timezone.utc)
        records = {}
        for hours, success_count, passed in [
            (2, 0, False), (6, 0, True), (12, 2, True), (24, 3, True)
        ]:
            for minutes in (-1, 0, 1):
                key = f"https://example.invalid/{hours}/{minutes}"
                records[key] = {
                    "name": key, "last_seen": (
                        now - __import__("datetime").timedelta(hours=hours, minutes=minutes)
                    ).isoformat(),
                    "technical": "TEKNIK_AKIS_VAR" if passed else "FAILED",
                    "media": "VIDEO_SES_VAR" if passed else "UNKNOWN",
                    "successful_runs": [{}] * success_count}
        old = module.plan(records, now)
        new = retest_rows(records, now)
        self.assertEqual(old, new)
        self.assertEqual(sum(row["TEST_ZAMANI_GELDI"] == "EVET" for row in new), 8)


if __name__ == "__main__":
    unittest.main()
