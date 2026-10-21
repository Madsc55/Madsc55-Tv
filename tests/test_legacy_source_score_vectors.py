"""Source-derived score vectors from old scripts/akilli_aday_puanla.py.

These assert the legacy *scoring contract*, not 92-workflow parity.
No network access, playlist writes, or automatic approvals.
"""
import unittest
from madsc.legacy_scoring import legacy_technical_score, legacy_approval_decision


class LegacySourceScoreVectors(unittest.TestCase):
    def test_source_derived_score_matrix(self):
        # Old source: video=20, sound=15, resolution=3/7/10, HTTPS logo=5.
        vectors = [
            ("VIDEO_SES_VAR", "", "", "", 35, "TEKNIK_ADAY"),
            ("VIDEO_SES_VAR", "", "1920x1080", "https://example.org/logo.png", 50, "TEKNIK_ADAY"),
            ("YALNIZ_VIDEO", "", "1280x720", "", 27, "EK_DOGRULAMA_GEREKLI"),
            ("YALNIZ_VIDEO", "true", "640x360", "", 38, "TEKNIK_ADAY"),
            ("YALNIZ_VIDEO", "TRUE", "bad", "https://example.org/logo", 40, "TEKNIK_ADAY"),
            ("YALNIZ_VIDEO", "false", "640x480", "http://example.org/logo", 23, "EK_DOGRULAMA_GEREKLI"),
            ("BAD", "true", "1920x1080", "https://example.org/logo", 15, "EK_DOGRULAMA_GEREKLI"),
            ("VIDEO_SES_VAR", "", "1920x1079", "", 42, "TEKNIK_ADAY"),
            ("VIDEO_SES_VAR", "", "1920x720", "", 42, "TEKNIK_ADAY"),
            ("VIDEO_SES_VAR", "", "1920x719", "", 38, "TEKNIK_ADAY"),
        ]
        for technical, audio, resolution, logo, points, status in vectors:
            with self.subTest(technical=technical, audio=audio, resolution=resolution, logo=logo):
                result = legacy_technical_score(technical, audio, resolution, logo)
                self.assertEqual(result["score"], points)
                self.assertEqual(result["status"], status)
                self.assertFalse(result["identity_verified"])
                self.assertFalse(result["ibo_device_verified"])
                self.assertFalse(result["production_change_allowed"])
                self.assertTrue(result["legacy_scoring_contract_only"])

    def test_approval_never_grants_playlist_write(self):
        for score in (0, 35, 80, 100):
            for technical in ("VIDEO_SES_VAR", "YALNIZ_VIDEO", "BAD"):
                for stable in (False, True):
                    with self.subTest(score=score, technical=technical, stable=stable):
                        result = legacy_approval_decision(score, technical, stable)
                        self.assertEqual(result["add_to_main_playlist"], "HAYIR")
                        self.assertEqual(result["ibo_approval"], "YOK")
                        self.assertEqual(result["user_approval"], "YOK")
                        self.assertFalse(result["production_change_allowed"])
                        self.assertLessEqual(result["score"], 100)

    def test_source_contract_rejects_untrusted_types(self):
        for invalid in (None, [], {}, 4, True):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    legacy_technical_score(technical=invalid)
