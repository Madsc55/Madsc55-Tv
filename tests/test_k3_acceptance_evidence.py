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
            for hour in (0, 3, 6):
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
            middle = json.loads(files[1].read_text(encoding="utf-8"))
            middle["results"][0]["https_reachable"] = False
            files[1].write_text(json.dumps(middle), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Inconsistent successful"):
                assess(files)

    def test_manifest_only_cannot_claim_decoded_audio_video(self):
        with TemporaryDirectory() as folder:
            paths = []
            for hour in (0, 6, 12):
                rows = [{"url_sha256": format(i, "064x"), "hls_manifest_seen": True,
                         "https_reachable": True, "status": "manifest_only",
                         "audio_video_verified": False} for i in range(75)]
                report = {"stage": "K3_REAL_NETWORK_MANIFEST_PILOT",
                          "measured_at_utc": f"2026-10-23T{hour:02d}:00:00+00:00",
                          "candidate_limit": 75, "candidate_shortfall": 0,
                          "production_playlist_modified": False, "probed": 75,
                          "manifest_seen": 75, "audio_video_verified": 0,
                          "results": rows}
                path = Path(folder) / f"{hour}.json"
                path.write_text(json.dumps(report), encoding="utf-8")
                paths.append(path)
            self.assertTrue(assess(paths)["manifest_acceptance"])
            for scope in ("report", "row"):
                altered = json.loads(paths[1].read_text(encoding="utf-8"))
                if scope == "report":
                    altered["audio_video_verified"] = 1
                else:
                    altered["results"][0]["audio_video_verified"] = True
                paths[1].write_text(json.dumps(altered), encoding="utf-8")
                with self.subTest(scope=scope), self.assertRaisesRegex(ValueError, "audio/video"):
                    assess(paths)
                altered["audio_video_verified"] = 0
                altered["results"][0]["audio_video_verified"] = False
                paths[1].write_text(json.dumps(altered), encoding="utf-8")

    def test_malformed_row_and_counter_fail_closed(self):
        with TemporaryDirectory() as folder:
            paths = []
            for hour in (0, 6, 12):
                rows = [{"url_sha256": format(i, "064x"), "hls_manifest_seen": True,
                         "https_reachable": True, "status": "manifest_only"} for i in range(75)]
                report = {"stage": "K3_REAL_NETWORK_MANIFEST_PILOT",
                          "measured_at_utc": f"2026-10-23T{hour:02d}:00:00+00:00",
                          "candidate_limit": 75, "candidate_shortfall": 0,
                          "production_playlist_modified": False, "probed": 75,
                          "manifest_seen": 75, "results": rows}
                path = Path(folder) / f"{hour}.json"
                path.write_text(json.dumps(report), encoding="utf-8")
                paths.append(path)
            original = json.loads(paths[1].read_text(encoding="utf-8"))
            for mutation in ("null_row", "string_row", "boolean_counter"):
                altered = json.loads(json.dumps(original))
                if mutation == "null_row":
                    altered["results"][0] = None
                elif mutation == "string_row":
                    altered["results"][0] = "bad"
                else:
                    altered["audio_video_verified"] = False
                paths[1].write_text(json.dumps(altered), encoding="utf-8")
                with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                    assess(paths)

    def test_invalid_snapshot_timestamp_and_shape_rejected(self):
        with TemporaryDirectory() as folder:
            paths = []
            for hour in (0, 6, 12):
                rows = [{"url_sha256": format(i, "064x"), "hls_manifest_seen": True,
                         "https_reachable": True, "status": "manifest_only"} for i in range(75)]
                report = {"stage": "K3_REAL_NETWORK_MANIFEST_PILOT",
                          "measured_at_utc": f"2026-10-23T{hour:02d}:00:00+00:00",
                          "candidate_limit": 75, "candidate_shortfall": 0,
                          "production_playlist_modified": False, "probed": 75,
                          "manifest_seen": 75, "results": rows}
                path = Path(folder) / f"{hour}.json"
                path.write_text(json.dumps(report), encoding="utf-8")
                paths.append(path)
            original = json.loads(paths[1].read_text(encoding="utf-8"))
            for bad in (None, [], {"measured_at_utc": None},
                        {**original, "measured_at_utc": "not-a-date"}):
                paths[1].write_text(json.dumps(bad), encoding="utf-8")
                with self.subTest(bad=repr(bad)[:40]), self.assertRaises(ValueError):
                    assess(paths)

    def test_manifest_count_and_observation_types_fail_closed(self):
        with TemporaryDirectory() as folder:
            paths = []
            for hour in (0, 6, 12):
                rows = [{"url_sha256": format(i, "064x"), "hls_manifest_seen": True,
                         "https_reachable": True, "status": "manifest_only"} for i in range(75)]
                report = {"stage": "K3_REAL_NETWORK_MANIFEST_PILOT",
                          "measured_at_utc": f"2026-10-23T{hour:02d}:00:00+00:00",
                          "candidate_limit": 75, "candidate_shortfall": 0,
                          "production_playlist_modified": False, "probed": 75,
                          "manifest_seen": 75, "results": rows}
                path = Path(folder) / f"{hour}.json"
                path.write_text(json.dumps(report), encoding="utf-8")
                paths.append(path)
            original = json.loads(paths[1].read_text(encoding="utf-8"))
            for field, value in (("manifest_seen", 75.0), ("manifest_seen", True),
                                 ("hls_manifest_seen", 1), ("hls_manifest_seen", "true")):
                altered = json.loads(json.dumps(original))
                if field == "hls_manifest_seen":
                    altered["results"][0][field] = value
                else:
                    altered[field] = value
                paths[1].write_text(json.dumps(altered), encoding="utf-8")
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    assess(paths)

    def test_candidate_accounting_rejects_float_and_boolean_aliases(self):
        with TemporaryDirectory() as folder:
            paths = []
            for hour in (0, 6, 12):
                rows = [{"url_sha256": format(i, "064x"), "hls_manifest_seen": True,
                         "https_reachable": True, "status": "manifest_only"} for i in range(75)]
                report = {"stage": "K3_REAL_NETWORK_MANIFEST_PILOT",
                          "measured_at_utc": f"2026-10-23T{hour:02d}:00:00+00:00",
                          "candidate_limit": 75, "candidate_shortfall": 0,
                          "production_playlist_modified": False, "probed": 75,
                          "manifest_seen": 75, "results": rows}
                path = Path(folder) / f"{hour}.json"
                path.write_text(json.dumps(report), encoding="utf-8")
                paths.append(path)
            original = json.loads(paths[1].read_text(encoding="utf-8"))
            for field, value in (("candidate_limit", 75.0),
                                 ("candidate_shortfall", False),
                                 ("probed", 75.0)):
                altered = {**original, field: value}
                paths[1].write_text(json.dumps(altered), encoding="utf-8")
                with self.subTest(field=field), self.assertRaisesRegex(ValueError, "75-candidate"):
                    assess(paths)

    def test_unverified_row_cannot_claim_https_success(self):
        with TemporaryDirectory() as folder:
            paths = []
            for hour in (0, 6, 12):
                rows = [{"url_sha256": format(i, "064x"), "hls_manifest_seen": True,
                         "https_reachable": True, "status": "manifest_only"} for i in range(75)]
                report = {"stage": "K3_REAL_NETWORK_MANIFEST_PILOT",
                          "measured_at_utc": f"2026-10-23T{hour:02d}:00:00+00:00",
                          "candidate_limit": 75, "candidate_shortfall": 0,
                          "production_playlist_modified": False, "probed": 75,
                          "manifest_seen": 75, "results": rows}
                path = Path(folder) / f"{hour}.json"
                path.write_text(json.dumps(report), encoding="utf-8")
                paths.append(path)
            middle = json.loads(paths[1].read_text(encoding="utf-8"))
            middle["results"][0].pop("hls_manifest_seen")
            middle["results"][0]["status"] = "blocked_or_unreachable"
            middle["manifest_seen"] = 74
            paths[1].write_text(json.dumps(middle), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "HTTPS observation"):
                assess(paths)

    def test_non_utc_snapshot_timestamp_rejected(self):
        with TemporaryDirectory() as folder:
            paths = []
            for hour in (0, 6, 12):
                rows = [{"url_sha256": format(i, "064x"), "hls_manifest_seen": True,
                         "https_reachable": True, "status": "manifest_only"} for i in range(75)]
                report = {"stage": "K3_REAL_NETWORK_MANIFEST_PILOT",
                          "measured_at_utc": f"2026-10-23T{hour:02d}:00:00+00:00",
                          "candidate_limit": 75, "candidate_shortfall": 0,
                          "production_playlist_modified": False, "probed": 75,
                          "manifest_seen": 75, "results": rows}
                path = Path(folder) / f"{hour}.json"
                path.write_text(json.dumps(report), encoding="utf-8")
                paths.append(path)
            middle = json.loads(paths[1].read_text(encoding="utf-8"))
            middle["measured_at_utc"] = "2026-10-23T08:00:00+02:00"
            paths[1].write_text(json.dumps(middle), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "UTC snapshot"):
                assess(paths)

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
