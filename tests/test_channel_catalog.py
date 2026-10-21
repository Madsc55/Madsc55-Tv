import unittest
from hashlib import sha256
from madsc.channel_catalog import prepare_channel_catalog


class ChannelCatalogTests(unittest.TestCase):
    def test_discovery_to_presentation_and_legacy_order(self):
        rows = [
            {"name": "izmir tv", "url": "https://example.org/1", "group_title": "Haber", "tvg_id": "a"},
            {"name": "yabancı kanal", "url": "https://example.org/2", "group_title": "Yabancı", "foreign": True},
            {"name": "tekrar", "url": "https://example.org/1", "group_title": "Haber"},
        ]
        digest = sha256(b"https://example.org/1").hexdigest()
        out = prepare_channel_catalog(
            rows,
            measurements={digest: {"verified": True, "width": 1920, "height": 1080,
                                   "technical_status": "NEEDS_REVIEW"}},
            logos={digest: {"url": "https://example.org/a.png", "identity_match": True, "reachable": True}},
            ibo_results={digest: "WORKING"})
        self.assertEqual(len(out["channels"]), 2)
        self.assertEqual(len(out["duplicates"]), 1)
        self.assertEqual(out["category_order"], ["Haber", "Yabancı"])
        self.assertEqual(out["channels"][0]["display_name"], "İZMİR TV FHD")
        self.assertEqual(out["channels"][0]["bucket"], "IBO_ONAYLI_CALISAN")
        self.assertTrue(out["channels"][0]["logo_verified"])
        self.assertFalse(out["production_writes"])

    def test_unknown_fingerprint_rejected(self):
        rows = [{"name": "A", "url": "https://example.org/a"}]
        with self.assertRaises(ValueError):
            prepare_channel_catalog(rows, measurements={"x" * 64: {"verified": True}})

    def test_no_evidence_does_not_claim_live_checks(self):
        out = prepare_channel_catalog([{"name": "A", "url": "https://example.org/a"}])
        self.assertEqual(out["channels"][0]["bucket"], "TEST_BEKLIYOR")
        self.assertFalse(out["network_probed"])
        self.assertFalse(out["device_verified_by_this_function"])


if __name__ == "__main__":
    unittest.main()
