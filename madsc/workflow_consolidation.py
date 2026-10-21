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


def _command_in_run_step(content: str, command: str) -> bool:
    """Find commands in YAML run steps; reject comments and non-run metadata."""
    run_indent = None
    for line in content.splitlines():
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if run_indent is not None and stripped and indent <= run_indent:
            run_indent = None
        if stripped.startswith(("run: ", "- run: ")):
            value = stripped.split("run:", 1)[1].strip()
            value = value.split(" #", 1)[0].rstrip()
            if command in value:
                return True
        if stripped in ("run: |", "run: >", "- run: |", "- run: >"):
            run_indent = indent
        if run_indent is not None and indent > run_indent:
            # Shell comments inside YAML block scalars are not executed.
            executable = stripped.split(" #", 1)[0].rstrip()
            if command in executable and not executable.startswith("#"):
                return True
    return False


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
        forbidden = ("pull_request:", "schedule:", "workflow_call:")
        if stage != "K5":
            forbidden += ("push:",)
        if any(line.lstrip().startswith(forbidden) for line in body.splitlines()):
            raise ValueError("Unsafe automatic trigger in main: " + name)
        if stage == "K5":
            expected_push = ("  push:\n    branches: [main]\n"
                             "    paths:\n      - 'madsc/**'\n"
                             "      - 'tests/**'\n"
                             "      - '.github/workflows/madsc-05-bakim.yml'\n")
            if expected_push not in body:
                raise ValueError("K5 auto regression trigger is not restricted")
    entries = []
    for name, (stage, command, external) in AUXILIARY.items():
        path = folder / name
        if path.is_symlink():
            raise ValueError("Symlink workflow forbidden")
        data = path.read_text(encoding="utf-8")
        if "workflow_dispatch:" not in data or "permissions:" not in data:
            raise ValueError("Missing manual trigger or permissions: " + name)
        # Reuse executable-step validation for both source and destination.
        # Presence in a YAML comment or metadata is not execution evidence.
        if not _command_in_run_step(data, command):
            raise ValueError("Mapped behavior command absent from source run step: " + name)
        if any(line.lstrip().startswith(("push:", "pull_request:", "schedule:", "workflow_call:"))
               for line in data.splitlines()):
            raise ValueError("Automatic trigger found: " + name)
        targets = [MAIN[key] for key in stage.split("+")]
        main_contents = [ (folder / target).read_text(encoding="utf-8") for target in targets ]
        # Only count commands inside a YAML run step, never comments,
        # descriptions, env values, or arbitrary quoted strings.
        migrated = any(_command_in_run_step(content, command) for content in main_contents)
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



def auxiliary_behavior_matrix(root: Path) -> dict:
    """Read-only comparison of workflow operational contracts, not parity acceptance."""
    import re
    folder = Path(root) / ".github" / "workflows"
    rows = []
    for name, (stages, command, external) in AUXILIARY.items():
        source = (folder / name).read_text(encoding="utf-8")
        targets = [MAIN[stage] for stage in stages.split("+")]
        main_sources = [(folder / target).read_text(encoding="utf-8") for target in targets]
        def contracts(body):
            timeout = [int(n) for n in re.findall(r"^\\s*timeout-minutes:\\s*(\\d+)\\s*$", body, re.M)]
            artifacts = re.findall(r"^\\s*name:\\s*(madsc-[a-z0-9-]+|turkish-tv-batch-validation)\\s*$", body, re.M)
            return {"timeout_minutes": timeout, "artifact_names": artifacts,
                    "actions_read": bool(re.search(r"^\\s*actions:\\s*read\\s*$", body, re.M)),
                    "always_upload": bool(re.search(r"^\\s*if:\\s*(?:\\$\\{\\{\\s*)?always\\(\\)", body, re.M))}
        src = contracts(source)
        destinations = [contracts(body) for body in main_sources]
        gaps = []
        if src["timeout_minutes"] and not any(
                actual >= required for required in src["timeout_minutes"]
                for dst in destinations for actual in dst["timeout_minutes"]):
            gaps.append("timeout")
        if src["artifact_names"] and not all(
                any(a in dst["artifact_names"] for dst in destinations)
                for a in src["artifact_names"]):
            gaps.append("artifact_name")
        if src["actions_read"] and not all(dst["actions_read"] for dst in destinations):
            gaps.append("actions_permission")
        if src["always_upload"] and not any(dst["always_upload"] for dst in destinations):
            gaps.append("always_upload")
        rows.append({"source": name, "stages": stages, "command_present": any(
            _command_in_run_step(body, command) for body in main_sources),
            "source_contract": src, "main_contracts": destinations,
            "static_contract_gaps": gaps, "behavioral_parity_verified": False,
            "external_evidence_required": external})
    return {"auxiliary_count": len(rows), "rows": rows,
            "static_gaps_total": sum(len(row["static_contract_gaps"]) for row in rows),
            "behavioral_parity_verified": False, "production_writes": False}


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    import argparse
    parser = argparse.ArgumentParser(description="Read-only workflow consolidation audit")
    parser.add_argument("--behavior-matrix", action="store_true", help="Compare auxiliary workflow contracts")
    args = parser.parse_args()
    report = auxiliary_behavior_matrix(root) if args.behavior_matrix else consolidation_plan(root)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
