import unittest

from madsc.k1_runtime_26_evidence import assess_26_rules


class K1Runtime26EvidenceTests(unittest.TestCase):
    def test_empty_remains_unverified(self):
        report = assess_26_rules([])
        self.assertEqual(report["total_rules"], 26)
        self.assertEqual(report["observed_pass_claims"], 0)
        self.assertFalse(report["independently_accepted"])
        self.assertEqual(len(report["observations"]), 26)

    def test_pass_requires_runtime_evidence(self):
        with self.assertRaises(ValueError):
            assess_26_rules([{"rule_id": "K1-R01", "result": "pass"}])
        report = assess_26_rules([{"rule_id": "K1-R01", "result": "pass",
                                  "runtime_executed": True,
                                  "independent_evidence": "run/123"}])
        self.assertEqual(report["observed_pass_claims"], 1)
        self.assertFalse(report["independently_accepted"])

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            assess_26_rules([{"rule_id": "K1-R01", "result": "unverified"},
                             {"rule_id": "K1-R01", "result": "unverified"}])
