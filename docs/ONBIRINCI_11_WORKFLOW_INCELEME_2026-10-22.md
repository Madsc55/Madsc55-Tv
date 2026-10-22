# K1–K5: 11 eski workflow güvenlik ve işlev analizi

Kaynak: `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`. Bu dosyaların YAML içerikleri doğrudan okundu. Statik kaynak incelemesi, çalışma zamanı davranışsal kabul değildir.

| Workflow | Kaynaktan doğrulanan davranış |
|---|---|
| `test-31-protected-write-gate.yml` | Manuel statik tarama; yazma yetkisi ve komutlarını saptayıp environment işaretini raporlar; yetkilendirmeyi fiilen uygulamaz. |
| `test-32-unapproved-write-regression.yml` | Manuel/YAML veya iki aday workflow push; `yeni-kanal-arama-2026` ve `aday-yedekleme` için yedek hedefi+git push+environment denetimi; ihlalde başarısız. |
| `test-33-all-write-paths.yml` | Manuel/YAML push; workflow ve job yazma izinleri, git/API komutları; HIGH/REVIEW JSON risk envanteri; dolaylı betik yazmaları kapsam dışı. |
| `test-34-protected-write-regression.yml` | Manuel veya beş seçili workflow push; bu beşinde contents:write ve git push/commit olmamasını regex ile sınar. |
| `test-35-remaining-write-gate.yml` | Manuel veya `aday-bekletme` push; karantina workflow'unda yazma/reset bulunmaması, artifact ve credentials=false zorunluluğu. |
| `test-36-system-integration-audit.yml` | Manuel/YAML push; YAML, izin, cron, git add/commit/push riskini tarar; korunan yazma riski bulursa başarısız olur. |
| `test-37-indirect-write-audit.yml` | Manuel/YAML push; workflow'larda düz `python script.py` komutlarını regex ile bulup ilgili betik satırlarında korunan dosya veya git yazma sinyali arar; eksik betikleri raporlar ama başarısızlık koşulu yok. |
| `test-38-audit-selftest.yml` | Manuel/YAML push; test 32–37 dosyalarının salt okunur güvenlik işaretlerini ve iki gerçek koruma fonksiyonunun sentetik olumlu/olumsuz örneklerini sınar. |
| `test-39-protected-playlist.yml` | Push/PR/manuel; `scripts/protected_playlist_audit.py` çalıştırır, 5 dk; gerçek iç kontrol betikte. |
| `test-kanal-adaylari.yml` | Main push/manuel; aday yayın testi ve yerel `yedekler/TARAMA-TEST-SONUCLARI.m3u` ile JSON'u onay bekleyen artifact olarak yükler; repo push yok. |
| `toplu-sistem-kontrol.yml` | Manuel/YAML push; Python/YAML/M3U envanteri, her korunan listeden en fazla 8 HTTP Range GET, hash kontrolü, iki unittest discover ve JSON artifact; erişim oynatma kanıtı değildir. |

## Kritik bulgular

- `test-37` regex'i modül çağrıları, shell wrapper, dinamik script adı ve çok satırlı dolaylı yazmaları kaçırabilir; `NO_MATCHES_FOUND` güvenlik kabulü değildir.
- `test-31`, `test-33`, `test-36` statik işaretleri değerlendirir; production onay enforcement kanıtı değildir.
- `test-32` iki belirli workflow'a ve environment metin işaretine odaklanır; tüm 92 workflow'u kapsamaz.
- `test-39` gerçek güvenlik kapsamı için çağrılan Python betiği ayrıca okunmalıdır.

Önceki turda 88/99 olarak raporlanmıştı. Bu turda 11 yeni YAML incelendi; ancak **99 dosyanın tek tek benzersiz kapsama mutabakatı** ayrı bir makine tarafından doğrulanmadığından `99/99 tamamlandı` iddiası henüz davranışsal veya benzersiz dosya kabulü değildir. Davranışsal kabul: **0/92**. Üretim dosyaları değiştirilmedi; Actions tetiklenmedi.
