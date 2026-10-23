import unittest
import tempfile
from pathlib import Path
from madsc.write_path_audit import (audit_write_paths, enforce_write_paths,
                                    enforce_local_output_path,
                                    enforce_local_append_path,
                                    enforce_local_turkish_tv_test_playlist,
                                    ProtectedWriteRejected)

class WritePathAuditTests(unittest.TestCase):
    def test_unicode_noncharacters_are_rejected_without_writes(self):
        for suffix in ("\ufdd0", "\ufffe", "\U0001fffe", "\U0010ffff"):
            with self.subTest(codepoint=hex(ord(suffix))):
                path = "reports/evidence" + suffix + ".json"
                result = audit_write_paths([path])
                self.assertEqual(result["rejected"], [path])
                self.assertFalse(result["write_performed"])
                with self.assertRaises(ProtectedWriteRejected):
                    enforce_write_paths([path])

    def test_protected_paths_blocked(self):
        report = audit_write_paths(["CALISANLAR.m3u", "epg/sample.xml", "logolar/a.png"])
        self.assertTrue(report["blocked"])
        self.assertEqual(len(report["rejected"]), 3)
        self.assertFalse(report["write_performed"])
        self.assertFalse(report["runtime_gate_enforced"])

    def test_main_xmltv_and_playlist_are_protected_at_any_depth(self):
        paths = ["xmltv.xml", "XMLTV.XML", "nested/xmltv.xml",
                 "playlist.m3u8", "nested/PLAYLIST.M3U8"]
        result = audit_write_paths(paths)
        self.assertEqual(result["rejected"], paths)
        with self.assertRaises(ProtectedWriteRejected):
            enforce_write_paths(["reports/ok.json", "xmltv.xml"])

    def test_unprotected_report_path(self):
        report = audit_write_paths(["reports/sample.json"])
        self.assertFalse(report["blocked"])

    def test_traversal_rejected(self):
        for path in ("../CALISANLAR.m3u", "/tmp/a", "a/../b", "a\\b"):
            with self.subTest(path=path):
                self.assertTrue(audit_write_paths([path])["blocked"])

    def test_legacy_exact_and_suffix_protection(self):
        report = audit_write_paths(["AGENTS.md", "CALISMAYANLAR.txt",
                                    "sample.m3u8", "nested/YENILER.m3u"])
        self.assertEqual(len(report["rejected"]), 4)

    def test_legacy_prefix_casefold_protection(self):
        report = audit_write_paths(["YEDEKLER/a.txt", "LoGoS/a.png",
                                    "ArSiV/sample.txt", "EPG/data.xml"])
        self.assertEqual(len(report["rejected"]), 4)
    def test_ambiguous_and_control_character_paths_blocked(self):
        paths = ["reports/a\x00.json", "reports/a\n.json", "reports/a\t.json",
                 "reports/file:stream", "reports/file. ", "reports/file.",
                 "~/reports.json", "reports/dir /file.json"]
        result = audit_write_paths(paths)
        self.assertTrue(result["blocked"])
        self.assertEqual(result["rejected"], paths)
        self.assertFalse(result["runtime_gate_enforced"])

    def test_unicode_compatibility_aliases_cannot_bypass_protection(self):
        paths = ["ＦＡＶＯＲＩＬＥＲ/channel.txt", "ＥＰＧ/guide.xml",
                 "reports/ＣＡＬＩＳＡＮＬＡＲ.m3u",
                 "reports/ＳＡＦＥ.json", "reports/SAFE.json"]
        result = audit_write_paths(paths)
        self.assertEqual(result["rejected"], paths[:3] + paths[4:])
        with self.assertRaises(ProtectedWriteRejected):
            enforce_write_paths(["ＦＡＶＯＲＩＬＥＲ/channel.txt"])

    def test_unicode_normalized_traversal_and_suffix_blocked(self):
        paths = ["reports/．．/safe.json", "reports/．/safe.json",
                 "reports/file．m3u8", "reports/file．m3u",
                 "reports/file．", "reports/dir／../safe.json"]
        result = audit_write_paths(paths)
        self.assertEqual(result["rejected"], paths)
        with self.assertRaises(ProtectedWriteRejected):
            enforce_write_paths(["reports/．．/safe.json"])

    def test_unicode_compatibility_backslash_is_rejected(self):
        paths = ["reports／safe.json", "reports＼safe.json",
                 "reports/ＥＰＧ＼guide.xml"]
        report = audit_write_paths(paths)
        self.assertEqual(report["rejected"], paths)
        with self.assertRaises(ProtectedWriteRejected):
            enforce_write_paths(["reports＼safe.json"])

    def test_c1_unicode_control_characters_are_rejected(self):
        paths = ["reports/unsafe\u0085name.json", "reports/unsafe\u009bname.json"]
        result = audit_write_paths(paths)
        self.assertEqual(result["rejected"], paths)
        with self.assertRaises(ProtectedWriteRejected):
            enforce_write_paths([paths[0]])

    def test_unicode_line_and_paragraph_separators_are_rejected(self):
        paths = ["reports/bad\u2028name.json", "reports/bad\u2029name.json"]
        result = audit_write_paths(paths)
        self.assertEqual(result["rejected"], paths)
        for path in paths:
            with self.subTest(path=repr(path)):
                with self.assertRaises(ProtectedWriteRejected):
                    enforce_write_paths([path])

    def test_nul_and_control_characters_are_rejected(self):
        paths = ["reports/bad" + chr(0) + ".json",
                 "reports/bad" + chr(10) + ".json",
                 "reports/safe.json"]
        result = audit_write_paths(paths)
        self.assertEqual(result["rejected"], paths[:2])
        with self.assertRaises(ProtectedWriteRejected):
            enforce_write_paths([paths[0]])

    def test_mixed_safe_and_unsafe_paths_do_not_clear_block(self):
        result = audit_write_paths(["reports/safe.json", "EPG/guide.xml"])
        self.assertTrue(result["blocked"])
        self.assertEqual(result["rejected"], ["EPG/guide.xml"])
    def test_nested_protected_exact_names_blocked(self):
        paths = ["docs/AGENTS.md", "nested/GUVENLIK_KURALLARI.md",
                 "reports/CALISMAYANLAR.txt", "nested/YENILER.m3u"]
        result = audit_write_paths(paths)
        self.assertEqual(result["rejected"], paths)
        self.assertTrue(result["blocked"])


    def test_duplicate_paths_rejected_fail_closed(self):
        result = audit_write_paths(["reports/safe.json", "reports/SAFE.json"])
        self.assertTrue(result["blocked"])
        self.assertEqual(result["rejected"], ["reports/SAFE.json"])
        self.assertFalse(result["write_performed"])

    def test_identical_paths_rejected_fail_closed(self):
        result = audit_write_paths(["reports/safe.json", "reports/safe.json"])
        self.assertTrue(result["blocked"])
        self.assertEqual(result["rejected"], ["reports/safe.json"])

    def test_enforcement_rejects_protected_write_before_side_effect(self):
        for path in ("CALISANLAR.m3u", "epg/guide.xml", "FAVORILER/list.txt",
                     "nested/../reports/output.json", "reports/x.m3u8"):
            with self.subTest(path=path):
                called = []
                with self.assertRaises(ProtectedWriteRejected):
                    enforce_write_paths([path])
                    called.append("write")
                self.assertEqual(called, [])

    def test_enforcement_allows_only_unprotected_report_paths(self):
        result = enforce_write_paths(["reports/legacy-audit.json"])
        self.assertTrue(result["runtime_gate_enforced"])
        self.assertFalse(result["write_performed"])
        self.assertEqual(result["checked_paths"], ["reports/legacy-audit.json"])

    def test_enforcement_fails_closed_on_mixed_paths(self):
        with self.assertRaises(ProtectedWriteRejected):
            enforce_write_paths(["reports/ok.json", "logos/channel.png"])

    def test_enforcement_rejects_duplicate_paths(self):
        with self.assertRaises(ProtectedWriteRejected):
            enforce_write_paths(["reports/a.json", "reports/A.json"])


