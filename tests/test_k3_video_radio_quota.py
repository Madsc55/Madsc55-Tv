"""Offline regression for the real-network TV pilot's selection budget."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from madsc import k3_turkish_tv_video_pilot as pilot


class K3VideoRadioQuotaTests(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()
