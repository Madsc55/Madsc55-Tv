import unittest
from madsc.write_path_audit import audit_write_paths

class WritePathAuditTests(unittest.TestCase):
    def test_protected_paths_blocked(self):
        report = audit_write_paths(["CALISANLAR.m3u", "epg/sample.xml", "logolar/a.png"])
        self.assertTrue(report["blocked"])
        self.assertEqual(len(report["rejected"]), 3)
        self.assertFalse(report["write_performed"])
        self.assertFalse(report["runtime_gate_enforced"])

    def test_unprotected_report_path(self):
        report = audit_write_paths(["reports/sample.json"])
        self.assertFalse(report["blocked"])

    def test_traversal_rejected(self):
        for path in ("../CALISANLAR.m3u", "/tmp/a", "a/../b", "a\\b"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                audit_write_paths([path])
