import hashlib
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
        self.assertTrue(result["head_transport_observed"])
        self.assertFalse(result["actual_stream_measurements_verified"])
        self.assertFalse(result["production_ready"])

    def test_fail_closed_on_forged_claims(self):
        for key, value in (("http_status", 302), ("http_status", True),
                           ("url_sha256", "0" * 64), ("k2_source_digest", "fake"),
                           ("tls_verified", False), ("dns_pinned", None),
                           ("stream_continuity_verified", True),
                           ("production_ready", True), ("network_probed", 1)):
            with self.subTest(key=key, value=value):
                item = dict(self.observation, **{key: value})
                with self.assertRaises(ValueError):
                    evaluate_k3_head_observation(item, self.envelope,
                                                 self.run, self.sha)


if __name__ == "__main__":
    unittest.main()
