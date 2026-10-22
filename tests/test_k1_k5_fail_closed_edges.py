"""Fail-closed K1 write preflight and K5 fixture evidence boundaries."""
import unittest

from madsc.write_path_audit import audit_write_paths, enforce_write_paths
from madsc.maintenance import verify_fixture_evidence


class K1K5FailClosedEdges(unittest.TestCase):
    def test_empty_k1_write_batch_is_not_authorized(self):
        for check in (audit_write_paths, enforce_write_paths):
            with self.subTest(check=check.__name__):
                with self.assertRaises(ValueError):
                    check([])

    def test_k5_blank_fixture_check_name_rejected(self):
        reports = [
            {"category": category, "status": "success",
             "production_writes": False, "fixture_checks": {"isolation": True}}
            for category in ("k1", "k2", "k3", "k4", "k5")
        ]
        reports[4]["fixture_checks"] = {" ": True}
        result = verify_fixture_evidence(reports)
        self.assertFalse(result["fixture_evidence_verified"])
        self.assertEqual(result["missing_fixture_evidence"], ["k5"])

    def test_k5_named_fixture_checks_remain_valid_offline(self):
        reports = [
            {"category": category, "status": "success",
             "production_writes": False, "fixture_checks": {"isolation": True}}
            for category in ("k1", "k2", "k3", "k4", "k5")
        ]
        result = verify_fixture_evidence(reports)
        self.assertTrue(result["fixture_evidence_verified"])
        self.assertFalse(result["production_ready"])


if __name__ == "__main__":
    unittest.main()
