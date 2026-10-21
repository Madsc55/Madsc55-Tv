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

    def test_original_manifest_still_verifies(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "good.txt").write_text("ok")
            self.assertTrue(verify_manifest(root, snapshot_manifest(root, ["good.txt"])))


if __name__ == "__main__":
    unittest.main()
