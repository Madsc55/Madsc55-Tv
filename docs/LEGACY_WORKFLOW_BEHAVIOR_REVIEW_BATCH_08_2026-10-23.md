# Legacy workflow behavior review — batch 08 (2026-10-23)

Frozen legacy source inventory: `Madsc55/madsc-tv`, source tree reference `ca374df3b9585c0d76a078db9536150ebbc260f7`. Read-only source inspection only; no legacy workflow was dispatched and no production data was accessed or changed.

## 1. `.github/workflows/kanal-kararlilik.yml`

- Workflow blob SHA: `c968204d3d9d54cf218d92954189c9e6945a509f`.
- Triggers: `workflow_dispatch` and path-filtered pushes; `contents: read`; checkout credentials disabled; 30-minute timeout.
- Steps restore `KARARLILIK_GECMISI.json` from Actions cache, install ffmpeg, run `scripts/oncelikli_kanal_dogrula.py`, run `scripts/kanal_kararlilik_takip.py`, save history under a run-specific cache key, and always upload three reports for 30 days.
- Script blob SHAs: `scripts/oncelikli_kanal_dogrula.py` `d72fcddfa0018684eae513a874e8ea5cc1864adb`; `scripts/kanal_kararlilik_takip.py` `1c21d48734e756b09534437f75e2ea70f349ff07`.
- The history tracker validates timestamps, rejects naive/future timestamps and conflicting observations at the same time, rejects untested rows, and copies history before updates. These source properties do not prove cache restore/save succeeds in independent real runs.
- The probe script fetches multiple external M3U sources and invokes ffprobe; this is live network behavior, not an offline parity test. Cache misses, corrupt history, source failures, ffprobe failure/timeout, and always-upload behavior need differential coverage.
- Repeated observations and required time windows cannot be manufactured by retiming a single run. A cache key in source is not evidence that history persisted between independent runs.
- Acceptance requires two independent run artifacts proving restore then save, frozen candidate inputs, genuinely separated chronological observations, cache-miss/corrupt-history and ffprobe failure cases, exact report schemas, and protected-playlist before/after hashes. **Status: reviewed-source, not accepted.**

## 2. `.github/workflows/kaynak-puanlama-kontrol.yml`

- Workflow blob SHA: `0ffc33a27ff7d6bb459fbfa608db1095218379f0`.
- Triggers: manual dispatch and path-filtered pushes; `contents: read`; five-minute timeout.
- Compiles `kaynak_guven_puani.py` and runs `tests/test_kaynak_guven_puani.py`; the workflow itself defines no artifact upload or live probing.
- Script blob SHA: `kaynak_guven_puani.py` `d3153f880d507f36a41187758a5529e202e2e496`.
- The script reads `aday_bekletme/gecmis.json` if present, groups records by source/hostname, distinguishes untested candidates from tested outcomes, counts unique runs/successes, applies a smoothed score, creates `aday_bekletme/`, and writes `KAYNAK_GUVEN_PUANLARI.csv`. It has a filesystem write side effect despite being a scoring/test workflow.
- Risks to lock down: absent history silently becomes an empty scoring dataset; malformed JSON fails before output; malformed/non-dict records are skipped; score semantics depend on the meaning and uniqueness of `runs` and `successful_runs`.
- Acceptance requires fixtures for absent/empty/corrupt history, untested-only sources, duplicate run IDs, one vs. multiple successes, invalid URLs/source names, exact rounding and CSV bytes, and proof output is confined to a temporary directory. **Status: reviewed-source, not accepted.**

## 3. `.github/workflows/ibo-bagimsiz-test-listesi.yml`

- Workflow blob SHA: `be63acf659a9b50c68a8b01ff5434a3151877a8f`.
- Triggers: manual dispatch and path-filtered pushes; `contents: read`; checkout credentials disabled; 40-minute timeout.
- Installs ffmpeg, runs `yeni_kanal_tara.py` with `SCAN_BATCH=-1`, runs `scripts/genel_aday_medya_test.py` with `ADAY_TEST_GRUBU=0`, runs `scripts/ibo_bagimsiz_test_listesi.py`, then uploads three isolated IBO review artifacts and fails if absent.
- Script blob SHAs: `yeni_kanal_tara.py` `9dcbdfa078a510644da17fcb9582927cfcaae6df`; `scripts/genel_aday_medya_test.py` `bdaca46d5630b992015b8ca78a172966be135fce`; `scripts/ibo_bagimsiz_test_listesi.py` `539c17c8a8769ed8ea2d12cab937abc538b7e826`.
- Discovery fetches external M3U sources. Media testing sorts candidates, uses batches of 30, calls ffprobe with a 16-second timeout and records video/audio metadata; empty/out-of-range batches raise. The IBO list builder selects only `VIDEO_SES_VAR` rows with HTTP(S) URLs, deduplicates by URL, sanitizes channel names, validates logo URL schemes, writes separate test M3U/CSV/JSON files, and reports that no candidate is added to the main list.
- **Pipeline mismatch:** discovery uses `SCAN_BATCH=-1` as a full-scan mode, while the media test is explicitly limited to `ADAY_TEST_GRUBU=0` (the first sorted 30 candidates). Therefore the full discovered candidate set is not necessarily media-tested or included in the IBO artifact. Never report all discovered candidates as tested.
- Acceptance requires frozen discovery/media CSV fixtures, source failures, duplicate URLs and conflicting names, missing/empty reports, ffprobe timeout/nonzero exit, exact first-30 selection, artifact semantics, and proof protected playlists/device data remain unchanged. A generated list is not IBO device acceptance. **Status: reviewed-source, not accepted.**

## Batch summary

- Three previously unreviewed workflows and their directly invoked scripts were inspected against frozen Git blob SHAs.
- Cumulative documented static source reviews: **24/92**; **68/92** remain for static review, subject to canonical scope exclusions.
- Behavioral parity accepted in this batch: **0/3**; overall legacy parity remains **0/92**. Runtime security remains **0/26** and independent main-task acceptance remains **0/22**.
- No workflow was dispatched. The legacy repository remained read-only. No protected playlist, EPG, device, backup, archive, or production data was changed.
- Next: build isolated differential tests for deterministic scoring and list-building before considering any real workflow execution. Live discovery/ffprobe and IBO acceptance require explicit authorization and independent evidence.
