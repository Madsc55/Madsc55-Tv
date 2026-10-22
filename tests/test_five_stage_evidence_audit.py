"""Five-stage audit must never turn a report into production acceptance."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from madsc.five_stage_evidence_audit import audit


class EvidenceAuditTests(unittest.TestCase):
    def test_all_five_stages_report_missing_without_acceptance(self):
        with TemporaryDirectory() as d:
            result = audit(Path(d))
            self.assertEqual(set(result["stages"]), {"K1", "K2", "K3", "K4", "K5"})
            self.assertFalse(result["production_ready"])
            self.assertFalse(result["production_writes"])
            self.assertTrue(all(not x["evidence_files_valid"] for x in result["stages"].values()))

    def test_valid_report_does_not_imply_runtime_verification(self):
        with TemporaryDirectory() as d:
            reports = Path(d) / "reports"
            reports.mkdir()
            (reports / "k2-live-pilot.json").write_text(json.dumps({"accepted": 100}))
            result = audit(Path(d))
            self.assertTrue(result["stages"]["K2"]["evidence_files_valid"])
            self.assertFalse(result["stages"]["K2"]["runtime_verified"])
            self.assertFalse(result["stages"]["K2"]["production_accepted"])

    def test_symlinked_report_directory_is_rejected(self):
        with TemporaryDirectory() as d, TemporaryDirectory() as external:
            (Path(external) / "k2-live-pilot.json").write_text("{}")
            (Path(d) / "reports").symlink_to(external, target_is_directory=True)
            self.assertFalse(audit(Path(d))["stages"]["K2"]["evidence_files_valid"])


if __name__ == "__main__":
    unittest.main()
