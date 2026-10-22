"""K5 candidate review must reject oversized untrusted batches."""
import unittest
from madsc.maintenance import review_candidate_batch


class K5CandidateReviewLimitTests(unittest.TestCase):
    def test_oversized_candidate_batch_fails_closed(self):
        coordination = {"candidates": [None] * 10001}
        with self.assertRaisesRegex(ValueError, "safe review limit"):
            review_candidate_batch(coordination, {})

    def test_empty_safe_batch_does_not_claim_completion(self):
        coordination = {
            "candidates": [], "production_writes": False,
            "production_ready": False, "network_probed": False,
        }
        backup = {
            "production_writes": False,
            "production_restore_verified": False,
            "external_storage_proven": False,
            "independent_sandbox_restore_matches": True,
        }
        result = review_candidate_batch(coordination, backup)
        self.assertEqual(result["candidate_count"], 0)
        self.assertFalse(result["review_evidence_complete"])
        self.assertFalse(result["production_ready"])


if __name__ == "__main__":
    unittest.main()
