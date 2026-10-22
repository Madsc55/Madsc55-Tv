"""Compatibility Unicode colons must not bypass K1 path policy."""
import unittest
from madsc.write_path_audit import audit_write_paths, enforce_write_paths, ProtectedWriteRejected


class UnicodeStreamSeparatorTests(unittest.TestCase):
    def test_normalized_colon_aliases_rejected(self):
        for path in ("reports/name：stream.txt", "reports/：hidden",
                     "reports/name︓stream.json", "reports/Ｘ：meta.txt"):
            with self.subTest(path=path):
                self.assertTrue(audit_write_paths([path])["blocked"])
                with self.assertRaises(ProtectedWriteRejected):
                    enforce_write_paths([path])

    def test_safe_unicode_without_colon_is_allowed(self):
        self.assertFalse(audit_write_paths(["reports/özet.json"])["blocked"])


if __name__ == "__main__":
    unittest.main()
