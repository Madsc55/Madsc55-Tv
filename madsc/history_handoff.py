"""K2 history envelope transport bound to a single GitHub run and commit.

Independent from candidate transport; fixture evidence only, never production approval.
"""
import hashlib
import json
import re
from pathlib import Path

from madsc.history_pair_store import decode_pair, encode_pair
from madsc.batch_acceptance import _unique_json_pairs


def pack_history(pair, run_id, commit_sha):
    if not isinstance(run_id, str) or not re.fullmatch(r"[0-9]+", run_id):
        raise ValueError("Invalid run id")
    if not isinstance(commit_sha, str) or not re.fullmatch(r"[0-9a-f]{40}", commit_sha):
        raise ValueError("Invalid commit")
    payload = json.loads(encode_pair(pair))
    body = {"schema": 1, "run_id": run_id, "commit_sha": commit_sha,
            "history_envelope": payload, "read_only": True,
            "production_ready": False}
    digest = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {**body, "digest": digest}


def unpack_history(envelope, run_id, commit_sha):
    if not isinstance(envelope, dict) or set(envelope) != {
            "schema", "run_id", "commit_sha", "history_envelope", "read_only",
            "production_ready", "digest"}:
        raise ValueError("Invalid history handoff")
    if (envelope["schema"] != 1 or envelope["run_id"] != run_id
            or envelope["commit_sha"] != commit_sha
            or envelope["read_only"] is not True
            or envelope["production_ready"] is not False):
        raise ValueError("History handoff provenance or approval mismatch")
    history = decode_pair(json.dumps(envelope["history_envelope"]))
    expected = pack_history(history, run_id, commit_sha)
    if envelope["digest"] != expected["digest"]:
        raise ValueError("History handoff digest mismatch")
    return history


def load_history(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 16 * 1024 * 1024:
        raise ValueError("Unsafe history handoff path")
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_json_pairs)


def verify_history_chain(k2, k3, k5, run_id, commit_sha):
    unpack_history(k2, run_id, commit_sha)
    expected = {"schema": "madsc-history-handoff-v1", "run_id": run_id,
                "commit_sha": commit_sha, "source_digest": k2["digest"],
                "read_only": True, "production_ready": False}
    if k3 != expected or k5 != expected:
        raise ValueError("K2-K3-K5 history chain mismatch")
    return {"history_chain_verified": True, "source_digest": k2["digest"],
            "production_ready": False}
