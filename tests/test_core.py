import tempfile
import unittest
from pathlib import Path
from madsc.core import CATEGORIES, run, execute

class IsolationTests(unittest.TestCase):
    def test_all_five_categories_are_isolated(self):
        with tempfile.TemporaryDirectory() as directory:
            for key in CATEGORIES:
                path = Path(directory) / (key + ".json")
                result = run(key, path)
                self.assertTrue(path.exists())
                self.assertFalse(result["production_writes"])
                self.assertFalse(result["legacy_workflows_executed"])
                self.assertFalse(result["checks"]["runtime_rule_evidence"])
                self.assertFalse(result["checks"]["legacy_behavioral_equivalence"])
    def test_category_report_cannot_overwrite_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "k1.json"
            run("k1", output)
            first = output.read_bytes()
            with self.assertRaises(PermissionError):
                run("k1", output)
            self.assertEqual(output.read_bytes(), first)

    def test_category_report_rejects_protected_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "playlist.m3u8"
            with self.assertRaises(PermissionError):
                run("k1", output)
            self.assertFalse(output.exists())

    def test_protected_report_rejected_before_reports_directory_creation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "reports" / "playlist.m3u8"
            with self.assertRaises(PermissionError):
                run("k1", output)
            self.assertFalse((root / "reports").exists(),
                             "protected output must be rejected before mkdir side effects")

    def test_category_report_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.json"
            target.write_text("original", encoding="utf-8")
            link = root / "k1.json"
            link.symlink_to(target)
            with self.assertRaises(PermissionError):
                run("k1", link)
            self.assertEqual(target.read_text(encoding="utf-8"), "original")

    def test_k1_fixture_report_write_guard_in_batch(self):
        evidence = execute("k1")
        self.assertTrue(evidence["fixture_report_write_guard"])

    def test_k3_ibo_protection_is_in_batch_report(self):
        evidence = execute("k3")
        self.assertTrue(evidence["ibo_working_survives_technical_failure"])
        self.assertTrue(evidence["ibo_fixture_not_live_device_evidence"])
        self.assertTrue(evidence["ibo_report_not_device_verified"])

    def test_k3_legacy_epg_logo_and_retest_in_batch(self):
        evidence = execute("k3")
        self.assertTrue(evidence["legacy_epg_logo_pilot_join"])
        self.assertTrue(evidence["legacy_390_offline_decode_contract"])

    def test_k4_independent_restore_stays_fixture_only(self):
        evidence = execute("k4")
        self.assertTrue(evidence["three_tree_restore_fixture"])
        self.assertTrue(evidence["independent_restore_reports_no_production_proof"])
        self.assertTrue(evidence["external_backup_not_claimed"])
        self.assertTrue(evidence["restore_not_claimed"])

    def test_k5_checks_cross_category_and_no_duplicate_schedule(self):
        evidence = execute("k5")
        self.assertTrue(evidence["cross_category_handoff"])
        self.assertTrue(evidence["single_batch_no_extra_triggers"])
        self.assertTrue(evidence["no_schedule_activation"])
        self.assertTrue(evidence["no_legacy_shutdown"])

    def test_unknown_category_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                run("k6", Path(directory) / "bad.json")

if __name__ == "__main__":
    unittest.main()
