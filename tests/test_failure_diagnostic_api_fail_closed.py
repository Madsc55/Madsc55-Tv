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

    def test_missing_ambiguous_or_expired_diagnostic_artifact_rejected(self):
        for mismatch in ("missing", "duplicate", "expired", "workflow_blob"):
            origin, artifact, archive = evidence()
            original_fetch, _ = fetcher(origin, artifact)

            def fetch(url, token=None):
                data = original_fetch(url, token=token)
                if "/artifacts?" in url:
                    if mismatch == "missing":
                        data["artifacts"] = []
                        data["total_count"] = 0
                    elif mismatch == "duplicate":
                        data["artifacts"].append(dict(data["artifacts"][0]))
                        data["total_count"] = 2
                    elif mismatch == "expired":
                        data["artifacts"][0]["expired"] = True
                elif mismatch == "workflow_blob" and "/contents/" in url:
                    data["sha"] = "f" * 40
                return data

            with self.subTest(mismatch=mismatch), self.assertRaises(ValueError):
                verify_failure_diagnostic_evidence(
                    origin, artifact, archive, fetch=fetch)


    def test_incomplete_api_listing_and_run_state_are_rejected(self):
        for mismatch in ("total_count", "run_status", "run_conclusion", "run_repository"):
            origin, artifact, archive = evidence()
            original_fetch, _ = fetcher(origin, artifact)

            def fetch(url, token=None):
                data = original_fetch(url, token=token)
                if "/artifacts?" in url and mismatch == "total_count":
                    data["total_count"] = 2
                elif "/actions/runs/" in url and "/artifacts?" not in url:
                    if mismatch == "run_status":
                        data["status"] = "in_progress"
                    elif mismatch == "run_conclusion":
                        data["conclusion"] = "success"
                    elif mismatch == "run_repository":
                        data["repository"]["full_name"] = "other/repo"
                return data

            with self.subTest(mismatch=mismatch), self.assertRaises(ValueError):
                verify_failure_diagnostic_evidence(
                    origin, artifact, archive, fetch=fetch)


    def test_run_head_repository_branch_event_and_workflow_mismatch_rejected(self):
        for mismatch in ("head_repository", "head_branch", "event", "path"):
            origin, artifact, archive = evidence()
            original_fetch, _ = fetcher(origin, artifact)

            def fetch(url, token=None):
                data = original_fetch(url, token=token)
                if "/actions/runs/" in url and "/artifacts?" not in url:
                    if mismatch == "head_repository":
                        data["head_repository"]["full_name"] = "other/repo"
                    elif mismatch == "head_branch":
                        data["head_branch"] = "untrusted"
                    elif mismatch == "event":
                        data["event"] = "workflow_dispatch"
                    elif mismatch == "path":
                        data["path"] = ".github/workflows/other.yml"
                return data

            with self.subTest(mismatch=mismatch), self.assertRaises(ValueError):
                verify_failure_diagnostic_evidence(
                    origin, artifact, archive, fetch=fetch)


    def test_malformed_api_record_shapes_rejected_as_value_errors(self):
        for mismatch in ("artifact_item", "artifact_workflow_run",
                         "run_repository_object", "head_repository_object"):
            origin, artifact, archive = evidence()
            original_fetch, _ = fetcher(origin, artifact)

            def fetch(url, token=None):
                data = original_fetch(url, token=token)
                if "/artifacts?" in url:
                    if mismatch == "artifact_item":
                        data["artifacts"].append(None)
                        data["total_count"] = 2
                    elif mismatch == "artifact_workflow_run":
                        data["artifacts"][0]["workflow_run"] = "invalid"
                elif "/actions/runs/" in url:
                    if mismatch == "run_repository_object":
                        data["repository"] = "invalid"
                    elif mismatch == "head_repository_object":
                        data["head_repository"] = "invalid"
                return data

            with self.subTest(mismatch=mismatch), self.assertRaises(ValueError):
                verify_failure_diagnostic_evidence(
                    origin, artifact, archive, fetch=fetch)



if __name__ == "__main__":
    unittest.main()
