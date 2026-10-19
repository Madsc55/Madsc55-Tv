"""Legacy candidate score contract, pure and read-only.

This preserves the old technical scoring semantics separately from the new
coordination score. It does not certify stream identity or playback.
"""
from __future__ import annotations
import re


def legacy_technical_score(technical: str = "", audio: str = "",
                           resolution: str = "", logo_url: str = "") -> dict:
    if any(not isinstance(v, str) for v in (technical, audio, resolution, logo_url)):
        raise ValueError("Invalid legacy scoring evidence")
    video = technical in ("VIDEO_SES_VAR", "YALNIZ_VIDEO")
    sound = technical == "VIDEO_SES_VAR" or (video and audio.lower() == "true")
    points = (20 if video else 0) + (15 if sound else 0)
    if resolution:
        match = re.search(r"(\d+)x(\d+)", resolution)
        if match:
            height = int(match.group(2))
            points += 10 if height >= 1080 else 7 if height >= 720 else 3
    if logo_url.startswith("https://"):
        points += 5
    return {"score": points,
            "status": "TEKNIK_ADAY" if video and sound else "EK_DOGRULAMA_GEREKLI",
            "identity_verified": False, "ibo_device_verified": False,
            "production_change_allowed": False, "legacy_scoring_contract_only": True}
