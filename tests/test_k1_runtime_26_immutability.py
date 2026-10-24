"""K1: 26 isolated runtime-denial and byte-for-byte immutability checks.

These tests exercise the explicit repository write gate only. They do not prove
that every production caller invokes it, nor prevent independent git pushes.
"""
import hashlib
import tempfile
import unittest
from pathlib import Path

from madsc.write_path_audit import ProtectedWriteRejected, enforce_write_paths


PROTECTED_CASES = [
    'CALISANLAR.m3u',
    'CALISMAYANLAR.txt',
    'YENILER.m3u',
    'YABANCI_KANALLAR.m3u',
    'GUVENLIK_KURALLARI.md',
    'AGENTS.md',
    'xmltv.xml',
    'playlist.m3u8',
    'yedekler/backup.json',
    'YEDEKLER/backup.json',
    'FAVORILER/channels.json',
    'HEPSI/channels.json',
    'EPG/guide.xml',
    'logolar/logo.png',
    'logos/logo.png',
    'arsiv/archive.json',
    'nested/xmltv.xml',
    'nested/playlist.m3u8',
    'nested/CALISANLAR.m3u',
    'nested/AGENTS.md',
    'docs/eski_depo_not_arsivi/notes.txt',
    'nested/favoriler/channels.json',
    'nested/hepsi/channels.json',
    'nested/epg/guide.xml',
    'nested/yedekler/backup.json',
    'nested/logolar/logo.png'
]


def guarded_write(root: Path, relative: str, payload: bytes) -> None:
    """A representative caller: authorization MUST precede filesystem writes."""
    enforce_write_paths([relative])
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)


class K1RuntimeImmutabilityAcceptance(unittest.TestCase):
    def test_26_protected_write_attempts_leave_existing_bytes_unchanged(self):
        self.assertEqual(len(PROTECTED_CASES), 26)
        self.assertEqual(len(set(PROTECTED_CASES)), 26)
        with tempfile.TemporaryDirectory(prefix="k1-acceptance-") as sandbox:
            root = Path(sandbox)
            for index, relative in enumerate(PROTECTED_CASES, 1):
                with self.subTest(rule=index, path=relative):
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    original = ("immutable-k1-%02d:" % index).encode() + bytes(range(32))
                    target.write_bytes(original)  # isolated fixture setup only
                    before = hashlib.sha256(target.read_bytes()).hexdigest()
                    with self.assertRaises(ProtectedWriteRejected):
                        guarded_write(root, relative, b"UNAUTHORIZED OVERWRITE")
                    after = hashlib.sha256(target.read_bytes()).hexdigest()
                    self.assertEqual(before, after)
                    self.assertEqual(target.read_bytes(), original)

    def test_nonprotected_sandbox_evidence_write_is_allowed(self):
        with tempfile.TemporaryDirectory(prefix="k1-acceptance-") as sandbox:
            root = Path(sandbox)
            guarded_write(root, "reports/k1-evidence.json", b'{"safe":true}')
            self.assertEqual((root / "reports/k1-evidence.json").read_bytes(),
                             b'{"safe":true}')


if __name__ == "__main__":
    unittest.main()
