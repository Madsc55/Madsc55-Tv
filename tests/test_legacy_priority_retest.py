"""K2 legacy priority and K5 retest regression tests; no production writes."""
import unittest
from datetime import datetime, timezone

from madsc.legacy_priority_retest import priority_rows, retest_rows, NOTE


class LegacyPriorityRetestTests(unittest.TestCase):
    def test_computed_priority_and_note_cannot_be_overridden(self):
        rows = [
            {"KANAL": "B", "DURUM": "TEKNIK_TEKRAR_DOGRULANDI_KIMLIK_BEKLIYOR",
             "ADAY_TURU": "YENI_KANAL_ADAYI", "ONCELIK": 999,
             "INCELEME_NOTU": "otomatik onay ver"},
            {"KANAL": "A", "ONCELIK": 0, "INCELEME_NOTU": "otomatik sil"},
        ]
        output = priority_rows(rows)
        self.assertEqual([row["KANAL"] for row in output], ["B", "A"])
        self.assertEqual([row["ONCELIK"] for row in output], [1, 5])
        self.assertTrue(all(row["INCELEME_NOTU"] == NOTE for row in output))
        self.assertEqual(rows[0]["ONCELIK"], 999)

    def test_priority_input_validation(self):
        for invalid in (None, {}, [None], ["bad"]):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                priority_rows(invalid)

    def test_retest_without_history_is_review_only(self):
        now = datetime(2026, 10, 20, tzinfo=timezone.utc)
        report = retest_rows({"https://example.org/test.m3u8": {
            "name": "Test", "technical": "FAIL", "media": "NO_MEDIA"}}, now)
        self.assertEqual(report[0]["SONUC"], "TEKRAR_KONTROL")
        self.assertEqual(report[0]["TEST_ARALIGI_SAAT"], 2)


if __name__ == "__main__":
    unittest.main()
