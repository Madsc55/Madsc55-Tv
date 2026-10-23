"""Independent, offline K5 archive preview verification; no production writes."""
from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence

from madsc.isolated_ibo_archive_preview import build_6115_archive_preview


def verify_6115_archive_preview(urls: Sequence[str], manifest: Mapping) -> dict:
    """Recompute expected preview independently of stored manifest assertions.

    This checks positional partition and source-order integrity. It does not
    prove stream playback, country, logo provenance, or device acceptance.
    """
    if not isinstance(manifest, dict):
        raise ValueError("Manifest must be a JSON object")
    expected = build_6115_archive_preview(urls)
    if set(manifest) != set(expected):
        raise ValueError("Manifest fields differ")
    for key, value in expected.items():
        actual = manifest[key]
        if type(actual) is not type(value) or actual != value:
            raise ValueError("Manifest mismatch: " + key)
    archived = manifest["archived_original_positions"]
    retained = manifest["retained_original_positions"]
    if (len(archived) + len(retained) != 6115
            or set(archived).intersection(retained)
            or set(archived).union(retained) != set(range(1, 6116))):
        raise ValueError("Incomplete positional partition")
    canonical = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "verified": True,
        "source_order_sha256": expected["source_order_sha256"],
        "manifest_sha256": hashlib.sha256(canonical).hexdigest(),
        "position_count": 6115,
        "source_identity_verified": False,
        "playback_verified": False,
        "logo_history_verified": False,
        "device_verified": False,
    }
