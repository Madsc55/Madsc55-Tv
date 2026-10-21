import unittest
from madsc.channel_test import evaluate_probe, evaluate_repeated_probes, evaluate_ffprobe_json

class ChannelTests(unittest.TestCase):

    def test_three_stage_six_hour_preliminary_window(self):
        from madsc.channel_test import evaluate_three_stage_continuity
        base = {"url_sha256": "a" * 64, "http_status": 200,
                "video": True, "audio": True, "duration_seconds": 40}
        samples = [{**base, "observed_at": t} for t in
                   ("2026-10-21T10:00:00+00:00", "2026-10-21T13:00:00+00:00",
                    "2026-10-21T16:00:00+00:00")]
        result = evaluate_three_stage_continuity(samples)
        self.assertTrue(result["three_stage_six_hour_preliminary"])
        self.assertEqual(result["elapsed_hours"], 6)
        self.assertFalse(result["observation_provenance_verified"])
        self.assertFalse(result["stream_continuity_verified"])

    def test_three_stage_rejects_short_or_out_of_order_evidence(self):
        from madsc.channel_test import evaluate_three_stage_continuity
        base = {"url_sha256": "a" * 64, "http_status": 200,
                "video": True, "audio": True, "duration_seconds": 40}
        times = ("2026-10-21T10:00:00Z", "2026-10-21T11:00:00Z",
                 "2026-10-21T12:00:00Z")
        samples = [{**base, "observed_at": t} for t in times]
        self.assertFalse(evaluate_three_stage_continuity(samples)["three_stage_six_hour_preliminary"])
        with self.assertRaises(ValueError):
            evaluate_three_stage_continuity(list(reversed(samples)))
        with self.assertRaises(ValueError):
            evaluate_three_stage_continuity(samples[:2])


    def test_batch_continuity_reports_missing_candidates(self):
        from madsc.channel_test import summarize_candidate_continuity
        report = summarize_candidate_continuity(["a" * 64, "b" * 64], {})
        self.assertEqual(report["candidate_count"], 2)
        self.assertEqual(report["missing_count"], 2)
        self.assertEqual(report["preliminary_window_passes"], 0)
        self.assertFalse(report["production_change_allowed"])

    def test_batch_continuity_rejects_orphan_fingerprint(self):
        from madsc.channel_test import summarize_candidate_continuity
        with self.assertRaises(ValueError):
            summarize_candidate_continuity(["a" * 64], {"b" * 64: []})


    def test_batch_continuity_rejects_invalid_fingerprint_types(self):
        from madsc.channel_test import summarize_candidate_continuity
        for candidates, measurements in (([[]], {}), (["a" * 64], {1: []}),
                                         (["a" * 64, "a" * 64], {})):
            with self.subTest(candidates=candidates, measurements=measurements):
                with self.assertRaises(ValueError):
                    summarize_candidate_continuity(candidates, measurements)


    def test_bulk_candidate_selection_is_stable(self):
        from pathlib import Path
        source = Path("madsc/turkish_tv_batch_validation.py").read_text(encoding="utf-8")
        self.assertIn('sorted(found.items(), key=lambda item: item[0])[:MAX_PROBES]', source)
        self.assertIn('"selected_candidate_sha256"', source)


    def test_bulk_discovery_retains_source_provenance(self):
        from pathlib import Path
        source = Path("madsc/turkish_tv_batch_validation.py").read_text(encoding="utf-8")
        self.assertIn('source_by_digest.setdefault(key, set()).add(name)', source)
        self.assertIn('"source_names": sorted(source_by_digest[digest])', source)
        self.assertIn('"source_provenance_declared_only": True', source)


    def test_bulk_source_failures_are_reported(self):
        from pathlib import Path
        source = Path("madsc/turkish_tv_batch_validation.py").read_text(encoding="utf-8")
        self.assertIn('source_errors[name] = "source_scan_failed"', source)
        self.assertIn('"source_failures_count": len(source_errors)', source)


    def test_bulk_discovery_has_fingerprint_and_excludes_failed_scans(self):
        from pathlib import Path
        source = Path("madsc/turkish_tv_batch_validation.py").read_text(encoding="utf-8")
        self.assertIn('discovery_fingerprint_sha256', source)
        self.assertIn('if not eligible_source(name) or error is not None:', source)

    def test_success_is_not_device_approval(self):
        result = evaluate_probe({"url_sha256":"a"*64,"http_status":200,"video":True,
                                 "audio":True,"duration_seconds":60})
        self.assertEqual(result["technical_status"], "PRELIMINARY_PASS")
        self.assertFalse(result["ibo_device_verified"])
        self.assertFalse(result["channel_identity_verified"])
        self.assertFalse(result["stream_continuity_verified"])
        self.assertFalse(result["production_change_allowed"])
    def test_nonfinite_duration_rejected(self):
        for duration in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=str(duration)):
                probe = {"url_sha256": "a" * 64, "http_status": 200,
                         "video": True, "audio": True, "duration_seconds": duration}
                with self.assertRaises(ValueError):
                    evaluate_probe(probe)

    def test_invalid_probe_types_fail_closed(self):
        valid = {"url_sha256": "a" * 64, "http_status": 200,
                 "video": True, "audio": True, "duration_seconds": 40}
        for invalid in (None, [], "invalid", {**valid, "video": "yes"},
                        {**valid, "audio": 1}, {**valid, "duration_seconds": True}):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    evaluate_probe(invalid)

    def test_missing_evidence_fails_closed(self):
        with self.assertRaises(ValueError):
            evaluate_probe({"http_status":200})

    def test_repeated_probe_evidence_is_not_live_claim(self):
        probe = {"url_sha256": "a" * 64, "http_status": 200,
                 "video": True, "audio": True, "duration_seconds": 40}
        result = evaluate_repeated_probes([probe, probe])
        self.assertTrue(result["stable_preliminary"])
        self.assertFalse(result["actual_network_measurements_verified"])
        self.assertFalse(result["production_change_allowed"])

    def test_repeated_probe_rejects_mixed_streams(self):
        a = {"url_sha256": "a" * 64, "http_status": 200,
             "video": True, "audio": True, "duration_seconds": 40}
        with self.assertRaises(ValueError):
            evaluate_repeated_probes([a, {**a, "url_sha256": "b" * 64}])

    def test_ffprobe_json_parser_is_conservative(self):
        payload = {"streams": [{"codec_type": "video"}, {"codec_type": "audio"}],
                   "format": {"duration": "42.5"}}
        result = evaluate_ffprobe_json(payload, "a" * 64)
        self.assertEqual(result["technical_status"], "PRELIMINARY_PASS")
        self.assertFalse(result["stream_continuity_verified"])
        self.assertFalse(result["live_probe_executed_by_this_function"])
        self.assertFalse(result["production_change_allowed"])

    def test_ffprobe_json_rejects_bad_duration(self):
        with self.assertRaises(ValueError):
            evaluate_ffprobe_json({"streams": [], "format": {"duration": "NaN"}}, "a" * 64)


    def test_ffprobe_streams_missing_audio_require_review(self):
        payload = {"streams": [{"codec_type": "video"}], "format": {"duration": "65"}}
        result = evaluate_ffprobe_json(payload, "a" * 64)
        self.assertEqual(result["technical_status"], "NEEDS_REVIEW")
        self.assertFalse(result["production_change_allowed"])
        self.assertFalse(result["ibo_device_verified"])

    def test_ffprobe_malformed_streams_fail_closed(self):
        for streams in (None, {}, [None], ["video"]):
            with self.subTest(streams=streams), self.assertRaises(ValueError):
                evaluate_ffprobe_json({"streams": streams}, "a" * 64)

    def test_repeated_probe_with_one_failure_is_not_stable(self):
        passing = {"url_sha256": "a" * 64, "http_status": 200,
                   "video": True, "audio": True, "duration_seconds": 40}
        failed = {**passing, "http_status": 503}
        result = evaluate_repeated_probes([passing, failed])
        self.assertFalse(result["stable_preliminary"])
        self.assertEqual(result["preliminary_passes"], 1)
        self.assertFalse(result["actual_network_measurements_verified"])

    def test_offline_probe_summary_mixed_results(self):
        from madsc.channel_test import summarize_offline_probe_evidence
        records = [
            {"url_sha256": "a" * 64, "ffprobe": {"streams": [{"codec_type": "video"}, {"codec_type": "audio"}], "format": {"duration": "40"}}},
            {"url_sha256": "b" * 64, "ffprobe": {"streams": [{"codec_type": "video"}], "format": {"duration": "40"}}},
        ]
        result = summarize_offline_probe_evidence(records)
        self.assertEqual((result["channel_count"], result["preliminary_passes"], result["needs_review"]), (2, 1, 1))
        self.assertFalse(result["network_probed"])
        self.assertFalse(result["production_ready"])

    def test_offline_probe_summary_duplicate_rejected(self):
        from madsc.channel_test import summarize_offline_probe_evidence
        record = {"url_sha256": "a" * 64, "ffprobe": {"streams": [], "format": {}}}
        with self.assertRaises(ValueError):
            summarize_offline_probe_evidence([record, record])
