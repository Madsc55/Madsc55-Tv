"""K1 guarded data writes must not modify repository control files."""
import unittest
from madsc.write_path_audit import audit_write_paths, enforce_write_paths, ProtectedWriteRejected


class GitMetadataGuardTests(unittest.TestCase):
    def test_git_and_workflow_paths_are_blocked(self):
        for path in (".git/config", ".github/workflows/test.yml",
                     ".gitmodules", ".gitattributes",
                     "reports/.git/config", "reports/.github/workflows/evil.yml",
                     "ＲＥＰＯＲＴＳ/.ＧＩＴ/config"):
            with self.subTest(path=path):
                self.assertTrue(audit_write_paths([path])["blocked"])
                with self.assertRaises(ProtectedWriteRejected):
                    enforce_write_paths([path])

    def test_regular_isolated_json_stays_allowed(self):
        result = enforce_write_paths(["reports/k1-safe-evidence.json"])
        self.assertFalse(result["blocked"])
        self.assertTrue(result["runtime_gate_enforced"])


if __name__ == "__main__":
    unittest.main()
