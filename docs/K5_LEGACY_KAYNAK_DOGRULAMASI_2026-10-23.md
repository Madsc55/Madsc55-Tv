# K5 — Doğrudan sabit kaynaktan karşılaştırma: üç workflow

Tarih: 2026-10-23. Eski depo `Madsc55/madsc-tv`, sabit commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. Bu belge GitHub'dan **workflow içerikleri okunarak** yapılan statik sözleşme karşılaştırmasıdır; çağrılan Python script'lerinin tüm yan etkileri bu adımda denetlenmedi ve hiçbir workflow çalıştırılmadı. Daha önce incelenmiş olabilecek satırlar tekrar sayılmadı; toplam ayrıntılı inceleme için doğrulanmış alt sınır 45/92 olarak korunur.

| Eski workflow (doğrulanan blob) | Eski tetik / gerçek workflow adımları | Beşli karşılık / açık eşdeğerlik boşluğu |
|---|---|---|
| `390-aday-tekrar-test.yml` (`b12f53a17434fe719a65edfdc968f675e1f16b95`) | Manuel veya `yedekler/tekrar_test_390.py` değişiminde push; ffmpeg kurar; 10 worker ile 20 saniyelik A/V test; 90 dk job timeout; CSV ve M3U artifact'ını `if: always()` ile yükler | **K3** teknik test + **K5** rapor/timeout yönetimi. Beşli karşılıkta aynı 390 girdisi, 20 sn/10 worker sınırı, rapor dosyası/isimleri, timeout ve başarısız koşu artifact'ı için karşılaştırma kanıtı yok. |
| `aday-bekletme.yml` (`68564680a2c32b11d1c5ed78825f01c85d0378e8`) | Manuel veya 8 belirtilen workflow/script yolunda push; `contents: read`, `persist-credentials: false`, tek concurrency grubu; 90 dk timeout; tarama, tekrar tespiti, medya testi, bekletme, takvim, 5'lik retest, kaynak puanı, öncelik ve çoklu CSV/JSON artifact | **K2** aday/kaynak + **K3** medya testi + **K5** planlama ve rapor. Yeni sistemde bu **adım sırası**, `RETEST_LIMIT=5`, rapor şemaları, push tetik eşdeğerliği ve başarısızlık artifact'ı bağımsız kanıtlanmadı. |
| `aday-logo-epg-test.yml` (`21214309014625c4a63f00ee16c9017efac6b0a7`) | Manuel veya workflow/script değişiminde push; script sözdizimi testi; `CALISANLAR.m3u` ön/son SHA256 eşitliği; `pilot_epg_channels == 5`; tüm adaylar `playlist_approved=false` ve `ready_for_playlist=false`; JSON artifact | **K3** EPG/logo birleşimi + **K1** korunan playlist değişmezliği + **K5** kanıt raporu. Beşli karşılıkta 5 pilot kanal, rapor şeması ve SHA değişmezliği için aynı girdili ayrı koşu/çıktı kanıtı eksik. |

## Kabul kararı

Üç workflow'un eski kaynak yolu ve blob SHA'sı GitHub üzerinden doğrulandı. Bu satırlarda **kaynak-temelli statik sözleşme karşılaştırması yapıldı**; bağımsız eski/yeni execution run ID, aynı input SHA, artifact hash, failure/timeout/retry sonuçları ve onay yok. **Davranışsal kabul 0/92** olarak kalır. Kaynakta `contents: read` olması çağrılan script'lerin tüm yan etkilerinin güvenli olduğunu tek başına kanıtlamaz.

Hiçbir canlı test, workflow dispatch, üretim dosyası değişikliği, eski otomasyon kapatma veya cihaz işlemi yapılmadı.
