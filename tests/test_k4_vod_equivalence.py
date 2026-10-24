import unittest
from madsc.k4_vod_equivalence import compare_vod_manifests


def fixture(path="vod/movie.ts", size=3, digest="a" * 64,
            retention="30d", access="subscriber"):
    return {"entries": [{"path": path, "bytes": size, "sha256": digest,
                         "retention": retention, "access": access}]}


class K4VODEquivalenceTests(unittest.TestCase):
    def test_identical_fixture_passes_without_production_claim(self):
        result = compare_vod_manifests(fixture(), fixture())
        self.assertTrue(result["equivalent"])
        self.assertFalse(result["production_vod_verified"])
        self.assertFalse(result["production_writes"])

    def test_missing_extra_and_changed_are_rejected(self):
        for target in (fixture("vod/other.ts"), fixture(size=4),
                       fixture(digest="b" * 64), fixture(retention="60d"),
                       fixture(access="public")):
            with self.subTest(target=target):
                self.assertFalse(compare_vod_manifests(fixture(), target)["equivalent"])

    def test_unsafe_or_aliased_paths_fail_closed(self):
        for path in ("../secret", "/absolute", "vod//file", "vod/./file",
                     "vod\\file", "vod/\u202efile", "C:/windows"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                compare_vod_manifests(fixture(path=path), fixture(path=path))
        dup = fixture()
        dup["entries"].append({**dup["entries"][0], "path": "VOD/MOVIE.TS"})
        with self.assertRaises(ValueError):
            compare_vod_manifests(dup, dup)

    def test_invalid_types_and_forged_claims_fail_closed(self):
        for entry in ({"bytes": True}, {"sha256": "bad"}, {"access": ""},
                      {"retention": None}):
            candidate = fixture()
            candidate["entries"][0].update(entry)
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                compare_vod_manifests(candidate, fixture())
        candidate = fixture()
        candidate["production_vod_verified"] = True
        with self.assertRaises(ValueError):
            compare_vod_manifests(candidate, fixture())


if __name__ == "__main__":
    unittest.main()
