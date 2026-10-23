import tempfile
import unittest
from pathlib import Path

from madsc.k4_restore_gate import audit_k4_restore


class K4RestoreGateTests(unittest.TestCase):
    def test_restore_roots_with_traversal_segments_are_rejected(self):
        from unittest.mock import patch
        with patch('madsc.k4_restore_gate.verify_independent_restore') as verify:
            with self.assertRaisesRegex(ValueError, 'canonical absolute paths'):
                audit_k4_restore(Path('/tmp/source/../source'), Path('/tmp/backup'),
                                 Path('/tmp/restored'), ['file.txt'])
            verify.assert_not_called()

    def test_relative_restore_roots_are_rejected_before_hashing(self):
        from unittest.mock import patch
        with patch('madsc.k4_restore_gate.verify_independent_restore') as verify:
            with self.assertRaisesRegex(ValueError, 'canonical absolute paths'):
                audit_k4_restore(Path('source'), Path('backup'), Path('restored'), ['file.txt'])
            verify.assert_not_called()

    def test_empty_restore_inventory_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ('source', 'backup', 'restored')]
            for root in trees:
                root.mkdir()
            with self.assertRaisesRegex(ValueError, 'at least one declared file'):
                audit_k4_restore(*trees, [])

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

    def test_manifest_file_ceiling_rejected_before_hashing(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ('source', 'backup', 'restored')]
            for root in trees:
                root.mkdir()
            names = [f'file_{index}.txt' for index in range(10001)]
            with patch('madsc.k4_restore_gate.verify_independent_restore') as verify:
                with self.assertRaisesRegex(ValueError, 'manifest entry limit'):
                    audit_k4_restore(*trees, names)
                verify.assert_not_called()

    def test_declared_inventory_limit_rejected_before_hashing(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ("source", "backup", "restored")]
            for root in trees:
                root.mkdir()
            names = [f"file_{index}.txt" for index in range(20001)]
            with patch("madsc.k4_restore_gate.verify_independent_restore") as verify:
                with self.assertRaisesRegex(ValueError, "manifest entry limit"):
                    audit_k4_restore(*trees, names)
                verify.assert_not_called()

    def test_declared_nested_directory_overflow_rejected_before_hashing(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ("source", "backup", "restored")]
            for root in trees:
                root.mkdir()
            # 10,001 distinct two-level directories plus their files exceed
            # the total inventory budget without requiring extreme path depth.
            names = [f"folder_{i}/child/file.txt" for i in range(10001)]
            with patch("madsc.k4_restore_gate.verify_independent_restore") as verify:
                with self.assertRaisesRegex(ValueError, "manifest entry limit"):
                    audit_k4_restore(*trees, names)
                verify.assert_not_called()

    def test_unsafe_declared_paths_rejected_before_hashing(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ("source", "backup", "restored")]
            for root in trees:
                root.mkdir()
            for name in ("../escape", "nested/../escape", "nested//file",
                         "nested/./file", "/absolute", "C:drive", "~alias",
                         "nested\\\\file", "bad\\nname"):
                with self.subTest(name=name):
                    with patch("madsc.k4_restore_gate.verify_independent_restore") as verify:
                        with self.assertRaisesRegex(ValueError, "Unsafe restore audit path"):
                            audit_k4_restore(*trees, [name])
                        verify.assert_not_called()

    def test_file_directory_collision_rejected_before_hashing(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ('source', 'backup', 'restored')]
            for root in trees:
                root.mkdir()
            with patch('madsc.k4_restore_gate.verify_independent_restore') as verify:
                with self.assertRaisesRegex(ValueError, 'file conflicts with declared directory'):
                    audit_k4_restore(*trees, ['folder', 'folder/file.txt'])
                verify.assert_not_called()

    def test_invisible_format_controls_rejected_before_hashing(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ('source', 'backup', 'restored')]
            for root in trees:
                root.mkdir()
            for name in ('bad\\u202ename.txt', 'bad\\u200bname.txt'):
                with self.subTest(name=name):
                    with patch('madsc.k4_restore_gate.verify_independent_restore') as verify:
                        with self.assertRaisesRegex(ValueError, 'Unsafe restore audit path'):
                            audit_k4_restore(*trees, [name])
                        verify.assert_not_called()

    def test_portable_path_aliases_rejected_before_hashing(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ('source', 'backup', 'restored')]
            for root in trees:
                root.mkdir()
            for names in (["A.txt", "a.TXT"], ["file.txt", "ﬁle.txt"]):
                with self.subTest(names=names):
                    with patch('madsc.k4_restore_gate.verify_independent_restore') as verify:
                        with self.assertRaisesRegex(ValueError, 'Ambiguous restore audit path alias'):
                            audit_k4_restore(*trees, names)
                        verify.assert_not_called()

    def test_duplicate_oversized_and_surrogate_paths_fail_before_hashing(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ("source", "backup", "restored")]
            for root in trees:
                root.mkdir()
            for names, error in (
                (["file.txt", "file.txt"], "Duplicate restore audit path"),
                (["a" * 4097], "bounded length"),
                (["bad\\ud800name"], "Unsafe restore audit path"),
            ):
                with self.subTest(error=error):
                    with patch("madsc.k4_restore_gate.verify_independent_restore") as verify:
                        with self.assertRaisesRegex(ValueError, error):
                            audit_k4_restore(*trees, names)
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
