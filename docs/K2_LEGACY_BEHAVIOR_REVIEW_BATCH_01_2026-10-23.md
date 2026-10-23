# K2 — Legacy workflow behavioral parity review (batch 1)

Date: 2026-10-23. Read-only static review. **No workflow was executed; no production files were changed.**

## Acceptance method
For each of the 92 pinned behavior workflows, require a pinned legacy source blob, a source-bound replacement workflow and consumer mapping, independently obtained execution/run metadata, the **same input SHA-256**, independently verified artifact SHA-256 bytes, matching outputs, side effects, exit/timeout behavior, and reviewer approval. Offline fixture tests, static mapping, or matching self-declared JSON are insufficient. Status remains **NOT ACCEPTED** until all checks pass.

## Individually inspected legacy workflows

| Legacy workflow (pinned blob SHA) | Legacy trigger/behavior | Replacement candidate | Static difference / blocker | Acceptance |
| --- | --- | --- | --- | --- |
| `.github/workflows/390-aday-tekrar-test.yml` (`b12f53a17434fe719a65edfdc968f675e1f16b95`) | Manual and push on `yedekler/tekrar_test_390.py`; installs ffmpeg; runs `TEST_WORKERS=10 python3 yedekler/tekrar_test_390.py`, 20-second audio/video checks; exports CSV and M3U, 90-minute job timeout | `madsc-03-kanal-test.yml` | Replacement uses opt-in live probes and different executors/artifact names; original 390-entry behavior, 20-second timing, worker count, trigger and CSV/M3U byte outputs **not established equivalent** | **BLOCKED — no common-input run/artifact pair** |
| `.github/workflows/aday-bekletme.yml` (`68564680a2c32b11d1c5ed78825f01c85d0378e8`) | Manual and selected push paths; sequentially runs discovery, duplicate, media, quarantine, schedule, retest (limit 5), source scoring, priority; exports 10 named reports; 90-minute timeout | K2 discovery and K3 tests | New opt-in discovery does not establish exact 8-command order, retest limit, side effects, triggers or 10 report outputs | **BLOCKED — no common-input run/artifact pair** |
| `.github/workflows/aday-logo-epg-test.yml` (`21214309014625c4a63f00ee16c9017efac6b0a7`) | Manual/push; compiles `scripts/candidate_epg_logo_join.py`; verifies `CALISANLAR.m3u` SHA unchanged; asserts 5 pilot EPG channels and candidate approval flags; uploads JSON | K3 channel/EPG and K2 discovery | Replacement isolated report does not establish same join logic, five-channel assertion, protected-file before/after hash, trigger, or JSON schema | **BLOCKED — no common-input run/artifact pair** |

## Evidence and safety
- These are **three static source comparisons**, not three accepted behavior equivalents. The other 89 pinned behavior workflows still require individual comparison (subject to pinned scope classification).
- Current acceptance counters: behavioral parity **0/92**, main tasks **0/22**. No synthetic runs, guessed artifacts, or fabricated SHA-256 evidence.
- Old repository `Madsc55/madsc-tv` and working IPTV playlist, EPG, logos, favorites, archives, backups, production data remain untouched.
- Do not enable live probes, publish channels, merge old PRs, or test IBO Player Pro until explicit final-stage user validation.

## Next evidence required
Collect independent legacy and replacement run IDs and artifact bytes for a safe, matching input fixture per workflow; verify both GitHub execution origins and SHA-256 before comparing outputs and failure/timeout/side-effect behavior. Record actual differences and only then seek independent reviewer approval.
