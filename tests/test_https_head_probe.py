import hashlib
import subprocess
from types import SimpleNamespace
import unittest
from unittest.mock import patch, MagicMock

from madsc.artifact_handoff import pack
from madsc.https_head_probe import observe_https_headers


class HTTPSHeadProbeTests(unittest.TestCase):
    def setUp(self):
        self.url = "https://video.example.com/live.m3u8"
        self.run, self.sha = "12345", "a" * 40
        self.envelope = pack({"candidates": [{
            "url_sha256": hashlib.sha256(self.url.encode()).hexdigest()
        }]}, self.run, self.sha)

    def test_opt_in_required_before_dns(self):
        with patch("madsc.https_head_probe.subprocess.run") as dns:
            with self.assertRaises(PermissionError):
                observe_https_headers(self.url, self.envelope, self.run, self.sha)
            dns.assert_not_called()

    def test_timeout_and_foreign_candidate_rejected_before_dns(self):
        with patch("madsc.https_head_probe.subprocess.run") as dns:
            for timeout in (0, -1, 6, True, float("nan"), float("inf"), float("-inf")):
                with self.subTest(timeout=timeout), self.assertRaises(ValueError):
                    observe_https_headers(self.url, self.envelope, self.run, self.sha,
                                          authorized=True, timeout=timeout)
            with self.assertRaises(ValueError):
                observe_https_headers("https://foreign.example.com/live", self.envelope,
                                      self.run, self.sha, authorized=True)
            dns.assert_not_called()

    def test_private_dns_answer_never_opens_socket(self):
        answers = [(2, 1, 6, "", ("8.8.8.8", 443)),
                   (2, 1, 6, "", ("127.0.0.1", 443))]
        with patch("madsc.https_head_probe.subprocess.run", return_value=SimpleNamespace(stdout=__import__("json").dumps([x[4][0] for x in answers]))), \
             patch("madsc.https_head_probe.socket.socket") as connect:
            with self.assertRaises(ValueError):
                observe_https_headers(self.url, self.envelope, self.run, self.sha,
                                      authorized=True)
            connect.assert_not_called()


    def test_shared_deadline_blocks_socket_after_dns(self):
        answers = [(2, 1, 6, "", ("8.8.8.8", 443))]
        with patch("madsc.https_head_probe.subprocess.run", return_value=SimpleNamespace(stdout=__import__("json").dumps([x[4][0] for x in answers]))), \
             patch("madsc.https_head_probe.time.monotonic", side_effect=[100.0, 106.0]), \
             patch("madsc.https_head_probe.socket.socket") as connect:
            with self.assertRaises(TimeoutError):
                observe_https_headers(self.url, self.envelope, self.run, self.sha,
                                      authorized=True, timeout=5)
            connect.assert_not_called()

    def test_non_ascii_path_rejected_before_socket(self):
        url = "https://video.example.com/ç.m3u8"
        envelope = pack({"candidates": [{
            "url_sha256": hashlib.sha256(url.encode()).hexdigest()
        }]}, self.run, self.sha)
        with patch("madsc.https_head_probe.subprocess.run",
                   return_value=SimpleNamespace(stdout='["8.8.8.8"]')), \
             patch("madsc.https_head_probe.socket.socket") as connect:
            with self.assertRaises(ValueError):
                observe_https_headers(url, envelope, self.run, self.sha, authorized=True)
            connect.assert_not_called()


    def test_dns_timeout_kills_resolution_before_socket(self):
        with patch("madsc.https_head_probe.subprocess.run",
                   side_effect=subprocess.TimeoutExpired("dns", 1)), \
             patch("madsc.https_head_probe.socket.socket") as connect:
            with self.assertRaises(TimeoutError):
                observe_https_headers(self.url, self.envelope, self.run, self.sha,
                                      authorized=True, timeout=1)
            connect.assert_not_called()


if __name__ == "__main__":
    unittest.main()
