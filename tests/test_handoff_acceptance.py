import unittest
from madsc.discovery import classify_candidates
from madsc.artifact_handoff import pack
from madsc.handoff_acceptance import verify

class HandoffAcceptanceTests(unittest.TestCase):
    def setUp(self):
        discovery = classify_candidates([{"name": "A", "url": "https://example.org/a.m3u8"}])
        self.k2 = pack(discovery, "123", "a" * 40)
        self.report = {"schema": "madsc-handoff-verification-v1", "run_id": "123",
                       "commit_sha": "a" * 40, "source_digest": self.k2["digest"],
                       "candidate_count": 1, "read_only": True,
                       "network_probed": False, "production_ready": False}

    def test_same_run_accepted_without_production_claim(self):
        result = verify(self.k2, self.report, self.report, "123", "a" * 40)
        self.assertTrue(result["k2_k3_k5_same_run_verified"])
        self.assertFalse(result["production_ready"])

    def test_wrong_run_rejected(self):
        with self.assertRaises(ValueError):
            verify(self.k2, self.report, self.report, "124", "a" * 40)

    def test_mismatched_k5_digest_rejected(self):
        with self.assertRaises(ValueError):
            verify(self.k2, self.report, {**self.report, "source_digest": "f" * 64}, "123", "a" * 40)

    def test_false_production_claim_rejected(self):
        with self.assertRaises(ValueError):
            verify(self.k2, {**self.report, "production_ready": True}, self.report, "123", "a" * 40)

    def test_mismatched_candidate_count_rejected(self):
        with self.assertRaises(ValueError):
            verify(self.k2, self.report, {**self.report, "candidate_count": 2}, "123", "a" * 40)
