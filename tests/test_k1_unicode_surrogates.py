"""Reject unpaired surrogate code points before filesystem operations."""
import unittest
from madsc.write_path_audit import audit_write_paths, enforce_write_paths, ProtectedWriteRejected


class SurrogateTests(unittest.TestCase):
    def test_unpaired_surrogates_are_rejected(self):
        for path in ("reports/a" + chr(0xD800) + ".json",
                     "reports/a" + chr(0xDFFF) + ".json",
                     "reports/" + chr(0xDC00) + "/file.json"):
            with self.subTest(path=ascii(path)):
                self.assertTrue(audit_write_paths([path])["blocked"])
                with self.assertRaises(ProtectedWriteRejected):
                    enforce_write_paths([path])

    def test_valid_unicode_allowed(self):
        self.assertFalse(audit_write_paths(["reports/kanal-özet.json"])["blocked"])


if __name__ == "__main__":
    unittest.main()
