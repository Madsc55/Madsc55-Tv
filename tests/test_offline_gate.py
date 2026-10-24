import unittest
import subprocess
import io
import json
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import patch
from madsc.offline_gate import main

class OfflineGateTests(unittest.TestCase):
    @patch("madsc.offline_gate.subprocess.run")
    def test_fixed_unittest_child_disables_bytecode_writes(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, "", "Ran 1 test in 0.1s\nOK\n")
        with patch("madsc.offline_five_gate.assess_all", return_value={
                "passed": True, "categories": {
                    name: {"success": True, "production_ready": False}
                    for name in ("k1", "k2", "k3", "k4", "k5")}}), \
             patch("sys.stdout", new_callable=io.StringIO):
            main()
        command = run.call_args.args[0]
        self.assertEqual(command[1:3], ["-B", "-m"])
        self.assertEqual(run.call_args.kwargs["cwd"],
                         Path(__file__).resolve().parents[1])
    @patch("madsc.offline_gate.subprocess.run")
    def test_success(self, run):
        run.return_value.returncode = 0
        run.return_value.stdout = ""
        run.return_value.stderr = "Ran 73 tests in 0.123s\n\nOK"
        self.assertEqual(main(), 0)
        self.assertTrue(run.call_args.kwargs["capture_output"])
        self.assertFalse(run.call_args.kwargs["check"])
    @patch("madsc.workflow_consolidation.contract_gate")
    @patch("madsc.offline_gate.subprocess.run")
    def test_lost_operational_contract_blocks_green_tests(self, run, contract):
        run.return_value.returncode = 0
        run.return_value.stdout = ""
        run.return_value.stderr = "Ran 73 tests in 0.123s\n\nOK"
        contract.return_value = {"pass": False, "blocking_contract_gaps": [
            {"source": "madsc-legacy-99-bulk-audit.yml", "gaps": ["timeout"]}]}
        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(io.StringIO()):
            self.assertEqual(main(), 1)
        report = json.loads(output.getvalue())
        self.assertTrue(report["tests_passed"])
        self.assertFalse(report["all_offline_gates_passed"])
        self.assertEqual(report["test_exit_code"], 4)
        self.assertEqual(report["operational_contract_gate"], contract.return_value)

    @patch("madsc.offline_five_gate.assess_all")
    @patch("madsc.offline_gate.subprocess.run")
    def test_five_stage_failure_blocks_green_unittest(self, run, five):
        run.return_value.returncode = 0
        run.return_value.stdout = ""
        run.return_value.stderr = "Ran 73 tests in 0.123s\n\nOK"
        five.return_value = {"fixture_gate_passed": False, "categories": {"k3": "failure"},
                             "errors": {"k3": "invalid_fixture_evidence"}}
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(), 1)
        report = json.loads(output.getvalue())
        self.assertEqual(report["test_exit_code"], 3)
        self.assertFalse(report["five_stage_fixture_gate_passed"])
        self.assertTrue(report["tests_passed"])
        self.assertFalse(report["all_offline_gates_passed"])
        self.assertFalse(report["production_acceptance"])

    @patch("madsc.offline_five_gate.assess_all")
    @patch("madsc.offline_gate.subprocess.run")
    def test_both_gates_required_for_success(self, run, five):
        run.return_value.returncode = 0
        run.return_value.stdout = ""
        run.return_value.stderr = "Ran 73 tests in 0.123s\n\nOK"
        five.return_value = {"fixture_gate_passed": True, "categories_checked": 5,
                             "production_ready": False, "production_writes": False, "categories": {
            key: "success" for key in ("k1", "k2", "k3", "k4", "k5")}, "errors": {}}
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(), 0)
        report = json.loads(output.getvalue())
        self.assertTrue(report["five_stage_fixture_gate_passed"])
        self.assertTrue(report["all_offline_gates_passed"])
        self.assertFalse(report["production_acceptance"])

    @patch("madsc.offline_five_gate.assess_all")
    @patch("madsc.offline_gate.subprocess.run")
    def test_incomplete_five_stage_evidence_fails_closed(self, run, five):
        run.return_value.returncode = 0
        run.return_value.stdout = ""
        run.return_value.stderr = "Ran 73 tests in 0.123s\n\nOK"
        five.return_value = {"fixture_gate_passed": True, "categories_checked": 4,
                             "categories": {key: "success" for key in ("k1", "k2", "k3", "k4")},
                             "production_ready": False, "production_writes": False}
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(), 1)
        self.assertFalse(json.loads(output.getvalue())["five_stage_fixture_gate_passed"])

    @patch("madsc.offline_gate.subprocess.run")
    def test_zero_discovered_tests_never_pass(self, run):
        run.return_value.returncode = 0
        run.return_value.stdout = ""
        run.return_value.stderr = "Ran 0 tests in 0.000s\n\nOK"
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
