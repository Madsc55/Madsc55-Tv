import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
from src.madsc_guard import safe_relative_path, validate_manifest

class GuardTests(unittest.TestCase):
    def test_cli_rejects_symlink_and_oversized_manifest(self):
        from src.madsc_guard import main
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            valid = root / "valid.json"
            valid.write_text('{"production_write": false, "output_paths": ["artifacts/a.json"]}')
            link = root / "link.json"
            link.symlink_to(valid)
            oversized = root / "oversized.json"
            oversized.write_bytes(b" " * (1024 * 1024 + 1))
            for path in (link, oversized):
                with self.subTest(path=path.name):
                    with patch("sys.argv", ["madsc_guard", str(path)]):
                        with self.assertRaises(SystemExit) as caught:
                            main()
                        self.assertEqual(caught.exception.code, 2)

    def test_cli_reads_valid_manifest_from_single_descriptor(self):
        from src.madsc_guard import main
        with tempfile.TemporaryDirectory() as folder:
            manifest = Path(folder) / "valid.json"
            manifest.write_text('{"production_write": false, "output_paths": ["artifacts/report.json"]}')
            with patch("sys.argv", ["madsc_guard", str(manifest)]):
                main()

    def test_cli_rejects_nonregular_directory_manifest(self):
        from src.madsc_guard import main
        with tempfile.TemporaryDirectory() as folder:
            with patch("sys.argv", ["madsc_guard", folder]):
                with self.assertRaises(SystemExit) as caught:
                    main()
                self.assertEqual(caught.exception.code, 2)

    def test_cli_rejects_malformed_json_without_traceback(self):
        from src.madsc_guard import main
        with tempfile.TemporaryDirectory() as folder:
            manifest = Path(folder) / "malformed.json"
            manifest.write_text("{not-json")
            with patch("sys.argv", ["madsc_guard", str(manifest)]):
                with self.assertRaises(SystemExit) as caught:
                    main()
                self.assertEqual(caught.exception.code, 2)

    def test_cli_rejects_invalid_utf8_manifest_without_traceback(self):
        from src.madsc_guard import main
        with tempfile.TemporaryDirectory() as folder:
            manifest = Path(folder) / "invalid-utf8.json"
            manifest.write_bytes(b'{"production_write": false, "output_paths": ["artifacts/\xff"]}')
            with patch("sys.argv", ["madsc_guard", str(manifest)]):
                with self.assertRaises(SystemExit) as caught:
                    main()
                self.assertEqual(caught.exception.code, 2)

    def test_cli_fails_closed_without_no_follow_support(self):
        import os
        from src.madsc_guard import main
        with tempfile.TemporaryDirectory() as folder:
            manifest = Path(folder) / "valid.json"
            manifest.write_text('{"production_write": false, "output_paths": ["artifacts/report.json"]}')
            with patch.object(os, "O_NOFOLLOW", None, create=True):
                with patch("sys.argv", ["madsc_guard", str(manifest)]):
                    with self.assertRaises(SystemExit) as caught:
                        main()
                    self.assertEqual(caught.exception.code, 2)

    def test_allowed(self):
        validate_manifest({"production_write": False, "output_paths": ["artifacts/report.json"]})
    def test_denied(self):
        for path in ["artifacts/playlist.m3u8", "artifacts/xmltv.xml", "artifacts\\\\escape", "artifacts/../escape", "../artifacts/x", "/tmp/x", "artifacts/FAVORILER.m3u", "artifacts/epg/report.json", "CALISANLAR.m3u"]:
            with self.subTest(path=path):
                self.assertFalse(safe_relative_path(path))
        for manifest in [{"production_write": True, "output_paths": ["artifacts/a"]}, {"production_write": False, "output_paths": ["../escape"]}]:
            with self.assertRaises(ValueError):
                validate_manifest(manifest)

    def test_duplicate_paths_after_normalization(self):
        for paths in (["artifacts/report.json", "artifacts/REPORT.JSON"],
                      ["artifacts/a/b.json", "artifacts/a\\\\b.json"],
                      ["artifacts/report.json", "artifacts/ｒｅｐｏｒｔ.json"]):
            with self.subTest(paths=paths):
                with self.assertRaises(ValueError):
                    validate_manifest({"production_write": False, "output_paths": paths})

    def test_nfkc_normalization_precedes_protected_path_check(self):
        for path in ("artifacts/ｐｌａｙｌｉｓｔ.m3u8",
                     "artifacts/ｘｍｌｔｖ.xml",
                     "ａｒｔｉｆａｃｔｓ/report.json"):
            with self.subTest(path=path):
                with self.assertRaises(ValueError):
                    validate_manifest({"production_write": False, "output_paths": [path]})

    def test_manifest_input_and_path_hardening(self):
        for manifest in (None, [], {"production_write": False, "output_paths": ["artifacts/a", "artifacts/a"]}):
            with self.subTest(manifest=manifest):
                with self.assertRaises(ValueError):
                    validate_manifest(manifest)
        for path in ("artifacts/a\\nb", "artifacts/C:/escape", "artifacts\\\\..\\\\escape"):
            with self.subTest(path=path):
                self.assertFalse(safe_relative_path(path))

if __name__ == "__main__":
    unittest.main()
