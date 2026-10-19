"""H03 provenance and H05 two-file replace fault regression, isolated."""
import tempfile
import unittest
from pathlib import Path

from madsc.legacy_history_provenance import select_ancestor_run, verify_artifact_provenance

SHA_A = "a" * 40
SHA_B = "b" * 40


def run(ident, sha, **overrides):
    data = dict(id=ident, head_sha=sha, head_branch="main", status="completed",
                conclusion="success", head_repository={"full_name": "Madsc55/Madsc55-Tv"},
                path=".github/workflows/madsc-02-kesif.yml", event="push",
                created_at=f"2026-10-20T12:{ident:02d}:00Z")
    data.update(overrides)
    return data


class HistoryProvenanceTests(unittest.TestCase):
    def test_only_successful_same_branch_ancestor_selected(self):
        runs = [run(1, SHA_A), run(2, SHA_B),
                run(3, SHA_A, head_branch="other"),
                run(4, SHA_A, conclusion="failure"),
                run(5, SHA_A, head_repository={"full_name": "fork/repo"})]
        selected = select_ancestor_run(
            runs, repo="Madsc55/Madsc55-Tv", branch="main", current_run="99",
            ancestor_check=lambda sha: sha == SHA_A, workflows=("madsc-02-kesif.yml",))
        self.assertEqual(selected["id"], 1)
        with self.assertRaises(ValueError):
            select_ancestor_run(
                [run(1, SHA_A)], repo="Madsc55/Madsc55-Tv", branch="main",
                current_run="99", ancestor_check=lambda sha: None,
                workflows=("madsc-02-kesif.yml",))

    def test_artifact_run_sha_expiry_and_duplicates(self):
        source = run(1, SHA_A)
        good = dict(name="report", expired=False,
                    workflow_run={"id": 1, "head_sha": SHA_A})
        self.assertTrue(verify_artifact_provenance(source, [good], "report"))
        for bad in ([{**good, "expired": True}], [good, good],
                    [{**good, "workflow_run": {"id": 2, "head_sha": SHA_A}}],
                    [{**good, "workflow_run": {"id": 1, "head_sha": SHA_B}}], []):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                verify_artifact_provenance(source, bad, "report")

    def test_two_replaces_are_not_transactional(self):
        # H05 reproduces old algorithm's partial update after second replace fails.
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            first, second = folder / "gecmis.json", folder / "ana_liste_test_gecmisi.json"
            first.write_text("old-first")
            second.write_text("old-second")
            stage1, stage2 = folder / "stage1", folder / "stage2"
            stage1.write_text("new-first")
            stage2.write_text("new-second")
            with self.assertRaises(OSError):
                stage1.replace(first)
                raise OSError("simulated second replace failure")
            self.assertEqual(first.read_text(), "new-first")
            self.assertEqual(second.read_text(), "old-second")


if __name__ == "__main__":
    unittest.main()
