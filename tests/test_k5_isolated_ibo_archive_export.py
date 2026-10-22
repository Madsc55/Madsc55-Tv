"""K5 offline tests for create-only isolated IBO archive evidence."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest

from madsc.isolated_ibo_archive_export import export_6115_archive_manifest


class K5IboArchiveExportTests(unittest.TestCase):
    def setUp(self):
        self.urls = [f"https://example.invalid/fixture/{i}" for i in range(6115)]

    def test_success_creates_only_manifest_in_fresh_directory(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            destination = root / "isolated-ibo"
            result = export_6115_archive_manifest(self.urls, destination)
            self.assertEqual(json.loads((destination / "ibo_6115_archive_preview.json").read_text()), result)
            self.assertEqual([p.name for p in destination.iterdir()], ["ibo_6115_archive_preview.json"])
            self.assertFalse(result["production_writes"])
            with self.assertRaises(FileExistsError):
                export_6115_archive_manifest(self.urls, destination)

    def test_bad_input_creates_no_directory(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            with self.assertRaises(ValueError):
                export_6115_archive_manifest(self.urls[:-1], destination)
            self.assertFalse(destination.exists())

    def test_partial_serialization_failure_rolls_back(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            def partial_failure(obj, handle, **kwargs):
                handle.write('{"partial":')
                raise OSError("fixture serialization failure")
            with patch("madsc.isolated_ibo_archive_export.json.dump", side_effect=partial_failure):
                with self.assertRaisesRegex(OSError, "fixture serialization failure"):
                    export_6115_archive_manifest(self.urls, destination)
            self.assertFalse(destination.exists())

    def test_root_and_dot_destinations_fail_without_writing(self):
        with TemporaryDirectory() as tmp:
            with self.assertRaises((PermissionError, FileExistsError)):
                export_6115_archive_manifest(self.urls, Path(tmp) / ".")
            with self.assertRaises((PermissionError, FileExistsError)):
                export_6115_archive_manifest(self.urls, Path("/"))
            self.assertFalse((Path(tmp) / "ibo_6115_archive_preview.json").exists())

    def test_symlink_parent_and_protected_destination_rejected(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "real").mkdir()
            (root / "alias").symlink_to(root / "real", target_is_directory=True)
            with self.assertRaises(PermissionError):
                export_6115_archive_manifest(self.urls, root / "alias" / "preview")
            with self.assertRaises(PermissionError):
                export_6115_archive_manifest(self.urls, root / "FAVORILER")
            self.assertFalse((root / "FAVORILER").exists())


if __name__ == "__main__":
    unittest.main()
