import unittest
from src.madsc_guard import safe_relative_path, validate_manifest

class GuardTests(unittest.TestCase):
    def test_allowed(self):
        validate_manifest({"production_write": False, "output_paths": ["artifacts/report.json"]})
    def test_denied(self):
        for path in ["artifacts/playlist.m3u8", "artifacts/xmltv.xml", "artifacts\\\\escape", "artifacts/../escape", "../artifacts/x", "/tmp/x", "artifacts/FAVORILER.m3u", "artifacts/epg/report.json", "CALISANLAR.m3u"]:
            with self.subTest(path=path):
                self.assertFalse(safe_relative_path(path))
        for manifest in [{"production_write": True, "output_paths": ["artifacts/a"]}, {"production_write": False, "output_paths": ["../escape"]}]:
            with self.assertRaises(ValueError):
                validate_manifest(manifest)

if __name__ == "__main__":
    unittest.main()

    def test_manifest_input_and_path_hardening(self):
        for manifest in (None, [], {"production_write": False, "output_paths": ["artifacts/a", "artifacts/a"]}):
            with self.subTest(manifest=manifest):
                with self.assertRaises(ValueError):
                    validate_manifest(manifest)
        for path in ("artifacts/a\\nb", "artifacts/C:/escape", "artifacts\\\\..\\\\escape"):
            with self.subTest(path=path):
                self.assertFalse(safe_relative_path(path))
