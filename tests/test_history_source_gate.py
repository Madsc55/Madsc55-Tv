"""Real source gate rejects fixture claims, missing files and altered bytes."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from madsc.history_source_gate import load_verified_source


class HistorySourceGateTests(unittest.TestCase):
    def test_verified_source_and_negative_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "history"
            folder.mkdir()
            documents = {
                "gecmis.json": {"history": {"a": {"runs": 2}}},
                "ana_liste_test_gecmisi.json": {"channels": {"a": {"runs": 2}}}}
            for name, doc in documents.items():
                (folder / name).write_text(json.dumps(doc), encoding="utf-8")
            manifest = {
                "schema": 1, "mode": "VERIFIED_SOURCE", "source_run_id": "123",
                "source_commit_sha": "a" * 40, "production_writes": False,
                "hashes": {name: hashlib.sha256((folder / name).read_bytes()).hexdigest()
                           for name in documents}}
            path = root / "manifest.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertEqual(load_verified_source(folder, path, run_id="123",
                                                   commit_sha="a" * 40), documents)
            for change in ({"mode": "ISOLATED_FIXTURE"},
                           {"source_run_id": "999"}, {"production_writes": True},
                           {"source_commit_sha": "b" * 40}):
                with self.subTest(change=change):
                    path.write_text(json.dumps({**manifest, **change}), encoding="utf-8")
                    with self.assertRaises(ValueError):
                        load_verified_source(folder, path, run_id="123", commit_sha="a" * 40)
            path.write_text(json.dumps(manifest), encoding="utf-8")
            (folder / "gecmis.json").write_text('{"history":{}}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_verified_source(folder, path, run_id="123", commit_sha="a" * 40)

    def test_missing_source_rejected_without_bootstrap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ValueError):
                load_verified_source(root / "missing", root / "manifest.json",
                                     run_id="123", commit_sha="a" * 40)


if __name__ == "__main__":
    unittest.main()
