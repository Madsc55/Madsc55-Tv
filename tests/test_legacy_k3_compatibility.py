import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from madsc.legacy_epg_logo import join_pilot
from madsc.legacy_retest_390 import evaluate_entries, parse_entries


class LegacyK3CompatibilityTests(unittest.TestCase):
    def test_epg_logo_pilot_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            xml = Path(tmp) / "pilot.xml"
            xml.write_text('<tv><channel id="a"/><channel id="b"/>'
                           '<programme channel="a"/></tv>', encoding="utf-8")
            original = xml.read_bytes()
            report = join_pilot([
                {"channel": "A", "channel_id": "a", "stream_sha256": "x"},
                {"channel": "B", "channel_id": "b", "stream_sha256": "y"},
                {"channel": "C", "channel_id": "c", "stream_sha256": "z"}],
                [{"stream_sha256": "x", "status": "PREPARED"}], xml)
            self.assertEqual([r["epg_pilot_status"] for r in report["candidate_results"]],
                             ["PILOT_MATCH_WITH_PROGRAMMES", "PILOT_ID_NO_PROGRAMMES",
                              "NOT_IN_FIVE_CHANNEL_PILOT"])
            self.assertEqual(report["candidate_results"][0]["logo_status"], "PREPARED")
            self.assertTrue(all(not r["playlist_approved"] and not r["ready_for_playlist"]
                                for r in report["candidate_results"]))
            self.assertFalse(report["production_ready"])
            self.assertEqual(original, xml.read_bytes())

    def test_390_contract_without_network(self):
        calls = []
        def fake(args, **kwargs):
            calls.append((args, kwargs))
            return SimpleNamespace(returncode=0, stderr="",
                                   stdout="video\naudio\n" if args[0] == "ffprobe" else "")
        rows = parse_entries("#EXTM3U\n#EXTINF:-1,Sample\nhttps://example.invalid/a\n")
        result = evaluate_entries(rows, runner=fake, workers=2)
        self.assertEqual(result["technical_pass_count"], 1)
        self.assertEqual([x[1]["timeout"] for x in calls], [22, 45])
        self.assertIn("20", calls[1][0])
        self.assertFalse(result["production_ready"])
        self.assertFalse(result["identity_verified"])

    def test_390_missing_audio_is_rejected(self):
        def fake(args, **kwargs):
            return SimpleNamespace(returncode=0, stdout="video\n", stderr="")
        result = evaluate_entries(parse_entries("#EXTM3U\n#EXTINF:-1,No Audio\nhttp://example.invalid/b"),
                                  runner=fake)
        self.assertEqual(result["technical_pass_count"], 0)
        self.assertEqual(result["technical_m3u"], "#EXTM3U\n")


    def test_logo_join_uses_digest_not_channel_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            xml = Path(tmp) / "pilot.xml"
            xml.write_text('<tv><channel id="match"/><programme channel="match"/></tv>',
                           encoding="utf-8")
            report = join_pilot(
                [{"channel": "Same Name", "channel_id": "match", "stream_sha256": "digest-a"},
                 {"channel": "Same Name", "channel_id": "missing", "stream_sha256": "digest-b"}],
                [{"stream_sha256": "digest-b", "status": "PREPARED",
                  "visual_match": "NOT_VERIFIED"}], xml)
            a, b = report["candidate_results"]
            self.assertEqual(a["logo_status"], "NOT_PREPARED")
            self.assertEqual(b["logo_status"], "PREPARED")
            self.assertEqual(a["epg_pilot_status"], "PILOT_MATCH_WITH_PROGRAMMES")
            self.assertEqual(b["epg_pilot_status"], "NOT_IN_FIVE_CHANNEL_PILOT")
            self.assertFalse(report["production_writes"])
            self.assertFalse(report["ibo_device_verified"])

    def test_390_decode_failure_is_not_promoted(self):
        calls = []
        def fake(args, **kwargs):
            calls.append(args[0])
            return SimpleNamespace(returncode=1 if args[0] == "ffmpeg" else 0,
                                   stdout="video\naudio\n", stderr="decode error")
        rows = parse_entries("#EXTM3U\n#EXTINF:-1,Fail\nhttps://example.invalid/stream")
        report = evaluate_entries(rows, runner=fake, workers=1)
        self.assertEqual(calls, ["ffprobe", "ffmpeg"])
        self.assertEqual(report["technical_pass_count"], 0)
        self.assertEqual(report["technical_m3u"], "#EXTM3U\n")
        self.assertIn("decode error", report["csv_text"])
        self.assertFalse(report["production_ready"])

    def test_390_probe_exception_stays_failed(self):
        def broken(args, **kwargs):
            raise TimeoutError("fixture timeout")
        rows = parse_entries("#EXTM3U\n#EXTINF:-1,Timeout\nhttps://example.invalid/stream")
        report = evaluate_entries(rows, runner=broken, workers=1)
        self.assertEqual(report["technical_pass_count"], 0)
        self.assertIn("fixture timeout", report["csv_text"])
        self.assertFalse(report["identity_verified"])

    def test_worker_cap_and_invalid_xml(self):
        with self.assertRaises(ValueError):
            evaluate_entries([], workers=13)
        with tempfile.TemporaryDirectory() as tmp:
            xml = Path(tmp) / "invalid.xml"
            xml.write_text("<other/>", encoding="utf-8")
            with self.assertRaises(ValueError):
                join_pilot([], [], xml)
