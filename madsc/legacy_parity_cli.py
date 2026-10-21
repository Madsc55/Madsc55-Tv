"""Read-only CLI for batch legacy/replacement execution snapshot comparison."""
import argparse
import json
from pathlib import Path
from madsc.legacy_parity_evidence import compare_snapshot_batch


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


def run(inventory_path, snapshots_path, output_path):
    inventory = load_json(inventory_path)
    snapshots = load_json(snapshots_path)
    report = compare_snapshot_batch(inventory, snapshots)
    destination = Path(output_path)
    if destination.exists() or destination.is_symlink():
        raise ValueError("Refusing to overwrite comparison evidence")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, ensure_ascii=False, sort_keys=True)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--snapshots", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = run(args.inventory, args.snapshots, args.output)
    print(json.dumps({key: report[key] for key in
                      ("total", "pairs_supplied", "snapshot_matches",
                       "snapshot_mismatches", "missing_pairs", "behavioral_parity_accepted")}))
    return 0 if report["snapshot_mismatches"] == 0 and report["missing_pairs"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
