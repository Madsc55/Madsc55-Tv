import hashlib
import os
import tempfile
import unittest
from pathlib import Path

from madsc.k2_artifact_integrity import verify_artifact_bytes


class K2ArtifactIntegrityTests(unittest.TestCase):
    def test_matching_and_mismatching_bytes_never_approve(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "artifact.bin"
            path.write_bytes(b"same fixture input")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            result = verify_artifact_bytes(path, digest)
            self.assertTrue(result["digest_matches"])
            self.assertFalse(result["execution_origin_verified"])
            self.assertFalse(result["behavioral_parity_accepted"])
            self.assertFalse(verify_artifact_bytes(path, "0" * 64)["digest_matches"])

    def test_invalid_digest_and_limits_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "a"
            path.write_bytes(b"1234")
            for digest in ("BAD", "A" * 64, None):
                with self.subTest(digest=digest), self.assertRaises(ValueError):
                    verify_artifact_bytes(path, digest)
            with self.assertRaises(ValueError):
                verify_artifact_bytes(path, "0" * 64, max_bytes=3)
            for limit in (True, 0, 64_000_001):
                with self.subTest(limit=limit), self.assertRaises(ValueError):
                    verify_artifact_bytes(path, "0" * 64, max_bytes=limit)

    def test_symlinks_hardlinks_and_directories_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            original = root / "original"
            original.write_bytes(b"test")
            alias = root / "hardlink"
            os.link(original, alias)
            with self.assertRaises(ValueError):
                verify_artifact_bytes(original, "0" * 64)
            link = root / "symlink"
            link.symlink_to(original)
            with self.assertRaises((OSError, ValueError)):
                verify_artifact_bytes(link, "0" * 64)
            with self.assertRaises(ValueError):
                verify_artifact_bytes(root, "0" * 64)


    def test_empty_file_and_exact_boundary(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "empty"
            path.write_bytes(b"")
            expected = hashlib.sha256(b"").hexdigest()
            result = verify_artifact_bytes(path, expected, max_bytes=1)
            self.assertTrue(result["digest_matches"])
            self.assertEqual(result["bytes"], 0)
            path.write_bytes(b"abcd")
            result = verify_artifact_bytes(
                path, hashlib.sha256(b"abcd").hexdigest(), max_bytes=4
            )
            self.assertTrue(result["digest_matches"])
            self.assertEqual(result["bytes"], 4)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX FIFO support required")
    def test_fifo_rejected_without_waiting_for_writer(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "pipe"
            os.mkfifo(path)
            with self.assertRaises(ValueError):
                verify_artifact_bytes(path, "0" * 64)



if __name__ == "__main__":
    unittest.main()
