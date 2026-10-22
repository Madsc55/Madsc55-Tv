"""Independent fail-closed API-origin checks for diagnostic artifacts."""
import unittest

from madsc.github_legacy_pair_client import verify_failure_diagnostic_evidence
from tests.test_failure_diagnostic_artifact import evidence, fetcher


class DiagnosticApiFailClosedTests(unittest.TestCase):
    def test_mismatched_api_run_and_artifact_identity_are_rejected(self):
        for mismatch in ("run_attempt", "run_id", "head_sha", "artifact_digest"):
            origin, artifact, archive = evidence()
            original_fetch, _ = fetcher(origin, artifact)

            def fetch(url, token=None):
                data = original_fetch(url, token=token)
                if mismatch == "run_attempt" and "/actions/runs/" in url and "/artifacts?" not in url:
                    data["run_attempt"] += 1
                elif mismatch == "run_id" and "/artifacts?" in url:
                    data["artifacts"][0]["workflow_run"]["id"] += 1
                elif mismatch == "head_sha" and "/artifacts?" in url:
                    data["artifacts"][0]["workflow_run"]["head_sha"] = "f" * 40
                elif mismatch == "artifact_digest" and "/artifacts?" in url:
                    data["artifacts"][0]["digest"] = "sha256:" + "f" * 64
                return data

            with self.subTest(mismatch=mismatch), self.assertRaises(ValueError):
                verify_failure_diagnostic_evidence(
                    origin, artifact, archive, fetch=fetch)


if __name__ == "__main__":
    unittest.main()
