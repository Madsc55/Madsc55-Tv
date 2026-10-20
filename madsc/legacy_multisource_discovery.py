"""Multi-source Turkish TV discovery based on read-only legacy source inventory."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

LEGACY_SOURCE_INVENTORY = {"iptv-turk-tr-EK-KAYNAK":"https://raw.githubusercontent.com/iptv-turk-tr/iptv/main/list.m3u","iptv-org-TR":"https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u","iptv-org-TURKIYE":"https://iptv-org.github.io/iptv/countries/tr.m3u","iptv-org-TURKCE":"https://iptv-org.github.io/iptv/languages/tur.m3u","iptv-org-AZERBAYCAN":"https://iptv-org.github.io/iptv/countries/az.m3u","omerdenizhan-TR":"https://raw.githubusercontent.com/omerdenizhan/IPTV-M3U/main/m3u/turkiye.m3u","ilyswch-TR":"https://raw.githubusercontent.com/ilyswch/turk-iptv/main/index.m3u","itasli-TR":"https://itasli.github.io/TURKTV/index.m3u","gkhncksn-TR":"https://raw.githubusercontent.com/gkhncksn/m3u8_lists/main/TURK_KANALLARI.m3u","Lunedor-TR":"https://raw.githubusercontent.com/Lunedor/iptvTR/main/iptv_tum_kanallar.m3u","dearbulut-TR":"https://dearbulut.github.io/iptv/playlists/country/tr.m3u","dearbulut-TURKCE":"https://dearbulut.github.io/iptv/playlists/language/tur.m3u","dearbulut-AZERBAYCAN":"https://dearbulut.github.io/iptv/playlists/country/az.m3u","dearbulut-KURTCE":"https://dearbulut.github.io/iptv/playlists/language/kur.m3u","dearbulut-AZERICE":"https://dearbulut.github.io/iptv/playlists/language/aze.m3u","dearbulut-TURKMENCE":"https://dearbulut.github.io/iptv/playlists/language/tuk.m3u","dearbulut-KIBRIS":"https://dearbulut.github.io/iptv/playlists/country/cy.m3u","dearbulut-TURKMENISTAN":"https://dearbulut.github.io/iptv/playlists/country/tm.m3u","dearbulut-ALMANYA":"https://dearbulut.github.io/iptv/playlists/country/de.m3u","dearbulut-ISVEC":"https://dearbulut.github.io/iptv/playlists/country/se.m3u","dearbulut-HOLLANDA":"https://dearbulut.github.io/iptv/playlists/country/nl.m3u","dearbulut-BELCIKA":"https://dearbulut.github.io/iptv/playlists/country/be.m3u","dearbulut-AVUSTURYA":"https://dearbulut.github.io/iptv/playlists/country/at.m3u","dearbulut-HABER":"https://dearbulut.github.io/iptv/playlists/category/news.m3u","dearbulut-SPOR":"https://dearbulut.github.io/iptv/playlists/category/sports.m3u","dearbulut-BELGESEL":"https://dearbulut.github.io/iptv/playlists/category/documentary.m3u","dearbulut-COCUK":"https://dearbulut.github.io/iptv/playlists/category/kids.m3u","dearbulut-MUZIK":"https://dearbulut.github.io/iptv/playlists/category/music.m3u","dearbulut-KULTUR":"https://dearbulut.github.io/iptv/playlists/category/culture.m3u","dearbulut-BILIM":"https://dearbulut.github.io/iptv/playlists/category/science.m3u","dearbulut-EGITIM":"https://dearbulut.github.io/iptv/playlists/category/education.m3u","dearbulut-ISVEC_DILI":"https://dearbulut.github.io/iptv/playlists/language/swe.m3u","dearbulut-ARAPCA":"https://dearbulut.github.io/iptv/playlists/language/ara.m3u","dearbulut-country-us":"https://dearbulut.github.io/iptv/playlists/country/us.m3u","dearbulut-country-in":"https://dearbulut.github.io/iptv/playlists/country/in.m3u","dearbulut-country-ru":"https://dearbulut.github.io/iptv/playlists/country/ru.m3u","dearbulut-country-br":"https://dearbulut.github.io/iptv/playlists/country/br.m3u","dearbulut-country-it":"https://dearbulut.github.io/iptv/playlists/country/it.m3u","dearbulut-country-es":"https://dearbulut.github.io/iptv/playlists/country/es.m3u","dearbulut-country-do":"https://dearbulut.github.io/iptv/playlists/country/do.m3u","dearbulut-country-cl":"https://dearbulut.github.io/iptv/playlists/country/cl.m3u","dearbulut-country-uk":"https://dearbulut.github.io/iptv/playlists/country/uk.m3u","dearbulut-country-fr":"https://dearbulut.github.io/iptv/playlists/country/fr.m3u","dearbulut-country-ua":"https://dearbulut.github.io/iptv/playlists/country/ua.m3u","dearbulut-country-ar":"https://dearbulut.github.io/iptv/playlists/country/ar.m3u","dearbulut-country-mx":"https://dearbulut.github.io/iptv/playlists/country/mx.m3u","dearbulut-country-pe":"https://dearbulut.github.io/iptv/playlists/country/pe.m3u","dearbulut-country-cn":"https://dearbulut.github.io/iptv/playlists/country/cn.m3u","dearbulut-country-ro":"https://dearbulut.github.io/iptv/playlists/country/ro.m3u","dearbulut-country-hu":"https://dearbulut.github.io/iptv/playlists/country/hu.m3u","dearbulut-country-ca":"https://dearbulut.github.io/iptv/playlists/country/ca.m3u","dearbulut-country-id":"https://dearbulut.github.io/iptv/playlists/country/id.m3u","dearbulut-country-pl":"https://dearbulut.github.io/iptv/playlists/country/pl.m3u","dearbulut-country-ir":"https://dearbulut.github.io/iptv/playlists/country/ir.m3u","dearbulut-country-co":"https://dearbulut.github.io/iptv/playlists/country/co.m3u","dearbulut-country-pk":"https://dearbulut.github.io/iptv/playlists/country/pk.m3u","dearbulut-country-ec":"https://dearbulut.github.io/iptv/playlists/country/ec.m3u","dearbulut-country-vn":"https://dearbulut.github.io/iptv/playlists/country/vn.m3u","dearbulut-country-hn":"https://dearbulut.github.io/iptv/playlists/country/hn.m3u","dearbulut-country-th":"https://dearbulut.github.io/iptv/playlists/country/th.m3u","dearbulut-country-kr":"https://dearbulut.github.io/iptv/playlists/country/kr.m3u","dearbulut-country-gr":"https://dearbulut.github.io/iptv/playlists/country/gr.m3u","dearbulut-country-ve":"https://dearbulut.github.io/iptv/playlists/country/ve.m3u","dearbulut-country-bo":"https://dearbulut.github.io/iptv/playlists/country/bo.m3u","dearbulut-country-cz":"https://dearbulut.github.io/iptv/playlists/country/cz.m3u","dearbulut-country-cr":"https://dearbulut.github.io/iptv/playlists/country/cr.m3u","dearbulut-country-gt":"https://dearbulut.github.io/iptv/playlists/country/gt.m3u","dearbulut-country-bg":"https://dearbulut.github.io/iptv/playlists/country/bg.m3u","dearbulut-country-py":"https://dearbulut.github.io/iptv/playlists/country/py.m3u","dearbulut-country-sk":"https://dearbulut.github.io/iptv/playlists/country/sk.m3u","dearbulut-country-pt":"https://dearbulut.github.io/iptv/playlists/country/pt.m3u","dearbulut-country-il":"https://dearbulut.github.io/iptv/playlists/country/il.m3u","dearbulut-country-sa":"https://dearbulut.github.io/iptv/playlists/country/sa.m3u","dearbulut-country-iq":"https://dearbulut.github.io/iptv/playlists/country/iq.m3u","dearbulut-country-ng":"https://dearbulut.github.io/iptv/playlists/country/ng.m3u","dearbulut-country-rs":"https://dearbulut.github.io/iptv/playlists/country/rs.m3u","dearbulut-country-kz":"https://dearbulut.github.io/iptv/playlists/country/kz.m3u","dearbulut-country-sv":"https://dearbulut.github.io/iptv/playlists/country/sv.m3u","dearbulut-country-au":"https://dearbulut.github.io/iptv/playlists/country/au.m3u","dearbulut-country-ke":"https://dearbulut.github.io/iptv/playlists/country/ke.m3u","dearbulut-country-ae":"https://dearbulut.github.io/iptv/playlists/country/ae.m3u","dearbulut-country-mn":"https://dearbulut.github.io/iptv/playlists/country/mn.m3u","dearbulut-country-uz":"https://dearbulut.github.io/iptv/playlists/country/uz.m3u","dearbulut-country-lb":"https://dearbulut.github.io/iptv/playlists/country/lb.m3u","dearbulut-country-ch":"https://dearbulut.github.io/iptv/playlists/country/ch.m3u","dearbulut-country-pr":"https://dearbulut.github.io/iptv/playlists/country/pr.m3u","dearbulut-country-bd":"https://dearbulut.github.io/iptv/playlists/country/bd.m3u","dearbulut-country-kh":"https://dearbulut.github.io/iptv/playlists/country/kh.m3u","dearbulut-country-tw":"https://dearbulut.github.io/iptv/playlists/country/tw.m3u","dearbulut-country-mk":"https://dearbulut.github.io/iptv/playlists/country/mk.m3u","dearbulut-country-sg":"https://dearbulut.github.io/iptv/playlists/country/sg.m3u","dearbulut-country-fi":"https://dearbulut.github.io/iptv/playlists/country/fi.m3u","dearbulut-country-za":"https://dearbulut.github.io/iptv/playlists/country/za.m3u","dearbulut-country-pa":"https://dearbulut.github.io/iptv/playlists/country/pa.m3u","dearbulut-country-hr":"https://dearbulut.github.io/iptv/playlists/country/hr.m3u","dearbulut-country-my":"https://dearbulut.github.io/iptv/playlists/country/my.m3u","dearbulut-country-md":"https://dearbulut.github.io/iptv/playlists/country/md.m3u","dearbulut-country-ge":"https://dearbulut.github.io/iptv/playlists/country/ge.m3u","dearbulut-country-ug":"https://dearbulut.github.io/iptv/playlists/country/ug.m3u","dearbulut-country-al":"https://dearbulut.github.io/iptv/playlists/country/al.m3u","dearbulut-country-hk":"https://dearbulut.github.io/iptv/playlists/country/hk.m3u","dearbulut-country-ee":"https://dearbulut.github.io/iptv/playlists/country/ee.m3u","dearbulut-country-ps":"https://dearbulut.github.io/iptv/playlists/country/ps.m3u","dearbulut-country-jo":"https://dearbulut.github.io/iptv/playlists/country/jo.m3u","dearbulut-country-ni":"https://dearbulut.github.io/iptv/playlists/country/ni.m3u","dearbulut-country-mm":"https://dearbulut.github.io/iptv/playlists/country/mm.m3u","dearbulut-country-ci":"https://dearbulut.github.io/iptv/playlists/country/ci.m3u","dearbulut-country-si":"https://dearbulut.github.io/iptv/playlists/country/si.m3u","dearbulut-country-by":"https://dearbulut.github.io/iptv/playlists/country/by.m3u","dearbulut-country-eg":"https://dearbulut.github.io/iptv/playlists/country/eg.m3u","dearbulut-country-qa":"https://dearbulut.github.io/iptv/playlists/country/qa.m3u","dearbulut-country-cd":"https://dearbulut.github.io/iptv/playlists/country/cd.m3u","dearbulut-country-lt":"https://dearbulut.github.io/iptv/playlists/country/lt.m3u","dearbulut-country-ba":"https://dearbulut.github.io/iptv/playlists/country/ba.m3u","dearbulut-country-sn":"https://dearbulut.github.io/iptv/playlists/country/sn.m3u","dearbulut-country-cm":"https://dearbulut.github.io/iptv/playlists/country/cm.m3u","dearbulut-country-lk":"https://dearbulut.github.io/iptv/playlists/country/lk.m3u","dearbulut-country-af":"https://dearbulut.github.io/iptv/playlists/country/af.m3u","dearbulut-country-tj":"https://dearbulut.github.io/iptv/playlists/country/tj.m3u","dearbulut-country-ph":"https://dearbulut.github.io/iptv/playlists/country/ph.m3u","dearbulut-country-ht":"https://dearbulut.github.io/iptv/playlists/country/ht.m3u","dearbulut-country-kg":"https://dearbulut.github.io/iptv/playlists/country/kg.m3u","dearbulut-country-dk":"https://dearbulut.github.io/iptv/playlists/country/dk.m3u","dearbulut-country-lv":"https://dearbulut.github.io/iptv/playlists/country/lv.m3u","dearbulut-country-tg":"https://dearbulut.github.io/iptv/playlists/country/tg.m3u","dearbulut-country-lu":"https://dearbulut.github.io/iptv/playlists/country/lu.m3u","dearbulut-country-aw":"https://dearbulut.github.io/iptv/playlists/country/aw.m3u","dearbulut-country-kw":"https://dearbulut.github.io/iptv/playlists/country/kw.m3u","dearbulut-country-nz":"https://dearbulut.github.io/iptv/playlists/country/nz.m3u","dearbulut-country-ie":"https://dearbulut.github.io/iptv/playlists/country/ie.m3u","dearbulut-country-xk":"https://dearbulut.github.io/iptv/playlists/country/xk.m3u","dearbulut-country-gh":"https://dearbulut.github.io/iptv/playlists/country/gh.m3u","dearbulut-country-bj":"https://dearbulut.github.io/iptv/playlists/country/bj.m3u","dearbulut-country-sy":"https://dearbulut.github.io/iptv/playlists/country/sy.m3u","dearbulut-country-mv":"https://dearbulut.github.io/iptv/playlists/country/mv.m3u","dearbulut-language-eng":"https://dearbulut.github.io/iptv/playlists/language/eng.m3u","dearbulut-language-spa":"https://dearbulut.github.io/iptv/playlists/language/spa.m3u","dearbulut-language-rus":"https://dearbulut.github.io/iptv/playlists/language/rus.m3u","dearbulut-language-por":"https://dearbulut.github.io/iptv/playlists/language/por.m3u","dearbulut-language-fra":"https://dearbulut.github.io/iptv/playlists/language/fra.m3u","dearbulut-language-hin":"https://dearbulut.github.io/iptv/playlists/language/hin.m3u","dearbulut-language-ita":"https://dearbulut.github.io/iptv/playlists/language/ita.m3u","dearbulut-language-deu":"https://dearbulut.github.io/iptv/playlists/language/deu.m3u","dearbulut-language-zho":"https://dearbulut.github.io/iptv/playlists/language/zho.m3u","dearbulut-language-fas":"https://dearbulut.github.io/iptv/playlists/language/fas.m3u","dearbulut-language-nld":"https://dearbulut.github.io/iptv/playlists/language/nld.m3u","dearbulut-language-ukr":"https://dearbulut.github.io/iptv/playlists/language/ukr.m3u","dearbulut-language-ron":"https://dearbulut.github.io/iptv/playlists/language/ron.m3u","dearbulut-language-dan":"https://dearbulut.github.io/iptv/playlists/language/dan.m3u","dearbulut-language-hun":"https://dearbulut.github.io/iptv/playlists/language/hun.m3u","dearbulut-language-ind":"https://dearbulut.github.io/iptv/playlists/language/ind.m3u","dearbulut-language-tam":"https://dearbulut.github.io/iptv/playlists/language/tam.m3u","dearbulut-language-pol":"https://dearbulut.github.io/iptv/playlists/language/pol.m3u","dearbulut-language-nor":"https://dearbulut.github.io/iptv/playlists/language/nor.m3u","dearbulut-language-ben":"https://dearbulut.github.io/iptv/playlists/language/ben.m3u","dearbulut-language-vie":"https://dearbulut.github.io/iptv/playlists/language/vie.m3u"}

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
# Expand discovery across the complete old inventory, but treat other countries
# and languages as candidate sources only, never as proof of Turkish speech.
SOURCES = dict(LEGACY_SOURCE_INVENTORY)

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
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
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
