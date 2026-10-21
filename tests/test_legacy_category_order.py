import unittest
from madsc.legacy_category_order import load_historical_categories, route_discovered_candidates, audit_historical_metadata


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

    def test_metadata_audit_reports_embedded_attributes_without_repair(self):
        import json
        import tempfile
        from pathlib import Path
        original = load_historical_categories()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "snapshot.json"
            sample = dict(original)
            sample["entries"] = [dict(row) for row in original["entries"]]
            sample["entries"][0]["name"] = "bad group-title=INJECTED"
            path.write_text(json.dumps(sample), encoding="utf-8")
            before = path.read_bytes()
            report = audit_historical_metadata(path)
            self.assertEqual(report["records_checked"], 1934)
            self.assertIn({"file": "CALISANLAR.m3u", "order": 0,
                           "issue": "embedded_m3u_attributes_in_name"}, report["issues"])
            self.assertFalse(report["production_writes"])
            self.assertFalse(report["auto_repairs"])
            self.assertEqual(before, path.read_bytes())

    def test_rejects_invalid_snapshot_root_and_source_manifest(self):
        import json
        import tempfile
        from pathlib import Path
        original = load_historical_categories()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "snapshot.json"
            for bad in ([], {"schema": "madsc55-legacy-order-v1", "entries": []},
                        {**original, "source_repository": "untrusted/repo"},
                        {**original, "source_ref": "unreviewed-branch"},
                        {**original, "source_files": []},
                        {**original, "source_files": [original["source_files"][0]] * 4},
                        {**original, "source_files": [
                            {**entry, "sha": "invalid"} if index == 0 else entry
                            for index, entry in enumerate(original["source_files"])]}):
                path.write_text(json.dumps(bad), encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_historical_categories(path)

    def test_actual_snapshot_metadata_audit_is_read_only(self):
        from pathlib import Path
        from madsc.legacy_category_order import SNAPSHOT
        before = Path(SNAPSHOT).read_bytes()
        report = audit_historical_metadata()
        self.assertEqual(report["records_checked"], 1934)
        self.assertFalse(report["production_writes"])
        self.assertFalse(report["auto_repairs"])
        self.assertEqual(before, Path(SNAPSHOT).read_bytes())
        for issue in report["issues"]:
            self.assertIn(issue["file"], {
                "CALISANLAR.m3u", "YABANCI_KANALLAR.m3u",
                "YENILER.m3u", "CALISMAYANLAR.txt"})
            self.assertIn(issue["issue"], {
                "blank_name", "embedded_m3u_attributes_in_name"})

    def test_metadata_audit_detects_uppercase_embedded_attributes(self):
        import json
        import tempfile
        from pathlib import Path
        original = load_historical_categories()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "snapshot.json"
            sample = dict(original)
            sample["entries"] = [dict(row) for row in original["entries"]]
            sample["entries"][0]["name"] = "Channel TVG-LOGO=unexpected"
            path.write_text(json.dumps(sample), encoding="utf-8")
            report = audit_historical_metadata(path)
            self.assertIn("embedded_m3u_attributes_in_name",
                          [item["issue"] for item in report["issues"]])
            self.assertFalse(report["production_writes"])

    def test_new_candidates_are_isolated_and_ordered(self):
        result = route_discovered_candidates([{"name": "Yeni A"}, {"name": "Yeni B"}])
        self.assertEqual([x["name"] for x in result["queued"]], ["Yeni A", "Yeni B"])
        self.assertTrue(all(x["destination"] == "IZOLE_ADAY_TEST_KUYRUGU"
                            for x in result["queued"]))
        self.assertFalse(result["production_writes"])
        self.assertFalse(result["existing_order_modified"])


if __name__ == "__main__":
    unittest.main()
