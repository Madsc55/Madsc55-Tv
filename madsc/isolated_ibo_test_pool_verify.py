"""K5 independent read-only verification of isolated test-pool manifests."""
import hashlib
import json
from collections.abc import Mapping

from madsc.isolated_ibo_test_pool import build_isolated_test_pool


def verify_isolated_test_pool(records, pool):
    """Rebuild the pool from source metadata and reject any modified output."""
    if not isinstance(pool, Mapping) or type(pool) is not dict:
        raise ValueError("Invalid test-pool manifest")
    expected = build_isolated_test_pool(records)
    if set(pool) != set(expected):
        raise ValueError("Test-pool manifest fields differ")
    for key, value in expected.items():
        actual = pool[key]
        if type(actual) is not type(value) or actual != value:
            raise ValueError("Test-pool mismatch: " + key)
    encoded = json.dumps(pool["entries"], ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    if hashlib.sha256(encoded).hexdigest() != pool["entries_sha256"]:
        raise ValueError("Test-pool digest mismatch")
    return {
        "verified": True,
        "entry_count": 6115,
        "entries_sha256": pool["entries_sha256"],
        "source_identity_verified": False,
        "playback_verified": False,
        "device_verified": False,
        "production_writes": False,
    }
