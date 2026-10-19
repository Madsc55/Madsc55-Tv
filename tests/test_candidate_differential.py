"""Differential execution against a pinned, isolated copy of the legacy script.

No network, protected playlist, or production input is used.
"""
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from madsc.legacy_candidate_merge import merge_legacy_candidate_rows

LEGACY = Path(__file__).parent / "fixtures" / "legacy_akilli_aday_puanla.py"
FIELDS = ["YAYIN_URL", "KANAL", "ADAY_TURU", "TEKNIK_MEDYA",
          "COZUNURLUK", "SES_IZI", "LOGO_ADAY_URL", "KAYNAK"]


class DifferentialCandidateTests(unittest.TestCase):
    def test_old_and_new_same_synthetic_inputs(self):
        cases = [
            {"ONCELIKLI_KANAL_TEK_NIK_RAPOR.csv": [
                {"YAYIN_URL": "https://example.invalid/a", "TEKNIK_MEDYA": "VIDEO_SES_VAR",
                 "COZUNURLUK": "1920x1080", "SES_IZI": "true"}],
             "KESIF.csv": [
                {"YAYIN_URL": "https://example.invalid/a", "KANAL": "Alpha",
                 "LOGO_ADAY_URL": "https://example.invalid/logo"},
                {"YAYIN_URL": "https://example.invalid/a", "KANAL": "Later"},
                {"YAYIN_URL": "http://example.invalid/b", "KANAL": "Beta",
                 "TEKNIK_MEDYA": "YALNIZ_VIDEO"},
                {"YAYIN_URL": "ftp://example.invalid/no", "KANAL": "Rejected"}]},
            {"KESIF.csv": []},
            {"KESIF.csv": [
                {"YAYIN_URL": "https://example.invalid/duplicate", "KANAL": "Zulu",
                 "TEKNIK_MEDYA": "YALNIZ_VIDEO"},
                {"YAYIN_URL": "https://example.invalid/duplicate", "KANAL": "Alpha",
                 "TEKNIK_MEDYA": "VIDEO_SES_VAR", "SES_IZI": "true",
                 "COZUNURLUK": "1920x1080"},
                {"YAYIN_URL": "https://example.invalid/other", "KANAL": "Other",
                 "TEKNIK_MEDYA": "BILINMIYOR"},
                {"YAYIN_URL": "not-a-url", "KANAL": "Discard"}]},
            {"ONCELIKLI_KANAL_TEK_NIK_RAPORU.csv": [
                {"YAYIN_URL": "https://example.invalid/same",
                 "TEKNIK_MEDYA": "YALNIZ_VIDEO", "SES_IZI": "false"}],
             "GENEL_ADAY_GERCEK_MEDYA_RAPORU.csv": [
                {"YAYIN_URL": "https://example.invalid/same",
                 "TEKNIK_MEDYA": "VIDEO_SES_VAR", "SES_IZI": "true",
                 "COZUNURLUK": "1280x720"}],
             "KESIF.csv": [
                {"YAYIN_URL": "https://example.invalid/same", "KANAL": "Matched",
                 "LOGO_ADAY_URL": "https://example.invalid/logo.png"}]},
            {"GENEL_ADAY_GERCEK_MEDYA_RAPORU.csv": [
                {"YAYIN_URL": "http://example.invalid/z", "KANAL": "Z",
                 "TEKNIK_MEDYA": "YALNIZ_VIDEO", "SES_IZI": "true"},
                {"YAYIN_URL": "http://example.invalid/y", "KANAL": "Y",
                 "COZUNURLUK": "1280x720"}]},
        ]
        for case in cases:
            with self.subTest(case=list(case)), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                paths = []
                inputs = []
                for filename, records in case.items():
                    path = root / filename
                    with path.open("w", encoding="utf-8-sig", newline="") as handle:
                        writer = csv.DictWriter(handle, fieldnames=FIELDS)
                        writer.writeheader()
                        writer.writerows(records)
                    paths.append(path)
                    with path.open(encoding="utf-8-sig", newline="") as handle:
                        inputs.append((path.stem, list(csv.DictReader(handle))))
                run = subprocess.run([sys.executable, str(LEGACY),
                                      *map(str, paths), "--output", str(root / "output.csv")],
                                     cwd=root, capture_output=True, text=True, timeout=10)
                self.assertEqual(run.returncode, 0, run.stderr)
                new = merge_legacy_candidate_rows(inputs)
                raw = (root / "output.csv").read_bytes()
                self.assertTrue(raw.startswith(bytes.fromhex("efbbbf")))
                with (root / "output.csv").open(encoding="utf-8-sig", newline="") as handle:
                    reader = csv.DictReader(handle)
                    self.assertEqual(reader.fieldnames, new["fields"])
                    actual = list(reader)
                expected = [{k: str(v) for k, v in row.items()} for row in new["rows"]]
                self.assertEqual(actual, expected)
                old_summary = json.loads((root / "AKILLI_ADAY_OZET.json").read_text(encoding="utf-8"))
                for key in ("aday_sayisi", "durumlar", "en_yuksek_puan", "eslesen_teknik_kanit"):
                    self.assertEqual(old_summary[key], new["summary"][key])
                self.assertEqual(json.loads(run.stdout), old_summary)
                self.assertTrue(all(row["ANA_LISTEYE_EKLENEBILIR"] == "HAYIR" for row in actual))


if __name__ == "__main__":
    unittest.main()
