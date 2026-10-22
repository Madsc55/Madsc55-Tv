"""Read-only legacy XMLTV pilot and candidate logo evidence comparison."""
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET


def join_pilot(candidates: list[dict], logos: list[dict], xmltv: Path) -> dict:
    if (not isinstance(candidates, list) or not isinstance(logos, list)
            or len(candidates) > 20000 or len(logos) > 20000
            or any(not isinstance(item, dict) for item in candidates + logos)):
        raise ValueError("Invalid EPG/logo evidence")
    xmltv = Path(xmltv)
    if xmltv.is_symlink() or not xmltv.is_file() or xmltv.stat().st_size > 16_000_000:
        raise ValueError("Invalid XMLTV source")
    root = ET.parse(xmltv).getroot()
    if root.tag != "tv":
        raise ValueError("Invalid XMLTV")
    if len(root) > 200000:
        raise ValueError("Oversized XMLTV document")
    channels = {node.get("id") for node in root.findall("channel")}
    counts = Counter(node.get("channel") for node in root.findall("programme"))
    by_digest = {item.get("stream_sha256"): item for item in logos
                 if item.get("stream_sha256")}
    results = []
    for item in candidates:
        channel_id = item.get("channel_id", "").strip()
        digest = item.get("stream_sha256", "")
        logo = by_digest.get(digest, {})
        epg_status = ("PILOT_MATCH_WITH_PROGRAMMES" if channel_id in channels and counts[channel_id]
                      else "PILOT_ID_NO_PROGRAMMES" if channel_id in channels
                      else "NOT_IN_FIVE_CHANNEL_PILOT")
        results.append({"channel": item.get("channel", ""),
                        "stream_sha256": digest, "channel_id": channel_id,
                        "epg_pilot_status": epg_status,
                        "logo_status": logo.get("status", "NOT_PREPARED"),
                        "logo_visual_match": logo.get("visual_match", "NOT_VERIFIED"),
                        "broadcast_status": "SEE_EXISTING_DISCOVERY_AND_CONTINUITY_REPORTS",
                        "sweden_ibo_status": "NOT_DEVICE_VERIFIED",
                        "playlist_approved": False, "ready_for_playlist": False})
    return {"source_candidates": len(candidates), "candidate_results": results,
            "pilot_epg_channels": len(channels), "production_writes": False,
            "ibo_device_verified": False, "production_ready": False}
