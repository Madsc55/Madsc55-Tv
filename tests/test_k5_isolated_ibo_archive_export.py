"""K5 offline tests for create-only isolated IBO archive evidence."""
import json
import os
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

    def test_manifest_open_failure_removes_created_directory(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            real_open = os.open
            def fail_manifest_open(path, flags, *args, **kwargs):
                if Path(path).name == "ibo_6115_archive_preview.json":
                    raise OSError("fixture manifest open failure")
                return real_open(path, flags, *args, **kwargs)
            with patch("madsc.isolated_ibo_archive_export.os.open",
                       side_effect=fail_manifest_open):
                with self.assertRaisesRegex(OSError, "manifest open failure"):
                    export_6115_archive_manifest(self.urls, destination)
            self.assertFalse(destination.exists())

    def test_export_directory_has_private_permissions(self):
        if os.name != "posix":
            self.skipTest("POSIX permission bits unavailable")
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            export_6115_archive_manifest(self.urls, destination)
            self.assertEqual(destination.stat().st_mode & 0o777, 0o700)

    def test_permission_adjustment_failure_cleans_created_directory(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            original_chmod = Path.chmod
            def fail_chmod(path, mode, *args, **kwargs):
                if path == destination:
                    raise OSError("fixture chmod failure")
                return original_chmod(path, mode, *args, **kwargs)
            with patch("madsc.isolated_ibo_archive_export.Path.chmod",
                       autospec=True, side_effect=fail_chmod):
                with self.assertRaisesRegex(OSError, "chmod failure"):
                    export_6115_archive_manifest(self.urls, destination)
            self.assertFalse(destination.exists())

    def test_manifest_file_has_private_permissions(self):
        if os.name != "posix":
            self.skipTest("POSIX permission bits unavailable")
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            export_6115_archive_manifest(self.urls, destination)
            manifest = destination / "ibo_6115_archive_preview.json"
            self.assertEqual(manifest.stat().st_mode & 0o777, 0o600)

    def test_manifest_open_uses_exclusive_creation_and_nofollow(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            original_open = os.open
            observed = []
            def inspect_open(path, flags, *args, **kwargs):
                if Path(path).name == "ibo_6115_archive_preview.json":
                    observed.append(flags)
                return original_open(path, flags, *args, **kwargs)
            with patch("madsc.isolated_ibo_archive_export.os.open",
                       side_effect=inspect_open):
                export_6115_archive_manifest(self.urls, destination)
            self.assertEqual(len(observed), 1)
            self.assertTrue(observed[0] & os.O_EXCL)
            self.assertTrue(observed[0] & os.O_CREAT)
            if hasattr(os, "O_NOFOLLOW"):
                self.assertTrue(observed[0] & os.O_NOFOLLOW)

    def test_fdopen_failure_closes_descriptor_and_rolls_back(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            original_open = os.open
            opened = []
            def record_open(path, flags, *args, **kwargs):
                fd = original_open(path, flags, *args, **kwargs)
                if Path(path).name == "ibo_6115_archive_preview.json":
                    opened.append(fd)
                return fd
            with patch("madsc.isolated_ibo_archive_export.os.open", side_effect=record_open):
                with patch("madsc.isolated_ibo_archive_export.os.fdopen",
                           side_effect=OSError("fixture fdopen failure")):
                    with self.assertRaisesRegex(OSError, "fdopen failure"):
                        export_6115_archive_manifest(self.urls, destination)
            self.assertEqual(len(opened), 1)
            with self.assertRaises(OSError):
                os.fstat(opened[0])
            self.assertFalse(destination.exists())

    def test_manifest_write_failure_closes_file_and_rolls_back(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            real_fdopen = os.fdopen
            opened_handles = []
            class FailingWriter:
                def __init__(self, handle):
                    self.handle = handle
                    opened_handles.append(handle)
                def __enter__(self):
                    return self
                def __exit__(self, *args):
                    return self.handle.__exit__(*args)
                def write(self, data):
                    raise OSError("fixture write failure")
                def flush(self):
                    return self.handle.flush()
                def fileno(self):
                    return self.handle.fileno()
            def wrapped_fdopen(fd, mode):
                return FailingWriter(real_fdopen(fd, mode))
            with patch("madsc.isolated_ibo_archive_export.os.fdopen",
                       side_effect=wrapped_fdopen):
                with self.assertRaisesRegex(OSError, "write failure"):
                    export_6115_archive_manifest(self.urls, destination)
            self.assertEqual(len(opened_handles), 1)
            self.assertTrue(opened_handles[0].closed)
            self.assertFalse(destination.exists())

    def test_file_sync_failure_rolls_back(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            with patch("madsc.isolated_ibo_archive_export.os.fsync",
                       side_effect=OSError("fixture file sync failure")):
                with self.assertRaisesRegex(OSError, "file sync failure"):
                    export_6115_archive_manifest(self.urls, destination)
            self.assertFalse(destination.exists())

    def test_directory_sync_failure_rolls_back(self):
        if not hasattr(os, "O_DIRECTORY"):
            self.skipTest("Directory fsync unsupported")
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            original = os.fsync
            calls = []
            def fail_directory_sync(fd):
                calls.append(fd)
                if len(calls) == 2:
                    raise OSError("fixture directory sync failure")
                return original(fd)
            with patch("madsc.isolated_ibo_archive_export.os.fsync", side_effect=fail_directory_sync):
                with self.assertRaisesRegex(OSError, "directory sync failure"):
                    export_6115_archive_manifest(self.urls, destination)
            self.assertFalse(destination.exists())

    def test_directory_open_uses_nofollow_when_available(self):
        if not all(hasattr(os, name) for name in ("O_DIRECTORY", "O_NOFOLLOW")):
            self.skipTest("Directory nofollow unsupported")
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            real_open = os.open
            directory_flags = []
            def inspect_open(path, flags, *args, **kwargs):
                if Path(path) == destination:
                    directory_flags.append(flags)
                return real_open(path, flags, *args, **kwargs)
            with patch("madsc.isolated_ibo_archive_export.os.open", side_effect=inspect_open):
                export_6115_archive_manifest(self.urls, destination)
            self.assertEqual(len(directory_flags), 1)
            self.assertTrue(directory_flags[0] & os.O_DIRECTORY)
            self.assertTrue(directory_flags[0] & os.O_NOFOLLOW)

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

    def test_missing_parent_fails_closed_without_creating_anything(self):
        with TemporaryDirectory() as tmp:
            parent = Path(tmp) / "missing-parent"
            destination = parent / "isolated-ibo"
            with self.assertRaisesRegex(PermissionError, "parent missing"):
                export_6115_archive_manifest(self.urls, destination)
            self.assertFalse(parent.exists())
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
                with self.assertRaisesRegex(OSError, "byte integrity mismatch"):
                    export_6115_archive_manifest(self.urls, destination)
            self.assertFalse(destination.exists())

    def test_invalid_json_readback_is_rejected_by_byte_integrity_first(self):
        with TemporaryDirectory() as tmp:
            destination = Path(tmp) / "isolated-ibo"
            original = Path.read_bytes
            def invalid_readback(path):
                if path.name == "ibo_6115_archive_preview.json":
                    return b"{invalid-json"
                return original(path)
            with patch("madsc.isolated_ibo_archive_export.Path.read_bytes",
                       autospec=True, side_effect=invalid_readback):
                with self.assertRaisesRegex(OSError, "byte integrity mismatch"):
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

    def test_unsafe_destination_characters_fail_before_write(self):
        with TemporaryDirectory() as tmp:
            for suffix in ("bad" + chr(10) + "name", "bad" + chr(127) + "name",
                           "bad" + chr(0xD800) + "name"):
                destination = Path(tmp) / suffix
                with self.subTest(suffix=repr(suffix)):
                    with self.assertRaises(PermissionError):
                        export_6115_archive_manifest(self.urls, destination)
                    self.assertFalse(destination.exists())

    def test_destination_symlink_is_rejected_without_touching_target(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            real = root / "real-directory"
            real.mkdir()
            destination = root / "alias-directory"
            destination.symlink_to(real, target_is_directory=True)
            with self.assertRaises(FileExistsError):
                export_6115_archive_manifest(self.urls, destination)
            self.assertEqual(list(real.iterdir()), [])
            self.assertTrue(destination.is_symlink())

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
