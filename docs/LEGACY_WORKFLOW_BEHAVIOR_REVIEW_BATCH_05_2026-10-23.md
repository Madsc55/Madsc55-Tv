# Legacy workflow behavioral review — batch 05 (2026-10-23)

Frozen legacy source: `Madsc55/madsc-tv`, source commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. Static source inspection only; no legacy workflows were dispatched and no candidate/live playlist data was changed.

## 1. `.github/workflows/altinci-aday-tekrar-test.yml`

Observed contract:
- Manual trigger and push on this workflow, `altinci_aday_tekrar_test.py`, or `yanlis_pozitif_koruma.py`; read-only contents permission; 20-minute timeout.
- Runs compile/import and mock-based contract checks before installing ffmpeg.
- Test contract: a candidate with fewer than two successful runs remains eligible; mocked HLS technical flow plus ffprobe video/audio and a successful independent HLS verification yields `TEKNIK_TEST_GECTI_KIMLIK_BEKLIYOR`; failed HLS verification yields `TEKRAR_TEST_BEKLIYOR` and `SUREKLILIK_DOGRULANAMADI`.
- Then installs ffmpeg, runs actual scheduled due candidates with `RETEST_LIMIT=5`, and always uploads the CSV report if it exists (missing report warns).
- The script reads `aday_bekletme/gecmis.json`, tests only due HTTP(S) candidates, and deliberately does not promote candidates to the main playlist.

Potential replacement: `madsc/candidate_coordination.py`, `madsc/legacy_stability.py`, and K3 probe modules cover parts of due scheduling, observation and media checks. Exact state-file schema, schedule rules, candidate ordering, five-item limit, live HLS check, and report row semantics still need differential parity evidence.

Acceptance evidence: deterministic fixture history; due/not-due boundaries; zero/one/two prior successes; exactly five candidates selected and order compared; HLS pass/fail and ffprobe timeout; artifact present on partial failure; source and protected playlists unchanged. Status: reviewed-source, not accepted.

## 2. `.github/workflows/birlesik-aday-raporu.yml`

Observed contract:
- Manual and push triggers; read-only permissions; checkout credentials disabled; 60-minute timeout.
- Attempts to restore longitudinal observations from Actions cache using a run-specific key and `kanal-kararlilik-` restore prefix.
- Pipeline order: broad discovery; focused technical stream evidence; first general media-test batch (`ADAY_TEST_GRUBU=0`); score merge; longitudinal stability report; consolidated approval report.
- Requires four final artifacts and retains them 30 days.
- The scoring script intentionally sets identity, stability and main-list eligibility flags to HAYIR; unified report preserves IBO/user approval as absent and never automatically adds channels.

Important parity risk: a run-specific cache key plus a restore prefix may restore a prior matching cache but does not itself demonstrate that updated `KARARLILIK_GECMISI.json` is saved back under a reusable key. Inspect complete workflow/source and cache-save behavior before asserting longitudinal state persists across runs.

Potential replacement: K2/K3 ranking/probe, `madsc/legacy_stability.py`, and evidence merger are candidates, not accepted replacements.

Acceptance evidence: stage-by-stage frozen input/output hashes; cache restore and save test across two separate runs; source merge precedence; scoring and stable sort differential; all four artifacts required; failures in each stage; verify no auto-approval and no playlist write. Status: reviewed-source, not accepted.

## 3. `.github/workflows/genel-aday-medya-test.yml`

Observed contract:
- Manual and push triggers; read-only permissions; checkout credentials disabled; 40-minute timeout.
- Installs ffmpeg, runs broad read-only discovery, probes only the selected group `ADAY_TEST_GRUBU=0`.
- Media script sorts candidates by new-candidate type, channel and URL; uses a 30-candidate page and six workers; ffprobe timeout is 16 seconds per candidate with a 9-second read/write timeout; records video/audio/resolution/errors in CSV and JSON.
- Artifact upload is mandatory; missing report fails; retention is 30 days.
- The workflow itself tests only the first group; complete coverage requires separate group invocations.

Potential replacement: K3 probe functionality is related but must preserve group selection, deterministic ordering, timeout, worker limit, result schema and mandatory artifact behavior.

Acceptance evidence: fixed 30+ candidate fixture; exact group 0 selection and stable sort; missing/invalid URL; ffprobe absent/timeout/failure; worker bound; schema and report comparison; missing output must fail; source playlist unchanged. Status: reviewed-source, not accepted.

## Batch summary
- Source YAMLs reviewed in this batch: 3.
- Cumulative documented source review in batches 01–05: 15 workflow YAMLs.
- Accepted behavioral parity in batch 05: 0/3; overall accepted legacy workflow parity remains 0/92.
- This is static behavior analysis, not runtime or production acceptance.
