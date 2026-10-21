"""CLI for isolated K2 history evidence and K3/K5 read-only receipts."""
import argparse
import json
from pathlib import Path

from madsc.history_handoff import load_history, pack_history, unpack_history, verify_history_chain
from madsc.history_pair_bridge import import_legacy_pair
from madsc.write_path_audit import enforce_local_output_path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=("produce", "consume", "verify"))
    p.add_argument("--legacy-folder", type=Path)
    p.add_argument("--path", type=Path)
    p.add_argument("--k2", type=Path)
    p.add_argument("--k3", type=Path)
    p.add_argument("--k5", type=Path)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--commit-sha", required=True)
    a = p.parse_args()
    if a.action == "produce":
        result = pack_history(import_legacy_pair(a.legacy_folder), a.run_id, a.commit_sha)
    elif a.action == "consume":
        source = load_history(a.path)
        unpack_history(source, a.run_id, a.commit_sha)
        result = {"schema": "madsc-history-handoff-v1", "run_id": a.run_id,
                  "commit_sha": a.commit_sha, "source_digest": source["digest"],
                  "read_only": True, "production_ready": False}
    else:
        result = verify_history_chain(load_history(a.k2), load_history(a.k3),
                                      load_history(a.k5), a.run_id, a.commit_sha)
    if a.output.is_symlink():
        raise ValueError("Symlinked output")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    enforce_local_output_path(a.output.absolute())
    a.output.write_text(json.dumps(result, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
