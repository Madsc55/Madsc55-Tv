"""Read-only presentation of discovered channels in the legacy category order."""
from __future__ import annotations

QUALITY = ((3840, 2160, "4K"), (2560, 1440, "QHD"),
           (1920, 1080, "FHD"), (1280, 720, "HD"))


def quality_label(width, height):
    if type(width) is not int or type(height) is not int or width <= 0 or height <= 0:
        return None
    for minimum_width, minimum_height, label in QUALITY:
        if width >= minimum_width and height >= minimum_height:
            return label
    return "SD"


def present_channel(row: dict, *, measurement: dict | None = None,
                    logo_evidence: dict | None = None,
                    ibo_result: str = "UNKNOWN") -> dict:
    """Never infer verified metadata from names or untrusted logo URLs."""
    if not isinstance(row, dict) or not isinstance(row.get("name"), str) or not row["name"].strip():
        raise ValueError("Missing channel name")
    if ibo_result not in ("UNKNOWN", "WORKING", "NOT_WORKING"):
        raise ValueError("Invalid IBO status")
    measurement = measurement or {}
    logo_evidence = logo_evidence or {}
    if not isinstance(measurement, dict) or not isinstance(logo_evidence, dict):
        raise ValueError("Invalid evidence")
    measured = measurement.get("verified") is True
    quality = quality_label(measurement.get("width"), measurement.get("height")) if measured else None
    # Turkish dotted/dotless i needs explicit handling independent of host locale.
    name = row["name"].strip().translate(str.maketrans({"i": "İ", "ı": "I"})).upper()
    if quality and not name.endswith(" " + quality):
        name += " " + quality
    logo = logo_evidence.get("url") if (
        logo_evidence.get("identity_match") is True
        and logo_evidence.get("reachable") is True
        and isinstance(logo_evidence.get("url"), str)
        and logo_evidence["url"].startswith("https://")) else None
    technical = measurement.get("technical_status", "UNTESTED")
    if ibo_result == "WORKING":
        bucket = "IBO_ONAYLI_CALISAN"
    elif row.get("foreign") is True:
        bucket = "YABANCI"
    elif technical == "PRELIMINARY_PASS":
        bucket = "CALISAN_ADAY"
    elif technical == "NEEDS_REVIEW":
        bucket = "CALISMAYAN_ADAY"
    else:
        bucket = "TEST_BEKLIYOR"
    return {"display_name": name, "quality": quality,
            "resolution": [measurement["width"], measurement["height"]] if quality else None,
            "logo_url": logo, "logo_verified": logo is not None,
            "group_title": row.get("group_title", ""),
            "tvg_id": row.get("tvg_id", ""),
            "bucket": bucket, "ibo_result": ibo_result,
            "preserve_existing": ibo_result == "WORKING",
            "production_writes": False, "production_change_allowed": False}
