"""Source audit must reject forged workflow blobs before reporting."""
import base64
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from madsc import legacy_99_bulk_audit as audit


class Legacy99SourceIntegrityTests(unittest.TestCase):
    def test_all_99_blobs_verified_byte_exactly(self):
        raw = b"name: sample\\non: workflow_dispatch\\n"
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\0" + raw).hexdigest()
        entries = [{"path": f".github/workflows/{i:03d}.yml",
                    "type": "blob", "size": len(raw), "sha": sha}
                   for i in range(99)]
        def fake_github(url, token):
            if "/git/trees/" in url:
                return {"tree": entries, "sha": "source-tree", "truncated": False}
            return {"sha": sha, "encoding": "base64",
                    "content": base64.b64encode(raw).decode()}
        with tempfile.TemporaryDirectory() as temp, patch.object(audit, "github", side_effect=fake_github):
            path = Path(temp) / "audit.json"
            audit.run(path, "")
            import json
            report = json.loads(path.read_text())
            self.assertEqual(report["source_workflow_count"], 99)
            self.assertEqual(report["source_tree_sha"], "source-tree")
            self.assertEqual(report["behavioral_parity_verified_count"], 0)

    def test_forged_blob_is_rejected(self):
        raw = b"name: sample\\n"
        sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\0" + raw).hexdigest()
        entries = [{"path": f".github/workflows/{i:03d}.yml",
                    "type": "blob", "size": len(raw), "sha": sha}
                   for i in range(99)]
        def fake_github(url, token):
            if "/git/trees/" in url:
                return {"tree": entries, "truncated": False}
            return {"sha": sha, "encoding": "base64",
                    "content": base64.b64encode(b"evil payload!").decode()}
        with tempfile.TemporaryDirectory() as temp, patch.object(audit, "github", side_effect=fake_github):
            with self.assertRaises(ValueError):
                audit.run(Path(temp) / "audit.json", "")


if __name__ == "__main__":
    unittest.main()
