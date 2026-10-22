"""Read-only K1-K5 evidence inventory; no acceptance inflation or live writes."""
from __future__ import annotations
import argparse
import json
import os
import stat
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


def _read_regular_report(path: Path) -> bytes:
    """Read one bounded single-link report and reject in-read replacement."""
    if not hasattr(os, "O_NOFOLLOW") or path.is_symlink():
        raise ValueError("Unsafe evidence report")
    flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_NONBLOCK", 0)
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1
                or before.st_size > MAX_REPORT_BYTES):
            raise ValueError("Unsafe evidence report")
        chunks = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(65536, MAX_REPORT_BYTES + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > MAX_REPORT_BYTES:
                raise ValueError("Oversized evidence report")
        after = os.fstat(descriptor)
        current = path.lstat()
        version = lambda info: (info.st_dev, info.st_ino, info.st_size,
                                info.st_mtime_ns, info.st_ctime_ns, info.st_nlink)
        if version(before) != version(after) or version(after) != version(current):
            raise ValueError("Evidence report changed during read")
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def audit(root: Path) -> dict:
    root = Path(root).absolute()
    reports = root / "reports"
    stages = {}
    for stage in STAGES:
        evidence = []
        for filename in REQUIRED[stage]:
            path = reports / filename
            record = {"name": filename, "present": False, "valid_json": False}
            if not reports.is_symlink() and not path.is_symlink():
                try:
                    payload = json.loads(_read_regular_report(path).decode("utf-8"))
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
