# Eski workflow davranış komutları — ilk 23 kaynak

Kaynak: `Madsc55/madsc-tv`, `madsc/bes-sistem-toplu-birlestirme`. Her satır eski YAML içinden okunan komutların özetidir; alt Python betiklerinin tam davranış çözümlemesi veya yeni sistem eşdeğerliği **değildir**.

| Workflow | Kaynaktan görülen iş akışı | Entegrasyon durumu |
|---|---|---|
| `390-aday-tekrar-test.yml` | 390 aday için paralel ffmpeg ses/görüntü tekrar testi; CSV ve M3U raporu | Kanıt bekliyor |
| `aday-bekletme.yml` | Aday tarama → tekrarlar → medya testi → bekletme → takvim → yeniden test → kaynak puanı → öncelik raporu | Kanıt bekliyor |
| `aday-logo-epg-test.yml` | Aday EPG/logo kanıtlarını birleştirir; ana liste SHA değişmemeli | Kanıt bekliyor |
| `aday-oncelik-kontrol.yml` | Örnek adaylar üzerinde öncelik sıralamasını doğrular | Kanıt bekliyor |
| `aday-yedekleme.yml` | Teknik adayları yedek taslağına aktarır; yedek verisi korumalı | Kanıt bekliyor |
| `akilli-aday-puanlama.yml` | Tarama, ffprobe, teknik puanlama ve ayrı aday raporları | Kanıt bekliyor |
| `altinci-aday-tekrar-test.yml` | Altıncı tekrar testi ve ffmpeg tabanlı medya kanıtı | Kanıt bekliyor |
| `automatic-png-logos.yml` | PNG logo üretimi ve görsel kanıt raporu | Kanıt bekliyor |
| `besinci-zaman-asimi-test.yml` | ffmpeg zaman aşımı davranışı için izole test | Kanıt bekliyor |
| `birlesik-aday-raporu.yml` | Tarama → teknik doğrulama → genel medya → puanlama → kararlılık → birleşik rapor | Kanıt bekliyor |
| `birlesik-durum-raporu.yml` | Test özeti, eksik Türk kanalları, kaynak kapsamı, genel bakım raporları | Kanıt bekliyor |
| `dokuzuncu-akilli-tekrar-test.yml` | Akıllı tekrar takvimi birim testi | Kanıt bekliyor |
| `epg-gunluk.yml` | EPG üretimi, IBO EPG ve hazır olma kontrolü; GIT COMMIT/PUSH içerir, otomatik taşıma YASAK | Kanıt bekliyor |
| `epg-pages.yml` | EPG Pages yayın hazırlığı; kaynak adımları daha ayrıntılı incelenmeli | Kanıt bekliyor |
| `felaket-kurtarma-tatbikati.yml` | Felaket kurtarma dry-run raporu | Kanıt bekliyor |
| `genel-aday-medya-test.yml` | Aday tarama ve ffprobe medya testi | Kanıt bekliyor |
| `genis-kanal-tarama.yml` | Geniş kanal taraması ve kanıt raporu | Kanıt bekliyor |
| `ibo-bagimsiz-test-listesi.yml` | Aday tarama → medya testi → bağımsız IBO listesi | Kanıt bekliyor |
| `ibo-epg-kimlik-denetimi.yml` | Korunan CALISANLAR.m3u ile XMLTV kanal kimliği karşılaştırması, rapor | Kanıt bekliyor |
| `ibo-yedek-kalite.yml` | Yedek aday kalite ölçümü, ffprobe | Kanıt bekliyor |
| `iptv-test.yml` | Aday M3U için ffmpeg/iptv_test.py | Kanıt bekliyor |
| `kanal-kararlilik.yml` | Teknik doğrulama ve kararlılık takibi | Kanıt bekliyor |
| `kaynak-puanlama-kontrol.yml` | Kaynak güven puanı sözdizimi ve birim testi | Kanıt bekliyor |

**Kritik koruma:** `epg-gunluk.yml` otomatik `git commit`/`git push` yapıyor; bu yan etki yeni sisteme izinsiz taşınmayacak. `aday-yedekleme.yml` korunan yedek alanına ilişkin, yazma izni verilmeden yürütülmeyecek. IBO cihaz testi kullanıcıda kalır.

99 kaynak YAML listesi ve Git blob kimlikleri için `docs/LEGACY_99_PINNED_WORKFLOW_SCOPE_2026-10-22.md` esas alınır. Davranışsal kabul: 0/92.
