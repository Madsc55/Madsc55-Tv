# Legacy workflow behavioral review — batch 04 (2026-10-23)

Frozen source: `Madsc55/madsc-tv`, commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. Read-only source review. No legacy workflow was dispatched and no live candidate list was modified.

## 1. `.github/workflows/aday-yedekleme.yml`

Observed contract:
- Manual trigger, plus push to main when `.github/commands/aday-yedekleme.txt` changes.
- `contents: read`, checkout with persisted credentials disabled, 30-minute timeout.
- Runs `yedekler/teknik_adaylari_aktar.py` with `GH_TOKEN`.
- The script queries two hard-coded historical Actions run IDs, requires exactly 34 and 66 artifacts respectively with names beginning `YENILER-KANAL-ADAYLARI-GRUP-`, downloads each artifact and reads `YENILER_TARAMA_RAPORU.csv`.
- Imports only rows whose technical evidence is `TEKNIK_AKIS_VAR` and media evidence `VIDEO_SES_VAR`; excludes URLs already in `CALISANLAR.m3u` and a prior backup file; deduplicates URLs; writes a separate M3U backup with explicit “identity not verified” text.
- Always uploads the backup artifact if present; missing file only warns.
- Script's API fetch helper uses 50-second per-request timeout; YAML job timeout is 30 minutes. Artifact count and historical run IDs are brittle assumptions that should be explicitly versioned and reviewed.

Potential replacement: K2/K3 evidence intake and duplicate handling are related, but historical-run selection, exact artifact prefix/count, CSV criteria, name deduplication and output M3U schema are not yet proven equivalent.

Required acceptance: archived source run metadata and artifact hashes; fixed fixtures for technical/media criteria; duplicate URL/name cases; missing artifact and malformed CSV failure; redirects do not leak token off api.github.com; no main playlist writes; exact output comparison. Status: reviewed-source, not accepted.

## 2. `.github/workflows/akilli-aday-puanlama.yml`

Observed contract:
- Manual and push triggers for the scoring script/workflow; read-only permissions and checkout credentials disabled; 55-minute timeout.
- Installs ffmpeg, runs broad read-only candidate discovery with `SCAN_BATCH=-1`, verifies prioritized streams via real ffprobe, then scores candidate CSVs.
- Script scores only recognized input filename classes, merges selected media evidence by URL, awards points for video/audio, resolution and HTTPS logo, and withholds identity/stability approval.
- Outputs `AKILLI_ADAY_PUANLARI.csv`, `AKILLI_ADAY_OZET.json`, `ONCELIKLI_KANAL_TEK_NIK_RAPOR.csv`, `ONCELIKLI_OZET.json`; artifact upload is required and retained 30 days.
- The script explicitly marks `KIMLIK_DOGRULANDI`, `KARARLILIK_DOGRULANDI`, and `ANA_LISTEYE_EKLENEBILIR` as `HAYIR`.

Potential replacement: K2 ranking and K3 probe evidence are conceptually related, but score formula, source merge precedence, URL deduplication, tie ordering, report schemas and ffprobe failure semantics need differential tests. Do not treat a technical score as channel identity or playlist approval.

Required acceptance: exact CSV/JSON diff over frozen fixtures; threshold/field-missing/tie cases; ffprobe missing, timeout and malformed media; duplicate URL from multiple evidence files; assert protected playlists unchanged and all approval fields remain false. Status: reviewed-source, not accepted.

## 3. `.github/workflows/felaket-kurtarma-tatbikati.yml`

Observed contract:
- Manual and push triggers; contents read; checkout credentials disabled; 8-minute timeout.
- `scripts/disaster_recovery_dry_run.py` verifies that working-tree bytes of `CALISANLAR.m3u` and `YENILER.m3u` exactly equal Git HEAD snapshots.
- Validates M3U header and at least one channel; simulates corruption in a temporary directory, detects it, restores the exact snapshot bytes, and confirms the original files were untouched.
- Always uploads `DISASTER-RECOVERY-REPORT.json`; missing report is a hard error.
- Report explicitly states Git history is not an independent offsite backup and does not verify IBO playback or untracked files.

Potential replacement: `madsc/restore_drill.py` exercises an allowlisted temporary backup/restore sandbox but has a different input/output contract. Neither isolated drill proves external backup recovery or production restore.

Required acceptance: compare exact source file set and hash results; corruption-detection parity; source unchanged; report schema; missing report failure; explicit separate offsite restore evidence. Status: reviewed-source, not accepted.

## Batch summary
- Source YAMLs reviewed in this batch: 3.
- Cumulative documented source review in batches 01–04: 12 workflow YAMLs.
- Accepted behavioral parity in batch 04: 0/3; overall accepted legacy workflow parity remains 0/92.
- Static review only; no production playlist, EPG, device data, backups, or legacy repository changes.
