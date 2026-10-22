import tempfile
import unittest
from pathlib import Path

from madsc.k4_restore_gate import audit_k4_restore


class K4RestoreGateTests(unittest.TestCase):
    def test_independent_matching_trees_pass_sandbox_only(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            for name in ("source", "backup", "restored"):
                (base / name).mkdir()
                (base / name / "fixture.txt").write_bytes(b"original bytes")
            result = audit_k4_restore(base / "source", base / "backup",
                                      base / "restored", ["fixture.txt"])
            self.assertTrue(result["sandbox_restore_accepted"])
            self.assertFalse(result["production_restore_approved"])
            self.assertFalse(result["external_storage_proven"])
            self.assertFalse(result["production_writes"])

    def test_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            for name in ("source", "backup", "restored"):
                (base / name).mkdir()
                (base / name / "fixture.txt").write_bytes(b"original bytes")
            (base / "restored" / "fixture.txt").write_bytes(b"corrupt")
            result = audit_k4_restore(base / "source", base / "backup",
                                      base / "restored", ["fixture.txt"])
            self.assertFalse(result["sandbox_restore_accepted"])
            self.assertEqual(result["next_action"], "HALT_AND_INVESTIGATE")

    def test_extra_restored_file_blocks_sandbox_acceptance(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / n for n in ("source", "backup", "restored")]
            for root in trees:
                root.mkdir()
                (root / "file.txt").write_bytes(b"same")
            self.assertTrue(audit_k4_restore(*trees, ["file.txt"])["sandbox_restore_accepted"])
            (trees[2] / "unexpected.txt").write_bytes(b"extra")
            result = audit_k4_restore(*trees, ["file.txt"])
            self.assertFalse(result["sandbox_restore_accepted"])
            self.assertEqual(result["next_action"], "HALT_AND_INVESTIGATE")

    def test_extra_empty_directory_and_source_symlink_block_acceptance(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / n for n in ("source", "backup", "restored")]
            for root in trees:
                (root / "nested").mkdir(parents=True)
                (root / "nested" / "file.txt").write_bytes(b"same")
            names = ["nested/file.txt"]
            self.assertTrue(audit_k4_restore(*trees, names)["sandbox_restore_accepted"])
            (trees[1] / "unexpected_dir").mkdir()
            self.assertFalse(audit_k4_restore(*trees, names)["sandbox_restore_accepted"])
            (trees[1] / "unexpected_dir").rmdir()
            (trees[0] / "alias").symlink_to(trees[0] / "nested", target_is_directory=True)
            self.assertFalse(audit_k4_restore(*trees, names)["sandbox_restore_accepted"])

    def test_nested_tree_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            for name in ("source", "backup"):
                (base / name).mkdir()
            (base / "backup" / "restored").mkdir()
            with self.assertRaises(ValueError):
                audit_k4_restore(base / "source", base / "backup",
                                 base / "backup" / "restored", ["fixture.txt"])


if __name__ == "__main__":
    unittest.main()
