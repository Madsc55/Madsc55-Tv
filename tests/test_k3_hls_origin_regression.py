"""Offline K3 HLS origin security regressions (no network calls)."""
import unittest
from unittest.mock import patch
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

    def test_raw_hls_segment_reference_is_rejected_before_download(self):
        from madsc.k3_turkish_tv_video_pilot import verify_av
        manifest = b'#EXTM3U\\n#EXTINF:6,\\n segment.ts\\n'
        with patch("madsc.k3_turkish_tv_video_pilot.safe_curl", return_value=manifest) as fetch:
            self.assertEqual(verify_av("https://media.example.org/live.m3u8"),
                             (False, False, "unsafe_segment_reference"))
            self.assertEqual(fetch.call_count, 1)

    def test_raw_hls_variant_reference_is_rejected_before_download(self):
        from madsc.k3_turkish_tv_video_pilot import verify_av
        manifest = b'#EXTM3U\\n#EXT-X-STREAM-INF:BANDWIDTH=500000\\nvariant.m3u8#bad\\n'
        with patch("madsc.k3_turkish_tv_video_pilot.safe_curl", return_value=manifest) as fetch:
            self.assertEqual(verify_av("https://media.example.org/live.m3u8"),
                             (False, False, "unsafe_variant_reference"))
            self.assertEqual(fetch.call_count, 1)
