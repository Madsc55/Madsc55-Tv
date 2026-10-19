"""End-to-end read-only M3U/M3U8 -> K2 -> K3 -> K5 evidence tests."""
import json
import tempfile
import unittest
from pathlib import Path
from madsc.source_import import extract_candidates
from madsc.artifact_handoff import pack, unpack
from madsc.handoff import assess_candidates
from madsc.handoff_acceptance import verify, load

class SourcePipelineTests(unittest.TestCase):
    def test_both_source_formats_cross_job(self):
        for suffix in (".m3u", ".m3u8"):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as folder:
                source = Path(folder) / ("input" + suffix)
                source.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="sample.tv" tvg-logo="https://example.org/logo.png",Sample\nhttps://example.org/live.m3u8\n', encoding="utf-8")
                original = source.read_bytes()
                discovery = extract_candidates(source)
                envelope = pack(discovery, "123", "a" * 40)
                artifact = Path(folder) / "k2.json"
                artifact.write_text(json.dumps(envelope), encoding="utf-8")
                loaded = load(artifact)
                assessed = assess_candidates(unpack(loaded, "123", "a" * 40), {})
                self.assertEqual(assessed["candidate_count"], 1)
                self.assertEqual(assessed["assessed"][0]["technical_status"], "UNTESTED")
                self.assertFalse(assessed["production_playlist_modified"])
                report = {"schema": "madsc-handoff-verification-v1", "run_id": "123",
                          "commit_sha": "a" * 40, "source_digest": envelope["digest"],
                          "candidate_count": 1, "read_only": True, "network_probed": False,
                          "production_ready": False}
                self.assertTrue(verify(loaded, report, report, "123", "a" * 40)["k2_k3_k5_same_run_verified"])
                self.assertEqual(source.read_bytes(), original)

    def test_modified_artifact_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "input.m3u"
            source.write_text("#EXTM3U\n#EXTINF:-1,Sample\nhttps://example.org/a.m3u8\n", encoding="utf-8")
            envelope = pack(extract_candidates(source), "123", "a" * 40)
            envelope["discovery"]["candidates"] = []
            with self.assertRaises(ValueError):
                unpack(envelope, "123", "a" * 40)
