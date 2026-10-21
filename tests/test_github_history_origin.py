"""Independent GitHub origin contract: positive and fail-closed scenarios."""
import unittest
from madsc.github_history_origin import verify_github_origin

A = "a" * 40
B = "b" * 40
REPO = "Madsc55/Madsc55-Tv"
PATH = ".github/workflows/madsc-05-bakim.yml"


class GithubHistoryOriginTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {"source_run_id": "123", "source_commit_sha": A}
        self.run = {"id": 123, "head_sha": A, "repository": {"full_name": REPO},
                    "head_repository": {"full_name": REPO}, "head_branch": "main",
                    "path": PATH, "status": "completed", "conclusion": "success",
                    "event": "push"}
        self.artifact = {"id": 456, "name": "madsc-k2-history-source",
                         "expired": False, "workflow_run": {"id": 123, "head_sha": A}}

    def verify(self, *, manifest=None, run=None, artifacts=None, verdict="ahead"):
        return verify_github_origin(
            self.manifest if manifest is None else manifest,
            self.run if run is None else run,
            [self.artifact] if artifacts is None else artifacts,
            repository=REPO, branch="main", workflow_path=PATH,
            current_sha=B, ancestry_verdict=verdict)

    def test_valid_independent_run_artifact_and_ancestry(self):
        result = self.verify()
        self.assertTrue(result["github_origin_verified"])
        self.assertFalse(result["production_ready"])

    def test_wrong_branch_workflow_repo_status_commit_or_run_rejected(self):
        for field, value in (
                ("head_branch", "other"),
                ("path", ".github/workflows/untrusted.yml"),
                ("status", "in_progress"),
                ("conclusion", "failure"),
                ("head_sha", B),
                ("id", 999),
                ("event", "pull_request"),
                ("repository", {"full_name": "other/repo"}),
                ("head_repository", {"full_name": "fork/repo"})):
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.verify(run={**self.run, field: value})

    def test_non_ancestor_and_unverified_comparison_rejected(self):
        for verdict in ("behind", "diverged", None, "unknown"):
            with self.subTest(verdict=verdict), self.assertRaises(ValueError):
                self.verify(verdict=verdict)

    def test_expired_wrong_run_duplicate_and_missing_artifacts_rejected(self):
        for artifacts in (
                [], [self.artifact, self.artifact],
                [{**self.artifact, "expired": True}],
                [{**self.artifact, "workflow_run": {"id": 999, "head_sha": A}}],
                [{**self.artifact, "workflow_run": {"id": 123, "head_sha": B}}]):
            with self.subTest(artifacts=artifacts), self.assertRaises(ValueError):
                self.verify(artifacts=artifacts)

    def test_manifest_identity_mismatch_rejected(self):
        for change in ({"source_run_id": "999"}, {"source_commit_sha": B}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.verify(manifest={**self.manifest, **change})


if __name__ == "__main__":
    unittest.main()
