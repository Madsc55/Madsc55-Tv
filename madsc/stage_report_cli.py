"""K3/K5 isolated evidence CLI; never probes live streams or writes production."""
import argparse
import json
from pathlib import Path

from madsc.batch_acceptance import _unique_json_pairs, CATEGORIES, MODULES, collect
from madsc.channel_test import summarize_offline_probe_evidence
from madsc.maintenance import summarize_batch
from madsc.fixture_report_writer import write_stage_report


def build_report(stage, payload):
    if stage == "k3":
        result = summarize_offline_probe_evidence(payload)
    elif stage == "k5":
        result = summarize_batch(payload)
    else:
        raise ValueError("Only K3 and K5 are supported")
    return {"category": stage, "production_writes": False,
            "production_ready": False, "evidence": result}


def load_batch_reports(root: Path) -> list[dict]:
    """Validate the complete artifact package with the same K5 acceptance gate."""
    root = Path(root)
    collect(root)
    reports = []
    for stage in CATEGORIES:
        path = root / f"madsc-batch-{stage}" / f"{stage}.json"
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_json_pairs)
        reports.append({"category": stage, "status": "success",
                        "production_writes": False,
                        "fixture_checks": data["fixture_checks"]})
    return reports

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("k3", "k5"), required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path)
    source.add_argument("--batch-evidence-root", type=Path)
    parser.add_argument("--isolated-report-root", type=Path, required=True)
    args = parser.parse_args()
    if args.batch_evidence_root is not None:
        if args.stage != "k5":
            raise ValueError("Batch evidence is only supported for K5")
        payload = load_batch_reports(args.batch_evidence_root)
    else:
        if args.input.is_symlink() or not args.input.is_file() or args.input.stat().st_size > 1024 * 1024:
            raise ValueError("Invalid input evidence")
        payload = json.loads(args.input.read_text(encoding="utf-8"),
                             object_pairs_hook=_unique_json_pairs)
    report = build_report(args.stage, payload)
    print(json.dumps(write_stage_report(args.isolated_report_root, args.stage, report),
                     sort_keys=True))


if __name__ == "__main__":
    main()
