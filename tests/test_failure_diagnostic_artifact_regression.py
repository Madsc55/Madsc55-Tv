"""Fail-closed regression cases for separate failure diagnostic artifacts."""
import hashlib
import io
import json
import unittest
import zipfile

from madsc.legacy_pair_artifact import verify_failure_diagnostic_artifact


WORKFLOW = ".github/workflows/madsc-01-guvenlik.yml"
FILES = {
    "process_stdout": "parity-process-stdout.log",
    "process_stderr": "parity-process-stderr.log",
    "process_outcome": "parity-process-outcome.json",
}


def fixture(*, exit_code=23, timed_out=False):
    outcome = {"schema": "madsc-local-process-outcome-v1", "consumer": "k1",
               "exit_code": exit_code, "timed_out": timed_out,
               "behavioral_parity_accepted": False, "production_ready": False}
    payloads = {
        FILES["process_stdout"]: b"partial output\n",
        FILES["process_stderr"]: b"failure details\n",
        FILES["process_outcome"]: (json.dumps(outcome) + "\n").encode(),
    }
    snapshot = {"exit_code": exit_code, "timed_out": timed_out,
                "outputs": {label: hashlib.sha256(payloads[name]).hexdigest()
                            for label, name in FILES.items()}, "side_effects": {}}
    payloads["madsc-parity-snapshot.json"] = json.dumps(snapshot).encode()
    origin = {"repository": "Madsc55/Madsc55-Tv", "branch": "main",
              "workflow_path": WORKFLOW, "conclusion": "failure",
              "run_id": 123, "head_sha": "a" * 40, "snapshot": snapshot,
              "artifact": {"id": 7, "repository": "Madsc55/Madsc55-Tv"}}
    artifact = {"id": 8, "name": "madsc-k1-failed-consumer-snapshot",
                "repository": origin["repository"], "run_id": origin["run_id"],
                "head_sha": origin["head_sha"], "sha256": ""}
    return origin, artifact, payloads


def pack(artifact, payloads):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, data in payloads.items():
            bundle.writestr(name, data)
    raw = stream.getvalue()
    artifact["sha256"] = hashlib.sha256(raw).hexdigest()
    return raw


class FailureDiagnosticArtifactRegressionTests(unittest.TestCase):
    def test_measured_failure_and_timeout_are_not_acceptance(self):
        for code, timed_out in [(23, False), (124, True)]:
            with self.subTest(code=code):
                origin, artifact, files = fixture(exit_code=code, timed_out=timed_out)
                result = verify_failure_diagnostic_artifact(
                    origin, artifact, pack(artifact, files))
                self.assertTrue(result["diagnostic_artifact_bytes_verified"])
                self.assertEqual(result["exit_code"], code)
                self.assertEqual(result["timed_out"], timed_out)
                self.assertFalse(result["behavioral_parity_accepted"])
                self.assertFalse(result["production_ready"])

    def test_missing_duplicate_and_mutated_members_fail_closed(self):
        origin, artifact, files = fixture()
        for name in files:
            with self.subTest(missing=name):
                reduced = dict(files)
                del reduced[name]
                with self.assertRaises(ValueError):
                    verify_failure_diagnostic_artifact(
                        origin, artifact, pack(artifact, reduced))
        mutated = dict(files)
        mutated[FILES["process_stderr"]] = b"tampered"
        with self.assertRaises(ValueError):
            verify_failure_diagnostic_artifact(origin, artifact, pack(artifact, mutated))
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w") as bundle:
            for name, data in files.items():
                bundle.writestr(name, data)
            bundle.writestr(FILES["process_stderr"], b"duplicate")
        raw = stream.getvalue()
        artifact["sha256"] = hashlib.sha256(raw).hexdigest()
        with self.assertRaises(ValueError):
            verify_failure_diagnostic_artifact(origin, artifact, raw)

    def test_outcome_mismatch_and_wrong_origin_fail_closed(self):
        origin, artifact, files = fixture()
        outcome = json.loads(files[FILES["process_outcome"]])
        outcome["exit_code"] = 0
        files[FILES["process_outcome"]] = json.dumps(outcome).encode()
        with self.assertRaises(ValueError):
            verify_failure_diagnostic_artifact(origin, artifact, pack(artifact, files))
        origin, artifact, files = fixture()
        artifact["id"] = origin["artifact"]["id"]
        with self.assertRaises(ValueError):
            verify_failure_diagnostic_artifact(origin, artifact, pack(artifact, files))

    def test_symlink_and_oversize_member_fail_closed(self):
        origin, artifact, files = fixture()
        for case in ("symlink", "oversize"):
            with self.subTest(case=case):
                stream = io.BytesIO()
                with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
                    for name, data in files.items():
                        if name == FILES["process_stdout"] and case == "oversize":
                            data = b"x" * (1024 * 1024 + 1)
                        if name == FILES["process_stdout"] and case == "symlink":
                            info = zipfile.ZipInfo(name)
                            info.create_system = 3
                            info.external_attr = (0o120777 << 16)
                            bundle.writestr(info, data)
                        else:
                            bundle.writestr(name, data)
                raw = stream.getvalue()
                artifact["sha256"] = hashlib.sha256(raw).hexdigest()
                with self.assertRaises(ValueError):
                    verify_failure_diagnostic_artifact(origin, artifact, raw)


if __name__ == "__main__":
    unittest.main()
