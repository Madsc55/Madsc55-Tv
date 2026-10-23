import unittest
from madsc.trial_epg_matching import matches, playlist_entries, programme_coverage

XML = '<tv><channel id="a"><display-name>TRT 1</display-name></channel><channel id="b"><display-name>TV 8</display-name></channel><channel id="c"><display-name>TV-8</display-name></channel></tv>'
class TrialEpgMatchingTest(unittest.TestCase):
    def test_exact_and_ambiguous_and_unmatched(self):
        m = '#EXTM3U\n#EXTINF:-1,TRT 1\nhttps://example.org/a.m3u8\n#EXTINF:-1,TV8\nhttps://example.org/b.m3u8\n#EXTINF:-1,Unknown\nhttps://example.org/c.m3u8\n'
        result = matches(m, XML)
        self.assertEqual([x["status"] for x in result], ["exact_unique", "ambiguous", "unmatched"])
        self.assertEqual(result[0]["matched_id"], "a")
        self.assertEqual(result[1]["matched_id"], "")
    def test_programme_coverage_distinguishes_matching_from_actual_guide(self):
        xml = '<tv><channel id="a"><display-name>TRT 1</display-name></channel><channel id="b"><display-name>TV 8</display-name></channel><programme channel="a" start="20261023100000 +0000" stop="20261023110000 +0000"><title>News</title></programme></tv>'
        rows = programme_coverage('#EXTINF:-1 tvg-id="a",TRT 1\n#EXTINF:-1 tvg-id="b",TV 8\n#EXTINF:-1,Unknown', xml)
        self.assertEqual([r["programme_count"] for r in rows], [1, 0, 0])
        self.assertEqual([r["has_programmes"] for r in rows], [True, False, False])
    def test_orphan_xmltv_programme_does_not_create_guide_coverage(self):
        xml = '<tv><channel id="a"><display-name>TRT 1</display-name></channel><programme channel="missing" start="20261023100000 +0000"><title>Orphan</title></programme></tv>'
        rows = programme_coverage('#EXTINF:-1 tvg-id="a",TRT 1', xml)
        self.assertEqual(rows[0]["programme_count"], 0)
        self.assertFalse(rows[0]["has_programmes"])
    def test_programme_coverage_rejects_entities(self):
        with self.assertRaisesRegex(ValueError, "DTD/entity"):
            programme_coverage('#EXTINF:-1,TRT 1', '<!DOCTYPE tv><tv/>')
    def test_existing_id(self):
        self.assertEqual(matches('#EXTINF:-1 tvg-id="a",Other', XML)[0]["status"], "existing_valid")
    def test_duplicate_xmltv_channel_ids_fail_closed(self):
        duplicate = '<tv><channel id="a"/><channel id="a"/></tv>'
        with self.assertRaisesRegex(ValueError, "Duplicate XMLTV channel id"):
            matches('#EXTINF:-1 tvg-id="a",TRT 1', duplicate)
    def test_invalid_xmltv_root_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "root element"):
            matches('#EXTINF:-1 tvg-id="a",TRT 1', '<playlist/>')
    def test_missing_xmltv_channel_id_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "missing a nonempty id"):
            matches('#EXTINF:-1,TRT 1', '<tv><channel/></tv>')
    def test_empty(self):
        self.assertEqual(playlist_entries("#EXTM3U"), [])
    def test_quoted_comma_in_attribute(self):
        self.assertEqual(playlist_entries('#EXTINF:-1 tvg-name="News, Live" tvg-id="a",TRT 1'), [("TRT 1", "a")])
    def test_duplicate_tvg_id_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "Duplicate tvg-id"):
            playlist_entries('#EXTINF:-1 tvg-id="a" tvg-id="b",TRT 1')
    def test_malformed_tvg_id_fails_closed(self):
        for entry in ('#EXTINF:-1 tvg-id=a,TRT 1', '#EXTINF:-1 tvg-id ="a",TRT 1', '#EXTINF:-1 tvg-id="a" tvg-id=b,TRT 1'):
            with self.subTest(entry=entry), self.assertRaisesRegex(ValueError, "Malformed tvg-id"):
                playlist_entries(entry)
    def test_tvg_id_trailing_garbage_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "Malformed tvg-id"):
            playlist_entries('#EXTINF:-1 tvg-id="a"junk,TRT 1')

    def test_quoted_other_attribute_is_not_tvg_id(self):
        self.assertEqual(playlist_entries('#EXTINF:-1 tvg-name="contains tvg-id=bogus",TRT 1'), [("TRT 1", "")])
    def test_malformed_separator_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "Malformed EXTINF"):
            playlist_entries('#EXTINF:-1 tvg-id="a" TRT 1')
    def test_xmltv_entity_declaration_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "DTD/entity"):
            matches('#EXTINF:-1,TRT 1', '<!DOCTYPE tv [<!ENTITY x "y">]><tv/>')
    def test_title_does_not_inject_tvg_id(self):
        self.assertEqual(playlist_entries('#EXTINF:-1,Title tvg-id="fake"'), [('Title tvg-id="fake"', '')])
    def test_existing_quality_variant_id_retained(self):
        m = '#EXTINF:-1 tvg-id="a",TRT 1 HD\n#EXTINF:-1 tvg-id="a",TRT 1 SD'
        self.assertEqual([r["status"] for r in matches(m, XML)], ["existing_valid", "existing_valid"])
if __name__ == "__main__":
    unittest.main()
