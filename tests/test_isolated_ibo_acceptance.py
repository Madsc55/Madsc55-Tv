"""Offline acceptance gate must never claim production readiness."""
import hashlib
import unittest

from madsc.isolated_ibo_archive_preview import build_6115_archive_preview
from madsc.isolated_ibo_test_pool import build_isolated_test_pool
from madsc.isolated_ibo_acceptance import assess_k5_acceptance


class TestK5Acceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.urls = [f"https://example.invalid/channel/{i}" for i in range(1, 6116)]
        cls.records = [{"position": i, "source_sha256": hashlib.sha256(cls.urls[i - 1].encode("utf-8")).hexdigest()}
                       for i in range(1, 6116)]
        cls.archive = build_6115_archive_preview(cls.urls)
        cls.pool = build_isolated_test_pool(cls.records)

    def test_integrity_is_not_release_authorization(self):
        report = assess_k5_acceptance(self.urls, self.archive, self.records, self.pool)
        self.assertTrue(report["archive_integrity_verified"])
        self.assertTrue(report["pool_integrity_verified"])
        self.assertFalse(report["production_ready"])
        self.assertFalse(report["production_writes"])
        self.assertIn("external_source_provenance_not_verified", report["blockers"])

    def test_tampered_archive_fails_closed(self):
        archive = dict(self.archive)
        archive["archive_count"] += 1
        with self.assertRaises(ValueError):
            assess_k5_acceptance(self.urls, archive, self.records, self.pool)

    def test_tampered_pool_fails_closed(self):
        pool = dict(self.pool)
        pool["device_verified"] = True
        with self.assertRaises(ValueError):
            assess_k5_acceptance(self.urls, self.archive, self.records, pool)

    def test_unrelated_source_hashes_rejected(self):
        records = [dict(record) for record in self.records]
        records[0]["source_sha256"] = "0" * 64
        unrelated_pool = build_isolated_test_pool(records)
        with self.assertRaises(ValueError):
            assess_k5_acceptance(self.urls, self.archive, records, unrelated_pool)
