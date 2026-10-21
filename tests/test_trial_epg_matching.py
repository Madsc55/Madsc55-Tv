import unittest
from madsc.trial_epg_matching import matches, playlist_entries

XML = '<tv><channel id="a"><display-name>TRT 1</display-name></channel><channel id="b"><display-name>TV 8</display-name></channel><channel id="c"><display-name>TV-8</display-name></channel></tv>'
class TrialEpgMatchingTest(unittest.TestCase):
    def test_exact_and_ambiguous_and_unmatched(self):
        m = '#EXTM3U\n#EXTINF:-1,TRT 1\nhttps://example.org/a.m3u8\n#EXTINF:-1,TV8\nhttps://example.org/b.m3u8\n#EXTINF:-1,Unknown\nhttps://example.org/c.m3u8\n'
        result = matches(m, XML)
        self.assertEqual([x["status"] for x in result], ["exact_unique", "ambiguous", "unmatched"])
        self.assertEqual(result[0]["matched_id"], "a")
        self.assertEqual(result[1]["matched_id"], "")
    def test_existing_id(self):
        self.assertEqual(matches('#EXTINF:-1 tvg-id="a",Other', XML)[0]["status"], "existing_valid")
    def test_empty(self):
        self.assertEqual(playlist_entries("#EXTM3U"), [])
if __name__ == "__main__":
    unittest.main()
