import unittest

from madsc.k2_daily_evidence import build_daily_evidence, verify_daily_evidence


class K2DailyEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.row = {"name": "Example", "source_kind": "official_broadcaster",
                    "source_page": "https://example.org/watch",
                    "stream_url": "https://example.org/live.m3u8"}
        self.kw = {"day": "2026-10-24", "source_commit": "a" * 40}

    def test_deterministic_artifact_and_fail_closed_claims(self):
        first = build_daily_evidence([self.row], **self.kw)
        second = build_daily_evidence([self.row], **self.kw)
        self.assertEqual(first, second)
        self.assertTrue(verify_daily_evidence(first))
        self.assertFalse(first["license_verified"])
        self.assertFalse(first["production_ready"])
        self.assertFalse(first["network_probed"])

    def test_daily_delta(self):
        first = build_daily_evidence([self.row], **self.kw)
        later = build_daily_evidence([], previous_fingerprints=first["candidate_fingerprints"], **self.kw)
        self.assertEqual(later["added"], [])
        self.assertEqual(later["missing_from_today"], first["candidate_fingerprints"])
        self.assertTrue(verify_daily_evidence(later))

    def test_tampering_is_detected(self):
        artifact = build_daily_evidence([self.row], **self.kw)
        artifact["report"]["production_ready"] = True
        self.assertFalse(verify_daily_evidence(artifact))

    def test_bad_provenance_inputs_rejected(self):
        for day in ("2026-02-30", "tomorrow", "2026-1-1"):
            with self.subTest(day=day), self.assertRaises(ValueError):
                build_daily_evidence([], day=day, source_commit="a" * 40)
        with self.assertRaises(ValueError):
            build_daily_evidence([], day="2026-10-24", source_commit="unknown")
        with self.assertRaises(ValueError):
            build_daily_evidence([], previous_fingerprints=["not-a-hash"], **self.kw)
