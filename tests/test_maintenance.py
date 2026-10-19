import unittest
from madsc.maintenance import retry_decision, aggregate

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

    def test_missing_categories_never_ready(self):
        self.assertFalse(aggregate([{"category":"k1","production_writes":False}])["all_five_present"])
