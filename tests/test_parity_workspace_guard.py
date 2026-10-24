import os
from pathlib import Path
import tempfile
import unittest

from madsc.parity_workspace_guard import (enforce_workspace_effects,
                                          build_workspace_effect_receipt,
                                          snapshot_workspace)


class ParityWorkspaceGuardTests(unittest.TestCase):
    def test_declared_single_output_creation_is_the_only_allowed_effect(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "reports").mkdir()
            (root / "input.txt").write_bytes(b"input")
            before = snapshot_workspace(root)
            (root / "reports/result.json").write_bytes(b"{}\n")
            after = snapshot_workspace(root)
            self.assertEqual(
                enforce_workspace_effects(
                    before, after, expected_output="reports/result.json"),
                ("reports", "reports/result.json"))
            changed = enforce_workspace_effects(
                before, after, expected_output="reports/result.json")
            receipt = build_workspace_effect_receipt(
                before, after, consumer="k4",
                expected_output="reports/result.json",
                observed_changes=changed)
            self.assertIn(b'"schema":"madsc-parity-workspace-effects-v1"', receipt)
            self.assertIn(b'"external_effects_verified":false', receipt)

    def test_undeclared_create_delete_and_rewrite_are_rejected(self):
        mutations = ("create", "delete", "rewrite")
        for mutation in mutations:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory).resolve()
                (root / "reports").mkdir()
                source = root / "source.txt"
                source.write_bytes(b"original")
                before = snapshot_workspace(root)
                if mutation == "create":
                    (root / "other.txt").write_bytes(b"other")
                elif mutation == "delete":
                    source.unlink()
                else:
                    original = source.read_bytes()
                    source.write_bytes(b"changed")
                    source.write_bytes(original)
                after = snapshot_workspace(root)
                with self.assertRaisesRegex(PermissionError, "Unexpected"):
                    enforce_workspace_effects(
                        before, after, expected_output="reports/result.json")

    def test_symlink_is_not_followed_and_target_change_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "reports").mkdir()
            outside = root.parent / (root.name + "-outside")
            outside.write_bytes(b"outside")
            try:
                (root / "link").symlink_to(outside)
                before = snapshot_workspace(root)
                (root / "link").unlink()
                (root / "link").symlink_to("reports")
                after = snapshot_workspace(root)
                with self.assertRaisesRegex(PermissionError, "Unexpected"):
                    enforce_workspace_effects(before, after, expected_output=None)
                self.assertEqual(outside.read_bytes(), b"outside")
            finally:
                outside.unlink(missing_ok=True)

    def test_special_entry_fails_closed_without_blocking(self):
        if not hasattr(os, "mkfifo"):
            self.skipTest("FIFO unsupported")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            os.mkfifo(root / "pipe")
            with self.assertRaisesRegex(PermissionError, "special"):
                snapshot_workspace(root)


if __name__ == "__main__":
    unittest.main()
