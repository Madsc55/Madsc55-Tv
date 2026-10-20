import unittest
from madsc.offline_five_gate import assess_all


class OfflineFiveGateTests(unittest.TestCase):
    def test_five_fixture_checks_pass_without_production_approval(self):
        result = assess_all(lambda category: {"isolated": True})
        self.assertTrue(result["fixture_gate_passed"])
        self.assertEqual(result["categories_checked"], 5)
        self.assertFalse(result["production_ready"])
        self.assertFalse(result["production_writes"])

    def test_failed_check_blocks_batch(self):
        result = assess_all(lambda category: {"isolated": category != "k3"})
        self.assertFalse(result["fixture_gate_passed"])
        self.assertEqual(result["categories"]["k3"], "failure")

    def test_exception_blocks_batch(self):
        def executor(category):
            if category == "k2":
                raise RuntimeError("failure")
            return {"isolated": True}
        result = assess_all(executor)
        self.assertFalse(result["fixture_gate_passed"])
        self.assertEqual(result["categories_checked"], 5)
        self.assertEqual(result["errors"]["k2"], "RuntimeError")

    def test_missing_checks_block_batch(self):
        result = assess_all(lambda category: {})
        self.assertFalse(result["fixture_gate_passed"])


if __name__ == "__main__":
    unittest.main()
