"""Bounded parser for same-input legacy parity evidence artifacts."""
import hashlib
import io
import json
import stat
import zipfile

from madsc.legacy_parity_cli import unique_pairs
from madsc.legacy_parity_evidence import (compare_execution_snapshots,
                                          compare_provenance_bound_pair)


MANIFEST_NAME = "madsc-parity-evidence.json"
MAX_ARCHIVE_BYTES = 2 * 1024 * 1024
MAX_MANIFEST_BYTES = 1024 * 1024
MAX_DIAGNOSTIC_ARCHIVE_BYTES = 4 * 1024 * 1024
MAX_DIAGNOSTIC_TOTAL_BYTES = 3 * 1024 * 1024
DIAGNOSTIC_MEMBERS = {
    "process_stdout": ("parity-process-stdout.log", 1024 * 1024),
    "process_stderr": ("parity-process-stderr.log", 1024 * 1024),
    "process_outcome": ("parity-process-outcome.json", 8192),
}
DIAGNOSTIC_SNAPSHOT_NAME = "madsc-parity-snapshot.json"
FAILURE_ARTIFACT_NAMES = {
    ".github/workflows/madsc-01-guvenlik.yml": "madsc-k1-failed-consumer-snapshot",
    ".github/workflows/madsc-04-yedek.yml": "madsc-k4-failed-consumer-snapshot",
    ".github/workflows/madsc-05-bakim.yml": "madsc-k2-failed-consumer-snapshot",
}
FAILURE_CONSUMERS = {
    ".github/workflows/madsc-01-guvenlik.yml": "k1",
    ".github/workflows/madsc-04-yedek.yml": "k4",
    ".github/workflows/madsc-05-bakim.yml": "k5",
}


def _json_object(raw, message):
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(message) from exc


