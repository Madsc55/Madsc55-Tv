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


    def test_invalid_alternative_container_rejected(self):
        for alternatives in (None, 5, "not-a-list", {"url_sha256": "a" * 64}):
            with self.subTest(alternatives=alternatives):
                discovery = dict(self.discovery)
                discovery["alternatives"] = alternatives
                with self.assertRaisesRegex(ValueError, "Invalid alternative evidence"):
                    pack(discovery, "123", "a" * 40)


    def test_non_json_discovery_metadata_rejected(self):
        for value in (float("nan"), float("inf"), {1, 2}):
            with self.subTest(value=repr(value)):
                discovery = dict(self.discovery)
                discovery["unexpected_metadata"] = value
                with self.assertRaisesRegex(ValueError, "Invalid JSON discovery evidence"):
                    pack(discovery, "123", "a" * 40)

    def test_oversized_serialized_discovery_rejected(self):
        discovery = dict(self.discovery)
        discovery["unexpected_metadata"] = "x" * (16 * 1024 * 1024)
        with self.assertRaisesRegex(ValueError, "Oversized discovery evidence"):
            pack(discovery, "123", "a" * 40)


    def test_noncanonical_evidence_digests_rejected(self):
        for digest in (self.envelope["digest"].upper(),
                       self.envelope["digest"][:-1],
                       self.envelope["digest"] + "0",
                       "g" * 64, None, 123):
            with self.subTest(digest=repr(digest)):
                envelope = dict(self.envelope)
                envelope["digest"] = digest
                with self.assertRaisesRegex(ValueError, "Evidence digest mismatch"):
                    unpack(envelope, "123", "a" * 40)


    def test_run_id_length_bound(self):
        self.assertEqual(pack(self.discovery, "9" * 20, "a" * 40)["run_id"], "9" * 20)
        for run_id in ("", "9" * 21, "1" * 10000):
            with self.subTest(length=len(run_id)), self.assertRaisesRegex(ValueError, "Invalid run id"):
                pack(self.discovery, run_id, "a" * 40)

