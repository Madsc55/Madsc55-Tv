import tempfile
import unittest
from pathlib import Path

from madsc.k1_immutability_evidence import snapshot, compare


class K1ImmutabilityEvidenceTests(unittest.TestCase):
    def test_unchanged_and_modified_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            protected = root / "production.m3u"
            protected.write_bytes(b"original")
            before = snapshot(root, ["production.m3u"])
            self.assertTrue(compare(before, snapshot(root, ["production.m3u"]))["unchanged"])
            protected.write_bytes(b"modified")
            self.assertFalse(compare(before, snapshot(root, ["production.m3u"]))["unchanged"])

    def test_symlink_and_traversal_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "real").write_bytes(b"x")
            (root / "link").symlink_to(root / "real")
            for item in ("link", "../escape", "/etc/passwd"):
                with self.subTest(item=item), self.assertRaises(ValueError):
                    snapshot(root, [item])

    def test_missing_and_duplicate_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "x").write_bytes(b"x")
            with self.assertRaises(ValueError):
                snapshot(root, ["missing"])
            with self.assertRaises(ValueError):
                snapshot(root, ["x", "x"])

    def test_root_symlink_and_empty_snapshot_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "root"
            root.mkdir()
            (root / "x").write_bytes(b"safe")
            (base / "alias").symlink_to(root, target_is_directory=True)
            with self.assertRaises(ValueError):
                snapshot(base / "alias", ["x"])
            before = snapshot(root, ["x"])
            with self.assertRaises(ValueError):
                compare(before, {"schema": before["schema"], "root": before["root"], "files": []})
            duplicate = {**before, "files": before["files"] * 2}
            with self.assertRaises(ValueError):
                compare(before, duplicate)
