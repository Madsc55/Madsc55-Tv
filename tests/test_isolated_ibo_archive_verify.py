"""Offline K5 independent manifest verifier regression tests."""
import unittest

from madsc.isolated_ibo_archive_preview import build_6115_archive_preview
from madsc.isolated_ibo_archive_verify import verify_6115_archive_preview


class K5ManifestVerificationTests(unittest.TestCase):
    def setUp(self):
        self.urls = [f"https://example.org/live/{i}.m3u8" for i in range(6115)]
        self.manifest = build_6115_archive_preview(self.urls)

    def test_valid(self):
        report = verify_6115_archive_preview(self.urls, self.manifest)
        self.assertTrue(report["verified"])
        self.assertFalse(report["playback_verified"])

    def test_source_reorder_rejected(self):
        urls = self.urls.copy()
        urls[0], urls[1] = urls[1], urls[0]
        with self.assertRaises(ValueError):
            verify_6115_archive_preview(urls, self.manifest)

    def test_position_tamper_rejected(self):
        altered = dict(self.manifest)
        altered["archived_original_positions"] = self.manifest["archived_original_positions"][:-1]
        with self.assertRaises(ValueError):
            verify_6115_archive_preview(self.urls, altered)

    def test_extra_fields_rejected(self):
        with self.assertRaises(ValueError):
            verify_6115_archive_preview(self.urls, {**self.manifest, "device_verified": True})

    def test_bool_count_rejected(self):
        with self.assertRaises(ValueError):
            verify_6115_archive_preview(self.urls, {**self.manifest, "source_count": True})


if __name__ == "__main__":
    unittest.main()
