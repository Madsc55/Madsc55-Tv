import tempfile
import json
from unittest.mock import patch
import unittest
from pathlib import Path
from madsc.restore_drill import run_drill, main


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

    def test_corrupted_backup_is_rejected_without_source_modification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "safe.txt").write_bytes(b"ORIGINAL")
            from madsc import restore_drill
            original_copy = restore_drill.shutil.copyfile

            def corrupt_copy(src, dst, *args, **kwargs):
                result = original_copy(src, dst, *args, **kwargs)
                if Path(dst).parent.name == "backup":
                    Path(dst).write_bytes(b"CORRUPTED")
                return result

            with patch.object(restore_drill.shutil, "copyfile", side_effect=corrupt_copy):
                with self.assertRaises(ValueError):
                    run_drill(source, ["safe.txt"])
            self.assertEqual((source / "safe.txt").read_bytes(), b"ORIGINAL")

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

    def test_k4_cli_uses_k1_guard_for_isolated_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "source").mkdir()
            (root / "source" / "a.txt").write_text("safe")
            (root / "reports").mkdir()
            output = root / "reports/k4-isolated-evidence.json"
            args = ["restore_drill", "--source", str(root / "source"),
                    "--file", "a.txt", "--output", str(output),
                    "--isolated-report-root", str(root)]
            with patch("sys.argv", args):
                main()
            payload = json.loads(output.read_text())
            self.assertEqual(payload["category"], "k4")
            self.assertFalse(payload["production_writes"])
            with patch("sys.argv", args), self.assertRaises(FileExistsError):
                main()
