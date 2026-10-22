# Kapsam açığı: son 13 eski workflow'un doğrudan YAML incelemesi

Kaynak `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`. Bu 13 YAML okundu; çalışma veya üretim değişikliği yapılmadı.

| Workflow | Kaynakta tanımlı görev |
|---|---|
| `madsc-son-kontrol-kurtarma-teshis.yml` | Manuel/YAML push; kayıtlı sonuç JSON'u ve son 20 koşunun GitHub API teşhisi, unit test; yayın denemesi yok. |
| `madsc-son-kontrol.yml` | Günlük 06:10 UTC, manuel, başarılı üç aşamalı workflow_run; `final_validation.py` ile 5 dakikalık süreklilik testi; yalnız rapor JSON'larını ana dala push eder; 10 kez yarışma korumalı retry. Write ve actions write yetkisi var. |
| `madsc-toplu-butunluk.yml` | Manuel/script push; `bulk_integrity_gate.py`, arşiv/tekrar/yedek bütünlük JSON artifact. |
| `madsc-tum-sistem-yedek.yml` | Ayın 1 ve 15'i 05:40 UTC veya manuel; repo ayar envanteri ve `full_system_backup.py`; tar.gz ve JSON artifact, 30 gün saklama. Offsite kalıcılık değil. |
| `madsc-turk-kanal-geri-sec.yml` | YAML push; `recover_turkish_backups.py` ülke kaynaklarına göre geri seçer, `CALISANLAR.m3u` değiştirip gate+commit+push yapar. |
| `madsc-yedek-turk-ayir.yml` | YAML push; `keep_turkish_backups.py` yabancı/belirsiz yedekleri arşive ayırır, `CALISANLAR.m3u` ve raporları gate+commit+push yapar. |
| `madsc-yedekler-aktarim-test.yml` | Manuel/kod push; `test_yedekler_teknik_aktar` unittest; üretim aktarımı değil. |
| `madsc-yedekler-sayi-duzelt.yml` | Manuel/YAML push; `sync_yedekler_category_count.py` ana liste grup sayısını düzeltir, gate+commit+push. |
| `oncelikli-kanal-dogrulama.yml` | Manuel/script push; ffprobe öncelikli kanallar, CSV/JSON artifact; salt okunur. |
| `onikinci-hata-siniflandirma-test.yml` | Manuel/kod push; 403, coğrafi engel, timeout, medya ve belirsiz hata için sentetik sınıflandırma ve CSV testleri. |
| `publish-iptv-png-logos.yml` | Manuel veya SVG push; CairoSVG ile 320x320 PNG üretimi, gate+commit+push; logo dosyası yazarı. |
| `sekizinci-tekrar-raporu-test.yml` | Manuel/kod push; iki kaynak ve aynı kaynak URL tekrarları için sentetik CSV testi. |
| `sozcu-akit-ozel-test.yml` | Manuel/script push; Sözcü/Akit ffprobe aday testi, CSV artifact. |

## Güvenlik ve eşdeğerlik ayrımı

- `madsc-son-kontrol`, `madsc-turk-kanal-geri-sec`, `madsc-yedek-turk-ayir`, `madsc-yedekler-sayi-duzelt`, `publish-iptv-png-logos` gerçek depo yazarıdır. Üretim korumaları ve çağrılan Python betiklerinin yan etkileri ayrıca incelenmelidir.
- Tam sistem yedeği yalnız Actions artifact üzerinde 30 gün tutulur; bağımsız, kalıcı, geri yüklenebilir offsite yedek kanıtı değildir.
- Son kontrol 5 dakikalık teknik süreklilik ölçümü; gerçek oynatıcı uyumluluğu veya kullanıcı onayı yerine geçmez.

Önceki 10 inceleme belgesi 70 benzersiz YAML adını kapsıyordu. Birinci 8 + ikinci 8 + bu son 13 ile **99/99 benzersiz YAML adının doğrudan kaynak okuması bu üç tur ve önceki belgelerle belgelenmiştir**. Bu, 99 betiğin bütün yan etkilerinin veya 92 davranışsal eşdeğerliğin kanıtı değildir. Davranışsal kabul **0/92**, 26 kural üretim kabulü **0/26**.
