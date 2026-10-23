"""Pure K5 archive classification preview; never opens or writes a playlist.

The positions here reproduce the frozen legacy *classification intent*, not
proof of channel identity, playback, or full behavioral parity.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

@dataclass(frozen=True)
class ArchivePreview:
    scenario: str
    input_count: int
    kept_positions: tuple[int, ...]
    archived_positions: tuple[int, ...]
    user_reported_unverified_positions: tuple[int, ...]
    user_classified_foreign_positions: tuple[int, ...]

_RULES = {
    "354": (354, ((1, 2),), ((3, 334), (335, 354))),
    "364": (364, ((1, 354),), ((355, 364),)),
    "398": (398, ((1, 15), (50, 398)), ((16, 49),)),
}

def _expand(ranges: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    return tuple(i for first, last in ranges for i in range(first, last + 1))

def classify_archive_positions(scenario: str, entries: Sequence[object]) -> ArchivePreview:
    """Return 1-based position partitions without mutating input or filesystem.

    The caller must parse/validate M3U before invoking this planner. A matching
    entry count alone is never sufficient to authorize playlist changes.
    """
    if not isinstance(scenario, str) or scenario not in _RULES:
        raise ValueError("Unknown archive scenario")
    if isinstance(entries, (str, bytes, bytearray)) or not isinstance(entries, Sequence):
        raise TypeError("Entries must be a sequence of parsed channels")
    count, kept_ranges, archive_ranges = _RULES[scenario]
    if len(entries) != count:
        raise ValueError(f"Expected {count} channels for archive scenario {scenario}")
    kept = _expand(kept_ranges)
    archived = _expand(archive_ranges)
    if tuple(sorted(kept + archived)) != tuple(range(1, count + 1)):
        raise AssertionError("Archive partition does not cover source exactly once")
    return ArchivePreview(
        scenario=scenario,
        input_count=count,
        kept_positions=kept,
        archived_positions=archived,
        user_reported_unverified_positions=tuple(range(3, 335)) if scenario == "354" else (),
        user_classified_foreign_positions=(
            tuple(range(335, 355)) if scenario == "354" else archived
        ),
    )
