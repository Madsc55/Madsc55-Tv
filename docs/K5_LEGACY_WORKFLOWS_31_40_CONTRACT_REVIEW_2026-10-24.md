# K5 — Eski workflow 31–40: sabit YAML sözleşmeleri ve yazma riski

Kaynak `Madsc55/madsc-tv` commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. Her YAML doğrudan okundu, çalıştırılmadı. **Statik kaynak incelemesi, davranışsal kabul değildir.**

| # | Eski workflow | Kaynakta gözlenen komut/sözleşme | Süre | Risk ve K eşlemesi |
|---:|---|---|---|---|
| 31 | `madsc-genis-kaynak-kontrol.yml` | Haftalık ve aylık kaynak taraması; artifact; rapor dizinini çakışma denetimiyle commit/push | 45 dk | `contents:write`, `actions:write`; K1/K2/K5 |
| 32 | `madsc-ibo-3-5281.yml` | Yalnızca güvenli dry-run uyarısı, otomatik mutasyon kapalı | 15 dk | K1/K4/K5; gerçek ayırma yapılmıyor |
| 33 | `madsc-ibo-354-classify.yml` | `archive_backups_354_classified.py`; CALISANLAR ve arşiv raporu git add/commit/push | Tanımlı değil | **Korunan liste yazma**; K1/K4/K5 |
| 34 | `madsc-ibo-364-355-364.yml` | `archive_backups_355_364.py`; yabancı liste değişmezliği kontrolü; CALISANLAR ve arşiv commit/push | Tanımlı değil | **Korunan liste yazma**; K1/K4/K5 |
| 35 | `madsc-ibo-398-16-49.yml` | `archive_backups_16_49.py`; arşiv ve CALISANLAR commit/push | Tanımlı değil | **Korunan liste yazma**; K1/K4/K5 |
| 36 | `madsc-ibo-530-archive.yml` | `archive_backups_399_onward.py`; arşiv ve CALISANLAR commit/push | Tanımlı değil | **Korunan liste yazma**; K1/K4/K5 |
| 37 | `madsc-ibo-6115-second.yml` | `apply_ibo_6115_second.py`; kullanıcı kararları, arşiv, CALISANLAR commit/push | 15 dk | **Korunan liste yazma**; K1/K4/K5 |
| 38 | `madsc-ibo-ilk-239.yml` | `apply_ibo_first_239_decisions.py`; karar CSV, rapor ve CALISANLAR commit/push | 15 dk | **Korunan liste yazma**; K1/K4/K5 |
| 39 | `madsc-ibo-kararlar-grup1.yml` | `apply_ibo_decisions_group1.py`; kullanıcı kararlarını raporlar ve CALISANLAR commit/push | 15 dk | **Korunan liste yazma**; K1/K4/K5 |
| 40 | `madsc-ibo-second-voice.yml` | `apply_ibo_second_voice.py`; yabancı kanalları arşivler, CALISANLAR commit/push | 15 dk | **Korunan liste yazma**; K1/K4/K5 |

## Önemli kontrol noktaları

- #31 ve #33–40 gerçek GitHub yazma yollarına sahiptir. Canlı workflow dispatch, ana dal push, cihaz erişimi veya üretim listesi üzerinde test **yapılmamalıdır**.
- #32 yalnızca dry-run uyarısı verdiği için gerçek kanal ayırma işlevi varmış gibi eşleştirilmemelidir.
- Eski kaynakta `protected_write_gate.py` çağrılması, yeni sistemin fail-closed kabulünü tek başına kanıtlamaz.
- Güvenli davranış karşılaştırması için ayrı fixture kökleri, dış ağ/kimlik bilgisi olmaması, yan etki manifestleri, çıkış kodu ve artifact SHA256 karşılaştırması gerekir.
- Bu 10 YAML'ın kaynak düzeyi ilk incelemesi tamamlandı. Çağrılan script'lerin tamamı ve yeni sistem karşılıkları henüz bağımsız doğrulanmadı. İlk 40 YAML bu doğrudan inceleme serisinde ele alındı; önceki 45/92 raporuyla mükerrerlik denetlenmeden birleştirilmemeli. Davranışsal kabul **0/92**.
