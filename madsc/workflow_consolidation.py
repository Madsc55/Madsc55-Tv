"""K1-K5 consolidation registry for ten auxiliary manual workflows.

Pure metadata: importing, planning or listing NEVER executes a command.
No workflow is deleted or silently declared behaviorally equivalent.
"""
from __future__ import annotations

import json
from pathlib import Path

AUXILIARY = {
    "01-guvenlik.yml": ("K1", "python -m src.madsc_guard config/shadow_manifest.json", False),
    "madsc-k2-legacy-multisource.yml": ("K2", "python -m madsc.legacy_multisource_discovery", True),
    "madsc-k2-live-pilot.yml": ("K2", "python -m madsc.live_discovery_pilot", True),
    "madsc-k2-real-history-source.yml": ("K2", "python -m madsc.history_real_source_publish", False),
    "madsc-k2-verified-history.yml": ("K2", "python -m madsc.history_verified_workflow", True),
    "madsc-k3-live-manifest-pilot.yml": ("K3", "python -m madsc.k3_live_manifest_pilot", True),
    "madsc-k3-turkish-tv-video.yml": ("K3", "python -m madsc.k3_turkish_tv_video_pilot", True),
    "madsc-legacy-99-bulk-audit.yml": ("K5", "python -m madsc.legacy_99_bulk_audit", True),
    "madsc-legacy-notes-bulk-merge.yml": ("K5", "python scripts/birlestir_eski_sistem_notlari.py", False),
    "madsc-turkish-tv-batch.yml": ("K2+K3", "python -m madsc.turkish_tv_batch_validation", True),
}
MAIN = {
    "K1": "madsc-01-guvenlik.yml",
    "K2": "madsc-02-kesif.yml",
    "K3": "madsc-03-kanal-test.yml",
    "K4": "madsc-04-yedek.yml",
    "K5": "madsc-05-bakim.yml",
}


def consolidation_plan(root: Path) -> dict:
    """Validate exact inventory and map every auxiliary behavior to main stages."""
    root = Path(root)
    folder = root / ".github" / "workflows"
    if not folder.is_dir() or folder.is_symlink():
        raise ValueError("Workflow directory missing or unsafe")
    files = {p.name for p in folder.iterdir() if p.is_file() and p.suffix in (".yml", ".yaml")}
    expected = set(AUXILIARY) | set(MAIN.values())
    if files != expected:
        raise ValueError("Workflow inventory drift: " + repr(sorted(files ^ expected)))
    for stage, name in MAIN.items():
        path = folder / name
        if path.is_symlink():
            raise ValueError("Symlink main workflow forbidden: " + name)
        body = path.read_text(encoding="utf-8")
        if "workflow_dispatch:" not in body or "permissions:" not in body:
            raise ValueError("Missing manual trigger or permissions in main: " + name)
        if any(line.lstrip().startswith(("push:", "pull_request:", "schedule:", "workflow_call:"))
               for line in body.splitlines()):
            raise ValueError("Automatic trigger in main: " + name)
    entries = []
    for name, (stage, command, external) in AUXILIARY.items():
        path = folder / name
        if path.is_symlink():
            raise ValueError("Symlink workflow forbidden")
        data = path.read_text(encoding="utf-8")
        if "workflow_dispatch:" not in data or "permissions:" not in data:
            raise ValueError("Missing manual trigger or permissions: " + name)
        if command not in data:
            raise ValueError("Mapped behavior command absent from source: " + name)
        if any(line.lstrip().startswith(("push:", "pull_request:", "schedule:", "workflow_call:"))
               for line in data.splitlines()):
            raise ValueError("Automatic trigger found: " + name)
        targets = [MAIN[key] for key in stage.split("+")]
        main_contents = [ (folder / target).read_text(encoding="utf-8") for target in targets ]
        # Only count commands inside a YAML run step, never comments,
        # descriptions, env values, or arbitrary quoted strings.
        def in_run_step(content: str) -> bool:
            run_indent = None
            for line in content.splitlines():
                stripped = line.lstrip()
                indent = len(line) - len(stripped)
                if run_indent is not None and stripped and indent <= run_indent:
                    run_indent = None
                if stripped.startswith(("run: ", "- run: ")):
                    value = stripped.split("run:", 1)[1].strip()
                    # A command in an inline YAML comment is not executable.
                    value = value.split(" #", 1)[0].rstrip()
                    if command in value:
                        return True
                if stripped in ("run: |", "run: >"):
                    run_indent = indent
                if run_indent is not None and indent > run_indent:
                    if command in stripped and not stripped.startswith("#"):
                        return True
            return False

        migrated = any(in_run_step(content) for content in main_contents)
        entries.append({
            "command_present_in_main": migrated,
            "workflow": name,
            "target_stage": stage,
            "legacy_command": command,
            "network_or_external_evidence_required": external,
            "behavioral_parity_verified": False,
            "migration_status": "command_integrated_unverified" if migrated else "mapped_not_merged",
        })
    return {
        "schema": "madsc-five-main-consolidation-v1",
        "main_workflows": MAIN,
        "auxiliary_count": len(entries),
        "auxiliary": entries,
        "unmapped_auxiliary": [],
        "commands_integrated_in_main": sum(item["command_present_in_main"] for item in entries),
        "all_ten_commands_integrated_in_main": all(item["command_present_in_main"] for item in entries),
        "five_main_only": False,
        "legacy_behavioral_parity_verified": False,
        "github_actions_triggered": False,
        "tests_executed": False,
        "production_writes": False,
    }


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    print(json.dumps(consolidation_plan(root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
