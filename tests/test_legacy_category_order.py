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

    def test_rejects_invalid_historical_rows_without_mutation(self):
        import json
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "snapshot.json"
            for entries in ([None], [{"file": "UNKNOWN", "order": 0}]):
                path.write_text(json.dumps({"schema": "madsc55-legacy-order-v1",
                                            "entries": entries}), encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_historical_categories(path)

    def test_blank_candidate_name_is_rejected(self):
        for name in ("", "  ", chr(10)):
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    route_discovered_candidates([{"name": name}])

    def test_new_candidates_are_isolated_and_ordered(self):
        result = route_discovered_candidates([{"name": "Yeni A"}, {"name": "Yeni B"}])
        self.assertEqual([x["name"] for x in result["queued"]], ["Yeni A", "Yeni B"])
        self.assertTrue(all(x["destination"] == "IZOLE_ADAY_TEST_KUYRUGU"
                            for x in result["queued"]))
        self.assertFalse(result["production_writes"])
        self.assertFalse(result["existing_order_modified"])


if __name__ == "__main__":
    unittest.main()
