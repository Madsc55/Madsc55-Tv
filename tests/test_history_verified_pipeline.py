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


if __name__ == "__main__":
    unittest.main()
