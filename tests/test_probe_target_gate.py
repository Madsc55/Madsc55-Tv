import unittest
from madsc.probe_target_gate import (validate_probe_target, validate_resolved_addresses,
                                     validate_probe_handoff)
from madsc.artifact_handoff import pack
import hashlib


class ProbeTargetGateTests(unittest.TestCase):
    def test_authorization_required_and_no_network_claim(self):
        with self.assertRaises(PermissionError):
            validate_probe_target("https://video.example.com/live.m3u8")
        result = validate_probe_target("https://video.example.com/live.m3u8", authorized=True)
        self.assertEqual(len(result["url_sha256"]), 64)
        self.assertFalse(result["network_probed"])
        self.assertFalse(result["production_ready"])
        self.assertEqual(result["target_kind"], "DNS_REQUIRES_CONNECT_TIME_PINNING")

    def test_block_private_and_unsafe_targets(self):
        urls = (
            "http://video.example.com/a", "https://localhost/a",
            "https://127.0.0.1/a", "https://10.0.0.1/a",
            "https://169.254.169.254/latest/meta-data",
            "https://[::1]/a", "https://user:password@video.example.com/a",
            "https://video.example.com:8443/a", "https://host.internal/a",
            "https://video.example.com/a#fragment", "https://video.example.com/a\n",
            "https://host/a", "https://video.example.com\\\\@127.0.0.1/a",
        )
        for url in urls:
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_probe_target(url, authorized=True)


    def test_dns_answers_all_public_and_unique(self):
        self.assertEqual(validate_resolved_addresses(["8.8.8.8", "1.1.1.1"]),
                         ("8.8.8.8", "1.1.1.1"))
        self.assertEqual(validate_resolved_addresses(["8.8.8.8", "8.8.8.8"]),
                         ("8.8.8.8",))
        for answers in ([], ["8.8.8.8", "127.0.0.1"], ["169.254.169.254"],
                        ["::1"], ["invalid"],
                        ["::ffff:8.8.8.8"]):
            with self.subTest(answers=answers), self.assertRaises(ValueError):
                validate_resolved_addresses(answers)

    def test_k2_provenance_required_before_probe(self):
        url = "https://video.example.com/live.m3u8"
        run, sha = "12345", "a" * 40
        digest = hashlib.sha256(url.encode()).hexdigest()
        envelope = pack({"candidates": [{"url_sha256": digest}]}, run, sha)
        with self.assertRaises(PermissionError):
            validate_probe_handoff(url, envelope, run, sha)
        valid = validate_probe_handoff(url, envelope, run, sha, authorized=True)
        self.assertEqual(valid["k2_source_digest"], envelope["digest"])
        self.assertFalse(valid["network_probed"])
        self.assertFalse(valid["redirects_allowed"])
        self.assertTrue(valid["dns_pinning_required"])
        for bad_url, bad_run in (("https://other.example.com/live", run), (url, "999")):
            with self.assertRaises(ValueError):
                validate_probe_handoff(bad_url, envelope, bad_run, sha, authorized=True)


if __name__ == "__main__":
    unittest.main()
