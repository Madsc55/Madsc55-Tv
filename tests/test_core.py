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
