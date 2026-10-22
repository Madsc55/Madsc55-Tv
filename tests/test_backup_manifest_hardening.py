import hashlib
import tempfile
import unittest
from pathlib import Path

from madsc.backup import snapshot_manifest, verify_manifest


class BackupManifestHardeningTests(unittest.TestCase):
    def test_control_character_in_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.txt").write_text("ok")
            with self.assertRaises(ValueError):
                snapshot_manifest(root, ["bad\nname.txt"])

    def test_duplicate_manifest_entries_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.txt").write_text("ok")
            manifest = snapshot_manifest(root, ["good.txt"])
            manifest["entries"].append(dict(manifest["entries"][0]))
            with self.assertRaises(ValueError):
                verify_manifest(root, manifest)

    def test_multichunk_file_hash_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = b"test-pattern-" * 200000
            (root / "large.bin").write_bytes(payload)
            manifest = snapshot_manifest(root, ["large.bin"])
            self.assertEqual(manifest["entries"][0]["bytes"], len(payload))
            self.assertEqual(manifest["entries"][0]["sha256"], hashlib.sha256(payload).hexdigest())
            self.assertTrue(verify_manifest(root, manifest))
            with (root / "large.bin").open("r+b") as handle:
                handle.seek(1024 * 1024 + 7)
                handle.write(b"!")
            self.assertFalse(verify_manifest(root, manifest))

    def test_change_during_manifest_read_fails_closed(self):
        import os
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "stable.bin"
            target.write_bytes(b"stable-data")
            original_fstat = os.fstat
            observations = []

            def mutate_on_second_stat(fd):
                if len(observations) == 1:
                    # Same inode and byte count, but a changed source timestamp.
                    original = original_fstat(fd)
                    os.utime(target, ns=(original.st_atime_ns,
                                         original.st_mtime_ns + 1_000_000_000))
                observations.append(fd)
                return original_fstat(fd)

            with patch("madsc.backup.os.fstat", side_effect=mutate_on_second_stat):
                with self.assertRaisesRegex(ValueError, "changed during manifest read"):
                    snapshot_manifest(root, ["stable.bin"])
            self.assertEqual(len(observations), 2)

    def test_copy_inode_audit_rejects_symlink_swap_after_snapshots(self):
        from unittest.mock import patch
        from madsc import backup as module
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source, target = base / "source", base / "target"
            source.mkdir()
            target.mkdir()
            (source / "file.bin").write_bytes(b"original")
            (target / "file.bin").write_bytes(b"original")
            outside = base / "outside.bin"
            outside.write_bytes(b"secret")
            original_snapshot = module.snapshot_manifest
            calls = []

            def swap_after_snapshots(root, names):
                result = original_snapshot(root, names)
                calls.append(root)
                if len(calls) == 2:
                    (target / "file.bin").unlink()
                    (target / "file.bin").symlink_to(outside)
                return result

            with patch("madsc.backup.snapshot_manifest", side_effect=swap_after_snapshots):
                with self.assertRaises(OSError):
                    module.compare_copy(source, target, ["file.bin"])
            self.assertEqual(outside.read_bytes(), b"secret")

    def test_three_tree_inode_audit_rejects_symlink_swap(self):
        from unittest.mock import patch
        from madsc import backup as module
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            roots = [base / name for name in ("source", "backup", "restore")]
            for root in roots:
                root.mkdir()
                (root / "file.bin").write_bytes(b"original")
            outside = base / "outside.bin"
            outside.write_bytes(b"secret")
            original_snapshot = module.snapshot_manifest
            calls = []

            def swap_after_snapshots(root, names):
                result = original_snapshot(root, names)
                calls.append(root)
                if len(calls) == 3:
                    (roots[2] / "file.bin").unlink()
                    (roots[2] / "file.bin").symlink_to(outside)
                return result

            with patch("madsc.backup.snapshot_manifest", side_effect=swap_after_snapshots):
                with self.assertRaises(OSError):
                    module.verify_independent_restore(*roots, ["file.bin"])
            self.assertEqual(outside.read_bytes(), b"secret")

    def test_failed_target_creation_closes_backup_source_descriptor(self):
        import os
        from unittest.mock import patch
        from madsc import backup as module
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "source"
            source.mkdir()
            (source / "file.bin").write_bytes(b"fixture")
            destination = base / "new-backup"
            opened = []
            real_open = module._open_relative_file_nofollow

            def capture_open(root, parts):
                descriptor = real_open(root, parts)
                opened.append(descriptor)
                return descriptor

            with patch("madsc.backup._open_relative_file_nofollow", side_effect=capture_open), \
                 patch("madsc.backup._create_relative_file_nofollow",
                       side_effect=OSError("simulated target failure")):
                with self.assertRaisesRegex(OSError, "simulated target failure"):
                    module.backup_to_new_sandbox(source, destination, ["file.bin"])
            self.assertFalse(destination.exists())
            self.assertEqual(len(opened), 2)
            with self.assertRaises(OSError):
                os.fstat(opened[-1])

    def test_failed_target_creation_closes_restore_source_descriptor(self):
        import os
        from unittest.mock import patch
        from madsc import backup as module
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "source"
            source.mkdir()
            (source / "file.bin").write_bytes(b"fixture")
            destination = base / "new-restore"
            opened = []
            real_open = module._open_relative_file_nofollow

            def capture_open(root, parts):
                descriptor = real_open(root, parts)
                opened.append(descriptor)
                return descriptor

            with patch("madsc.backup._open_relative_file_nofollow", side_effect=capture_open), \
                 patch("madsc.backup._create_relative_file_nofollow",
                       side_effect=OSError("simulated target failure")):
                with self.assertRaisesRegex(OSError, "simulated target failure"):
                    module.restore_to_new_sandbox(source, destination, ["file.bin"])
            self.assertFalse(destination.exists())
            self.assertEqual(len(opened), 2)
            with self.assertRaises(OSError):
                os.fstat(opened[-1])

    def test_secure_source_open_rejects_traversal_components(self):
        from madsc import backup as module
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "safe.txt").write_bytes(b"safe")
            for parts in (("..", "outside.txt"), (".", "safe.txt"),
                          ("", "safe.txt"), ("nested/sibling",),
                          ("nested\\sibling",), ("safe.txt", "..")):
                with self.subTest(parts=parts):
                    with self.assertRaisesRegex(ValueError, "Unsafe backup source path"):
                        module._open_relative_file_nofollow(root, parts)
            self.assertEqual((root / "safe.txt").read_bytes(), b"safe")

    def test_manifest_rejects_forged_external_backup_and_restore_claims(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.txt").write_bytes(b"fixture")
            original = snapshot_manifest(root, ["good.txt"])
            self.assertTrue(verify_manifest(root, original))
            for claim in ("external_backup_verified", "restore_verified", "production_writes"):
                for forged in (True, 1, "true", None):
                    with self.subTest(claim=claim, forged=forged):
                        manifest = dict(original)
                        manifest[claim] = forged
                        with self.assertRaisesRegex(ValueError, "Unverified backup manifest attestation"):
                            verify_manifest(root, manifest)
            self.assertTrue(verify_manifest(root, original))

    def test_oversized_manifest_rejected_before_filesystem_reads(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.txt").write_bytes(b"fixture")
            original = snapshot_manifest(root, ["good.txt"])
            forged = dict(original)
            forged["entries"] = [dict(original["entries"][0]) for _ in range(10001)]
            with patch("madsc.backup.snapshot_manifest",
                       side_effect=AssertionError("must not access filesystem")):
                with self.assertRaisesRegex(ValueError, "bounded entry limit"):
                    verify_manifest(root, forged)
            self.assertTrue(verify_manifest(root, original))

    def test_manifest_rejects_oversized_path_without_reading_files(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.txt").write_bytes(b"fixture")
            original = snapshot_manifest(root, ["good.txt"])
            forged = dict(original)
            forged["entries"] = [{**original["entries"][0], "path": "x" * 4097}]
            with patch("madsc.backup.snapshot_manifest",
                       side_effect=AssertionError("unexpected filesystem access")):
                with self.assertRaisesRegex(ValueError, "bounded length"):
                    verify_manifest(root, forged)
            self.assertTrue(verify_manifest(root, original))

    def test_snapshot_rejects_oversized_source_inventory_and_path(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.txt").write_bytes(b"fixture")
            with patch("madsc.backup._open_relative_file_nofollow",
                       side_effect=AssertionError("unexpected source file read")):
                with self.assertRaisesRegex(ValueError, "bounded entry limit"):
                    snapshot_manifest(root, [f"file-{index}" for index in range(10001)])
                with self.assertRaisesRegex(ValueError, "bounded length"):
                    snapshot_manifest(root, ["x" * 4097])
            self.assertEqual(len(snapshot_manifest(root, ["good.txt"])["entries"]), 1)

    def test_manifest_rejects_forged_external_modes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.txt").write_bytes(b"fixture")
            original = snapshot_manifest(root, ["good.txt"])
            self.assertTrue(verify_manifest(root, original))
            for mode in ("external", "verified_restore", True, None, 1):
                with self.subTest(mode=mode):
                    forged = dict(original)
                    forged["mode"] = mode
                    with self.assertRaisesRegex(ValueError, "Unsupported backup manifest mode"):
                        verify_manifest(root, forged)
            self.assertTrue(verify_manifest(root, original))

    def test_manifest_mode_rejects_string_subclass(self):
        class StringSubclass(str):
            pass

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.txt").write_bytes(b"fixture")
            original = snapshot_manifest(root, ["good.txt"])
            forged = dict(original)
            forged["mode"] = StringSubclass("manifest_only")
            with self.assertRaisesRegex(ValueError, "Unsupported backup manifest mode"):
                verify_manifest(root, forged)
            self.assertTrue(verify_manifest(root, original))

    def test_manifest_rejects_controls_and_surrogates_before_file_reads(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.txt").write_bytes(b"fixture")
            original = snapshot_manifest(root, ["good.txt"])
            for invalid in ("good\x00.txt", "good\n.txt", "good\x7f.txt",
                            "good\ud800.txt", "good\udfff.txt"):
                with self.subTest(invalid=repr(invalid)):
                    forged = dict(original)
                    forged["entries"] = [{**original["entries"][0], "path": invalid}]
                    with patch("madsc.backup.snapshot_manifest",
                               side_effect=AssertionError("unexpected filesystem access")):
                        with self.assertRaisesRegex(ValueError, "Unsafe backup manifest path"):
                            verify_manifest(root, forged)
            self.assertTrue(verify_manifest(root, original))

    def test_snapshot_rejects_surrogate_source_before_file_open(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.txt").write_bytes(b"fixture")
            with patch("madsc.backup._open_relative_file_nofollow",
                       side_effect=AssertionError("unexpected source open")):
                with self.assertRaisesRegex(ValueError, "Unsafe backup source path"):
                    snapshot_manifest(root, ["good" + chr(0xD800) + ".txt"])
            self.assertEqual(len(snapshot_manifest(root, ["good.txt"])["entries"]), 1)

    def test_original_manifest_still_verifies(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.txt").write_text("ok")
            self.assertTrue(verify_manifest(root, snapshot_manifest(root, ["good.txt"])))


if __name__ == "__main__":
    unittest.main()
