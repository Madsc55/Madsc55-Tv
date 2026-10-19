import unittest
from madsc.candidate_coordination import coordinate
from madsc.discovery import classify_candidates

class CandidateCoordinationTests(unittest.TestCase):
    def setUp(self):
        self.rows = [{"name": "Sample", "url": "https://example.org/live.m3u8"}]
        self.digest = classify_candidates(self.rows)["candidates"][0]["url_sha256"]

    def test_missing_probe_is_held(self):
        result = coordinate(self.rows, {}, {})
        self.assertTrue(result["candidates"][0]["hold"])
        self.assertFalse(result["production_ready"])

    def test_pass_not_approved(self):
        probe = {"url_sha256": self.digest, "http_status": 200, "video": True, "audio": True, "duration_seconds": 40}
        result = coordinate(self.rows, {self.digest: probe}, {})
        self.assertTrue(result["candidates"][0]["hold"])
        self.assertEqual(result["candidates"][0]["score"], 50)
        self.assertFalse(result["candidates"][0]["production_change_allowed"])

    def test_retry_limit(self):
        probe = {"url_sha256": self.digest, "http_status": 200, "video": True, "audio": True, "duration_seconds": 40}
        result = coordinate(self.rows, {self.digest: probe}, {self.digest: 3})
        self.assertTrue(result["candidates"][0]["hold"])

    def test_mismatch_fails_closed(self):
        with self.assertRaises(ValueError):
            coordinate(self.rows, {self.digest: {"url_sha256": "a" * 64}}, {})


    def test_epg_logo_scoring_and_hold(self):
        probe = {"url_sha256": self.digest, "http_status": 200,
                 "video": True, "audio": True, "duration_seconds": 40}
        rows = [{"name": "Sample", "url": "https://example.org/live.m3u8", "tvg_id": "sample.tv"}]
        report = coordinate(rows, {self.digest: probe}, {}, {"sample.tv"}, set())
        item = report["candidates"][0]
        self.assertTrue(item["epg_match"])
        self.assertFalse(item["logo_match"])
        self.assertTrue(item["hold"])
        self.assertEqual(item["score"], 70)
        self.assertEqual(item["next_action"], "MANUAL_METADATA_REVIEW")

    def test_ibo_working_cannot_be_deleted(self):
        report = coordinate(self.rows, {}, {}, ibo_results={self.digest: "WORKING"})
        self.assertTrue(report["candidates"][0]["protected_working"])
        self.assertFalse(report["candidates"][0]["delete_allowed"])
        self.assertFalse(report["ibo_device_verified"])

    def test_full_metadata_is_not_production_approval(self):
        probe = {"url_sha256": self.digest, "http_status": 200,
                 "video": True, "audio": True, "duration_seconds": 40}
        rows = [{"name": "Sample", "url": "https://example.org/live.m3u8", "tvg_id": "sample.tv"}]
        report = coordinate(rows, {self.digest: probe}, {}, {"sample.tv"}, {"sample.tv"})
        self.assertEqual(report["candidates"][0]["score"], 80)
        self.assertTrue(report["candidates"][0]["hold"])
        self.assertFalse(report["candidates"][0]["production_change_allowed"])
        self.assertFalse(report["production_ready"])

    def test_malformed_probe_rejected(self):
        for bad in ("invalid", [], 42):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                coordinate(self.rows, {self.digest: bad}, {})

    def test_invalid_retry_counts_rejected(self):
        for bad in (-1, 1.5, True, "3"):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                coordinate(self.rows, {}, {self.digest: bad})

    def test_explicit_ibo_working_still_never_allows_writes(self):
        probe = {"url_sha256": self.digest, "http_status": 200, "video": True, "audio": True, "duration_seconds": 40}
        report = coordinate(self.rows, {self.digest: probe}, {}, ibo_results={self.digest: "WORKING"})
        self.assertFalse(report["candidates"][0]["hold"])
        self.assertFalse(report["candidates"][0]["production_change_allowed"])

    def test_unknown_ibo_keeps_full_score_candidate_held(self):
        probe = {"url_sha256": self.digest, "http_status": 200,
                 "video": True, "audio": True, "duration_seconds": 40}
        rows = [{"name": "Sample", "url": "https://example.org/live.m3u8", "tvg_id": "sample.tv"}]
        report = coordinate(rows, {self.digest: probe}, {}, {"sample.tv"}, {"sample.tv"})
        item = report["candidates"][0]
        self.assertEqual(item["score"], 80)
        self.assertTrue(item["hold"])
        self.assertTrue(item["ibo_review_required"])
        self.assertEqual(item["next_action"], "MANUAL_IBO_REVIEW")

    def test_retry_halt_overrides_metadata_and_ibo_review(self):
        report = coordinate(self.rows, {}, {self.digest: 3}, set(), set())
        self.assertTrue(report["candidates"][0]["hold"])
        self.assertEqual(report["candidates"][0]["next_action"], "HALT_AND_REPORT")

    def test_duplicate(self):
        result = coordinate(self.rows + self.rows, {}, {})
        self.assertEqual(len(result["candidates"]), 1)
        self.assertEqual(len(result["duplicates"]), 1)
    def test_ibo_working_with_failed_probe_prioritizes_preservation(self):
        failed = {"url_sha256": self.digest, "http_status": 503,
                  "video": False, "audio": False, "duration_seconds": 0}
        report = coordinate(self.rows, {self.digest: failed}, {self.digest: 3},
                            epg_ids=set(), logo_ids=set(),
                            ibo_results={self.digest: "WORKING"})
        item = report["candidates"][0]
        self.assertTrue(item["protected_working"])
        self.assertTrue(item["hold"])
        self.assertEqual(item["next_action"], "PRESERVE_IBO_WORKING_AND_REVIEW")
        self.assertFalse(item["delete_allowed"])
        self.assertFalse(item["production_change_allowed"])

    def test_normalized_tvg_id_used_for_epg_and_logo(self):
        rows = [{"name": "Sample", "url": "https://example.org/live.m3u8",
                 "tvg_id": " sample.tv "}]
        report = coordinate(rows, {}, {}, {"sample.tv"}, {"sample.tv"})
        item = report["candidates"][0]
        self.assertEqual(item["tvg_id"], "sample.tv")
        self.assertTrue(item["epg_match"])
        self.assertTrue(item["logo_match"])

    def test_unlinked_evidence_rejected(self):
        other = 'f' * 64
        for probes, attempts, ibo in (({other: {}}, {}, None), ({}, {other: 1}, None), ({}, {}, {other: 'WORKING'})):
            with self.subTest(probes=probes, attempts=attempts, ibo=ibo):
                with self.assertRaises(ValueError):
                    coordinate(self.rows, probes, attempts, ibo_results=ibo)
