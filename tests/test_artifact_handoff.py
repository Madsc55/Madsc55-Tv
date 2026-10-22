import unittest
from madsc.discovery import classify_candidates
from madsc.artifact_handoff import pack, unpack

class ArtifactHandoffTests(unittest.TestCase):
    def setUp(self):
        self.discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/a.m3u8"}])
        self.envelope = pack(self.discovery, "123", "a" * 40)

    def test_round_trip(self):
        self.assertEqual(unpack(self.envelope, "123", "a" * 40), self.discovery)

    def test_wrong_run_rejected(self):
        with self.assertRaises(ValueError):
            unpack(self.envelope, "124", "a" * 40)

    def test_wrong_commit_rejected(self):
        with self.assertRaises(ValueError):
            unpack(self.envelope, "123", "b" * 40)

    def test_tampering_rejected(self):
        envelope = dict(self.envelope)
        envelope["discovery"] = dict(self.discovery)
        envelope["discovery"]["candidates"] = []
        with self.assertRaises(ValueError):
            unpack(envelope, "123", "a" * 40)

    def test_duplicate_fingerprint_rejected(self):
        discovery = dict(self.discovery)
        discovery["candidates"] = self.discovery["candidates"] * 2
        with self.assertRaises(ValueError):
            pack(discovery, "123", "a" * 40)

    def test_unicode_run_id_rejected(self):
        with self.assertRaises(ValueError):
            pack(self.discovery, "１２３", "a" * 40)

    def test_malformed_discovery_rejected(self):
        with self.assertRaises(ValueError):
            pack({"candidates": None}, "123", "a" * 40)

    def test_invalid_digest_type_rejected(self):
        envelope = dict(self.envelope)
        envelope["digest"] = []
        with self.assertRaises(ValueError):
            unpack(envelope, "123", "a" * 40)

    def test_oversized_candidate_and_alternative_lists_rejected(self):
        candidate = self.discovery["candidates"][0]
        for key, value in (("candidates", candidate), ("alternatives", {
                "url_sha256": "b" * 64, "alternative_to_sha256": candidate["url_sha256"]})):
            with self.subTest(key=key):
                discovery = dict(self.discovery)
                discovery[key] = [value] * 20001
                with self.assertRaisesRegex(ValueError, "Too many"):
                    pack(discovery, "123", "a" * 40)

