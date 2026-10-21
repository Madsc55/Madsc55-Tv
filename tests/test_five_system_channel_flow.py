import unittest
from hashlib import sha256

from madsc.five_system_channel_flow import build_offline_channel_previews


class FiveSystemChannelFlowTests(unittest.TestCase):
    def test_combined_flow_keeps_ibo_and_legacy_category(self):
        rows = [{"name": "izmir tv", "url": "https://example.org/live",
                 "tvg_id": "izmir.tv", "group_title": "Haber"}]
        digest = sha256(b"https://example.org/live").hexdigest()
        result = build_offline_channel_previews(
            rows, ibo_results={digest: "WORKING"},
            probes={digest: {"url_sha256": digest, "http_status": 503,
                             "video": False, "audio": False, "duration_seconds": 0}},
            measurements={digest: {"verified": True, "width": 1920, "height": 1080}},
            logos={digest: {"url": "https://example.org/logo.png",
                            "identity_match": True, "reachable": True}})
        self.assertEqual(result["automation_count"], 5)
        self.assertEqual(result["catalog"]["channels"][0]["technical_status"], "NEEDS_REVIEW")
        self.assertEqual(result["catalog"]["channels"][0]["bucket"], "IBO_ONAYLI_CALISAN")
        playlist = result["previews"]["IBO_ONAYLI_CALISAN"]
        self.assertIn("İZMİR TV FHD", playlist)
        self.assertIn('group-title="Haber"', playlist)
        self.assertIn('tvg-logo="https://example.org/logo.png"', playlist)
        self.assertEqual(result["counts"]["IBO_ONAYLI_CALISAN"], 1)
        self.assertFalse(result["production_writes"])
        self.assertFalse(result["k4_backup_invoked"])
        self.assertFalse(result["ibo_device_test_executed"])

    def test_no_evidence_stays_untested(self):
        result = build_offline_channel_previews(
            [{"name": "kanal", "url": "https://example.org/stream"}])
        self.assertEqual(result["counts"]["TEST_BEKLIYOR"], 1)
        self.assertFalse(result["network_probed"])
        self.assertFalse(result["production_ready"])

    def test_three_stage_evidence_is_attached_but_not_production_approval(self):
        rows = [{"name": "kanal", "url": "https://example.org/stream"}]
        digest = sha256(b"https://example.org/stream").hexdigest()
        sample = {"url_sha256": digest, "http_status": 200,
                  "video": True, "audio": True, "duration_seconds": 31}
        staged = [{"captured_at": stamp, "probe": dict(sample)} for stamp in (
            "2026-10-20T00:00:00Z", "2026-10-20T06:00:00Z",
            "2026-10-20T12:00:00Z")]
        out = build_offline_channel_previews(rows, three_stage={digest: staged})
        channel = out["catalog"]["channels"][0]
        self.assertTrue(channel["three_stage_preliminary_pass"])
        self.assertEqual(channel["bucket"], "TEST_BEKLIYOR")
        self.assertFalse(out["production_ready"])
        self.assertFalse(out["network_probed"])

    def test_mismatched_three_stage_channel_is_rejected(self):
        rows = [{"name": "kanal", "url": "https://example.org/stream"}]
        digest = sha256(b"https://example.org/stream").hexdigest()
        sample = {"url_sha256": "a" * 64, "http_status": 200,
                  "video": True, "audio": True, "duration_seconds": 31}
        staged = [{"captured_at": stamp, "probe": dict(sample)} for stamp in (
            "2026-10-20T00:00:00Z", "2026-10-20T06:00:00Z",
            "2026-10-20T12:00:00Z")]
        with self.assertRaises(ValueError):
            build_offline_channel_previews(rows, three_stage={digest: staged})

    def test_bad_probe_rejected_before_any_preview(self):
        rows = [{"name": "kanal", "url": "https://example.org/stream"}]
        with self.assertRaises(ValueError):
            build_offline_channel_previews(rows, probes={"0" * 64: {}})


if __name__ == "__main__":
    unittest.main()
