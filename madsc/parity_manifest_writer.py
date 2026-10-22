"""Deterministic, K1-guarded producer for replacement parity manifests.

This writer records an input digest and a bounded execution snapshot.  It does
not run a workflow, upload an artifact, verify a legacy origin, or grant parity.
"""
import hashlib
import json
from pathlib import Path

from madsc.fixture_report_writer import write_fixture_report
from madsc.legacy_pair_artifact import MANIFEST_NAME, MAX_MANIFEST_BYTES
from madsc.legacy_parity_evidence import (CENTRAL_REPLACEMENT_WORKFLOWS,
                                          compare_execution_snapshots)


OUTPUT_PATH = f"reports/{MANIFEST_NAME}"
MAX_INPUT_BYTES = 2 * 1024 * 1024


def _lower_hex(value, size):
    return (isinstance(value, str) and len(value) == size
            and all(char in "0123456789abcdef" for char in value))


def build_replacement_parity_manifest(execution, input_payload):
    """Create the v1 manifest from actual input bytes and replacement facts."""
    required = {"repository", "branch", "workflow_path", "run_id", "head_sha",
                "snapshot"}
    if not isinstance(execution, dict) or set(execution) != required:
        raise ValueError("Incomplete replacement execution")
    if (execution["repository"] != "Madsc55/Madsc55-Tv"
            or execution["branch"] != "main"
            or execution["workflow_path"] not in CENTRAL_REPLACEMENT_WORKFLOWS):
        raise ValueError("Manifest producer is restricted to the five replacement workflows")
    if (type(execution["run_id"]) is not int or execution["run_id"] <= 0
            or not _lower_hex(execution["head_sha"], 40)):
        raise ValueError("Invalid replacement execution identity")
    if (not isinstance(input_payload, bytes) or not input_payload
            or len(input_payload) > MAX_INPUT_BYTES):
        raise ValueError("Invalid parity input payload")
    # Reuse the fail-closed snapshot shape and digest validation without making
    # a behavioral comparison or accepting parity.
    compare_execution_snapshots(execution["snapshot"], execution["snapshot"])
    manifest = {
        "schema": "madsc-parity-artifact-v1",
        "repository": execution["repository"],
        "run_id": execution["run_id"],
        "head_sha": execution["head_sha"],
        "workflow_path": execution["workflow_path"],
        "input_sha256": hashlib.sha256(input_payload).hexdigest(),
        "snapshot": execution["snapshot"],
    }
    encoded = json.dumps(
        manifest, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ) + "\n"
    if len(encoded.encode("utf-8")) > MAX_MANIFEST_BYTES:
        raise ValueError("Oversized parity manifest")
    return manifest, encoded


def write_replacement_parity_manifest(root: Path, execution, input_payload):
    """Write one isolated manifest through the shared K1 evidence writer."""
    manifest, encoded = build_replacement_parity_manifest(execution, input_payload)
    result = write_fixture_report(Path(root), OUTPUT_PATH, encoded)
    return {
        **result,
        "relative_path": OUTPUT_PATH,
        "input_sha256": manifest["input_sha256"],
        "behavioral_parity_accepted": False,
        "production_ready": False,
    }
