"""Fail-closed static readiness audit for the five parity producer hooks."""
import hashlib
import json
from pathlib import Path

from madsc.fixture_report_writer import write_fixture_report
from madsc.legacy_parity_evidence import CENTRAL_REPLACEMENT_WORKFLOWS


OUTPUT_PATH = "reports/parity-workflow-readiness.json"
MAX_WORKFLOW_BYTES = 512 * 1024
MARKERS = {
    "explicit_opt_in": "allow_parity_evidence:",
    "opt_in_condition": "inputs.allow_parity_evidence == true",
    "snapshot_command": "python -m madsc.parity_snapshot_cli",
    "manifest_command": "python -m madsc.parity_manifest_cli",
    "manifest_artifact": "reports/madsc-parity-evidence.json",
    "artifact_upload": "uses: actions/upload-artifact@v4",
}

FILE_DATAFLOW_CONTRACTS = {
    ".github/workflows/madsc-01-guvenlik.yml": {
        "consumer": "python -m src.madsc_guard config/shadow_manifest.json | tee reports/k1-guard.txt",
        "manifest_input": "--input config/shadow_manifest.json",
        "snapshot_output": "--output guard=reports/k1-guard.txt",
    },
    ".github/workflows/madsc-04-yedek.yml": {
        "consumer": "python -m madsc.restore_drill --source reports/k4-source --file nested/sample.txt --output reports/k4-restore-drill.json",
        "manifest_input": "--input reports/k4-source/nested/sample.txt",
        "snapshot_output": "--output restore=reports/k4-restore-drill.json",
    },
    ".github/workflows/madsc-05-bakim.yml": {
        "consumer": "python -m madsc.artifact_transport produce --path reports/k2-candidates.json --source reports/k2-input.m3u",
        "manifest_input": "--input reports/k2-input.m3u",
        "snapshot_output": "--output candidates=reports/k2-candidates.json",
    },
}

EXTERNAL_INPUT_BLOCKERS = {
    ".github/workflows/madsc-02-kesif.yml":
        "Standalone K2 comparable behavior depends on live network or externally supplied history files.",
    ".github/workflows/madsc-03-kanal-test.yml":
        "Standalone K3 comparable behavior depends on live stream probes or external candidate sources.",
}


def _read_workflow(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise PermissionError("Workflow must be a regular non-symlink file")
    raw = path.read_bytes()
    if not raw or len(raw) > MAX_WORKFLOW_BYTES:
        raise ValueError("Invalid workflow size")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Workflow must be UTF-8") from exc
    # Ignore whole-line comments so a commented example cannot satisfy a hook.
    active = "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("#"))
    return raw, active


def audit_parity_workflow_readiness(root):
    """Audit hook markers without claiming that static text proves behavior."""
    root = Path(root).absolute()
    if root.is_symlink() or not root.is_dir():
        raise PermissionError("Invalid repository root")
    rows = []
    for relative_path in sorted(CENTRAL_REPLACEMENT_WORKFLOWS):
        raw, active = _read_workflow(root / relative_path)
        markers = {name: token in active for name, token in MARKERS.items()}
        snapshot_at = active.find(MARKERS["snapshot_command"])
        manifest_at = active.find(MARKERS["manifest_command"])
        artifact_at = active.find(MARKERS["manifest_artifact"])
        ordered = (snapshot_at >= 0 and manifest_at > snapshot_at
                   and artifact_at > manifest_at)
        markers["producer_order"] = ordered
        missing = [name for name, present in markers.items() if not present]
        contract = FILE_DATAFLOW_CONTRACTS.get(relative_path)
        if contract:
            consumer_at = active.find(contract["consumer"])
            snapshot_output_at = active.find(contract["snapshot_output"])
            manifest_input_at = active.find(contract["manifest_input"])
            file_binding_complete = (
                consumer_at >= 0 and snapshot_output_at > consumer_at
                and manifest_input_at > snapshot_output_at)
            input_classification = (
                "isolated_file_bound" if file_binding_complete
                else "isolated_file_contract_incomplete")
            dataflow_blocker = (None if file_binding_complete
                                else "Declared file consumer/input/output order is incomplete")
        else:
            file_binding_complete = False
            input_classification = "external_or_live_input_blocked"
            dataflow_blocker = EXTERNAL_INPUT_BLOCKERS[relative_path]
        rows.append({
            "workflow_path": relative_path,
            "workflow_sha256": hashlib.sha256(raw).hexdigest(),
            "markers": markers,
            "marker_contract_complete": not missing,
            "missing_markers": missing,
            "input_classification": input_classification,
            "static_file_binding_complete": file_binding_complete,
            "dataflow_blocker": dataflow_blocker,
            "runtime_origin_verified": False,
            "real_behavior_ready": False,
            "behavioral_parity_accepted": False,
        })
    return {
        "schema": "madsc-parity-workflow-readiness-v1",
        "workflow_count": 5,
        "marker_contract_complete": sum(
            row["marker_contract_complete"] for row in rows),
        "static_file_bindings_complete": sum(
            row["static_file_binding_complete"] for row in rows),
        "external_or_live_input_blockers": sum(
            row["input_classification"] == "external_or_live_input_blocked"
            for row in rows),
        "real_behavior_ready": 0,
        "behavioral_parity_accepted": 0,
        "production_ready": False,
        "rows": rows,
        "note": "Static hook markers are readiness inventory, never runtime or parity proof.",
    }


def write_parity_workflow_readiness(root):
    report = audit_parity_workflow_readiness(root)
    encoded = json.dumps(report, sort_keys=True, ensure_ascii=False) + "\n"
    result = write_fixture_report(Path(root), OUTPUT_PATH, encoded)
    return {**result, "relative_path": OUTPUT_PATH,
            "marker_contract_complete": report["marker_contract_complete"],
            "static_file_bindings_complete": report["static_file_bindings_complete"],
            "external_or_live_input_blockers": report["external_or_live_input_blockers"],
            "real_behavior_ready": 0, "behavioral_parity_accepted": 0,
            "production_ready": False}
