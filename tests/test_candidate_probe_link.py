import hashlib
import unittest

from madsc.artifact_handoff import pack
from madsc.candidate_probe_link import link_candidate_probes, link_candidate_continuity


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
        with self.assertRaisesRegex(ValueError, "Duplicate candidate fingerprint"):
            pack({"candidates": [{"url_sha256": digest}, {"url_sha256": digest}]},
                 "1", "b" * 40)

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


    def test_continuity_link_pass_and_missing(self):
        run, sha = "123", "b" * 40
        a, b = "a" * 64, "c" * 64
        envelope = pack({"candidates": [{"url_sha256": a}, {"url_sha256": b}]}, run, sha)
        base = {"url_sha256": a, "http_status": 200, "video": True,
                "audio": True, "duration_seconds": 40}
        samples = [{**base, "observed_at": t} for t in (
            "2026-10-21T10:00:00Z", "2026-10-21T16:00:00Z",
            "2026-10-21T22:00:00Z")]
        result = link_candidate_continuity(envelope, {a: samples}, run, sha)
        self.assertEqual(result["preliminary_window_passes"], 1)
        self.assertEqual(result["missing_count"], 1)
        self.assertFalse(result["production_ready"])
        self.assertFalse(result["actual_network_measurements_verified"])

    def test_continuity_link_rejects_foreign_and_wrong_run(self):
        run, sha = "123", "b" * 40
        envelope = pack({"candidates": [{"url_sha256": "a" * 64}]}, run, sha)
        with self.assertRaises(ValueError):
            link_candidate_continuity(envelope, {"c" * 64: []}, run, sha)
        with self.assertRaises(ValueError):
            link_candidate_continuity(envelope, {}, "124", sha)


    def test_cli_exposes_mutually_exclusive_offline_evidence_modes(self):
        from pathlib import Path
        source = Path("madsc/candidate_probe_link.py").read_text(encoding="utf-8")
        self.assertIn("add_mutually_exclusive_group(required=True)", source)
        self.assertIn('evidence_group.add_argument("--probes", type=Path)', source)
        self.assertIn('evidence_group.add_argument("--continuity", type=Path)', source)
        self.assertIn("link_candidate_continuity(candidates, load_evidence(args.continuity)", source)

    def test_cli_uses_descriptor_relative_no_follow_path_walk(self):
        from pathlib import Path
        source = Path("madsc/candidate_probe_link.py").read_text(encoding="utf-8")
        self.assertIn('os.open not in os.supports_dir_fd', source)
        self.assertIn('os.O_DIRECTORY | os.O_NOFOLLOW', source)
        self.assertIn('dir_fd=descriptor', source)
        self.assertIn('os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK', source)
        self.assertIn('os.fstat(handle.fileno())', source)
        self.assertIn('stat.S_ISREG(opened.st_mode)', source)
        self.assertIn('handle.read(16 * 1024 * 1024 + 1)', source)

    def test_continuity_link_rejects_duplicate_candidates(self):
        run, sha = "123", "b" * 40
        with self.assertRaisesRegex(ValueError, "Duplicate candidate fingerprint"):
            pack({"candidates": [{"url_sha256": "a" * 64},
                                 {"url_sha256": "a" * 64}]}, run, sha)


    def test_continuity_rejects_clustered_samples_despite_long_total_window(self):
        run, sha, digest = "123", "b" * 40, "a" * 64
        envelope = pack({"candidates": [{"url_sha256": digest}]}, run, sha)
        base = {"url_sha256": digest, "http_status": 200, "video": True,
                "audio": True, "duration_seconds": 40}
        samples = [{**base, "observed_at": timestamp} for timestamp in (
            "2026-10-20T00:00:00Z", "2026-10-20T00:01:00Z",
            "2026-10-20T12:00:00Z")]
        result = link_candidate_continuity(envelope, {digest: samples}, run, sha)
        self.assertEqual(result["preliminary_window_passes"], 0)
        self.assertEqual(result["results"][digest]["status"], "NEEDS_REVIEW")
        self.assertFalse(result["production_change_allowed"])


    def test_continuity_rejects_tampered_envelope(self):
        run, sha, digest = "123", "b" * 40, "a" * 64
        envelope = pack({"candidates": [{"url_sha256": digest}]}, run, sha)
        forged = {**envelope, "digest": "0" * 64}
        with self.assertRaisesRegex(ValueError, "Evidence digest mismatch"):
            link_candidate_continuity(forged, {}, run, sha)
        with self.assertRaises(ValueError):
            link_candidate_continuity(envelope, {}, run, "c" * 40)

    def test_continuity_rejects_mismatched_sample_fingerprint(self):
        run, sha, digest = "123", "b" * 40, "a" * 64
        envelope = pack({"candidates": [{"url_sha256": digest}]}, run, sha)
        base = {"url_sha256": "c" * 64, "http_status": 200,
                "video": True, "audio": True, "duration_seconds": 40}
        samples = [{**base, "observed_at": stamp} for stamp in (
            "2026-10-21T10:00:00Z", "2026-10-21T16:00:00Z",
            "2026-10-21T22:00:00Z")]
        with self.assertRaisesRegex(ValueError, "Continuity fingerprint mismatch"):
            link_candidate_continuity(envelope, {digest: samples}, run, sha)

    def test_invalid_k2_candidate_fingerprints_fail_closed(self):
        run, sha = "123", "b" * 40
        for candidate in ({"url_sha256": "A" * 64}, {"url_sha256": "a" * 63},
                          {"url_sha256": None}, {"url_sha256": ["a" * 64]}, {}):
            with self.subTest(candidate=candidate):
                with self.assertRaises(ValueError):
                    pack({"candidates": [candidate]}, run, sha)

    def test_invalid_k2_candidate_container_rejected(self):
        run, sha = "123", "b" * 40
        for candidates in (None, {}, "invalid"):
            with self.subTest(candidates=candidates):
                with self.assertRaises(ValueError):
                    pack({"candidates": candidates}, run, sha)


    def test_k3_loader_module_compiles_and_imports(self):
        import ast
        from pathlib import Path
        source = Path("madsc/candidate_probe_link.py").read_text(encoding="utf-8")
        parsed = ast.parse(source, filename="madsc/candidate_probe_link.py")
        self.assertTrue(any(isinstance(node, ast.FunctionDef)
                            and node.name == "load_evidence" for node in parsed))
        from madsc.candidate_probe_link import load_evidence
        self.assertTrue(callable(load_evidence))

    def test_evidence_loader_accepts_regular_json_and_rejects_duplicates(self):
        import tempfile
        from pathlib import Path
        from madsc.candidate_probe_link import load_evidence
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.json"
            path.write_text('{"ok": true}', encoding="utf-8")
            self.assertEqual(load_evidence(path), {"ok": True})
            path.write_text('{"ok": true, "ok": false}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_evidence(path)

    def test_evidence_loader_rejects_symlink_and_oversize(self):
        import tempfile
        from pathlib import Path
        from madsc.candidate_probe_link import load_evidence
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "evidence.json"
            target.write_text("{}", encoding="utf-8")
            alias = root / "alias.json"
            alias.symlink_to(target)
            with self.assertRaises(ValueError):
                load_evidence(alias)
            target.write_bytes(b"x" * (16 * 1024 * 1024 + 1))
            with self.assertRaises(ValueError):
                load_evidence(target)


    def test_evidence_loader_rejects_malformed_json_and_utf8(self):
        import tempfile
        from pathlib import Path
        from madsc.candidate_probe_link import load_evidence
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            for payload in (b'{"broken":', bytes([255])):
                with self.subTest(payload=payload):
                    path.write_bytes(payload)
                    with self.assertRaises((ValueError, UnicodeError)):
                        load_evidence(path)

    def test_evidence_loader_fails_closed_without_no_follow(self):
        import os
        import tempfile
        from pathlib import Path
        from unittest.mock import patch
        from madsc.candidate_probe_link import load_evidence
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.json"
            path.write_text("{}", encoding="utf-8")
            with patch.object(os, "O_NOFOLLOW", None, create=True):
                with self.assertRaisesRegex(ValueError, "Secure evidence opening is unavailable"):
                    load_evidence(path)

    def test_evidence_loader_rejects_fifo_without_waiting_for_writer(self):
        import os
        import tempfile
        from pathlib import Path
        from madsc.candidate_probe_link import load_evidence
        if not hasattr(os, "mkfifo"):
            self.skipTest("FIFO unsupported on this platform")
        with tempfile.TemporaryDirectory() as directory:
            fifo = Path(directory) / "evidence.pipe"
            os.mkfifo(fifo)
            with self.assertRaises(ValueError):
                load_evidence(fifo)

    def test_evidence_loader_rejects_symlink_parent(self):
        import tempfile
        from pathlib import Path
        from madsc.candidate_probe_link import load_evidence
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "real"
            folder.mkdir()
            (folder / "evidence.json").write_text("{}", encoding="utf-8")
            alias = root / "alias"
            alias.symlink_to(folder, target_is_directory=True)
            with self.assertRaises(ValueError):
                load_evidence(alias / "evidence.json")


if __name__ == "__main__":
    unittest.main()
