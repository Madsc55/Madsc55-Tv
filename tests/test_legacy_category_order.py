import unittest
from madsc.legacy_category_order import load_historical_categories, route_discovered_candidates


class LegacyCategoryOrderTests(unittest.TestCase):
    def test_snapshot_exact_original_order_and_counts(self):
        data = load_historical_categories()
        self.assertEqual(len(data["entries"]), 1934)
        self.assertEqual(data["entries"][0]["name"], "TRT 1 5 720P HD")
        self.assertEqual(data["entries"][0]["category"], "⭐ FAVORİLER (66)")
        self.assertEqual(data["entries"][0]["order"], 0)
        self.assertNotIn("url", data["entries"][0])

    def test_new_candidates_are_isolated_and_ordered(self):
        result = route_discovered_candidates([{"name": "Yeni A"}, {"name": "Yeni B"}])
        self.assertEqual([x["name"] for x in result["queued"]], ["Yeni A", "Yeni B"])
        self.assertTrue(all(x["destination"] == "YENILER_TEST_BEKLIYOR"
                            for x in result["queued"]))
        self.assertFalse(result["production_writes"])
        self.assertFalse(result["existing_order_modified"])


if __name__ == "__main__":
    unittest.main()
