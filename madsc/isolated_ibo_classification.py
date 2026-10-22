"""K5: pure, offline IBO positional classification without production writes.

Legacy 6115-entry rules are modeled as a preview, never a playlist mutation.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IboClassification:
    original_position: int
    action: str
    country: str
    playback: str = "BELIRTILMEDI"


def classify_6115_positions(total: int = 6115) -> tuple[IboClassification, ...]:
    """Return all original 1-based positions, with no I/O or source mutation.

    Classification is user-reported, not a channel identity/playback assertion.
    Refuse unexpected input sizes instead of silently shifting positions.
    """
    if type(total) is not int or total != 6115:
        raise ValueError("IBO positional preview requires exactly 6115 backup entries")
    turkish = (
        set(range(3, 11)) | set(range(14, 19))
        | {782, 3504, 3505, 3920, 4310, 4311, 5935}
        | set(range(3555, 3905)) | set(range(4987, 4997))
    )
    turkish.discard(3564)
    reviewed = set(range(3, 5967))
    return tuple(
        IboClassification(
            original_position=position,
            action="KALDI" if position not in reviewed or position in turkish else "ARSIV_ONIZLEME",
            country=("TURK_KULLANICI_BILDIRIMI" if position in turkish
                     else "YABANCI_KULLANICI_BILDIRIMI" if position in reviewed
                     else "INCELENMEDI"),
        )
        for position in range(1, total + 1)
    )
