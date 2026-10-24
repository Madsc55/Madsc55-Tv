"""Read-only, fail-closed EPG matching for isolated trial playlists."""
import re
import unicodedata
from datetime import datetime
import xml.etree.ElementTree as ET

ATTR = re.compile(r'(?:^|\s)([A-Za-z][\w-]*)="([^"]*)"(?=\s|$)')

def norm(value):
    value = (value or "").casefold().translate({ord("ı"): "i"})
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = value.translate({ord("ı"): "i"})
    return re.sub(r"[^a-z0-9]+", "", value)

def xmltv_channels(xml_data):
    raw = xml_data.encode("utf-8") if isinstance(xml_data, str) else xml_data
    if b"\x00" in raw:
        raise ValueError("NUL byte in XMLTV")
    if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise ValueError("XMLTV DTD/entity declarations are not allowed")
    root = ET.fromstring(raw)
    if root.tag != "tv":
        raise ValueError("XMLTV root element must be <tv>")
    result = {}
    for channel in root.findall("channel"):
        key = channel.get("id", "").strip()
        if not key:
            raise ValueError("XMLTV channel is missing a nonempty id")
        if key in result:
            raise ValueError("Duplicate XMLTV channel id")
        result[key] = [n.text or "" for n in channel.findall("display-name")]
    return result

def playlist_entries(playlist):
    entries = []
    for line in playlist.splitlines():
        if not line.startswith("#EXTINF:"):
            continue
        quoted = False
        separator = None
        for i, char in enumerate(line):
            if char == '"':
                quoted = not quoted
            elif char == "," and not quoted:
                separator = i
                break
        if quoted or separator is None or not line[separator + 1:].strip():
            raise ValueError("Malformed EXTINF channel name separator")
        attributes = line[:separator]
        if attributes.count('"') % 2:
            raise ValueError("Malformed EXTINF attributes")
        found = [m.group(2) for m in ATTR.finditer(attributes)
                 if m.group(1) == "tvg-id" and attributes[:m.start(1)].count('"') % 2 == 0]
        declared = [m for m in re.finditer(r'(?:^|\s)tvg-id(?=\s|=)', attributes)
                    if attributes[:m.start()].count('"') % 2 == 0]
        if len(declared) != len(found):
            raise ValueError("Malformed tvg-id attribute")
        if len(found) > 1:
            raise ValueError("Duplicate tvg-id attribute")
        entries.append((line[separator + 1:].strip(), found[0].strip() if found else ""))
    return entries

def matches(playlist, xml_data):
    channels = xmltv_channels(xml_data)
    names = {}
    for key, variants in channels.items():
        for name in [key, *variants]:
            normalized = norm(name)
            if normalized:
                names.setdefault(normalized, set()).add(key)
    output = []
    for title, old_id in playlist_entries(playlist):
        keys = sorted(names.get(norm(title), set()))
        if old_id in channels:
            status, matched = "existing_valid", old_id
        elif len(keys) == 1:
            status, matched = "exact_unique", keys[0]
        elif len(keys) > 1:
            status, matched = "ambiguous", ""
        else:
            status, matched = "unmatched", ""
        output.append({"title": title, "old_id": old_id, "matched_id": matched, "status": status})
    return output


def _valid_xmltv_time(value):
    """Accept XMLTV timestamps only when calendar date and UTC offset are valid."""
    if not re.fullmatch(r"\d{12}(?:\d{2})? [+-]\d{4}", value):
        return False
    fmt = "%Y%m%d%H%M%S %z" if len(value.split(" ")[0]) == 14 else "%Y%m%d%H%M %z"
    try:
        parsed = datetime.strptime(value, fmt)
        if parsed.utcoffset() is None or abs(parsed.utcoffset().total_seconds()) > 14 * 3600:
            return False
    except ValueError:
        return False
    return True

def programme_coverage(playlist, xml_data, reference_time=None):
    """Read-only counts; optional aware reference_time measures current guide coverage."""
    if reference_time is not None and (reference_time.tzinfo is None or reference_time.utcoffset() is None):
        raise ValueError("reference_time must be timezone-aware")
    raw = xml_data.encode("utf-8") if isinstance(xml_data, str) else xml_data
    if b"\x00" in raw:
        raise ValueError("NUL byte in XMLTV")
    if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise ValueError("XMLTV DTD/entity declarations are not allowed")
    root = ET.fromstring(raw)
    if root.tag != "tv":
        raise ValueError("XMLTV root element must be <tv>")
    results = matches(playlist, raw)
    known_channels = xmltv_channels(raw)
    counts = {}
    current_counts = {}
    for programme in root.findall("programme"):
        channel = (programme.get("channel") or "").strip()
        start = (programme.get("start") or "").strip()
        stop = (programme.get("stop") or "").strip()
        if channel in known_channels and _valid_xmltv_time(start) and (not stop or _valid_xmltv_time(stop)):
            start_dt = datetime.strptime(start, "%Y%m%d%H%M%S %z" if len(start.split(" ")[0]) == 14 else "%Y%m%d%H%M %z")
            if stop:
                stop_dt = datetime.strptime(stop, "%Y%m%d%H%M%S %z" if len(stop.split(" ")[0]) == 14 else "%Y%m%d%H%M %z")
                if stop_dt <= start_dt:
                    continue
            counts[channel] = counts.get(channel, 0) + 1
            if reference_time is not None:
                if stop and start_dt <= reference_time < stop_dt:
                    current_counts[channel] = current_counts.get(channel, 0) + 1
    for row in results:
        channel = row["matched_id"]
        row["programme_count"] = counts.get(channel, 0) if channel else 0
        row["has_programmes"] = row["programme_count"] > 0
        if reference_time is not None:
            row["current_programme_count"] = current_counts.get(channel, 0) if channel else 0
            row["has_current_programmes"] = row["current_programme_count"] > 0
    return results


def coverage_summary(rows):
    """Aggregate read-only K3 acceptance metrics from programme_coverage rows."""
    rows = list(rows)
    statuses = ("existing_valid", "exact_unique", "ambiguous", "unmatched")
    summary = {"total_channels": len(rows)}
    summary["empty_tvg_id"] = sum(not (row.get("old_id") or "").strip() for row in rows)
    summary["unresolved_tvg_id"] = sum(not row.get("matched_id") for row in rows)
    summary["resolved_tvg_id"] = len(rows) - summary["unresolved_tvg_id"]
    for status in statuses:
        summary[status] = sum(row["status"] == status for row in rows)
    summary["with_programmes"] = sum(bool(row["has_programmes"]) for row in rows)
    summary["without_programmes"] = len(rows) - summary["with_programmes"]
    if any("has_current_programmes" in row for row in rows) and not all("has_current_programmes" in row for row in rows):
        raise ValueError("Mixed current-guide coverage rows are not comparable")
    if rows and all("has_current_programmes" in row for row in rows):
        summary["with_current_programmes"] = sum(bool(row["has_current_programmes"]) for row in rows)
        summary["without_current_programmes"] = len(rows) - summary["with_current_programmes"]
    return summary
