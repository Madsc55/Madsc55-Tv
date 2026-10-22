"""K5 offline fixture regression for frozen legacy IBO group-count rewrite.

No legacy scripts are executed; no production playlist is opened or changed.
"""
import re
import unittest


class K5LegacyIboCountPatternTests(unittest.TestCase):
    def test_double_escaped_legacy_pattern_does_not_match_real_group(self):
        source_line = '#EXTINF:-1 group-title="📦 YEDEKLER (6115)",Example\n'
        frozen_pattern = r'group-title="📦 YEDEKLER \\(\\d+\\)"'
        self.assertEqual(re.sub(frozen_pattern, 'group-title="📦 YEDEKLER (500)"', source_line), source_line)

    def test_corrected_pattern_rewrites_count_only(self):
        source_line = '#EXTINF:-1 tvg-id="one" group-title="📦 YEDEKLER (6115)",Example\n'
        corrected = r'group-title="📦 YEDEKLER \(\d+\)"'
        actual, matches = re.subn(corrected, 'group-title="📦 YEDEKLER (500)"', source_line)
        self.assertEqual(matches, 1)
        self.assertEqual(actual, '#EXTINF:-1 tvg-id="one" group-title="📦 YEDEKLER (500)",Example\n')

    def test_corrected_pattern_leaves_unrelated_groups_untouched(self):
        line = '#EXTINF:-1 group-title="🇹🇷 TURKIYE (6115)",News\n'
        actual, matches = re.subn(r'group-title="📦 YEDEKLER \(\d+\)"', 'group-title="📦 YEDEKLER (500)"', line)
        self.assertEqual(matches, 0)
        self.assertEqual(actual, line)


if __name__ == "__main__":
    unittest.main()
