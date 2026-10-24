import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from madsc.core_fixture_writer import write_core_fixture
from madsc.write_path_audit import ProtectedWriteRejected


class CoreFixtureWriterTests(unittest.TestCase):
    def test_new_fixture_fsyncs_file_and_parent_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with mock.patch("madsc.core_fixture_writer.os.fsync", wraps=os.fsync) as sync:
                write_core_fixture(root, "fixture.txt", b"durable")
            self.assertEqual(sync.call_count, 2)
            self.assertEqual((root / "fixture.txt").read_bytes(), b"durable")

    def test_allowlisted_fixture_is_created_and_explicitly_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = write_core_fixture(root, "fixture.txt", b"first")
            self.assertEqual(output.read_bytes(), b"first")
            write_core_fixture(root, "fixture.txt", b"second", overwrite=True)
            self.assertEqual(output.read_bytes(), b"second")

    def test_overwrite_fsyncs_file_and_parent_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_core_fixture(root, "fixture.txt", b"first")
            with mock.patch("madsc.core_fixture_writer.os.fsync", wraps=os.fsync) as sync:
                write_core_fixture(root, "fixture.txt", b"second", overwrite=True)
            self.assertEqual(sync.call_count, 2)
            self.assertEqual((root / "fixture.txt").read_bytes(), b"second")

    def test_failed_new_fixture_fsync_removes_partial_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            real_fsync = os.fsync
            calls = 0
            def fail_first_sync(fd):
                nonlocal calls
                calls += 1
                if calls == 1:
                    raise OSError("injected fixture sync failure")
                return real_fsync(fd)
            with mock.patch("madsc.core_fixture_writer.os.fsync", side_effect=fail_first_sync):
                with self.assertRaises(OSError):
                    write_core_fixture(root, "fixture.txt", b"partial")
            self.assertFalse((root / "fixture.txt").exists())

    def test_failed_staged_overwrite_preserves_original_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = write_core_fixture(root, "fixture.txt", b"original")
            with mock.patch("madsc.core_fixture_writer.os.replace",
                            side_effect=OSError("injected replacement failure")):
                with self.assertRaises(OSError):
                    write_core_fixture(root, "fixture.txt", b"replacement", overwrite=True)
            self.assertEqual(target.read_bytes(), b"original")
            self.assertEqual(sorted(p.name for p in root.iterdir()), ["fixture.txt"])

    def test_staged_overwrite_keeps_original_if_stage_sync_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = write_core_fixture(root, "fixture.txt", b"original")
            with mock.patch("madsc.core_fixture_writer.os.fsync",
                            side_effect=OSError("injected stage sync failure")):
                with self.assertRaises(OSError):
                    write_core_fixture(root, "fixture.txt", b"replacement", overwrite=True)
            self.assertEqual(target.read_bytes(), b"original")
            self.assertEqual(sorted(p.name for p in root.iterdir()), ["fixture.txt"])

    def test_swapped_staging_name_is_not_unlinked_on_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = write_core_fixture(root, "fixture.txt", b"original")
            real_replace = os.replace
            def swap_stage_then_fail(src, dst, **kwargs):
                staged = root / src
                staged.unlink()
                staged.write_bytes(b"attacker replacement")
                raise OSError("injected replacement failure")
            with mock.patch("madsc.core_fixture_writer.os.replace",
                            side_effect=swap_stage_then_fail):
                with self.assertRaises(OSError):
                    write_core_fixture(root, "fixture.txt", b"new", overwrite=True)
            self.assertEqual(target.read_bytes(), b"original")
            staged = [p for p in root.iterdir() if p.name.startswith(".fixture-stage-")]
            self.assertEqual(len(staged), 1)
            self.assertEqual(staged[0].read_bytes(), b"attacker replacement")

    def test_swapped_stage_before_replace_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = write_core_fixture(root, "fixture.txt", b"original")
            real_stat = os.stat
            swapped = False
            def swap_before_stat(path, *args, **kwargs):
                nonlocal swapped
                if (isinstance(path, str) and path.startswith(".fixture-stage-")
                        and not swapped):
                    swapped = True
                    (root / path).unlink()
                    (root / path).write_bytes(b"untrusted")
                return real_stat(path, *args, **kwargs)
            with mock.patch("madsc.core_fixture_writer.os.stat", side_effect=swap_before_stat):
                with self.assertRaises(PermissionError):
                    write_core_fixture(root, "fixture.txt", b"new", overwrite=True)
            self.assertTrue(swapped)
            self.assertEqual(target.read_bytes(), b"original")

    def test_symlinked_stage_before_replace_is_rejected(self):
        with (tempfile.TemporaryDirectory() as directory,
              tempfile.TemporaryDirectory() as outside):
            root = Path(directory)
            external = Path(outside) / "external.txt"
            external.write_bytes(b"external")
            target = write_core_fixture(root, "fixture.txt", b"original")
            real_stat = os.stat
            swapped = False
            def replace_stage_with_symlink(path, *args, **kwargs):
                nonlocal swapped
                if (isinstance(path, str) and path.startswith(".fixture-stage-")
                        and not swapped):
                    swapped = True
                    (root / path).unlink()
                    (root / path).symlink_to(external)
                return real_stat(path, *args, **kwargs)
            with mock.patch("madsc.core_fixture_writer.os.stat",
                            side_effect=replace_stage_with_symlink):
                with self.assertRaises(PermissionError):
                    write_core_fixture(root, "fixture.txt", b"new", overwrite=True)
            self.assertTrue(swapped)
            self.assertEqual(target.read_bytes(), b"original")
            self.assertEqual(external.read_bytes(), b"external")

    def test_overwrite_identity_check_uses_open_parent_descriptor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = write_core_fixture(root, "fixture.txt", b"original")
            real_stat = os.stat
            checked = False
            def track_descriptor_stat(path, *args, **kwargs):
                nonlocal checked
                if path == "fixture.txt" and kwargs.get("dir_fd") is not None:
                    checked = True
                return real_stat(path, *args, **kwargs)
            with mock.patch("madsc.core_fixture_writer.os.stat",
                            side_effect=track_descriptor_stat):
                write_core_fixture(root, "fixture.txt", b"new", overwrite=True)
            self.assertTrue(checked)
            self.assertEqual(target.read_bytes(), b"new")

    def test_unknown_protected_and_traversing_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in ("CALISANLAR.m3u", "playlist.m3u8", "../fixture.txt"):
                with self.subTest(relative=relative):
                    with self.assertRaises(ProtectedWriteRejected):
                        write_core_fixture(root, relative, b"blocked")
                    self.assertFalse((root / relative).exists())

    def test_nested_or_non_system_temp_root_is_rejected_before_descriptor_open(self):
        with tempfile.TemporaryDirectory() as directory:
            nested = Path(directory) / "nested"
            nested.mkdir()
            with mock.patch(
                    "madsc.core_fixture_writer.os.open") as descriptor_open:
                with self.assertRaises(ProtectedWriteRejected):
                    write_core_fixture(nested, "fixture.txt", b"blocked")
            descriptor_open.assert_not_called()

    def test_symlinked_history_parent_is_rejected_without_touching_target(self):
        with (tempfile.TemporaryDirectory() as directory,
              tempfile.TemporaryDirectory() as outside):
            root = Path(directory)
            target = Path(outside)
            (root / "legacy_history").symlink_to(target, target_is_directory=True)
            with self.assertRaises(ProtectedWriteRejected):
                write_core_fixture(root, "legacy_history/gecmis.json", b"blocked")
            self.assertEqual(list(target.iterdir()), [])

    def test_fifo_swapped_at_descriptor_open_cannot_block_writer(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "fixture.txt"
            target.write_bytes(b"original")
            real_open = os.open
            def swap_then_open(path, flags, *args, **kwargs):
                if path == "fixture.txt":
                    target.unlink()
                    os.mkfifo(target)
                return real_open(path, flags, *args, **kwargs)
            with mock.patch("madsc.core_fixture_writer.os.open", side_effect=swap_then_open):
                with self.assertRaises(OSError):
                    write_core_fixture(root, "fixture.txt", b"new", overwrite=True)
            self.assertTrue(target.is_fifo())

    def test_symlinked_overwrite_target_is_rejected_without_mutation(self):
        with (tempfile.TemporaryDirectory() as directory,
              tempfile.TemporaryDirectory() as outside):
            root = Path(directory)
            target = Path(outside) / "target.txt"
            target.write_bytes(b"original")
            (root / "fixture.txt").symlink_to(target)
            with self.assertRaises(ProtectedWriteRejected):
                write_core_fixture(root, "fixture.txt", b"blocked", overwrite=True)
            self.assertEqual(target.read_bytes(), b"original")

    def test_hardlinked_overwrite_target_is_rejected_without_mutation(self):
        with (tempfile.TemporaryDirectory() as directory,
              tempfile.TemporaryDirectory() as outside):
            root = Path(directory)
            target = Path(outside) / "target.txt"
            target.write_bytes(b"original")
            os.link(target, root / "fixture.txt")
            with self.assertRaises(ProtectedWriteRejected):
                write_core_fixture(root, "fixture.txt", b"blocked", overwrite=True)
            self.assertEqual(target.read_bytes(), b"original")


if __name__ == "__main__":
    unittest.main()
