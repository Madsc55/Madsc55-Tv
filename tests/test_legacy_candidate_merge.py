import unittest
from madsc.legacy_candidate_merge import merge_legacy_candidate_rows, FIELDS

class LegacyCandidateMergeTests(unittest.TestCase):
    def test_evidence_precedence_dedup_and_order(self):
        url = "https://example.org/live.m3u8"
        inputs = [
            ("GENEL_ADAY_GERCEK_MEDYA_RAPORU", [
                {"YAYIN_URL": url, "TEKNIK_MEDYA": "YALNIZ_VIDEO", "COZUNURLUK": "640x360"}]),
            ("ONCELIKLI_KANAL_TEK_NIK_RAPOR", [
                {"YAYIN_URL": url, "TEKNIK_MEDYA": "VIDEO_SES_VAR", "COZUNURLUK": "1920x1080"}]),
            ("KESIF", [
                {"YAYIN_URL": url, "KANAL": "A", "LOGO_ADAY_URL": "https://example.org/logo.png"},
                {"YAYIN_URL": url, "KANAL": "B", "LOGO_ADAY_URL": ""},
                {"YAYIN_URL": "https://example.org/second", "KANAL": "C", "TEKNIK_MEDYA": "YALNIZ_VIDEO"},
                {"YAYIN_URL": "ftp://example.org/skip", "KANAL": "Skip"}])]
        result = merge_legacy_candidate_rows(inputs)
        self.assertEqual(result["fields"], list(FIELDS))
        self.assertEqual(result["summary"]["aday_sayisi"], 2)
        self.assertEqual(result["summary"]["eslesen_teknik_kanit"], 1)
        self.assertEqual(result["rows"][0]["KANAL"], "A")
        self.assertEqual(result["rows"][0]["PUAN"], 50)
        self.assertEqual(result["rows"][0]["ANA_LISTEYE_EKLENEBILIR"], "HAYIR")
        self.assertFalse(result["summary"]["production_change_allowed"])

    def test_ties_keep_first_and_empty_inputs(self):
        url = "https://example.org/a"
        result = merge_legacy_candidate_rows([("KESIF", [
            {"YAYIN_URL": url, "KANAL": "First"},
            {"YAYIN_URL": url, "KANAL": "Second"}])])
        self.assertEqual(result["rows"][0]["KANAL"], "First")
        self.assertEqual(merge_legacy_candidate_rows([])["summary"]["aday_sayisi"], 0)

    def test_reject_invalid_input(self):
        for invalid in (None, {}, "x", [("KESIF", [None])]):
            with self.subTest(invalid=invalid), self.assertRaises((ValueError, TypeError)):
                merge_legacy_candidate_rows(invalid)
