"""Negative archive cases: tampering, traversal, symlink, extra files."""
import hashlib
import io
import tempfile
import unittest
import zipfile
from pathlib import Path

from madsc.history_artifact_download import extract_verified_history

FILES = {"gecmis.json": b'{"history":{}}',
         "ana_liste_test_gecmisi.json": b'{"channels":{}}'}


def archive(files):
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as z:
        for name, raw in files.items():
            z.writestr(name, raw)
    return out.getvalue()


class HistoryArtifactDownloadTests(unittest.TestCase):
    def test_verified_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            hashes = {name: hashlib.sha256(raw).hexdigest() for name, raw in FILES.items()}
            output = Path(tmp) / "history"
            result = extract_verified_history(archive(FILES), hashes, output)
            self.assertEqual(set(result), set(FILES))
            self.assertEqual((output / "gecmis.json").read_bytes(), FILES["gecmis.json"])

    def test_tampered_or_extra_file_rejected_before_writes(self):
        hashes = {name: hashlib.sha256(raw).hexdigest() for name, raw in FILES.items()}
        for files in ({**FILES, "gecmis.json": b'{"history":{"tampered":true}}'},
                      {**FILES, "../escape.json": b"bad"},
                      {"gecmis.json": FILES["gecmis.json"]}):
            with tempfile.TemporaryDirectory() as tmp:
                output = Path(tmp) / "history"
                with self.subTest(files=list(files)), self.assertRaises(ValueError):
                    extract_verified_history(archive(files), hashes, output)
                self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
