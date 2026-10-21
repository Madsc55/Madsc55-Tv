import hashlib
import json
import unittest

from madsc.artifact_handoff import pack
from madsc.k5_channel_gate import evaluate_k3_head_observation


class K5HeadObservationTests(unittest.TestCase):
    def setUp(self):
        self.run = "123"
        self.sha = "a" * 40
        self.digest = hashlib.sha256(b"https://video.example.com/a").hexdigest()
        self.envelope = pack({"candidates": [{"url_sha256": self.digest}]},
                             self.run, self.sha)
        self.observation = {
            "schema": "madsc-k3-https-head-observation-v1",
            "url_sha256": self.digest, "k2_source_digest": self.envelope["digest"],
            "run_id": self.run, "commit_sha": self.sha, "http_status": 200,
            "tls_verified": True, "dns_pinned": True, "network_probed": True,
            "redirects_followed": False, "stream_continuity_verified": False,
            "ibo_device_verified": False, "production_writes": False,
            "production_ready": False}

    def test_head_transport_never_grants_stream_acceptance(self):
        result = evaluate_k3_head_observation(self.observation, self.envelope,
                                              self.run, self.sha)
        self.assertTrue(result["head_transport_claim_validated"])
        self.assertFalse(result["head_transport_independently_verified"])
        self.assertFalse(result["actual_stream_measurements_verified"])
        self.assertFalse(result["production_ready"])
        self.assertTrue(result["http_success_status"])
        self.assertEqual(result["observation_sha256"], hashlib.sha256(
            json.dumps(self.observation, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False).encode("utf-8")).hexdigest())

    def test_fail_closed_on_forged_claims(self):
        for key, value in (("http_status", 302), ("http_status", True),
                           ("url_sha256", "0" * 64), ("k2_source_digest", "fake"),
                           ("tls_verified", False), ("dns_pinned", None),
                           ("stream_continuity_verified", True),
                           ("production_ready", True), ("network_probed", 1),
                           ("actual_network_measurements_verified", True),
                           ("actual_stream_measurements_verified", True),
                           ("live_continuity_verified", True),
                           ("candidate_identity_verified", True),
                           ("channel_identity_verified", True),
                           ("production_change_allowed", True),
                           ("production_approved", True),
                           ("ibo_approved", True),
                           ("head_transport_independently_verified", True)):
            with self.subTest(key=key, value=value):
                item = dict(self.observation, **{key: value})
                with self.assertRaises(ValueError):
                    evaluate_k3_head_observation(item, self.envelope,
                                                 self.run, self.sha)


    def test_rejects_unknown_and_missing_fields(self):
        for extra in ({"hidden_approval": True}, {"extra": "harmless"}):
            with self.subTest(extra=extra):
                with self.assertRaises(ValueError):
                    evaluate_k3_head_observation(
                        dict(self.observation, **extra), self.envelope,
                        self.run, self.sha)
        for missing in ("tls_verified", "http_status", "schema"):
            with self.subTest(missing=missing):
                altered = dict(self.observation)
                del altered[missing]
                with self.assertRaises(ValueError):
                    evaluate_k3_head_observation(
                        altered, self.envelope, self.run, self.sha)

    def test_digest_changes_on_evidence_change(self):
        baseline = evaluate_k3_head_observation(
            self.observation, self.envelope, self.run, self.sha)
        altered = evaluate_k3_head_observation(
            dict(self.observation, http_status=204), self.envelope,
            self.run, self.sha)
        self.assertNotEqual(baseline["observation_sha256"],
                            altered["observation_sha256"])
        self.assertFalse(altered["head_transport_independently_verified"])

    def test_non_success_http_is_not_live_success(self):
        for status in (100, 401, 403, 404, 500):
            with self.subTest(status=status):
                result = evaluate_k3_head_observation(
                    dict(self.observation, http_status=status), self.envelope,
                    self.run, self.sha)
                self.assertFalse(result["http_success_status"])
                self.assertFalse(result["production_ready"])


if __name__ == "__main__":
    unittest.main()
