"""Verify K2 artifact against an independently supplied trusted SHA-256."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from madsc.k2_daily_evidence import verify_daily_evidence


def verify_file(path: str, trusted_sha256: str) -> bool:
    if len(trusted_sha256) != 64 or any(c not in "0123456789abcdef" for c in trusted_sha256):
        return False
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != trusted_sha256:
        return False
    try:
        return verify_daily_evidence(json.loads(raw))
    except (ValueError, UnicodeError, TypeError):
        return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact")
    parser.add_argument("--trusted-sha256", required=True,
                        help="Expected digest from a separate trusted channel")
    args = parser.parse_args()
    if not verify_file(args.artifact, args.trusted_sha256):
        raise SystemExit("K2 artifact verification FAILED")
    print("K2 artifact bytes and internal hashes verified; origin attestation NOT verified")


if __name__ == "__main__":
    main()
