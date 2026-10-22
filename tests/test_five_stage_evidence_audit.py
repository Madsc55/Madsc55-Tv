"""Five-stage audit must never turn a report into production acceptance."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
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

    def test_hardlinked_report_is_rejected(self):
        with TemporaryDirectory() as d, TemporaryDirectory() as external:
            reports = Path(d) / "reports"
            reports.mkdir()
            original = Path(external) / "evidence.json"
            original.write_text("{}")
            (reports / "k2-live-pilot.json").hardlink_to(original)
            self.assertFalse(audit(Path(d))["stages"]["K2"]["evidence_files_valid"])

    def test_replaced_report_during_read_is_rejected(self):
        with TemporaryDirectory() as d:
            reports = Path(d) / "reports"
            reports.mkdir()
            evidence = reports / "k2-live-pilot.json"
            evidence.write_text("{}")
            from madsc import five_stage_evidence_audit as module
            original_read = module.os.read
            replaced = False

            def replace_after_read(descriptor, size):
                nonlocal replaced
                data = original_read(descriptor, size)
                if data and not replaced:
                    replaced = True
                    evidence.unlink()
                    evidence.write_text("{}")
                return data

            with patch.object(module.os, "read", side_effect=replace_after_read):
                self.assertFalse(audit(Path(d))["stages"]["K2"]["evidence_files_valid"])


if __name__ == "__main__":
    unittest.main()
