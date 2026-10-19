import unittest

from madsc.ci_diagnostics import diagnose


class DiagnosticsTests(unittest.TestCase):
    def test_failure_extraction(self):
        report = diagnose("FAIL: test_case (tests.test_sample.Case)\nRan 210 tests in 0.359s\nFAILED (failures=3)")
        self.assertEqual(report["tests_run"], 210)
        self.assertEqual(report["result"], "failed")
        self.assertEqual(report["failed_cases"][0]["test"], "test_case")
        self.assertFalse(report["automatic_code_fix_applied"])

    def test_success(self):
        report = diagnose("Ran 210 tests in 0.359s\n\nOK\n")
        self.assertEqual(report["result"], "passed")
        self.assertFalse(report["requires_review"])

    def test_missing_log_fails_closed(self):
        self.assertEqual(diagnose("")["result"], "unknown")
        self.assertTrue(diagnose("")["requires_review"])
