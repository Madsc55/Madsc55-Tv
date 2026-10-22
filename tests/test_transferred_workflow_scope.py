import unittest
from madsc.legacy_workflow_safety import job_scope, assess_workflow_source

class TransferredWorkflowScopeTests(unittest.TestCase):
    def test_job_scope_gate_in_different_job_cannot_cover_writer(self):
            jobs = job_scope("jobs:\n  check:\n    steps:\n      - run: python3 tools/workflow_failure_gate.py\n"
                             "  writer:\n    if: github.ref == 'refs/heads/main'\n    steps:\n      - run: git push origin main\n")
            self.assertEqual([j["job"] for j in jobs], ["check", "writer"])
            self.assertEqual(len(jobs[1]["mutation_lines_without_prior_failure_gate_signal"]), 1)
            self.assertIn("refs/heads/main", jobs[1]["condition_signal"])
            self.assertFalse(jobs[1]["runtime_verified"])

    def test_job_scope_late_or_ignored_gate_does_not_cover_mutation(self):
            for steps in (
                "      - run: git push origin main\n      - run: python3 tools/workflow_failure_gate.py\n",
                "      - run: python3 tools/workflow_failure_gate.py\n        continue-on-error: true\n      - run: git push origin main\n",
            ):
                with self.subTest(steps=steps):
                    jobs = job_scope("jobs:\n  writer:\n    steps:\n" + steps)
                    self.assertEqual(len(jobs[0]["mutation_lines_without_prior_failure_gate_signal"]), 1)

    def test_job_scope_ignores_trigger_names_and_embedded_test_strings(self):
            jobs = job_scope('on:\n  workflow_dispatch:\njobs:\n  audit:\n    steps:\n'
                             '      - name: Read source\n        run: |\n'
                             '          python - <<\'PY\'\n          text = "git push origin main"\n          PY\n'
                             '      - run: echo "git push"\n')
            self.assertEqual([j["job"] for j in jobs], ["audit"])
            self.assertFalse(jobs[0]["mutation_lines_without_prior_failure_gate_signal"])

    def test_job_scope_distinguishes_get_only_api_and_dispatch(self):
            jobs = job_scope('jobs:\n  audit:\n    steps:\n      - run: |\n'
                             '          gh api "repos/${GITHUB_REPOSITORY}/actions/runs"\n'
                             '          gh workflow run next.yml\n')
            self.assertEqual(len(jobs[0]["mutation_lines_without_prior_failure_gate_signal"]), 1)

    def test_readonly_api_does_not_hide_same_line_write(self):
            jobs = job_scope('jobs:\n  publish:\n    steps:\n      - run: |\n'
                             '          gh api "repos/${GITHUB_REPOSITORY}/actions/runs" && curl -X POST https://example.invalid\n')
            self.assertEqual(len(jobs[0]["mutation_lines_without_prior_failure_gate_signal"]), 1)

    def test_prior_same_job_gate_is_only_order_signal(self):
            jobs = job_scope('jobs:\n  publish:\n    steps:\n'
                             '      - run: python3 tools/workflow_failure_gate.py\n'
                             '      - run: git push origin main\n')
            self.assertFalse(jobs[0]['mutation_lines_without_prior_failure_gate_signal'])
            self.assertFalse(jobs[0]['runtime_verified'])

    def test_job_scope_records_reusable_workflow_without_runtime_clearance(self):
            jobs = job_scope('jobs:\n  delegate:\n    uses: ./.github/workflows/madsc-02-kesif.yml\n')
            self.assertIn('madsc-02-kesif.yml', jobs[0]['reusable_workflow_signal'])
            self.assertFalse(jobs[0]['runtime_verified'])

