"""Bulk gate must include the newest installation contract (read-only)."""
import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from madsc.offline_gate import main


class InstallationGateIntegrationTests(unittest.TestCase):
    @patch("madsc.five_stage_installation.assess_installation")
    @patch("madsc.offline_gate.subprocess.run")
    def test_missing_installation_contract_blocks_green_unit_tests(self, run, installation):
        run.return_value.returncode = 0
        run.return_value.stdout = ""
        run.return_value.stderr = "Ran 759 tests in 0.100s\n\nOK"
        installation.side_effect = ValueError("K1-K5 inventory drift")
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(), 1)
        report = json.loads(output.getvalue())
        self.assertFalse(report["five_stage_installation_inventory_passed"])
        self.assertEqual(report["five_stage_installation_inventory_error"], "ValueError")
        self.assertFalse(report["all_offline_gates_passed"])
        self.assertEqual(report["test_exit_code"], 6)


if __name__ == "__main__":
    unittest.main()
