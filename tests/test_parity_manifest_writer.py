import hashlib
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from madsc.legacy_pair_artifact import verify_parity_artifact_manifest
from madsc.legacy_parity_evidence import CENTRAL_REPLACEMENT_WORKFLOWS
from madsc.parity_manifest_writer import (OUTPUT_PATH,
                                          build_replacement_parity_manifest,
                                          write_replacement_parity_manifest)


def execution(workflow_path=".github/workflows/madsc-05-bakim.yml"):
    return {
        "repository": "Madsc55/Madsc55-Tv",
        "branch": "main",
        "workflow_path": workflow_path,
        "run_id": 123,
        "head_sha": "a" * 40,
        "snapshot": {"exit_code": 0, "timed_out": False,
                     "outputs": {"report": "b" * 64}, "side_effects": {}},
    }


class ParityManifestWriterTests(unittest.TestCase):
    def test_all_and_only_installed_five_workflows_are_allowed(self):
        expected = {
            ".github/workflows/madsc-01-guvenlik.yml",
            ".github/workflows/madsc-02-kesif.yml",
            ".github/workflows/madsc-03-kanal-test.yml",
            ".github/workflows/madsc-04-yedek.yml",
            ".github/workflows/madsc-05-bakim.yml",
        }
        self.assertEqual(CENTRAL_REPLACEMENT_WORKFLOWS, expected)
        for path in expected:
            manifest, _ = build_replacement_parity_manifest(execution(path), b"same input")
            self.assertEqual(manifest["workflow_path"], path)

    def test_deterministic_manifest_is_accepted_by_archive_verifier(self):
        manifest, first = build_replacement_parity_manifest(execution(), b"same input")
        _, second = build_replacement_parity_manifest(execution(), b"same input")
        self.assertEqual(first, second)
        archive_buffer = io.BytesIO()
        with zipfile.ZipFile(archive_buffer, "w") as bundle:
            info = zipfile.ZipInfo("madsc-parity-evidence.json", (1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o100600 << 16
            bundle.writestr(info, first)
        archive = archive_buffer.getvalue()
        origin = {**execution(), "run_attempt": 1, "event": "workflow_dispatch",
                  "conclusion": "success", "workflow_blob_sha": "c" * 40,
                  "input_sha256": manifest["input_sha256"],
                  "artifact": {"id": 456, "name": "parity",
                               "repository": "Madsc55/Madsc55-Tv", "run_id": 123,
                               "head_sha": "a" * 40,
                               "sha256": hashlib.sha256(archive).hexdigest()}}
        verified = verify_parity_artifact_manifest(origin, archive)
        self.assertTrue(verified["artifact_manifest_verified"])

    def test_k1_writer_rejects_overwrite_symlink_and_bad_origin_before_write(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            result = write_replacement_parity_manifest(root, execution(), b"same input")
            self.assertEqual(result["relative_path"], OUTPUT_PATH)
            self.assertFalse(result["behavioral_parity_accepted"])
            self.assertFalse(result["production_ready"])
            with self.assertRaises(FileExistsError):
                write_replacement_parity_manifest(root, execution(), b"same input")

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "reports").symlink_to(root / "outside", target_is_directory=True)
            with self.assertRaises(PermissionError):
                write_replacement_parity_manifest(root, execution(), b"same input")

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            invalid = execution(".github/workflows/madsc-05-genel-bakim.yml")
            with self.assertRaises(ValueError):
                write_replacement_parity_manifest(root, invalid, b"same input")
            self.assertFalse((root / "reports").exists())

    def test_invalid_input_snapshot_and_repository_fail_closed(self):
        bad_repo = execution()
        bad_repo["repository"] = "Madsc55/madsc-tv"
        with self.assertRaises(ValueError):
            build_replacement_parity_manifest(bad_repo, b"same input")
        with self.assertRaises(ValueError):
            build_replacement_parity_manifest(execution(), b"")
        bad_snapshot = execution()
        bad_snapshot["snapshot"]["outputs"]["report"] = "not-a-digest"
        with self.assertRaises(ValueError):
            build_replacement_parity_manifest(bad_snapshot, b"same input")


if __name__ == "__main__":
    unittest.main()
