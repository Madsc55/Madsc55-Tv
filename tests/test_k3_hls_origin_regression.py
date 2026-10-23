"""Offline K3 HLS origin security regressions (no network calls)."""
import unittest
from madsc.k3_turkish_tv_video_pilot import same_origin_https


class K3HlsOriginRegressionTests(unittest.TestCase):
    def test_valid_same_origin_relative_resolution(self):
        self.assertTrue(same_origin_https(
            "https://media.example.org/master.m3u8",
            "https://media.example.org/segment.ts"))

    def test_fragment_and_whitespace_rejected(self):
        parent = "https://media.example.org/master.m3u8"
        for child in (
            "https://media.example.org/segment.ts#fragment",
            "https://media.example.org/segment.ts ",
            "https://media.example.org/seg ment.ts",
            "https://media.example.org/seg\tment.ts",
        ):
            with self.subTest(child=child):
                self.assertFalse(same_origin_https(parent, child))

    def test_cross_host_credentials_and_ports_rejected(self):
        parent = "https://media.example.org/master.m3u8"
        for child in (
            "https://elsewhere.example.org/segment.ts",
            "http://media.example.org/segment.ts",
            "https://user:pass@media.example.org/segment.ts",
            "https://media.example.org:444/segment.ts",
        ):
            with self.subTest(child=child):
                self.assertFalse(same_origin_https(parent, child))
