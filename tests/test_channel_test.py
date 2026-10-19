import unittest
from madsc.channel_test import evaluate_probe, evaluate_repeated_probes, evaluate_ffprobe_json

class ChannelTests(unittest.TestCase):
    def test_success_is_not_device_approval(self):
        result = evaluate_probe({"url_sha256":"a"*64,"http_status":200,"video":True,
                                 "audio":True,"duration_seconds":60})
        self.assertEqual(result["technical_status"], "PRELIMINARY_PASS")
        self.assertFalse(result["ibo_device_verified"])
        self.assertFalse(result["channel_identity_verified"])
        self.assertFalse(result["stream_continuity_verified"])
        self.assertFalse(result["production_change_allowed"])
    def test_nonfinite_duration_rejected(self):
        for duration in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=str(duration)):
                probe = {"url_sha256": "a" * 64, "http_status": 200,
                         "video": True, "audio": True, "duration_seconds": duration}
                with self.assertRaises(ValueError):
                    evaluate_probe(probe)

    def test_missing_evidence_fails_closed(self):
        with self.assertRaises(ValueError):
            evaluate_probe({"http_status":200})

    def test_repeated_probe_evidence_is_not_live_claim(self):
        probe = {"url_sha256": "a" * 64, "http_status": 200,
                 "video": True, "audio": True, "duration_seconds": 40}
        result = evaluate_repeated_probes([probe, probe])
        self.assertTrue(result["stable_preliminary"])
        self.assertFalse(result["actual_network_measurements_verified"])
        self.assertFalse(result["production_change_allowed"])

    def test_repeated_probe_rejects_mixed_streams(self):
        a = {"url_sha256": "a" * 64, "http_status": 200,
             "video": True, "audio": True, "duration_seconds": 40}
        with self.assertRaises(ValueError):
            evaluate_repeated_probes([a, {**a, "url_sha256": "b" * 64}])

    def test_ffprobe_json_parser_is_conservative(self):
        payload = {"streams": [{"codec_type": "video"}, {"codec_type": "audio"}],
                   "format": {"duration": "42.5"}}
        result = evaluate_ffprobe_json(payload, "a" * 64)
        self.assertEqual(result["technical_status"], "PRELIMINARY_PASS")
        self.assertFalse(result["stream_continuity_verified"])
        self.assertFalse(result["live_probe_executed_by_this_function"])
        self.assertFalse(result["production_change_allowed"])

    def test_ffprobe_json_rejects_bad_duration(self):
        with self.assertRaises(ValueError):
            evaluate_ffprobe_json({"streams": [], "format": {"duration": "NaN"}}, "a" * 64)
