import unittest
from madsc.k5_archive_preview import classify_archive_positions

class K5ArchivePreviewTests(unittest.TestCase):
    def test_exact_frozen_partitions(self):
        for scenario, count, keep, archive in (
            ("354", 354, 2, 352),
            ("364", 364, 354, 10),
            ("398", 398, 364, 34),
        ):
            with self.subTest(scenario=scenario):
                source = tuple(range(count))
                result = classify_archive_positions(scenario, source)
                self.assertEqual(len(result.kept_positions), keep)
                self.assertEqual(len(result.archived_positions), archive)
                self.assertEqual(source, tuple(range(count)))
                self.assertEqual(sorted(result.kept_positions + result.archived_positions),
                                 list(range(1, count + 1)))

    def test_exact_position_boundaries_and_input_immutability(self):
        cases = (
            ("354", 354, (1, 2), (3, 334, 335, 354)),
            ("364", 364, (1, 354), (355, 364)),
            ("398", 398, (1, 15, 50, 398), (16, 49)),
        )
        for scenario, count, kept_edges, archive_edges in cases:
            with self.subTest(scenario=scenario):
                entries = list(range(count))
                original = entries.copy()
                preview = classify_archive_positions(scenario, entries)
                self.assertEqual(entries, original)
                for position in kept_edges:
                    self.assertIn(position, preview.kept_positions)
                    self.assertNotIn(position, preview.archived_positions)
                for position in archive_edges:
                    self.assertIn(position, preview.archived_positions)
                    self.assertNotIn(position, preview.kept_positions)
                self.assertEqual(len(set(preview.kept_positions + preview.archived_positions)), count)

    def test_classification_is_not_playback_proof(self):
        result = classify_archive_positions("354", tuple(range(354)))
        self.assertEqual(result.user_reported_unverified_positions, tuple(range(3, 335)))
        self.assertEqual(result.user_classified_foreign_positions, tuple(range(335, 355)))

    def test_354_reported_classes_are_disjoint_and_cover_archive(self):
        preview = classify_archive_positions("354", tuple(range(354)))
        unverified = set(preview.user_reported_unverified_positions)
        foreign = set(preview.user_classified_foreign_positions)
        self.assertFalse(unverified & foreign)
        self.assertEqual(unverified | foreign, set(preview.archived_positions))
        self.assertFalse(set(preview.kept_positions) & (unverified | foreign))

    def test_wrong_count_does_not_iterate_or_mutate_entries(self):
        class LengthOnly:
            def __init__(self, count):
                self.count = count
                self.reads = 0
            def __len__(self):
                return self.count
            def __getitem__(self, index):
                self.reads += 1
                raise AssertionError("planner must not read channel payloads")
        for scenario, count in (("354", 354), ("364", 364), ("398", 398)):
            with self.subTest(scenario=scenario):
                entries = LengthOnly(count - 1)
                with self.assertRaises(ValueError):
                    classify_archive_positions(scenario, entries)
                self.assertEqual(entries.reads, 0)

    def test_fail_closed_on_count_and_unknown_scenario(self):
        for scenario, count in (("354", 354), ("364", 364), ("398", 398)):
            for wrong in (count - 1, count + 1):
                with self.subTest(scenario=scenario, wrong=wrong):
                    with self.assertRaises(ValueError):
                        classify_archive_positions(scenario, tuple(range(wrong)))
        with self.assertRaises(ValueError):
            classify_archive_positions("other", ())
        with self.assertRaises(TypeError):
            classify_archive_positions("354", "x" * 354)

if __name__ == "__main__":
    unittest.main()
