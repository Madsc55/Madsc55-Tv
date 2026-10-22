import json
import tempfile
import unittest
from pathlib import Path

from madsc.parity_manifest_cli import produce_from_files


SNAPSHOT = {"exit_code": 0, "timed_out": False,
            "outputs": {"report": "b" * 64}, "side_effects": {}}


def arguments(root):
    return {
        "input_path": root / "input.bin",
        "snapshot_path": root / "snapshot.json",
        "output_root": root,
        "repository": "Madsc55/Madsc55-Tv",
        "branch": "main",
        "workflow_path": ".github/workflows/madsc-02-kesif.yml",
        "run_id": 123,
        "head_sha": "a" * 40,
    }


class ParityManifestCliTests(unittest.TestCase):
    def test_real_file_bytes_are_hashed_and_written(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            args = arguments(root)
            args["input_path"].write_bytes(b"actual job input")
            args["snapshot_path"].write_text(json.dumps(SNAPSHOT), encoding="utf-8")
            result = produce_from_files(**args)
            manifest = json.loads((root / result["relative_path"]).read_text())
            self.assertEqual(
                manifest["input_sha256"],
                "d91ecdc79bf3c39d4471016746bb7d18c9f644bd25d6466e70e10e7e3cd211c5")
            self.assertFalse(result["behavioral_parity_accepted"])

    def test_symlink_input_and_duplicate_snapshot_keys_fail_without_output(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            args = arguments(root)
            (root / "real-input").write_bytes(b"actual job input")
            args["input_path"].symlink_to(root / "real-input")
            args["snapshot_path"].write_text(json.dumps(SNAPSHOT), encoding="utf-8")
            with self.assertRaises(PermissionError):
                produce_from_files(**args)
            self.assertFalse((root / "reports").exists())

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            args = arguments(root)
            args["input_path"].write_bytes(b"actual job input")
            args["snapshot_path"].write_text(
                '{"exit_code":0,"exit_code":1,"timed_out":false,'
                '"outputs":{},"side_effects":{}}', encoding="utf-8")
            with self.assertRaises(ValueError):
                produce_from_files(**args)
            self.assertFalse((root / "reports").exists())

    def test_wrong_workflow_fails_before_output(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            args = arguments(root)
            args["input_path"].write_bytes(b"actual job input")
            args["snapshot_path"].write_text(json.dumps(SNAPSHOT), encoding="utf-8")
            args["workflow_path"] = ".github/workflows/not-installed.yml"
            with self.assertRaises(ValueError):
                produce_from_files(**args)
            self.assertFalse((root / "reports").exists())


if __name__ == "__main__":
    unittest.main()
