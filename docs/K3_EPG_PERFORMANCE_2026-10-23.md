## K3 XMLTV güvenlik kontrolü — 2026-10-23
- IBO Player Pro cihaz doğrulaması en son kullanıcı tarafından yapılacak; bu aşamada cihaz testini isteme.
- Run `39870824796`, tested commit `0e2d5e6844f93f4e04970f9992018d00ad593eaf`: **success**, `tests_discovered=1056`, `test_exit_code=0`, `tests_passed=true`, `all_offline_gates_passed=true`; 18 EPG testini içerir.
- `2c5de38eb36ebaefe6160535392e900a3003a4a3`: XMLTV içeriğinde `<!DOCTYPE` veya `<!ENTITY` bildirimi tespit edilirse XML ayrıştırılmadan önce reddedilir.
- `1cd621757362cd39b34b21d45b022e536ed112ed`: DTD/entity içeren XMLTV için regresyon testi; EPG test sayısı 19.
- **19. test için henüz başarılı CI sonucu teyit edilmedi**. Gerçek HLS video/ses, 6+ saat süreklilik, Pages/XMLTV ve logolar açık; cihaz doğrulaması en son.
- Üretim playlist, XMLTV, logo, favori, yedek, arşiv, cihaz verileri değiştirilmedi.

---

## Yeni K3 kontrolü — 2026-10-23
- Kullanıcı IBO Player Pro cihaz testini en sona bıraktı; cihaz kabulünü yalnız kullanıcı deneyecek ve sonucunu bildirecek.
- `39870641608` GitHub Actions run'u **success**; tested commit `36155ba9f7b9e2684d86f79a666cdeeb82d87fee`, `tests_discovered=1049`, `test_exit_code=0`, `tests_passed=true`, `all_offline_gates_passed=true`. Bu commit 17 EPG testini ve lineer duplicate-ID kontrolünü içeriyor.
- Yeni kod commit'i `7a87a130b818f364df1d11364e4ea9f3a821a134`: bozuk M3U girdisindeki NUL baytları `ValueError` ile reddedilir.
- Yeni test commit'i `291f6c3e7594f2e2d015db9f74cab2e2a3306432`: NUL bayt regresyonu; EPG test fonksiyonu sayısı 18.
- **18. test için başarılı CI kanıtı henüz yok**; 1049-testlik başarılı koşu bu son iki commit'ten öncedir. CI tamamlanana kadar sonucu geçti diye kaydetme.
- K3 canlı HLS video/ses, süreklilik, Pages/XMLTV zinciri, logo kimliği ve en son kullanıcı cihaz kabulü açık. Üretim verilerine dokunulmadı.

---

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
