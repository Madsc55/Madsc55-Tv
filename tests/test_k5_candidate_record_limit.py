"""K5 rejects oversized candidate dictionaries before accepting evidence."""
import unittest
from madsc.maintenance import review_candidate_batch


class K5CandidateRecordLimitTests(unittest.TestCase):
    def test_oversized_candidate_record_rejected(self):
        record = {f"extra_{i}": False for i in range(33)}
        coordination = {"candidates": [record]}
        with self.assertRaisesRegex(ValueError, "Oversized candidate"):
            review_candidate_batch(coordination, {})

    def test_small_malformed_candidate_still_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid or repeated candidate"):
            review_candidate_batch({"candidates": [{}]}, {})


if __name__ == "__main__":
    unittest.main()
