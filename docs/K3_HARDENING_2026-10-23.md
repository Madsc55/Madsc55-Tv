## Ek regresyon — EXTINF görünen adından sahte tvg-id alınması
- Yeni hata: önceki regex tüm `#EXTINF` satırını taradığı için virgülden sonraki görünen kanal adı `News tvg-id="trt1.tr"` ise bu metin gerçek nitelikmiş gibi algılanabilirdi.
- Düzeltme commit'i: `2e1ee36d2f54b9d8a6b72eb43751ab4e60224c9f`; artık regex yalnız virgülden önceki nitelik bölümünde çalışıyor.
- Yeni regresyon commit'i: `7ced6524a166c76c1994a7f0d79574c519c7dc17`; `tests/test_epg.py` şu anda 15 EPG test fonksiyonu içeriyor.
- Bu iki yeni commit'in Actions koşuları, diğer K1–K5 commit'leri aynı concurrency grubuna gönderildiği için iptal edildi. Son başarılı ortak offline koşu #99 / `39868459061` 1016 testi geçmişti ve önceki 14 EPG testini içeriyordu; yeni 15. test henüz başarılı CI ile doğrulanmış değil.
- Doğru sonraki adım: yeni kod commit'leri durduğunda tek bir güncel main commit'i için offline suite'in tamamlanmasını beklemek/doğrulamak.

---

## CI yeniden doğrulaması — 2026-10-23
- Güncel ortak offline suite, run #99 / ID `39868459061`, commit `a0469c34ec9a8642acffdddfbda55dadf9d39aba`: **completed / success**.
- Log: `tests_discovered=1016`, `test_exit_code=0`, `tests_passed=true`, `all_offline_gates_passed=true`; K3 fixture category success.
- Bu commit'te `madsc/epg.py` blob'u `762a5b4a09cb2f8d9ea6b87c52b48ef9722b393b`, `tests/test_epg.py` blob'u `b1deb2b544250526b90a98eeb1249d22cfec9aaa`; test dosyası 14 EPG test fonksiyonu içeriyor. Yani header/tvg-id sertleştirmesi ve ilgili iki yeni regresyon bu başarılı koşunun içindedir.
- Bu sonuç önceki K5 hatasının da ortak suite'te giderilmiş haliyle sonraki commit'te yeniden geçtiğini gösterir; K3'e özel canlı yayın kabulü değildir.
- Mevcut main HEAD run commit'i `a0469c34ec9a8642acffdddfbda55dadf9d39aba` ile eşleşiyor.

---

# K3 EPG hardening follow-up — 2026-10-23

Repository: Madsc55/Madsc55-Tv
Branch: main

## Changes committed
- `dece8693d378465d8e118665ee2a9e38cac03efd`: M3U header validation now checks the first non-empty line as a complete header token, rejecting malformed prefixes such as `#EXTM3U-invalid`.
- `dcdf7cf8aead168567d8bb1a38de0cdb6577a1b5`: M3U `tvg-id` is now matched as a whitespace-delimited attribute rather than a word-boundary substring. This prevents `not-tvg-id="..."` from being misread as a real `tvg-id`.
- `e2339f700445353eeb45773283a36f47208c6064`: added a regression for malformed M3U header suffixes.
- `a26a94d7ca8286f72cd5ec513db9c265c88b6d20`: added a regression proving `not-tvg-id` does not satisfy the required channel id.
- Current `tests/test_epg.py` has 14 test functions; current `madsc/epg.py` and test file were fetched back from GitHub and their blob IDs checked.

## CI state
- The EPG-specific push runs for the latest changes were cancelled by the repository's shared workflow concurrency while multiple K1–K5 commits were arriving: run `39868327329` (validator fix) and run `39868336469` (new regression test) both concluded `cancelled`.
- Earlier run #89 (`39867960099`) passed the repository offline gate, but it predates these latest M3U hardening changes. Do not claim that the current 14-test file has a passing CI run until a run on a commit containing these changes completes.
- Other recent offline runs showed an unrelated K5 failure in `test_manifest_serialization_failure_cleans_partial_bundle_and_preserves_source`; it expected the simulated serialization error but got `Output must be outside the source directory tree`. This was not changed in the K3 workstream.

## Remaining acceptance
- These are structural EPG parser changes only. Real HLS video/audio probing, 6+ hour continuity, live Pages/XMLTV chain, IBO Player Pro device EPG rendering, and logo identity are not yet confirmed.
- No production playlist, XMLTV feed, device settings, favorites, logos, backup, or archive was modified.
- K3-13 remains in progress until live/device evidence is recorded.
