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
    if len(discovery["candidates"]) > 20000:
        raise ValueError("Too many candidates in discovery")
    alternatives = discovery.get("alternatives", [])
    if not isinstance(alternatives, list):
        raise ValueError("Invalid alternative evidence")
    if len(alternatives) > 20000:
        raise ValueError("Too many alternatives in discovery")
    assess_candidates(discovery, {})
    body = {"schema": 1, "run_id": run_id, "commit_sha": commit_sha, "discovery": discovery}
    try:
        serialized = json.dumps(body, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError, OverflowError, RecursionError) as exc:
        raise ValueError("Invalid JSON discovery evidence") from exc
    if len(serialized.encode("utf-8")) > 16 * 1024 * 1024:
        raise ValueError("Oversized discovery evidence")
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
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
