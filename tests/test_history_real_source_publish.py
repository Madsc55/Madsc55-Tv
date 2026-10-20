"""Real-source producer cannot fabricate fixture history."""
import hashlib
import tempfile
from unittest.mock import patch
import unittest
from pathlib import Path

from madsc.history_real_source_publish import publish_source


class RealSourcePublisherTests(unittest.TestCase):
    def test_missing_source_fails_without_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            target = root / "out"
            with self.assertRaises(ValueError):
                publish_source(source, target)
            self.assertFalse(target.exists())

    def test_valid_supplied_pair_copied_byte_for_byte_not_authenticated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            files = {
                "gecmis.json": b'{"history":{}}',
                "ana_liste_test_gecmisi.json": b'{"channels":{}}',
            }
            for name, data in files.items():
                (source / name).write_bytes(data)
            target = root / "out"
            report = publish_source(source, target)
            self.assertFalse(report["real_source_independently_authenticated"])
            self.assertFalse(report["production_writes"])
            self.assertTrue(report["byte_integrity_verified"])
            self.assertEqual(report["source_sha256"], {
                name: hashlib.sha256(data).hexdigest() for name, data in files.items()
            })
            for name, data in files.items():
                self.assertEqual((target / name).read_bytes(), data)
            with self.assertRaises(ValueError):
                publish_source(source, target)

    def test_source_mutation_during_publication_rejected_without_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (source / "gecmis.json").write_text('{"history":{}}')
            (source / "ana_liste_test_gecmisi.json").write_text('{"channels":{}}')
            target = root / "out"
            original = Path.read_bytes
            counter = {"reads": 0}

            def changing_read(path):
                if Path(path) == source / "gecmis.json":
                    counter["reads"] += 1
                    if counter["reads"] >= 2:
                        return b'{"history":{"changed":{}}}'
                return original(path)

            with patch.object(Path, "read_bytes", changing_read):
                with self.assertRaisesRegex(ValueError, "changed during validation"):
                    publish_source(source, target)
            self.assertFalse(target.exists())

    def test_symlinked_source_file_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            (root / "outside").write_text('{"history":{}}')
            (source / "gecmis.json").symlink_to(root / "outside")
            (source / "ana_liste_test_gecmisi.json").write_text('{"channels":{}}')
            with self.assertRaises(ValueError):
                publish_source(source, root / "out")


if __name__ == "__main__":
    unittest.main()
