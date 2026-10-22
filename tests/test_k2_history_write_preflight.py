"""K2 validates history schemas and full output paths before creating files."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from madsc.history_artifact_download import extract_verified_history
from madsc.history_pair_store import atomic_write_pair
from tests.test_history_artifact_download import archive, FILES

class K2HistoryWritePreflightTests(unittest.TestCase):
    def test_invalid_schema_creates_no_history_directory(self):
        for bad in (b'{}', b'{"history":[]}', b'{"history":null}'):
            files = {**FILES, 'gecmis.json': bad}
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / 'history'
                with self.assertRaises(ValueError):
                    extract_verified_history(archive(files),
                        {k: hashlib.sha256(v).hexdigest() for k,v in files.items()}, target)
                self.assertFalse(target.exists())

    def test_atomic_pair_rejects_protected_parent_without_staging(self):
        pair = {'gecmis.json': {'history': {}}, 'ana_liste_test_gecmisi.json': {'channels': {}}}
        with tempfile.TemporaryDirectory() as tmp:
            protected = Path(tmp) / 'EPG'
            protected.mkdir()
            for exists in (False, True):
                target = protected / 'history.json'
                if exists:
                    target.write_bytes(b'keep')
                with patch('madsc.history_pair_store.tempfile.NamedTemporaryFile') as stage:
                    with self.assertRaises(PermissionError):
                        atomic_write_pair(target, pair)
                    stage.assert_not_called()
                if exists:
                    self.assertEqual(target.read_bytes(), b'keep')
                else:
                    self.assertEqual(list(protected.iterdir()), [])

    def test_atomic_pair_rejects_hardlinked_existing_evidence(self):
        import os
        pair = {'gecmis.json': {'history': {}}, 'ana_liste_test_gecmisi.json': {'channels': {}}}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, target = root / 'original.json', root / 'history.json'
            source.write_bytes(b'keep')
            os.link(source, target)
            with self.assertRaises(PermissionError):
                atomic_write_pair(target, pair)
            self.assertEqual(target.stat().st_ino, source.stat().st_ino)
            self.assertEqual(source.read_bytes(), b'keep')