def verify_failure_diagnostic_artifact(origin, diagnostic_artifact, archive):
    """Bind measured failure diagnostic bytes to one replacement execution.

    The failure ZIP is a separate GitHub artifact from the parity manifest.
    Verifying it does not grant parity or production acceptance.
    """
    if (not isinstance(origin, dict) or not isinstance(diagnostic_artifact, dict)
            or not isinstance(archive, bytes) or not archive
            or len(archive) > MAX_DIAGNOSTIC_ARCHIVE_BYTES):
        raise ValueError("Invalid failure diagnostic verification input")
    workflow = origin.get("workflow_path")
    expected_name = FAILURE_ARTIFACT_NAMES.get(workflow)
    if (origin.get("repository") != "Madsc55/Madsc55-Tv"
            or origin.get("branch") != "main" or expected_name is None
            or origin.get("conclusion") not in {"failure", "timed_out"}
            or type(origin.get("run_id")) is not int or origin["run_id"] <= 0
            or not isinstance(origin.get("head_sha"), str)
            or len(origin["head_sha"]) != 40
            or any(char not in "0123456789abcdef" for char in origin["head_sha"])):
        raise ValueError("Failure diagnostics require a failed replacement execution")
    required_artifact = {"id", "name", "repository", "run_id", "head_sha", "sha256"}
    if (set(diagnostic_artifact) != required_artifact
            or type(diagnostic_artifact.get("id")) is not int
            or diagnostic_artifact["id"] <= 0
            or diagnostic_artifact.get("name") != expected_name
            or diagnostic_artifact.get("repository") != origin.get("repository")
            or diagnostic_artifact.get("run_id") != origin.get("run_id")
            or diagnostic_artifact.get("head_sha") != origin.get("head_sha")
            or not isinstance(diagnostic_artifact.get("sha256"), str)
            or len(diagnostic_artifact["sha256"]) != 64
            or any(char not in "0123456789abcdef"
                   for char in diagnostic_artifact["sha256"])):
        raise ValueError("Diagnostic artifact is not bound to the execution origin")
    primary_artifact = origin.get("artifact")
    if (not isinstance(primary_artifact, dict)
            or primary_artifact.get("repository") != diagnostic_artifact["repository"]
            or primary_artifact.get("id") == diagnostic_artifact["id"]):
        raise ValueError("Failure diagnostics must use a separate artifact origin")
    if hashlib.sha256(archive).hexdigest() != diagnostic_artifact["sha256"]:
        raise ValueError("Diagnostic artifact archive digest mismatch")

    expected_files = {value[0] for value in DIAGNOSTIC_MEMBERS.values()}
    expected_files.add(DIAGNOSTIC_SNAPSHOT_NAME)
    payloads = {}
    try:
        with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
            infos = bundle.infolist()
            if len(infos) != len(expected_files) or {info.filename for info in infos} != expected_files:
                raise ValueError("Diagnostic artifact members are missing, duplicate or unexpected")
            total = 0
            limits = {name: limit for name, limit in DIAGNOSTIC_MEMBERS.values()}
            limits[DIAGNOSTIC_SNAPSHOT_NAME] = MAX_MANIFEST_BYTES
            for info in infos:
                mode = info.external_attr >> 16
                limit = limits[info.filename]
                if (info.is_dir() or info.flag_bits & 1 or stat.S_ISLNK(mode)
                        or info.file_size > limit
                        or info.compress_size > MAX_DIAGNOSTIC_ARCHIVE_BYTES
                        or (info.compress_size and info.file_size > info.compress_size * 100)):
                    raise ValueError("Unsafe diagnostic artifact member")
                total += info.file_size
                if total > MAX_DIAGNOSTIC_TOTAL_BYTES:
                    raise ValueError("Oversized diagnostic artifact contents")
                payloads[info.filename] = bundle.read(info)
    except (zipfile.BadZipFile, RuntimeError, OSError) as exc:
        raise ValueError("Invalid diagnostic artifact ZIP") from exc

    snapshot = _json_object(payloads[DIAGNOSTIC_SNAPSHOT_NAME],
                            "Invalid diagnostic snapshot JSON")
    declared_snapshot = origin.get("snapshot")
    if snapshot != declared_snapshot or not isinstance(snapshot, dict):
        raise ValueError("Diagnostic snapshot is not bound to the execution origin")
    compare_execution_snapshots(snapshot, snapshot)
    outputs = snapshot.get("outputs")
    if (set(snapshot) != {"exit_code", "timed_out", "outputs", "side_effects"}
            or not isinstance(outputs, dict)
            or set(outputs) != set(DIAGNOSTIC_MEMBERS)
            or snapshot.get("side_effects") != {}
            or (snapshot.get("exit_code") == 0 and snapshot.get("timed_out") is not True)
            or (origin.get("conclusion") == "timed_out"
                and snapshot.get("timed_out") is not True)):
        raise ValueError("Invalid failure diagnostic snapshot")
    for label, (name, _limit) in DIAGNOSTIC_MEMBERS.items():
        if hashlib.sha256(payloads[name]).hexdigest() != outputs.get(label):
            raise ValueError("Diagnostic member digest does not match the snapshot")

    outcome = _json_object(payloads[DIAGNOSTIC_MEMBERS["process_outcome"][0]],
                           "Invalid process outcome JSON")
    required_outcome = {"schema", "consumer", "exit_code", "timed_out",
                        "behavioral_parity_accepted", "production_ready"}
    if (not isinstance(outcome, dict) or set(outcome) != required_outcome
            or outcome.get("schema") != "madsc-local-process-outcome-v1"
            or outcome.get("consumer") != FAILURE_CONSUMERS[workflow]
            or type(outcome.get("exit_code")) is not int
            or type(outcome.get("timed_out")) is not bool
            or outcome.get("exit_code") != snapshot.get("exit_code")
            or outcome.get("timed_out") != snapshot.get("timed_out")
            or outcome.get("behavioral_parity_accepted") is not False
            or outcome.get("production_ready") is not False):
        raise ValueError("Process outcome does not match the failure snapshot")
    return {
        "diagnostic_artifact_bytes_verified": True,
        "artifact_sha256": diagnostic_artifact["sha256"],
        "snapshot_sha256": hashlib.sha256(payloads[DIAGNOSTIC_SNAPSHOT_NAME]).hexdigest(),
        "diagnostic_member_sha256": dict(outputs),
        "exit_code": outcome["exit_code"],
        "timed_out": outcome["timed_out"],
        "behavioral_parity_accepted": False,
        "production_ready": False,
    }


