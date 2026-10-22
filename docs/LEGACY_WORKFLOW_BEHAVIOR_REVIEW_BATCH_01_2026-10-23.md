# Legacy workflow behavioral review — batch 01 (2026-10-23)

Scope: read-only source review of three exact YAML files from the frozen source repository `Madsc55/madsc-tv`, source commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. This is a behavioral specification draft, not a parity acceptance. No legacy files, playlists, EPG outputs, devices, or backups were modified.

## 1. `.github/workflows/epg-gunluk.yml`

### Observed legacy behavior
- Triggers: manual `workflow_dispatch` and daily schedule `25 3 * * *` (03:25 UTC).
- Permissions: `contents: write`; this workflow commits generated outputs.
- Steps: checkout; Python 3.12; run `scripts/build_epg.py` and `scripts/build_ibo_epg_test.py`; run `scripts/epg_tv_readiness.py`.
- Commit allowlist: `epg/madsc-epg.xml`, `epg/ibo-test-epg.xml`, `epg/report.json`, `epg/tv_kontrol_bekliyor.json`.
- Push behavior: only commit if staged changes exist; rebase on origin/main before push.
- Failure behavior: a failed command stops the default shell sequence; no explicit retry policy is defined in this YAML.

### Candidate replacement components (not yet proven equivalent)
- `madsc/epg.py`: read-only M3U tvg-id to XMLTV mapping check.
- `madsc/epg_inventory.py`: read-only XMLTV channel/programme inventory.
- These validate supplied artifacts; they do not generate the same four outputs or commit them. A direct one-to-one replacement has NOT been established.

### Required acceptance evidence
1. Frozen input playlist/source manifest and content hashes.
2. Generated main and five-channel pilot XMLTV hashes, channel/programme counts, and readiness report.
3. Exact output allowlist comparison.
4. Schedule/manual-trigger equivalence and explicit policy for the former write/commit action.
5. Two consecutive runs demonstrating idempotency; injected build failure proves no partial publication.
Status: `reviewed-source`; behavioral acceptance: `not-accepted`.

## 2. `.github/workflows/epg-pages.yml`

### Observed legacy behavior
- Triggers: manual; `workflow_run` after “EPG Günlük Güncelleme” completes on main.
- Deployment guard: workflow_run proceeds only when conclusion is success and head_branch is main.
- Permissions: contents read, pages write, id-token write; concurrency group `epg-pages`, cancel-in-progress true.
- Input is explicitly checked out from current `main`, not the triggering workflow's exact commit.
- Validates `epg/madsc-epg.xml` root `tv`, nonzero channel/programme counts; pilot XML must have exactly 5 channels and at least one programme.
- Creates `_site/.nojekyll`, HTML index, main XMLTV and pilot XMLTV; uploads Pages artifact and deploys it.
- After deployment, downloads published main XMLTV and retries up to 20 times with 3-second sleeps, 15-second request timeout, cache-busting query; requires SHA256 equality.
- The post-deploy published-content check is a hard failure if no matching hash is found.

### Candidate replacement components (not yet proven equivalent)
- `madsc/epg.py` and `madsc/epg_inventory.py` only perform local read-only validation.
- No replacement deployment/Pages publication component was confirmed in the inspected current files. Treating local XMLTV validation as equivalent to publishing and verifying remote bytes would be incorrect.

### Required acceptance evidence
1. Workflow-run trigger matrix for success, failure, non-main branch, and manual dispatch.
2. Pages artifact file list and SHA256s for main/pilot XMLTV.
3. Deployed URL response and SHA256 matching the uploaded artifact.
4. Cancellation/concurrency test and deployment permission review.
5. Negative tests for malformed main XML, pilot channel count != 5, missing programme, and persistent remote mismatch.
Status: `reviewed-source`; behavioral acceptance: `not-accepted`.

## 3. `.github/workflows/390-aday-tekrar-test.yml`

### Observed legacy behavior
- Triggers: manual and push when `yedekler/tekrar_test_390.py` changes.
- Permissions: contents read; checkout credentials disabled.
- Job timeout: 90 minutes.
- Installs ffmpeg; runs parallel 20-second video/audio tests with `TEST_WORKERS=10`.
- Uploads CSV and M3U outputs even after test failure (`if: always()`); missing files produce a warning rather than failing the upload step.
- Artifact name: `390-aday-tekrar-test`; paths are date-stamped `TEKRAR_TEST_2026-10-09.csv` and `TEKNIK_DOGRULANANLAR_2026-10-09.m3u`.

### Candidate replacement components (not yet proven equivalent)
- Current K2/K3 candidate and probe modules may cover parts of candidate intake and technical verification, but this workflow's exact 20-second media test, 10-worker concurrency, 90-minute bound, ffmpeg dependency, and CSV/M3U artifact contract have not been demonstrated as equivalent by the inspected source.
- Do not map this to a generic probe test without comparing the legacy script's parsing, thresholds, retry behavior, output schema, ordering, and exit codes.

### Required acceptance evidence
1. Read-only copy of the exact legacy script and dependency/version inventory.
2. Deterministic fixture batch proving input order, 20-second audio/video criteria, worker count, timeout and exit-code parity.
3. Schema and content comparison for CSV and M3U outputs, including partial-failure artifact behavior.
4. Missing ffmpeg, one candidate timeout, malformed media, and all-worker failure scenarios.
Status: `reviewed-source`; behavioral acceptance: `not-accepted`.

## Batch result
- Exact YAML source behavior reviewed: 3/3.
- Candidate replacement mappings identified as tentative: 3/3.
- Behavioral parity accepted: 0/3.
- This document intentionally does not increase the overall 92-workflow acceptance counter. Acceptance requires executable differential evidence and reviewed source-to-replacement mappings.
