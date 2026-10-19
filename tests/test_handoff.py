import unittest
from hashlib import sha256
from madsc.discovery import classify_candidates
from madsc.handoff import assess_candidates

class HandoffTests(unittest.TestCase):
    def test_unprobed_candidate_is_untested(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        result = assess_candidates(discovery, {})
        self.assertEqual(result["assessed"][0]["technical_status"], "UNTESTED")
        self.assertFalse(result["production_playlist_modified"])
    def test_valid_probe_is_not_production_approval(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        digest = discovery["candidates"][0]["url_sha256"]
        result = assess_candidates(discovery, {digest: {"url_sha256": digest, "http_status": 200,
                                   "video": True, "audio": True, "duration_seconds": 40}})
        self.assertEqual(result["assessed"][0]["technical_status"], "PRELIMINARY_PASS")
        self.assertFalse(result["assessed"][0]["production_change_allowed"])
    def test_mismatched_probe_rejected(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        digest = discovery["candidates"][0]["url_sha256"]
        with self.assertRaises(ValueError):
            assess_candidates(discovery, {digest: {"url_sha256": "a" * 64, "http_status": 200,
                                "video": True, "audio": True, "duration_seconds": 40}})

    def test_ibo_working_remains_protected_after_failed_probe(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        digest = discovery["candidates"][0]["url_sha256"]
        failed = {"url_sha256": digest, "http_status": 503, "video": False,
                  "audio": False, "duration_seconds": 0}
        result = assess_candidates(discovery, {digest: failed}, {digest: "WORKING"})
        entry = result["assessed"][0]
        self.assertEqual(entry["technical_status"], "NEEDS_REVIEW")
        self.assertEqual(entry["ibo_result"], "WORKING")
        self.assertTrue(entry["protected_working"])
        self.assertFalse(entry["delete_allowed"])
        self.assertFalse(entry["production_change_allowed"])
    def test_invalid_ibo_evidence_fails_closed(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        digest = discovery["candidates"][0]["url_sha256"]
        with self.assertRaises(ValueError):
            assess_candidates(discovery, {}, {digest: "ASSUMED_WORKING"})
