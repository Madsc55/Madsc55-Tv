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

    def test_truthy_nonboolean_is_rejected(self):
        result = assess_all(lambda category: {"isolated": 1})
        self.assertFalse(result["fixture_gate_passed"])
        self.assertEqual(len(result["errors"]), 5)

    def test_one_stage_failure_does_not_skip_other_stages(self):
        visited = []
        def executor(category):
            visited.append(category)
            if category == "k2":
                raise RuntimeError("failed")
            return {"isolated": True}
        result = assess_all(executor)
        self.assertEqual(visited, ["k1", "k2", "k3", "k4", "k5"])
        self.assertFalse(result["fixture_gate_passed"])

    def test_real_k1_to_k5_fixture_integration(self):
        # Unlike mocked decision tests, exercise the actual five stage executors.
        result = assess_all()
        self.assertEqual(result["categories_checked"], 5)
        self.assertEqual(set(result["categories"]), {"k1", "k2", "k3", "k4", "k5"})
        self.assertTrue(result["fixture_gate_passed"], result["errors"])
        self.assertFalse(result["production_ready"])
        self.assertFalse(result["production_writes"])
        self.assertEqual(result["legacy_92_behavioral_acceptance"], 0)
        self.assertEqual(result["runtime_security_26_acceptance"], 0)

    def test_real_k5_joins_candidate_and_independent_restore(self):
        from madsc.core import execute
        checks = execute("k5")
        self.assertIs(checks["k2_k3_k4_k5_candidate_restore_review"], True)
        self.assertIs(checks["k4_corruption_blocks_k5_review"], True)
        self.assertIs(checks["k1_guards_k5_report_write"], True)

    def test_missing_checks_block_batch(self):
        result = assess_all(lambda category: {})
        self.assertFalse(result["fixture_gate_passed"])


if __name__ == "__main__":
    unittest.main()
