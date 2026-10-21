import tempfile
import unittest
from pathlib import Path

from madsc.workflow_consolidation import AUXILIARY, MAIN, consolidation_plan


class WorkflowConsolidationTests(unittest.TestCase):
    def make_root(self, root):
        folder = root / ".github" / "workflows"
        folder.mkdir(parents=True)
        for name in list(AUXILIARY) + list(MAIN.values()):
            command = AUXILIARY[name][1] if name in AUXILIARY else "echo fixture"
            (folder / name).write_text(
                "name: fixture\non:\n  workflow_dispatch:\npermissions:\n  contents: read\n" + command + "\n",
                encoding="utf-8",
            )
        return folder

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
