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


    def test_path_replacement_during_hashing_is_rejected(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "artifact"
            path.write_bytes(b"original")
            digest = hashlib.sha256(b"original").hexdigest()
            real_stat = os.stat
            replaced = False

            def swapping_stat(target, *args, **kwargs):
                nonlocal replaced
                if not replaced and str(target) == str(path):
                    replaced = True
                    path.rename(Path(folder) / "moved")
                    path.write_bytes(b"replacement")
                return real_stat(target, *args, **kwargs)

            with patch("os.stat", side_effect=swapping_stat):
                with self.assertRaises(ValueError):
                    verify_artifact_bytes(path, digest)
            self.assertTrue(replaced)

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



class K2ArtifactParentPathTests(unittest.TestCase):

    def test_parent_traversal_rejected_before_open(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "artifact").write_bytes(b"safe")
            expected = hashlib.sha256(b"safe").hexdigest()
            with self.assertRaises(ValueError):
                verify_artifact_bytes(root / "subdir" / ".." / "artifact", expected)

    def test_symlinked_parent_directory_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            actual = root / "actual"
            actual.mkdir()
            (actual / "artifact").write_bytes(b"sample")
            alias = root / "alias"
            alias.symlink_to(actual, target_is_directory=True)
            with self.assertRaises(ValueError):
                verify_artifact_bytes(alias / "artifact", hashlib.sha256(b"sample").hexdigest())


class K2ArtifactPairTests(unittest.TestCase):
    def test_equal_bytes_still_not_behavioral_acceptance(self):
        from madsc.k2_artifact_integrity import compare_artifact_pair
        with tempfile.TemporaryDirectory() as folder:
            first = Path(folder) / "legacy"
            second = Path(folder) / "replacement"
            first.write_bytes(b"evidence")
            second.write_bytes(b"evidence")
            digest = hashlib.sha256(b"evidence").hexdigest()
            result = compare_artifact_pair(first, second, digest, digest)
            self.assertTrue(result["artifact_bytes_match"])
            self.assertFalse(result["independent_origin_api_verified"])
            self.assertFalse(result["behavioral_parity_accepted"])
            self.assertFalse(result["production_ready"])

    def test_alias_paths_to_same_file_are_rejected(self):
        from madsc.k2_artifact_integrity import compare_artifact_pair
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "artifact"
            path.write_bytes(b"same inode")
            digest = hashlib.sha256(b"same inode").hexdigest()
            with self.assertRaises(ValueError):
                compare_artifact_pair(path, root / "." / "artifact", digest, digest)
            alias = root / "symlink"
            alias.symlink_to(path)
            with self.assertRaises(ValueError):
                compare_artifact_pair(path, alias, digest, digest)
            hardlink = root / "hardlink"
            os.link(path, hardlink)
            with self.assertRaises(ValueError):
                compare_artifact_pair(path, hardlink, digest, digest)

    def test_mismatch_and_forged_expected_hash_rejected(self):
        from madsc.k2_artifact_integrity import compare_artifact_pair
        with tempfile.TemporaryDirectory() as folder:
            first = Path(folder) / "legacy"
            second = Path(folder) / "replacement"
            first.write_bytes(b"a")
            second.write_bytes(b"b")
            a = hashlib.sha256(b"a").hexdigest()
            b = hashlib.sha256(b"b").hexdigest()
            self.assertFalse(compare_artifact_pair(first, second, a, b)["artifact_bytes_match"])
            with self.assertRaises(ValueError):
                compare_artifact_pair(first, second, a, a)
            with self.assertRaises(ValueError):
                compare_artifact_pair(first, first, a, a)


class K2PinnedLegacySourceTests(unittest.TestCase):
    def test_entire_pinned_workflow_inventory_is_well_formed(self):
        import json
        import re
        scope_path = Path(__file__).resolve().parents[1] / "docs" / "LEGACY_SOURCE_SCOPE.json"
        scope = json.loads(scope_path.read_text(encoding="utf-8"))
        self.assertEqual(scope["source_repository"], "Madsc55/madsc-tv")
        self.assertEqual(len(scope["workflows"]), 99)
        paths = []
        for entry in scope["workflows"]:
            path = entry["path"]
            paths.append(path)
            with self.subTest(path=path):
                self.assertTrue(path.startswith(".github/workflows/"))
                self.assertTrue(path.endswith((".yml", ".yaml")))
                self.assertNotIn("..", Path(path).parts)
                self.assertRegex(entry["git_blob_sha"], r"^[0-9a-f]{40}$")
                self.assertIsInstance(entry["bytes"], int)
                self.assertGreater(entry["bytes"], 0)
        self.assertEqual(len(set(paths)), len(paths))

    def test_three_reviewed_workflows_have_pinned_source_blobs(self):
        import json
        scope_path = Path(__file__).resolve().parents[1] / "docs" / "LEGACY_SOURCE_SCOPE.json"
        scope = json.loads(scope_path.read_text(encoding="utf-8"))
        self.assertEqual(scope["source_commit"], "ca374df3b9585c0d76a078db9536150ebbc260f7")
        blobs = {row["path"]: row["git_blob_sha"] for row in scope["workflows"]}
        self.assertEqual(len(blobs), 99)
        expected = {
            ".github/workflows/390-aday-tekrar-test.yml":
                "b12f53a17434fe719a65edfdc968f675e1f16b95",
            ".github/workflows/aday-bekletme.yml":
                "68564680a2c32b11d1c5ed78825f01c85d0378e8",
            ".github/workflows/aday-logo-epg-test.yml":
                "21214309014625c4a63f00ee16c9017efac6b0a7",
        }
        for path, blob in expected.items():
            with self.subTest(path=path):
                self.assertEqual(blobs.get(path), blob)

if __name__ == "__main__":
    unittest.main()
