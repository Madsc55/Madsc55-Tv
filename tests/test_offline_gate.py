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
        self.assertEqual(main(), 0)
        self.assertTrue(run.call_args.kwargs["capture_output"])
        self.assertFalse(run.call_args.kwargs["check"])
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
