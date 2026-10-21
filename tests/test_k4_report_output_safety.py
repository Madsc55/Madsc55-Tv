import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from madsc import k4_evidence, restore_drill
from madsc.write_path_audit import ProtectedWriteRejected


class K4ReportOutputSafetyTests(unittest.TestCase):
    def test_restore_drill_rejects_existing_report(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            source.mkdir()
            (source / "fixture.txt").write_text("data")
            output = root / "report.json"
            output.write_text("original")
            with patch("sys.argv", ["restore_drill", "--source", str(source),
                                    "--file", "fixture.txt", "--output", str(output)]):
                with self.assertRaises(ProtectedWriteRejected):
                    restore_drill.main()
            self.assertEqual(output.read_text(), "original")

    def test_k4_evidence_rejects_protected_playlist_path(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            evidence = root / "evidence.json"
            evidence.write_text(json.dumps({
                **{key: True for key in k4_evidence.REQUIRED_TRUE},
                **{key: False for key in k4_evidence.REQUIRED_FALSE},
                "files_checked": 1,
            }))
            target = root / "CALISANLAR.m3u"
            with patch("sys.argv", ["k4_evidence", "--report", str(evidence),
                                    "--output", str(target)]):
                with self.assertRaises(ProtectedWriteRejected):
                    k4_evidence.main()
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
