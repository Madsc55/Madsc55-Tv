import re
import unittest
from pathlib import Path

from madsc.parity_workflow_readiness import audit_parity_workflow_readiness


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


class ParityWorkflowIntegrationTests(unittest.TestCase):
    def test_only_three_real_file_slices_have_complete_opt_in_hooks(self):
        report = audit_parity_workflow_readiness(ROOT)
        complete = {row["workflow_path"] for row in report["rows"]
                    if row["marker_contract_complete"]}
        self.assertEqual(complete, {
            ".github/workflows/madsc-01-guvenlik.yml",
            ".github/workflows/madsc-04-yedek.yml",
            ".github/workflows/madsc-05-bakim.yml",
        })
        self.assertEqual(report["marker_contract_complete"], 3)
        self.assertEqual(report["static_file_bindings_complete"], 3)
        self.assertEqual(report["external_or_live_input_blockers"], 2)
        self.assertEqual(report["real_behavior_ready"], 0)
        self.assertEqual(report["behavioral_parity_accepted"], 0)

    def test_k1_k4_and_k5_inputs_are_consumed_before_snapshot_and_manifest(self):
        cases = {
            "madsc-01-guvenlik.yml": (
                "python -m src.madsc_guard config/shadow_manifest.json | tee reports/k1-guard.txt",
                "--input config/shadow_manifest.json",
                "--output guard=reports/k1-guard.txt",
            ),
            "madsc-04-yedek.yml": (
                "python -m madsc.restore_drill --source reports/k4-source",
                "--input reports/k4-source/nested/sample.txt",
                "--output restore=reports/k4-restore-drill.json",
            ),
            "madsc-05-bakim.yml": (
                "python -m madsc.artifact_transport produce --path reports/k2-candidates.json --source reports/k2-input.m3u",
                "--input reports/k2-input.m3u",
                "--output candidates=reports/k2-candidates.json",
            ),
        }
        for filename, (producer, manifest_input, snapshot_output) in cases.items():
            data = (WORKFLOWS / filename).read_text(encoding="utf-8")
            with self.subTest(workflow=filename):
                self.assertLess(data.index(producer), data.index(snapshot_output))
                self.assertLess(data.index(snapshot_output), data.index(manifest_input))
                self.assertLess(data.index(manifest_input),
                                data.index("path: reports/madsc-parity-evidence.json"))

    def test_opt_in_input_hash_guards_surround_consumer_and_manifest(self):
        cases = {
            "madsc-01-guvenlik.yml": (
                "config/shadow_manifest.json",
                "python -m src.madsc_guard config/shadow_manifest.json",
            ),
            "madsc-04-yedek.yml": (
                "reports/k4-source/nested/sample.txt",
                "python -m madsc.restore_drill --source reports/k4-source",
            ),
            "madsc-05-bakim.yml": (
                "reports/k2-input.m3u",
                "python -m madsc.artifact_transport produce --path reports/k2-candidates.json",
            ),
        }
        for filename, (input_path, consumer) in cases.items():
            data = (WORKFLOWS / filename).read_text(encoding="utf-8")
            before = f"sha256sum {input_path} > reports/parity-input-before.sha256"
            check = "sha256sum --check --status reports/parity-input-before.sha256"
            manifest = "python -m madsc.parity_manifest_cli"
            with self.subTest(workflow=filename):
                self.assertIn(before, data)
                self.assertEqual(data.count(check), 2)
                first_check = data.index(check)
                second_check = data.index(check, first_check + len(check))
                self.assertLess(data.index(before), data.index(consumer))
                self.assertLess(data.index(consumer), first_check)
                self.assertLess(first_check, data.index(manifest))
                self.assertLess(data.index(manifest), second_check)
                self.assertLess(second_check,
                                data.index("path: reports/madsc-parity-evidence.json"))
                self.assertIn('inputs.allow_parity_evidence', data)

    def test_every_parity_hook_is_default_off_and_conditioned(self):
        for filename in ("madsc-01-guvenlik.yml", "madsc-04-yedek.yml",
                         "madsc-05-bakim.yml"):
            data = (WORKFLOWS / filename).read_text(encoding="utf-8")
            self.assertRegex(
                data,
                r"(?m)^      allow_parity_evidence:\n"
                r"(?:(?!^      [A-Za-z_][A-Za-z_0-9]*:).+\n)*?"
                r"        default: false\s*$",
            )
            parity_steps = [
                step for step in re.split(r"(?=^      - name: )", data, flags=re.MULTILINE)
                if ("madsc.parity_" in step
                    or "path: reports/madsc-parity-evidence.json" in step)
            ]
            self.assertEqual(len(parity_steps), 3, filename)
            self.assertTrue(all(
                "if: ${{ inputs.allow_parity_evidence == true }}" in step
                for step in parity_steps), filename)


if __name__ == "__main__":
    unittest.main()
