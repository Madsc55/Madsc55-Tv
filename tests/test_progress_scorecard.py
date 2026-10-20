import unittest
from madsc.progress_scorecard import scorecard


class ProgressScorecardTests(unittest.TestCase):
    def test_source_review_not_counted_as_acceptance(self):
        result = scorecard(verified_ci=True)
        self.assertEqual(result["source_inventory"]["legacy_yaml_source_review"]["done"], 99)
        self.assertEqual(result["acceptance"]["legacy_behavioral_equivalence"]["accepted"], 0)
        self.assertEqual(result["acceptance"]["runtime_security_rules"]["accepted"], 0)
        self.assertIsNone(result["calculated_overall_percent"])
        self.assertFalse(result["production_ready"])

    def test_scoped_rates_are_calculated_without_fake_overall(self):
        result = scorecard(accepted_behaviors=46, accepted_security=13)
        progress = result["measured_progress"]
        self.assertEqual(progress["legacy_behavioral_acceptance_percent"], 50.0)
        self.assertEqual(progress["runtime_security_acceptance_percent"], 50.0)
        self.assertEqual(progress["combined_acceptance_percent"], 50.0)
        self.assertEqual(progress["combined_acceptance_denominator"], 118)
        self.assertIsNone(result["calculated_overall_percent"])
        self.assertFalse(result["production_ready"])

    def test_invalid_counts_rejected(self):
        for value in (-1, 93, True, 1.2):
            with self.assertRaises(ValueError):
                scorecard(accepted_behaviors=value)
        with self.assertRaises(ValueError):
            scorecard(accepted_security=27)
        with self.assertRaises(ValueError):
            scorecard(verified_ci="true")


if __name__ == "__main__":
    unittest.main()
