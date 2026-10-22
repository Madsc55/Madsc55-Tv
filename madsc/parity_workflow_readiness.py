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
        rows.append({
            "workflow_path": relative_path,
            "workflow_sha256": hashlib.sha256(raw).hexdigest(),
            "markers": markers,
            "marker_contract_complete": not missing,
            "missing_markers": missing,
            "runtime_origin_verified": False,
            "real_behavior_ready": False,
            "behavioral_parity_accepted": False,
        })
    return {
        "schema": "madsc-parity-workflow-readiness-v1",
        "workflow_count": 5,
        "marker_contract_complete": sum(
            row["marker_contract_complete"] for row in rows),
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
            "real_behavior_ready": 0, "behavioral_parity_accepted": 0,
            "production_ready": False}
