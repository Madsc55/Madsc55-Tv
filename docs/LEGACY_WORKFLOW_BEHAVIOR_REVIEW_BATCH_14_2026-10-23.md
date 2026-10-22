# Legacy workflow behavior review — Batch 14
Date: 2026-10-23 (Europe/Stockholm)
Scope: read-only review of three legacy workflow files at frozen tree `ca374df3b9585c0d76a078db9536150ebbc260f7` in `Madsc55/madsc-tv`, branch `madsc/bes-sistem-toplu-birlestirme`. No workflow was dispatched; no legacy or production files were changed.

## 1. `.github/workflows/madsc-genis-kaynak-kontrol.yml`
- Workflow blob SHA: `396d33dd8d5f3440dc81ae76abb91fc0d43f6a94`.
- Direct script SHAs: `tools/genis_kaynak_taramasi.py` `d0330c0fca9ab6dfacb729868cec534c4ce73f37`; `tools/protected_write_gate.py` `c3c8f278db7de4cd0fd61cdb4180f9c03cb2c4c1`.
- Manual-only, main-branch-gated, but grants `contents: write` and `actions: write`, and checkout credentials persist by default. It runs weekly and monthly source scans sequentially, uploads a report artifact, commits scan/history output, checks changed paths through the protected-write gate, retries push conflicts, then dispatches the existing three-stage workflow.
- Source scanner parses `SOURCES` from `madsc_akilli_kesif.py`, fetches external M3U feeds with bounded 3 MB reads and 16-second timeouts, creates a separate source review queue, and writes reports/history under `madsc_genis_tarama/`; it does not itself test playback or edit playlists. Prior state parse failure stops rather than discarding history.
- Risks: the workflow has broad write permissions for a manually requested audit; report conflict deliberately fails after retaining the artifact, so no successful persistent update is implied. The post-scan dispatch can start additional live verification work; it must not be triggered during static review. The source set and network results can change, and metadata matches do not establish source independence, licensing, stable playback or IBO identity.
- Status: source-reviewed only; no scan, push or dispatch performed.

## 2. `.github/workflows/madsc-hizli-on-kontrol.yml`
- Workflow blob SHA: `92ba7ce2731d544b7361fb8877c531d4c4911840`.
- Direct script SHAs: `scripts/five_system_cutover_readiness.py` `ebcfc3aa0d362361a2ca0ba7d7ba80f6f38a97e9`; `scripts/five_category_preflight.py` `c4ec135e119a357629253f3fd7d8908596dde46b`; `scripts/five_category_shared_controls.py` `ea36a0408a8dac40f89e520f6d6433005d228472`.
- Manual and feature-branch push triggers; `contents: read`, checkout credentials disabled, 15-minute timeout. It emits a migration-readiness report, runs shared-control and 92-workflow inventory regressions, and runs a category preflight that checks referenced scripts/tests, manual triggers, read-only permissions and protected hash checks.
- The readiness report explicitly keeps `migration_approved`, `cutover_allowed` and legacy retirement false, with required blockers including 26 runtime rules, 92 behavioral parity, current-SHA CI, independent offsite restore, IBO acceptance and explicit user cutover approval. This is a good fail-safe distinction between static readiness and authorization.
- Limitation: preflight uses regex/static file references and only covers five category workflows; it cannot prove Actions actually succeeded, runtime side effects are absent, or all 92 legacy workflows are behaviorally equivalent. Missing report artifacts are warnings at upload, so job step outcomes—not artifact presence—remain the execution evidence.
- Status: source-reviewed only; no workflow dispatch performed.

## 3. `.github/workflows/madsc-ibo-3-5281.yml`
- Workflow blob SHA: `4b0745614a11625f020baa39b832983ce5fc42ca`.
- Manual and feature-branch push triggers; `contents: read`; 15-minute timeout. The only step prints a dry-run notice that protected playlist mutation requires explicit approval and automatic mutation is disabled.
- The workflow name suggests a channel-separation operation, but the actual workflow performs no separation, reads no candidate data and emits no structured result or evidence artifact. Treat it as a disabled placeholder, not proof that IBO channels were classified or separated.
- Status: source-reviewed only; no workflow dispatch or playlist change performed.

## Batch summary
- Three additional workflows reviewed against exact frozen source SHAs. No legacy repo write or live operation.
- Cumulative static source review advances from 39/92 to **42/92**; **50/92** remain subject to canonical exclusions and deduplication.
- Behavioral parity accepted this batch: **0/3**; overall remains **0/92**. Runtime security acceptance remains **0/26**; main-task acceptance remains **0/22**.
- Priorities: keep manual source-scan write permissions narrow and avoid automatic chaining into live tests during review; label preflight as static-only; do not count the IBO placeholder as implemented behavior.
- Static review does not grant migration approval. Protected playlists, EPG, favorites, logos, backups and devices remain untouched.