def verify_parity_artifact_manifest(origin, archive):
    """Bind a single-file artifact ZIP to its declared execution and snapshot."""
    if not isinstance(origin, dict) or not isinstance(archive, bytes):
        raise ValueError("Invalid artifact verification input")
    if not archive or len(archive) > MAX_ARCHIVE_BYTES:
        raise ValueError("Invalid artifact archive size")
    declared = origin.get("artifact") or {}
    if hashlib.sha256(archive).hexdigest() != declared.get("sha256"):
        raise ValueError("Artifact archive digest mismatch")
    try:
        with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
            infos = bundle.infolist()
            if len(infos) != 1 or infos[0].filename != MANIFEST_NAME:
                raise ValueError("Artifact must contain exactly the parity manifest")
            info = infos[0]
            mode = info.external_attr >> 16
            if (info.is_dir() or info.flag_bits & 1 or info.file_size > MAX_MANIFEST_BYTES
                    or info.compress_size > MAX_ARCHIVE_BYTES
                    or (info.compress_size and info.file_size > info.compress_size * 100)
                    or stat.S_ISLNK(mode)):
                raise ValueError("Unsafe artifact manifest entry")
            raw = bundle.read(info)
    except (zipfile.BadZipFile, RuntimeError, OSError) as exc:
        raise ValueError("Invalid artifact ZIP") from exc
    if len(raw) > MAX_MANIFEST_BYTES:
        raise ValueError("Oversized parity manifest")
    try:
        manifest = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid parity manifest JSON") from exc
    required = {"schema", "repository", "run_id", "head_sha", "workflow_path",
                "input_sha256", "snapshot"}
    if (not isinstance(manifest, dict) or set(manifest) != required
            or manifest["schema"] != "madsc-parity-artifact-v1"
            or manifest["repository"] != origin.get("repository")
            or manifest["run_id"] != origin.get("run_id")
            or manifest["head_sha"] != origin.get("head_sha")
            or manifest["workflow_path"] != origin.get("workflow_path")
            or manifest["input_sha256"] != origin.get("input_sha256")
            or manifest["snapshot"] != origin.get("snapshot")):
        raise ValueError("Parity manifest is not bound to the execution origin")
    return {
        "artifact_manifest_verified": True,
        "artifact_sha256": declared["sha256"],
        "input_sha256": manifest["input_sha256"],
        "snapshot_sha256": hashlib.sha256(
            json.dumps(manifest["snapshot"], sort_keys=True,
                       separators=(",", ":")).encode("utf-8")).hexdigest(),
    }


def verify_provenance_pair_artifacts(legacy_path, legacy_blob_sha, pair,
                                     legacy_archive, replacement_archive, *,
                                     replacement_workflow_root=None):
    """Verify both artifact manifests before comparing the declared pair."""
    comparison = compare_provenance_bound_pair(
        legacy_path, legacy_blob_sha, pair,
        replacement_workflow_root=replacement_workflow_root)
    legacy = verify_parity_artifact_manifest(pair["legacy"], legacy_archive)
    replacement = verify_parity_artifact_manifest(
        pair["replacement"], replacement_archive)
    if legacy["input_sha256"] != replacement["input_sha256"]:
        raise ValueError("Artifact manifests do not use the same input")
    return {
        **comparison,
        "artifact_manifests_verified": True,
        "same_input_artifacts_verified": True,
        "legacy_artifact_manifest": legacy,
        "replacement_artifact_manifest": replacement,
        "behavioral_parity_accepted": False,
        "production_ready": False,
    }
