import tempfile
import unittest
from pathlib import Path

from madsc.workflow_consolidation import AUXILIARY, MAIN, consolidation_plan, auxiliary_behavior_matrix


class WorkflowConsolidationTests(unittest.TestCase):
    def make_root(self, root):
        folder = root / ".github" / "workflows"
        folder.mkdir(parents=True)
        for name in list(AUXILIARY) + list(MAIN.values()):
            command = AUXILIARY[name][1] if name in AUXILIARY else "echo fixture"
            trigger = ("  push:\n    branches: [main]\n    paths:\n"
                       "      - 'madsc/**'\n      - 'tests/**'\n"
                       "      - '.github/workflows/madsc-05-bakim.yml'\n"
                       if name == MAIN["K5"] else "")
            (folder / name).write_text(
                "name: fixture\non:\n" + trigger +
                "  workflow_dispatch:\npermissions:\n  contents: read\njobs:\n  isolated:\n    steps:\n      - run: " + command + "\n",
                encoding="utf-8",
            )
        return folder




    def test_real_isolated_workflows_keep_failure_evidence(self):
        root = Path(__file__).resolve().parent.parent
        for stage in ("K1", "K2", "K3"):
            with self.subTest(stage=stage):
                body = (root / ".github" / "workflows" / MAIN[stage]).read_text(
                    encoding="utf-8")
                self.assertIn(
                    "      - name: Upload isolated evidence\\n"
                    "        if: ${{ always() && !cancelled() }}\\n"
                    "        uses: actions/upload-artifact@v4", body)
                self.assertIn("workflow_dispatch:", body)
                self.assertNotIn("  schedule:", body)

    def test_longer_destination_timeout_is_not_a_gap(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            source = folder / "madsc-k2-live-pilot.yml"
            source.write_text(source.read_text(encoding="utf-8") +
                              "    timeout-minutes: 5\n", encoding="utf-8")
            target = folder / MAIN["K2"]
            target.write_text(target.read_text(encoding="utf-8") +
                              "    timeout-minutes: 10\n", encoding="utf-8")
            result = auxiliary_behavior_matrix(Path(d))
            row = next(x for x in result["rows"] if x["source"] == source.name)
            self.assertNotIn("timeout", row["static_contract_gaps"])

    def test_bulk_contract_matrix_flags_missing_timeout_and_artifact(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            source = folder / "madsc-k2-live-pilot.yml"
            source.write_text(source.read_text(encoding="utf-8") +
                              "    timeout-minutes: 5\n"
                              "      - uses: actions/upload-artifact@v4\n"
                              "        with:\n"
                              "          name: madsc-k2-real-channel-discovery-pilot\n",
                              encoding="utf-8")
            result = auxiliary_behavior_matrix(Path(d))
            row = next(x for x in result["rows"] if x["source"] == source.name)
            self.assertEqual(result["auxiliary_count"], 10)
            self.assertFalse(row["command_present"])
            self.assertIn("timeout", row["static_contract_gaps"])
            self.assertIn("artifact_name", row["static_contract_gaps"])
            self.assertFalse(result["behavioral_parity_verified"])

    def test_all_ten_mapped_to_five_without_claiming_parity(self):
        with tempfile.TemporaryDirectory() as d:
            self.make_root(Path(d))
            result = consolidation_plan(Path(d))
            self.assertEqual(result["auxiliary_count"], 10)
            self.assertEqual(result["unmapped_auxiliary"], [])
            self.assertFalse(result["five_main_only"])
            self.assertFalse(result["legacy_behavioral_parity_verified"])
            self.assertFalse(result["github_actions_triggered"])

    def test_all_ten_commands_detected_in_main_workflows(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            for name, (stage, command, _) in AUXILIARY.items():
                main_name = MAIN[stage.split("+")[0]]
                with (folder / main_name).open("a", encoding="utf-8") as out:
                    out.write("      - run: " + command + "\n")
            result = consolidation_plan(Path(d))
            self.assertEqual(result["commands_integrated_in_main"], 10)
            self.assertTrue(result["all_ten_commands_integrated_in_main"])
            self.assertTrue(all(item["command_present_in_main"] for item in result["auxiliary"]))
            self.assertFalse(result["legacy_behavioral_parity_verified"])

    def test_missing_main_command_not_reported_as_integrated(self):
        with tempfile.TemporaryDirectory() as d:
            self.make_root(Path(d))
            result = consolidation_plan(Path(d))
            self.assertEqual(result["commands_integrated_in_main"], 0)
            self.assertFalse(result["all_ten_commands_integrated_in_main"])

    def test_commented_main_command_is_not_counted_as_migrated(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            command = AUXILIARY["madsc-k2-live-pilot.yml"][1]
            with (folder / MAIN["K2"]).open("a", encoding="utf-8") as out:
                out.write("      # " + command + "\n")
            result = consolidation_plan(Path(d))
            self.assertEqual(result["commands_integrated_in_main"], 0)
            self.assertFalse(result["all_ten_commands_integrated_in_main"])

    def test_env_value_is_not_executable_migration(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            command = AUXILIARY["madsc-k2-live-pilot.yml"][1]
            with (folder / MAIN["K2"]).open("a", encoding="utf-8") as out:
                out.write("      - name: non-executable metadata\n")
                out.write("        env:\n")
                out.write("          DESCRIPTION: " + command + "\n")
            result = consolidation_plan(Path(d))
            self.assertEqual(result["commands_integrated_in_main"], 0)

    def test_inline_comment_is_not_executable_migration(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            command = AUXILIARY["madsc-k2-live-pilot.yml"][1]
            with (folder / MAIN["K2"]).open("a", encoding="utf-8") as out:
                out.write("      - run: echo fixture # " + command + "\n")
            result = consolidation_plan(Path(d))
            self.assertEqual(result["commands_integrated_in_main"], 0)

    def test_multiline_shell_comment_does_not_count_as_migration(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            command = AUXILIARY["madsc-k2-live-pilot.yml"][1]
            with (folder / MAIN["K2"]).open("a", encoding="utf-8") as out:
                out.write("      - run: |\n")
                out.write("          echo fixture # " + command + "\n")
            result = consolidation_plan(Path(d))
            self.assertEqual(result["commands_integrated_in_main"], 0)

    def test_list_style_multiline_run_is_migrated(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            command = AUXILIARY["madsc-k2-live-pilot.yml"][1]
            with (folder / MAIN["K2"]).open("a", encoding="utf-8") as out:
                out.write("      - run: |\n")
                out.write("          " + command + "\n")
            result = consolidation_plan(Path(d))
            self.assertEqual(result["commands_integrated_in_main"], 1)

    def test_automatic_trigger_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            (folder / "01-guvenlik.yml").write_text(
                "on:\n  workflow_dispatch:\n  push:\npermissions:\n  contents: read\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                consolidation_plan(Path(d))

    def test_missing_mapped_command_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            (folder / "madsc-k2-live-pilot.yml").write_text(
                "on:\n  workflow_dispatch:\npermissions:\n  contents: read\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                consolidation_plan(Path(d))

    def test_commented_source_command_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            command = AUXILIARY["madsc-k2-live-pilot.yml"][1]
            (folder / "madsc-k2-live-pilot.yml").write_text(
                "on:\n  workflow_dispatch:\npermissions:\n  contents: read\n"
                "jobs:\n  isolated:\n    steps:\n      # " + command + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                consolidation_plan(Path(d))

    def test_k5_unrestricted_push_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            path = folder / MAIN["K5"]
            content = path.read_text(encoding="utf-8")
            content = content.replace("    branches: [main]", "    branches: ['**']")
            path.write_text(content, encoding="utf-8")
            with self.assertRaises(ValueError):
                consolidation_plan(Path(d))

    def test_main_automatic_trigger_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            (folder / MAIN["K1"]).write_text(
                "on:\n  workflow_dispatch:\n  schedule:\npermissions:\n  contents: read\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                consolidation_plan(Path(d))

    def test_untracked_workflow_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            (folder / "unexpected.yml").write_text("on:\n  workflow_dispatch:\n")
            with self.assertRaises(ValueError):
                consolidation_plan(Path(d))

    def test_missing_workflow_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            (folder / "madsc-k2-live-pilot.yml").unlink()
            with self.assertRaises(ValueError):
                consolidation_plan(Path(d))


if __name__ == "__main__":
    unittest.main()
