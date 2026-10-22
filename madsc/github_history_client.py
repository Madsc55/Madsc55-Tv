"""Read-only GitHub REST provenance client.

Fetches independent GitHub records, not values copied from a source manifest.
Requires explicit repository, current SHA, and approved workflow.
"""
import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request
from madsc.github_transport import github_opener

from madsc.github_history_origin import verify_github_origin


def github_json(path, *, token, opener=None):
    if not path.startswith("https://api.github.com/"):
        raise ValueError("Unexpected GitHub API URL")
    headers = {"Accept": "application/vnd.github+json",
               "X-GitHub-Api-Version": "2022-11-28",
               "User-Agent": "madsc55-history-origin"}
    if token:
        headers["Authorization"] = "Bearer " + token
    request = Request(path, headers=headers, method="GET")
    opener = github_opener().open if opener is None else opener
    try:
        with opener(request, timeout=15) as response:
            raw = response.read(2 * 1024 * 1024 + 1)
    except (HTTPError, URLError, TimeoutError) as exc:
        raise ValueError("GitHub provenance request failed") from exc
    if len(raw) > 2 * 1024 * 1024:
        raise ValueError("Oversized GitHub provenance response")
    try:
        return json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid GitHub provenance JSON") from exc


def verify_live_github_origin(manifest, *, repository, branch, workflow_path,
                              current_sha, token=None, fetch=github_json):
    if repository != "Madsc55/Madsc55-Tv" or branch != "main":
        raise ValueError("Unexpected repository or branch")
    run_id = manifest.get("source_run_id")
    source_sha = manifest.get("source_commit_sha")
    if not isinstance(run_id, str) or not run_id.isascii() or not run_id.isdigit():
        raise ValueError("Invalid source run ID")
    if not isinstance(source_sha, str) or len(source_sha) != 40 or any(
            c not in "0123456789abcdef" for c in source_sha):
        raise ValueError("Invalid source SHA")
    base = "https://api.github.com/repos/" + repository
    run = fetch(base + "/actions/runs/" + quote(run_id), token=token)
    artifact_page = fetch(base + "/actions/runs/" + quote(run_id) + "/artifacts?per_page=100",
                          token=token)
    if not isinstance(artifact_page, dict) or not isinstance(artifact_page.get("artifacts"), list):
        raise ValueError("Invalid artifact listing")
    if artifact_page.get("total_count") != len(artifact_page["artifacts"]):
        raise ValueError("Artifact pagination required; refusing incomplete listing")
    comparison = fetch(base + "/compare/" + source_sha + "..." + current_sha, token=token)
    if not isinstance(comparison, dict):
        raise ValueError("Invalid GitHub ancestry comparison")
    return verify_github_origin(
        manifest, run, artifact_page["artifacts"], repository=repository,
        branch=branch, workflow_path=workflow_path, current_sha=current_sha,
        ancestry_verdict=comparison.get("status"))
