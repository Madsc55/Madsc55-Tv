import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from madsc.parity_snapshot_cli import _observations
from madsc.parity_snapshot_writer import (OUTPUT_PATH, build_execution_snapshot,
                                          write_execution_snapshot)


class ParitySnapshotWriterTests(unittest.TestCase):
    def test_hashes_real_output_and_side_effect_files_without_acceptance(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            output = root / "result.json"
            side_effect = root / "changed-files.txt"
            output.write_bytes(b"real output")
            side_effect.write_bytes(b"reports/one.json\n")
            result = write_execution_snapshot(
                root, exit_code=0, timed_out=False,
                outputs=[("result", output)], side_effects=[("git-diff", side_effect)])
            snapshot = json.loads((root / OUTPUT_PATH).read_text())
            self.assertEqual(snapshot["outputs"]["result"],
                             hashlib.sha256(b"real output").hexdigest())
            self.assertEqual(snapshot["side_effects"]["git-diff"],
                             hashlib.sha256(b"reports/one.json\n").hexdigest())
            self.assertFalse(result["behavioral_parity_accepted"])
            self.assertFalse(result["production_ready"])

    def test_duplicate_labels_symlinks_and_empty_outputs_fail_before_write(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            observed = root / "observed"
            observed.write_bytes(b"output")
            with self.assertRaises(ValueError):
                build_execution_snapshot(
                    exit_code=0, timed_out=False,
                    outputs=[("same", observed), ("same", observed)], side_effects=[])
            self.assertFalse((root / "reports").exists())

            link = root / "link"
            link.symlink_to(observed)
            with self.assertRaises(PermissionError):
                build_execution_snapshot(
                    exit_code=0, timed_out=False,
                    outputs=[("result", link)], side_effects=[])
            with self.assertRaises(ValueError):
                build_execution_snapshot(
                    exit_code=0, timed_out=False, outputs=[], side_effects=[])
            self.assertFalse((root / "reports").exists())

    def test_cli_observation_contract_and_existing_snapshot_fail_closed(self):
        self.assertEqual(_observations(["report=reports/result.json"]),
                         [("report", Path("reports/result.json"))])
        for value in ("missing-separator", "=empty-label", "empty-path="):
            with self.assertRaises(ValueError):
                _observations([value])
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            observed = root / "observed"
            observed.write_bytes(b"output")
            (root / "reports").mkdir()
            target = root / OUTPUT_PATH
            target.write_text("preserve", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                write_execution_snapshot(
                    root, exit_code=1, timed_out=True,
                    outputs=[("result", observed)], side_effects=[])
            self.assertEqual(target.read_text(encoding="utf-8"), "preserve")


if __name__ == "__main__":
    unittest.main()
