"""Read-only GitHub verifier for provenance-bound legacy comparison pairs.

The caller supplies bounded snapshots and declared identities.  This module
independently reads each run, its artifact listing, and the workflow blob at
the recorded head SHA. Optional bounded ZIP downloads bind API origins to bytes.
It never dispatches Actions or writes production data.
"""
from urllib.parse import quote
from madsc.github_transport import GitHubRedirectHandler, github_opener
import re

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
    if (type(run.get("id")) is not int
            or type(run.get("run_attempt")) is not int
            or run.get("id") != origin.get("run_id")
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
    if (not isinstance(declared, dict)
            or type(declared.get("id")) is not int
            or declared["id"] <= 0):
        raise ValueError("Missing or invalid declared artifact")
    if not all(isinstance(item, dict) for item in artifacts):
        raise ValueError("Invalid artifact listing entries")
    artifact_ids = [item.get("id") for item in artifacts]
    if (any(type(value) is not int or value <= 0 for value in artifact_ids)
            or len(set(artifact_ids)) != len(artifact_ids)):
        raise ValueError("Invalid or duplicate artifact IDs")
    matches = [item for item in artifacts
               if item.get("id") == declared.get("id")
               and item.get("name") == declared.get("name")]
    if len(matches) != 1:
        raise ValueError("Missing or ambiguous artifact")
    artifact = matches[0]
    workflow_run = artifact.get("workflow_run")
    if not isinstance(workflow_run, dict):
        raise ValueError("Invalid artifact workflow origin")
    run_repository_id = run["repository"].get("id")
    head_repository_id = run["head_repository"].get("id")
    for key, expected in (("repository_id", run_repository_id),
                          ("head_repository_id", head_repository_id)):
        if key in workflow_run and expected is not None:
            if (type(workflow_run[key]) is not int
                    or type(expected) is not int
                    or workflow_run[key] != expected):
                raise ValueError("Artifact repository identity mismatch")
    if ("run_attempt" in workflow_run
            and (type(workflow_run["run_attempt"]) is not int
                 or workflow_run["run_attempt"] != origin.get("run_attempt"))):
        raise ValueError("Artifact run attempt mismatch")
    if ("status" in workflow_run
            and workflow_run["status"] != "completed"):
        raise ValueError("Artifact workflow status mismatch")
    if ("conclusion" in workflow_run
            and workflow_run["conclusion"] != origin.get("conclusion")):
        raise ValueError("Artifact workflow conclusion mismatch")
    if ("event" in workflow_run
            and workflow_run["event"] != origin.get("event")):
        raise ValueError("Artifact event origin mismatch")
    if ("head_branch" in workflow_run
            and workflow_run["head_branch"] != origin.get("branch")):
        raise ValueError("Artifact branch origin mismatch")
    if (type(workflow_run.get("id")) is not int
            or artifact.get("expired") is not False
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
            or not isinstance(head_sha, str)
            or re.fullmatch(r"[0-9a-f]{40}", head_sha) is None
            or not isinstance(workflow_path, str)
            or not workflow_path.startswith(".github/workflows/")
            or any(segment in {"", ".", ".."} for segment in workflow_path.split("/"))
            or not workflow_path.endswith((".yml", ".yaml"))):
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


# Artifacts are downloaded only after both independent API origins pass.
# Redirects to signed storage URLs must not receive the GitHub bearer token.
def _artifact_opener():
    return github_opener(allow_storage=True)


class _ArtifactRedirectHandler(GitHubRedirectHandler):
    def __init__(self):
        super().__init__(allow_storage=True)


def download_execution_artifact(origin, *, token, opener=None):
    """Read a bounded ZIP from its fixed GitHub artifact endpoint; never extract."""
    from urllib.request import Request
    from urllib.error import HTTPError, URLError
    from madsc.legacy_pair_artifact import MAX_ARCHIVE_BYTES
    repository = origin.get("repository") if isinstance(origin, dict) else None
    artifact = origin.get("artifact") if isinstance(origin, dict) else None
    if (repository not in {"Madsc55/madsc-tv", "Madsc55/Madsc55-Tv"}
            or not isinstance(artifact, dict)
            or type(artifact.get("id")) is not int or artifact["id"] <= 0
            or not isinstance(token, str) or not token):
        raise ValueError("Invalid artifact download identity or missing token")
    request = Request(
        f"https://api.github.com/repos/{repository}/actions/artifacts/{artifact['id']}/zip",
        headers={"Authorization": "Bearer " + token,
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "madsc55-parity-evidence"}, method="GET")
    opener = _artifact_opener().open if opener is None else opener
    try:
        with opener(request, timeout=30) as response:
            archive = response.read(MAX_ARCHIVE_BYTES + 1)
    except (HTTPError, URLError, TimeoutError) as exc:
        raise ValueError("GitHub parity artifact download failed") from exc
    if not isinstance(archive, bytes) or not archive or len(archive) > MAX_ARCHIVE_BYTES:
        raise ValueError("Invalid parity artifact download size")
    return archive


def verify_provenance_pair_evidence(legacy_path, legacy_blob_sha, pair, *,
                                    token=None, fetch=github_json,
                                    download=download_execution_artifact,
                                    replacement_workflow_root=None):
    """Bind API-verified independent executions to both actual ZIP manifests.

    Snapshot agreement still requires semantic/side-effect review. No production
    or behavioral acceptance is granted by this transport/evidence verification.
    """
    from madsc.legacy_pair_artifact import verify_provenance_pair_artifacts
    if not isinstance(token, str) or not token:
        raise ValueError("GitHub artifact token required")
    api = verify_provenance_pair_api(
        legacy_path, legacy_blob_sha, pair, token=token, fetch=fetch,
        replacement_workflow_root=replacement_workflow_root)
    archives = [download(pair[role], token=token) for role in ("legacy", "replacement")]
    byte_proof = verify_provenance_pair_artifacts(
        legacy_path, legacy_blob_sha, pair, *archives,
        replacement_workflow_root=replacement_workflow_root)
    return {**api, **byte_proof,
            "independent_origin_api_verified": True,
            "api_bound_artifact_bytes_verified": True,
            "artifacts_downloaded": 2,
            "behavioral_parity_accepted": False, "production_ready": False}
