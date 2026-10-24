import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from madsc.k2_artifact_verify import verify_file
from madsc.k2_daily_evidence import build_daily_evidence


class K2ArtifactVerifyTests(unittest.TestCase):
    def test_trusted_digest_and_internal_integrity(self):
        artifact = build_daily_evidence([], day="2026-10-24", source_commit="a" * 40)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "artifact.json"
            path.write_text(json.dumps(artifact), encoding="utf-8")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertTrue(verify_file(str(path), digest))
            self.assertFalse(verify_file(str(path), "0" * 64))
            artifact["production_ready"] = True
            path.write_text(json.dumps(artifact), encoding="utf-8")
            self.assertFalse(verify_file(str(path), digest))
            self.assertFalse(verify_file(str(path), hashlib.sha256(path.read_bytes()).hexdigest()))
