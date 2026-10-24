# K5 — İlk 10 sabit eski workflow'un doğrudan sözleşme incelemesi

Kaynak depo: `Madsc55/madsc-tv`
Sabit kaynak commit: `ca374df3b9585c0d76a078db9536150ebbc260f7`
İnceleme yöntemi: YAML'lar sabit commit'ten doğrudan okundu. Eski workflow'lar çalıştırılmadı. Bu kayıt davranışsal eşdeğerlik kabulü değildir.

| Eski workflow | Davranış sözleşmesi | Süre sınırı | Artifact / çıktı | Beşli sistem adayı | Yan etki / kabul engeli |
|---|---|---:|---|---|---|
| `390-aday-tekrar-test.yml` | ffmpeg kurar; `yedekler/tekrar_test_390.py` ile 10 worker'lı paralel 20 saniyelik ses/video testi | 90 dk | CSV ve teknik doğrulananlar M3U | K3, K5 | M3U artifact'i gerçek çıktı; aynı fixture ve çıktı SHA eşlemesi gerekli |
| `aday-bekletme.yml` | Kanal keşfi, tekrar raporu, medya testi, aday bekletme, yeniden test takvimi, en çok 5 tekrar, kaynak puanı ve öncelik raporu | 90 dk | `aday-bekletme-raporu` (yol kapsamı YAML'da kontrol edilmeli) | K2, K3, K5 | Çok aşamalı durum geçişleri; aday dosyaları ve retry eşdeğerliği gerekli |
| `aday-logo-epg-test.yml` | Python syntax; CALISANLAR.m3u SHA öncesi/sonrası; 5 EPG pilotu ve playlist onay koruması | 10 dk | `madsc_kesif/candidate_epg_logo_join.json` | K1, K2, K3, K5 | Korunan liste değişmezliği açık sözleşme |
| `aday-oncelik-kontrol.yml` | İzole geçici dizinde örnek adaylarla öncelik sıralamasını sınar | Workflow timeout tanımlı değil | Geçici CSV raporu | K2, K5 | Ana listeye değil temp fixture'a yazmalı |
| `aday-yedekleme.yml` | Teknik olarak başarılı adayları yedek taslağına aktarır | 30 dk | Onay bekleyen M3U artifact'i | K2, K4, K5 | GitHub token kullanımı ve hedef yol davranışı incelenmeden canlı koşturulmamalı |
| `akilli-aday-puanlama.yml` | Aday keşfi, gerçek ffprobe, teknik kanıtla puanlama | 55 dk | CSV/JSON rapor artifact'leri | K2, K3, K5 | Ağ/harici yayın probe'u; salt-okunur, onaylı test fixture'ı gerekir |
| `altinci-aday-tekrar-test.yml` | Retry uygunluğu, HLS ve ffprobe davranışını mock'larla test eder; sonra bekleyen adayları test eder | 20 dk | Workflow devamında belirlenir | K2, K3, K5 | Mock test ve gerçek ağ testi ayrılmalı; retry sınırı korunmalı |
| `automatic-png-logos.yml` | Logo üretimi/görsel kanıtı; CALISANLAR.m3u değişirse restore etmeye çalışır | 15 dk | Logo ve görsel inceleme artifact'leri | K1, K3, K5 | Üretim dosyası üzerinde geçici yazma bile risk; izole checkout/fixture şart |
| `besinci-zaman-asimi-test.yml` | 65 saniyelik subprocess timeout'unun aday durumunu yanlışlıkla bozuk saymadığını test eder | Workflow timeout tanımlı değil | Konsol testi | K3, K5 | Timeout ve retry semantiği eşleşmeli |
| `birlesik-aday-raporu.yml` | Cache geri yükleme, keşif, ffprobe, genel medya testi, puanlama, kararlılık ve konsolide rapor | 60 dk | CSV/JSON konsolide rapor | K2, K3, K5 | Cache anahtarı, zaman serisi ve artifact çıktıları aynı girdi ile karşılaştırılmalı |

## Kapanış ölçütü

Bu 10 YAML için tetikleyici, komut sırası, timeout, artifact ve risk alanları kaynak metninden çıkarıldı. Ancak çağrılan script'lerin tüm davranışları burada kanıtlanmış değildir. Her bir eski workflow için sabit kaynak blob SHA'sı, yeni workflow/komut karşılığı, aynı fixture SHA'sı, ayrı yürütme kimlikleri, çıkış kodu, stdout/stderr SHA, artifact SHA, yan etki manifesti, timeout ve retry kanıtı olmadan davranışsal kabul verilmez.

Bu belge eski workflow'ları çalıştırmaz, canlı ağı başlatmaz, üretim dosyası değiştirmez ve davranışsal kabul sayısını artırmaz. Toplam 92 workflow'un sadece ilk 10'u doğrudan incelenmiştir; kalan 82 için ayrı kaynak incelemesi gerekir. Bu ilk 10, önceki 45/92 statik inceleme sayısına mükerrerlik denetimi yapılmadan eklenmemelidir.
