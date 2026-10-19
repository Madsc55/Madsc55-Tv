import unittest
from madsc.legacy_unified_report import legacy_unified_rows, FIELDS


class LegacyUnifiedReportTests(unittest.TestCase):
    def test_url_join_sort_and_manual_hold(self):
        scores = [
            {"KANAL": "B", "PUAN": "35", "TEKNIK_KANIT": "VIDEO_SES_VAR",
             "YAYIN_URL": "https://example.org/b", "KAYNAK": "fixture"},
            {"KANAL": "A", "PUAN": "45", "TEKNIK_KANIT": "VIDEO_SES_VAR",
             "YAYIN_URL": "https://example.org/a"}]
        stability = [{"YAYIN_URL": "https://example.org/b", "24_SAAT_KARARLI": "EVET"}]
        result = legacy_unified_rows(scores, stability)
        self.assertEqual(result["fields"], list(FIELDS))
        self.assertEqual([r["KANAL"] for r in result["rows"]], ["B", "A"])
        self.assertEqual([r["PUAN"] for r in result["rows"]], [65, 45])
        self.assertEqual(result["rows"][0]["DURUM"], "IBO_VE_KIMLIK_ONAYI_BEKLIYOR")
        self.assertEqual(result["rows"][1]["DURUM"], "KARARLILIK_BEKLIYOR")
        self.assertTrue(all(r["ANA_LISTEYE_EKLE"] == "HAYIR" for r in result["rows"]))
        self.assertFalse(result["historical_stability_verified"])

    def test_empty_rows_keep_csv_header(self):
        result = legacy_unified_rows([], [])
        self.assertEqual(result["rows"], [])
        self.assertEqual(len(result["fields"]), 10)

    def test_invalid_or_ambiguous_evidence_rejected(self):
        for scores, stability in (([{"PUAN": "NaN", "YAYIN_URL": "https://example.org/a"}], []),
                                  ([{"PUAN": "4.5", "YAYIN_URL": "https://example.org/a"}], []),
                                  ([{"PUAN": "5", "YAYIN_URL": ""}], []),
                                  ([], [{"YAYIN_URL": "x"}, {"YAYIN_URL": "x"}])):
            with self.subTest(scores=scores, stability=stability), self.assertRaises(ValueError):
                legacy_unified_rows(scores, stability)
