"""K5: ensure legacy IBO decisions are offline, deterministic and position-safe."""
import unittest

from madsc.isolated_ibo_classification import classify_6115_positions


class K5IsolatedIboClassificationTests(unittest.TestCase):
    def test_all_original_positions_are_preserved_without_reindexing(self):
        result = classify_6115_positions()
        self.assertEqual(len(result), 6115)
        self.assertEqual([x.original_position for x in result], list(range(1, 6116)))
        self.assertEqual(result[0].country, "INCELENMEDI")
        self.assertEqual(result[5966].country, "INCELENMEDI")

    def test_reviewed_positions_are_not_automatically_confirmed_as_playable(self):
        result = classify_6115_positions()
        self.assertEqual(result[2].country, "TURK_KULLANICI_BILDIRIMI")
        self.assertEqual(result[2].action, "KALDI")
        self.assertEqual(result[3563].country, "YABANCI_KULLANICI_BILDIRIMI")
        self.assertEqual(result[3563].action, "ARSIV_ONIZLEME")
        self.assertEqual(result[5934].country, "TURK_KULLANICI_BILDIRIMI")
        self.assertTrue(all(x.playback == "BELIRTILMEDI" for x in result))

    def test_unexpected_input_size_fails_closed(self):
        for value in (0, 6114, 6116, True, "6115"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    classify_6115_positions(value)

    def test_preview_has_no_filesystem_arguments_or_side_effects(self):
        first = classify_6115_positions()
        self.assertEqual(first, classify_6115_positions())
        self.assertEqual(sum(x.action == "ARSIV_ONIZLEME" for x in first),
                         len(range(3, 5967)) -
                         sum(x.country == "TURK_KULLANICI_BILDIRIMI" for x in first))


if __name__ == "__main__":
    unittest.main()
