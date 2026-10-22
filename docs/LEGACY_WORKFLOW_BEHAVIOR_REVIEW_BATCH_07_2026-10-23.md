# Legacy workflow behavior review — batch 07 (2026-10-23)

Frozen legacy source: `Madsc55/madsc-tv`, branch `madsc/bes-sistem-toplu-birlestirme`, commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. This is read-only source inspection; no legacy files or live/production data were changed.

## 1. `.github/workflows/automatic-png-logos.yml`

- Frozen workflow blob SHA: `3d321b81f023647d1cd29c99f015d296a34df525`.
- Trigger: manual `workflow_dispatch` only; `contents: read`; concurrency group `automatic-png-logos`, no cancellation; job timeout 15 minutes.
- Steps install Pillow/CairoSVG, run `logo_deneme/audit.py`, then `scripts/automatic_png_logos.py`, install ffmpeg, run `scripts/logo_visual_evidence.py`, upload visual frames (missing frames ignored), then always upload logo and review JSON/artifacts for 30 days.
- Script source SHA `51cb734691edee5b9207ce36a40a8f295698e008`; helper SHA `c70ea7b5444b60805651fafa4c2269e880076e7c`; audit SHA `b33b8bbfd72b0b5316936088725d68ef61bee980`.
- **Critical write-side-effect finding:** despite the “safe preparation” label, `automatic_png_logos.py` reads `CALISANLAR.m3u`, may download/convert logos into `logos/auto/`, and calls `playlist.write_text(updated, encoding='utf-8')` on `CALISANLAR.m3u`. It asserts all non-logo fields stay equal and gates new logo values on a saved visual review plus PNG SHA256, but it still writes the protected playlist file. The workflow subsequently checks `git diff` and calls `git restore -- CALISANLAR.m3u` if changed, discarding the workspace diff after the write has already occurred. That cleanup is not equivalent to never writing the protected path, and could erase pre-existing runner-workspace changes if the assumptions about a clean checkout are violated.
- The visual helper deletes/replaces per-channel frame files under `logo_deneme/visual_frames/` and writes review JSON; these are generated review artifacts. Existing logo identity/device compatibility remains unverified. No automatic approval is inferred from a decoded image.
- Replacement/parity acceptance requires a fixture-only playlist copy, zero writes to any protected playlist path (not write-then-restore), unchanged protected source SHA, exact PNG hashes, reviewed source/visual evidence, generated artifact list, and failure/missing-dependency behavior. **Status: reviewed-source, not accepted.**

## 2. `.github/workflows/birlesik-durum-raporu.yml`

- Frozen workflow blob SHA: `cfd859aa1c5d474749edd09d99506b006ab0f82b`.
- Triggers on main push for this workflow and two named tools, plus manual dispatch; `contents: read`; checkout uses `persist-credentials: false`; Python 3.11; five-minute timeout.
- Runs `tools/guncel_test_durum_ozeti.py` to stdout JSON, `tools/eksik_turk_kanal_takibi.py` to stdout JSON, `tools/kaynak_kapsam_denetimi.py` to stdout JSON, and `tools/genel_sistem_bakimi.py`; uploads three JSON snapshots plus `madsc_bakim/weekly_health.json` for 30 days.
- Tool SHAs: `guncel_test_durum_ozeti.py` `39e5b1301e9859d3e810fe86078c31f3269dc612`; `eksik_turk_kanal_takibi.py` `fe63daf98b674c87cc24df787b276e8cf9bd04bc`; `kaynak_kapsam_denetimi.py` `f76608b5c7bab91925da3f683a66d35cdc426a75`; `genel_sistem_bakimi.py` `05dcd6a1e2e5ed5303683ffd145e7c03ef164949`.
- The first tool requires both three-stage and final summary snapshots, rejects inconsistent candidate counts, reports historical snapshot times, and explicitly labels device confirmation as user/IBO-required; it starts no stream tests. The second reads the playlist and historical discovery JSON, performs normalized exact-name/alias matching for four Turkish targets, and never proves station identity or tests URLs. The third parses the configured source dictionary via AST and reports counts from the prior source-access CSV; it does not fetch the extra feeds. The fourth checks required files and JSON snapshots and writes only the generated `madsc_bakim/weekly_health.json` report.
- The workflow is an artifact-producing snapshot, not an equivalent replacement for discovery, testing, live status, or external backup. Missing/invalid summary behavior and output schema need differential tests; snapshot timestamps must not be described as current live service state.
- Acceptance requires frozen input snapshots, exact JSON schemas/values, missing/corrupt inputs, consistent and inconsistent counts, artifact presence, no network/stream test invocation, and a source/protected-playlist SHA before/after. **Status: reviewed-source, not accepted.**

## 3. `.github/workflows/genis-kanal-tarama.yml`

- Frozen workflow blob SHA: `ffea4c826bf1ea9f2b586ddbd279d169f930b9b1`.
- Triggers on main push to `.github/commands/genel-guncelleme.txt` or manual dispatch; `contents: read`; checkout credentials disabled; installs ffmpeg; job timeout 55 minutes; always uploads `GENIS_KANAL_TARAMA_RAPORU.csv` for 30 days.
- Script SHA: `genis_kanal_tara.py` `256cbc32a74b0de84a64424d9800bfda365de1e4`.
- Reads `CALISANLAR.m3u` to build known URL/name/ID sets. Fetches nine configured public M3U sources concurrently (22-second request timeout each), parses and deduplicates new URLs, labels candidates as alternative/new, and probes candidates concurrently with ffprobe (11-second process timeout, bounded probe settings). Writes CSV columns `KANAL,KAYNAK,TUR,ON_TEST,URL,TVG_ID,LOGO_ADAY`; network/source errors become `DOGRULANAMADI`. The workflow's 55-minute timeout bounds the job but does not prove all source fetches or probes completed.
- This is real network discovery and live stream probing, not an offline report-only task. It must not be invoked for fixture parity or accepted without explicit authorization and a frozen, non-production fixture. The script does not write the main playlist; it reads it and writes the generated candidate CSV.
- Acceptance requires source-by-source success/error records, deterministic URL deduplication and ordering, exact CSV schema/rows, ffprobe missing/timeout/nonzero-exit cases, partial source failure, job timeout and always-upload semantics, and before/after proof that protected playlist bytes remain unchanged. **Status: reviewed-source, not accepted.**

## Batch summary

- Three additional workflow YAMLs inspected against the frozen source branch; their workflow blob SHAs match the recorded source inventory.
- Cumulative documented static source reviews: 21/92; 71 remain for static review, subject to the canonical 92-workflow scope exclusions. This count is source review only.
- Behavioral parity accepted in this batch: 0/3; overall legacy parity remains **0/92**. Runtime security remains **0/26**; independent main-task acceptance remains **0/22**.
- No workflow was dispatched. No legacy repository was written. No live IPTV/EPG, production playlist, logo, device, backup, or archive data was changed.
