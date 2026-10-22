"""Batch offline differential against pinned old retest scheduler script."""
import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from madsc.legacy_priority_retest import retest_rows

LEGACY = Path(__file__).parent / "fixtures" / "legacy_akilli_tekrar_test_takvimi.py"
NOW = datetime(2026, 10, 20, 12, 0, tzinfo=timezone.utc)


class LegacyRetestDifferentialBatch(unittest.TestCase):
    def test_full_interval_matrix_and_invalid_history(self):
        records = {
            "https://example.invalid/a": {"name": "fail", "technical": "FAIL",
                "media": "NO_MEDIA", "last_seen": "2026-10-20T11:00:00Z"},
            "https://example.invalid/b": {"name": "pass-one", "technical": "TEKNIK_AKIS_VAR",
                "media": "VIDEO_SES_VAR", "successful_runs": ["x"],
                "last_seen": "2026-10-20T06:00:00Z"},
            "https://example.invalid/c": {"name": "pass-two", "technical": "TEKNIK_AKIS_VAR",
                "media": "VIDEO_SES_VAR", "successful_runs": ["x", "y"],
                "last_seen": "2026-10-19T23:00:00Z"},
            "https://example.invalid/d": {"name": "pass-three", "technical": "TEKNIK_AKIS_VAR",
                "media": "VIDEO_SES_VAR", "successful_runs": ["x", "y", "z"],
                "last_seen": "2026-10-19T12:00:00Z"},
            "https://example.invalid/e": {"name": "bad-time", "technical": "FAIL",
                "last_seen": "invalid"},
            "https://example.invalid/f": "not a record",
        }
        expected = retest_rows(records, NOW)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "aday_bekletme").mkdir()
            (root / "aday_bekletme" / "gecmis.json").write_text(
                json.dumps(records), encoding="utf-8")
            # Freeze the clock explicitly in the disposable fixture script.
            # sitecustomize is not reliably imported in every embedded Python runtime.
            legacy_text = LEGACY.read_text(encoding="utf-8")
            legacy_text = legacy_text.replace(
                "now = datetime.now(timezone.utc)",
                "now = datetime(2026, 10, 20, 12, 0, tzinfo=timezone.utc)")
            self.assertNotEqual(legacy_text, LEGACY.read_text(encoding="utf-8"),
                                "legacy clock seam was not found")
            (root / "legacy.py").write_text(legacy_text, encoding="utf-8")
            env = {**os.environ, "PYTHONPATH": str(root)}
            result = subprocess.run([sys.executable, "legacy.py"], cwd=root,
                                    env=env, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            with (root / "aday_bekletme" / "AKILLI_TEKRAR_TEST_TAKVIMI.csv").open(
                    encoding="utf-8-sig", newline="") as file:
                actual = list(csv.DictReader(file))
            self.assertEqual(len(actual), len(expected))
            self.assertEqual(
                actual, [{k: str(v) for k, v in row.items()} for row in expected])
            self.assertEqual(
                {row["KANAL"]: int(row["TEST_ARALIGI_SAAT"]) for row in actual},
                {"fail": 2, "pass-one": 6, "pass-two": 12,
                 "pass-three": 24, "bad-time": 2})
            self.assertFalse((root / "CALISANLAR.m3u").exists())


if __name__ == "__main__":
    unittest.main()
