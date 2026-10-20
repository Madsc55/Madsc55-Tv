import tempfile
import unittest
from pathlib import Path
from madsc.restore_drill import run_drill


class RestoreDrillTests(unittest.TestCase):
    def test_end_to_end_nested_backup_restore(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "nested").mkdir()
            (root / "nested" / "history.json").write_bytes(b'{"history":{}}')
            (root / "channels.m3u").write_bytes(b"#EXTM3U\n")
            before = {p: (root / p).read_bytes() for p in ("nested/history.json", "channels.m3u")}
            result = run_drill(root, list(before))
            self.assertTrue(result["drill_executed"])
            self.assertTrue(result["independent_sandbox_restore_matches"])
            self.assertTrue(result["source_unchanged"])
            self.assertFalse(result["external_storage_proven"])
            self.assertFalse(result["production_restore_verified"])
            self.assertFalse(result["production_writes"])
            self.assertEqual(before, {p: (root / p).read_bytes() for p in before})

    def test_missing_and_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "safe.txt").write_text("safe")
            for names in ([], ["missing.txt"], ["../outside"], ["safe.txt", "safe.txt"]):
                with self.subTest(names=names), self.assertRaises((ValueError, FileNotFoundError)):
                    run_drill(root, names)

    def test_symlink_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "real.txt").write_text("safe")
            (root / "alias.txt").symlink_to(root / "real.txt")
            with self.assertRaises(ValueError):
                run_drill(root, ["alias.txt"])
