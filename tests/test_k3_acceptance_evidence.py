"""Offline acceptance evidence tests."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from madsc.k3_acceptance_evidence import assess


class K3EvidenceTests(unittest.TestCase):
    def test_three_stages_and_six_hours_required(self):
        with TemporaryDirectory() as folder:
            files = []
            for hour in (0, 6, 12):
                rows = [{"url_sha256": format(i, "064x"), "hls_manifest_seen": True,
                         "https_reachable": True, "status": "manifest_only"}
                        for i in range(75)]
                report = {"stage": "K3_REAL_NETWORK_MANIFEST_PILOT",
                          "measured_at_utc": f"2026-10-23T{hour:02d}:00:00+00:00",
                          "candidate_limit": 75, "candidate_shortfall": 0,
                          "production_playlist_modified": False,
                          "probed": 75, "manifest_seen": 75, "results": rows}
                file = Path(folder) / f"{hour}.json"
                file.write_text(json.dumps(report), encoding="utf-8")
                files.append(file)
            result = assess(files)
            self.assertTrue(result["manifest_acceptance"])
            self.assertFalse(result["full_k3_acceptance"])
            self.assertEqual(result["elapsed_seconds"], 43200)
            self.assertEqual(result["adjacent_interval_seconds"], [21600, 21600])
            with self.assertRaises(ValueError):
                assess([files[0], files[0], files[2]])
            data = json.loads(files[2].read_text())
            data["candidate_shortfall"] = 1
            files[2].write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                assess(files)

    def test_contradictory_success_is_rejected(self):
        with TemporaryDirectory() as folder:
            files = []
            for hour in (0, 6, 12):
                rows = [{"url_sha256": format(i, "064x"), "hls_manifest_seen": True,
                         "https_reachable": True, "status": "manifest_only"}
                        for i in range(75)]
                if hour == 12:
                    rows[0]["https_reachable"] = False
                report = {"stage": "K3_REAL_NETWORK_MANIFEST_PILOT",
                          "measured_at_utc": f"2026-10-23T{hour:02d}:00:00+00:00",
                          "candidate_limit": 75, "candidate_shortfall": 0,
                          "production_playlist_modified": False,
                          "probed": 75, "manifest_seen": 75, "results": rows}
                file = Path(folder) / f"{hour}.json"
                file.write_text(json.dumps(report), encoding="utf-8")
                files.append(file)
            with self.assertRaisesRegex(ValueError, "Inconsistent successful"):
                assess(files)

    def test_short_middle_interval_does_not_pass(self):
        with TemporaryDirectory() as folder:
            files = []
            for hour in (0, 1, 12):
                rows = [{"url_sha256": format(i, "064x"), "hls_manifest_seen": True,
                         "https_reachable": True, "status": "manifest_only"} for i in range(75)]
                report = {"stage": "K3_REAL_NETWORK_MANIFEST_PILOT",
                          "measured_at_utc": f"2026-10-23T{hour:02d}:00:00+00:00",
                          "candidate_limit": 75, "candidate_shortfall": 0,
                          "production_playlist_modified": False, "probed": 75,
                          "manifest_seen": 75, "results": rows}
                path = Path(folder) / f"{hour}.json"
                path.write_text(json.dumps(report), encoding="utf-8")
                files.append(path)
            result = assess(files)
            self.assertFalse(result["minimum_six_hours_met"])
            self.assertFalse(result["manifest_acceptance"])
            self.assertEqual(result["adjacent_interval_seconds"], [3600, 39600])
