"""K5 must never accept duplicate or malformed batch identities."""
import unittest
from madsc.maintenance import aggregate, summarize_batch


class K5ReportIdentityTests(unittest.TestCase):
    def test_duplicate_category_blocks_acceptance(self):
        reports = [{"category": key, "status": "success", "production_writes": False}
                   for key in ("k1", "k2", "k3", "k4", "k4")]
        result = summarize_batch(reports)
        self.assertFalse(result["all_five_present"])
        self.assertFalse(result["all_five_successful"])
        self.assertTrue(result["requires_review"])
        self.assertEqual(result["duplicate_categories"], ["k4"])
        self.assertEqual(result["missing_categories"], ["k5"])

    def test_exact_five_read_only_reports_are_fixture_success_only(self):
        reports = [{"category": key, "status": "success", "production_writes": False}
                   for key in ("k1", "k2", "k3", "k4", "k5")]
        result = aggregate(reports)
        self.assertTrue(result["all_five_successful"])
        self.assertFalse(result["production_ready"])
        self.assertFalse(result["runtime_evidence_verified"])

    def test_unverified_write_flag_blocks_success(self):
        reports = [{"category": key, "status": "success", "production_writes": False}
                   for key in ("k1", "k2", "k3", "k4", "k5")]
        reports[0].pop("production_writes")
        self.assertFalse(aggregate(reports)["all_five_successful"])


if __name__ == "__main__":
    unittest.main()
