import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from madsc.fixture_report_writer import write_fixture_report, write_stage_report
from madsc.history_pair_store import write_isolated_history_pair, decode_pair


class FixtureReportWriterTests(unittest.TestCase):
    def test_allowed_fixture_report(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            result = write_fixture_report(root, "reports/result.json", "{}")
            self.assertTrue(result["isolated_report_written"])
            self.assertFalse(result["production_write_allowed"])
            self.assertEqual((root / "reports/result.json").read_text(), "{}")

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
            with self.assertRaises(ValueError):
                write_stage_report(root, "k6", {"category": "k6", "production_writes": False})
