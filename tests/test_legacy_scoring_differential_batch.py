"""Batch differential: execute pinned legacy scoring CLI against new scoring.

The pinned fixture is not independently authenticated old-repo source. This is
script-level offline comparison, never full workflow parity or production proof.
"""
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from madsc.legacy_scoring import legacy_technical_score

LEGACY = Path(__file__).parent / "fixtures" / "legacy_akilli_aday_puanla.py"
FIELDS = ["KANAL", "YAYIN_URL", "TEKNIK_MEDYA", "SES_IZI", "COZUNURLUK",
          "LOGO_ADAY_URL", "ADAY_TURU", "KAYNAK"]


class ScoringDifferentialBatch(unittest.TestCase):
    def test_cli_and_new_scoring_on_batch_with_duplicates_and_boundaries(self):
        vectors = [
            ("VIDEO_SES_VAR", "", "1920x1080", "https://example.invalid/l"),
            ("YALNIZ_VIDEO", "true", "1280x720", ""),
            ("YALNIZ_VIDEO", "false", "640x360", "http://example.invalid/l"),
            ("BAD", "true", "1920x1080", "https://example.invalid/l"),
            ("VIDEO_SES_VAR", "", "1920x1079", ""),
            ("VIDEO_SES_VAR", "", "1920x719", ""),
            ("YALNIZ_VIDEO", "TRUE", "invalid", "https://example.invalid/l"),
            ("", "", "", ""),
        ]
        rows = [
            dict(zip(FIELDS, [f"Candidate {i}", f"https://example.invalid/{i}",
                              *vector, "NEW", "fixture"]))
            for i, vector in enumerate(vectors)
        ]
        # Same URL appears twice: CLI keeps only highest scoring row.
        rows += [
            dict(zip(FIELDS, ["Duplicate low", "https://example.invalid/0",
                              "BAD", "", "", "", "OLD", "fixture"])),
            dict(zip(FIELDS, ["Ignored", "file:///not-a-stream",
                              "VIDEO_SES_VAR", "", "", "", "OLD", "fixture"])),
        ]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "candidates.csv"
            with source.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            proc = subprocess.run(
                [sys.executable, str(LEGACY), str(source), "--output", "scores.csv"],
                cwd=root, capture_output=True, text=True, timeout=15)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with (root / "scores.csv").open(encoding="utf-8-sig", newline="") as handle:
                actual = list(csv.DictReader(handle))
            self.assertEqual(len(actual), len(vectors))
            self.assertEqual(len({row["YAYIN_URL"] for row in actual}), len(vectors))
            for i, (technical, audio, resolution, logo) in enumerate(vectors):
                with self.subTest(i=i):
                    item = next(row for row in actual
                                if row["YAYIN_URL"] == f"https://example.invalid/{i}")
                    expected = legacy_technical_score(technical, audio, resolution, logo)
                    self.assertEqual(int(item["PUAN"]), expected["score"])
                    self.assertEqual(item["DURUM"], expected["status"])
                    self.assertEqual(item["ANA_LISTEYE_EKLENEBILIR"], "HAYIR")
                    self.assertEqual(item["KIMLIK_DOGRULANDI"], "HAYIR")
            self.assertEqual(actual, sorted(actual,
                key=lambda row: (-int(row["PUAN"]), row["KANAL"])))
            summary = json.loads((root / "AKILLI_ADAY_OZET.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["aday_sayisi"], len(vectors))
            self.assertEqual(summary["en_yuksek_puan"],
                             max(int(row["PUAN"]) for row in actual))
            self.assertFalse((root / "CALISANLAR.m3u").exists())


if __name__ == "__main__":
    unittest.main()
