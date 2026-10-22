import hashlib
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from madsc.legacy_pair_artifact import MANIFEST_NAME, verify_parity_artifact_manifest
from madsc.parity_manifest_cli import produce_from_files
from madsc.parity_snapshot_writer import OUTPUT_PATH as SNAPSHOT_PATH
from madsc.parity_snapshot_writer import write_execution_snapshot


class ParityProducerChainTests(unittest.TestCase):
    def test_real_files_flow_from_snapshot_to_digest_bound_artifact(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            actual_input = root / "actual-input.bin"
            actual_output = root / "actual-output.json"
            actual_input.write_bytes(b"identical input bytes")
            actual_output.write_bytes(b'{"result":"measured"}\n')
            write_execution_snapshot(
                root, exit_code=0, timed_out=False,
                outputs=[("result", actual_output)], side_effects=[])
            produce_from_files(
                input_path=actual_input, snapshot_path=root / SNAPSHOT_PATH,
                output_root=root, repository="Madsc55/Madsc55-Tv", branch="main",
                workflow_path=".github/workflows/madsc-05-bakim.yml",
                run_id=123, head_sha="a" * 40)

            manifest_path = root / "reports" / MANIFEST_NAME
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            archive_buffer = io.BytesIO()
            with zipfile.ZipFile(archive_buffer, "w") as bundle:
                bundle.write(manifest_path, MANIFEST_NAME)
            archive = archive_buffer.getvalue()
            origin = {
                "repository": "Madsc55/Madsc55-Tv", "branch": "main",
                "workflow_path": ".github/workflows/madsc-05-bakim.yml",
                "workflow_blob_sha": "c" * 40, "run_id": 123, "run_attempt": 1,
                "head_sha": "a" * 40, "event": "workflow_dispatch",
                "conclusion": "success", "input_sha256": manifest["input_sha256"],
                "snapshot": manifest["snapshot"],
                "artifact": {"id": 456, "name": "parity",
                             "repository": "Madsc55/Madsc55-Tv", "run_id": 123,
                             "head_sha": "a" * 40,
                             "sha256": hashlib.sha256(archive).hexdigest()},
            }
            verified = verify_parity_artifact_manifest(origin, archive)
            self.assertTrue(verified["artifact_manifest_verified"])
            self.assertEqual(manifest["snapshot"]["outputs"]["result"],
                             hashlib.sha256(actual_output.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
