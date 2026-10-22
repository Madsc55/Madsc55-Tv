"""Read-only CLI for batch legacy/replacement execution snapshot comparison."""
import argparse
import json
from pathlib import Path
from madsc.legacy_parity_evidence import (compare_snapshot_batch,
                                         compare_provenance_bound_batch)
from madsc.write_path_audit import enforce_local_output_path


def load_json(path):
    with Path(path).open("r", encoding="utf-8") as stream:
        return json.load(stream, object_pairs_hook=unique_pairs)


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def run(inventory_path, snapshots_path, output_path, *, replacement_workflow_root=None,
        verify_github_artifacts=False, token=None, fetch=None, download=None):
    destination = Path(output_path)
    if destination.exists() or destination.is_symlink():
        raise ValueError("Refusing to overwrite comparison evidence")
    enforce_local_output_path(destination.absolute())
    inventory = load_json(inventory_path)
    snapshots = load_json(snapshots_path)
    if (isinstance(snapshots, dict)
            and snapshots.get("schema") == "madsc-legacy-provenance-pairs-v1"
            and {"schema", "pairs"} <= set(snapshots)
            and set(snapshots) <= {"schema", "pairs", "behavior_mappings", "mapping_review_rows"}):
        report = compare_provenance_bound_batch(
            inventory, snapshots["pairs"], replacement_workflow_root=replacement_workflow_root,
            behavior_mappings=snapshots.get("behavior_mappings"),
            mapping_review_rows=snapshots.get("mapping_review_rows"))
        if verify_github_artifacts:
            from madsc.github_legacy_pair_client import verify_provenance_pair_evidence
            if not snapshots["pairs"]:
                raise ValueError("GitHub verification requires supplied execution pairs")
            if not isinstance(token, str) or not token:
                raise ValueError("GitHub artifact token required")
            blobs = {row["path"]: row["git_blob_sha"] for row in inventory["workflows"]}
            dependencies = {}
            if fetch is not None:
                dependencies["fetch"] = fetch
            if download is not None:
                dependencies["download"] = download
            proofs = {path: verify_provenance_pair_evidence(
                path, blobs[path], pair, token=token,
                replacement_workflow_root=replacement_workflow_root, **dependencies)
                for path, pair in sorted(snapshots["pairs"].items())}
            report["github_artifact_verification"] = {
                "supplied_pairs_verified": len(proofs), "proofs": proofs,
                "behavioral_parity_accepted": 0, "production_ready": False}
    else:
        if verify_github_artifacts:
            raise ValueError("GitHub verification requires provenance-bound pairs")
        if replacement_workflow_root is not None:
            raise ValueError("Workflow preflight requires provenance-bound pairs")
        report = compare_snapshot_batch(inventory, snapshots)
    destination = Path(output_path)
    if destination.exists() or destination.is_symlink():
        raise ValueError("Refusing to overwrite comparison evidence")
    enforce_local_output_path(destination.absolute())
    # Exclusive, no-follow creation prevents a late symlink swap at the output leaf.
    import os
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(destination, flags, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", closefd=False) as stream:
            json.dump(report, stream, indent=2, ensure_ascii=False, sort_keys=True)
    finally:
        os.close(fd)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--snapshots", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--replacement-workflow-root", type=Path)
    parser.add_argument("--verify-github-artifacts", action="store_true",
                        help="Read API origins and bounded ZIP bytes for supplied pairs")
    args = parser.parse_args()
    import os
    report = run(args.inventory, args.snapshots, args.output,
                 replacement_workflow_root=args.replacement_workflow_root,
                 verify_github_artifacts=args.verify_github_artifacts,
                 token=os.environ.get("GITHUB_TOKEN") if args.verify_github_artifacts else None)
    print(json.dumps({key: report[key] for key in
                      ("total", "pairs_supplied", "snapshot_matches",
                       "snapshot_mismatches", "missing_pairs", "behavioral_parity_accepted")}))
    return 0 if report["snapshot_mismatches"] == 0 and report["missing_pairs"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
