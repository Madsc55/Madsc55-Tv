import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from madsc.epg import check_epg_mapping

class EpgTests(unittest.TestCase):

    def test_malformed_tvg_id_forms_fail_closed(self):
        for attribute in ('tvg-id=trt1.tr', 'tvg-id = "trt1.tr"', 'tvg-id="trt1.tr" tvg-id=other.tr'):
            with self.subTest(attribute=attribute), tempfile.TemporaryDirectory() as d:
                p = Path(d) / "playlist.m3u8"
                e = Path(d) / "xmltv.xml"
                p.write_text(f'#EXTM3U\n#EXTINF:-1 {attribute},TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
                e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "Malformed M3U tvg-id attribute"):
                    check_epg_mapping(p, e)

    def test_malformed_extinf_directive_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text("#EXTM3U\n#EXTINF -1,TRT 1\nhttps://example.org/live\n", encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Malformed M3U EXTINF directive"):
                check_epg_mapping(p, e)

    def test_malformed_extinf_rejected_alongside_valid_channel(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\nhttps://example.org/a.m3u8\n#EXTINF -1,Broken\nhttps://example.org/b.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Malformed M3U EXTINF directive"):
                check_epg_mapping(p, e)

    def test_non_http_stream_uri_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\nfile:///local/video.ts\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "invalid stream URI"):
                check_epg_mapping(p, e)

    def test_empty_playlist_is_not_reported_as_matching(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text("#EXTM3U\n", encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            result = check_epg_mapping(p, e)
            self.assertEqual(result["playlist_channels"], 0)
            self.assertFalse(result["matching_verified"])

    def test_duplicate_xmltv_channel_ids_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/><channel id="trt1.tr"/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Duplicate XMLTV channel id"):
                check_epg_mapping(p, e)

    def test_xmltv_channel_without_id_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing a nonempty id"):
                check_epg_mapping(p, e)

    def test_playlist_m3u8_and_xmltv_match(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\nhttps://example.org/index.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"><display-name>TRT 1</display-name></channel><programme channel="trt1.tr" start="20261019010000 +0000" stop="20261019020000 +0000"><title>Test</title></programme></tv>', encoding="utf-8")
            original = p.read_bytes()
            result = check_epg_mapping(p, e)
            self.assertTrue(result["matching_verified"])
            self.assertFalse(result["device_verified"])
            self.assertEqual(p.read_bytes(), original)
            e.write_text('<tv><channel id="other"/></tv>', encoding="utf-8")
            self.assertFalse(check_epg_mapping(p, e)["matching_verified"])

    def test_programme_without_channel_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/><programme start="20261019010000 +0000" stop="20261019020000 +0000"><title>Test</title></programme></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "programme is missing a nonempty channel"):
                check_epg_mapping(p, e)

    def test_blank_programme_channel_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/><programme channel="  " start="20261019010000 +0000" stop="20261019020000 +0000"><title>Test</title></programme></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "programme is missing a nonempty channel"):
                check_epg_mapping(p, e)

    def test_unmatched_programme_channel_blocks_matching(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/><programme channel="missing.tr" start="20261019010000 +0000" stop="20261019020000 +0000"><title>Test</title></programme></tv>', encoding="utf-8")
            result = check_epg_mapping(p, e)
            self.assertFalse(result["matching_verified"])
            self.assertEqual(result["unmatched_programme_ids"], ["missing.tr"])

    def test_duplicate_playlist_tvg_id_attributes_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr" tvg-id="other.tr",TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/><channel id="other.tr"/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Duplicate M3U tvg-id attribute"):
                check_epg_mapping(p, e)

    def test_whitespace_around_playlist_tvg_id_is_normalized(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id=" trt1.tr ",TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            result = check_epg_mapping(p, e)
            self.assertTrue(result["matching_verified"])
            self.assertEqual(result["unmatched_playlist_ids"], [])

    def test_invalid_playlist_header_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTINF:-1 tvg-id="trt1.tr",TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Invalid M3U8 playlist"):
                check_epg_mapping(p, e)

    def test_invalid_xmltv_root_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<playlist><channel id="trt1.tr"/></playlist>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Expected XMLTV tv root"):
                check_epg_mapping(p, e)

    def test_malformed_xmltv_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"></tv>', encoding="utf-8")
            with self.assertRaises(ET.ParseError):
                check_epg_mapping(p, e)

    def test_malformed_m3u_header_suffix_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U-invalid\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Invalid M3U8 playlist"):
                check_epg_mapping(p, e)

    def test_tvg_id_substring_in_another_attribute_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 not-tvg-id="trt1.tr",TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            result = check_epg_mapping(p, e)
            self.assertEqual(result["missing_tvg_id"], 1)
            self.assertFalse(result["matching_verified"])

    def test_tvg_id_text_in_display_name_is_not_an_attribute(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1,News tvg-id="trt1.tr"\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            result = check_epg_mapping(p, e)
            self.assertEqual(result["missing_tvg_id"], 1)
            self.assertFalse(result["matching_verified"])

    def test_duplicate_playlist_channel_ids_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\nhttps://example.org/a.m3u8\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1 duplicate\nhttps://example.org/b.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            result = check_epg_mapping(p, e)
            self.assertEqual(result["duplicate_playlist_ids"], ["trt1.tr"])
            self.assertFalse(result["matching_verified"])

    def test_multiple_duplicate_ids_are_sorted_and_empty_ids_excluded(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            ids = ("z.tr", "a.tr", "z.tr", "", "a.tr", "")
            rows = ['#EXTM3U']
            for i, channel_id in enumerate(ids):
                rows.extend((f'#EXTINF:-1 tvg-id="{channel_id}",Channel {i}', f'https://example.org/{i}.m3u8'))
            p.write_text("\n".join(rows) + "\n", encoding="utf-8")
            e.write_text('<tv><channel id="a.tr"/><channel id="z.tr"/></tv>', encoding="utf-8")
            result = check_epg_mapping(p, e)
            self.assertEqual(result["duplicate_playlist_ids"], ["a.tr", "z.tr"])
            self.assertEqual(result["missing_tvg_id"], 2)
            self.assertFalse(result["matching_verified"])

    def test_nul_byte_in_playlist_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_bytes(b'#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\x00\nhttps://example.org/a.m3u8\n')
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "NUL byte"):
                check_epg_mapping(p, e)

    def test_xmltv_doctype_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<!DOCTYPE tv [<!ENTITY channel "trt1.tr">]><tv><channel id="&channel;"/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "DTD and entity"):
                check_epg_mapping(p, e)

    def test_extinf_without_comma_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr"\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing channel-name separator"):
                check_epg_mapping(p, e)

    def test_comma_inside_quoted_metadata_does_not_split_extinf(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 group-title="News, International" tvg-id="trt1.tr",TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            self.assertTrue(check_epg_mapping(p, e)["matching_verified"])

    def test_unclosed_quoted_attribute_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 group-title="News, International tvg-id="trt1.tr",TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing channel-name separator"):
                check_epg_mapping(p, e)

    def test_tvg_id_text_inside_other_quoted_attribute_is_ignored(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 group-title="News tvg-id="trt1.tr"",Channel\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            self.assertFalse(check_epg_mapping(p, e)["matching_verified"])

    def test_unbalanced_quote_in_extinf_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr" group-title="News,TRT 1\nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing channel-name separator"):
                check_epg_mapping(p, e)

    def test_empty_extinf_channel_name_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",   \nhttps://example.org/a.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "empty channel name"):
                check_epg_mapping(p, e)

    def test_extinf_without_stream_uri_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing stream URI"):
                check_epg_mapping(p, e)

    def test_next_extinf_cannot_replace_missing_stream_uri(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "playlist.m3u8"
            e = Path(d) / "xmltv.xml"
            p.write_text('#EXTM3U\n#EXTINF:-1 tvg-id="trt1.tr",TRT 1\n#EXTINF:-1 tvg-id="other.tr",Other\nhttps://example.org/b.m3u8\n', encoding="utf-8")
            e.write_text('<tv><channel id="trt1.tr"/><channel id="other.tr"/></tv>', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing stream URI"):
                check_epg_mapping(p, e)
