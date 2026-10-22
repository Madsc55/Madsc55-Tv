"""The shared K1 fixture writer refuses overwrite and leaves no partial output."""
import tempfile
import unittest
from pathlib import Path
from madsc.fixture_report_writer import write_fixture_report


class ExclusiveFixtureWriterTests(unittest.TestCase):
    def test_new_report_is_written_once(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = write_fixture_report(root, "reports/evidence.json", '{"ok":true}')
            self.assertTrue(result["isolated_report_written"])
            self.assertEqual((root / "reports/evidence.json").read_text(), '{"ok":true}')
            with self.assertRaises(FileExistsError):
                write_fixture_report(root, "reports/evidence.json", "replacement")
            self.assertEqual((root / "reports/evidence.json").read_text(), '{"ok":true}')

    def test_protected_extension_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(PermissionError):
                write_fixture_report(Path(temp), "reports/playlist.m3u8", "unsafe")


if __name__ == "__main__":
    unittest.main()
