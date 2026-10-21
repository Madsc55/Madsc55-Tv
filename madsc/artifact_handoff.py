"""Read-only K2 to K3 candidate evidence envelope."""
import hashlib
import json
import re
from madsc.handoff import assess_candidates

def pack(discovery, run_id, commit_sha):
    if not isinstance(run_id, str) or not re.fullmatch(r"[0-9]+", run_id):
        raise ValueError("Invalid run id")
    if not isinstance(commit_sha, str) or len(commit_sha) != 40 or any(c not in "0123456789abcdef" for c in commit_sha):
        raise ValueError("Invalid commit SHA")
    if not isinstance(discovery, dict) or not isinstance(discovery.get("candidates"), list):
        raise ValueError("Invalid discovery")
    assess_candidates(discovery, {})
    body = {"schema": 1, "run_id": run_id, "commit_sha": commit_sha, "discovery": discovery}
    digest = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {**body, "digest": digest}

def unpack(envelope, run_id, commit_sha):
    if not isinstance(envelope, dict) or set(envelope) != {"schema", "run_id", "commit_sha", "discovery", "digest"}:
        raise ValueError("Invalid evidence envelope")
    if envelope["schema"] != 1 or envelope["run_id"] != run_id or envelope["commit_sha"] != commit_sha:
        raise ValueError("Evidence provenance mismatch")
    expected = pack(envelope["discovery"], run_id, commit_sha)
    if not isinstance(envelope["digest"], str) or envelope["digest"] != expected["digest"]:
        raise ValueError("Evidence digest mismatch")
    return envelope["discovery"]
