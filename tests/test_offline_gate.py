import unittest
import subprocess
import io
import json
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import patch
from madsc.offline_gate import main

class OfflineGateTests(unittest.TestCase):
    @patch("madsc.offline_gate.subprocess.run")
    def test_success(self, run):
        run.return_value.returncode = 0
        run.return_value.stdout = ""
        run.return_value.stderr = "Ran 73 tests in 0.123s\\n\\nOK"
        self.assertEqual(main(), 0)
        self.assertTrue(run.call_args.kwargs["capture_output"])
        self.assertFalse(run.call_args.kwargs["check"])
    @patch("madsc.offline_gate.subprocess.run")
    def test_zero_discovered_tests_never_pass(self, run):
        run.return_value.returncode = 0
        run.return_value.stdout = ""
        run.return_value.stderr = "Ran 0 tests in 0.000s\\n\\nOK"
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(), 1)
        report = json.loads(output.getvalue())
        self.assertEqual(report["tests_discovered"], 0)
        self.assertEqual(report["test_exit_code"], 2)
        self.assertFalse(report["tests_passed"])

    @patch("madsc.offline_gate.subprocess.run")
    def test_missing_unittest_summary_never_passes(self, run):
        run.return_value.returncode = 0
        run.return_value.stdout = ""
        run.return_value.stderr = ""
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main(), 1)

    @patch("madsc.offline_gate.subprocess.run")
    def test_failure_is_not_hidden(self, run):
        run.return_value.returncode = 1
        run.return_value.stdout = ""
        run.return_value.stderr = "test failure"
        self.assertEqual(main(), 1)

    @patch("madsc.offline_gate.subprocess.run")
    def test_timeout_is_failure_with_diagnostics(self, run):
        run.side_effect = subprocess.TimeoutExpired(["python", "-m", "unittest"], 180,
                                                  output=b"partial output", stderr=b"timeout details")
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            self.assertEqual(main(), 1)
        report = json.loads(stdout.getvalue())
        self.assertEqual(report["test_exit_code"], 124)
        self.assertTrue(report["timed_out"])
        self.assertFalse(report["tests_passed"])
        self.assertIn("partial output", stderr.getvalue())
        self.assertIn("timeout details", stderr.getvalue())

if __name__ == "__main__":
    unittest.main()
