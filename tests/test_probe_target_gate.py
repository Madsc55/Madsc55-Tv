import unittest
from madsc.probe_target_gate import validate_probe_target


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
            "https://host/a",
        )
        for url in urls:
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_probe_target(url, authorized=True)


if __name__ == "__main__":
    unittest.main()
