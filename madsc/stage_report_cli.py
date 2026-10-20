"""K3/K5 isolated evidence CLI; never probes live streams or writes production."""
import argparse
import json
from pathlib import Path

from madsc.batch_acceptance import _unique_json_pairs
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("k3", "k5"), required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--isolated-report-root", type=Path, required=True)
    args = parser.parse_args()
    if args.input.is_symlink() or not args.input.is_file() or args.input.stat().st_size > 1024 * 1024:
        raise ValueError("Invalid input evidence")
    payload = json.loads(args.input.read_text(encoding="utf-8"),
                         object_pairs_hook=_unique_json_pairs)
    report = build_report(args.stage, payload)
    print(json.dumps(write_stage_report(args.isolated_report_root, args.stage, report),
                     sort_keys=True))


if __name__ == "__main__":
    main()
