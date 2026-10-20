"""Multi-source Turkish TV discovery based on read-only legacy source inventory."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

SOURCES = {
    "iptv-org-TR": "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u",
    "iptv-org-TURKIYE": "https://iptv-org.github.io/iptv/countries/tr.m3u",
    "iptv-org-TURKCE": "https://iptv-org.github.io/iptv/languages/tur.m3u",
    "iptv-turk-tr": "https://raw.githubusercontent.com/iptv-turk-tr/iptv/main/list.m3u",
    "omerdenizhan-TR": "https://raw.githubusercontent.com/omerdenizhan/IPTV-M3U/main/m3u/turkiye.m3u",
    "ilyswch-TR": "https://raw.githubusercontent.com/ilyswch/turk-iptv/main/index.m3u",
    "itasli-TR": "https://itasli.github.io/TURKTV/index.m3u",
    "gkhncksn-TR": "https://raw.githubusercontent.com/gkhncksn/m3u8_lists/main/TURK_KANALLARI.m3u",
    "Lunedor-TR": "https://raw.githubusercontent.com/Lunedor/iptvTR/main/iptv_tum_kanallar.m3u",
    "dearbulut-TR": "https://dearbulut.github.io/iptv/playlists/country/tr.m3u",
    "dearbulut-TURKCE": "https://dearbulut.github.io/iptv/playlists/language/tur.m3u",
}
RADIO = ("radyo", "radio", "fm radio", "radio fm")


def scan(item):
    name, url = item
    try:
        request = Request(url, headers={"User-Agent": "Madsc55-Tv-multi-source-discovery/1.0"})
        with urlopen(request, timeout=18) as response:
            if response.geturl() != url:
                raise ValueError("redirect_not_allowed")
            data = response.read(2_000_001)
        if len(data) > 2_000_000 or not data.decode("utf-8-sig", errors="replace").lstrip().startswith("#EXTM3U"):
            raise ValueError("invalid_m3u_or_size")
        entries = []
        title = None
        for line in data.decode("utf-8-sig", errors="replace").splitlines():
            line = line.strip()
            if line.startswith("#EXTINF:"):
                title = line.split(",", 1)[-1].strip() if "," in line else None
            elif line and not line.startswith("#"):
                if title and line.startswith(("https://", "http://")):
                    entries.append((title, line))
                title = None
        return name, entries, None
    except Exception as exc:
        return name, [], type(exc).__name__


def run():
    seen = set()
    summary = []
    total = 0
    radio = 0
    duplicates = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for name, entries, error in pool.map(scan, SOURCES.items()):
            accepted = 0
            for title, url in entries:
                total += 1
                if any(word in title.casefold() for word in RADIO):
                    radio += 1
                    continue
                digest = hashlib.sha256(url.encode()).hexdigest()
                if digest in seen:
                    duplicates += 1
                    continue
                seen.add(digest)
                accepted += 1
            summary.append({"source": name, "status": "error" if error else "ok",
                            "error_type": error, "entries": len(entries), "unique_nonradio_candidates": accepted})
    report = {"stage": "LEGACY_MULTI_SOURCE_TURKISH_TV_DISCOVERY",
              "sources_checked": len(SOURCES), "sources_ok": sum(x["status"] == "ok" for x in summary),
              "entries": total, "radio_name_excluded": radio, "duplicate_urls": duplicates,
              "unique_nonradio_candidates": len(seen), "video_verified": 0,
              "turkish_audio_verified": 0, "playlist_modified": False,
              "note": "Candidate discovery only; feed membership does not prove Turkish language or playback.",
              "sources": summary}
    out = Path("reports/k2-legacy-multisource.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "sources"}, ensure_ascii=False))


if __name__ == "__main__":
    run()
