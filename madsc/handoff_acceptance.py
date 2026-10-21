"""Cross-check K2, K3 and K5 read-only evidence from one Actions run."""
import argparse
import json
from pathlib import Path
from madsc.write_path_audit import enforce_local_output_path
from madsc.artifact_handoff import unpack
from madsc.batch_acceptance import _unique_json_pairs

def verify(k2, k3, k5, run_id, commit_sha):
    discovery = unpack(k2, run_id, commit_sha)
    expected = {"schema": "madsc-handoff-verification-v1", "run_id": run_id,
                "commit_sha": commit_sha, "source_digest": k2["digest"],
                "candidate_count": len(discovery["candidates"]), "read_only": True,
                "network_probed": False, "production_ready": False}
    if k3 != expected or k5 != expected:
        raise ValueError("K2-K3-K5 evidence mismatch")
    return {"k2_k3_k5_same_run_verified": True, "candidate_count": expected["candidate_count"],
            "source_digest": expected["source_digest"], "production_ready": False}

def load(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ValueError("Invalid evidence path")
    if path.stat().st_size > 16 * 1024 * 1024:
        raise ValueError("Evidence exceeds 16 MiB safety limit")
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_json_pairs)

def main():
    p = argparse.ArgumentParser()
    for arg in ("k2", "k3", "k5", "output"):
        p.add_argument("--" + arg, required=True, type=Path)
    p.add_argument("--run-id", required=True)
    p.add_argument("--commit-sha", required=True)
    a = p.parse_args()
    enforce_local_output_path(a.output.absolute())
    result = verify(load(a.k2), load(a.k3), load(a.k5), a.run_id, a.commit_sha)
    if a.output.is_symlink():
        raise ValueError("Invalid acceptance output path")
    enforce_local_output_path(a.output.absolute())
    with a.output.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, sort_keys=True) + "\n")
    print(json.dumps(result))
if __name__ == "__main__":
    main()
