import unittest
from madsc.channel_test import evaluate_probe

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
