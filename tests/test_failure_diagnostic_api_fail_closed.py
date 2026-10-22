"""Independent fail-closed API-origin checks for diagnostic artifacts."""
import unittest

from madsc.github_legacy_pair_client import (fetch_verified_execution_origin,
    verify_failure_diagnostic_evidence)
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


    def test_invalid_sha_and_workflow_paths_rejected_before_network(self):
        origin, artifact, _archive = evidence()
        origin["artifact"] = artifact
        cases = (
            ("head_sha", "g" * 40),
            ("head_sha", "A" * 40),
            ("workflow_path", ".github/workflows/../secret.yml"),
            ("workflow_path", ".github/workflows/./safe.yml"),
            ("workflow_path", ".github/workflows//safe.yml"),
            ("workflow_path", ".github/workflows/safe.txt"),
        )
        for key, value in cases:
            declared = dict(origin)
            declared[key] = value
            calls = []

            def fetch(url, token=None):
                calls.append(url)
                raise AssertionError("Network fetch must not be attempted")

            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                fetch_verified_execution_origin(declared, fetch=fetch)
            self.assertEqual(calls, [])


    def test_duplicate_or_invalid_artifact_ids_are_rejected(self):
        for mismatch in ("same_id_different_name", "boolean_id", "missing_id"):
            origin, artifact, archive = evidence()
            original_fetch, _ = fetcher(origin, artifact)

            def fetch(url, token=None):
                data = original_fetch(url, token=token)
                if "/artifacts?" in url:
                    if mismatch == "same_id_different_name":
                        duplicate = dict(data["artifacts"][0])
                        duplicate["name"] = "unrelated-artifact"
                        data["artifacts"].append(duplicate)
                        data["total_count"] = 2
                    elif mismatch == "boolean_id":
                        data["artifacts"][0]["id"] = True
                    elif mismatch == "missing_id":
                        del data["artifacts"][0]["id"]
                return data

            with self.subTest(mismatch=mismatch), self.assertRaises(ValueError):
                verify_failure_diagnostic_evidence(
                    origin, artifact, archive, fetch=fetch)


    def test_boolean_run_and_artifact_identity_values_rejected(self):
        for mismatch in ("run_id", "run_attempt", "workflow_run_id",
                         "declared_artifact_id"):
            origin, artifact, archive = evidence()
            original_fetch, _ = fetcher(origin, artifact)
            if mismatch == "declared_artifact_id":
                artifact["id"] = True

            def fetch(url, token=None):
                data = original_fetch(url, token=token)
                if "/artifacts?" in url and mismatch == "workflow_run_id":
                    data["artifacts"][0]["workflow_run"]["id"] = True
                elif "/actions/runs/" in url and "/artifacts?" not in url:
                    if mismatch == "run_id":
                        data["id"] = True
                    elif mismatch == "run_attempt":
                        data["run_attempt"] = True
                return data

            with self.subTest(mismatch=mismatch), self.assertRaises(ValueError):
                verify_failure_diagnostic_evidence(
                    origin, artifact, archive, fetch=fetch)


    def test_artifact_repository_and_branch_metadata_must_match_run(self):
        for mismatch in ("repository_id", "head_repository_id", "head_branch"):
            origin, artifact, archive = evidence()
            original_fetch, _ = fetcher(origin, artifact)

            def fetch(url, token=None):
                data = original_fetch(url, token=token)
                if "/artifacts?" in url:
                    workflow_run = data["artifacts"][0]["workflow_run"]
                    if mismatch == "repository_id":
                        workflow_run["repository_id"] = 999
                    elif mismatch == "head_repository_id":
                        workflow_run["head_repository_id"] = 999
                    else:
                        workflow_run["head_branch"] = "other-branch"
                elif "/actions/runs/" in url:
                    data["repository"]["id"] = 123
                    data["head_repository"]["id"] = 123
                return data

            with self.subTest(mismatch=mismatch), self.assertRaises(ValueError):
                verify_failure_diagnostic_evidence(
                    origin, artifact, archive, fetch=fetch)

    def test_matching_artifact_repository_and_branch_metadata_is_allowed(self):
        origin, artifact, archive = evidence()
        original_fetch, _ = fetcher(origin, artifact)

        def fetch(url, token=None):
            data = original_fetch(url, token=token)
            if "/artifacts?" in url:
                workflow_run = data["artifacts"][0]["workflow_run"]
                workflow_run.update(repository_id=123,
                                    head_repository_id=123,
                                    head_branch=origin["branch"])
            elif "/actions/runs/" in url:
                data["repository"]["id"] = 123
                data["head_repository"]["id"] = 123
            return data

        result = verify_failure_diagnostic_evidence(
            origin, artifact, archive, fetch=fetch)
        self.assertTrue(result["diagnostic_artifact_api_origin_verified"])
        self.assertFalse(result["behavioral_parity_accepted"])



if __name__ == "__main__":
    unittest.main()
