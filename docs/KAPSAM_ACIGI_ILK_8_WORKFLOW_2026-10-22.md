# İlk sekiz belge kapsam boşluğu: doğrudan YAML incelemesi

Sabit kaynak: `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`. Bu sekiz YAML doğrudan okundu; yalnız statik analiz, Actions koşusu değildir.

| YAML | İşlev ve risk |
|---|---|
| `iptv-test.yml` | Çarşamba 06:30 UTC, manuel veya genel komut push; `iptv_test.py` aday M3U test eder; `CALISANLAR.m3u`, hata ve CSV'yi artifact olarak sunar. Salt okunur token üretim dosyası değişmezliği demek değildir; betik yerel dosya yazabilir. |
| `k1-protected-write-tests.yml` | Push/manuel; 26 kural/92 workflow raporu, negatif testler, izin risk envanteri, başlangıç/son hash; rapor artifact. Ana dalla fark adımı `continue-on-error`, son kapı başarısızlığına bağlanmış. |
| `kanal-kararlilik.yml` | Manuel/script push; cache geçmişini geri yükler, ffprobe öncelikli kontrol, kararlılık karşılaştırması, yeni cache ve artifact; zaman serisi cache geri dönüşüne bağlı. |
| `kaynak-puanlama-kontrol.yml` | Manuel/kod push; `kaynak_guven_puani.py` py_compile ve unittest; gerçek kaynak doğruluğu testi değildir. |
| `madsc-01-guvenlik.yml` | Manuel veya workflow_call; K1 raporları, 26 kural kanıtı, çoklu regresyon, SHA256 ve son başarısızlık kapısı; 26 runtime kanıtı tamam değilse fail. |
| `madsc-02-kesif.yml` | Günde dört cron zamanı, manuel veya workflow_call; geçmiş restore, keşif, aday EPG/logo eşleme, geniş kaynak tarama, regresyon, hash ve fail gate. Salt okunur token; yerel raporlar artifact. |
| `madsc-03-kanal-test.yml` | Günlük 06:40 UTC, eski dal push, manuel/call; kimlik/EPG/logo, medya, puanlama, 100 kanallık parti, regresyon ve hash; her koşu tam liste testi değildir. |
| `madsc-04-arsiv-yedek.yml` | Manuel/call; izole git restore, yedek kanıtı, arşiv tutarlılığı, disaster dry-run, regresyon ve hash; offsite kopya ve tarihsel restore doğrulanmış sayılmaz. |

Önemli: `madsc-02-kesif` içindeki aday EPG/logo join çalışır; eski `madsc-birlesik-kesif` workflow'unda aynı işlem devre dışıdır. Bunlar davranışsal olarak otomatik eşdeğer değildir. `madsc-03` 100 kanallık parti denetler, tam kapsam zaman içinde ayrıca kanıtlanmalıdır.

Bu 8 dosya, önceki 10 belgede adı bulunmayan 29 dosyadan seçilmiştir. Böylece **o belge kümesi + bu notta dosya adıyla eşleşen en az 78/99**; diğer eski belgeler henüz mutabakata dahil edilmemiştir. Davranışsal kabul **0/92**, güvenlik üretim kabulü **0/26**.
