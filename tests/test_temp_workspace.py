"""K1 tests for identity-bound temporary workspaces."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from madsc.temp_workspace import guarded_temporary_directory
from madsc.write_path_audit import ProtectedWriteRejected


class TempWorkspaceTests(unittest.TestCase):
    def test_workspace_is_direct_child_and_cleaned(self):
        with guarded_temporary_directory("madsc-k3-video-") as workspace:
            self.assertEqual(workspace.parent, Path(tempfile.gettempdir()))
            self.assertTrue(workspace.name.startswith("madsc-k3-video-"))
            self.assertTrue(workspace.is_dir())
            (workspace / "sample.ts").write_bytes(b"fixture")
        self.assertFalse(workspace.exists())

    def test_unknown_prefix_is_rejected_before_creation(self):
        with patch("madsc.temp_workspace.tempfile.TemporaryDirectory") as creator:
            with self.assertRaises(ProtectedWriteRejected):
                with guarded_temporary_directory("unknown-"):
                    pass
        creator.assert_not_called()

    def test_replaced_workspace_is_not_removed(self):
        replacement = None
        with self.assertRaises(ProtectedWriteRejected):
            with guarded_temporary_directory("madsc-k4-") as workspace:
                original = workspace.with_name(workspace.name + "-original")
                workspace.rename(original)
                workspace.mkdir()
                replacement = workspace
        self.assertIsNotNone(replacement)
        self.assertTrue(replacement.is_dir())
        replacement.rmdir()
        original.rmdir()
