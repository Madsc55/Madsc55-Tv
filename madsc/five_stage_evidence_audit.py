"""Read-only K1-K5 evidence inventory; no acceptance inflation or live writes."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

STAGES = ("K1", "K2", "K3", "K4", "K5")
REQUIRED = {
    "K1": ("k1-isolated-evidence.json",),
    "K2": ("k2-live-pilot.json",),
    "K3": ("k3-real-manifest-pilot.json",),
    "K4": ("k4-isolated-evidence.json",),
    "K5": ("k5-isolated-evidence.json",),
}
MAX_REPORT_BYTES = 2_000_000


def audit(root: Path) -> dict:
    root = Path(root).absolute()
    reports = root / "reports"
    stages = {}
    for stage in STAGES:
        evidence = []
        for filename in REQUIRED[stage]:
            path = reports / filename
            record = {"name": filename, "present": False, "valid_json": False}
            if not reports.is_symlink() and not path.is_symlink() and path.is_file():
                if path.stat().st_size <= MAX_REPORT_BYTES:
                    try:
                        with path.open("r", encoding="utf-8") as handle:
                            payload = json.load(handle)
                        if isinstance(payload, dict):
                            record["present"] = True
                            record["valid_json"] = True
                    except (OSError, ValueError, UnicodeError):
                        pass
            evidence.append(record)
        stages[stage] = {
            "reports": evidence,
            "evidence_files_valid": all(x["valid_json"] for x in evidence),
            "runtime_verified": False,
            "production_accepted": False,
        }
    return {"stages": stages, "stage_count": 5,
            "evidence_inventory_only": True,
            "legacy_behavior_accepted": 0,
            "production_ready": False, "production_writes": False}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Read-only K1-K5 evidence audit")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    print(json.dumps(audit(args.root), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
