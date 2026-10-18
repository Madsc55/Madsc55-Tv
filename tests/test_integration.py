import tempfile
import unittest
from pathlib import Path
from madsc.core import CATEGORIES, run

class IntegratedTests(unittest.TestCase):
    def test_all_five_execute_fixture_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            for category in CATEGORIES:
                report = run(category, Path(directory) / (category + ".json"))
                self.assertTrue(all(report["fixture_checks"].values()))
                self.assertFalse(report["production_writes"])
                self.assertFalse(report["checks"]["runtime_rule_evidence"])
                self.assertFalse(report["checks"]["legacy_behavioral_equivalence"])
                self.assertTrue((Path(directory) / (category + ".json")).is_file())

if __name__ == "__main__":
    unittest.main()
