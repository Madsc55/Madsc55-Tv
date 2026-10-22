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

    def test_deep_nested_directory_inventory_is_canonical(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ("source", "backup", "restored")]
            for root in trees:
                (root / "first" / "second").mkdir(parents=True)
                (root / "first" / "second" / "file.txt").write_bytes(b"same")
            result = audit_k4_restore(*trees, ["first/second/file.txt"])
            self.assertTrue(result["sandbox_restore_accepted"])
            self.assertFalse(result["external_storage_proven"])

    def test_symlinked_ancestor_rejected_before_restore_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            actual = base / "actual"
            actual.mkdir()
            alias = base / "alias"
            alias.symlink_to(actual, target_is_directory=True)
            roots = [actual / name for name in ("source", "backup", "restored")]
            for root in roots:
                root.mkdir()
                (root / "file.txt").write_bytes(b"same")
            with self.assertRaisesRegex(ValueError, "symlink ancestors"):
                audit_k4_restore(alias / "source", roots[1], roots[2], ["file.txt"])

    def test_inventory_scan_rejects_more_than_twenty_thousand_entries(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ("source", "backup", "restored")]
            for root in trees:
                root.mkdir()
                (root / "file.txt").write_bytes(b"same")
            original_rglob = Path.rglob

            def oversized_inventory(root, pattern):
                if root == trees[2]:
                    return iter([root / "file.txt"] * 20001)
                return original_rglob(root, pattern)

            with patch.object(Path, "rglob", autospec=True, side_effect=oversized_inventory):
                result = audit_k4_restore(*trees, ["file.txt"])
            self.assertFalse(result["sandbox_restore_accepted"])
            self.assertEqual(result["next_action"], "HALT_AND_INVESTIGATE")
            self.assertFalse(result["production_restore_approved"])

    def test_declared_inventory_limit_rejected_before_hashing(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ("source", "backup", "restored")]
            for root in trees:
                root.mkdir()
            names = [f"file_{index}.txt" for index in range(20001)]
            with patch("madsc.k4_restore_gate.verify_independent_restore") as verify:
                with self.assertRaisesRegex(ValueError, "safe entry limit"):
                    audit_k4_restore(*trees, names)
                verify.assert_not_called()

    def test_declared_nested_directory_overflow_rejected_before_hashing(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ("source", "backup", "restored")]
            for root in trees:
                root.mkdir()
            # One declared file can expand into more than the safe directory budget.
            deep_name = "/".join(f"d{i}" for i in range(20001)) + "/file.txt"
            with patch("madsc.k4_restore_gate.verify_independent_restore") as verify:
                with self.assertRaisesRegex(ValueError, "safe entry limit"):
                    audit_k4_restore(*trees, [deep_name])
                verify.assert_not_called()

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
