"""K3 snapshot regression tests: bounded probes, full source identity."""
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from madsc import k3_live_manifest_pilot as pilot
from madsc.live_discovery_pilot import MAX_BYTES


class K3SourceSnapshotTests(unittest.TestCase):
    def test_byte_limits_match_k2(self):
        self.assertEqual(pilot.SOURCE_MAX_BYTES, MAX_BYTES)

    def test_k3_hashes_full_source_and_probes_at_most_twelve(self):
        data = b"#EXTM3U\n" + b"".join(
            f"#EXTINF:-1,Example {i}\nhttps://example.org/live/{i}\n".encode()
            for i in range(25))
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, size): return data[:size]
        with TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            def fake_write(_root, path, content):
                (root / path).write_text(content)
            with (patch.object(pilot, "urlopen", return_value=Response()),
                  patch.object(pilot, "probe", return_value={
                      "url_sha256": "a" * 64, "hls_manifest_seen": False}),
                  patch.object(pilot, "write_fixture_report", side_effect=fake_write),
                  patch.object(pilot.Path, "cwd", return_value=root)):
                pilot.run()
            report = json.loads((root / "reports/k3-real-manifest-pilot.json").read_text())
            self.assertEqual(report["source_sha256"], hashlib.sha256(data).hexdigest())
            self.assertEqual(report["source_bytes"], len(data))
            self.assertEqual(report["probed"], pilot.LIMIT)
            self.assertFalse(report["production_playlist_modified"])

    def test_duplicate_urls_only_probed_once(self):
        data = (b"#EXTM3U\n" +
                b"#EXTINF:-1,One\nhttps://example.org/one\n" * 15 +
                b"#EXTINF:-1,Two\nhttps://example.org/two\n")
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, size): return data[:size]
        with TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            def fake_write(_root, path, content):
                (root / path).write_text(content)
            with (patch.object(pilot, "urlopen", return_value=Response()),
                  patch.object(pilot, "probe", side_effect=lambda url: {
                      "url_sha256": hashlib.sha256(url.encode()).hexdigest(),
                      "hls_manifest_seen": False}) as probe_mock,
                  patch.object(pilot, "write_fixture_report", side_effect=fake_write),
                  patch.object(pilot.Path, "cwd", return_value=root)):
                pilot.run()
            report = json.loads((root / "reports/k3-real-manifest-pilot.json").read_text())
            self.assertEqual(report["probed"], 2)
            self.assertEqual(probe_mock.call_count, 2)
            self.assertEqual(len({r["url_sha256"] for r in report["results"]}), 2)

    def test_normalized_url_identity_matches_k2_and_skips_invalid(self):
        from madsc.discovery import classify_candidates
        from madsc.remote_m3u_parser import parse_remote_m3u
        data = (b"#EXTM3U\n"
                b"#EXTINF:-1,One\nHTTPS://EXAMPLE.ORG/live\n"
                b"#EXTINF:-1,Same\nhttps://example.org/live\n"
                b"#EXTINF:-1,Invalid\nftp://example.org/live\n"
                b"#EXTINF:-1,Two\nhttps://example.org/two\n")
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, size): return data[:size]
        expected = classify_candidates(parse_remote_m3u(data, max_bytes=pilot.SOURCE_MAX_BYTES))
        hashes = {item["url_sha256"] for item in expected["candidates"]}
        with TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            def fake_write(_root, path, content):
                (root / path).write_text(content)
            with (patch.object(pilot, "urlopen", return_value=Response()),
                  patch.object(pilot, "probe", side_effect=lambda url: {
                      "url_sha256": hashlib.sha256(url.encode()).hexdigest(),
                      "hls_manifest_seen": False}) as probe_mock,
                  patch.object(pilot, "write_fixture_report", side_effect=fake_write),
                  patch.object(pilot.Path, "cwd", return_value=root)):
                pilot.run()
            report = json.loads((root / "reports/k3-real-manifest-pilot.json").read_text())
            self.assertEqual(report["probed"], 2)
            self.assertEqual(probe_mock.call_count, 2)
            self.assertEqual({item["url_sha256"] for item in report["results"]}, hashes)

    def test_http_entries_do_not_consume_https_probe_budget(self):
        data = (b"#EXTM3U\n" +
                b"".join(f"#EXTINF:-1,HTTP {i}\nhttp://example.org/{i}\n".encode()
                         for i in range(15)) +
                b"#EXTINF:-1,HTTPS\nhttps://example.org/valid\n")
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, size): return data[:size]
        with TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            def fake_write(_root, path, content):
                (root / path).write_text(content)
            with (patch.object(pilot, "urlopen", return_value=Response()),
                  patch.object(pilot, "probe", side_effect=lambda url: {
                      "url_sha256": hashlib.sha256(url.encode()).hexdigest(),
                      "hls_manifest_seen": False}) as probe_mock,
                  patch.object(pilot, "write_fixture_report", side_effect=fake_write),
                  patch.object(pilot.Path, "cwd", return_value=root)):
                pilot.run()
            report = json.loads((root / "reports/k3-real-manifest-pilot.json").read_text())
            self.assertEqual(report["probed"], 1)
            probe_mock.assert_called_once_with("https://example.org/valid")

    def test_k3_rejects_oversize_source(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, size): return b"#EXTM3U\n" + b"x" * (size + 1)
        with patch.object(pilot, "urlopen", return_value=Response()):
            with self.assertRaises(ValueError):
                list(pilot.candidates())


if __name__ == "__main__":
    unittest.main()
