import unittest
from madsc.k5_channel_gate import evaluate_k3_evidence


class K5ChannelGateTests(unittest.TestCase):
    def test_offline_link_is_not_live_approval(self):
        e = {"schema": "madsc-k2-k3-offline-link-v1",
             "candidate_count": 1, "probed_candidates": 0, "untested_candidates": 1,
             "network_probed": False, "ibo_device_verified": False,
             "live_continuity_verified": False, "candidate_identity_verified": False,
             "production_writes": False, "production_ready": False, "results": []}
        r = {"category": "k3", "production_writes": False,
             "production_ready": False, "evidence": e}
        result = evaluate_k3_evidence(r)
        self.assertFalse(result["production_ready"])
        self.assertTrue(result["offline_fingerprint_link_verified"])
        for key in ("network_probed", "ibo_device_verified", "live_continuity_verified"):
            bad = {"category": "k3", "production_writes": False,
                   "production_ready": False, "evidence": {**e, key: True}}
            with self.assertRaises(ValueError):
                evaluate_k3_evidence(bad)
        with self.assertRaises(ValueError):
            evaluate_k3_evidence({**r, "evidence": {**e, "untested_candidates": 0}})


if __name__ == "__main__":
    unittest.main()
