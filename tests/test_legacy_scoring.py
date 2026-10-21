import unittest
from madsc.legacy_scoring import legacy_technical_score, legacy_approval_decision


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

    def test_unified_approval_status_and_score_cap(self):
        stable = legacy_approval_decision(80, "VIDEO_SES_VAR", True)
        self.assertEqual(stable["score"], 100)
        self.assertEqual(stable["status"], "IBO_VE_KIMLIK_ONAYI_BEKLIYOR")
        self.assertEqual(stable["add_to_main_playlist"], "HAYIR")
        self.assertFalse(stable["production_change_allowed"])
        self.assertEqual(legacy_approval_decision(35, "VIDEO_SES_VAR", False)["status"], "KARARLILIK_BEKLIYOR")
        self.assertEqual(legacy_approval_decision(20, "YALNIZ_VIDEO", True)["status"], "TEKNIK_DOGRULAMA_BEKLIYOR")

    def test_unified_approval_rejects_untrusted_evidence(self):
        for bad in (-1, True, "40", None):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                legacy_approval_decision(bad, "VIDEO_SES_VAR", True)
        with self.assertRaises(ValueError):
            legacy_approval_decision(20, "VIDEO_SES_VAR", "EVET")
