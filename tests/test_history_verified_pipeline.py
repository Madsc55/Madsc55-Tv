"""Orchestrator rejects unverified sources without emitting a handoff."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from madsc.history_verified_pipeline import produce_verified_history

A = "a" * 40
B = "b" * 40
FILES = {"gecmis.json": b'{"history":{}}',
         "ana_liste_test_gecmisi.json": b'{"channels":{}}'}


class VerifiedHistoryPipelineTests(unittest.TestCase):
    def test_verified_source_creates_read_only_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({
                "schema": 1, "mode": "VERIFIED_SOURCE",
                "source_run_id": "123", "source_commit_sha": A,
                "production_writes": False,
                "hashes": {n: hashlib.sha256(v).hexdigest() for n, v in FILES.items()}}))
            output = root / "handoff.json"
            def verify(*args, **kwargs):
                return {"artifact_id": 456, "source_run_id": "123",
                        "source_commit_sha": A}
            def download(*, destination, **kwargs):
                destination.mkdir()
                for name, value in FILES.items():
                    (destination / name).write_bytes(value)
            result = produce_verified_history(
                manifest, output, current_sha=B, run_id="789", token="test-token",
                verify_origin=verify, download=download)
            self.assertFalse(result["production_ready"])
            self.assertEqual(json.loads(output.read_text())["run_id"], "789")

    def test_missing_token_or_rejected_github_record_fails_without_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({
                "schema": 1, "mode": "VERIFIED_SOURCE",
                "source_run_id": "123", "source_commit_sha": A,
                "production_writes": False, "hashes": {
                    n: hashlib.sha256(v).hexdigest() for n, v in FILES.items()}}))
            output = root / "handoff.json"
            with self.assertRaises(ValueError):
                produce_verified_history(manifest, output, current_sha=B, run_id="789")
            def reject(*args, **kwargs):
                raise ValueError("wrong workflow")
            with self.assertRaises(ValueError):
                produce_verified_history(manifest, output, current_sha=B,
                                         run_id="789", token="test", verify_origin=reject)
            self.assertFalse(output.exists())


    def test_existing_evidence_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({
                "schema": 1, "mode": "VERIFIED_SOURCE",
                "source_run_id": "123", "source_commit_sha": A,
                "production_writes": False,
                "hashes": {n: hashlib.sha256(v).hexdigest() for n, v in FILES.items()}
            }))
            output = root / "handoff.json"
            output.write_text("ORIGINAL", encoding="utf-8")
            def verify(*args, **kwargs):
                return {"artifact_id": 456, "source_run_id": "123",
                        "source_commit_sha": A}
            def download(*, destination, **kwargs):
                destination.mkdir()
                for name, value in FILES.items():
                    (destination / name).write_bytes(value)
            with self.assertRaises(ValueError):
                produce_verified_history(
                    manifest, output, current_sha=B, run_id="789",
                    token="test-token", verify_origin=verify, download=download)
            self.assertEqual(output.read_text(encoding="utf-8"), "ORIGINAL")

    def test_k1_rejects_protected_output_before_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"mode": "VERIFIED_SOURCE"}))
            calls = []
            def verify(*args, **kwargs):
                calls.append("network")
                raise AssertionError("Network verification must not run")
            with self.assertRaises(PermissionError):
                produce_verified_history(manifest, root / "playlist.m3u8",
                                         current_sha=B, run_id="789", token="test",
                                         verify_origin=verify)
            self.assertEqual(calls, [])
            self.assertFalse((root / "playlist.m3u8").exists())

    def test_fixture_workflow_cannot_be_real_source_origin(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({
                "schema": 1, "mode": "VERIFIED_SOURCE",
                "source_run_id": "123", "source_commit_sha": A,
                "production_writes": False,
                "hashes": {n: hashlib.sha256(v).hexdigest() for n, v in FILES.items()}
            }))
            seen = []
            def verify(*args, **kwargs):
                seen.append(kwargs["workflow_path"])
                if kwargs["workflow_path"] == ".github/workflows/madsc-05-bakim.yml":
                    raise AssertionError("Fixture CI must never be a verified real source")
                raise ValueError("No independent real source producer exists yet")
            output = root / "handoff.json"
            with self.assertRaisesRegex(ValueError, "No independent real source"):
                produce_verified_history(
                    manifest, output, current_sha=B, run_id="789",
                    token="test-token", verify_origin=verify)
            self.assertEqual(seen, [".github/workflows/madsc-k2-real-history-source.yml"])
            self.assertFalse(output.exists())

if __name__ == "__main__":
    unittest.main()
