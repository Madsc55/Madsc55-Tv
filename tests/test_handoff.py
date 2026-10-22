import unittest
from hashlib import sha256
from madsc.discovery import classify_candidates
from madsc.handoff import assess_candidates

class HandoffTests(unittest.TestCase):

    def test_k2_alternative_stream_not_duplicate_url(self):
        report = classify_candidates([
            {"name": "TRT 1", "url": "https://example.org/a.m3u8", "tvg_id": "trt1"},
            {"name": "TRT 1 HD", "url": "https://example.org/b.m3u8", "tvg_id": "trt1"},
            {"name": "TRT 1", "url": "https://example.org/a.m3u8", "tvg_id": "trt1"},
        ])
        self.assertEqual(len(report["candidates"]), 2)
        self.assertEqual(len(report["duplicates"]), 1)
        self.assertEqual(len(report["alternatives"]), 1)
        self.assertEqual(report["alternatives"][0]["alternative_to_sha256"],
                         report["candidates"][0]["url_sha256"])
        self.assertFalse(report["production_playlist_modified"])

    def test_k2_distinct_channel_identities_are_not_alternatives(self):
        report = classify_candidates([
            {"name": "A", "url": "https://example.org/a", "tvg_id": "a"},
            {"name": "B", "url": "https://example.org/b", "tvg_id": "b"},
        ])
        self.assertEqual(report["alternatives"], [])


    def test_k2_k3_handoff_keeps_alternative_stream_relationship(self):
        discovery = classify_candidates([
            {"name": "TRT 1", "url": "https://example.org/a", "tvg_id": "trt1"},
            {"name": "TRT 1 HD", "url": "https://example.org/b", "tvg_id": "trt1"},
        ])
        report = assess_candidates(discovery, {})
        primary, alternative = report["assessed"]
        self.assertIsNone(primary["alternative_to_sha256"])
        self.assertEqual(alternative["alternative_to_sha256"], primary["url_sha256"])
        self.assertEqual(alternative["technical_status"], "UNTESTED")
        self.assertFalse(alternative["production_change_allowed"])


    def test_k2_alternative_relation_survives_k3_handoff(self):
        discovery = classify_candidates([
            {"name": "TRT 1", "url": "https://example.org/a", "tvg_id": "trt1"},
            {"name": "TRT 1 HD", "url": "https://example.org/b", "tvg_id": "trt1"},
        ])
        report = assess_candidates(discovery, {})
        first, second = report["assessed"]
        self.assertIsNone(first["alternative_to_sha256"])
        self.assertEqual(second["alternative_to_sha256"], first["url_sha256"])
        self.assertEqual(second["technical_status"], "UNTESTED")
        self.assertFalse(second["production_change_allowed"])

    def test_orphan_alternative_relation_fails_closed(self):
        discovery = classify_candidates([{"name": "TRT 1", "url": "https://example.org/a"}])
        discovery["alternatives"] = [{
            "url_sha256": "f" * 64,
            "alternative_to_sha256": discovery["candidates"][0]["url_sha256"],
        }]
        with self.assertRaises(ValueError):
            assess_candidates(discovery, {})


    def test_k2_duplicate_provenance_is_explicit(self):
        rows = [
            {"name": "A", "url": "https://example.org/a"},
            {"name": "A again", "url": "https://example.org/a"},
            {"name": "B", "url": "https://example.org/b"},
        ]
        result = classify_candidates(rows, known_urls={"https://example.org/b"})
        self.assertEqual(len(result["candidates"]), 1)
        self.assertEqual([item["duplicate_reason"] for item in result["duplicates"]],
                         ["same_batch", "already_known"])
        self.assertFalse(result["production_playlist_modified"])

    def test_k2_invalid_known_url_container_fails_closed(self):
        with self.assertRaises(ValueError):
            classify_candidates([], known_urls=["https://example.org/a"])


    def test_k3_continuity_is_attached_to_candidate_without_production_approval(self):
        discovery = classify_candidates([{"name": "A", "url": "https://example.org/a"}])
        digest = discovery["candidates"][0]["url_sha256"]
        base = {"url_sha256": digest, "http_status": 200,
                "video": True, "audio": True, "duration_seconds": 40}
        samples = [{**base, "observed_at": stamp} for stamp in
                   ("2026-10-21T10:00:00Z", "2026-10-21T13:00:00Z",
                    "2026-10-21T16:00:00Z")]
        report = assess_candidates(discovery, {}, continuity_samples={digest: samples})
        item = report["assessed"][0]
        self.assertTrue(item["continuity"]["three_stage_six_hour_preliminary"])
        self.assertFalse(item["continuity"]["observation_provenance_verified"])
        self.assertFalse(item["production_change_allowed"])

    def test_k3_continuity_rejects_orphan_and_mismatched_fingerprints(self):
        discovery = classify_candidates([{"name": "A", "url": "https://example.org/a"}])
        digest = discovery["candidates"][0]["url_sha256"]
        base = {"url_sha256": "f" * 64, "http_status": 200,
                "video": True, "audio": True, "duration_seconds": 40}
        samples = [{**base, "observed_at": stamp} for stamp in
                   ("2026-10-21T10:00:00Z", "2026-10-21T13:00:00Z",
                    "2026-10-21T16:00:00Z")]
        with self.assertRaises(ValueError):
            assess_candidates(discovery, {}, continuity_samples={digest: samples})
        with self.assertRaises(ValueError):
            assess_candidates(discovery, {}, continuity_samples={"f" * 64: samples})


    def test_cross_channel_alternative_relation_is_rejected(self):
        discovery = classify_candidates([
            {"name": "A", "url": "https://example.org/a", "tvg_id": "a"},
            {"name": "B", "url": "https://example.org/b", "tvg_id": "b"},
        ])
        first, second = discovery["candidates"]
        discovery["alternatives"] = [{
            **second, "alternative_to_sha256": first["url_sha256"],
        }]
        with self.assertRaises(ValueError):
            assess_candidates(discovery, {})

    def test_unprobed_candidate_is_untested(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        result = assess_candidates(discovery, {})
        self.assertEqual(result["assessed"][0]["technical_status"], "UNTESTED")
        self.assertFalse(result["assessed"][0]["ibo_device_verified"])
        self.assertFalse(result["assessed"][0]["ibo_result_supplied"])
        self.assertFalse(result["production_playlist_modified"])
    def test_valid_probe_is_not_production_approval(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        digest = discovery["candidates"][0]["url_sha256"]
        result = assess_candidates(discovery, {digest: {"url_sha256": digest, "http_status": 200,
                                   "video": True, "audio": True, "duration_seconds": 40}})
        self.assertEqual(result["assessed"][0]["technical_status"], "PRELIMINARY_PASS")
        self.assertFalse(result["assessed"][0]["production_change_allowed"])
    def test_mismatched_probe_rejected(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        digest = discovery["candidates"][0]["url_sha256"]
        with self.assertRaises(ValueError):
            assess_candidates(discovery, {digest: {"url_sha256": "a" * 64, "http_status": 200,
                                "video": True, "audio": True, "duration_seconds": 40}})

    def test_ibo_working_remains_protected_after_failed_probe(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        digest = discovery["candidates"][0]["url_sha256"]
        failed = {"url_sha256": digest, "http_status": 503, "video": False,
                  "audio": False, "duration_seconds": 0}
        result = assess_candidates(discovery, {digest: failed}, {digest: "WORKING"})
        entry = result["assessed"][0]
        self.assertEqual(entry["technical_status"], "NEEDS_REVIEW")
        self.assertEqual(entry["ibo_result"], "WORKING")
        self.assertTrue(entry["protected_working"])
        self.assertFalse(entry["ibo_device_verified"])
        self.assertTrue(entry["ibo_result_supplied"])
        self.assertFalse(entry["delete_allowed"])
        self.assertFalse(entry["production_change_allowed"])
    def test_invalid_handoff_shapes_fail_closed(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        for invalid in (None, [], "bad"):
            with self.subTest(probes=invalid), self.assertRaises(ValueError):
                assess_candidates(discovery, invalid)
            if invalid is not None:
                with self.subTest(ibo=invalid), self.assertRaises(ValueError):
                    assess_candidates(discovery, {}, invalid)
        for invalid in (None, [], {"candidates": None}, {"candidates": [None]}):
            with self.subTest(discovery=invalid), self.assertRaises(ValueError):
                assess_candidates(invalid, {})

    def test_invalid_fingerprint_length_fails_closed(self):
        with self.assertRaises(ValueError):
            assess_candidates({"candidates": [{"url_sha256": "bad"}]}, {})

    def test_nonhex_fingerprint_fails_closed(self):
        for invalid in ("z" * 64, "G" * 64, " " * 64):
            with self.subTest(value=invalid), self.assertRaises(ValueError):
                assess_candidates({"candidates": [{"url_sha256": invalid}]}, {})

    def test_invalid_probe_record_fails_closed(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        digest = discovery["candidates"][0]["url_sha256"]
        with self.assertRaises(ValueError):
            assess_candidates(discovery, {digest: []})

    def test_invalid_ibo_evidence_fails_closed(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        digest = discovery["candidates"][0]["url_sha256"]
        with self.assertRaises(ValueError):
            assess_candidates(discovery, {}, {digest: "ASSUMED_WORKING"})
    def test_tvg_id_survives_handoff_and_ibo_working_is_protected(self):
        discovery = classify_candidates([{"name": "TRT", "url": "https://example.org/live", "tvg_id": "trt.tv"}])
        digest = discovery["candidates"][0]["url_sha256"]
        result = assess_candidates(discovery, {}, {digest: "WORKING"})
        item = result["assessed"][0]
        self.assertEqual(item["tvg_id"], "trt.tv")
        self.assertTrue(item["protected_working"])
        self.assertFalse(item["delete_allowed"])

    def test_duplicate_fingerprints_and_bad_metadata_fail_closed(self):
        discovery = classify_candidates([{"name": "TRT", "url": "https://example.org/live"}])
        item = discovery["candidates"][0]
        with self.assertRaises(ValueError):
            assess_candidates({"candidates": [item, item]}, {})
        with self.assertRaises(ValueError):
            assess_candidates({"candidates": [{**item, "tvg_id": []}]}, {})
    def test_display_metadata_survives_k2_to_k3(self):
        discovery = classify_candidates([{"name": "TRT 1", "url": "https://example.org/live.m3u8",
            "tvg_id": "trt1", "tvg_logo": "https://example.org/logo.png", "group_title": "Haber"}])
        item = assess_candidates(discovery, {})["assessed"][0]
        self.assertEqual(item["name"], "TRT 1")
        self.assertEqual(item["tvg_id"], "trt1")
        self.assertEqual(item["tvg_logo"], "https://example.org/logo.png")
        self.assertEqual(item["group_title"], "Haber")
        self.assertFalse(item["production_change_allowed"])

    def test_invalid_display_metadata_is_rejected(self):
        discovery = classify_candidates([{"name": "TRT", "url": "https://example.org/live"}])
        for field in ("name", "tvg_logo", "group_title"):
            with self.subTest(field=field), self.assertRaises(ValueError):
                assess_candidates({"candidates": [{**discovery["candidates"][0], field: []}]}, {})

    def test_orphan_probe_and_ibo_evidence_fail_closed(self):
        discovery = classify_candidates([{"name": "Sample", "url": "https://example.org/live.m3u8"}])
        orphan = 'f' * 64
        with self.assertRaises(ValueError):
            assess_candidates(discovery, {orphan: {"url_sha256": orphan}})
        with self.assertRaises(ValueError):
            assess_candidates(discovery, {}, {orphan: "WORKING"})


    def test_mixed_candidates_keep_ibo_evidence_isolated_by_fingerprint(self):
        discovery = classify_candidates([
            {"name": "A", "url": "https://example.org/a.m3u8"},
            {"name": "B", "url": "https://example.org/b.m3u8"},
        ])
        a, b = (entry["url_sha256"] for entry in discovery["candidates"])
        probes = {
            a: {"url_sha256": a, "http_status": 503, "video": False,
                "audio": False, "duration_seconds": 0},
            b: {"url_sha256": b, "http_status": 200, "video": True,
                "audio": True, "duration_seconds": 40},
        }
        report = assess_candidates(discovery, probes, {a: "WORKING"})
        by_digest = {item["url_sha256"]: item for item in report["assessed"]}
        self.assertEqual(by_digest[a]["technical_status"], "NEEDS_REVIEW")
        self.assertTrue(by_digest[a]["protected_working"])
        self.assertFalse(by_digest[a]["delete_allowed"])
        self.assertEqual(by_digest[b]["technical_status"], "PRELIMINARY_PASS")
        self.assertFalse(by_digest[b]["ibo_result_supplied"])
        self.assertFalse(by_digest[b]["production_change_allowed"])
        self.assertFalse(report["production_playlist_modified"])
        self.assertFalse(report["network_probed"])

    def test_empty_discovery_rejects_unlinked_ibo_evidence(self):
        orphan = "f" * 64
        with self.assertRaises(ValueError):
            assess_candidates({"candidates": []}, {}, {orphan: "WORKING"})

    def test_alternative_chain_and_reverse_mapping_rejected(self):
        discovery = classify_candidates([
            {"name": "News", "url": "https://example.org/a", "tvg_id": "news"},
            {"name": "News HD", "url": "https://example.org/b", "tvg_id": "news"},
            {"name": "News Backup", "url": "https://example.org/c", "tvg_id": "news"},
        ])
        a, b, c = [item["url_sha256"] for item in discovery["candidates"]]
        for child, parent in ((c, b), (a, b)):
            with self.subTest(child=child, parent=parent):
                tampered = dict(discovery)
                tampered["alternatives"] = [
                    {"url_sha256": child, "alternative_to_sha256": parent}
                ]
                with self.assertRaisesRegex(ValueError, "Conflicting alternative channel identity"):
                    assess_candidates(tampered, {})


    def test_unsafe_tvg_ids_rejected_at_handoff(self):
        discovery = classify_candidates([
            {"name": "News", "url": "https://example.org/a", "tvg_id": "news"}
        ])
        for unsafe in ("news\\\\bad", "news\\nmore", "news\\x7f"):
            with self.subTest(unsafe=repr(unsafe)):
                altered = dict(discovery)
                altered["candidates"] = [dict(discovery["candidates"][0], tvg_id=unsafe)]
                with self.assertRaisesRegex(ValueError, "Unsafe candidate tvg-id"):
                    assess_candidates(altered, {})


    def test_unsafe_display_metadata_rejected_at_handoff(self):
        discovery = classify_candidates([
            {"name": "News", "url": "https://example.org/a", "tvg_id": "news"}
        ])
        for field, value in (("name", " "), ("name", "News\\nExtra"),
                             ("tvg_logo", "logo\\\\path"),
                             ("group_title", "group\\x7f")):
            with self.subTest(field=field, value=repr(value)):
                altered = dict(discovery)
                altered["candidates"] = [dict(discovery["candidates"][0], **{field: value})]
                with self.assertRaisesRegex(ValueError, "Unsafe candidate display metadata"):
                    assess_candidates(altered, {})


    def test_direct_handoff_rejects_oversized_discovery(self):
        candidate = classify_candidates([
            {"name": "News", "url": "https://example.org/a"}
        ])["candidates"][0]
        with self.assertRaisesRegex(ValueError, "Too many candidates"):
            assess_candidates({"candidates": [candidate] * 20001}, {})
        with self.assertRaisesRegex(ValueError, "Too many alternatives"):
            assess_candidates({"candidates": [], "alternatives": [{}] * 20001}, {})

