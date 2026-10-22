"""CLI for hashing real execution outputs into a bounded parity snapshot."""
import argparse
import json
from pathlib import Path

from madsc.parity_snapshot_writer import write_execution_snapshot


def _observations(values):
    result = []
    for value in values:
        if not isinstance(value, str) or "=" not in value:
            raise ValueError("Observation must use LABEL=PATH")
        label, path = value.split("=", 1)
        if not label or not path:
            raise ValueError("Observation must use non-empty LABEL=PATH")
        result.append((label, Path(path)))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--exit-code", required=True, type=int)
    parser.add_argument("--timed-out", action="store_true")
    parser.add_argument("--output", action="append", required=True,
                        help="Observed output as LABEL=PATH")
    parser.add_argument("--side-effect", action="append", default=[],
                        help="Observed side effect as LABEL=PATH")
    parser.add_argument("--output-root", default=".")
    args = parser.parse_args(argv)
    result = write_execution_snapshot(
        Path(args.output_root).absolute(), exit_code=args.exit_code,
        timed_out=args.timed_out, outputs=_observations(args.output),
        side_effects=_observations(args.side_effect))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
