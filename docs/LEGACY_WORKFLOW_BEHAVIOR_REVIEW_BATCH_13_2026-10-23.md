# Legacy workflow behavior review — Batch 13
Date: 2026-10-23 (Europe/Stockholm)
Scope: read-only review of three more workflows in `Madsc55/madsc-tv`, branch `madsc/bes-sistem-toplu-birlestirme`, frozen tree `ca374df3b9585c0d76a078db9536150ebbc260f7`. No legacy-repository writes, workflow dispatch, live probes, or production/device changes were performed.

## 1. `.github/workflows/madsc-birlesik-kesif.yml`
- Workflow blob SHA: `da472ae0e45aa0d3c03a7dc8f9833bf43f733902`.
- Direct scripts/blob SHAs: `tools/workflow_failure_gate.py` `e7add25cb3af1639dfff26df322b101f253bcf75`; `tools/protected_write_gate.py` `c3c8f278db7de4cd0fd61cdb4180f9c03cb2c4c1`; `scripts/discovery_archive.py` `22274f17f34a501f691bedb5e3667bb1fe00bf32`; `madsc_akilli_kesif.py` `d8673dbd763c7411878bd27fa432b455c15c9b31`.
- Scheduled twice daily and manual; branch-gated to main, but grants `contents: write` and `actions: write` and uses checkout credentials by default. It probes many external sources, writes persistent discovery/history reports, commits the report directory and pushes to main after running the protected-path gate.
- Safety positives: the fail-chain circuit breaker queries previous runs and fails closed if current-run provenance is missing; the publisher preserves generated reports outside the runner checkout before resetting the checkout; it checks whether the remote report folder changed since the recorded base and refuses to overwrite a concurrent report update; protected-path gate runs before push and denies M3U/EPG/favorites/logo/archive paths.
- Residual risk: the gate is a code-level path policy, not branch protection, and this job has broad write permissions. The conflict branch exits successfully after preserving its report only as an artifact, so a green run does not guarantee reports were committed. The false-guarded EPG/logo join is intentionally skipped; EPG remains deferred and must not be inferred as checked. Source probing and candidate status are time-dependent and do not prove source independence, licensing, channel identity or IBO playback.
- Status: source-reviewed only; no workflow dispatch or remote report write performed.

## 2. `.github/workflows/madsc-cuma-ana-liste-denetimi.yml`
- Workflow blob SHA: `b14aca32502179ae27e2399b0278502c512c2984`.
- Direct scripts/blob SHAs: `tools/haftalik_ana_liste_denetimi.py` `1c7e87aebe73c6abbc188a6068a7bc0ea4ebf5c8`; `tools/cuma_denetim_uyari_ozeti.py` `09a5db996b4f568b9e8bedbee2982edc67556f43`.
- Manual-only workflow, `contents: read`, checkout credentials disabled, 55-minute timeout. It runs ffprobe against all parsed playlist entries, downloads the first EPG URL from the M3U header, writes a JSON report, then always generates a warning summary and uploads the report artifact.
- The report explicitly redacts stream URLs into short hashes and labels identity as requiring visual verification. Network/EPG failures become `ERISIM_DOGRULANAMADI` or `EPG_OKUNAMADI`; they are not converted into delete/change decisions. The warning summary does not fail the job merely because channels or EPG records are missing, so workflow success means the inspection ran, not that channel health passed. Preserve that distinction in downstream reports.
- Static robustness concern: `epg_status()` reads only the first EPG URL and only the first 30 MB of response, then parses the XML as a whole; truncated or oversized feeds become an unverified EPG result. This is a bounded probe, not full-feed validation.
- Status: source-reviewed only; no live playlist/EPG test performed.

## 3. `.github/workflows/madsc-documentation-check.yml`
- Workflow blob SHA: `0678a8a201eb194503f9097265fe37e68b1e4d3d`.
- Manual-only, `contents: read`; checks non-empty `AGENTS.md`, `OZELLIK_ENVANTERI.md`, `DEVAM_NOTU.md`, literal `Kural 25`, literal `build_epg.py`, and that the first line of `CALISANLAR.m3u` starts with `#EXTM3U`.
- Limitation: this is a small presence/string smoke check, not Markdown/link/schema validation, documentation-to-code consistency, or M3U parse/behavior validation. Literal wording changes can cause false negatives; a file containing those strings can pass despite stale or contradictory guidance. Treat it only as a lightweight sanity check.
- Status: source-reviewed only; no workflow dispatch performed.

## Batch summary
- Three more workflows reviewed against exact frozen blob SHAs. No production or legacy repository mutation.
- Cumulative static source-review ledger advances from 36/92 to **39/92**; **53/92** remain, subject to canonical exclusions and deduplication. The 99-YAML source tree and 92-workflow parity scope are different inventories.
- Behavioral parity accepted this batch: **0/3**; total remains **0/92**. Runtime security acceptance remains **0/26**; main-task acceptance remains **0/22**.
- Follow-up priorities: keep the broad-write discovery publisher isolated and branch-protected; label warning-only weekly reports as inspection-not-health-acceptance; replace literal-string documentation checks with structured consistency checks in the replacement repository.
- Static review is not acceptance. Protected playlists, EPG, favorites, logos, backups and real devices remain untouched.