import unittest
from madsc.remote_m3u_parser import parse_remote_m3u


class RemoteM3UParserTests(unittest.TestCase):
    def test_quoted_commas_and_channel_names(self):
        raw = b'#EXTM3U\n#EXTINF:-1 group-title="News, TR",TRT 1, HD\nhttps://example.org/live\n'
        self.assertEqual(parse_remote_m3u(raw, max_bytes=1000),
                         [{"name": "TRT 1, HD", "url": "https://example.org/live"}])

    def test_bounded_and_unpaired_inputs(self):
        for raw in (b"#EXTM3U\n#EXTINF:-1,Orphan\n",
                    b"#EXTM3U\nhttps://example.org/live\n",
                    b"bad\n", b"#EXTM3U\n#EXTINF:-1,\nhttps://example.org/live\n"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                parse_remote_m3u(raw, max_bytes=1000)
        with self.assertRaises(ValueError):
            parse_remote_m3u(b"#EXTM3U\n", max_bytes=3)


if __name__ == "__main__":
    unittest.main()
