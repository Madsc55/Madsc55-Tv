"""Guarded writes reject invisible and bidirectional Unicode path tricks."""
import unittest

from madsc.write_path_audit import (
    ProtectedWriteRejected, audit_write_paths, enforce_write_paths,
)


class UnicodeFormatGuardTests(unittest.TestCase):
    def test_invisible_and_bidi_format_characters_blocked(self):
        for path in (
            "reports/safe\u200b.json",
            "reports/\u202ejson.elif",
            "reports/safe\u2066name\u2069.json",
            "reports/a\u200d.json",
        ):
            with self.subTest(path=repr(path)):
                self.assertTrue(audit_write_paths([path])["blocked"])
                with self.assertRaises(ProtectedWriteRejected):
                    enforce_write_paths([path])

    def test_normal_unicode_report_name_allowed(self):
        report = enforce_write_paths(["reports/güvenlik-kanıtı.json"])
        self.assertFalse(report["blocked"])


if __name__ == "__main__":
    unittest.main()
