import tempfile
import unittest
from pathlib import Path
from madsc.backup import snapshot_manifest, verify_manifest

class BackupTests(unittest.TestCase):
    def test_manifest_detects_changes_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/"a.txt").write_text("original")
            report = snapshot_manifest(root, ["a.txt"])
            self.assertTrue(verify_manifest(root, report))
            self.assertFalse(report["external_backup_verified"])
            self.assertFalse(report["restore_verified"])
            (root/"a.txt").write_text("changed")
            self.assertFalse(verify_manifest(root, report))
    def test_escape_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises((ValueError, FileNotFoundError)):
                snapshot_manifest(Path(directory), ["../outside"])
