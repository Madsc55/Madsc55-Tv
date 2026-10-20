import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from madsc.stage_report_cli import build_report, main


class StageReportCLITests(unittest.TestCase):
    def test_k3_k5_real_evaluators_and_guarded_write(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            cases = {
                "k3": [{"url_sha256": "a" * 64,
                        "ffprobe": {"streams": [{"codec_type": "video"},
                                                {"codec_type": "audio"}],
                                    "format": {"duration": "40"}}}],
                "k5": [{"category": k, "production_writes": False, "status": "success"}
                       for k in ("k1", "k2", "k3", "k4", "k5")],
            }
            for stage, payload in cases.items():
                source = root / (stage + "-input.json")
                source.write_text(json.dumps(payload))
                args = ["stage_report_cli", "--stage", stage, "--input", str(source),
                        "--isolated-report-root", str(root)]
                with patch("sys.argv", args):
                    main()
                report = json.loads((root / "reports" / (stage + "-isolated-evidence.json")).read_text())
                self.assertEqual(report["category"], stage)
                self.assertFalse(report["production_ready"])
                self.assertFalse(report["production_writes"])
                with patch("sys.argv", args), self.assertRaises(FileExistsError):
                    main()

    def test_invalid_stage_and_bad_payload_rejected(self):
        with self.assertRaises(ValueError):
            build_report("k4", [])
        with self.assertRaises(ValueError):
            build_report("k3", {"unexpected": True})
        with self.assertRaises(ValueError):
            build_report("k5", {"unexpected": True})


if __name__ == "__main__":
    unittest.main()
