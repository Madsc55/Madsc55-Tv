# K1-K5: Sekiz eski workflow incelemesi (88/99)

Kaynak: `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`. Sekiz YAML tam metin incelendi. Statik kaynak incelemesidir, davranışsal kabul değildir.

| Workflow | Tetikleme ve kanıtlanan YAML zinciri |
|---|---|
| `madsc-documentation-check.yml` | Sadece manuel; AGENTS, özellik, devir notu varlığı, Kural 25, build_epg kaydı ve M3U başlığı; içerik eşdeğerliği yok. |
| `madsc-genis-kaynak-kontrol.yml` | Sadece manuel; contents/actions write; weekly ve monthly 155 kaynak taraması; artifact; beş denemeli main rapor push; başarıda `madsc-uc-asama.yml` için API dispatch. **Başka workflow tetikler.** |
| `madsc-hizli-on-kontrol.yml` | Manuel veya eski birleşim dalında seçili push; geçiş hazırlığı, K1-K5 ortak kurallar, 92 workflow envanteri ve preflight; artifact. Kabul değil ön kontrol. |
| `madsc-ibo-3-5281.yml` | Manuel veya eski birleşim dalında YAML push; sadece güvenli dry-run echo. **Kanal ayırma yapılmaz.** |
| `madsc-ibo-354-classify.yml` | YAML push; main'de contents write; `archive_backups_354_classified.py`; `CALISANLAR.m3u` ve iki arşiv/rapor stage; protected gate, commit, push. **Üretim ana listesine yazabilir.** |
| `madsc-ibo-364-355-364.yml` | YAML push; main'de contents write; `archive_backups_355_364.py`; yabancı liste diff kontrolü, `CALISANLAR.m3u` ve arşiv raporu commit/push. |
| `madsc-ibo-398-16-49.yml` | YAML push; main'de contents write; `archive_backups_16_49.py`; yabancı liste diff kontrolü, `CALISANLAR.m3u` ve arşiv raporu commit/push. |
| `madsc-ibo-530-archive.yml` | YAML push; main'de contents write; `archive_backups_399_onward.py`; yabancı liste diff kontrolü, `CALISANLAR.m3u` ve arşiv raporu commit/push. |

## Güvenlik ve entegrasyon kararı

Dört IBO arşivleme workflow'u `CALISANLAR.m3u` üzerinde üretim yazma yetkisine sahiptir. İlgili Python betikleri, korunan yazma kapısının gerçek uygulaması ve kullanıcı onayı olmadan beşli sisteme otomatik taşınamaz. `madsc-genis-kaynak-kontrol` yalnızca rapor yazmaz, başarılıysa başka bir workflow dispatch eder. `madsc-ibo-3-5281` yalnızca echo'dur; kanal ayırma kabulü değildir.

Statik YAML incelemesi **88/99**, kalan **11**. Davranışsal kabul **0/92**. Bu inceleme Actions başlatmadı veya üretim listelerini değiştirmedi.
