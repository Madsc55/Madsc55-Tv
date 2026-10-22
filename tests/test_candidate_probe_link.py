import hashlib
import unittest

from madsc.artifact_handoff import pack
from madsc.candidate_probe_link import link_candidate_probes


class CandidateProbeLinkTests(unittest.TestCase):
    def test_matching_candidate_probe_and_unprobed_count(self):
        url = "https://example.org/test.m3u8"
        digest = hashlib.sha256(url.encode()).hexdigest()
        run, sha = "12345", "a" * 40
        discovery = {"candidates": [{"url_sha256": digest, "name": "Fixture",
                                     "tvg_id": "fixture.tv"}]}
        envelope = pack(discovery, run, sha)
        records = [{"url_sha256": digest, "ffprobe": {
            "streams": [{"codec_type": "video"}, {"codec_type": "audio"}],
            "format": {"duration": "40"}}}]
        linked = link_candidate_probes(envelope, records, run, sha)
        self.assertEqual(linked["source_digest"], envelope["digest"])
        self.assertEqual(linked["probed_candidates"], 1)
        self.assertEqual(linked["untested_candidates"], 0)
        self.assertFalse(linked["network_probed"])
        self.assertFalse(linked["production_ready"])

    def test_foreign_probe_and_wrong_run_rejected(self):
        digest = "a" * 64
        run, sha = "12345", "b" * 40
        envelope = pack({"candidates": [{"url_sha256": digest}]}, run, sha)
        records = [{"url_sha256": "c" * 64, "ffprobe": {
            "streams": [{"codec_type": "video"}], "format": {"duration": "40"}}}]
        with self.assertRaises(ValueError):
            link_candidate_probes(envelope, records, run, sha)
        with self.assertRaises(ValueError):
            link_candidate_probes(envelope, [], "54321", sha)
        empty = link_candidate_probes(envelope, [], run, sha)
        self.assertEqual(empty["untested_candidates"], 1)
        self.assertEqual(empty["preliminary_passes"], 0)

    def test_duplicate_candidate_fingerprint_rejected(self):
        digest = "a" * 64
        envelope = pack({"candidates": [{"url_sha256": digest}, {"url_sha256": digest}]}, "1", "b" * 40)
        with self.assertRaisesRegex(ValueError, "Duplicate K2 candidate"):
            link_candidate_probes(envelope, [], "1", "b" * 40)

    def test_duplicate_probe_records_rejected(self):
        digest = "a" * 64
        envelope = pack({"candidates": [{"url_sha256": digest}]}, "1", "b" * 40)
        record = {"url_sha256": digest, "ffprobe": {"streams": [{"codec_type": "video"}], "format": {"duration": "40"}}}
        with self.assertRaisesRegex(ValueError, "Duplicate channel evidence"):
            link_candidate_probes(envelope, [record, record], "1", "b" * 40)

    def test_malformed_probe_fingerprint_rejected(self):
        digest = "a" * 64
        envelope = pack({"candidates": [{"url_sha256": digest}]}, "1", "b" * 40)
        record = {"url_sha256": "A" * 64, "ffprobe": {"streams": [], "format": {"duration": "40"}}}
        with self.assertRaises(ValueError):
            link_candidate_probes(envelope, [record], "1", "b" * 40)


if __name__ == "__main__":
    unittest.main()
