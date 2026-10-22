import unittest

from madsc.github_legacy_pair_client import verify_provenance_pair_api


LEGACY_PATH = ".github/workflows/example.yml"
LEGACY_BLOB = "1" * 40
NEW_PATH = ".github/workflows/madsc-05-bakim.yml"


def origin(repository, branch, workflow_path, workflow_blob, run_id, artifact_id):
    snapshot = {"exit_code": 0, "timed_out": False,
                "outputs": {"report": "d" * 64}, "side_effects": {}}
    return {
        "repository": repository, "branch": branch,
        "workflow_path": workflow_path, "workflow_blob_sha": workflow_blob,
        "run_id": run_id, "run_attempt": 1, "head_sha": ("a" if run_id == 101 else "b") * 40,
        "event": "workflow_dispatch", "conclusion": "success",
        "artifact": {"id": artifact_id, "name": "comparison-evidence",
                     "repository": repository, "run_id": run_id,
                     "head_sha": ("a" if run_id == 101 else "b") * 40,
                     "sha256": "c" * 64},
        "input_sha256": "e" * 64, "snapshot": snapshot,
    }


class GithubLegacyPairClientTests(unittest.TestCase):
    def setUp(self):
        self.pair = {
            "legacy": origin("Madsc55/madsc-tv", "madsc/bes-sistem-toplu-birlestirme",
                             LEGACY_PATH, LEGACY_BLOB, 101, 201),
            "replacement": origin("Madsc55/Madsc55-Tv", "main", NEW_PATH,
                                  "2" * 40, 102, 202),
        }

    def fetcher(self, *, mutate=None):
        calls = []
        def fetch(url, *, token):
            calls.append(url)
            current = self.pair["legacy"] if "/Madsc55/madsc-tv/" in url else self.pair["replacement"]
            if "/artifacts?" in url:
                value = {"total_count": 1, "artifacts": [{
                    "id": current["artifact"]["id"], "name": current["artifact"]["name"],
                    "expired": False, "digest": "sha256:" + current["artifact"]["sha256"],
                    "workflow_run": {"id": current["run_id"], "head_sha": current["head_sha"]},
                }]}
            elif "/contents/" in url:
                value = {"type": "file", "path": current["workflow_path"],
                         "sha": current["workflow_blob_sha"]}
            else:
                value = {"id": current["run_id"], "run_attempt": current["run_attempt"],
                         "head_sha": current["head_sha"], "head_branch": current["branch"],
                         "path": current["workflow_path"], "event": current["event"],
                         "status": "completed", "conclusion": current["conclusion"],
                         "repository": {"full_name": current["repository"]},
                         "head_repository": {"full_name": current["repository"]}}
            return mutate(url, value) if mutate else value
        return fetch, calls

    def test_six_independent_reads_verify_both_origins_without_acceptance(self):
        fetch, calls = self.fetcher()
        result = verify_provenance_pair_api(
            LEGACY_PATH, LEGACY_BLOB, self.pair, fetch=fetch)
        self.assertEqual(len(calls), 6)
        self.assertTrue(result["independent_origin_api_verified"])
        self.assertTrue(result["snapshot_fields_match"])
        self.assertFalse(result["behavioral_parity_accepted"])
        self.assertFalse(result["production_ready"])

    def test_artifact_run_attempt_must_match_when_api_supplies_it(self):
        for value in (0, True, 2, "1"):
            def mismatched_attempt(url, record):
                if "/artifacts?" in url:
                    record["artifacts"][0]["workflow_run"]["run_attempt"] = value
                return record
            fetch, _ = self.fetcher(mutate=mismatched_attempt)
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "run attempt"):
                verify_provenance_pair_api(LEGACY_PATH, LEGACY_BLOB, self.pair, fetch=fetch)

    def test_artifact_event_must_match_when_api_supplies_it(self):
        for value in ("push", "schedule", None, True):
            def conflicting_event(url, record):
                if "/artifacts?" in url:
                    record["artifacts"][0]["workflow_run"]["event"] = value
                return record
            fetch, _ = self.fetcher(mutate=conflicting_event)
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "event origin"):
                verify_provenance_pair_api(LEGACY_PATH, LEGACY_BLOB, self.pair, fetch=fetch)

    def test_artifact_run_status_and_conclusion_must_agree(self):
        for field, value in (("status", "in_progress"), ("status", None),
                             ("conclusion", "failure"), ("conclusion", None)):
            def conflicting_result(url, record):
                if "/artifacts?" in url:
                    record["artifacts"][0]["workflow_run"][field] = value
                return record
            fetch, _ = self.fetcher(mutate=conflicting_result)
            with self.subTest(field=field, value=value), self.assertRaisesRegex(ValueError, field):
                verify_provenance_pair_api(LEGACY_PATH, LEGACY_BLOB, self.pair, fetch=fetch)

    def test_missing_digest_and_wrong_workflow_blob_fail_closed(self):
        def missing_digest(url, value):
            if "/artifacts?" in url:
                value["artifacts"][0].pop("digest")
            return value
        fetch, _ = self.fetcher(mutate=missing_digest)
        with self.assertRaises(ValueError):
            verify_provenance_pair_api(LEGACY_PATH, LEGACY_BLOB, self.pair, fetch=fetch)

        def wrong_blob(url, value):
            if "/contents/" in url:
                value["sha"] = "f" * 40
            return value
        fetch, _ = self.fetcher(mutate=wrong_blob)
        with self.assertRaises(ValueError):
            verify_provenance_pair_api(LEGACY_PATH, LEGACY_BLOB, self.pair, fetch=fetch)

    def test_incomplete_artifact_page_and_wrong_run_repository_fail_closed(self):
        def incomplete(url, value):
            if "/artifacts?" in url:
                value["total_count"] = 2
            return value
        fetch, _ = self.fetcher(mutate=incomplete)
        with self.assertRaises(ValueError):
            verify_provenance_pair_api(LEGACY_PATH, LEGACY_BLOB, self.pair, fetch=fetch)

        def wrong_repository(url, value):
            if "/actions/runs/" in url and "/artifacts?" not in url:
                value["repository"]["full_name"] = "other/repo"
            return value
        fetch, _ = self.fetcher(mutate=wrong_repository)
        with self.assertRaises(ValueError):
            verify_provenance_pair_api(LEGACY_PATH, LEGACY_BLOB, self.pair, fetch=fetch)


if __name__ == "__main__":
    unittest.main()
