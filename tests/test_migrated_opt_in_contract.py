"""Fail-closed static checks: migrated live operations stay opt-in."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / ".github" / "workflows"
SPECS = {
    "madsc-02-kesif.yml": {
        "allow_network_discovery": (
            "python -m madsc.legacy_multisource_discovery",
            "python -m madsc.live_discovery_pilot",
        ),
        "allow_verified_history": (
            "python -m madsc.history_real_source_publish",
            "python -m madsc.history_verified_workflow",
        ),
    },
    "madsc-03-kanal-test.yml": {
        "allow_live_probes": (
            "python -m madsc.k3_live_manifest_pilot",
            "python -m madsc.k3_turkish_tv_video_pilot",
        ),
        "allow_bulk_turkish_tv": (
            "python -m madsc.turkish_tv_batch_validation",
        ),
    },
    "madsc-05-bakim.yml": {
        "allow_legacy_source_audit": (
            "python -m madsc.legacy_99_bulk_audit",
        ),
        "allow_legacy_notes_merge": (
            "python scripts/birlestir_eski_sistem_notlari.py",
        ),
    },
}


class MigratedOptInContractTests(unittest.TestCase):
    def test_all_sensitive_commands_are_explicitly_guarded(self):
        for filename, inputs in SPECS.items():
            data = (ROOT / filename).read_text(encoding="utf-8")
            self.assertIn("workflow_dispatch:", data, filename)
            for input_name, commands in inputs.items():
                # The input must be explicitly declared and default to false.
                match = re.search(
                    r"^      " + re.escape(input_name) + r":\n"
                    r"(?:(?!^      [A-Za-z_][A-Za-z_0-9]*:).+\n)*?"
                    r"        default: false\s*$",
                    data, re.MULTILINE,
                )
                self.assertIsNotNone(match, (filename, input_name))
                for command in commands:
                    containing_steps = [
                        step for step in re.split(r"(?=^      - name: )", data, flags=re.MULTILINE)
                        if command in step
                    ]
                    self.assertEqual(len(containing_steps), 1, (filename, command))
                    step = containing_steps[0]
                    self.assertIn(
                        "if: ${{ inputs." + input_name + " == true }}",
                        step, (filename, command),
                    )

    def test_all_five_main_workflows_are_manual_only(self):
        for filename in (
            "madsc-01-guvenlik.yml", "madsc-02-kesif.yml",
            "madsc-03-kanal-test.yml", "madsc-04-yedek.yml",
            "madsc-05-bakim.yml",
        ):
            data = (ROOT / filename).read_text(encoding="utf-8")
            self.assertIn("workflow_dispatch:", data)
            for line in data.splitlines():
                self.assertFalse(
                    re.match(r"^\s*(push|pull_request|schedule|workflow_call):", line),
                    (filename, line),
                )


if __name__ == "__main__":
    unittest.main()
