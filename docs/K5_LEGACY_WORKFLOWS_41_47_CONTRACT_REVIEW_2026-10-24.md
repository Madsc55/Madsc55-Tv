# K5 — Eski workflow 41–47 doğrudan YAML incelemesi

Kaynak: `Madsc55/madsc-tv` sabit commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. Yedi YAML doğrudan okundu; hiçbir workflow çalıştırılmadı. Bu belge **statik sözleşme** kaydıdır; bağımsız davranışsal eşdeğerlik kabulü değildir.

| # | Workflow | Doğrulanan temel sözleşme | Timeout | Yan etki / risk | Aday |
|---:|---|---|---|---|---|
| 41 | `madsc-otomatik-devam.yml` | Manuel tetiklenir; yalnız çift tetikleme kaldırıldı mesajı verir, yeni tur başlatmaz | Tanımlı değil | Gerçek otomatik devam olarak eşleştirilmemeli | K5 |
| 42 | `madsc-rule24-test.yml` | `test_workflow_failure_gate` unittest çalıştırır | Tanımlı değil | Fail-closed hata zinciri semantiği korunmalı | K1/K5 |
| 43 | `madsc-sistem-saglik-denetimi.yml` | Ayın 1/15'i YAML parse, unittest, sistem sağlık denetimi, Actions son 100 run API raporu | 12 dk | `continue-on-error: true` denetim adımı; başarısızlık sinyalini maskeleyebilir | K1/K5 |
| 44 | `madsc-son-kontrol-kurtarma-teshis.yml` | Son kontrol testleri, mevcut rapor dosyaları ve GitHub Actions koşu durumlarını salt-okunur inceler | 10 dk | Gerçek yayın probe veya playlist yazması yapmaz | K1/K3/K5 |
| 45 | `madsc-son-kontrol.yml` | Günlük 06:10 UTC veya başarılı üç aşamalı doğrulama sonrası 5 dk medya sürekliliği; artifact ve rapor git yazma | 110 dk | `contents: write`, `actions: write`; `main` reset/push ve ağ testi riski | K1/K3/K5 |
| 46 | `madsc-toplu-butunluk.yml` | Arşiv, tekrar ve yedek bütünlük kontrol script'i; JSON artifact | 15 dk | Salt-okunur kapsam kanıtı ve artifact SHA eşlemesi gerekir | K4/K5 |
| 47 | `madsc-tum-sistem-yedek.yml` | Ayın 1/15'i repo ayar envanteri, tam tar.gz arşivi, geçici restore doğrulaması | 20 dk | Arşiv kapsamı ve geri yükleme bütünlüğü; GitHub token yalnız envanter için | K4/K5 |

## Açık engeller

1. #43'teki `continue-on-error` davranışı yeni sistemde başarısızlık algılamayı etkileyebilir. Testte ayrı kontrol edilmeli.
2. #45 canlı yayın testi ve GitHub yazma yetkisi içerir; workflow dispatch edilmemeli, yalnız ağsız izole fixture ile sınanmalı.
3. #47 için arşiv SHA ve geçici restore sonucu eşleşmeden K4 davranışsal kabul verilmemeli.
4. İlk 47 YAML bu inceleme serisinde doğrudan okundu; kalan 45 YAML için doğrudan kaynak incelemesi gerekiyor. Önceki 45/92 raporuyla mükerrerlik denetlenmeden toplam sayılar birleştirilmez. **Davranışsal kabul 0/92**.
