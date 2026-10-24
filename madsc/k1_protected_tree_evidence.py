"""K1 read-only tracked protected-file integrity evidence.

Capture SHA-256 before/after an isolated guard probe. This does not certify
production runtime enforcement or prove files cannot change later.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from madsc.write_path_audit import audit_write_paths


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    tracked = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, check=True, capture_output=True
    ).stdout
    paths = [p.decode("utf-8", "surrogateescape") for p in tracked.split(b"\\0") if p]
    protected = [p for p in paths if audit_write_paths([p])["blocked"]]
    def snapshot():
        evidence = {}
        for relative in protected:
            target = root / relative
            if target.is_symlink() or not target.is_file():
                raise RuntimeError("Protected tracked path is not a regular file")
            evidence[relative] = hashlib.sha256(target.read_bytes()).hexdigest()
        return evidence
    before = snapshot()
    # Read-only policy evaluation across every protected tracked path.
    for relative in protected:
        assert audit_write_paths([relative])["blocked"]
    after = snapshot()
    passed = before == after
    report = {
        "schema": "k1-readonly-protected-tree-v1",
        "scope": "git-tracked files in this checkout only",
        "protected_tracked_count": len(protected),
        "sha256_before": before,
        "sha256_after": after,
        "unchanged": passed,
        "production_runtime_accepted": False,
        "runtime_security_26_acceptance": 0,
        "production_writes": False,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
