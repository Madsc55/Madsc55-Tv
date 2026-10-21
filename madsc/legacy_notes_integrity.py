"""Independently verify every archived legacy note against merged bytes."""
import argparse
import hashlib
import json
from pathlib import Path
from madsc.write_path_audit import enforce_local_output_path

SUFFIXES = {".md", ".txt", ".rst", ".json", ".csv"}
EXCLUDE = {"ARSIV_REHBERI.md"}


def verify(merged, archive, report):
    merged, archive, report = Path(merged), Path(archive), Path(report)
    if archive.is_symlink() or not archive.is_dir() or merged.is_symlink():
        raise ValueError("Unsafe legacy note paths")
    sources = sorted(
        (p for p in archive.rglob("*") if p.is_file() and p.suffix.lower() in SUFFIXES
         and p.relative_to(archive).as_posix() not in EXCLUDE),
        key=lambda p: p.relative_to(archive).as_posix())
    if not sources or not any(p.name == "AGENTS.md" for p in sources):
        raise ValueError("Missing archived legacy notes")
    raw = merged.read_bytes()
    text = raw.decode("utf-8")
    if not text.startswith("# ESKİ SİSTEM NOTLARI\n"):
        raise ValueError("Invalid merged archive header")
    if f"Birleştirilen kaynak sayısı: {len(sources)}.\n" not in text:
        raise ValueError("Merged source count mismatch")
    # Reconstruct the entire document, not only the marked source sections.
    # Otherwise unmarked injected text can pass all per-source hash checks.
    expected = (
        "# ESKİ SİSTEM NOTLARI\n\n"
        "Kaynak: Madsc55/madsc-tv, madsc/bes-sistem-toplu-birlestirme.\n"
        "Bu belge tarihsel arşivdir; eski talimatlar yeni yazma izni vermez.\n"
        f"Birleştirilen kaynak sayısı: {len(sources)}.\n"
        "Her bölüm SHA256 ile tanımlanır; özgün içerik değiştirilmez.\n"
    ).encode("utf-8")
    results = []
    for p in sources:
        if p.is_symlink():
            raise ValueError("Symlinked legacy note")
        rel = p.relative_to(archive).as_posix()
        data = p.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        begin = f"\n\n<!-- KAYNAK-BASLANGIC: {rel} SHA256:{digest} -->\n"
        end = f"\n<!-- KAYNAK-BITIS: {rel} -->\n"
        if text.count(begin) != 1 or text.count(end) != 1:
            raise ValueError(f"Missing or duplicate source boundary: {rel}")
        body = text.split(begin, 1)[1].split(end, 1)[0].encode("utf-8")
        if body != data:
            raise ValueError(f"Byte mismatch: {rel}")
        expected += begin.encode("utf-8") + data + end.encode("utf-8")
        results.append({"path": rel, "sha256": digest, "bytes": len(data)})
    if text.count("<!-- KAYNAK-BASLANGIC:") != len(sources) or text.count("<!-- KAYNAK-BITIS:") != len(sources):
        raise ValueError("Unexpected extra merged source markers")
    if raw != expected:
        raise ValueError("Unexpected text outside verified legacy source sections")
    if report.exists() or report.is_symlink():
        raise ValueError("Refusing to overwrite verification report")
    enforce_local_output_path(report.absolute())
    result = {"verified": True, "sources": len(results), "merged_sha256": hashlib.sha256(raw).hexdigest(),
              "merged_bytes": len(raw), "entries": results, "production_writes": False}
    with report.open("x", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, sort_keys=True, indent=2)
        out.write("\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--merged", required=True)
    parser.add_argument("--archive", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    result = verify(args.merged, args.archive, args.report)
    print(json.dumps({"verified": result["verified"], "sources": result["sources"],
                      "merged_sha256": result["merged_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
