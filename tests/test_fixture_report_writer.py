import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from madsc.fixture_report_writer import (write_fixture_report, write_stage_report,
                                         write_turkish_tv_test_bundle,
                                         write_exclusive_bytes)
from madsc.history_pair_store import write_isolated_history_pair, decode_pair


class FixtureReportWriterTests(unittest.TestCase):
    def test_k4_fixture_exclusive_write_rejects_existing(self):
        from madsc.write_path_audit import (enforce_write_paths,
                                            enforce_local_evidence_path)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "reports/k4-source/nested/sample.txt"
            enforce_write_paths(["reports/k4-source/nested/sample.txt"])
            target.parent.mkdir(parents=True)
            enforce_local_evidence_path(target, allowed_root=root)
            write_exclusive_bytes(target, b"fixture", allowed_root=root)
            self.assertEqual(target.read_bytes(), b"fixture")
            with self.assertRaises(PermissionError):
                enforce_local_evidence_path(target, allowed_root=root)
            with self.assertRaises(PermissionError):
                write_exclusive_bytes(target, b"overwrite", allowed_root=root)
            self.assertEqual(target.read_bytes(), b"fixture")

    def test_exclusive_evidence_syncs_file_and_parent_directory(self):
        import os
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            destination = root / "reports/synced.json"
            real_fsync = os.fsync
            descriptors = []
            def observe_fsync(fd):
                descriptors.append(os.fstat(fd).st_mode)
                return real_fsync(fd)
            with patch("madsc.fixture_report_writer.os.fsync", side_effect=observe_fsync):
                write_exclusive_bytes(destination, b"{}", allowed_root=root)
            import stat
            self.assertTrue(any(stat.S_ISREG(mode) for mode in descriptors))
            self.assertTrue(any(stat.S_ISDIR(mode) for mode in descriptors))
            self.assertEqual(destination.read_bytes(), b"{}")

    def test_stage_report_rejects_nonfinite_json_without_creating_file(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            report = {"category": "k3", "production_writes": False,
                      "production_ready": False, "metric": float("nan")}
            with self.assertRaises(ValueError):
                write_stage_report(root, "k3", report)
            self.assertFalse((root / "reports/k3-isolated-evidence.json").exists())

    def test_turkish_tv_bundle_is_fixed_scoped_and_non_overwriting(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            result = write_turkish_tv_test_bundle(root, b"#EXTM3U\n", '{"ok": true}\n')
            playlist = root / result["playlist_path"]
            report = root / result["report_path"]
            self.assertEqual(playlist.read_bytes(), b"#EXTM3U\n")
            self.assertEqual(report.read_text(), '{"ok": true}\n')
            self.assertFalse(result["production_write_allowed"])
            with self.assertRaises(PermissionError):
                write_turkish_tv_test_bundle(root, b"changed", "changed")
            self.assertEqual(playlist.read_bytes(), b"#EXTM3U\n")

    def test_protected_fixture_root_rejected_before_reports_creation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "FAVORILER"
            root.mkdir()
            with self.assertRaises(PermissionError):
                write_turkish_tv_test_bundle(root, b"#EXTM3U\\n", "{}\\n")
            self.assertFalse((root / "reports").exists(),
                             "protected fixture root must fail before mkdir")

    def test_direct_exclusive_writer_rejects_protected_path_before_os_open(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            protected = root / "FAVORILER"
            protected.mkdir()
            target = protected / "evidence.json"
            with patch("madsc.fixture_report_writer.os.open") as open_call:
                with self.assertRaises(PermissionError):
                    write_exclusive_bytes(target, b"blocked", allowed_root=root)
            open_call.assert_not_called()
            self.assertFalse(target.exists())

    def test_turkish_tv_bundle_rejects_symlinked_reports_before_write(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            outside = root / "outside"
            outside.mkdir()
            (root / "reports").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(PermissionError):
                write_turkish_tv_test_bundle(root, b"#EXTM3U\n", "{}\n")
            self.assertEqual(list(outside.iterdir()), [])

    def test_turkish_tv_bundle_rolls_back_first_file_on_second_write_failure(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            original = __import__("madsc.fixture_report_writer", fromlist=["_exclusive_bytes"])
            real_write = original._exclusive_bytes
            calls = []
            def fail_second(path, payload, **policy):
                calls.append(path)
                if len(calls) == 2:
                    raise OSError("report write failed")
                return real_write(path, payload, **policy)
            with patch("madsc.fixture_report_writer._exclusive_bytes", side_effect=fail_second):
                with self.assertRaises(OSError):
                    write_turkish_tv_test_bundle(root, b"#EXTM3U\n", "{}\n")
            self.assertFalse((root / "reports/MADSC55_TURKCE_TV_ADAY_DENEME.m3u8").exists())
            self.assertFalse((root / "reports/turkish-tv-batch-validation.json").exists())

    def test_bundle_rollback_does_not_delete_concurrent_replacement(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            module = __import__("madsc.fixture_report_writer", fromlist=["_exclusive_bytes"])
            real_write = module._exclusive_bytes
            playlist = root / "reports/MADSC55_TURKCE_TV_ADAY_DENEME.m3u8"
            calls = []
            def replace_before_second_write(path, payload, **policy):
                calls.append(path)
                if len(calls) == 1:
                    return real_write(path, payload, **policy)
                held = root / "concurrent-replacement-held-inode"
                playlist.rename(held)
                playlist.write_bytes(b"concurrent replacement")
                raise OSError("simulated second write failure")
            with patch("madsc.fixture_report_writer._exclusive_bytes",
                       side_effect=replace_before_second_write):
                with self.assertRaisesRegex(OSError, "simulated"):
                    write_turkish_tv_test_bundle(root, b"#EXTM3U\n", "{}\n")
            self.assertTrue(playlist.exists(), "rollback must preserve the concurrent replacement")
            self.assertEqual(playlist.read_bytes(), b"concurrent replacement")

    def test_exclusive_writer_fails_closed_without_nofollow(self):
        import os
        from madsc.fixture_report_writer import _exclusive_bytes
        with tempfile.TemporaryDirectory() as d:
            destination = Path(d) / "evidence.json"
            with patch.object(os, "O_NOFOLLOW", None, create=True):
                with self.assertRaisesRegex(PermissionError, "Secure descriptor-relative output is unavailable"):
                    _exclusive_bytes(destination, b'{"ok": true}')
            self.assertFalse(destination.exists())

    def test_fixture_writer_rejects_symlinked_root_ancestor(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            real = base / "real"
            fixture = real / "fixture"
            fixture.mkdir(parents=True)
            alias = base / "alias"
            alias.symlink_to(real, target_is_directory=True)
            root_through_alias = alias / "fixture"
            with self.assertRaisesRegex(PermissionError, "ancestors"):
                write_fixture_report(root_through_alias, "reports/result.json", "{}")
            self.assertFalse((fixture / "reports").exists())

    def test_fixture_roots_reject_relative_and_traversing_inputs(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            for root in (Path("relative-fixture"), base / "child/../fixture"):
                with self.subTest(root=str(root)):
                    with self.assertRaisesRegex(PermissionError, "absolute and nontraversing"):
                        write_fixture_report(root, "reports/evidence.json", "{}")
                    with self.assertRaisesRegex(PermissionError, "absolute and nontraversing"):
                        write_turkish_tv_test_bundle(root, b"#EXTM3U\\n", "{}")
            self.assertFalse((base / "child").exists())
            self.assertFalse((base / "fixture").exists())

    def test_fixture_roots_reject_ambiguous_unicode_and_controls(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            invalid = (str(base) + "/bad\u202e", str(base) + "/bad\n",
                       str(base) + "/bad\uff0falias",
                       str(base) + "/bad\\\\alias",
                       str(base) + "/bad\uff1aalias")
            for raw in invalid:
                with self.subTest(root=repr(raw)):
                    with self.assertRaisesRegex(PermissionError, "absolute and nontraversing"):
                        write_fixture_report(Path(raw), "reports/evidence.json", "{}")
                    with self.assertRaisesRegex(PermissionError, "absolute and nontraversing"):
                        write_turkish_tv_test_bundle(Path(raw), b"#EXTM3U\\n", "{}")

    def test_fixture_root_rejects_oversized_and_noncharacter_names(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            for raw in (str(base) + "/" + "a" * 4097,
                        str(base) + "/bad\ufdd0",
                        str(base) + "/bad\u0085"):
                with self.subTest(root_length=len(raw)):
                    with self.assertRaisesRegex(PermissionError, "absolute and nontraversing"):
                        write_fixture_report(Path(raw), "reports/evidence.json", "{}")
            self.assertFalse((base / "reports").exists())

    def test_fixture_root_rejects_trailing_dot_and_space_aliases(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            for suffix in ("alias.", "alias ", "alias\uff0e", "alias\u3000"):
                root = base / suffix
                with self.subTest(suffix=repr(suffix)):
                    with self.assertRaisesRegex(PermissionError, "absolute and nontraversing"):
                        write_fixture_report(root, "reports/evidence.json", "{}")
                    with self.assertRaisesRegex(PermissionError, "absolute and nontraversing"):
                        write_turkish_tv_test_bundle(root, b"#EXTM3U\\n", "{}")
                    self.assertFalse(root.exists())

    def test_fixture_root_rejects_nfkc_alias_without_creating_reports(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            for alias in ("fixture\uff41", "fixture\u212a", "fixture\ufb01"):
                root = base / alias
                root.mkdir()
                with self.subTest(alias=repr(alias)):
                    with self.assertRaisesRegex(PermissionError, "absolute and nontraversing"):
                        write_fixture_report(root, "reports/evidence.json", "{}")
                    with self.assertRaisesRegex(PermissionError, "absolute and nontraversing"):
                        write_turkish_tv_test_bundle(root, b"#EXTM3U\\n", "{}")
                    self.assertFalse((root / "reports").exists())

    def test_bundle_reports_directory_created_using_root_descriptor(self):
        import os
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            real_mkdir = os.mkdir
            seen = []
            def observed_mkdir(path, mode=0o777, *, dir_fd=None):
                if path == "reports":
                    self.assertIsNotNone(dir_fd)
                    opened = os.fstat(dir_fd)
                    expected = root.stat()
                    self.assertEqual((opened.st_dev, opened.st_ino),
                                     (expected.st_dev, expected.st_ino))
                    seen.append(path)
                return real_mkdir(path, mode, dir_fd=dir_fd)
            real_fsync = os.fsync
            synced_root = []
            def observed_fsync(fd):
                opened = os.fstat(fd)
                expected = root.stat()
                if (opened.st_dev, opened.st_ino) == (expected.st_dev, expected.st_ino):
                    synced_root.append(True)
                return real_fsync(fd)
            with patch("madsc.fixture_report_writer.os.mkdir", side_effect=observed_mkdir), \
                 patch("madsc.fixture_report_writer.os.fsync", side_effect=observed_fsync):
                write_turkish_tv_test_bundle(root, b"#EXTM3U\\n", "{}")
            self.assertEqual(seen, ["reports"])
            self.assertTrue(synced_root, "root directory entry must be synced")

    def test_allowed_fixture_report(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            result = write_fixture_report(root, "reports/result.json", "{}")
            self.assertTrue(result["isolated_report_written"])
            self.assertFalse(result["production_write_allowed"])
            self.assertEqual((root / "reports/result.json").read_text(), "{}")

    def test_nontext_content_creates_no_empty_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for value in (None, b"binary", 7, {"result": "ok"}):
                with self.subTest(value=value), self.assertRaises(TypeError):
                    write_fixture_report(root, "reports/evidence.json", value)
                self.assertFalse((root / "reports/evidence.json").exists())
            self.assertFalse((root / "reports").exists())

    def test_protected_and_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for path in ("CALISANLAR.m3u", "epg/guide.xml", "reports/../bad",
                         "reports/channel.m3u", "reports/../../escape"):
                with self.subTest(path=path), self.assertRaises(PermissionError):
                    write_fixture_report(root, path, "no")
            self.assertFalse((root / "CALISANLAR.m3u").exists())

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "outside").mkdir()
            (root / "reports").symlink_to(root / "outside", target_is_directory=True)
            with self.assertRaises(PermissionError):
                write_fixture_report(root, "reports/data.json", "no")
            self.assertFalse((root / "outside" / "data.json").exists())

    def test_nested_symlink_does_not_create_outside_directories(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            outside = root / "outside"
            outside.mkdir()
            (root / "reports").mkdir()
            (root / "reports" / "linked").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(PermissionError):
                write_fixture_report(root, "reports/linked/new/sub/report.json", "{}")
            self.assertFalse((outside / "new").exists())

    def test_runtime_gate_is_invoked_before_any_report_write(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with patch("madsc.fixture_report_writer.enforce_write_paths",
                       side_effect=PermissionError("policy rejected")) as guard:
                with self.assertRaises(PermissionError):
                    write_fixture_report(root, "reports/rejected.json", "forbidden")
            guard.assert_called_once_with(["reports/rejected.json"])
            self.assertFalse((root / "reports").exists())

    def test_local_output_runtime_gate_is_invoked_before_write(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with patch("madsc.fixture_report_writer.enforce_local_output_path",
                       side_effect=PermissionError("runtime gate rejected")) as gate:
                with self.assertRaises(PermissionError):
                    write_fixture_report(root, "reports/rejected.json", "forbidden")
            gate.assert_called_once_with(root / "reports", allowed_root=root)
            self.assertFalse((root / "reports").exists())

    def test_failed_fsync_removes_only_the_partial_evidence_file(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            target = root / "reports/partial.json"
            with patch("madsc.fixture_report_writer.os.fsync",
                       side_effect=OSError("simulated durable-write failure")):
                with self.assertRaisesRegex(OSError, "simulated durable-write failure"):
                    write_fixture_report(root, "reports/partial.json", "partial payload")
            self.assertFalse(target.exists())

    def test_exclusive_writer_does_not_follow_symlinked_parent(self):
        from madsc.fixture_report_writer import _exclusive_bytes
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            outside = root / "outside"
            outside.mkdir()
            (root / "reports").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(OSError):
                _exclusive_bytes(root / "reports/escaped.json", b"blocked")
            self.assertFalse((outside / "escaped.json").exists())

    def test_existing_report_evidence_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write_fixture_report(root, "reports/evidence.json", "first")
            with self.assertRaises(FileExistsError):
                write_fixture_report(root, "reports/evidence.json", "second")
            self.assertEqual((root / "reports/evidence.json").read_text(), "first")

    def test_k2_history_is_protected_by_k1_and_does_not_overwrite(self):
        pair = {"gecmis.json": {"history": {}},
                "ana_liste_test_gecmisi.json": {"channels": {}}}
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            result = write_isolated_history_pair(root, "reports/history-pair.json", pair)
            self.assertTrue(result["isolated_history_written"])
            self.assertEqual(decode_pair((root / "reports/history-pair.json").read_text()), pair)
            with self.assertRaises(PermissionError):
                write_isolated_history_pair(root, "reports/history-pair.json", pair)

    def test_k2_history_uses_local_output_guard(self):
        pair = {"gecmis.json": {"history": {}},
                "ana_liste_test_gecmisi.json": {"channels": {}}}
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            with patch("madsc.write_path_audit.enforce_local_output_path") as guard:
                write_isolated_history_pair(root, "reports/history-pair.json", pair)
            guard.assert_called_once_with(
                root / "reports/history-pair.json", allowed_root=root)

    def test_k2_history_guard_refusal_creates_no_evidence(self):
        pair = {"gecmis.json": {"history": {}},
                "ana_liste_test_gecmisi.json": {"channels": {}}}
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            target = root / "reports/history-pair.json"
            with patch("madsc.write_path_audit.enforce_local_output_path",
                       side_effect=PermissionError("rejected")):
                with self.assertRaises(PermissionError):
                    write_isolated_history_pair(root, "reports/history-pair.json", pair)
            self.assertFalse(target.exists())

    def test_k2_history_rejects_traversal_and_protected_paths(self):
        pair = {"gecmis.json": {"history": {}},
                "ana_liste_test_gecmisi.json": {"channels": {}}}
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            for path in ("reports/../gecmis.json", "gecmis.json", "reports/test.m3u8"):
                with self.subTest(path=path), self.assertRaises(PermissionError):
                    write_isolated_history_pair(root, path, pair)

    def test_k3_k4_k5_shared_k1_gate(self):
        import json
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for stage in ("k3", "k4", "k5"):
                payload = {"category": stage, "production_writes": False,
                           "production_ready": False, "status": "fixture"}
                result = write_stage_report(root, stage, payload)
                self.assertEqual(result["stage"], stage)
                self.assertEqual(json.loads((root / result["relative_path"]).read_text()), payload)
                with self.assertRaises(FileExistsError):
                    write_stage_report(root, stage, payload)
            for stage in ("k3", "k4", "k5"):
                with self.assertRaises(ValueError):
                    write_stage_report(root, stage, {"category": stage, "production_writes": True})
            for invalid in (None, "false", 0, 1, True):
                with self.subTest(production_ready=invalid), self.assertRaises(ValueError):
                    write_stage_report(root, "k3", {
                        "category": "k3", "production_writes": False,
                        "production_ready": invalid})
            with self.assertRaises(ValueError):
                write_stage_report(root, "k3", {
                    "category": "k3", "production_writes": False})
            with self.assertRaises(ValueError):
                write_stage_report(root, "k6", {"category": "k6", "production_writes": False})
