"""Read-only 390-candidate legacy probe and decode compatibility."""
import concurrent.futures
import csv
import io
import subprocess


def parse_entries(content):
    if not isinstance(content, str) or len(content) > 8_000_000:
        raise ValueError("Invalid candidate playlist")
    entries = []
    meta = None
    for line in content.lstrip("\ufeff").splitlines():
        line = line.strip()
        if line.startswith("#EXTINF:"):
            meta = line
        elif meta and line.startswith(("https://", "http://")):
            entries.append((meta, line))
            meta = None
    return entries


def check_stream(item, runner=subprocess.run):
    meta, url = item
    name = meta.rsplit(",", 1)[-1]
    try:
        probe = runner(["ffprobe", "-v", "error", "-rw_timeout", "12000000",
                        "-analyzeduration", "4000000", "-show_entries",
                        "stream=codec_type", "-of", "csv=p=0", url],
                       capture_output=True, text=True, timeout=22)
        codecs = probe.stdout.lower().splitlines()
        if probe.returncode or not (any("video" in x for x in codecs)
                                    and any("audio" in x for x in codecs)):
            return meta, url, name, "DOGRULANAMADI", "Video ve ses birlikte dogrulanamadi"
        sample = runner(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
                         "-rw_timeout", "12000000", "-i", url, "-t", "20",
                         "-map", "0:v:0", "-map", "0:a:0", "-f", "null", "-"],
                        capture_output=True, text=True, timeout=45)
        if sample.returncode == 0:
            return meta, url, name, "TEKNIK_VIDEO_SES_20SN", (
                "20 saniye medya cozumleme basarili; kanal kimligi dogrulanmadi")
        return meta, url, name, "DOGRULANAMADI", sample.stderr[-180:].replace("\n", " ")
    except Exception as exc:
        return meta, url, name, "DOGRULANAMADI", str(exc)[:180]


def evaluate_entries(entries, runner=subprocess.run, workers=10):
    if (not isinstance(entries, list) or len(entries) > 20000
            or any(not isinstance(item, (tuple, list)) or len(item) != 2
                   or any(not isinstance(value, str) for value in item) for item in entries)
            or type(workers) is not int or not 1 <= workers <= 12):
        raise ValueError("Invalid worker count")
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(lambda item: check_stream(item, runner), entries))
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["KANAL", "DURUM", "ACIKLAMA", "URL"])
    writer.writerows((name, status, detail, url) for _, url, name, status, detail in results)
    lines = ["#EXTM3U"]
    for meta, url, _, status, _ in results:
        if status == "TEKNIK_VIDEO_SES_20SN":
            lines.extend((meta, url))
    return {"results": results, "csv_text": output.getvalue(),
            "technical_m3u": "\n".join(lines) + "\n",
            "technical_pass_count": (len(lines) - 1) // 2,
            "identity_verified": False, "ibo_device_verified": False,
            "production_writes": False, "production_ready": False}
