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
        self.assertFalse(result["candidates"][0]["hold"])
        self.assertEqual(result["candidates"][0]["score"], 50)
        self.assertFalse(result["candidates"][0]["production_change_allowed"])

    def test_retry_limit(self):
        probe = {"url_sha256": self.digest, "http_status": 200, "video": True, "audio": True, "duration_seconds": 40}
        result = coordinate(self.rows, {self.digest: probe}, {self.digest: 3})
        self.assertTrue(result["candidates"][0]["hold"])

    def test_mismatch_fails_closed(self):
        with self.assertRaises(ValueError):
            coordinate(self.rows, {self.digest: {"url_sha256": "a" * 64}}, {})

    def test_duplicate(self):
        result = coordinate(self.rows + self.rows, {}, {})
        self.assertEqual(len(result["candidates"]), 1)
        self.assertEqual(len(result["duplicates"]), 1)
