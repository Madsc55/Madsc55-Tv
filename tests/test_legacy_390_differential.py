"""Compare original legacy 390 batch script with new contract without network."""
import csv
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from madsc.legacy_retest_390 import evaluate_entries, parse_entries

LEGACY = Path(__file__).parent / "fixtures" / "legacy_tekrar_test_390.py"
PLAYLIST = ("#EXTM3U\n#EXTINF:-1,Good\nhttps://example.invalid/good\n"
            "#EXTINF:-1,Missing Audio\nhttps://example.invalid/video\n"
            "#EXTINF:-1,Decode Failure\nhttps://example.invalid/fail\n")


def fake_runner(args, **kwargs):
    url = next((part for part in args if isinstance(part, str)
                and part.startswith("https://example.invalid/")), "")
    if args[0] == "ffprobe":
        return SimpleNamespace(returncode=0, stderr="",
                               stdout="video\n" if url.endswith("/video")
                               else "video\naudio\n")
    return SimpleNamespace(returncode=1 if url.endswith("/fail") else 0,
                           stderr="decode failed" if url.endswith("/fail") else "",
                           stdout="")


class Legacy390DifferentialTests(unittest.TestCase):
    def test_original_script_and_new_contract_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "yedekler").mkdir()
            (root / "yedekler" / "TUM_TEKNIK_TEST_ADAYLARI_2026-10-09.m3u").write_text(
                PLAYLIST, encoding="utf-8")
            (root / "yedekler" / "tekrar_test_390.py").write_bytes(LEGACY.read_bytes())
            shim = root / "sitecustomize.py"
            shim.write_text(
                "import subprocess\n"
                "from types import SimpleNamespace\n"
                "def fake(args, **kwargs):\n"
                "    url = next((v for v in args if isinstance(v, str) and "
                "v.startswith('https://example.invalid/')), '')\n"
                "    if args[0] == 'ffprobe':\n"
                "        return SimpleNamespace(returncode=0, stderr='', "
                "stdout='video\\n' if url.endswith('/video') else 'video\\naudio\\n')\n"
                "    return SimpleNamespace(returncode=1 if url.endswith('/fail') else 0, "
                "stderr='decode failed' if url.endswith('/fail') else '', stdout='')\n"
                "subprocess.run = fake\n",
                encoding="utf-8")
            env = {**os.environ, "PYTHONPATH": str(root), "TEST_WORKERS": "1"}
            old = subprocess.run(
                [sys.executable, str(root / "yedekler" / "tekrar_test_390.py")],
                cwd=root, env=env, capture_output=True, text=True, timeout=15)
            self.assertEqual(old.returncode, 0, old.stderr)
            new = evaluate_entries(parse_entries(PLAYLIST), runner=fake_runner, workers=1)
            csv_path = root / "yedekler" / "TEKRAR_TEST_2026-10-09.csv"
            with csv_path.open(encoding="utf-8-sig", newline="") as handle:
                legacy_rows = list(csv.reader(handle))
            with __import__("io").StringIO(new["csv_text"], newline="") as handle:
                new_rows = list(csv.reader(handle))
            self.assertEqual(legacy_rows, new_rows)
            old_m3u = (root / "yedekler" / "TEKNIK_DOGRULANANLAR_2026-10-09.m3u").read_text(
                encoding="utf-8")
            self.assertEqual(old_m3u, new["technical_m3u"])
            self.assertEqual(new["technical_pass_count"], 1)
            self.assertFalse(new["identity_verified"])
            self.assertFalse(new["production_writes"])


if __name__ == "__main__":
    unittest.main()
