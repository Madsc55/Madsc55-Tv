"""H03 source-run provenance gate, independent of production artifacts."""
import re

SHA = re.compile(r"[0-9a-f]{40}\Z")


def select_ancestor_run(runs, *, repo, branch, current_run, ancestor_check, workflows):
    if (not isinstance(runs, list) or len(runs) > 20000
            or not isinstance(workflows, (list, tuple, set))
            or len(workflows) > 200 or any(not isinstance(x, str) for x in workflows)
            or any(not isinstance(run, dict) for run in runs)):
        raise ValueError("Invalid source run inventory")
    eligible = []
    allowed = {".github/workflows/" + name for name in workflows}
    for run in runs:
        if (str(run.get("id")) == str(current_run)
                or run.get("head_branch") != branch
                or run.get("status") != "completed"
                or run.get("conclusion") != "success"
                or (run.get("head_repository") or {}).get("full_name") != repo
                or run.get("path") not in allowed
                or run.get("event") not in ("push", "schedule", "workflow_dispatch")):
            continue
        sha = run.get("head_sha")
        if not isinstance(sha, str) or not SHA.fullmatch(sha):
            raise ValueError("Invalid source commit")
        verdict = ancestor_check(sha)
        if verdict is None:
            raise ValueError("Cannot verify source commit ancestry")
        if verdict:
            eligible.append(run)
    return max(eligible, key=lambda r: (r["created_at"], r["id"])) if eligible else None


def verify_artifact_provenance(source, artifacts, artifact_name):
    if (not isinstance(source, dict) or not isinstance(artifacts, list)
            or len(artifacts) > 20000 or any(not isinstance(item, dict) for item in artifacts)
            or not isinstance(artifact_name, str) or not artifact_name):
        raise ValueError("Invalid artifact provenance")
    matches = [item for item in artifacts if item.get("name") == artifact_name]
    if len(matches) != 1 or matches[0].get("expired"):
        raise ValueError("Artifact missing, duplicate or expired")
    run = matches[0].get("workflow_run") or {}
    if run.get("id") != source["id"] or run.get("head_sha") != source["head_sha"]:
        raise ValueError("Artifact run/commit mismatch")
    return True
