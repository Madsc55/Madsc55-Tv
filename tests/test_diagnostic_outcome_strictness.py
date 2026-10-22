"""Extra negative cases for measured diagnostic outcome semantics."""
import hashlib
import io
import json
import unittest
import zipfile

from madsc.legacy_pair_artifact import verify_failure_diagnostic_artifact
from tests.test_failure_diagnostic_artifact import evidence


def replace_member(origin, artifact, archive, name, value):
    with zipfile.ZipFile(io.BytesIO(archive)) as source:
        files = {info.filename: source.read(info) for info in source.infolist()}
    files[name] = value
    if name == "parity-process-outcome.json":
        origin["snapshot"]["outputs"]["process_outcome"] = hashlib.sha256(value).hexdigest()
        files["madsc-parity-snapshot.json"] = (
            json.dumps(origin["snapshot"], sort_keys=True, separators=(",", ":")) + "\n"
        ).encode()
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as target:
        for path, payload in files.items():
            target.writestr(path, payload)
    raw = stream.getvalue()
    artifact["sha256"] = hashlib.sha256(raw).hexdigest()
    return raw


class DiagnosticOutcomeStrictnessTests(unittest.TestCase):
    def test_duplicate_outcome_json_keys_are_rejected_even_with_valid_hashes(self):
        origin, artifact, archive = evidence()
        payload = (b'{"schema":"madsc-local-process-outcome-v1",'
                   b'"consumer":"k1","exit_code":23,"exit_code":23,'
                   b'"timed_out":false,"behavioral_parity_accepted":false,'
                   b'"production_ready":false}')
        archive = replace_member(
            origin, artifact, archive, "parity-process-outcome.json", payload)
        with self.assertRaises(ValueError):
            verify_failure_diagnostic_artifact(origin, artifact, archive)

    def test_github_timeout_conclusion_requires_measured_timeout(self):
        origin, artifact, archive = evidence()
        origin["conclusion"] = "timed_out"
        with self.assertRaises(ValueError):
            verify_failure_diagnostic_artifact(origin, artifact, archive)

    def test_outcome_consumer_identity_cannot_be_substituted(self):
        origin, artifact, archive = evidence()
        outcome = {"schema": "madsc-local-process-outcome-v1", "consumer": "k5",
                   "exit_code": 23, "timed_out": False,
                   "behavioral_parity_accepted": False, "production_ready": False}
        archive = replace_member(
            origin, artifact, archive, "parity-process-outcome.json",
            json.dumps(outcome).encode())
        with self.assertRaises(ValueError):
            verify_failure_diagnostic_artifact(origin, artifact, archive)


if __name__ == "__main__":
    unittest.main()
