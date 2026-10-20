import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from madsc.stage_report_cli import build_report, main, load_batch_reports
from madsc.batch_acceptance import MODULES


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


    def test_k5_requires_actual_complete_category_artifacts(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for stage in ("k1", "k2", "k3", "k4", "k5"):
                folder = root / ("madsc-batch-" + stage)
                folder.mkdir()
                (folder / (stage + ".json")).write_text(json.dumps({
                    "category": stage, "module": MODULES[stage],
                    "mode": "isolated_read_only", "production_writes": False,
                    "legacy_workflows_executed": False,
                    "status": "isolated_fixture_checks_passed_not_production_verified",
                    "fixture_checks": {"isolated": True},
                    "checks": {"isolation": True, "runtime_rule_evidence": False,
                               "legacy_behavioral_equivalence": False}}))
            result = build_report("k5", load_batch_reports(root))
            self.assertTrue(result["evidence"]["all_five_successful"])
            (root / "madsc-batch-k3/k3.json").unlink()
            with self.assertRaises(ValueError):
                load_batch_reports(root)
            (root / "madsc-batch-k3/k3.json").write_text(json.dumps({
                "category": "k3", "module": MODULES["k3"],
                "mode": "isolated_read_only", "production_writes": False,
                "legacy_workflows_executed": False,
                "status": "isolated_fixture_checks_passed_not_production_verified",
                "fixture_checks": {"isolated": True},
                "checks": {"isolation": True, "runtime_rule_evidence": False,
                           "legacy_behavioral_equivalence": False}}))
            (root / "madsc-batch-k3/extra.txt").write_text("unexpected")
            with self.assertRaises(ValueError):
                load_batch_reports(root)

if __name__ == "__main__":
    unittest.main()
