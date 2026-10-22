import tempfile
import unittest
from pathlib import Path

from madsc.legacy_parity_evidence import CENTRAL_REPLACEMENT_WORKFLOWS
from madsc.parity_workflow_readiness import (MARKERS, OUTPUT_PATH,
                                             audit_parity_workflow_readiness,
                                             write_parity_workflow_readiness)


ROOT = Path(__file__).resolve().parents[1]


def synthetic_workflows(root, content):
    for relative in CENTRAL_REPLACEMENT_WORKFLOWS:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


class ParityWorkflowReadinessTests(unittest.TestCase):
    def test_current_five_workflows_report_only_integrated_file_slices(self):
        report = audit_parity_workflow_readiness(ROOT)
        self.assertEqual(report["workflow_count"], 5)
        self.assertEqual(report["marker_contract_complete"], 3)
        self.assertEqual(report["static_file_bindings_complete"], 3)
        self.assertEqual(report["external_or_live_input_blockers"], 2)
        self.assertEqual(report["real_behavior_ready"], 0)
        self.assertEqual(report["behavioral_parity_accepted"], 0)
        self.assertFalse(report["production_ready"])
        self.assertEqual({row["workflow_path"] for row in report["rows"]},
                         CENTRAL_REPLACEMENT_WORKFLOWS)
        self.assertEqual(sum(bool(row["missing_markers"]) for row in report["rows"]), 2)
        blocked = {row["workflow_path"] for row in report["rows"]
                   if row["input_classification"] == "external_or_live_input_blocked"}
        self.assertEqual(blocked, {
            ".github/workflows/madsc-02-kesif.yml",
            ".github/workflows/madsc-03-kanal-test.yml",
        })

    def test_complete_ordered_static_markers_still_do_not_prove_runtime(self):
        content = "\n".join([
            "on:", "  workflow_dispatch:", "    inputs:",
            "      allow_parity_evidence:", "        default: false",
            "jobs:", "  audit:", "    steps:",
            "      - if: ${{ inputs.allow_parity_evidence == true }}",
            f"        run: {MARKERS['snapshot_command']} --output report=result.json",
            f"      - run: {MARKERS['manifest_command']} --input input.bin --snapshot snapshot.json",
            f"      - {MARKERS['artifact_upload']}",
            f"        with:\n          path: {MARKERS['manifest_artifact']}",
        ]) + "\n"
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            synthetic_workflows(root, content)
            report = audit_parity_workflow_readiness(root)
            self.assertEqual(report["marker_contract_complete"], 5)
            self.assertEqual(report["static_file_bindings_complete"], 0)
            self.assertEqual(report["real_behavior_ready"], 0)
            self.assertEqual(report["behavioral_parity_accepted"], 0)

    def test_comments_symlink_and_existing_report_fail_closed(self):
        comments = "\n".join(f"# {value}" for value in MARKERS.values()) + "\n"
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            synthetic_workflows(root, comments)
            report = audit_parity_workflow_readiness(root)
            self.assertEqual(report["marker_contract_complete"], 0)

            reports = root / "reports"
            reports.mkdir()
            target = root / OUTPUT_PATH
            target.write_text("preserve", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                write_parity_workflow_readiness(root)
            self.assertEqual(target.read_text(encoding="utf-8"), "preserve")

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            synthetic_workflows(root, "name: safe\n")
            first = root / sorted(CENTRAL_REPLACEMENT_WORKFLOWS)[0]
            real = root / "real.yml"
            real.write_text("name: replacement\n", encoding="utf-8")
            first.unlink()
            first.symlink_to(real)
            with self.assertRaises(PermissionError):
                audit_parity_workflow_readiness(root)

    def test_file_consumer_drift_breaks_static_binding_without_runtime_claim(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for relative in CENTRAL_REPLACEMENT_WORKFLOWS:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / relative).read_bytes())
            k1 = root / ".github/workflows/madsc-01-guvenlik.yml"
            data = k1.read_text(encoding="utf-8").replace(
                "python -m src.madsc_guard config/shadow_manifest.json | tee reports/k1-guard.txt",
                "python -m src.madsc_guard config/other.json | tee reports/k1-guard.txt")
            k1.write_text(data, encoding="utf-8")
            report = audit_parity_workflow_readiness(root)
            self.assertEqual(report["marker_contract_complete"], 3)
            self.assertEqual(report["static_file_bindings_complete"], 2)
            row = next(row for row in report["rows"]
                       if row["workflow_path"].endswith("madsc-01-guvenlik.yml"))
            self.assertEqual(row["input_classification"],
                             "isolated_file_contract_incomplete")
            self.assertFalse(row["real_behavior_ready"])


if __name__ == "__main__":
    unittest.main()
