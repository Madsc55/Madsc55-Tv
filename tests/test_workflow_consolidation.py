import tempfile
import unittest
from pathlib import Path

from madsc.workflow_consolidation import AUXILIARY, MAIN, consolidation_plan, auxiliary_behavior_matrix, contract_gate


class WorkflowConsolidationTests(unittest.TestCase):
    def make_root(self, root):
        folder = root / ".github" / "workflows"
        folder.mkdir(parents=True)
        for name in list(AUXILIARY) + list(MAIN.values()):
            command = AUXILIARY[name][1] if name in AUXILIARY else "echo fixture"
            trigger = ""
            (folder / name).write_text(
                "name: fixture\non:\n" + trigger +
                "  workflow_dispatch:\npermissions:\n  contents: read\njobs:\n  isolated:\n    steps:\n      - run: " + command + "\n",
                encoding="utf-8",
            )
        return folder






    def test_main_k5_is_manual_only(self):
        root = Path(__file__).resolve().parent.parent
        body = (root / ".github" / "workflows" / MAIN["K5"]).read_text(encoding="utf-8")
        self.assertIn("  workflow_dispatch:", body)
        self.assertNotIn("  push:", body)
        self.assertNotIn("  schedule:", body)

    def test_network_probe_steps_require_success_and_opt_in(self):
        root = Path(__file__).resolve().parent.parent / ".github" / "workflows"
        for stage, name, flag in (
            ("K2", "Public candidate discovery", "allow_network_discovery"),
            ("K3", "Bounded Turkish TV video probe", "allow_live_probes"),
        ):
            with self.subTest(stage=stage):
                body = (root / MAIN[stage]).read_text(encoding="utf-8")
                step = body.split("- name: " + name, 1)[1].split("- name:", 1)[0]
                self.assertIn("success() && inputs." + flag + " == true", step)
                self.assertNotIn("continue-on-error: true", step)

    def test_real_k2_k3_failure_uploads_cover_legacy_report_paths(self):
        root = Path(__file__).resolve().parent.parent / ".github" / "workflows"
        reports = {
            "K2": ("reports/k2-legacy-multisource.json",
                   "reports/k2-live-pilot.json",
                   "reports/verified-k2-history.json"),
            "K3": ("reports/k3-real-manifest-pilot.json",
                   "reports/k3-turkish-tv-video-pilot.json",
                   "reports/turkish-tv-batch-validation.json"),
        }
        for stage, paths in reports.items():
            with self.subTest(stage=stage):
                body = (root / MAIN[stage]).read_text(encoding="utf-8")
                upload = body.split("- name: Upload isolated evidence", 1)[1]
                self.assertIn("always() && !cancelled()", upload)
                for report in paths:
                    self.assertIn(report, upload)

    def test_real_isolated_workflows_keep_failure_evidence(self):
        root = Path(__file__).resolve().parent.parent
        for stage in ("K1", "K2", "K3"):
            with self.subTest(stage=stage):
                body = (root / ".github" / "workflows" / MAIN[stage]).read_text(
                    encoding="utf-8")
                self.assertIn(
                    "      - name: Upload isolated evidence\n"
                    "        if: ${{ always() && !cancelled() }}\n"
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
            target.write_text(target.read_text(encoding="utf-8").replace(
                              "echo fixture", AUXILIARY[source.name][1]) +
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
            self.assertIn("command_missing", row["static_contract_gaps"])
            self.assertIn(source.name, result["missing_commands"])
            self.assertIn("timeout", row["static_contract_gaps"])
            self.assertIn("artifact_name", row["static_contract_gaps"])
            self.assertFalse(result["behavioral_parity_verified"])





    def test_unrelated_report_lines_do_not_count_as_uploaded_paths(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            source = folder / "madsc-k2-live-pilot.yml"
            source.write_text(source.read_text(encoding="utf-8") +
                              "      - uses: actions/upload-artifact@v4\\n"
                              "        with:\\n"
                              "          path: reports/actual.json\\n"
                              "      - name: unrelated step\\n"
                              "        run: |\\n"
                              "          reports/not-uploaded.json\\n", encoding="utf-8")
            target = folder / MAIN["K2"]
            target.write_text(target.read_text(encoding="utf-8") +
                              "      - uses: actions/upload-artifact@v4\\n"
                              "        with:\\n"
                              "          path: reports/actual.json\\n", encoding="utf-8")
            row = next(x for x in auxiliary_behavior_matrix(Path(d))["rows"]
                       if x["source"] == source.name)
            self.assertEqual(row["missing_artifact_paths"], [])

    def test_declared_paths_never_count_as_produced_artifacts(self):
        with tempfile.TemporaryDirectory() as d:
            self.make_root(Path(d))
            matrix = auxiliary_behavior_matrix(Path(d))
            self.assertTrue(all(row["artifact_paths_declared_only"] for row in matrix["rows"]))
            self.assertTrue(all(not row["artifact_files_produced_verified"] for row in matrix["rows"]))
            self.assertFalse(contract_gate(Path(d))["artifact_files_produced_verified"])

    def test_artifact_report_path_gap_detected_even_when_name_differs(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            source = folder / "madsc-k2-live-pilot.yml"
            source.write_text(source.read_text(encoding="utf-8") +
                              "      - uses: actions/upload-artifact@v4" + chr(10) +
                              "        with:" + chr(10) +
                              "          name: madsc-old-pilot" + chr(10) +
                              "          path: reports/k2-live-pilot.json" + chr(10),
                              encoding="utf-8")
            matrix = auxiliary_behavior_matrix(Path(d))
            row = next(r for r in matrix["rows"] if r["source"] == source.name)
            self.assertIn("artifact_path", row["static_contract_gaps"])
            self.assertEqual(row["missing_artifact_paths"], ["reports/k2-live-pilot.json"])

    def test_unrelated_long_job_cannot_hide_command_timeout_loss(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            source = folder / "madsc-k2-live-pilot.yml"
            source.write_text(source.read_text() + "    timeout-minutes: 5\n")
            command = AUXILIARY[source.name][1]
            target = folder / MAIN["K2"]
            target.write_text(target.read_text().replace("echo fixture", command) +
                              "    timeout-minutes: 1\n"
                              "  unrelated:\n    timeout-minutes: 60\n"
                              "    steps:\n      - run: echo unrelated\n")
            row = next(r for r in auxiliary_behavior_matrix(Path(d))["rows"]
                       if r["source"] == source.name)
            self.assertEqual(row["main_command_job_timeouts"], [1])
            self.assertIn("timeout", row["static_contract_gaps"])
            self.assertFalse(contract_gate(Path(d))["pass"])

    def test_contract_gate_rejects_lost_paths_after_commands_migrate(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            for _, (stages, command, _) in AUXILIARY.items():
                with (folder / MAIN[stages.split("+")[0]]).open("a") as out:
                    out.write("      - run: " + command + "\n")
            source = folder / "madsc-k2-live-pilot.yml"
            source.write_text(source.read_text() +
                              "      - uses: actions/upload-artifact@v4\n"
                              "        with:\n          path: reports/lost.json\n")
            gate = contract_gate(Path(d))
            self.assertEqual(gate["missing_commands"], [])
            self.assertFalse(gate["pass"])
            self.assertEqual(gate["blocking_contract_gaps"],
                             [{"source": source.name, "gaps": ["artifact_path"]}])

    def test_real_k5_preserves_optional_job_budgets_and_failure_upload(self):
        root = Path(__file__).resolve().parent.parent
        matrix = auxiliary_behavior_matrix(root)
        for source in ("madsc-legacy-99-bulk-audit.yml",
                       "madsc-legacy-notes-bulk-merge.yml"):
            row = next(r for r in matrix["rows"] if r["source"] == source)
            self.assertNotIn("timeout", row["static_contract_gaps"])
        body = (root / ".github/workflows" / MAIN["K5"]).read_text()
        upload = body.split("- name: K5 opt-in eski kaynak raporlarını sakla", 1)[1].split("- name:", 1)[0]
        self.assertIn("always() && !cancelled()", upload)
        self.assertIn("inputs.allow_legacy_source_audit == true", upload)
        self.assertIn("inputs.allow_legacy_notes_merge == true", upload)
        self.assertTrue(contract_gate(root)["pass"])

    def test_contract_gate_rejects_missing_commands(self):
        with tempfile.TemporaryDirectory() as d:
            self.make_root(Path(d))
            gate = contract_gate(Path(d))
            self.assertFalse(gate["pass"])
            self.assertEqual(len(gate["missing_commands"]), 10)
            self.assertFalse(gate["behavioral_parity_verified"])

    def test_contract_gate_accepts_all_executable_commands_without_claiming_parity(self):
        with tempfile.TemporaryDirectory() as d:
            folder = self.make_root(Path(d))
            for name, (stages, command, _) in AUXILIARY.items():
                with (folder / MAIN[stages.split("+")[0]]).open("a", encoding="utf-8") as out:
                    out.write("      - run: " + command + chr(10))
            gate = contract_gate(Path(d))
            self.assertTrue(gate["pass"])
            self.assertEqual(gate["missing_commands"], [])
            self.assertFalse(gate["behavioral_parity_verified"])

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
            content = content.replace("  workflow_dispatch:", "  push:\n    branches: ['**']\n  workflow_dispatch:")
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


    def test_symlinked_workflow_entry_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            folder = self.make_root(root)
            target = root / "external.yml"
            target.write_text("name: external\\non:\\n  workflow_dispatch:\\npermissions:\\n  contents: read\\n", encoding="utf-8")
            link = folder / "unexpected.yml"
            try:
                link.symlink_to(target)
            except (OSError, NotImplementedError):
                self.skipTest("Filesystem does not permit symlinks")
            with self.assertRaisesRegex(ValueError, "Symlinked workflow entry"):
                consolidation_plan(root)


    def test_symlinked_github_directory_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            folder = self.make_root(root)
            github_dir = root / ".github"
            external_github = root / "external-github"
            github_dir.rename(external_github)
            try:
                github_dir.symlink_to(external_github, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("Filesystem does not permit directory symlinks")
            with self.assertRaisesRegex(ValueError, "Workflow directory missing or unsafe"):
                consolidation_plan(root)


if __name__ == "__main__":
    unittest.main()
