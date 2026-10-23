"""K4 portable directory alias regression tests."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from madsc.backup import snapshot_manifest, verify_manifest


class PortableDirectoryAliasTests(unittest.TestCase):
    def test_snapshot_rejects_directory_alias_before_file_open(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for names in (["Folder/a.txt", "folder/b.txt"],
                          ["ﬁles/a.txt", "files/b.txt"],
                          ["root/Folder/a.txt", "root/folder/b.txt"],
                          ["root/ﬁles/a.txt", "root/files/b.txt"],
                          ["file", "FILE/child.txt"],
                          ["root/file", "root/FILE/child.txt"]):
                with self.subTest(names=names):
                    with patch("madsc.backup._open_relative_file_nofollow") as opener:
                        with self.assertRaisesRegex(ValueError, "directory alias|file-directory collision"):
                            snapshot_manifest(root, names)
                        opener.assert_not_called()

    def test_manifest_rejects_directory_alias_before_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for names in (["Folder/a.txt", "folder/b.txt"],
                          ["file", "FILE/child.txt"]):
                entries = [{"path": name, "bytes": 0, "sha256": "0" * 64}
                           for name in sorted(names)]
                with self.subTest(names=names):
                    with patch("madsc.backup.snapshot_manifest") as snapshot:
                        with self.assertRaisesRegex(ValueError, "directory alias|file-directory collision"):
                            verify_manifest(root, {"entries": entries})
                        snapshot.assert_not_called()


if __name__ == "__main__":
    unittest.main()
