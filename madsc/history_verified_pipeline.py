"""Verified K2 history source orchestration, without fixture fallback.

The manifest's hashes are cross-checked with artifact bytes, but are not an
independent publisher signature. Do not treat this as production authorization.
"""
import json
import os
import tempfile
from pathlib import Path

from madsc.github_history_client import verify_live_github_origin
from madsc.history_artifact_download import download_verified_history_artifact
from madsc.history_handoff import pack_history
from madsc.history_source_gate import load_verified_source
from madsc.write_path_audit import enforce_local_output_path


def produce_verified_history(manifest_path, output_path, *, current_sha, run_id,
                             token=None, verify_origin=verify_live_github_origin,
                             download=download_verified_history_artifact):
    manifest_path, output_path = Path(manifest_path), Path(output_path)
    # K1 guards the destination before network verification or artifact download.
    enforce_local_output_path(output_path if output_path.is_absolute() else Path.cwd() / output_path)
    if manifest_path.is_symlink() or not manifest_path.is_file() or output_path.is_symlink():
        raise ValueError("Unsafe manifest or output path")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("mode") != "VERIFIED_SOURCE":
        raise ValueError("Verified real source required")
    if not token:
        raise ValueError("GitHub artifact token required")
    origin = verify_origin(
        manifest, repository="Madsc55/Madsc55-Tv", branch="main",
        workflow_path=".github/workflows/madsc-k2-real-history-source.yml",
        current_sha=current_sha, token=token)
    with tempfile.TemporaryDirectory(prefix="madsc-verified-history-") as tmp:
        folder = Path(tmp) / "source"
        download(repository="Madsc55/Madsc55-Tv",
                 artifact_id=origin["artifact_id"], token=token,
                 expected_hashes=manifest["hashes"], destination=folder)
        pair = load_verified_source(
            folder, manifest_path, run_id=origin["source_run_id"],
            commit_sha=origin["source_commit_sha"])
        handoff = pack_history(pair, run_id, current_sha)
    if output_path.exists() or output_path.is_symlink():
        raise ValueError("Refusing to overwrite existing history evidence")
    if not output_path.parent.is_dir() or output_path.parent.is_symlink():
        raise ValueError("Evidence output parent must be an existing real directory")
    # Exclusive creation prevents replacing evidence created by another process.
    with output_path.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(handoff, sort_keys=True) + "\n")
    return {"verified_source_run": origin["source_run_id"],
            "verified_artifact_id": origin["artifact_id"],
            "handoff_digest": handoff["digest"], "production_ready": False}
