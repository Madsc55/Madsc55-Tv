import copy
import hashlib
import io
import json
import stat
import unittest
import warnings
import zipfile

from madsc.github_legacy_pair_client import verify_failure_diagnostic_evidence
from madsc.legacy_pair_artifact import (DIAGNOSTIC_MEMBERS,
    DIAGNOSTIC_SNAPSHOT_NAME, verify_failure_diagnostic_artifact)
from tests.test_legacy_pair_artifact import execution


WORKFLOW = ".github/workflows/madsc-01-guvenlik.yml"


def evidence(*, outcome_update=None, snapshot_update=None, omit=None, extra=None,
             duplicate=None, symlink=None, oversized=None):
    origin = execution("Madsc55/Madsc55-Tv", "main", WORKFLOW, "2" * 40, 12, 22)
    origin["conclusion"] = "failure"
    outcome = {
        "schema": "madsc-local-process-outcome-v1", "consumer": "k1",
        "exit_code": 23, "timed_out": False,
        "behavioral_parity_accepted": False, "production_ready": False,
    }
    if outcome_update:
        outcome.update(outcome_update)
    payloads = {
        "parity-process-stdout.log": b"measured stdout\n",
        "parity-process-stderr.log": b"measured stderr\n",
        "parity-process-outcome.json":
            (json.dumps(outcome, sort_keys=True) + "\n").encode(),
    }
    snapshot = {
        "exit_code": 23, "timed_out": False,
        "outputs": {
            label: hashlib.sha256(payloads[name]).hexdigest()
            for label, (name, _limit) in DIAGNOSTIC_MEMBERS.items()
        },
        "side_effects": {},
    }
    if snapshot_update:
        snapshot_update(snapshot)
    origin["snapshot"] = copy.deepcopy(snapshot)
    payloads[DIAGNOSTIC_SNAPSHOT_NAME] = (
        json.dumps(snapshot, sort_keys=True, separators=(",", ":")) + "\n").encode()
    if oversized:
        payloads[oversized] = b"x" * (1024 * 1024 + 1)
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as bundle:
        for name, payload in payloads.items():
            if name == omit:
                continue
            if name == symlink:
                info = zipfile.ZipInfo(name)
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                bundle.writestr(info, payload)
            else:
                bundle.writestr(name, payload)
        if extra:
            bundle.writestr(extra, b"unexpected")
        if duplicate:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                bundle.writestr(duplicate, payloads[duplicate])
    archive = output.getvalue()
    artifact = {
        "id": 99, "name": "madsc-k1-failed-consumer-snapshot",
        "repository": origin["repository"], "run_id": origin["run_id"],
        "head_sha": origin["head_sha"],
        "sha256": hashlib.sha256(archive).hexdigest(),
    }
    return origin, artifact, archive


def fetcher(origin, artifact):
    calls = []

    def fetch(url, token=None):
        calls.append((url, token))
        if "/artifacts?" in url:
            return {"total_count": 1, "artifacts": [{
                "id": artifact["id"], "name": artifact["name"],
                "expired": False, "digest": "sha256:" + artifact["sha256"],
                "workflow_run": {"id": origin["run_id"],
                                 "head_sha": origin["head_sha"]},
            }]}
        if "/actions/runs/" in url:
            return {
                "id": origin["run_id"], "run_attempt": origin["run_attempt"],
                "head_sha": origin["head_sha"], "head_branch": origin["branch"],
                "path": origin["workflow_path"], "event": origin["event"],
                "status": "completed", "conclusion": origin["conclusion"],
                "repository": {"full_name": origin["repository"]},
                "head_repository": {"full_name": origin["repository"]},
            }
        return {"type": "file", "path": origin["workflow_path"],
                "sha": origin["workflow_blob_sha"]}
    return fetch, calls


