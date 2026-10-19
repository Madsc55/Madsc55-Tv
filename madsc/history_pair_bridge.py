"""Read-only compatibility bridge between legacy two-file history and one envelope.

Only explicitly designated isolated artifact paths are accepted by callers.
"""
from pathlib import Path

from madsc.history_pair_store import KEYS, atomic_write_pair, decode_pair, encode_pair
from madsc.legacy_history_merge import merge_pair

import json


def import_legacy_pair(folder):
    root = Path(folder)
    result = {}
    for name in KEYS:
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise ValueError("Missing or symlinked legacy history: " + name)
        result[name] = json.loads(path.read_text(encoding="utf-8"))
    # Validate both schemas without mutating legacy input.
    encode_pair(result)
    return result


def bridge_legacy_pair(folder, envelope_path):
    original = import_legacy_pair(folder)
    atomic_write_pair(envelope_path, original)
    return decode_pair(Path(envelope_path).read_text(encoding="utf-8"))


def merge_into_envelope(envelope_path, incoming_pair):
    path = Path(envelope_path)
    if path.is_symlink() or not path.is_file():
        raise ValueError("History envelope missing or symlinked")
    current = decode_pair(path.read_text(encoding="utf-8"))
    # Validate the complete incoming pair before any replacement.
    encode_pair(incoming_pair)
    merged, changes = merge_pair(current, incoming_pair)
    atomic_write_pair(path, merged)
    return changes
