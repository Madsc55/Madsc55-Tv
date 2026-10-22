import tempfile
import unittest
from pathlib import Path
from madsc.backup import snapshot_manifest, verify_manifest, compare_copy, verify_sandbox_restore, verify_independent_restore

class BackupTests(unittest.TestCase):
    def test_sandbox_destination_open_rejects_symlinked_parent(self):
        from madsc.backup import _create_relative_file_nofollow
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "destination"
            outside = base / "outside"
            root.mkdir()
            outside.mkdir()
            (outside / "sentinel.txt").write_text("keep")
            (root / "nested").symlink_to(outside, target_is_directory=True)
            st = root.stat()
            with self.assertRaises(OSError):
                _create_relative_file_nofollow(root, ("nested", "escaped.txt"),
                                                (st.st_dev, st.st_ino))
            self.assertFalse((outside / "escaped.txt").exists())
            self.assertEqual((outside / "sentinel.txt").read_text(), "keep")

    def test_sandbox_destination_open_requires_original_root_inode(self):
        from madsc.backup import _create_relative_file_nofollow
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "safe.txt").write_text("existing")
            st = root.stat()
            with self.assertRaisesRegex(ValueError, "root changed"):
                _create_relative_file_nofollow(root, ("new.txt",),
                                                (st.st_dev + 1, st.st_ino))
            self.assertFalse((root / "new.txt").exists())

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
    def test_manifest_rejects_duplicate_and_unsafe_paths(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.txt").write_text("safe")
            for names in (["a.txt", "a.txt"], ["a\\b"], ["./a.txt"],
                          ["a//b"], [""], [None]):
                with self.subTest(names=names), self.assertRaises(ValueError):
                    snapshot_manifest(root, names)

    def test_manifest_rejects_malformed_integrity_fields(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.txt").write_text("safe")
            entry = snapshot_manifest(root, ["a.txt"])["entries"][0]
            for bad in ({**entry, "sha256": "invalid"},
                        {**entry, "bytes": True}, {**entry, "bytes": -1}):
                with self.subTest(entry=bad), self.assertRaises(ValueError):
                    verify_manifest(root, {"entries": [bad]})
    def test_manifest_rejects_symlink_root(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            real = base / "real"
            real.mkdir()
            (real / "sample.txt").write_text("fixture")
            alias = base / "alias"
            alias.symlink_to(real, target_is_directory=True)
            with self.assertRaises(ValueError):
                snapshot_manifest(alias, ["sample.txt"])

    def test_independent_restore_rejects_symlink_tree(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            trees = [base / name for name in ("source", "backup", "restored")]
            for tree in trees:
                tree.mkdir()
                (tree / "sample.txt").write_text("fixture")
            alias = base / "backup-alias"
            alias.symlink_to(trees[1], target_is_directory=True)
            with self.assertRaises(ValueError):
                verify_independent_restore(trees[0], alias, trees[2], ["sample.txt"])
    def test_empty_sandbox_restore_cannot_claim_success(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            for invalid in ([], None, "sample.txt"):
                with self.subTest(names=invalid), self.assertRaises(ValueError):
                    verify_sandbox_restore(Path(a), Path(b), invalid)
    def test_independent_restore_rejects_nested_trees(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            source = base / "source"
            backup = source / "backup"
            restored = base / "restored"
            for tree in (source, backup, restored):
                tree.mkdir(parents=True, exist_ok=True)
                (tree / "sample.txt").write_text("fixture")
            with self.assertRaises(ValueError):
                verify_independent_restore(source, backup, restored, ["sample.txt"])

    def test_independent_restore_rejects_duplicate_resolved_roots(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            source, backup = base / "source", base / "backup"
            source.mkdir()
            backup.mkdir()
            for tree in (source, backup):
                (tree / "sample.txt").write_text("fixture")
            with self.assertRaises(ValueError):
                verify_independent_restore(source, backup, source / ".", ["sample.txt"])
    def test_manifest_rejects_duplicate_entries(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.txt").write_text("fixture")
            manifest = snapshot_manifest(root, ["a.txt"])
            manifest["entries"].append(dict(manifest["entries"][0]))
            with self.assertRaises(ValueError):
                verify_manifest(root, manifest)

    def test_manifest_verifies_only_declared_entries_and_canonical_order(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.txt").write_text("fixture")
            (root / "b.txt").write_text("fixture-b")
            manifest = snapshot_manifest(root, ["a.txt", "b.txt"])
            self.assertTrue(verify_manifest(root, manifest))
            missing = {**manifest, "entries": manifest["entries"][:1]}
            self.assertTrue(verify_manifest(root, missing))
            self.assertFalse(verify_manifest(root, {**manifest, "entries": list(reversed(manifest["entries"]))}))


    def test_backup_corruption_is_detected(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b, tempfile.TemporaryDirectory() as c:
            roots = [Path(x) for x in (a, b, c)]
            for root in roots:
                (root / "sample.txt").write_text("original")
            (roots[1] / "sample.txt").write_text("corrupted")
            result = verify_independent_restore(*roots, ["sample.txt"])
            self.assertFalse(result["backup_verified_against_source"])
            self.assertFalse(result["independent_sandbox_restore_matches"])
            self.assertFalse(result["production_writes"])

    def test_restore_corruption_is_detected(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b, tempfile.TemporaryDirectory() as c:
            roots = [Path(x) for x in (a, b, c)]
            for root in roots:
                (root / "sample.txt").write_text("original")
            (roots[2] / "sample.txt").write_text("corrupted")
            result = verify_independent_restore(*roots, ["sample.txt"])
            self.assertTrue(result["backup_verified_against_source"])
            self.assertFalse(result["restore_verified_against_backup"])
            self.assertFalse(result["production_restore_verified"])


    def test_three_tree_restore_detects_missing_or_changed_nested_file(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            roots = [base / name for name in ("source", "backup", "restored")]
            for root in roots:
                (root / "nested").mkdir(parents=True)
                (root / "nested" / "channel.txt").write_bytes(b"same-content")
            names = ["nested/channel.txt"]
            good = verify_independent_restore(*roots, names)
            self.assertTrue(good["independent_sandbox_restore_matches"])
            self.assertFalse(good["external_storage_proven"])
            (roots[2] / "nested" / "channel.txt").write_bytes(b"changed")
            changed = verify_independent_restore(*roots, names)
            self.assertFalse(changed["restore_verified_against_backup"])
            self.assertFalse(changed["independent_sandbox_restore_matches"])
            (roots[2] / "nested" / "channel.txt").unlink()
            with self.assertRaises((ValueError, FileNotFoundError)):
                verify_independent_restore(*roots, names)

    def test_three_tree_restore_rejects_symlinked_nested_backup_file(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            roots = [base / name for name in ("source", "backup", "restored")]
            for root in roots:
                (root / "nested").mkdir(parents=True)
                (root / "nested" / "channel.txt").write_text("fixture")
            target = roots[1] / "nested" / "channel.txt"
            target.unlink()
            target.symlink_to(roots[0] / "nested" / "channel.txt")
            with self.assertRaises(ValueError):
                verify_independent_restore(*roots, ["nested/channel.txt"])


    def test_three_tree_detects_same_length_content_corruption(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            roots = [base / name for name in ("source", "backup", "restored")]
            for root in roots:
                root.mkdir()
                (root / "channel.txt").write_bytes(b"ABCD")
            (roots[1] / "channel.txt").write_bytes(b"WXYZ")
            report = verify_independent_restore(*roots, ["channel.txt"])
            self.assertFalse(report["backup_verified_against_source"])
            self.assertFalse(report["restore_verified_against_backup"])
            self.assertFalse(report["independent_sandbox_restore_matches"])
            self.assertFalse(report["external_storage_proven"])

    def test_three_tree_multiple_files_detects_one_changed_restore(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            roots = [base / name for name in ("source", "backup", "restored")]
            for root in roots:
                root.mkdir()
                (root / "channels.txt").write_text("channels", encoding="utf-8")
                (root / "epg.xml").write_text("<tv/>", encoding="utf-8")
            names = ["channels.txt", "epg.xml"]
            self.assertTrue(verify_independent_restore(*roots, names)["independent_sandbox_restore_matches"])
            (roots[2] / "epg.xml").write_text("<tv>bad</tv>", encoding="utf-8")
            result = verify_independent_restore(*roots, names)
            self.assertTrue(result["backup_verified_against_source"])
            self.assertFalse(result["restore_verified_against_backup"])
            self.assertEqual(result["files_checked"], 2)
            self.assertFalse(result["production_restore_verified"])


    def test_manifest_rejects_reordered_entries_even_when_hashes_match(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.txt").write_text("A")
            (root / "b.txt").write_text("B")
            manifest = snapshot_manifest(root, ["b.txt", "a.txt"])
            self.assertTrue(verify_manifest(root, manifest))
            manifest["entries"].reverse()
            self.assertFalse(verify_manifest(root, manifest))

    def test_empty_manifest_never_verifies_as_backup(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            empty = snapshot_manifest(root, [])
            self.assertEqual(empty["entries"], [])
            self.assertFalse(verify_manifest(root, empty))

    def test_copy_audit_rejects_same_and_nested_trees(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            source = base / "source"
            nested = source / "nested"
            other = base / "other"
            for tree in (source, nested, other):
                tree.mkdir(parents=True, exist_ok=True)
                (tree / "sample.txt").write_text("fixture")
            for destination in (source, nested):
                with self.subTest(destination=destination), self.assertRaises(ValueError):
                    compare_copy(source, destination, ["sample.txt"])
                with self.subTest(restore=destination), self.assertRaises(ValueError):
                    verify_sandbox_restore(source, destination, ["sample.txt"])
            self.assertTrue(compare_copy(source, other, ["sample.txt"]))

    def test_copy_audit_rejects_empty_names_and_symlink_root(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            source, destination = base / "source", base / "destination"
            source.mkdir()
            destination.mkdir()
            (source / "sample.txt").write_text("fixture")
            (destination / "sample.txt").write_text("fixture")
            alias = base / "alias"
            alias.symlink_to(source, target_is_directory=True)
            with self.assertRaises(ValueError):
                compare_copy(source, destination, [])
            with self.assertRaises(ValueError):
                compare_copy(alias, destination, ["sample.txt"])

    def test_three_tree_restore_rejects_hard_linked_backup_or_restore(self):
        import os
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            roots = [base / name for name in ("source", "backup", "restored")]
            for root in roots:
                root.mkdir()
                (root / "sample.txt").write_text("fixture")
            (roots[1] / "sample.txt").unlink()
            os.link(roots[0] / "sample.txt", roots[1] / "sample.txt")
            with self.assertRaises(ValueError):
                verify_independent_restore(*roots, ["sample.txt"])
            (roots[1] / "sample.txt").unlink()
            (roots[1] / "sample.txt").write_text("fixture")
            (roots[2] / "sample.txt").unlink()
            os.link(roots[1] / "sample.txt", roots[2] / "sample.txt")
            with self.assertRaises(ValueError):
                verify_independent_restore(*roots, ["sample.txt"])

    def test_two_tree_copy_rejects_hard_linked_file(self):
        import os
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            source, destination = base / "source", base / "destination"
            source.mkdir()
            destination.mkdir()
            (source / "sample.txt").write_text("fixture")
            os.link(source / "sample.txt", destination / "sample.txt")
            with self.assertRaises(ValueError):
                compare_copy(source, destination, ["sample.txt"])
            with self.assertRaises(ValueError):
                verify_sandbox_restore(source, destination, ["sample.txt"])
            (destination / "sample.txt").unlink()
            (destination / "sample.txt").write_text("fixture")
            self.assertTrue(compare_copy(source, destination, ["sample.txt"]))

    def test_sandbox_restore_copies_bytes_and_preserves_backup(self):
        from madsc.backup import restore_to_new_sandbox
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            backup = base / "backup"
            backup.mkdir()
            (backup / "nested").mkdir()
            (backup / "nested" / "channel.txt").write_bytes(b"channel-data")
            destination = base / "restored"
            report = restore_to_new_sandbox(backup, destination, ["nested/channel.txt"])
            self.assertTrue(report["sandbox_restore_matches"])
            self.assertEqual(report["files_restored"], 1)
            self.assertEqual((destination / "nested" / "channel.txt").read_bytes(), b"channel-data")
            self.assertFalse(report["production_writes"])
            self.assertFalse(report["external_storage_proven"])
            self.assertFalse(report["production_restore_verified"])
            self.assertEqual((backup / "nested" / "channel.txt").read_bytes(), b"channel-data")

    def test_sandbox_restore_never_overwrites_existing_destination(self):
        from madsc.backup import restore_to_new_sandbox
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            backup, destination = base / "backup", base / "existing"
            backup.mkdir()
            destination.mkdir()
            (backup / "file.txt").write_text("backup")
            (destination / "file.txt").write_text("untouched")
            with self.assertRaises(ValueError):
                restore_to_new_sandbox(backup, destination, ["file.txt"])
            self.assertEqual((destination / "file.txt").read_text(), "untouched")

    def test_sandbox_restore_rejects_nested_destination(self):
        from madsc.backup import restore_to_new_sandbox
        with tempfile.TemporaryDirectory() as d:
            backup = Path(d) / "backup"
            backup.mkdir()
            (backup / "file.txt").write_text("fixture")
            with self.assertRaises(ValueError):
                restore_to_new_sandbox(backup, backup / "nested", ["file.txt"])
            self.assertFalse((backup / "nested").exists())

    def test_restore_rejects_symlinked_ancestor_without_writing(self):
        from madsc.backup import restore_to_new_sandbox
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            backup = base / "backup"
            backup.mkdir()
            (backup / "file.txt").write_text("fixture")
            real_parent = base / "real"
            real_parent.mkdir()
            alias = base / "alias"
            alias.symlink_to(real_parent, target_is_directory=True)
            target = alias / "nested" / "restore"
            (real_parent / "nested").mkdir()
            with self.assertRaises(ValueError):
                restore_to_new_sandbox(backup, target, ["file.txt"])
            self.assertFalse((real_parent / "nested" / "restore").exists())

    def test_real_sandbox_backup_restore_roundtrip(self):
        from madsc.backup import backup_to_new_sandbox, restore_to_new_sandbox
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            source, backup, restored = (base / name for name in ("source", "backup", "restored"))
            source.mkdir()
            (source / "nested").mkdir()
            (source / "nested" / "channel.txt").write_bytes(b"channel-bytes")
            (source / "guide.xml").write_bytes(b"<tv/>")
            names = ["nested/channel.txt", "guide.xml"]
            backup_report = backup_to_new_sandbox(source, backup, names)
            restore_report = restore_to_new_sandbox(backup, restored, names)
            self.assertTrue(backup_report["sandbox_backup_matches"])
            self.assertTrue(restore_report["sandbox_restore_matches"])
            audit = verify_independent_restore(source, backup, restored, names)
            self.assertTrue(audit["independent_sandbox_restore_matches"])
            self.assertEqual(audit["files_checked"], 2)
            self.assertFalse(audit["external_storage_proven"])
            self.assertFalse(backup_report["production_writes"])
            self.assertEqual((source / "guide.xml").read_bytes(), b"<tv/>")

    def test_real_sandbox_backup_never_overwrites_or_nests(self):
        from madsc.backup import backup_to_new_sandbox
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            source = base / "source"
            source.mkdir()
            (source / "file.txt").write_text("source")
            existing = base / "existing"
            existing.mkdir()
            (existing / "file.txt").write_text("keep")
            with self.assertRaises(ValueError):
                backup_to_new_sandbox(source, existing, ["file.txt"])
            self.assertEqual((existing / "file.txt").read_text(), "keep")
            with self.assertRaises(ValueError):
                backup_to_new_sandbox(source, source / "nested", ["file.txt"])
            self.assertFalse((source / "nested").exists())

    def test_sandbox_backup_rolls_back_when_integrity_check_fails(self):
        from unittest.mock import patch
        from madsc.backup import backup_to_new_sandbox
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source, backup = root / "source", root / "backup"
            source.mkdir()
            (source / "safe.txt").write_bytes(b"original")
            with patch("madsc.backup.verify_manifest", return_value=False):
                with self.assertRaises(ValueError):
                    backup_to_new_sandbox(source, backup, ["safe.txt"])
            self.assertFalse(backup.exists())
            self.assertEqual((source / "safe.txt").read_bytes(), b"original")

    def test_sandbox_restore_rolls_back_when_integrity_check_fails(self):
        from unittest.mock import patch
        from madsc.backup import restore_to_new_sandbox
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            backup, restored = root / "backup", root / "restored"
            backup.mkdir()
            (backup / "safe.txt").write_bytes(b"original")
            with patch("madsc.backup.verify_manifest", return_value=False):
                with self.assertRaises(ValueError):
                    restore_to_new_sandbox(backup, restored, ["safe.txt"])
            self.assertFalse(restored.exists())
            self.assertEqual((backup / "safe.txt").read_bytes(), b"original")

    def test_copy_audit_rejects_traversal_before_inode_probe(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            source, destination = base / "source", base / "destination"
            source.mkdir()
            destination.mkdir()
            with self.assertRaises(ValueError):
                compare_copy(source, destination, ["../outside"])

    def test_three_tree_restore_rejects_traversal_before_inode_probe(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            roots = [base / name for name in ("source", "backup", "restored")]
            for root in roots:
                root.mkdir()
            # The invalid name must be rejected by the manifest validator,
            # not by an unvalidated file metadata lookup.
            with self.assertRaises(ValueError):
                verify_independent_restore(*roots, ["../outside"])

    def test_backup_rejects_symlinked_source_ancestor(self):
        from madsc.backup import backup_to_new_sandbox
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            real = base / "real"
            real.mkdir()
            source = real / "source"
            source.mkdir()
            (source / "file.txt").write_text("fixture")
            alias = base / "alias"
            alias.symlink_to(real, target_is_directory=True)
            destination = base / "new-backup"
            with self.assertRaises(ValueError):
                backup_to_new_sandbox(alias / "source", destination, ["file.txt"])
            self.assertFalse(destination.exists())

    def test_restore_rejects_symlinked_source_ancestor(self):
        from madsc.backup import restore_to_new_sandbox
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            real = base / "real"
            real.mkdir()
            backup = real / "backup"
            backup.mkdir()
            (backup / "file.txt").write_text("fixture")
            alias = base / "alias"
            alias.symlink_to(real, target_is_directory=True)
            destination = base / "new-restore"
            with self.assertRaises(ValueError):
                restore_to_new_sandbox(alias / "backup", destination, ["file.txt"])
            self.assertFalse(destination.exists())

    def test_backup_detects_source_mutation_during_copy(self):
        from unittest.mock import patch
        from madsc.backup import backup_to_new_sandbox
        import shutil
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source, destination = root / "source", root / "backup"
            source.mkdir()
            file = source / "file.txt"
            file.write_bytes(b"original")
            original_copy = shutil.copyfileobj

            def mutate_after_copy(reader, writer, length=0):
                original_copy(reader, writer, length)
                file.write_bytes(b"changed")

            with patch("shutil.copyfileobj", side_effect=mutate_after_copy):
                with self.assertRaises(ValueError):
                    backup_to_new_sandbox(source, destination, ["file.txt"])
            self.assertFalse(destination.exists())

    def test_restore_detects_backup_mutation_during_copy(self):
        from unittest.mock import patch
        from madsc.backup import restore_to_new_sandbox
        import shutil
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            backup, destination = root / "backup", root / "restored"
            backup.mkdir()
            file = backup / "file.txt"
            file.write_bytes(b"original")
            original_copy = shutil.copyfileobj

            def mutate_after_copy(reader, writer, length=0):
                original_copy(reader, writer, length)
                file.write_bytes(b"changed")

            with patch("shutil.copyfileobj", side_effect=mutate_after_copy):
                with self.assertRaises(ValueError):
                    restore_to_new_sandbox(backup, destination, ["file.txt"])
            self.assertFalse(destination.exists())

    def test_manifest_rejects_hardlinked_source_file(self):
        import os
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / "original.txt"
            original.write_bytes(b"shared")
            os.link(original, root / "alias.txt")
            with self.assertRaises(ValueError):
                snapshot_manifest(root, ["original.txt"])

    def test_backup_rejects_hardlinked_source_without_output(self):
        import os
        from madsc.backup import backup_to_new_sandbox
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "source"
            source.mkdir()
            file = source / "file.txt"
            file.write_bytes(b"shared")
            os.link(file, base / "other.txt")
            destination = base / "backup"
            with self.assertRaises(ValueError):
                backup_to_new_sandbox(source, destination, ["file.txt"])
            self.assertFalse(destination.exists())

    def test_manifest_uses_open_file_descriptor_metadata(self):
        import os
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "file.txt").write_bytes(b"descriptor")
            with patch("madsc.backup.os.fstat", wraps=os.fstat) as checked:
                result = snapshot_manifest(root, ["file.txt"])
            self.assertEqual(result["entries"][0]["bytes"], len(b"descriptor"))
            self.assertTrue(checked.called)

    def test_manifest_rejects_symlinked_root_ancestor(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            real = base / "real"
            root = real / "backup"
            root.mkdir(parents=True)
            (root / "file.txt").write_text("fixture", encoding="utf-8")
            alias = base / "alias"
            alias.symlink_to(real, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "ancestors"):
                snapshot_manifest(alias / "backup", ["file.txt"])

    def test_backup_rollback_preserves_replaced_destination_directory(self):
        from unittest.mock import patch
        from madsc.backup import backup_to_new_sandbox
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source, destination = root / "source", root / "backup"
            source.mkdir()
            (source / "file.txt").write_text("original", encoding="utf-8")
            def replace_destination(*_args):
                moved = root / "original-created-backup"
                destination.rename(moved)
                destination.mkdir()
                (destination / "keep.txt").write_text("concurrent", encoding="utf-8")
                return False
            with patch("madsc.backup.verify_manifest", side_effect=replace_destination):
                with self.assertRaises(ValueError):
                    backup_to_new_sandbox(source, destination, ["file.txt"])
            self.assertEqual((destination / "keep.txt").read_text(encoding="utf-8"), "concurrent")
            self.assertEqual((source / "file.txt").read_text(encoding="utf-8"), "original")

    def test_restore_rollback_preserves_replaced_destination_directory(self):
        from unittest.mock import patch
        from madsc.backup import restore_to_new_sandbox
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            backup, destination = root / "backup", root / "restored"
            backup.mkdir()
            (backup / "file.txt").write_text("original", encoding="utf-8")
            def replace_destination(*_args):
                moved = root / "original-created-restore"
                destination.rename(moved)
                destination.mkdir()
                (destination / "keep.txt").write_text("concurrent", encoding="utf-8")
                return False
            with patch("madsc.backup.verify_manifest", side_effect=replace_destination):
                with self.assertRaises(ValueError):
                    restore_to_new_sandbox(backup, destination, ["file.txt"])
            self.assertEqual((destination / "keep.txt").read_text(encoding="utf-8"), "concurrent")
            self.assertEqual((backup / "file.txt").read_text(encoding="utf-8"), "original")

    def test_manifest_openat_rejects_symlinked_final_component(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            real = root / "real.txt"
            real.write_text("safe", encoding="utf-8")
            (root / "alias.txt").symlink_to(real)
            with self.assertRaises(ValueError):
                snapshot_manifest(root, ["alias.txt"])

    def test_manifest_openat_rejects_symlinked_intermediate_component(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            real_dir = root / "real"
            real_dir.mkdir()
            (real_dir / "file.txt").write_text("safe", encoding="utf-8")
            (root / "alias").symlink_to(real_dir, target_is_directory=True)
            with self.assertRaises(ValueError):
                snapshot_manifest(root, ["alias/file.txt"])

    def test_manifest_keeps_requested_relative_path_for_nested_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "nested"
            nested.mkdir()
            (nested / "file.txt").write_text("safe", encoding="utf-8")
            manifest = snapshot_manifest(root, ["nested/file.txt"])
            self.assertEqual(manifest["entries"][0]["path"], "nested/file.txt")

    def test_manifest_refuses_missing_nofollow_support(self):
        import os
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "file.txt").write_bytes(b"fixture")
            with patch.object(os, "O_NOFOLLOW", None, create=True):
                with self.assertRaisesRegex(ValueError, "Secure no-follow"):
                    snapshot_manifest(root, ["file.txt"])

    def test_backup_copy_rejects_source_symlink_swapped_after_manifest(self):
        from unittest.mock import patch
        from madsc import backup as module
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            original = source / "file.txt"
            original.write_bytes(b"original")
            external = root / "external.txt"
            external.write_bytes(b"private")
            destination = root / "new-backup"
            real_open = module._open_relative_file_nofollow
            calls = []

            def switch_before_copy(base, parts):
                calls.append(1)
                if len(calls) == 2:
                    original.rename(source / "held.txt")
                    original.symlink_to(external)
                return real_open(base, parts)

            with patch("madsc.backup._open_relative_file_nofollow",
                       side_effect=switch_before_copy):
                with self.assertRaises(OSError):
                    module.backup_to_new_sandbox(source, destination, ["file.txt"])
            self.assertFalse(destination.exists())
            self.assertEqual(external.read_bytes(), b"private")

    def test_restore_copy_rejects_backup_symlink_swapped_after_manifest(self):
        from unittest.mock import patch
        from madsc import backup as module
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            backup = root / "backup"
            backup.mkdir()
            original = backup / "file.txt"
            original.write_bytes(b"original")
            external = root / "external.txt"
            external.write_bytes(b"private")
            destination = root / "new-restore"
            real_open = module._open_relative_file_nofollow
            calls = []

            def switch_before_copy(base, parts):
                calls.append(1)
                if len(calls) == 2:
                    original.rename(backup / "held.txt")
                    original.symlink_to(external)
                return real_open(base, parts)

            with patch("madsc.backup._open_relative_file_nofollow",
                       side_effect=switch_before_copy):
                with self.assertRaises(OSError):
                    module.restore_to_new_sandbox(backup, destination, ["file.txt"])
            self.assertFalse(destination.exists())
            self.assertEqual(external.read_bytes(), b"private")
