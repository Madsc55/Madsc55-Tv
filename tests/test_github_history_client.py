"""Mocked REST tests ensure three independent GitHub reads and fail closed."""
import unittest
from madsc.github_history_client import verify_live_github_origin

A = "a" * 40
B = "b" * 40
REPO = "Madsc55/Madsc55-Tv"
PATH = ".github/workflows/madsc-05-bakim.yml"


class GithubHistoryClientTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {"source_run_id": "123", "source_commit_sha": A}
        self.run = {"id": 123, "head_sha": A, "repository": {"full_name": REPO},
                    "head_repository": {"full_name": REPO}, "head_branch": "main",
                    "path": PATH, "status": "completed", "conclusion": "success",
                    "event": "push"}
        self.artifact = {"id": 456, "name": "madsc-k2-history-source",
                         "expired": False, "workflow_run": {"id": 123, "head_sha": A}}

    def invoke(self, *, status="ahead", total=1, artifacts=None):
        calls = []
        def fetch(url, *, token):
            calls.append(url)
            if "/compare/" in url:
                return {"status": status}
            if "/artifacts?" in url:
                return {"total_count": total,
                        "artifacts": [self.artifact] if artifacts is None else artifacts}
            return self.run
        result = verify_live_github_origin(
            self.manifest, repository=REPO, branch="main",
            workflow_path=PATH, current_sha=B, fetch=fetch)
        return result, calls

    def test_three_independent_github_reads(self):
        result, calls = self.invoke()
        self.assertTrue(result["github_origin_verified"])
        self.assertEqual(len(calls), 3)
        self.assertTrue(any("/compare/" in url for url in calls))

    def test_incomplete_artifact_page_and_nonancestor_rejected(self):
        for kwargs in ({"total": 101}, {"status": "diverged"},
                       {"artifacts": []}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.invoke(**kwargs)

    def test_invalid_run_id_rejected_before_network(self):
        with self.assertRaises(ValueError):
            verify_live_github_origin(
                {"source_run_id": "../123", "source_commit_sha": A},
                repository=REPO, branch="main", workflow_path=PATH,
                current_sha=B, fetch=lambda *args, **kwargs: self.fail("network called"))


if __name__ == "__main__":
    unittest.main()
