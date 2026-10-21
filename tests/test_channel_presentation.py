import unittest
from madsc.channel_presentation import present_channel, quality_label


class ChannelPresentationTests(unittest.TestCase):
    def test_measured_resolution_and_original_category(self):
        row = {"name": "İstanbul tv", "group_title": "Yerel", "tvg_id": "istanbul.tv"}
        out = present_channel(row, measurement={"verified": True, "width": 1920, "height": 1080,
                                                 "technical_status": "PRELIMINARY_PASS"})
        self.assertEqual(out["display_name"], "İSTANBUL TV FHD")
        self.assertEqual(out["group_title"], "Yerel")
        self.assertEqual(out["bucket"], "CALISAN_ADAY")
        self.assertFalse(out["production_change_allowed"])

    def test_unmeasured_quality_is_not_invented(self):
        out = present_channel({"name": "KANAL"}, measurement={"width": 3840, "height": 2160})
        self.assertEqual(out["display_name"], "KANAL")
        self.assertIsNone(out["quality"])

    def test_logo_requires_verified_identity_and_reachability(self):
        row = {"name": "Test"}
        self.assertIsNone(present_channel(row, logo_evidence={"url": "https://example.org/logo.png",
                         "identity_match": True})["logo_url"])
        good = present_channel(row, logo_evidence={"url": "https://example.org/logo.png",
                               "identity_match": True, "reachable": True})
        self.assertTrue(good["logo_verified"])

    def test_ibo_working_overrides_failed_probe_without_mutation(self):
        out = present_channel({"name": "Test", "foreign": True},
                              measurement={"technical_status": "NEEDS_REVIEW"}, ibo_result="WORKING")
        self.assertEqual(out["bucket"], "IBO_ONAYLI_CALISAN")
        self.assertTrue(out["preserve_existing"])
        self.assertFalse(out["production_writes"])

    def test_foreign_and_failed_are_separate(self):
        self.assertEqual(present_channel({"name": "X", "foreign": True})["bucket"], "YABANCI")
        self.assertEqual(present_channel({"name": "X"},
                         measurement={"technical_status": "NEEDS_REVIEW"})["bucket"], "CALISMAYAN_ADAY")

    def test_invalid_measurement_and_status(self):
        self.assertIsNone(quality_label("1920", 1080))
        with self.assertRaises(ValueError):
            present_channel({"name": "X"}, ibo_result="CONFIRMED_BY_NETWORK")


if __name__ == "__main__":
    unittest.main()
