"""Offline regression for the real-network TV pilot's selection budget."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from madsc import k3_turkish_tv_video_pilot as pilot


class K3VideoRadioQuotaTests(unittest.TestCase):
    def test_nested_urls_reject_scheme_downgrade_and_origin_bypass(self):
        base = "https://example.org/master.m3u8"
        for target in ("http://example.org/segment.ts",
                       "https://example.org:8443/segment.ts",
                       "https://user:pass@example.org/segment.ts",
                       "https://evil.example.org/segment.ts"):
            with self.subTest(target=target):
                self.assertFalse(pilot.same_origin_https(base, target))
        self.assertTrue(pilot.same_origin_https(base, "https://example.org/segment.ts"))

    def test_http_segment_rejected_without_download(self):
        manifest = b"#EXTM3U\n#EXTINF:4,\nhttp://example.org/segment.ts\n"
        with patch.object(pilot, "safe_curl", return_value=manifest) as curl:
            self.assertEqual(pilot.verify_av("https://example.org/live.m3u8"),
                             (False, False, "cross_host_segment"))
            curl.assert_called_once()

    def test_unsupported_hls_layouts_fail_before_segment_fetch(self):
        for tag in ("#EXT-X-MAP:URI=\"init.mp4\"", "#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=100"):
            manifest = ("#EXTM3U\n" + tag + "\n#EXTINF:4,\nsegment.ts\n").encode()
            with self.subTest(tag=tag), patch.object(pilot, "safe_curl", return_value=manifest) as curl:
                self.assertEqual(pilot.verify_av("https://example.org/live.m3u8"),
                                 (False, False, "unsupported_hls_media_layout"))
                curl.assert_called_once()

    def test_master_tag_inside_comment_does_not_trigger_variant_fetch(self):
        manifest = b"#EXTM3U\n# comment #EXT-X-STREAM-INF fake\n#EXTINF:4,\nsegment.ts\n"
        with patch.object(pilot, "safe_curl", side_effect=[manifest, b"x" * 188]) as curl, \
             patch.object(pilot.subprocess, "run") as probe:
            probe.return_value.returncode = 1
            probe.return_value.stdout = b""
            self.assertEqual(pilot.verify_av("https://example.org/live.m3u8"),
                             (False, False, "probe_error"))
            self.assertEqual(curl.call_count, 2)

    def test_byte_range_and_low_latency_parts_are_not_misprobed(self):
        for tag in ("#EXT-X-BYTERANGE:1024@0", "#EXT-X-DISCONTINUITY",
                    "#EXT-X-GAP", "#EXT-X-SKIP:SKIPPED-SEGMENTS=2",
                    "#EXT-X-RENDITION-REPORT:URI=\"other.m3u8\"",
                    "#EXT-X-PART:DURATION=0.5,URI=\"part.ts\"",
                    "#EXT-X-PRELOAD-HINT:TYPE=PART,URI=\"next.ts\""):
            manifest = ("#EXTM3U\n" + tag + "\n#EXTINF:4,\nsegment.ts\n").encode()
            with self.subTest(tag=tag), patch.object(pilot, "safe_curl", return_value=manifest) as curl:
                self.assertEqual(pilot.verify_av("https://example.org/live.m3u8"),
                                 (False, False, "unsupported_hls_segment_layout"))
                curl.assert_called_once()

    def test_indented_comment_is_not_used_as_segment_url(self):
        manifest = b"#EXTM3U\n   #EXTINF:4,\n   # comment\nsegment.ts\n"
        with patch.object(pilot, "safe_curl", side_effect=[manifest, b"x" * 188]) as curl, \
             patch.object(pilot.subprocess, "run") as probe:
            probe.return_value.returncode = 1
            probe.return_value.stdout = b""
            self.assertEqual(pilot.verify_av("https://example.org/live.m3u8"),
                             (False, False, "probe_error"))
            self.assertEqual(curl.call_args_list[1].args[0],
                             "https://example.org/segment.ts")

    def test_encrypted_media_playlist_fails_before_segment_download(self):
        manifest = b'#EXTM3U\n#EXT-X-KEY:METHOD=AES-128,URI="key.bin"\n#EXTINF:4,\nsegment.ts\n'
        with patch.object(pilot, 'safe_curl', return_value=manifest) as curl:
            self.assertEqual(pilot.verify_av('https://example.org/live.m3u8'),
                             (False, False, 'encrypted_hls_unsupported'))
            curl.assert_called_once()

    def test_nested_master_fails_before_variant_download(self):
        master = b'#EXTM3U\n#EXT-X-STREAM-INF:BANDWIDTH=100\nchild.m3u8\n'
        with patch.object(pilot, 'safe_curl', side_effect=[master, master]) as curl:
            self.assertEqual(pilot.verify_av('https://example.org/live.m3u8'),
                             (False, False, 'nested_master_manifest'))
            self.assertEqual(curl.call_count, 2)

    def test_nested_variant_must_be_an_hls_manifest(self):
        master = b'#EXTM3U\n#EXT-X-STREAM-INF:BANDWIDTH=500000\nchild.m3u8\n'
        with patch.object(pilot, "safe_curl", side_effect=[master, b"not an HLS playlist"]) as curl:
            self.assertEqual(pilot.verify_av("https://example.org/master.m3u8"),
                             (False, False, "invalid_variant_manifest"))
        self.assertEqual(curl.call_count, 2)

    def test_malformed_ffprobe_streams_fail_closed(self):
        manifest = b'#EXTM3U\n#EXTINF:4,\nsegment.ts\n'
        with patch.object(pilot, "safe_curl", side_effect=[manifest, b"x" * 188]), \
             patch.object(pilot.subprocess, "run") as probe:
            probe.return_value.stdout = b'{"streams": [null]}'
            self.assertEqual(pilot.verify_av("https://example.org/media.m3u8"),
                             (False, False, "probe_error"))

    def test_ffprobe_nonzero_exit_cannot_verify_video(self):
        manifest = b'#EXTM3U\n#EXTINF:4,\nsegment.ts\n'
        with patch.object(pilot, "safe_curl", side_effect=[manifest, b"x" * 188]), \
             patch.object(pilot.subprocess, "run") as probe:
            probe.return_value.returncode = 1
            probe.return_value.stdout = b'{"streams": [{"codec_type": "video"}, {"codec_type": "audio"}]}'
            self.assertEqual(pilot.verify_av("https://example.org/media.m3u8"),
                             (False, False, "probe_error"))

    def test_radio_does_not_consume_tv_probe_quota(self):
        rows = [("Radyo Haber", "https://example.org/radio.m3u8")]
        rows += [(f"TV {i}", f"https://example.org/tv{i}.m3u8") for i in range(pilot.LIMIT + 2)]
        with tempfile.TemporaryDirectory() as d:
            with patch.object(pilot, "candidates", return_value=iter(rows)), \
                 patch.object(pilot, "verify_video", return_value=(False, "no_manifest")) as verify, \
                 patch.object(pilot, "write_fixture_report") as write, \
                 patch.object(pilot.Path, "cwd", return_value=Path(d)):
                pilot.run()
        self.assertEqual(verify.call_count, pilot.LIMIT)
        report = json.loads(write.call_args.args[2])
        self.assertEqual(report["tested"], pilot.LIMIT)
        self.assertEqual(report["radio_excluded"], 1)
        self.assertEqual(len(report["results"]), pilot.LIMIT + 1)
        self.assertFalse(report["playlist_modified"])


    def test_radio_only_source_scan_is_bounded(self):
        rows = [("Radyo FM", f"https://example.org/r{i}.m3u8") for i in range(pilot.MAX_SOURCE_ROWS + 10)]
        with tempfile.TemporaryDirectory() as d:
            with patch.object(pilot, "candidates", return_value=iter(rows)), \
                 patch.object(pilot, "verify_video") as verify, \
                 patch.object(pilot, "write_fixture_report") as write, \
                 patch.object(pilot.Path, "cwd", return_value=Path(d)):
                pilot.run()
        verify.assert_not_called()
        report = json.loads(write.call_args.args[2])
        self.assertEqual(report["tested"], 0)
        self.assertEqual(report["source_rows_scanned"], pilot.MAX_SOURCE_ROWS)
        self.assertEqual(report["radio_excluded"], pilot.MAX_SOURCE_ROWS)
        self.assertEqual(len(report["results"]), pilot.MAX_SOURCE_ROWS)


    def test_duplicate_tv_urls_do_not_consume_probe_quota(self):
        rows = [("TV duplicate", "https://example.org/first.m3u8")] * 3
        rows += [(f"TV {i}", f"https://example.org/tv{i}.m3u8") for i in range(pilot.LIMIT + 2)]
        with tempfile.TemporaryDirectory() as d:
            with patch.object(pilot, "candidates", return_value=iter(rows)), \
                 patch.object(pilot, "verify_video", return_value=(False, "no_manifest")) as verify, \
                 patch.object(pilot, "write_fixture_report") as write, \
                 patch.object(pilot.Path, "cwd", return_value=Path(d)):
                pilot.run()
        self.assertEqual(verify.call_count, pilot.LIMIT)
        report = json.loads(write.call_args.args[2])
        self.assertEqual(report["tested"], pilot.LIMIT)
        self.assertEqual(report["reason_counts"]["duplicate_excluded"], 2)
        self.assertFalse(report["playlist_modified"])


    def test_source_generator_is_not_consumed_beyond_limit(self):
        consumed = []
        def rows():
            for i in range(pilot.MAX_SOURCE_ROWS + 5):
                consumed.append(i)
                yield ("Radyo FM", f"https://example.org/r{i}.m3u8")
        with tempfile.TemporaryDirectory() as d:
            with patch.object(pilot, "candidates", side_effect=rows), \
                 patch.object(pilot, "verify_video") as verify, \
                 patch.object(pilot, "write_fixture_report"), \
                 patch.object(pilot.Path, "cwd", return_value=Path(d)):
                pilot.run()
        verify.assert_not_called()
        self.assertEqual(len(consumed), pilot.MAX_SOURCE_ROWS)

if __name__ == "__main__":
    unittest.main()
