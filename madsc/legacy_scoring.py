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


def legacy_approval_decision(base_score: int, technical: str,
                             stable_24h: bool) -> dict:
    """Preserve legacy unified-report decision; never approve playlist writes."""
    if type(base_score) is not int or base_score < 0 or type(technical) is not str or type(stable_24h) is not bool:
        raise ValueError("Invalid legacy approval evidence")
    score = min(100, base_score + (30 if stable_24h else 0))
    if stable_24h and technical == "VIDEO_SES_VAR":
        status = "IBO_VE_KIMLIK_ONAYI_BEKLIYOR"
    elif technical == "VIDEO_SES_VAR":
        status = "KARARLILIK_BEKLIYOR"
    else:
        status = "TEKNIK_DOGRULAMA_BEKLIYOR"
    return {"score": score, "status": status, "ibo_approval": "YOK",
            "user_approval": "YOK", "add_to_main_playlist": "HAYIR",
            "production_change_allowed": False, "stability_evidence_supplied_only": True}
