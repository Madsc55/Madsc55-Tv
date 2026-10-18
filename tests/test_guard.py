import unittest
from src.madsc_guard import safe_relative_path, validate_manifest

class GuardTests(unittest.TestCase):
    def test_allowed(self):
        validate_manifest({"production_write": False, "output_paths": ["artifacts/report.json"]})
    def test_denied(self):
        for path in ["../artifacts/x", "/tmp/x", "artifacts/FAVORILER.m3u", "artifacts/epg/report.json", "CALISANLAR.m3u"]:
            with self.subTest(path=path):
                self.assertFalse(safe_relative_path(path))
        for manifest in [{"production_write": True, "output_paths": ["artifacts/a"]}, {"production_write": False, "output_paths": ["../escape"]}]:
            with self.assertRaises(ValueError):
                validate_manifest(manifest)

if __name__ == "__main__":
    unittest.main()
