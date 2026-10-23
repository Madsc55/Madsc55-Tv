# K5 — On eski workflow: uçtan uca zincir ve kabul engelleri

Tarih 2026-10-23. Eski depo `Madsc55/madsc-tv`, sabit commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. Aşağıdaki on YAML doğrudan GitHub'dan okundu ve blob SHA kimlikleri doğrulandı. Eşleştirmeler statik adaydır; davranışsal kabul değildir.

| Eski workflow ve blob | Aday aşamalar | Eski kaynak sözleşmesi | Açık kanıt |
|---|---|---|---|
| `.github/workflows/madsc-sistem-saglik-denetimi.yml` / `c3c18155d13c2ca5e1a76304729fbcc6739849a5` | K1/K5 | Ayın 1,15'i 05:17; YAML parse, unit test, son 100 Actions run raporu; kritik audit hatası job fail | Güncel Actions API kanıtı |
| `.github/workflows/madsc-son-kontrol-kurtarma-teshis.yml` / `471540a306c4146fa12123510a4c70dcfe1356eb` | K3/K5 | 10 dk; önceki summary/results kontrolü, son kontrol run geçmişi; canlı probe yok | Kaydedilmiş rapor şeması |
| `.github/workflows/madsc-son-kontrol.yml` / `08871f1b397184459a093606c2519e1c19e5167a` | K1/K3/K5 | 06:10 günlük veya başarılı workflow_run; 110 dk; 5 dk A/V süreklilik; 10 kez rapor push retry | Canlı 5 dk test ve yan etki karşılaştırması |
| `.github/workflows/madsc-toplu-butunluk.yml` / `d7456c7a5526350b0d52e39b6708cf288d209dbf` | K1/K4 | 15 dk; arşiv/YEDEKLER bütünlük script'i, JSON artifact if:always | Bağımsız arşiv SHA kanıtı |
| `.github/workflows/madsc-tum-sistem-yedek.yml` / `f56db59dc9a8a12f21296a80ea53b602340454ef` | K4 | Ayın 1,15'i 05:40; 20 dk; tar.gz yedek ve geçici restore, 30 günlük artifact | Harici bağımsız restore ve artifact SHA |
| `.github/workflows/madsc-turk-kanal-geri-sec.yml` / `ee4538c2b9e11f5589d8babacd9f3ff39457cc9b` | K1/K2/K4 | Ülke kaynağına göre geri seçme, CALISANLAR.m3u commit/push | Yazma izni, kaynak kökeni, onay |
| `.github/workflows/madsc-uc-asama.yml` / `93c3a87372b1dfbe80ba9e59dabc2180511112ae` | K1/K2/K3/K5 | 40 dk; due aday filtresi; koşullu ffmpeg; 10 rapor push retry; kalan varsa kendini dispatch | Çift tetikleme/sonsuz döngü ve timeout eşdeğerliği |
| `.github/workflows/madsc-yedek-turk-ayir.yml` / `67b12b441fab5fa57eded1a7684ebf24e7d819c2` | K1/K2/K4 | Türk/yabancı/kimliği belirsiz ayrımı; CALISANLAR.m3u commit/push | Kimlik/lisans ve korunan yazma kanıtı |
| `.github/workflows/madsc-yedekler-aktarim-test.yml` / `e4de46aa7edbd84b8dc3bdda0e3d75a39421118b` | K1/K4 | Salt-okunur YEDEKLER aktarım unittest | Güvenli aktarım fixture eşdeğerliği |
| `.github/workflows/madsc-yedekler-sayi-duzelt.yml` / `feb92ccf12c62b3818cac164f0effe319083872f` | K1/K4 | YEDEKLER kategori sayısı düzeltme, CALISANLAR.m3u commit/push | Korumalı playlist değişmezliği ve kullanıcı onayı |

## Önemli riskler

`madsc-uc-asama.yml` kalan aday varsa kendi workflow'unu tekrar dispatch eder. `madsc-son-kontrol.yml` ayrı raporları 10 kez push retry ile kaydeder. `madsc-turk-kanal-geri-sec.yml`, `madsc-yedek-turk-ayir.yml` ve `madsc-yedekler-sayi-duzelt.yml` korunan `CALISANLAR.m3u` dosyasını commit/push zincirine sokar. Yeni beşli sistemde K1 güvenlik kapısı, K2 kimlik/köken, K3 canlı kanıt, K4 yedek ve K5 retry/rapor birlikte sınanmalıdır.

Hiçbir workflow dispatch edilmedi, hiçbir üretim dosyası değiştirilmedi. Eski script'lerin tüm içeriği ve eski/yeni bağımsız run artifact'ları henüz doğrulanmadı. Önceki statik 45/92 sayısı olası mükerrerlik nedeniyle artırılmadı; davranışsal kabul 0/92 ve üretim geçişi engelli.
