import unittest
from madsc.legacy_scoring import legacy_technical_score


class LegacyScoringTests(unittest.TestCase):
    def test_full_technical_evidence_matches_legacy_points(self):
        report = legacy_technical_score("VIDEO_SES_VAR", "", "1920x1080", "https://example.org/logo.png")
        self.assertEqual(report["score"], 50)
        self.assertEqual(report["status"], "TEKNIK_ADAY")
        self.assertFalse(report["production_change_allowed"])
        self.assertFalse(report["ibo_device_verified"])

    def test_video_only_and_resolution_thresholds(self):
        self.assertEqual(legacy_technical_score("YALNIZ_VIDEO", "", "1280x720")["score"], 27)
        self.assertEqual(legacy_technical_score("YALNIZ_VIDEO", "true", "640x360")["score"], 38)
        self.assertEqual(legacy_technical_score("BAD", "", "invalid", "http://example.org/logo")["score"], 0)

    def test_legacy_score_is_not_new_coordination_score(self):
        self.assertEqual(legacy_technical_score("VIDEO_SES_VAR")["score"], 35)
        self.assertTrue(legacy_technical_score("VIDEO_SES_VAR")["legacy_scoring_contract_only"])

    def test_invalid_evidence_fails_closed(self):
        for bad in (None, 42, [], {}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                legacy_technical_score(technical=bad)
