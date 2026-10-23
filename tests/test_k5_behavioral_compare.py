"""Regression tests for independent K5 workflow evidence comparison."""
import hashlib
import unittest

from madsc.k5_behavioral_compare import compare


def digest(data=b""):
    return hashlib.sha256(data).hexdigest()


def record():
    return {
        "exit_code": 0, "stdout_sha256": digest(), "stderr_sha256": digest(),
        "artifacts": {"report.json": digest(b"report")},
        "side_effects": {}, "timed_out": False, "retry_count": 0,
    }


def evidence():
    return {
        "workflow": ".github/workflows/example.yml",
        "fixture_sha256": digest(b"fixture"),
        "legacy": record(), "new": record(),
        "independent_runs": True, "isolated_fixture": True,
    }


class BehavioralCompareTests(unittest.TestCase):
    def test_identical_independent_fixture_evidence(self):
        result = compare(evidence())
        self.assertTrue(result["matched_evidence"])
        self.assertFalse(result["accepted"])
        self.assertTrue(result["requires_independent_execution_verification"])

    def test_output_mismatch_fails_closed(self):
        doc = evidence()
        doc["new"]["stdout_sha256"] = digest(b"different")
        self.assertIn("mismatch:stdout_sha256", compare(doc)["errors"])

    def test_artifact_mismatch_fails_closed(self):
        doc = evidence()
        doc["new"]["artifacts"] = {}
        self.assertIn("mismatch:artifacts", compare(doc)["errors"])

    def test_retry_and_timeout_mismatch(self):
        for field, value in (("retry_count", 1), ("timed_out", True)):
            with self.subTest(field=field):
                doc = evidence()
                doc["new"][field] = value
                self.assertIn("mismatch:" + field, compare(doc)["errors"])

    def test_unproven_independence_rejected(self):
        doc = evidence()
        doc["independent_runs"] = False
        self.assertFalse(compare(doc)["accepted"])

    def test_unproven_isolation_rejected(self):
        doc = evidence()
        doc["isolated_fixture"] = False
        self.assertFalse(compare(doc)["accepted"])

    def test_missing_or_malformed_evidence_rejected(self):
        for mutation in ("missing", "bad_digest", "extra"):
            with self.subTest(mutation=mutation):
                doc = evidence()
                if mutation == "missing":
                    del doc["legacy"]["exit_code"]
                elif mutation == "bad_digest":
                    doc["legacy"]["stdout_sha256"] = "invalid"
                else:
                    doc["new"]["unrecognized"] = True
                self.assertFalse(compare(doc)["accepted"])

    def test_exit_code_and_side_effect_mismatch(self):
        for field, value in (("exit_code", 2), ("side_effects", {"created.txt": digest(b"created")})):
            with self.subTest(field=field):
                doc = evidence()
                doc["new"][field] = value
                self.assertIn("mismatch:" + field, compare(doc)["errors"])

    def test_workflow_path_and_fixture_digest_are_required(self):
        doc = evidence()
        doc["workflow"] = "../outside.yml"
        result = compare(doc)
        self.assertFalse(result["matched_evidence"])
        doc = evidence()
        doc["fixture_sha256"] = "bad"
        self.assertIn("invalid_fixture_digest", compare(doc)["errors"])

    def test_boolean_exit_code_rejected(self):
        doc = evidence()
        doc["legacy"]["exit_code"] = False
        self.assertFalse(compare(doc)["accepted"])


if __name__ == "__main__":
    unittest.main()
