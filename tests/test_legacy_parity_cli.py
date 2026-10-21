import json
import tempfile
import unittest
from pathlib import Path
from madsc.legacy_parity_cli import run, load_json


class LegacyParityCliTests(unittest.TestCase):
    def test_read_only_batch_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inventory = {"source_repository": "Madsc55/madsc-tv",
                         "source_branch": "madsc/bes-sistem-toplu-birlestirme",
                         "workflows": [{"path": f".github/workflows/w{i:02}.yml"}
                                       for i in range(99)]}
            (root / "inventory.json").write_text(json.dumps(inventory))
            (root / "snapshots.json").write_text("{}")
            report = run(root / "inventory.json", root / "snapshots.json", root / "result.json")
            self.assertEqual(report["missing_pairs"], 99)
            self.assertEqual(report["behavioral_parity_accepted"], 0)
            with self.assertRaises(ValueError):
                run(root / "inventory.json", root / "snapshots.json", root / "result.json")

    def test_protected_outputs_and_symlink_ancestors_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inventory = {"source_repository": "Madsc55/madsc-tv",
                         "source_branch": "madsc/bes-sistem-toplu-birlestirme",
                         "workflows": [{"path": f".github/workflows/w{i:02}.yml"}
                                       for i in range(99)]}
            source = root / "inventory.json"
            snapshots = root / "snapshots.json"
            source.write_text(json.dumps(inventory))
            snapshots.write_text("{}")
            before = source.read_bytes(), snapshots.read_bytes()
            for name in ("playlist.m3u8", "xmltv.xml", "YEDEKLER/report.json",
                         "EPG/report.json", "FAVORILER/report.json"):
                output = root / name
                output.parent.mkdir(exist_ok=True)
                with self.subTest(name=name), self.assertRaises(PermissionError):
                    run(source, snapshots, output)
                self.assertFalse(output.exists())
            outside = root / "outside"
            outside.mkdir()
            (root / "alias").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(PermissionError):
                run(source, snapshots, root / "alias" / "report.json")
            self.assertEqual(list(outside.iterdir()), [])
            self.assertEqual(before, (source.read_bytes(), snapshots.read_bytes()))

    def test_duplicate_json_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "duplicate.json"
            path.write_text('{"x": 1, "x": 2}')
            with self.assertRaises(ValueError):
                load_json(path)


if __name__ == "__main__":
    unittest.main()
