# Sekizinci kaynak çözümlemesi: sekiz eski workflow (72/99)

Sabit kaynak: `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`. Sekiz YAML'ın tam kaynakları incelendi. Bunlar statik YAML bulgularıdır; çağrılan kodların ve canlı ortamın davranışsal kabulü değildir.

| Workflow | K adayı | Tetikleme | Zincir ve kabul için kritik semantik |
|---|---|---|---|
| `test-21-functional-e2e.yml` | K1/K2/K3/K5 | Manuel + YAML push | Python 3.11; üç sentetik aday; duplicate, HTTP 403 sınıfı, aday özeti, URL token maskeleme, geçici M3U değişiklik/dry-run, iki korunan listenin SHA256 eşitliği; 8 dk. Gerçek yayın testi değil. |
| `test-22-real-playlist.yml` | K1/K3 | Manuel + YAML push | İki gerçek korunan M3U'yu salt okunur parse, logo/EPG audit, özdeş içerik dry-run, önce/sonra SHA256; 8 dk. Ağ, oynatıcı veya XMLTV indirme testi değil. |
| `test-23-live-stream.yml` | K1/K3 | Manuel + YAML push | Her korunan listeden en çok 15 HTTP(S) kanalına Range 0–2047, 7 sn timeout, en çok 2048 bayt GET; erişim durumlarını sayar; SHA256 eşitliği; 12 dk. Erişilebilirlik çözülebilir ses/video kanıtı değildir. |
| `test-24-system-audit.yml` | K1/K5 | Manuel + YAML push | PyYAML kur; tüm Python AST, YAML/jobs/contents:write uyarıları, M3U URL bütünlüğü, yedek envanteri, korunan hash, iki unittest discover; JSON artifact always; 15 dk. |
| `test-25-full-project-readonly.yml` | K1/K4/K5 | Manuel + YAML push | Tüm Python/YAML/M3U, yazma riski ve backup envanteri; korunan SHA256; iki unittest discover; JSON artifact always; 20 dk. Gerçek playback ve uçtan uca otomasyon açıkça NOT PROVEN. |
| `test-26-automation-safety.yml` | K1/K5 | Manuel + YAML push | PyYAML; tüm YAML'larda write-all, write permission, git push/commit, gh api/release, create-pull-request için sezgisel risk taraması; JSON artifact always; 10 dk. Heuristik tarama gerçek güvenlik uygulama kanıtı değildir. |
| `test-27-pipeline-contract.yml` | K1/K2/K3/K4/K5 | Manuel + YAML push | Keşif, aday test, tekrar, yedek ve entegrasyon workflow dosyalarının varlığı; iki M3U SHA256/boyut; tüm Python AST; JSON artifact always; 10 dk. Varlık gerçek workflow bağlantısı değildir. |
| `test-28-approval-gate.yml` | K1/K2 | Manuel + YAML push | Aday durum özet fonksiyonunu yükleyip 6 statünün sınıflandırmasını doğrular; iki M3U SHA256; JSON artifact always; 10 dk. Tüm üretim yazma yollarında onay kapısı uygulanmasını doğrulamaz. |

## Önemli ayrımlar

- `test-23-live-stream` gerçek dış ağa GET yapar. Diğer yedi workflow ağırlıkla salt okunur denetim/fixture testidir; ağ denemesi açık izin olmadan taşınmamalıdır.
- `test-27-pipeline-contract` bazı dosyaların varlığını arar; 92 davranışsal eşdeğerlik için kanıt sayılmaz.
- `test-28-approval-gate` **yetkilendirme uygulamasını değil** aday durum sınıflandırmasını test eder; K1 26 kural kabulüne yazılamaz.
- `test-24` ve `test-25` iki farklı kapsamda envanter taraması yapar; iki kez aynı işin yürütülmesi gerekip gerekmediği performans açısından ayrıca değerlendirilmelidir.

**Ayrıntılı statik kaynak çözümlemesi: 72/99 (%72,7), kalan 27.** Davranışsal kabul **0/92**, güvenlik üretim kabulü **0/26**. Actions çalıştırılmadı, korunan dosyalar değiştirilmedi.
