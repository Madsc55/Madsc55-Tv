# K3 EPG performance and duplicate-ID regression — 2026-10-23

## Scope
User explicitly deferred IBO Player Pro device acceptance to the last step; user will test it and report back. Do not claim device verification or request it now.

## Changes
- `e6e9055b333c43ffd82a1f8d1ba06cd527f547c6`: replace the quadratic `ids.count(channel_id)` duplicate-ID detection in `madsc/epg.py` with one pass through a set of seen IDs and a set of duplicate IDs. Complexity is O(n) expected for detection plus O(d log d) to sort duplicate output, rather than O(n²) worst-case.
- `9c83d425fb0ef9c5e678546bd39dc939a25e2dde`: add a regression covering two duplicated channel IDs, deterministic sorted reporting, blank ID exclusion, and fail-closed `matching_verified`. EPG test function count now 17.

## Verification
- GitHub Actions run `39870559680` for the new test commit was pending when checked; do not claim a pass until completed successfully.
- Earlier offline suite runs `39870389256` and `39870378285` succeeded but predate this optimization.
- Real video/audio, continuity, Pages/XMLTV live-chain and logo checks remain outstanding. IBO Player Pro acceptance is the final step, performed by the user.
- Production playlist, XMLTV, devices, logos, favorites, backups and archive were not modified. PR #71 not merged.
