# K5 — Eski workflow 68–77 doğrudan YAML incelemesi

Kaynak: `Madsc55/madsc-tv` @ `ca374df3b9585c0d76a078db9536150ebbc260f7`. On YAML doğrudan okundu; çalıştırma ve üretim değişikliği yapılmadı. Bu statik sözleşme kaydıdır, **davranışsal eşdeğerlik kabulü değildir**.

| # | Workflow | Kaynaktan doğrulanan sözleşme | Timeout | K adayı |
|---:|---|---|---|---|
| 68 | `test-23-live-stream.yml` | CALISANLAR/YENILER listesinden URL seçerek HTTP Range canlı erişim testi; önce/sonra SHA | 12 dk | K3/K5; ağ isteği, çalıştırılmamalı |
| 69 | `test-24-system-audit.yml` | Python AST, YAML, M3U ve yazma izni envanteri | 15 dk | K1/K5 |
| 70 | `test-25-full-project-readonly.yml` | Proje geneli salt-okunur Python/YAML/liste/yedek denetimi ve korunan dosya SHA | 20 dk | K1/K4/K5 |
| 71 | `test-26-automation-safety.yml` | Workflow YAML parse, yazma izni ve mutasyon komutu statik taraması | 10 dk | K1/K5 |
| 72 | `test-27-pipeline-contract.yml` | Keşif/test/tekrar/yedek/entegrasyon workflow dosyası varlığı ve korunan liste SHA | 10 dk | K1–K5 |
| 73 | `test-28-approval-gate.yml` | Aday durum sınıflandırma ve korunan dosya statik denetimi | 10 dk | K1/K5 |
| 74 | `test-29-write-path-audit.yml` | YAML'da git push/commit, API yazma ve korunan yol işaretlerini tarar | 10 dk | K1/K5 |
| 75 | `test-30-write-risk-report.yml` | Yazma izni, mutasyon ve korunan yol bulguları için statik risk kaydı | 10 dk | K1/K5 |
| 76 | `test-31-protected-write-gate.yml` | Yazma yetkili workflow'larda environment işareti ve korunan yol kontrolü | 10 dk | K1/K5 |
| 77 | `test-32-unapproved-write-regression.yml` | İki yedek workflow'unda git push + yedek hedefi + environment gate yokluğu regresyonu | 8 dk | K1/K4/K5 |

## Kritik sınırlamalar

- #68 canlı ağ erişimi yapar; çevrimdışı fixture olmadan çalıştırılmamalıdır.
- #69–76 YAML/regex statik denetimleri **gerçek çalışma zamanı yetki onayını kanıtlamaz**. #76'nın kaynak metninde bu sınırlama açıkça kayıtlıdır.
- #77 yalnız iki hedef workflow için kural taraması yapar; tüm korunan yazma yollarının kapatıldığını kanıtlamaz.
- İlk 77 YAML doğrudan okundu; kalan 15. Eski/yeni izole yürütme ve artifact/yan etki kanıtları henüz oluşturulmadı. **Davranışsal kabul 0/92**.
