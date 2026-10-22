"""Git metadata auxiliary files must be rejected by guarded data writers."""
import unittest
from madsc.write_path_audit import audit_write_paths, enforce_write_paths, ProtectedWriteRejected


class GitAuxMetadataGuardTests(unittest.TestCase):
    def test_auxiliary_git_metadata_blocked(self):
        for name in (".gitignore", ".mailmap", "reports/.gitignore",
                     "reports/.mailmap", "reports/.GITIGNORE",
                     "reports/．gitignore"):
            with self.subTest(name=name):
                self.assertTrue(audit_write_paths([name])["blocked"])
                with self.assertRaises(ProtectedWriteRejected):
                    enforce_write_paths([name])

    def test_regular_report_path_allowed(self):
        self.assertFalse(enforce_write_paths(["reports/k1-audit.json"])["blocked"])


if __name__ == "__main__":
    unittest.main()
