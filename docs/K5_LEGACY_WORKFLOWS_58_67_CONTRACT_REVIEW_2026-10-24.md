# K5 — Eski workflow 58–67 doğrudan kaynak incelemesi

Kaynak: `Madsc55/madsc-tv` sabit commit `ca374df3b9585c0d76a078db9536150ebbc260f7`. On YAML doğrudan okundu; hiçbir workflow çalıştırılmadı. Bu statik inceleme **davranışsal eşdeğerlik kabulü değildir**.

| # | Workflow | Kaynaktan gözlenen sözleşme | Timeout | K adayı |
|---:|---|---|---|---|
| 58 | `test-13-kaynak-degisiklik.yml` | Geçici M3U'larda added/changed/removed ve otomatik rollback yapmama testi | Tanımlı değil | K2/K5 |
| 59 | `test-14-istikrar.yml` | Sabit UTC zamanda 7/30 günlük başarı oranı ve son başarı tarihi testi | Tanımlı değil | K3/K5 |
| 60 | `test-15-logo-epg.yml` | Tekrarlanan tvg-id, eksik logo/id ve şüpheli URL uyarıları; mevcut listeyi salt-okunur inceler | Tanımlı değil | K3/K5 |
| 61 | `test-16-workflow-safety.yml` | URL/token gizleme ve sınırlı retry/timeout testi | 5 dk (adım 2 dk) | K1/K5 |
| 62 | `test-17-candidate-summary.yml` | Beş aday durum grubu, bilinmeyen durum ve JSON/CSV okuma testi | 5 dk | K2/K5 |
| 63 | `test-18-change-simulation.yml` | Dry-run, değişiklik sayısı ve rollback SHA; korunan listelerde git diff | 5 dk | K1/K5 |
| 64 | `test-19-integration.yml` | Logo, aday, güvenlik, kararlılık, dry-run ve korunan liste SHA bütünlüğü | 5 dk | K1/K2/K3/K5 |
| 65 | `test-20-full-integration.yml` | Python AST parse, unittest, workflow varlık envanteri; kendi notu gerçek 1–18 E2E kanıtı olmadığını söyler | 10 dk | K1–K5 |
| 66 | `test-21-functional-e2e.yml` | Fixture ile tekrar, hata, özet, redaksiyon, değişiklik ve logo akışı; korunan liste SHA kontrolü | 8 dk | K1/K2/K3/K5 |
| 67 | `test-22-real-playlist.yml` | Gerçek CALISANLAR/YENILER dosyalarını salt-okunur parse/denetle; kendi notu stream erişimi/oynatma kanıtı olmadığını söyler | 8 dk | K1/K3/K5 |

## Kabul sınırları

- #58–66 güvenli, kontrollü fixture regresyonuna uygun başlangıç noktalarıdır; ancak yeni sistem karşılıkları ile bağımsız yürütme kanıtı oluşturulmadı.
- #67 gerçek dosya okur ama yayın erişilebilirliğini, EPG indirmeyi veya oynatıcıda görüntü/ses doğrulamayı **kanıtlamaz**.
- #65 workflow dosyası varlık kontrolü davranışsal entegrasyon değildir.
- Kaynak YAML'ların ilk 67'si doğrudan incelendi; 25 kaldı. Script ve tam çıktı sözleşmeleri ayrıca doğrulanmalıdır. **Davranışsal kabul 0/92**.
