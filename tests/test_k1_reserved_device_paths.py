"""K1 rejects Windows device aliases even on POSIX hosts."""
import unittest
from madsc.write_path_audit import audit_write_paths, enforce_write_paths, ProtectedWriteRejected


class ReservedDevicePathTests(unittest.TestCase):
    def test_reserved_stems_in_nested_paths(self):
        for path in ("CON", "con.txt", "reports/NUL.json", "tmp/aux",
                     "data/PRN.log", "reports/COM1.txt", "x/lpt9.csv",
                     "reports/ＣＯＮ.txt"):
            with self.subTest(path=path):
                self.assertTrue(audit_write_paths([path])["blocked"])
                with self.assertRaises(ProtectedWriteRejected):
                    enforce_write_paths([path])

    def test_non_reserved_similar_names_allowed(self):
        for path in ("reports/console.json", "reports/COM10.txt",
                     "reports/auxiliary.json", "reports/lpt10.json"):
            with self.subTest(path=path):
                self.assertFalse(audit_write_paths([path])["blocked"])


if __name__ == "__main__":
    unittest.main()
