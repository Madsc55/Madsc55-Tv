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

    def test_original_manifest_still_verifies(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.txt").write_text("ok")
            self.assertTrue(verify_manifest(root, snapshot_manifest(root, ["good.txt"])))


if __name__ == "__main__":
    unittest.main()
