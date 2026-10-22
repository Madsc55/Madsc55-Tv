"""Read-only GitHub verifier for provenance-bound legacy comparison pairs.

The caller supplies bounded snapshots and declared identities.  This module
independently reads each run, its artifact listing, and the workflow blob at
the recorded head SHA.  It never dispatches Actions or downloads artifacts.
"""
from urllib.parse import quote

from madsc.github_history_client import github_json
from madsc.legacy_pair_artifact import verify_failure_diagnostic_artifact
from madsc.legacy_parity_evidence import compare_provenance_bound_pair


def _artifact_digest(item):
    digest = item.get("digest")
    return digest[7:] if isinstance(digest, str) and digest.startswith("sha256:") else None


def verify_execution_origin_api(origin, run, artifact_page, workflow_file):
    """Cross-check one declared origin against three independent API records."""
    if not all(isinstance(value, dict) for value in (origin, run, artifact_page, workflow_file)):
        raise ValueError("Invalid GitHub origin records")
    repository = origin.get("repository")
    if (run.get("id") != origin.get("run_id")
            or run.get("run_attempt") != origin.get("run_attempt")
            or run.get("head_sha") != origin.get("head_sha")
            or run.get("head_branch") != origin.get("branch")
            or run.get("path") != origin.get("workflow_path")
            or run.get("event") != origin.get("event")
            or run.get("status") != "completed"
            or run.get("conclusion") != origin.get("conclusion")
            or not isinstance(run.get("repository"), dict)
            or run["repository"].get("full_name") != repository
            or not isinstance(run.get("head_repository"), dict)
            or run["head_repository"].get("full_name") != repository):
        raise ValueError("GitHub run origin mismatch")
    if (workflow_file.get("type") != "file"
            or workflow_file.get("path") != origin.get("workflow_path")
            or workflow_file.get("sha") != origin.get("workflow_blob_sha")):
        raise ValueError("Workflow blob origin mismatch")
    artifacts = artifact_page.get("artifacts")
    if (not isinstance(artifacts, list)
            or type(artifact_page.get("total_count")) is not int
            or artifact_page["total_count"] != len(artifacts)
            or len(artifacts) > 100):
        raise ValueError("Incomplete artifact listing")
    declared = origin.get("artifact")
    if not isinstance(declared, dict):
        raise ValueError("Missing declared artifact")
    if not all(isinstance(item, dict) for item in artifacts):
        raise ValueError("Invalid artifact listing entries")
    matches = [item for item in artifacts
               if item.get("id") == declared.get("id")
               and item.get("name") == declared.get("name")]
    if len(matches) != 1:
        raise ValueError("Missing or ambiguous artifact")
    artifact = matches[0]
    workflow_run = artifact.get("workflow_run")
    if not isinstance(workflow_run, dict):
        raise ValueError("Invalid artifact workflow origin")
    if (artifact.get("expired") is not False
            or workflow_run.get("id") != origin.get("run_id")
            or workflow_run.get("head_sha") != origin.get("head_sha")
            or _artifact_digest(artifact) != declared.get("sha256")):
        raise ValueError("GitHub artifact origin or digest mismatch")
    return {
        "repository": repository,
        "run_id": origin["run_id"],
        "run_attempt": origin["run_attempt"],
        "head_sha": origin["head_sha"],
        "workflow_blob_sha": origin["workflow_blob_sha"],
        "artifact_id": declared["id"],
        "artifact_sha256": declared["sha256"],
        "github_api_origin_verified": True,
    }


def fetch_verified_execution_origin(origin, *, token=None, fetch=github_json):
    repository = origin.get("repository") if isinstance(origin, dict) else None
    run_id = origin.get("run_id") if isinstance(origin, dict) else None
    head_sha = origin.get("head_sha") if isinstance(origin, dict) else None
    workflow_path = origin.get("workflow_path") if isinstance(origin, dict) else None
    if (repository not in {"Madsc55/madsc-tv", "Madsc55/Madsc55-Tv"}
            or type(run_id) is not int or run_id <= 0
            or not isinstance(head_sha, str) or len(head_sha) != 40
            or not isinstance(workflow_path, str)
            or not workflow_path.startswith(".github/workflows/")):
        raise ValueError("Invalid declared execution origin")
    base = "https://api.github.com/repos/" + repository
    run = fetch(f"{base}/actions/runs/{run_id}", token=token)
    artifacts = fetch(f"{base}/actions/runs/{run_id}/artifacts?per_page=100", token=token)
    encoded_path = quote(workflow_path, safe="/")
    workflow = fetch(f"{base}/contents/{encoded_path}?ref={quote(head_sha)}", token=token)
    return verify_execution_origin_api(origin, run, artifacts, workflow)


def verify_failure_diagnostic_evidence(origin, diagnostic_artifact, archive, *,
                                       token=None, fetch=github_json):
    """Verify diagnostic bytes and their separate GitHub artifact origin."""
    byte_proof = verify_failure_diagnostic_artifact(
        origin, diagnostic_artifact, archive)
    diagnostic_origin = {**origin, "artifact": dict(diagnostic_artifact)}
    api_proof = fetch_verified_execution_origin(
        diagnostic_origin, token=token, fetch=fetch)
    return {
        **byte_proof,
        "diagnostic_artifact_api_origin_verified": True,
        "diagnostic_api_origin": api_proof,
        "behavioral_parity_accepted": False,
        "production_ready": False,
    }


def verify_provenance_pair_api(legacy_path, legacy_blob_sha, pair, *, token=None,
                               fetch=github_json, replacement_workflow_root=None):
    """Verify both API origins, then compare their same-input snapshots."""
    comparison = compare_provenance_bound_pair(
        legacy_path, legacy_blob_sha, pair,
        replacement_workflow_root=replacement_workflow_root)
    legacy_api = fetch_verified_execution_origin(pair["legacy"], token=token, fetch=fetch)
    replacement_api = fetch_verified_execution_origin(
        pair["replacement"], token=token, fetch=fetch)
    if ((legacy_api["repository"], legacy_api["run_id"])
            == (replacement_api["repository"], replacement_api["run_id"])
            or (legacy_api["repository"], legacy_api["artifact_id"])
            == (replacement_api["repository"], replacement_api["artifact_id"])):
        raise ValueError("GitHub origins are not independent")
    return {
        **comparison,
        "independent_origin_api_verified": True,
        "legacy_api_origin": legacy_api,
        "replacement_api_origin": replacement_api,
        # API provenance plus snapshot equality is still not reviewer or
        # production acceptance for a legacy behavior.
        "behavioral_parity_accepted": False,
        "production_ready": False,
    }
