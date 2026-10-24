"""K1 Unicode path canonicalization regression tests (offline, no production writes)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from madsc_guard import safe_relative_path, validate_manifest


class TestK1UnicodePathGuard(unittest.TestCase):
    def test_direct_guard_rejects_compatibility_unicode(self):
        for path in ("artifacts/ｓafe.txt", "artifacts/ﬁle.txt", "artifacts/Ｋ1.txt"):
            with self.subTest(path=path):
                self.assertFalse(safe_relative_path(path))

    def test_direct_guard_accepts_canonical_artifact(self):
        self.assertTrue(safe_relative_path("artifacts/k1-safe-result.json"))

    def test_manifest_rejects_compatibility_unicode(self):
        with self.assertRaises(ValueError):
            validate_manifest({"production_write": False, "output_paths": ["artifacts/ｓafe.txt"]})


if __name__ == "__main__":
    unittest.main()
