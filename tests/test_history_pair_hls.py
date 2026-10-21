"""H05 atomic single-envelope fault injection and R05 offline HLS windows."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from madsc.history_pair_store import atomic_write_pair, decode_pair
from madsc.hls_segment_window import changed_segment_window


def pair(version):
    return {"gecmis.json": {"history": {"one": {"runs": version}}},
            "ana_liste_test_gecmisi.json": {"channels": {"one": {"runs": version}}}}


class HistoryPairStoreTests(unittest.TestCase):
    def test_single_commit_point_and_fault_preserves_both_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "history-pair.json"
            atomic_write_pair(dest, pair(1))
            before = dest.read_bytes()
            with patch("madsc.history_pair_store.os.replace",
                       side_effect=OSError("injected replace failure")):
                with self.assertRaises(OSError):
                    atomic_write_pair(dest, pair(2))
            self.assertEqual(dest.read_bytes(), before)
            self.assertEqual(decode_pair(dest.read_text()), pair(1))
            self.assertEqual(sorted(p.name for p in Path(tmp).iterdir()), ["history-pair.json"])
            atomic_write_pair(dest, pair(2))
            self.assertEqual(decode_pair(dest.read_text()), pair(2))

    def test_atomic_history_write_rejects_protected_filename_and_symlink_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("CALISANLAR.m3u", "xmltv.xml", "ＹＥＮＩＬＥＲ.m3u"):
                with self.subTest(name=name), self.assertRaises(PermissionError):
                    atomic_write_pair(root / name, pair(1))
                self.assertFalse((root / name).exists())
            real = root / "real"
            real.mkdir()
            linked = root / "linked"
            linked.symlink_to(real, target_is_directory=True)
            with self.assertRaises(ValueError):
                atomic_write_pair(linked / "history.json", pair(1))
            self.assertFalse((real / "history.json").exists())

    def test_corrupt_envelope_and_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dest = root / "pair.json"
            atomic_write_pair(dest, pair(1))
            with self.assertRaises(ValueError):
                decode_pair(dest.read_text().replace('"runs": 1', '"runs": 99'))
            alias = root / "alias.json"
            alias.symlink_to(dest)
            with self.assertRaises(ValueError):
                atomic_write_pair(alias, pair(2))


class HlsWindowTests(unittest.TestCase):
    def test_rotating_segments_and_unchanged_window(self):
        first = "#EXTM3U\n#EXT-X-MEDIA-SEQUENCE:10\n#EXTINF:4,\na.ts\n#EXTINF:4,\nb.ts\n"
        second = "#EXTM3U\n#EXT-X-MEDIA-SEQUENCE:11\n#EXTINF:4,\nb.ts\n#EXTINF:4,\nc.ts\n"
        changed = changed_segment_window(first, second)
        self.assertTrue(changed["changed"])
        self.assertFalse(changed["video_audio_verified"])
        self.assertFalse(changed["production_ready"])
        self.assertFalse(changed_segment_window(first, first)["changed"])

    def test_static_segment_is_not_proof_of_stream_failure(self):
        static = "#EXTM3U\n#EXTINF:10,\nsegment.ts\n"
        result = changed_segment_window(static, static)
        self.assertFalse(result["changed"])
        self.assertNotIn("stream_failed", result)
        for invalid in ("bad", "#EXTM3U\n#EXTINF:4,\nfile://unsafe",
                        "#EXTM3U\n#EXT-X-KEY:METHOD=AES-128\n#EXTINF:4,\na.ts"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                changed_segment_window(invalid, static)


if __name__ == "__main__":
    unittest.main()
