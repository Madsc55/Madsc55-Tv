"""K5 offline archive manifest regressions; synthetic URLs only."""
import unittest

from madsc.isolated_ibo_archive_preview import build_6115_archive_preview


class K5IboArchivePreviewTests(unittest.TestCase):
    def setUp(self):
        self.urls = [f"https://example.invalid/fixture/{i}" for i in range(1, 6116)]

    def test_complete_preview_is_deterministic_and_preserves_original_positions(self):
        result = build_6115_archive_preview(self.urls)
        self.assertEqual(result, build_6115_archive_preview(self.urls))
        self.assertEqual(result["source_count"], 6115)
        self.assertEqual(result["archive_count"] + result["retained_count"], 6115)
        self.assertEqual(sorted(result["archived_original_positions"] +
                                result["retained_original_positions"]), list(range(1, 6116)))
        self.assertIn(3564, result["archived_original_positions"])
        self.assertIn(5935, result["retained_original_positions"])
        self.assertFalse(result["production_writes"])
        self.assertFalse(result["production_ready"])
        self.assertFalse(result["device_verified"])

    def test_bad_count_duplicate_and_unsafe_urls_fail_closed(self):
        with self.assertRaises(ValueError):
            build_6115_archive_preview(self.urls[:-1])
        for bad in ("http://example.invalid/live", "https://example.invalid/space path",
                    " https://example.invalid/live", "", None, "https://", "https://user:secret@example.invalid/live",
                    "https://example.invalid/live#fragment", "https://example.invalid/path\\segment",
                    "https://example.invalid:0/live", "https://example.invalid:65536/live",
                    "https://example.invalid:invalid/live", "https://example.invalid/\u0001bad",
                    "https://example.invalid/\ud800"):
            candidate = self.urls.copy()
            candidate[10] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                build_6115_archive_preview(candidate)
        duplicate = self.urls.copy()
        duplicate[10] = duplicate[9]
        with self.assertRaises(ValueError):
            build_6115_archive_preview(duplicate)

    def test_order_change_changes_provenance_digest(self):
        swapped = self.urls.copy()
        swapped[1], swapped[2] = swapped[2], swapped[1]
        self.assertNotEqual(build_6115_archive_preview(self.urls)["source_order_sha256"],
                            build_6115_archive_preview(swapped)["source_order_sha256"])


if __name__ == "__main__":
    unittest.main()
