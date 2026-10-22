"""Actual producer/serialized-file/consumer checks for all five isolated stages."""
import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from madsc.offline_five_gate import assess_report_roundtrip
from madsc.offline_gate import main


class FiveReportRoundtripTests(unittest.TestCase):
    def test_actual_five_producers_are_consumed_without_modifying_bytes(self):
        report = assess_report_roundtrip()
        self.assertTrue(report['passed'])
        self.assertEqual(report['reports_written'], 5)
        self.assertEqual(len(report['reports_sha256']), 5)
        self.assertTrue(report['consumer_preserved_report_bytes'])
        self.assertFalse(report['independent_execution_evidence'])
        self.assertFalse(report['production_ready'])

    def test_missing_producer_output_is_not_accepted(self):
        with patch('madsc.core.run', return_value={}):
            with self.assertRaises(FileNotFoundError):
                assess_report_roundtrip()

    def test_bad_report_roundtrip_blocks_otherwise_green_gate(self):
        with (patch('madsc.offline_gate.subprocess.run') as run,
              patch('madsc.offline_five_gate.assess_report_roundtrip',
                    return_value={'passed': False})):
            run.return_value.returncode = 0
            run.return_value.stdout = ''
            run.return_value.stderr = 'Ran 754 tests in 1s\nOK'
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(), 1)
            report = json.loads(output.getvalue())
            self.assertEqual(report['test_exit_code'], 5)
            self.assertTrue(report['tests_passed'])
            self.assertFalse(report['all_offline_gates_passed'])
            self.assertFalse(report['five_report_roundtrip_passed'])
