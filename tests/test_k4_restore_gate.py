import tempfile
import unittest
from pathlib import Path

from madsc.k4_restore_gate import audit_k4_restore


class K4RestoreGateTests(unittest.TestCase):
    def test_relative_roots_do_not_probe_filesystem_before_rejection(self):
        from unittest.mock import patch
        with patch.object(Path, "is_symlink", side_effect=AssertionError("filesystem probe")):
            with self.assertRaisesRegex(ValueError, "canonical absolute paths"):
                audit_k4_restore(Path("relative/source"), Path("/tmp/backup"),
                                 Path("/tmp/restored"), ["file.txt"])

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

    def test_inventory_io_error_fails_closed(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ("source", "backup", "restored")]
            for root in trees:
                root.mkdir()
                (root / "file.txt").write_bytes(b"same")
            original_rglob = Path.rglob

            def interrupted_inventory(path, pattern):
                if path == trees[2]:
                    def broken():
                        yield from ()
                        raise OSError("simulated unreadable inventory")
                    return broken()
                return original_rglob(path, pattern)

            with patch.object(Path, "rglob", autospec=True, side_effect=interrupted_inventory):
                result = audit_k4_restore(*trees, ["file.txt"])
            self.assertFalse(result["sandbox_restore_accepted"])
            self.assertEqual(result["next_action"], "HALT_AND_INVESTIGATE")

    def test_inventory_symlink_never_uses_following_type_checks(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ("source", "backup", "restored")]
            for root in trees:
                root.mkdir()
                (root / "file.txt").write_bytes(b"same")
            (trees[2] / "alias").symlink_to(trees[2] / "file.txt")
            original_is_file = Path.is_file
            original_is_dir = Path.is_dir

            def forbid_alias_follow(path):
                if path.name == "alias":
                    raise AssertionError("Inventory must not follow symlink type checks")
                return original_is_file(path)

            def forbid_alias_dir(path):
                if path.name == "alias":
                    raise AssertionError("Inventory must not follow symlink type checks")
                return original_is_dir(path)

            with patch.object(Path, "is_file", autospec=True, side_effect=forbid_alias_follow), \
                 patch.object(Path, "is_dir", autospec=True, side_effect=forbid_alias_dir):
                result = audit_k4_restore(*trees, ["file.txt"])
            self.assertFalse(result["sandbox_restore_accepted"])

    def test_change_after_first_manifest_check_blocks_acceptance(self):
        from unittest.mock import patch
        from madsc.backup import verify_independent_restore as actual_verify
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ("source", "backup", "restored")]
            for root in trees:
                root.mkdir()
                (root / "file.txt").write_bytes(b"same")
            calls = [0]

            def change_after_verification(*args):
                result = actual_verify(*args)
                calls[0] += 1
                if calls[0] == 1:
                    (trees[2] / "file.txt").write_bytes(b"changed")
                return result

            with patch("madsc.k4_restore_gate.verify_independent_restore",
                       side_effect=change_after_verification):
                result = audit_k4_restore(*trees, ["file.txt"])
            self.assertGreaterEqual(calls[0], 2)
            self.assertFalse(result["sandbox_restore_accepted"])
            self.assertEqual(result["next_action"], "HALT_AND_INVESTIGATE")

    def test_coordinated_three_tree_change_after_initial_check_is_rejected(self):
        from unittest.mock import patch
        from madsc.backup import verify_independent_restore as real_verify
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            trees = [base / name for name in ("source", "backup", "restored")]
            for root in trees:
                root.mkdir()
                (root / "file.txt").write_bytes(b"same")
            calls = [0]

            def change_all_trees_after_first_verify(*args):
                result = real_verify(*args)
                calls[0] += 1
                if calls[0] == 1:
                    for root in trees:
                        (root / "file.txt").write_bytes(b"new shared content")
                return result

            with patch("madsc.k4_restore_gate.verify_independent_restore",
                       side_effect=change_all_trees_after_first_verify):
                result = audit_k4_restore(*trees, ["file.txt"])
            self.assertGreaterEqual(calls[0], 2)
            self.assertFalse(result["sandbox_restore_accepted"])
            self.assertEqual(result["next_action"], "HALT_AND_INVESTIGATE")

    def test_nested_directory_symlink_swap_during_inventory_fails_closed(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            roots = [base / name for name in ("source", "backup", "restored")]
            for root in roots:
                (root / "nested").mkdir(parents=True)
                (root / "nested" / "file.txt").write_bytes(b"same")
            original_rglob = Path.rglob
            swapped = [False]

            def swap_nested_during_walk(root, pattern):
                iterator = original_rglob(root, pattern)
                if root != roots[2]:
                    return iterator

                def changed():
                    for item in iterator:
                        if item.name == "file.txt" and not swapped[0]:
                            swapped[0] = True
                            (root / "nested").rename(root / "old-nested")
                            (root / "nested").symlink_to(root / "old-nested", target_is_directory=True)
                        yield item
                return changed()

            with patch.object(Path, "rglob", autospec=True, side_effect=swap_nested_during_walk):
                result = audit_k4_restore(*roots, ["nested/file.txt"])
            self.assertTrue(swapped[0])
            self.assertFalse(result["sandbox_restore_accepted"])

    def test_root_swap_before_inventory_prevents_walk(self):
        from unittest.mock import patch
        from madsc.backup import verify_independent_restore as real_verify
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            roots = [base / name for name in ("source", "backup", "restored")]
            for root in roots:
                root.mkdir()
                (root / "file.txt").write_bytes(b"same")
            original_rglob = Path.rglob
            calls = [0]

            def swap_root_after_first_verify(*args):
                result = real_verify(*args)
                calls[0] += 1
                if calls[0] == 1:
                    roots[2].rename(base / "old-restored")
                    roots[2].mkdir()
                    (roots[2] / "file.txt").write_bytes(b"same")
                return result

            def forbid_swapped_walk(root, pattern):
                if root == roots[2]:
                    raise AssertionError("swapped restore root must not be walked")
                return original_rglob(root, pattern)

            with patch("madsc.k4_restore_gate.verify_independent_restore", side_effect=swap_root_after_first_verify), \
                 patch.object(Path, "rglob", autospec=True, side_effect=forbid_swapped_walk):
                result = audit_k4_restore(*roots, ["file.txt"])
            self.assertEqual(calls[0], 1)
            self.assertFalse(result["sandbox_restore_accepted"])

    def test_ancestor_swap_before_inventory_prevents_walk(self):
        from unittest.mock import patch
        from madsc.backup import verify_independent_restore as real_verify
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            parent = base / "parent"
            parent.mkdir()
            roots = [parent / name for name in ("source", "backup", "restored")]
            for root in roots:
                root.mkdir()
                (root / "file.txt").write_bytes(b"same")
            calls = [0]
            original_rglob = Path.rglob

            def swap_after_first_verify(*args):
                result = real_verify(*args)
                calls[0] += 1
                if calls[0] == 1:
                    parent.rename(base / "real-parent")
                    parent.symlink_to(base / "real-parent", target_is_directory=True)
                return result

            def reject_inventory_walk(root, pattern):
                raise AssertionError("must not traverse symlinked ancestor")

            with patch("madsc.k4_restore_gate.verify_independent_restore", side_effect=swap_after_first_verify), \
                 patch.object(Path, "rglob", autospec=True, side_effect=reject_inventory_walk):
                result = audit_k4_restore(*roots, ["file.txt"])
            self.assertEqual(calls[0], 1)
            self.assertFalse(result["sandbox_restore_accepted"])

    def test_symlinked_ancestor_during_inventory_blocks_second_read(self):
        from unittest.mock import patch
        from madsc.backup import verify_independent_restore as real_verify
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            parent = base / "parent"
            parent.mkdir()
            roots = [parent / name for name in ("source", "backup", "restored")]
            for root in roots:
                root.mkdir()
                (root / "file.txt").write_bytes(b"same")
            original_rglob = Path.rglob
            calls = [0]
            swapped = [False]

            def swap_parent_during_inventory(root, pattern):
                if root == roots[2] and not swapped[0]:
                    swapped[0] = True
                    parent.rename(base / "real-parent")
                    parent.symlink_to(base / "real-parent", target_is_directory=True)
                return original_rglob(root, pattern)

            def count_verify(*args):
                calls[0] += 1
                return real_verify(*args)

            with patch.object(Path, "rglob", autospec=True, side_effect=swap_parent_during_inventory), \
                 patch("madsc.k4_restore_gate.verify_independent_restore", side_effect=count_verify):
                result = audit_k4_restore(*roots, ["file.txt"])
            self.assertEqual(calls[0], 1)
            self.assertFalse(result["sandbox_restore_accepted"])

    def test_symlinked_ancestor_added_after_verification_fails_closed(self):
        from unittest.mock import patch
        from madsc.backup import verify_independent_restore as real_verify
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            parent = base / "parent"
            parent.mkdir()
            roots = [parent / "source", parent / "backup", parent / "restored"]
            for root in roots:
                root.mkdir()
                (root / "file.txt").write_bytes(b"same")
            calls = [0]

            def replace_parent_after_verify(*args):
                result = real_verify(*args)
                calls[0] += 1
                if calls[0] == 2:
                    parent.rename(base / "real-parent")
                    parent.symlink_to(base / "real-parent", target_is_directory=True)
                return result

            with patch("madsc.k4_restore_gate.verify_independent_restore",
                       side_effect=replace_parent_after_verify):
                result = audit_k4_restore(*roots, ["file.txt"])
            self.assertEqual(calls[0], 2)
            self.assertFalse(result["sandbox_restore_accepted"])

    def test_root_swap_during_inventory_blocks_second_verification(self):
        from unittest.mock import patch
        from madsc.backup import verify_independent_restore as real_verify
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            roots = [base / name for name in ("source", "backup", "restored")]
            for root in roots:
                root.mkdir()
                (root / "file.txt").write_bytes(b"same")
            original_rglob = Path.rglob
            calls = [0]

            def swap_before_inventory(root, pattern):
                if root == roots[2]:
                    old = base / "old-restored"
                    roots[2].rename(old)
                    roots[2].mkdir()
                    (roots[2] / "file.txt").write_bytes(b"same")
                return original_rglob(root, pattern)

            def count_verification(*args):
                calls[0] += 1
                return real_verify(*args)

            with patch.object(Path, "rglob", autospec=True, side_effect=swap_before_inventory), \
                 patch("madsc.k4_restore_gate.verify_independent_restore", side_effect=count_verification):
                result = audit_k4_restore(*roots, ["file.txt"])
            self.assertEqual(calls[0], 1)
            self.assertFalse(result["sandbox_restore_accepted"])

    def test_replaced_restore_root_with_identical_bytes_fails_closed(self):
        from unittest.mock import patch
        from madsc.backup import verify_independent_restore as real_verify
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            roots = [base / name for name in ("source", "backup", "restored")]
            for root in roots:
                root.mkdir()
                (root / "file.txt").write_bytes(b"same")
            calls = [0]

            def replace_after_verify(*args):
                result = real_verify(*args)
                calls[0] += 1
                if calls[0] == 2:
                    old = base / "old-restored"
                    roots[2].rename(old)
                    roots[2].mkdir()
                    (roots[2] / "file.txt").write_bytes(b"same")
                return result

            with patch("madsc.k4_restore_gate.verify_independent_restore",
                       side_effect=replace_after_verify):
                result = audit_k4_restore(*roots, ["file.txt"])
            self.assertEqual(calls[0], 2)
            self.assertFalse(result["sandbox_restore_accepted"])
            self.assertEqual(result["next_action"], "HALT_AND_INVESTIGATE")

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

    def test_portable_directory_aliases_rejected_before_hashing(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            roots = [base / name for name in ("source", "backup", "restored")]
            for root in roots:
                root.mkdir()
            for names, error in (
                (["Folder/one.txt", "folder/two.txt"], "directory alias"),
                (["file", "FILE/child.txt"], "file-directory collision"),
                (["ﬁles/a.txt", "files/b.txt"], "directory alias"),
            ):
                with self.subTest(names=names):
                    with patch("madsc.k4_restore_gate.verify_independent_restore") as verify:
                        with self.assertRaisesRegex(ValueError, error):
                            audit_k4_restore(*roots, names)
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
