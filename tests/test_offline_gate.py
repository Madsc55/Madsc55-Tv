import unittest
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

if __name__ == "__main__":
    unittest.main()
