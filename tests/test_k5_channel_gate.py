import unittest
from madsc.k5_channel_gate import evaluate_k3_evidence
from madsc.artifact_handoff import pack


class K5ChannelGateTests(unittest.TestCase):
    def test_offline_link_is_not_live_approval(self):
        e = {"schema": "madsc-k2-k3-offline-link-v1",
             "candidate_count": 1, "probed_candidates": 0, "untested_candidates": 1,
             "network_probed": False, "ibo_device_verified": False,
             "live_continuity_verified": False, "candidate_identity_verified": False,
             "production_writes": False, "production_ready": False, "results": [],
             "technical_samples_supplied": False,
             "preliminary_passes": 0, "needs_review": 0}
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
        sample = {"url_sha256": "b" * 64, "technical_status": "NEEDS_REVIEW",
                  "stream_continuity_verified": False, "channel_identity_verified": False,
                  "ibo_device_verified": False, "production_change_allowed": False}
        measured = {**e, "probed_candidates": 1, "untested_candidates": 0,
                    "technical_samples_supplied": True, "needs_review": 1,
                    "results": [sample]}
        for flag in ("actual_network_measurements_verified", "network_probed",
                     "live_continuity_verified", "stream_continuity_verified",
                     "candidate_identity_verified", "channel_identity_verified",
                     "ibo_device_verified", "production_writes", "production_ready",
                     "production_change_allowed"):
            forged = {**sample, flag: True}
            with self.subTest(flag=flag), self.assertRaises(ValueError):
                evaluate_k3_evidence({**r, "evidence": {**measured, "results": [forged]}})
        for flag in ("actual_network_measurements_verified", "stream_continuity_verified",
                     "channel_identity_verified", "production_change_allowed"):
            with self.subTest(envelope_flag=flag), self.assertRaises(ValueError):
                evaluate_k3_evidence({**r, "evidence": {**measured, flag: True}})
        for invalid in (None, 1, "true"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                evaluate_k3_evidence({**r, "evidence": {**measured,
                    "results": [{**sample, "actual_network_measurements_verified": invalid}]}})
        with self.assertRaises(ValueError):
            evaluate_k3_evidence({**r, "evidence": {**e, "untested_candidates": 0}})
        with self.assertRaises(ValueError):
            evaluate_k3_evidence({**r, "evidence": {**e, "technical_samples_supplied": True}})
        with self.assertRaises(ValueError):
            evaluate_k3_evidence({**r, "evidence": {**e, "preliminary_passes": 1}})
        run, sha = "123", "a" * 40
        envelope = pack({"candidates": [{"url_sha256": "b" * 64, "name": "Fixture channel"}]}, run, sha)
        linked = {**e, "run_id": run, "commit_sha": sha,
                  "source_digest": envelope["digest"]}
        valid = {**r, "evidence": linked}
        self.assertFalse(evaluate_k3_evidence(valid, envelope, run, sha)["production_ready"])
        for bad in ({"source_digest": "c" * 64}, {"run_id": "124"},
                    {"candidate_count": 2, "untested_candidates": 2}):
            with self.assertRaises(ValueError):
                evaluate_k3_evidence({**r, "evidence": {**linked, **bad}}, envelope, run, sha)
        with self.assertRaises(ValueError):
            evaluate_k3_evidence(valid, envelope, "124", sha)


if __name__ == "__main__":
    unittest.main()
