import unittest
from madsc.maintenance import retry_decision, aggregate, summarize_batch

class MaintenanceTests(unittest.TestCase):
    def test_bounded_retry(self):
        self.assertEqual(retry_decision(3)["next_action"], "HALT_AND_REPORT")
        self.assertFalse(retry_decision(2)["blocked"])
        with self.assertRaises(ValueError):
            retry_decision(-1)
    def test_limit_boundary(self):
        self.assertFalse(retry_decision(2, 3)["blocked"])
        self.assertTrue(retry_decision(3, 3)["blocked"])
        self.assertTrue(retry_decision(4, 3)["blocked"])

    def test_noninteger_limit_rejected(self):
        for limit in (True, 2.5, "3"):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                retry_decision(1, limit)

    def test_batch_failure_summary(self):
        reports = [{"category": k, "production_writes": False, "status": "success"} for k in ("k1", "k2", "k3", "k4", "k5")]
        self.assertFalse(summarize_batch(reports)["requires_review"])
        reports[2]["status"] = "failure"
        summary = summarize_batch(reports)
        self.assertEqual(summary["failed_categories"], ["k3"])
        self.assertTrue(summary["requires_review"])
        self.assertFalse(summary["production_writes"])

    def test_missing_categories_never_ready(self):
        self.assertFalse(aggregate([{"category":"k1","production_writes":False}])["all_five_present"])
