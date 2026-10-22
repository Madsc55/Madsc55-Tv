"""Bounded parser for same-input legacy parity evidence artifacts."""
import hashlib
import io
import json
import stat
import zipfile

from madsc.legacy_parity_cli import unique_pairs
from madsc.legacy_parity_evidence import compare_provenance_bound_pair


MANIFEST_NAME = "madsc-parity-evidence.json"
MAX_ARCHIVE_BYTES = 2 * 1024 * 1024
MAX_MANIFEST_BYTES = 1024 * 1024


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
            if (info.is_dir() or info.file_size > MAX_MANIFEST_BYTES
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