class FailureDiagnosticArtifactTests(unittest.TestCase):
    def test_bytes_outcome_and_github_origin_are_bound_without_acceptance(self):
        origin, artifact, archive = evidence()
        fetch, calls = fetcher(origin, artifact)
        result = verify_failure_diagnostic_evidence(
            origin, artifact, archive, token="token", fetch=fetch)
        self.assertTrue(result["diagnostic_artifact_bytes_verified"])
        self.assertTrue(result["diagnostic_artifact_api_origin_verified"])
        self.assertEqual(result["exit_code"], 23)
        self.assertFalse(result["timed_out"])
        self.assertEqual(len(calls), 3)
        self.assertFalse(result["behavioral_parity_accepted"])
        self.assertFalse(result["production_ready"])

    def test_mutated_member_rejected_even_when_outer_archive_digest_matches(self):
        origin, artifact, archive = evidence()
        source = zipfile.ZipFile(io.BytesIO(archive))
        payloads = {info.filename: source.read(info) for info in source.infolist()}
        payloads["parity-process-stderr.log"] += b"mutated"
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w") as bundle:
            for name, payload in payloads.items():
                bundle.writestr(name, payload)
        archive = output.getvalue()
        artifact["sha256"] = hashlib.sha256(archive).hexdigest()
        with self.assertRaisesRegex(ValueError, "member digest"):
            verify_failure_diagnostic_artifact(origin, artifact, archive)

    def test_outcome_must_match_snapshot_semantics_not_only_its_hash(self):
        origin, artifact, archive = evidence(outcome_update={"exit_code": 24})
        with self.assertRaisesRegex(ValueError, "outcome does not match"):
            verify_failure_diagnostic_artifact(origin, artifact, archive)

    def test_missing_extra_duplicate_symlink_and_oversize_members_fail_closed(self):
        cases = (
            {"omit": "parity-process-stdout.log"},
            {"extra": "unexpected.txt"},
            {"duplicate": "parity-process-stdout.log"},
            {"symlink": "parity-process-stderr.log"},
            {"oversized": "parity-process-stdout.log"},
        )
        for options in cases:
            with self.subTest(options=options):
                origin, artifact, archive = evidence(**options)
                with self.assertRaises(ValueError):
                    verify_failure_diagnostic_artifact(origin, artifact, archive)

    def test_unsupported_compression_fails_closed(self):
        origin, artifact, archive = evidence()
        archive = bytearray(archive)
        # Modify the first diagnostic member's compression method in both headers.
        for signature, offset in ((b"PK\x03\x04", 8), (b"PK\x01\x02", 10)):
            start = archive.find(signature)
            self.assertGreaterEqual(start, 0)
            archive[start + offset:start + offset + 2] = (99).to_bytes(2, "little")
        archive = bytes(archive)
        artifact["sha256"] = hashlib.sha256(archive).hexdigest()
        with self.assertRaisesRegex(ValueError, "Invalid diagnostic artifact ZIP"):
            verify_failure_diagnostic_artifact(origin, artifact, archive)

    def test_artifact_identity_digest_and_failure_state_are_required(self):
        for mutation in ("name", "run_id", "sha256", "conclusion"):
            origin, artifact, archive = evidence()
            if mutation == "conclusion":
                origin[mutation] = "success"
            elif mutation == "run_id":
                artifact[mutation] = 999
            elif mutation == "sha256":
                artifact[mutation] = "f" * 64
            else:
                artifact[mutation] = "wrong"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                verify_failure_diagnostic_artifact(origin, artifact, archive)

    def test_timeout_outcome_is_preserved(self):
        def timeout_snapshot(snapshot):
            snapshot["exit_code"] = -15
            snapshot["timed_out"] = True
        origin, artifact, archive = evidence(
            outcome_update={"exit_code": -15, "timed_out": True},
            snapshot_update=timeout_snapshot)
        result = verify_failure_diagnostic_artifact(origin, artifact, archive)
        self.assertEqual(result["exit_code"], -15)
        self.assertTrue(result["timed_out"])


if __name__ == "__main__":
    unittest.main()
