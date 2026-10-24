# K5 — Eski workflow 78–92 doğrudan YAML incelemesi

Kaynak: `Madsc55/madsc-tv` sabit commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. Son 15 YAML doğrudan okundu; hiçbir workflow çalıştırılmadı. Bu yalnızca statik kaynak sözleşmesidir, **davranışsal kabul değildir**.

| # | Workflow | Kaynaktan doğrulanan davranış | Süre | Risk / aday |
|---:|---|---|---|---|
| 78 | `test-33-all-write-paths.yml` | Yazma yetkili workflow'ları tarar, statik rapor | 10 dk | Dolaylı script yazmaları ayrıca incelenmeli; K1/K5 |
| 79 | `test-34-protected-write-regression.yml` | Beş workflow'da yazma yetkisi/commit/push yokluğunu regex ile doğrular | 5 dk | Sadece belirtilen beş yol; K1/K5 |
| 80 | `test-35-remaining-write-gate.yml` | Aday bekletme workflow'unun salt-okunur ve artifact-only olduğunu denetler | 5 dk | Tek workflow; K1/K5 |
| 81 | `test-36-system-integration-audit.yml` | YAML ve korunan yazma maruziyeti taraması | 8 dk | Statik; EPG/VOD ayrı yazma sınıfı; K1/K5 |
| 82 | `test-37-indirect-write-audit.yml` | Workflow'ların çağırdığı Python script'lerde olası dolaylı yazma taraması | 8 dk | Regex ve manuel doğrulama gerekir; K1/K5 |
| 83 | `test-38-audit-selftest.yml` | Denetim 32–37 varlık/izin/checkout koşulları ve sentetik kötü örnek | 6 dk | Denetleyici selftest; K1/K5 |
| 84 | `test-39-protected-playlist.yml` | Korunan playlist bütünlüğü script'ini salt-okunur çalıştırır | 5 dk | K1/K5 |
| 85 | `test-kanal-adaylari.yml` | Aday yayınları test eder, yedek aday M3U ve JSON'u artifact olarak yükler | 15 dk | Canlı yayın testi; onay bekler; K2/K4/K5 |
| 86 | `toplu-sistem-kontrol.yml` | Python/YAML/liste denetimi ve örnek HTTP yayın erişimi | 35 dk | HTTP erişimi oynatma kanıtı değildir; K1/K3/K5 |
| 87 | `vod-guncelle.yml` | Günlük 07:17 UTC VOD metadata günceller ve git commit/push | Tanımlı değil | `contents:write`, üretim VOD yazması; K1/K3/K5 |
| 88 | `yedek-geri-yukleme-tatbikat.yml` | Yedekleri geçici dizine restore dry-run, JSON artifact | 8 dk | İzole geri yükleme; K4/K5 |
| 89 | `yedekler-yeniler-medya-kontrol.yml` | İki kategori ffprobe testi ve CSV/JSON artifact | 70 dk | Canlı yayın testi; K3/K5 |
| 90 | `yeni-aday-on-test.yml` | ffprobe ile aday ve logo ön testi, CSV artifact | 30 dk | Canlı medya testi; K2/K3/K5 |
| 91 | `yeni-kanal-arama-2026.yml` | SCAN_BATCH=1 keşif/ffprobe, rapor artifact; read-only token | 65 dk | Ağlı tarama; K2/K5 |
| 92 | `yeniler-guvenli-arama.yml` | Kaynak keşfi, artifact indirme, 34–99 batch matrisi ve ffprobe | İlk iş 20 dk, batch işi 35 dk | Çoklu canlı ağ testi; K2/K5 |

## Sonuç ve eksikler

- **92/92 eski workflow YAML dosyası doğrudan kaynak üzerinden ilk kez gözden geçirildi** (1–20, 21–30, 31–40, 41–47, 48–57, 58–67, 68–77, 78–92 inceleme belgeleri).
- Bu sonuç, her workflow'un tüm script bağımlılıklarının veya tam YAML gövdesinin ayrıntılı analiz edildiği anlamına gelmez. Özellikle uzun YAML'ların ilk kısımları okunmuş, tam adım sözleşmesi eksik kalabilir.
- Önceden raporlanan 45/92 statik ayrıntılı incelemeyle mükerrerlik denetimi yapılmadı. Bu sayı **92/92 davranışsal entegrasyon** olarak sunulamaz.
- **Bağımsız eski/yeni fixture yürütmesi ve kabul: 0/92.** CI yeşil olsa bile kabul otomatik açılmamalı.
- Sonraki adım: risk temelli ayrıntılı script/yürütme eşlemesi, özellikle #49/#92 uzun workflow tam gövdesi, bağımsız fixture SHA256, iki ayrı run ID, stdout/stderr/artifact/yan etki manifesti, korunan dosya hash değişmezliği ve negatif testler.
- Üretim listeleri, EPG, logo, VOD, yedekler ve cihaz verileri değiştirilmedi.
