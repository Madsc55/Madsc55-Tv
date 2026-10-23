import unittest

from madsc.trial_epg_audit import audit


class TrialEpgAuditTest(unittest.TestCase):
    def test_reports_empty_ids_and_real_programme_coverage(self):
        playlist = '#EXTINF:-1 tvg-id="a",TRT 1\n#EXTINF:-1,Unknown\n'
        xmltv = ('<tv><channel id="a"><display-name>TRT 1</display-name></channel>'
                 '<programme channel="a" start="20261023100000 +0000">'
                 '<title>News</title></programme></tv>')
        result = audit(playlist, xmltv)
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["empty_tvg_id"], 1)
        self.assertEqual(result["matched_with_programmes"], 1)
        self.assertEqual(result["matched_without_programmes"], 0)
        self.assertEqual(result["statuses"], {"existing_valid": 1, "unmatched": 1})

    def test_match_without_programmes_is_not_counted_as_guide(self):
        result = audit('#EXTINF:-1 tvg-id="a",TRT 1',
                       '<tv><channel id="a"/></tv>')
        self.assertEqual(result["matched_with_programmes"], 0)
        self.assertEqual(result["matched_without_programmes"], 1)


if __name__ == "__main__":
    unittest.main()
