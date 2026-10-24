# K5 — Eski workflow 48–57 doğrudan kaynak sözleşmesi

Kaynak: `Madsc55/madsc-tv` @ `ca374df3b9585c0d76a078db9536150ebbc260f7`. On workflow YAML'ı doğrudan okundu. Çalıştırma veya üretim yazması yapılmadı; davranışsal kabul değildir.

| # | Workflow | Temel davranış | Süre | Risk / aday |
|---:|---|---|---|---|
| 48 | `madsc-turk-kanal-geri-sec.yml` | `recover_turkish_backups.py`, arşiv raporu, CALISANLAR commit/push | 15 dk | Korunan liste yazma; K1/K4/K5 |
| 49 | `madsc-uc-asama.yml` | Failure gate, doğrulama testleri, aday kuyruğu, üç aşamalı medya doğrulama | 40 dk | `contents:write` ve `actions:write`; K1/K3/K5 |
| 50 | `madsc-yedek-turk-ayir.yml` | `keep_turkish_backups.py`, ayrılanlar arşivi ve CALISANLAR commit/push | 15 dk | Korunan liste yazma; K1/K4/K5 |
| 51 | `madsc-yedekler-aktarim-test.yml` | `test_yedekler_teknik_aktar` unittest | Tanımlı değil | Ağsız fixture'a uygun; K4/K5 |
| 52 | `madsc-yedekler-sayi-duzelt.yml` | YEDEKLER kategori sayısı senkronizasyonu, CALISANLAR commit/push | Tanımlı değil | Korunan liste yazma; K1/K4/K5 |
| 53 | `oncelikli-kanal-dogrulama.yml` | ffprobe öncelikli akış testi, CSV/JSON artifact | 30 dk | Canlı yayın testi; K3/K5 |
| 54 | `onikinci-hata-siniflandirma-test.yml` | HTTP403/coğrafi engel/timeout/başarılı/belirsiz hata senaryoları; temp CSV | 5 dk | Offline test için uygun; K3/K5 |
| 55 | `publish-iptv-png-logos.yml` | SVG→PNG dönüştürme ve PNG git commit/push | Tanımlı değil | `contents:write`, logo yayınlama; K1/K3/K5 |
| 56 | `sekizinci-tekrar-raporu-test.yml` | Çoklu kaynaktaki aynı URL için tekrar raporu, geçici CSV fixture | 5 dk | Offline test için uygun; K2/K5 |
| 57 | `sozcu-akit-ozel-test.yml` | İki özel kanal için ffprobe ve CSV artifact | 25 dk | Canlı medya testi; K3/K5 |

## Özel bulgular

- #48, #50, #52 korunan `CALISANLAR.m3u` dosyasını commit/push eder; üretimde veya normal CI'da test amacıyla çalıştırılmamalı.
- #49 workflow YAML'ının ilk bölümü incelendi; tam adım ve artifact sözleşmesi ayrıca okunmalı.
- #55 yalnız PNG yazsa da `main` dalına yayın yapar; izole çalışma gerektirir.
- #54 ve #56 için geçici dizinli test senaryoları kaynakta açıkça bulunuyor. Bunlar bağımsız fixture yürütme pilotu için düşük riskli adaylardır.
- İlk 57 YAML doğrudan kaynak incelemesinde ele alındı; kalan 35 workflow var. Çağrılan script semantiği ve bağımsız eski/yeni yürütme kanıtları henüz yok; **davranışsal kabul 0/92**.
