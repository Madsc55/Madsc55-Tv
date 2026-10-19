import unittest
from hashlib import sha256
from madsc.discovery import classify_candidates
from madsc.handoff import assess_candidates

class HandoffTests(unittest.TestCase):
    def test_unprobed_candidate_is_untested(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        result = assess_candidates(discovery, {})
        self.assertEqual(result["assessed"][0]["technical_status"], "UNTESTED")
        self.assertFalse(result["assessed"][0]["ibo_device_verified"])
        self.assertFalse(result["assessed"][0]["ibo_result_supplied"])
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
        self.assertFalse(entry["ibo_device_verified"])
        self.assertTrue(entry["ibo_result_supplied"])
        self.assertFalse(entry["delete_allowed"])
        self.assertFalse(entry["production_change_allowed"])
    def test_invalid_handoff_shapes_fail_closed(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        for invalid in (None, [], "bad"):
            with self.subTest(probes=invalid), self.assertRaises(ValueError):
                assess_candidates(discovery, invalid)
            if invalid is not None:
                with self.subTest(ibo=invalid), self.assertRaises(ValueError):
                    assess_candidates(discovery, {}, invalid)
        for invalid in (None, [], {"candidates": None}, {"candidates": [None]}):
            with self.subTest(discovery=invalid), self.assertRaises(ValueError):
                assess_candidates(invalid, {})

    def test_invalid_fingerprint_length_fails_closed(self):
        with self.assertRaises(ValueError):
            assess_candidates({"candidates": [{"url_sha256": "bad"}]}, {})

    def test_nonhex_fingerprint_fails_closed(self):
        for invalid in ("z" * 64, "G" * 64, " " * 64):
            with self.subTest(value=invalid), self.assertRaises(ValueError):
                assess_candidates({"candidates": [{"url_sha256": invalid}]}, {})

    def test_invalid_probe_record_fails_closed(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        digest = discovery["candidates"][0]["url_sha256"]
        with self.assertRaises(ValueError):
            assess_candidates(discovery, {digest: []})

    def test_invalid_ibo_evidence_fails_closed(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        digest = discovery["candidates"][0]["url_sha256"]
        with self.assertRaises(ValueError):
            assess_candidates(discovery, {}, {digest: "ASSUMED_WORKING"})
    def test_tvg_id_survives_handoff_and_ibo_working_is_protected(self):
        discovery = classify_candidates([{"name": "TRT", "url": "https://example.org/live", "tvg_id": "trt.tv"}])
        digest = discovery["candidates"][0]["url_sha256"]
        result = assess_candidates(discovery, {}, {digest: "WORKING"})
        item = result["assessed"][0]
        self.assertEqual(item["tvg_id"], "trt.tv")
        self.assertTrue(item["protected_working"])
        self.assertFalse(item["delete_allowed"])

    def test_duplicate_fingerprints_and_bad_metadata_fail_closed(self):
        discovery = classify_candidates([{"name": "TRT", "url": "https://example.org/live"}])
        item = discovery["candidates"][0]
        with self.assertRaises(ValueError):
            assess_candidates({"candidates": [item, item]}, {})
        with self.assertRaises(ValueError):
            assess_candidates({"candidates": [{**item, "tvg_id": []}]}, {})
