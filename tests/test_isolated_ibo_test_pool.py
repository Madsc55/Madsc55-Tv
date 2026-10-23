import unittest
from madsc.isolated_ibo_test_pool import build_isolated_test_pool

class TestK5Pool(unittest.TestCase):
    def setUp(self):
        self.records = [{"position": i, "source_sha256": f"{i:064x}"} for i in range(1, 6116)]

    def test_complete(self):
        pool = build_isolated_test_pool(self.records)
        self.assertEqual(sum(pool["counts"].values()), 6115)
        self.assertFalse(pool["production_writes"])

    def test_shift_rejected(self):
        self.records[0]["position"] = 2
        with self.assertRaises(ValueError):
            build_isolated_test_pool(self.records)

    def test_unverified_failure(self):
        self.records[0]["playback"] = "broken"
        self.assertEqual(build_isolated_test_pool(self.records)["entries"][0]["playback"], "unknown")

    def test_evidenced_failure(self):
        self.records[0].update(playback="broken", history=[{"status": "broken", "evidence_id": "old-1"}])
        self.assertEqual(build_isolated_test_pool(self.records)["entries"][0]["bucket"], "broken")

    def test_logo_validation(self):
        self.records[0]["logo_sha256"] = "bad"
        with self.assertRaises(ValueError):
            build_isolated_test_pool(self.records)

    def test_url_not_exported(self):
        self.records[0]["url"] = "https://private.example/token"
        with self.assertRaises(ValueError):
            build_isolated_test_pool(self.records)

    def test_evidence_url_rejected(self):
        self.records[0]["history"] = [{"status": "broken", "evidence_id": "https://private.example"}]
        with self.assertRaises(ValueError):
            build_isolated_test_pool(self.records)

    def test_single_backslash_evidence_rejected(self):
        self.records[0]["history"] = [{"status": "broken", "evidence_id": r"legacy\test"}]
        with self.assertRaises(ValueError):
            build_isolated_test_pool(self.records)
