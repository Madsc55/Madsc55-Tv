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

    def test_export_bytes_end_with_one_real_newline(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            export_6115_archive_manifest(self.urls, destination)
            payload = (destination / "ibo_6115_archive_preview.json").read_bytes()
            self.assertTrue(payload.endswith(bytes([10])))
            self.assertFalse(payload.endswith(bytes([92, 110])))
            self.assertEqual(payload.count(bytes([10, 10])), 0)

    def test_malformed_https_ports_fail_before_destination_creation(self):
        with TemporaryDirectory() as tmp:
            for invalid in ("https://example.invalid:bad/live",
                            "https://example.invalid:65536/live",
                            "https://example.invalid:0/live"):
                with self.subTest(invalid=invalid):
                    destination = Path(tmp) / "isolated-ibo"
                    urls = self.urls.copy()
                    urls[0] = invalid
                    with self.assertRaises(ValueError):
                        export_6115_archive_manifest(urls, destination)
                    self.assertFalse(destination.exists())

    def test_bad_input_creates_no_directory(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            with self.assertRaises(ValueError):
                export_6115_archive_manifest(self.urls[:-1], destination)
            self.assertFalse(destination.exists())

    def test_readback_mismatch_removes_manifest_and_directory(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            original = json.loads
            def tamper_readback(payload, *args, **kwargs):
                result = original(payload, *args, **kwargs)
                if isinstance(result, dict) and "source_count" in result:
                    result["source_count"] = -1
                return result
            with patch("madsc.isolated_ibo_archive_export.json.loads", side_effect=tamper_readback):
                with self.assertRaisesRegex(OSError, "readback mismatch"):
                    export_6115_archive_manifest(self.urls, destination)
            self.assertFalse(destination.exists())

    def test_corrupted_disk_bytes_trigger_cleanup(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            original = Path.read_bytes
            def corrupted_read(path):
                payload = original(path)
                if path.name == "ibo_6115_archive_preview.json":
                    return payload.replace(b'"source_count": 6115', b'"source_count": 6114')
                return payload
            with patch("madsc.isolated_ibo_archive_export.Path.read_bytes", autospec=True, side_effect=corrupted_read):
                with self.assertRaisesRegex(OSError, "readback mismatch"):
                    export_6115_archive_manifest(self.urls, destination)
            self.assertFalse(destination.exists())

    def test_partial_serialization_failure_rolls_back(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            def serialization_failure(obj, **kwargs):
                raise OSError("fixture serialization failure")
            with patch("madsc.isolated_ibo_archive_export.json.dumps", side_effect=serialization_failure):
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
