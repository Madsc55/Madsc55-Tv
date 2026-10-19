"""Independent GitHub Actions provenance verification (no production writes).

The caller supplies independently retrieved GitHub REST responses and an ancestry
verdict. Manifest-provided GitHub metadata must never be reused as these inputs.
"""
import re

SHA = re.compile(r"[0-9a-f]{40}\Z")


def verify_github_origin(manifest, run, artifacts, *, repository, branch,
                         workflow_path, current_sha, ancestry_verdict):
    if not isinstance(manifest, dict) or not isinstance(run, dict):
        raise ValueError("Missing independent provenance records")
    source_id = manifest.get("source_run_id")
    source_sha = manifest.get("source_commit_sha")
    if (not isinstance(source_id, str) or not re.fullmatch(r"[0-9]+", source_id)
            or not isinstance(source_sha, str) or not SHA.fullmatch(source_sha)
            or not isinstance(current_sha, str) or not SHA.fullmatch(current_sha)):
        raise ValueError("Invalid run or commit identity")
    if (str(run.get("id")) != source_id or run.get("head_sha") != source_sha
            or (run.get("repository") or {}).get("full_name") != repository
            or (run.get("head_repository") or {}).get("full_name") != repository
            or run.get("head_branch") != branch
            or run.get("path") != workflow_path
            or run.get("status") != "completed"
            or run.get("conclusion") != "success"
            or run.get("event") not in ("push", "workflow_dispatch", "schedule")):
        raise ValueError("GitHub workflow provenance mismatch")
    # GitHub compare(base=source_sha, head=current_sha) must say identical/ahead.
    if ancestry_verdict not in ("identical", "ahead"):
        raise ValueError("Source commit is not a verified ancestor")
    matches = [a for a in artifacts if a.get("name") == "madsc-k2-history-source"]
    if len(matches) != 1:
        raise ValueError("Missing or ambiguous history source artifact")
    artifact = matches[0]
    if (artifact.get("expired") is not False
            or (artifact.get("workflow_run") or {}).get("id") != run["id"]
            or (artifact.get("workflow_run") or {}).get("head_sha") != source_sha
            or not isinstance(artifact.get("id"), int)):
        raise ValueError("GitHub artifact provenance mismatch")
    return {"github_origin_verified": True, "source_run_id": source_id,
            "source_commit_sha": source_sha, "artifact_id": artifact["id"],
            "production_ready": False}
