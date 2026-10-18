import unittest
from madsc.ibo_policy import classify_channel

class IboPolicyTests(unittest.TestCase):
    def test_ibo_working_survives_failed_technical_check(self):
        result = classify_channel("NEEDS_REVIEW", "WORKING")
        self.assertTrue(result["protected_working"])
        self.assertFalse(result["technical_failure_overrides_ibo"])
        self.assertFalse(result["delete_allowed"])
        self.assertFalse(result["backup_write_allowed"])
    def test_unknown_does_not_authorize_mutation(self):
        result = classify_channel("PRELIMINARY_PASS")
        self.assertFalse(result["production_change_allowed"])
        self.assertFalse(result["delete_allowed"])
    def test_invalid_device_result_rejected(self):
        with self.assertRaises(ValueError):
            classify_channel("NEEDS_REVIEW", "GUESS")
