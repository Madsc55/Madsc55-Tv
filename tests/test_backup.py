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
    def test_malformed_manifest_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for invalid in (None, [], {}, {"entries": None}, {"entries": [None]}, {"entries": [{"path": 12}]}):
                with self.subTest(value=invalid), self.assertRaises(ValueError):
                    verify_manifest(root, invalid)

    def test_empty_manifest_has_no_verified_restore(self):
        with tempfile.TemporaryDirectory() as directory:
            result = snapshot_manifest(Path(directory), [])
            self.assertEqual(result["entries"], [])
            self.assertFalse(result["external_backup_verified"])
            self.assertFalse(result["restore_verified"])

    def test_absolute_path_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                snapshot_manifest(Path(directory), ["/tmp/another-file"])

    def test_symlink_source_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "real.txt").write_text("data")
            (root / "alias.txt").symlink_to(root / "real.txt")
            with self.assertRaises(ValueError):
                snapshot_manifest(root, ["alias.txt"])

    def test_intermediate_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "actual").mkdir()
            (root / "actual" / "file.txt").write_text("data")
            (root / "linked").symlink_to(root / "actual", target_is_directory=True)
            with self.assertRaises(ValueError):
                snapshot_manifest(root, ["linked/file.txt"])

    def test_escape_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises((ValueError, FileNotFoundError)):
                snapshot_manifest(Path(directory), ["../outside"])
