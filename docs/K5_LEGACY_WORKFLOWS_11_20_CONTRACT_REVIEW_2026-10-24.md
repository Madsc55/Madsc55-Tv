# K5 — Sabit eski workflow'lar 11–20: doğrudan YAML sözleşmesi

Kaynak: `Madsc55/madsc-tv`, commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. Her workflow YAML'ı sabit commit'ten doğrudan okundu. Hiçbiri çalıştırılmadı. Bu statik kaynak incelemesi davranışsal kabul değildir.

| # | Workflow | Gözlenen davranış | Timeout | Artifact / risk | Aday K alanı |
|---:|---|---|---:|---|---|
| 11 | `birlesik-durum-raporu.yml` | Durum, eksik Türkçe kanal ve 155 kaynak envanteri raporu; yayın testi başlatmıyor | 5 dk | Salt-okunur JSON raporları | K2, K5 |
| 12 | `dokuzuncu-akilli-tekrar-test.yml` | Tekrar test takvimi için unittest çalıştırır | Tanımlı değil | Test sonucu | K2, K5 |
| 13 | `epg-gunluk.yml` | Günlük 03:25 UTC EPG üretimi; kontrollü dosya listesi, kapı denetimi, commit/rebase/push | Tanımlı değil | EPG XML ve rapor dosyaları; **gerçek üretim yazma yolu** | K1, K3, K5 |
| 14 | `epg-pages.yml` | EPG güncelleme workflow_run başarılıysa Pages hazırlığı/yayın zinciri; XMLTV yapısını doğrular | Tanımlı değil | Pages deploy ve XMLTV; **dışarıya yayın yan etkisi** | K3, K5 |
| 15 | `felaket-kurtarma-tatbikati.yml` | Korunan listeler için dry-run felaket kurtarma testi | 8 dk | DISASTER-RECOVERY-REPORT.json | K1, K4, K5 |
| 16 | `genel-aday-medya-test.yml` | Salt-okunur aday keşfi, ffprobe ile video/ses testi | 40 dk | CSV/JSON test raporu | K2, K3, K5 |
| 17 | `genis-kanal-tarama.yml` | Çok kaynaklı salt-okunur tarama ve yayın testi | 55 dk | Geniş tarama CSV raporu | K2, K3, K5 |
| 18 | `ibo-bagimsiz-test-listesi.yml` | Aday keşfi, medya testi, ayrı IBO test playlist'i üretimi | 40 dk | İzole IBO M3U/CSV/JSON | K2, K3, K5 |
| 19 | `ibo-epg-kimlik-denetimi.yml` | CALISANLAR.m3u ile beş kanallı IBO XMLTV pilotunu salt-okunur eşleştirir | 10 dk | JSON kimlik denetimi | K3, K5 |
| 20 | `ibo-yedek-kalite.yml` | Yedek akışları ffprobe ile kalite ölçümü | 25 dk | CSV kalite raporu | K3, K4, K5 |

## Kritik bulgular

- `epg-gunluk.yml` `contents: write` iznine sahiptir ve EPG dosyalarını commit/push eder. Karşılaştırma testinde workflow_dispatch ile çalıştırılmamalı; yalnızca statik analiz veya tamamen izole fixture kullanılmalıdır.
- `epg-pages.yml` Pages deploy ve id-token izni kullanır. Gerçek deploy, açık onay ve yayın kapıları olmadan davranışsal test için tetiklenmemelidir.
- `ibo-epg-kimlik-denetimi.yml` mevcut korunan listeyi okur; output RUNNER_TEMP altındadır. Bunun gerçek workflow sonucu burada yürütülmedi.
- Medya testleri canlı stream URL'lerine erişebilir; çevrimdışı kabul koşusunda ağ erişimi kapatılmalı ve kontrollü fixture/mocks kullanılmalıdır.

Bu 10 workflow için trigger, komut sırası, izin, timeout ve artifact sözleşmesi statik olarak kaydedildi. Kapsam envanterindeki SHA'lar ile her dosyanın içerik SHA eşleşmesi ayrıca denetlenmelidir. Script davranışları, eski/yeni ayrı koşular ve artifact/yan etki SHA karşılaştırmaları olmadan kabul verilmez. Bu belge kabul sayısını artırmaz. İlk 20 workflow doğrudan incelenmiştir; kalan 72 için inceleme gereklidir.
