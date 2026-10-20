import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from madsc.fixture_report_writer import write_fixture_report


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
