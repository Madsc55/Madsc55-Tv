#!/usr/bin/env python3
"""Eski MADSC TV notlarini tek dosyada, kayipsiz birlestir.

Yalniz docs/eski_depo_not_arsivi altindaki tarihsel kopyalari okur.
GitHub API boyut sinirina takilmamak icin dosyalari yerel diskte akisa yazar.
Varsayilan davranis kaynaklari silmez. --remove-archived-notes yalnizca
birebir dogrulanan ve birlestirilen .md/.txt/.rst arşiv kopyalarini siler.
JSON/CSV kaynaklari yalnizca --include-structured ile dahil edilir.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs" / "eski_depo_not_arsivi"
OUTPUT = ROOT / "ESKI_SISTEM_NOTLARI.md"
EXTS = {".md", ".txt", ".rst"}
STRUCTURED = {".json", ".csv"}


def source_files(include_structured=False):
    suffixes = EXTS | (STRUCTURED if include_structured else set())
    return sorted(
        (p for p in ARCHIVE.rglob("*") if p.is_file() and p.suffix.lower() in suffixes),
        key=lambda p: p.relative_to(ARCHIVE).as_posix(),
    )


def build(include_structured=False, remove=False):
    paths = source_files(include_structured)
    if not paths:
        raise RuntimeError("Arsiv kaynak dosyalari bulunamadi")
    # Index/README (yeni arsiv aciklamasi) eski kaynak notu degildir.
    paths = [p for p in paths if p.relative_to(ARCHIVE).as_posix() != "ARSIV_REHBERI.md"]
    if not any(p.name == "AGENTS.md" for p in paths):
        raise RuntimeError("AGENTS.md arsivde yok; islem durduruldu")
    pieces = []
    hashes = {}
    for p in paths:
        rel = p.relative_to(ARCHIVE).as_posix()
        data = p.read_bytes()
        try:
            value = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise RuntimeError(f"UTF-8 olmayan not: {rel}") from exc
        hashes[rel] = hashlib.sha256(data).hexdigest()
        # Her bolumun ham icerigini degistirmeden sakla; fence/escape uygulama.
        pieces.append(f"\\n\\n<!-- KAYNAK-BASLANGIC: {rel} SHA256:{hashes[rel]} -->\\n")
        pieces.append(value)
        pieces.append(f"\\n<!-- KAYNAK-BITIS: {rel} -->\\n")
    header = (
        "# ESKİ SİSTEM NOTLARI\\n\\n"
        "Kaynak: Madsc55/madsc-tv, madsc/bes-sistem-toplu-birlestirme.\\n"
        "Bu belge tarihsel arşivdir; eski talimatlar yeni yazma izni vermez.\\n"
        f"Birleştirilen kaynak sayısı: {len(paths)}.\\n"
        "Her bölüm SHA256 ile tanımlanır; özgün içerik değiştirilmez.\\n"
    )
    merged = header + "".join(pieces)
    # Kaynaklar ancak tam byte-seviyesi geri ayristirma ile dogrulanir.
    for p in paths:
        rel = p.relative_to(ARCHIVE).as_posix()
        start = f"\\n\\n<!-- KAYNAK-BASLANGIC: {rel} SHA256:{hashes[rel]} -->\\n"
        end = f"\\n<!-- KAYNAK-BITIS: {rel} -->\\n"
        if merged.count(start) != 1 or merged.count(end) != 1:
            raise RuntimeError(f"Sinir isaretcisi tekil degil: {rel}")
        recovered = merged.split(start, 1)[1].split(end, 1)[0].encode("utf-8")
        if hashlib.sha256(recovered).hexdigest() != hashes[rel]:
            raise RuntimeError(f"Birlesim dogrulanamadi: {rel}")
    tmp = OUTPUT.with_suffix(".md.tmp")
    tmp.write_text(merged, encoding="utf-8")
    tmp.replace(OUTPUT)
    if remove:
        # Yalnizca eski metin not kopyalari. JSON/CSV arsiv kopyalari
        # ozellikle korunur; yanlislikla veri kaybi olmasin.
        for p in paths:
            if p.suffix.lower() in EXTS:
                p.unlink()
    print(json.dumps({"output": str(OUTPUT), "sources": len(paths),
                      "bytes": OUTPUT.stat().st_size, "removed_text_copies": bool(remove)},
                     ensure_ascii=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--include-structured", action="store_true")
    ap.add_argument("--remove-archived-notes", action="store_true")
    args = ap.parse_args()
    build(args.include_structured, args.remove_archived_notes)
