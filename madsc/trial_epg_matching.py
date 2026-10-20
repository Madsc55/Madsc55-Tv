"""Read-only XMLTV/M3U identity matching for trial playlists.

Never modifies production playlists, EPG or logos.
"""
import re
import xml.etree.ElementTree as ET

def norm(value):
    value = (value or "").casefold().replace("ı", "i")
    return re.sub(r"[^a-z0-9]+", "", value)

def xmltv_channels(xml_data):
    root = ET.fromstring(xml_data)
    result = {}
    for channel in root.findall("channel"):
        key = channel.get("id", "")
        names = [n.text or "" for n in channel.findall("display-name")]
        if key:
            result[key] = names
    return result

def playlist_entries(playlist):
    entries = []
    for line in playlist.splitlines():
        if not line.startswith("#EXTINF:"):
            continue
        title = line.split(",", 1)[-1].strip()
        match = re.search(r'\btvg-id="([^"]*)"', line)
        entries.append((title, match.group(1) if match else ""))
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
