import tempfile
import unittest
from pathlib import Path
from madsc.backup import snapshot_manifest, verify_manifest, compare_copy, verify_sandbox_restore, verify_independent_restore

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

    def test_sandbox_copy_integrity(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            left, right = Path(a), Path(b)
            (left / "sample.txt").write_text("same")
            (right / "sample.txt").write_text("same")
            self.assertTrue(compare_copy(left, right, ["sample.txt"]))
            (right / "sample.txt").write_text("changed")
            self.assertFalse(compare_copy(left, right, ["sample.txt"]))

    def test_sandbox_restore_audit(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            (Path(a) / "one.txt").write_text("fixture")
            (Path(b) / "one.txt").write_text("fixture")
            report = verify_sandbox_restore(Path(a), Path(b), ["one.txt"])
            self.assertTrue(report["sandbox_restore_matches"])
            self.assertFalse(report["production_restore_verified"])
            (Path(b) / "one.txt").write_text("corrupted")
            self.assertFalse(verify_sandbox_restore(Path(a), Path(b), ["one.txt"])["sandbox_restore_matches"])

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

    def test_independent_three_tree_restore(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b, tempfile.TemporaryDirectory() as c:
            for root in (a, b, c):
                (Path(root) / "sample.txt").write_text("original")
            report = verify_independent_restore(Path(a), Path(b), Path(c), ["sample.txt"])
            self.assertTrue(report["independent_sandbox_restore_matches"])
            self.assertFalse(report["external_storage_proven"])
            self.assertFalse(report["production_restore_verified"])
            (Path(c) / "sample.txt").write_text("damaged")
            self.assertFalse(verify_independent_restore(Path(a), Path(b), Path(c), ["sample.txt"])["independent_sandbox_restore_matches"])

    def test_independent_restore_rejects_same_tree(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            (Path(a) / "sample.txt").write_text("original")
            (Path(b) / "sample.txt").write_text("original")
            with self.assertRaises(ValueError):
                verify_independent_restore(Path(a), Path(a), Path(b), ["sample.txt"])

    def test_independent_restore_rejects_duplicate_names(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b, tempfile.TemporaryDirectory() as c:
            for root in (a, b, c):
                (Path(root) / "sample.txt").write_text("fixture")
            with self.assertRaises(ValueError):
                verify_independent_restore(Path(a), Path(b), Path(c), ["sample.txt", "sample.txt"])
