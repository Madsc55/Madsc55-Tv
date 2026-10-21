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
