"""K5 independent test-pool verification regression cases."""
import copy
import unittest

from madsc.isolated_ibo_test_pool import build_isolated_test_pool
from madsc.isolated_ibo_test_pool_verify import verify_isolated_test_pool


class TestK5PoolVerifier(unittest.TestCase):
    def setUp(self):
        self.records = [{"position": i, "source_sha256": f"{i:064x}"}
                        for i in range(1, 6116)]
        self.pool = build_isolated_test_pool(self.records)

    def test_valid_pool(self):
        report = verify_isolated_test_pool(self.records, self.pool)
        self.assertTrue(report["verified"])
        self.assertFalse(report["playback_verified"])

    def test_changed_position_rejected(self):
        altered = copy.deepcopy(self.pool)
        altered["entries"][0]["position"] = 2
        with self.assertRaises(ValueError):
            verify_isolated_test_pool(self.records, altered)

    def test_changed_logo_rejected(self):
        altered = copy.deepcopy(self.pool)
        altered["entries"][0]["logo_sha256"] = "a" * 64
        with self.assertRaises(ValueError):
            verify_isolated_test_pool(self.records, altered)

    def test_changed_count_rejected(self):
        altered = copy.deepcopy(self.pool)
        altered["counts"]["pending"] += 1
        with self.assertRaises(ValueError):
            verify_isolated_test_pool(self.records, altered)

    def test_reordered_sources_rejected(self):
        records = copy.deepcopy(self.records)
        records[0], records[1] = records[1], records[0]
        with self.assertRaises(ValueError):
            verify_isolated_test_pool(records, self.pool)

    def test_false_verification_claim_rejected(self):
        altered = copy.deepcopy(self.pool)
        altered["device_verified"] = True
        with self.assertRaises(ValueError):
            verify_isolated_test_pool(self.records, altered)
