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

    def test_unicode_probe_error_does_not_abort_remaining_channels(self):
        rows = [("TV Broken", "https://example.org/broken.m3u8"),
                ("TV Working", "https://example.org/working.m3u8")]
        with tempfile.TemporaryDirectory() as d:
            with patch.object(pilot, "candidates", return_value=iter(rows)), \
                 patch.object(pilot, "verify_video", side_effect=[UnicodeError("bad encoding"), (True, "video_detected")]) as verify, \
                 patch.object(pilot, "write_fixture_report") as write, \
                 patch.object(pilot.Path, "cwd", return_value=Path(d)):
                pilot.run()
        report = json.loads(write.call_args.args[2])
        self.assertEqual(report["tested"], 2)
        self.assertEqual(report["video_verified"], 1)
        self.assertEqual(report["reason_counts"]["blocked_or_unreachable"], 1)
        self.assertEqual(verify.call_count, 2)

    def test_nonbyte_manifest_fails_closed(self):
        with patch.object(pilot, "safe_curl", return_value="#EXTM3U") as curl:
            self.assertEqual(pilot.verify_av("https://example.org/live.m3u8"),
                             (False, False, "no_manifest"))
            curl.assert_called_once()

    def test_oversized_manifest_rejected_even_when_fetch_is_mocked(self):
        manifest = b"#EXTM3U\n" + b"#" * 65536
        with patch.object(pilot, "safe_curl", return_value=manifest) as curl:
            self.assertEqual(pilot.verify_av("https://example.org/live.m3u8"),
                             (False, False, "no_manifest"))
            curl.assert_called_once()

    def test_nonbyte_segment_rejected_before_ffprobe(self):
        manifest = b"#EXTM3U\n#EXTINF:4,\nsegment.ts\n"
        with patch.object(pilot, "safe_curl", side_effect=[manifest, "not bytes"]) as curl, \
             patch.object(pilot.subprocess, "run") as probe:
            self.assertEqual(pilot.verify_av("https://example.org/live.m3u8"),
                             (False, False, "segment_unreachable"))
            self.assertEqual(curl.call_count, 2)
            probe.assert_not_called()

    def test_oversized_segment_rejected_before_ffprobe(self):
        manifest = b"#EXTM3U\n#EXTINF:4,\nsegment.ts\n"
        with patch.object(pilot, "safe_curl", side_effect=[manifest, b"x" * (pilot.MAX_SEGMENT + 1)]) as curl, \
             patch.object(pilot.subprocess, "run") as probe:
            self.assertEqual(pilot.verify_av("https://example.org/live.m3u8"),
                             (False, False, "segment_unreachable"))
            self.assertEqual(curl.call_count, 2)
            probe.assert_not_called()

    def test_malformed_nested_url_is_rejected_without_exception(self):
        self.assertFalse(pilot.same_origin_https("https://example.org/master.m3u8",
                                                  "https://[broken/segment.ts"))
        self.assertFalse(pilot.same_origin_https("https://[broken/master.m3u8",
                                                  "https://example.org/segment.ts"))

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

    def test_alternate_audio_rendition_is_not_claimed_as_verified(self):
        manifest = (b'#EXTM3U\n#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio",'
                    b'NAME="Turkish",URI="audio.m3u8"\n#EXTINF:4,\nsegment.ts\n')
        with patch.object(pilot, "safe_curl", return_value=manifest) as curl:
            self.assertEqual(pilot.verify_av("https://example.org/live.m3u8"),
                             (False, False, "alternate_media_unsupported"))
            curl.assert_called_once()

    def test_external_session_metadata_is_not_silently_ignored(self):
        manifest = (b'#EXTM3U\n#EXT-X-SESSION-DATA:DATA-ID="example",'
                    b'URI="metadata.json"\n#EXTINF:4,\nsegment.ts\n')
        with patch.object(pilot, "safe_curl", return_value=manifest) as curl:
            self.assertEqual(pilot.verify_av("https://example.org/live.m3u8"),
                             (False, False, "alternate_media_unsupported"))
            curl.assert_called_once()

    def test_indented_vod_type_is_not_counted_as_live_tv(self):
        manifest = b"#EXTM3U\n  #EXT-X-PLAYLIST-TYPE:VOD\n#EXTINF:4,\nsegment.ts\n"
        with patch.object(pilot, "safe_curl", return_value=manifest) as curl:
            self.assertEqual(pilot.verify_av("https://example.org/live.m3u8"),
                             (False, False, "vod_playlist_not_live"))
            curl.assert_called_once()

    def test_explicit_vod_type_is_not_counted_as_live_tv(self):
        manifest = b"#EXTM3U\n#EXT-X-PLAYLIST-TYPE:VOD\n#EXTINF:4,\nsegment.ts\n"
        with patch.object(pilot, "safe_curl", return_value=manifest) as curl:
            self.assertEqual(pilot.verify_av("https://example.org/live.m3u8"),
                             (False, False, "vod_playlist_not_live"))
            curl.assert_called_once()

    def test_manifest_without_segment_duration_cannot_verify_tv(self):
        manifest = b"#EXTM3U\nsegment.ts\n"
        with patch.object(pilot, "safe_curl", return_value=manifest) as curl:
            self.assertEqual(pilot.verify_av("https://example.org/live.m3u8"),
                             (False, False, "no_segment_duration"))
            curl.assert_called_once()

    def test_vod_endlist_is_not_counted_as_live_tv(self):
        manifest = b"#EXTM3U\n#EXTINF:4,\nsegment.ts\n#EXT-X-ENDLIST\n"
        with patch.object(pilot, "safe_curl", return_value=manifest) as curl:
            self.assertEqual(pilot.verify_av("https://example.org/live.m3u8"),
                             (False, False, "vod_playlist_not_live"))
            curl.assert_called_once()

    def test_encrypted_media_playlist_fails_before_segment_download(self):
        manifest = b'#EXTM3U\n#EXT-X-KEY:METHOD=AES-128,URI="key.bin"\n#EXTINF:4,\nsegment.ts\n'
        with patch.object(pilot, 'safe_curl', return_value=manifest) as curl:
            self.assertEqual(pilot.verify_av('https://example.org/live.m3u8'),
                             (False, False, 'encrypted_hls_unsupported'))
            curl.assert_called_once()

    def test_master_alternate_audio_is_rejected_before_variant_download(self):
        for tag in ('#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="a",URI="audio.m3u8"',
                    '#EXT-X-SESSION-DATA:DATA-ID="x",URI="metadata.json"',
                    '#EXT-X-SESSION-KEY:METHOD=AES-128,URI="key.bin"'):
            master = ("#EXTM3U\n" + tag +
                      "\n#EXT-X-STREAM-INF:BANDWIDTH=500000\nvideo.m3u8\n").encode()
            with self.subTest(tag=tag), patch.object(pilot, "safe_curl", return_value=master) as curl:
                self.assertEqual(pilot.verify_av("https://example.org/master.m3u8"),
                                 (False, False, "unsupported_master_metadata"))
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

    def test_report_distinguishes_video_with_audio_from_video_only(self):
        rows = [("TV Audio", "https://example.org/av.m3u8"),
                ("TV Silent", "https://example.org/video.m3u8")]
        with tempfile.TemporaryDirectory() as d:
            with patch.object(pilot, "candidates", return_value=iter(rows)), \
                 patch.object(pilot, "verify_video",
                              side_effect=[(True, "video_audio_detected"),
                                           (True, "video_detected")]), \
                 patch.object(pilot, "write_fixture_report") as write, \
                 patch.object(pilot.Path, "cwd", return_value=Path(d)):
                pilot.run()
        report = json.loads(write.call_args.args[2])
        self.assertEqual(report["video_verified"], 2)
        self.assertEqual(report["video_audio_verified"], 1)
        self.assertEqual(report["video_only_detected"], 1)
        self.assertEqual(report["live_continuity_hours_verified"], 0)
        self.assertFalse(report["device_playback_verified"])
        self.assertFalse(report["acceptance_75_channels_met"])
        self.assertFalse(report["language_confirmed_by_audio"])

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


    def test_nonstring_channel_name_does_not_abort_pilot(self):
        rows = [(None, "https://example.org/unnamed.m3u8"),
                ("   ", "https://example.org/blank.m3u8"),
                ("TV Valid", "https://example.org/live.m3u8")]
        with tempfile.TemporaryDirectory() as d:
            with patch.object(pilot, "candidates", return_value=iter(rows)), \
                 patch.object(pilot, "verify_video", return_value=(False, "no_manifest")) as verify, \
                 patch.object(pilot, "write_fixture_report") as write, \
                 patch.object(pilot.Path, "cwd", return_value=Path(d)):
                pilot.run()
        report = json.loads(write.call_args.args[2])
        self.assertEqual(report["tested"], 1)
        self.assertEqual(report["radio_excluded"], 2)
        verify.assert_called_once_with("https://example.org/live.m3u8")

    def test_invalid_source_url_does_not_abort_tv_pilot(self):
        rows = [("TV Missing", None), ("TV Numeric", 17),
                ("TV Invalid Unicode", "https://example.org/" + chr(0xD800)),
                ("TV Oversized", "https://example.org/" + "x" * 4096),
                ("TV Blank", "   "),
                ("TV Valid", "https://example.org/live.m3u8")]
        with tempfile.TemporaryDirectory() as d:
            with patch.object(pilot, "candidates", return_value=iter(rows)), \
                 patch.object(pilot, "verify_video", return_value=(False, "no_manifest")) as verify, \
                 patch.object(pilot, "write_fixture_report") as write, \
                 patch.object(pilot.Path, "cwd", return_value=Path(d)):
                pilot.run()
        report = json.loads(write.call_args.args[2])
        self.assertEqual(report["tested"], 1)
        self.assertEqual(report["reason_counts"]["invalid_source_url"], 5)
        verify.assert_called_once_with("https://example.org/live.m3u8")

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
