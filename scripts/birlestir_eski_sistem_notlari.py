#!/usr/bin/env python3
"""Eski MADSC TV notlarini tek dosyada, kayipsiz birlestir.

Yalniz docs/eski_depo_not_arsivi altindaki tarihsel kopyalari okur.
GitHub API boyut sinirina takilmamak icin dosyalari yerel diskte akisa yazar.
Varsayilan davranis kaynaklari silmez. --remove-archived-notes geriye donuk
CLI uyumlulugu icin taninir ancak korunan arsiv kopyalarini silmeyi reddeder.
JSON/CSV kaynaklari yalnizca --include-structured ile dahil edilir.
"""
import argparse
import hashlib
import json
import os
import stat
from pathlib import Path

from madsc.fixture_report_writer import write_exclusive_bytes
from madsc.write_path_audit import (enforce_local_output_path,
                                    enforce_local_replace_path)

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs" / "eski_depo_not_arsivi"
OUTPUT = ROOT / "ESKI_SISTEM_NOTLARI.md"
EXTS = {".md", ".txt", ".rst"}
STRUCTURED = {".json", ".csv"}


def _replace_output_atomically(destination, payload):
    """Replace the merged note through one guarded, no-follow parent fd."""
    destination = Path(destination)
    allowed_root = destination.parent
    tmp = destination.with_suffix(destination.suffix + ".tmp")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory_flag = getattr(os, "O_DIRECTORY", None)
    if not isinstance(nofollow, int) or not isinstance(directory_flag, int):
        raise PermissionError("Secure descriptor-relative replacement is unavailable")
    enforce_local_replace_path(destination, allowed_root=allowed_root)
    enforce_local_output_path(tmp, allowed_root=allowed_root)
    write_exclusive_bytes(tmp, payload, allowed_root=allowed_root)
    identity = tmp.lstat()
    parent_fd = os.open(destination.parent.anchor,
                        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                        | getattr(os, "O_NOFOLLOW", 0))
    try:
        for part in destination.parent.parts[1:]:
            next_fd = os.open(part, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                              | getattr(os, "O_NOFOLLOW", 0),
                              dir_fd=parent_fd)
            os.close(parent_fd)
            parent_fd = next_fd
        current = os.stat(tmp.name, dir_fd=parent_fd, follow_symlinks=False)
        if (not stat.S_ISREG(current.st_mode) or current.st_nlink != 1
                or (current.st_dev, current.st_ino, current.st_size,
                    current.st_mtime_ns, current.st_ctime_ns) !=
                   (identity.st_dev, identity.st_ino, identity.st_size,
                    identity.st_mtime_ns, identity.st_ctime_ns)):
            raise PermissionError("Temporary merged note changed before replacement")
        enforce_local_replace_path(destination, allowed_root=allowed_root)
        os.replace(tmp.name, destination.name,
                   src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
    finally:
        os.close(parent_fd)


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
    if remove:
        raise PermissionError("Archived source note removal is prohibited")
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
        pieces.append(f"\n\n<!-- KAYNAK-BASLANGIC: {rel} SHA256:{hashes[rel]} -->\n")
        pieces.append(value)
        pieces.append(f"\n<!-- KAYNAK-BITIS: {rel} -->\n")
    header = (
        "# ESKİ SİSTEM NOTLARI\n\n"
        "Kaynak: Madsc55/madsc-tv, madsc/bes-sistem-toplu-birlestirme.\n"
        "Bu belge tarihsel arşivdir; eski talimatlar yeni yazma izni vermez.\n"
        f"Birleştirilen kaynak sayısı: {len(paths)}.\n"
        "Her bölüm SHA256 ile tanımlanır; özgün içerik değiştirilmez.\n"
    )
    merged = header + "".join(pieces)
    # Kaynaklar ancak tam byte-seviyesi geri ayristirma ile dogrulanir.
    for p in paths:
        rel = p.relative_to(ARCHIVE).as_posix()
        start = f"\n\n<!-- KAYNAK-BASLANGIC: {rel} SHA256:{hashes[rel]} -->\n"
        end = f"\n<!-- KAYNAK-BITIS: {rel} -->\n"
        if merged.count(start) != 1 or merged.count(end) != 1:
            raise RuntimeError(f"Sinir isaretcisi tekil degil: {rel}")
        recovered = merged.split(start, 1)[1].split(end, 1)[0].encode("utf-8")
        if hashlib.sha256(recovered).hexdigest() != hashes[rel]:
            raise RuntimeError(f"Birlesim dogrulanamadi: {rel}")
    _replace_output_atomically(OUTPUT, merged.encode("utf-8"))
    print(json.dumps({"output": str(OUTPUT), "sources": len(paths),
                      "bytes": OUTPUT.stat().st_size, "removed_text_copies": bool(remove)},
                     ensure_ascii=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--include-structured", action="store_true")
    ap.add_argument("--remove-archived-notes", action="store_true")
    args = ap.parse_args()
    build(args.include_structured, args.remove_archived_notes)