class LocalOutputGuardTests(unittest.TestCase):
    def test_fixed_turkish_tv_playlist_exception_does_not_relax_general_guard(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            target = root / "reports/MADSC55_TURKCE_TV_ADAY_DENEME.m3u8"
            result = enforce_local_turkish_tv_test_playlist(target, allowed_root=root)
            self.assertTrue(result["isolated_test_playlist"])
            with self.assertRaises(ProtectedWriteRejected):
                enforce_local_output_path(target, allowed_root=root)
            with self.assertRaises(ProtectedWriteRejected):
                enforce_local_turkish_tv_test_playlist(
                    root / "reports/another.m3u8", allowed_root=root)

    def test_local_output_rejects_ambiguous_unicode_and_backslashes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for name in ("unsafe\\name.json", "unsafe\u0085name.json",
                         "unsafe\u2028name.json", "unsafe\u2029name.json"):
                with self.subTest(name=repr(name)):
                    with self.assertRaises(ProtectedWriteRejected):
                        enforce_local_output_path(root / name)

    def test_safe_absolute_output_is_only_preflight(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "reports"
            path.mkdir()
            result = enforce_local_output_path(path / "evidence.json")
            self.assertTrue(result["path_checked"])
            self.assertFalse(result["production_write_allowed"])
            self.assertFalse((path / "evidence.json").exists())

    def test_protected_ancestor_and_existing_target_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            protected = root / "YEDEKLER"
            protected.mkdir()
            with self.assertRaises(ProtectedWriteRejected):
                enforce_local_output_path(protected / "evidence.json")
            existing = root / "existing.json"
            existing.write_text("original")
            with self.assertRaises(ProtectedWriteRejected):
                enforce_local_output_path(existing)
            self.assertEqual(existing.read_text(), "original")

    def test_absolute_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with self.assertRaises(ProtectedWriteRejected):
                enforce_local_output_path(root / "nested" / ".." / "evidence.json")
            self.assertFalse((root / "evidence.json").exists())

    def test_allowed_root_beneath_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            actual = base / "actual"
            (actual / "reports").mkdir(parents=True)
            linked = base / "linked"
            linked.symlink_to(actual, target_is_directory=True)
            target = linked / "reports" / "evidence.json"
            with self.assertRaises(ProtectedWriteRejected):
                enforce_local_output_path(target, allowed_root=linked / "reports")
            self.assertFalse((actual / "reports" / "evidence.json").exists())

    def test_append_preflight_can_be_confined_to_sandbox(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            sandbox = base / "sandbox"
            sandbox.mkdir()
            outside = base / "outside.json"
            outside.write_text("original", encoding="utf-8")
            with self.assertRaises(ProtectedWriteRejected):
                enforce_local_append_path(outside, allowed_root=sandbox)
            inside = sandbox / "summary.json"
            inside.write_text("safe", encoding="utf-8")
            result = enforce_local_append_path(inside, allowed_root=sandbox)
            self.assertTrue(result["path_checked"])
            self.assertFalse(result["production_write_allowed"])
            self.assertEqual(outside.read_text(encoding="utf-8"), "original")
            self.assertEqual(inside.read_text(encoding="utf-8"), "safe")

    def test_local_output_rejects_unicode_noncharacters(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for suffix in ("\ufdd0", "\ufffe", "\U0001fffe"):
                with self.subTest(codepoint=hex(ord(suffix))):
                    target = root / ("evidence" + suffix + ".json")
                    with self.assertRaises(ProtectedWriteRejected):
                        enforce_local_output_path(target, allowed_root=root)
                    self.assertFalse(target.exists())

    def test_allowed_root_traversal_and_control_characters_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            target = root / "evidence.json"
            for candidate in (str(root) + "/nested/..", str(root) + "/.",
                              str(root) + "/\ufdd0", str(root) + "/\u202e"):
                with self.subTest(candidate=repr(candidate)):
                    with self.assertRaises(ProtectedWriteRejected):
                        enforce_local_output_path(target, allowed_root=candidate)
            self.assertFalse(target.exists())

    def test_isolated_playlist_rejects_relative_and_traversing_roots(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            target = root / "reports/MADSC55_TURKCE_TV_ADAY_DENEME.m3u8"
            for bad_root in (Path("relative"), str(root) + "/.",
                             str(root) + "/nested/..", str(root) + "/\u202e"):
                with self.subTest(root=repr(bad_root)):
                    with self.assertRaises(ProtectedWriteRejected):
                        enforce_local_turkish_tv_test_playlist(target, allowed_root=bad_root)
            self.assertFalse(target.exists())

    def test_isolated_playlist_rejects_lexical_destination_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            expected = root / "reports/MADSC55_TURKCE_TV_ADAY_DENEME.m3u8"
            for candidate in (str(root) + "/reports/./MADSC55_TURKCE_TV_ADAY_DENEME.m3u8",
                              str(root) + "/reports/nested/../MADSC55_TURKCE_TV_ADAY_DENEME.m3u8"):
                with self.subTest(candidate=candidate):
                    with self.assertRaises(ProtectedWriteRejected):
                        enforce_local_turkish_tv_test_playlist(candidate, allowed_root=root)
            self.assertFalse(expected.exists())

    def test_isolated_playlist_rejects_nfkc_aliases(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            target = root / "reports/MADSC55_TURKCE_TV_ADAY_DENEME.m3u8"
            for suffix in ("／extra", "＼extra", "：stream"):
                with self.subTest(suffix=suffix):
                    with self.assertRaises(ProtectedWriteRejected):
                        enforce_local_turkish_tv_test_playlist(target, allowed_root=str(root) + suffix)
            for alias in ("／", "＼", "："):
                with self.subTest(alias=alias):
                    candidate = str(root) + "/reports" + alias + "MADSC55_TURKCE_TV_ADAY_DENEME.m3u8"
                    with self.assertRaises(ProtectedWriteRejected):
                        enforce_local_turkish_tv_test_playlist(candidate, allowed_root=root)
            self.assertFalse(target.exists())

    def test_allowed_root_rejects_nfkc_separator_aliases(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            target = root / "evidence.json"
            for suffix in ("／nested", "＼nested", "：stream"):
                with self.subTest(suffix=suffix):
                    with self.assertRaises(ProtectedWriteRejected):
                        enforce_local_output_path(target, allowed_root=str(root) + suffix)
            self.assertFalse(target.exists())

    def test_allowed_root_and_isolated_playlist_reject_nfkc_dot_aliases(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "reports").mkdir()
            evidence = root / "evidence.json"
            playlist = root / "reports/MADSC55_TURKCE_TV_ADAY_DENEME.m3u8"
            for suffix in ("/．", "/．．"):
                with self.subTest(suffix=suffix):
                    with self.assertRaises(ProtectedWriteRejected):
                        enforce_local_output_path(evidence, allowed_root=str(root) + suffix)
                    with self.assertRaises(ProtectedWriteRejected):
                        enforce_local_turkish_tv_test_playlist(playlist, allowed_root=str(root) + suffix)
            for component in ("．", "．．"):
                candidate = str(root) + "/reports/" + component + "/MADSC55_TURKCE_TV_ADAY_DENEME.m3u8"
                with self.subTest(component=component):
                    with self.assertRaises(ProtectedWriteRejected):
                        enforce_local_turkish_tv_test_playlist(candidate, allowed_root=root)
            self.assertFalse(evidence.exists())
            self.assertFalse(playlist.exists())

    def test_local_output_rejects_nfkc_dot_segment_aliases(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for candidate in (str(root) + "/．/evidence.json",
                              str(root) + "/．．/evidence.json"):
                with self.subTest(candidate=candidate):
                    with self.assertRaises(ProtectedWriteRejected):
                        enforce_local_output_path(candidate, allowed_root=root)
            self.assertFalse((root / "evidence.json").exists())

    def test_local_output_rejects_nfkc_separator_aliases(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for name in ("report／safe.json", "report＼safe.json", "report：stream.json"):
                with self.subTest(name=name):
                    target = root / name
                    with self.assertRaises(ProtectedWriteRejected):
                        enforce_local_output_path(target, allowed_root=root)
                    self.assertFalse(target.exists())

    def test_dangling_symlink_parent_is_rejected_before_directory_check(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            dangling = root / "dangling"
            dangling.symlink_to(root / "missing", target_is_directory=True)
            target = dangling / "evidence.json"
            with self.assertRaisesRegex(ProtectedWriteRejected, "Symlinked output ancestor"):
                enforce_local_output_path(target)
            self.assertFalse((root / "missing").exists())

    def test_symlinked_parent_and_root_boundary_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            real = root / "real"
            real.mkdir()
            linked = root / "linked"
            linked.symlink_to(real, target_is_directory=True)
            with self.assertRaises(ProtectedWriteRejected):
                enforce_local_output_path(linked / "evidence.json")
            with self.assertRaises(ProtectedWriteRejected):
                enforce_local_output_path(root / "elsewhere.json", allowed_root=real)
