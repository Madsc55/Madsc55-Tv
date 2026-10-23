"""Read-only GitHub API inventory of all 99 legacy workflow source blobs."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.parse
from madsc.github_history_client import github_json
from madsc.write_path_audit import enforce_local_output_path
from madsc.legacy_workflow_safety import assess_workflow_source

REPO = "Madsc55/madsc-tv"
BRANCH = "madsc/bes-sistem-toplu-birlestirme"



K_HINTS = {
    "K1": ("guvenlik", "security", "izin", "koruma"),
    "K2": ("kesif", "discovery", "aday", "candidate", "kaynak", "gecmis"),
    "K3": ("kanal-test", "iptv-test", "epg", "logo", "ibo", "stream", "retest"),
    "K4": ("yedek", "backup", "restore", "arsiv"),
    "K5": ("bakim", "maintenance", "rapor", "report", "saglik", "son-kontrol", "denetim"),
}


def candidate_stages(path):
    """Filename-based planning hints only; never behavioral acceptance."""
    name = Path(path).stem.casefold()
    stages = [stage for stage, terms in K_HINTS.items()
              if any(term in name for term in terms)]
    return stages or ["UNCLASSIFIED"]

def summarize_blockers(rows):
    """Report evidence work by type without treating inventory as parity."""
    required = ("legacy_execution", "new_execution", "input_output_comparison",
                "side_effect_comparison", "failure_timeout_comparison",
                "reviewer_approval")
    if not isinstance(rows, list):
        raise ValueError("Invalid workflow audit rows")
    counts = {name: 0 for name in required}
    for row in rows:
        if not isinstance(row, dict) or row.get("behavioral_parity_verified") is not False:
            raise ValueError("Unexpected accepted workflow")
        missing = row.get("evidence_missing")
        if (not isinstance(missing, list) or any(not isinstance(item, str) for item in missing)
                or len(missing) != len(required) or set(missing) != set(required)):
            raise ValueError("Invalid evidence blocker set")
        for name in missing:
            counts[name] += 1
    return counts


def github(url, token):
    return github_json(url, token=token)


def run(output, token):
    path = Path(output)
    enforce_local_output_path(path.absolute())
    if path.exists() or path.is_symlink():
        raise ValueError("Will not overwrite evidence")
    ref = urllib.parse.quote(BRANCH, safe="")
    tree = github(f"https://api.github.com/repos/{REPO}/git/trees/{ref}?recursive=1", token)
    if tree.get("truncated"):
        raise ValueError("Incomplete legacy tree")
    entries = sorted((item for item in tree["tree"]
                      if item["path"].startswith(".github/workflows/")
                      and item["path"].endswith((".yml", ".yaml"))
                      and item["type"] == "blob"), key=lambda item: item["path"])
    if len(entries) != 99:
        raise ValueError(f"Expected 99 original workflows, got {len(entries)}")
    rows = []
    for item in entries:
        if item.get("size", 0) > 250000:
            raise ValueError("Oversized workflow")
        blob = github(f"https://api.github.com/repos/{REPO}/git/blobs/{item['sha']}", token)
        if blob.get("encoding") != "base64":
            raise ValueError("Unexpected blob encoding")
        raw = base64.b64decode("".join(blob["content"].split()), validate=True)
        expected_sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
        if expected_sha != item["sha"] or blob.get("sha") != item["sha"]:
            raise ValueError("Source blob SHA mismatch")
        if len(raw) != item.get("size"):
            raise ValueError("Source blob size mismatch")
        source = raw.decode("utf-8")
        rows.append({
            "path": item["path"], "git_blob_sha": item["sha"], "bytes": len(raw),
            "uses": sorted(set(re.findall(r"(?m)^\s*-?\s*uses:\s*([^\s#]+)", source))),
            "trigger_indicators": sorted(set(re.findall(r"(?m)^\s*(workflow_dispatch|workflow_call|push|pull_request|schedule|workflow_run):", source))),
            "command_lines": [line.strip() for line in source.splitlines()
                              if any(word in line for word in ("python ", "python3 ", "bash ", "node ", "ffmpeg", "ffprobe"))][:150],
            "permission_lines": [line.strip() for line in source.splitlines()
                                 if any(word in line for word in ("contents:", "actions:", "pages:", "id-token:"))][:50],
            "artifact_lines": [line.strip() for line in source.splitlines()
                               if "upload-artifact" in line or "download-artifact" in line][:50],
            "candidate_k_stages": candidate_stages(item["path"]),
            "stage_mapping_reviewed": False,
            "failure_circuit_source_scope": assess_workflow_source(source),
            "behavioral_parity_verified": False,
            "behavioral_evidence_status": "BLOCKED_NEEDS_BEHAVIOR_EVIDENCE",
            "evidence_missing": ["legacy_execution", "new_execution",
                                 "input_output_comparison", "side_effect_comparison",
                                 "failure_timeout_comparison", "reviewer_approval"],
        })
    if len({row["path"] for row in rows}) != 99:
        raise ValueError("Duplicate workflow paths")
    blocker_counts = summarize_blockers(rows)
    report = {"candidate_mapping_only": True, "source_repository": REPO, "source_branch": BRANCH, "source_tree_sha": tree.get("sha"), "source_workflow_count": 99,
              "behavioral_parity_verified_count": 0,
              "blocked_workflow_count": len(rows),
              "missing_evidence_by_type": blocker_counts,
              "production_writes": False, "workflows": rows}
    path = Path(output)
    if path.exists():
        raise ValueError("Will not overwrite evidence")
    enforce_local_output_path(path.absolute())
    with path.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2, sort_keys=True)
    print(json.dumps({"workflow_count": len(rows), "behavioral_parity_verified_count": 0}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    run(args.output, os.getenv("GITHUB_TOKEN", ""))
