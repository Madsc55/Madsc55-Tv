"""Reject JSON bool/int equality confusion in measured diagnostic outcomes."""
import json
import unittest

from madsc.legacy_pair_artifact import verify_failure_diagnostic_artifact
from tests.test_diagnostic_outcome_strictness import replace_member
from tests.test_failure_diagnostic_artifact import evidence


class DiagnosticOutcomeTypeConfusionTests(unittest.TestCase):
    def test_boolean_exit_code_cannot_impersonate_integer_one(self):
        origin, artifact, archive = evidence()
        origin["snapshot"]["exit_code"] = 1
        payload = {
            "schema": "madsc-local-process-outcome-v1",
            "consumer": "k1",
            "exit_code": True,
            "timed_out": False,
            "behavioral_parity_accepted": False,
            "production_ready": False,
        }
        archive = replace_member(
            origin, artifact, archive, "parity-process-outcome.json",
            json.dumps(payload).encode("utf-8"))
        with self.assertRaises(ValueError):
            verify_failure_diagnostic_artifact(origin, artifact, archive)

    def test_integer_timeout_zero_cannot_impersonate_boolean_false(self):
        origin, artifact, archive = evidence()
        payload = {
            "schema": "madsc-local-process-outcome-v1",
            "consumer": "k1",
            "exit_code": 23,
            "timed_out": 0,
            "behavioral_parity_accepted": False,
            "production_ready": False,
        }
        archive = replace_member(
            origin, artifact, archive, "parity-process-outcome.json",
            json.dumps(payload).encode("utf-8"))
        with self.assertRaises(ValueError):
            verify_failure_diagnostic_artifact(origin, artifact, archive)


if __name__ == "__main__":
    unittest.main()
