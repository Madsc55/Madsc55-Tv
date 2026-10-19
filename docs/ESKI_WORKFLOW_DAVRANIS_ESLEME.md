# İlk davranışsal eşleme — 8 kaynak workflow (19 Ekim 2026)

Kaynak salt-okunur dal: `Madsc55/madsc-tv@madsc/bes-sistem-toplu-birlestirme`. Bu dosya **kanıt haritası**, tamamlandı/taşındı onayı değildir. Tetik, izin, script ve veri aktarımı gerçek eski YAML içeriklerinden kontrol edildi.

| Eski workflow | Tetik | İzin | Önemli gerçek işler / bağımlılık | K1–K5 hedefi | Durum |
|---|---|---|---|---|---|
| `madsc-01-guvenlik.yml` | dispatch, workflow_call | contents:read, actions:read | 26 kural runtime kanıt kapısı; protected snapshot/check; 92 eşdeğerlik audit; çoklu regresyon ve toplu hata kapısı | K1 + K5 | Eksik: 26/26 gerçek enforcement |
| `madsc-02-kesif.yml` | cron 05:17/17:17 ve 06:00/18:00 UTC, dispatch, call | contents:read, actions:read | geçmiş restore → discovery archive before/after → gerçek keşif → logo/EPG join → dört aşama; geniş tarama; toplu test | K2 → K3/K5 | Eksik: canlı keşif ve geçmiş aktarımı |
| `madsc-03-kanal-test.yml` | cron 06:40 UTC, sınırlı push, dispatch, call | contents:read, actions:read | ffmpeg; gerçek aday medya ölçümü → scoring; ana liste 100'lü salt-okunur health; logo/EPG, IBO artefakt; 10 adımlı sonuç kapısı | K3 → K5, K1 | Eksik: gerçek ffprobe ve zamanlı kanıt |
| `madsc-04-arsiv-yedek.yml` | kaynak YAML okundu | ayrıntı ayrıca sınıflandırılacak | yedek/restore, bağımsız arşiv kabulü için dosya içi script ve çıktı satırları ayrı doğrulanacak | K4 → K5 | Eksik: ayrıntılı görev incelemesi |
| `madsc-05-genel-bakim.yml` | workflow_call / dispatch, diğer kategorilere needs | contents:read, actions:read (çağrılan işler) | K1→K2→K3→K4 needs; önceki kategori artefaktları; 92 satırlık karar matrisi (tamamı BLOCKED); toplu sonuç ve hata listesi | K5 (K1–K4 bağımlı) | Eksik: gerçek koşu bazlı kabul |
| `aday-bekletme.yml` | dispatch, paths push | contents:read | yeni_kanal_tara → tekrar raporu → gelişmiş medya testi → aday bekletme → akıllı takvim → RETEST_LIMIT=5 yeniden test → kaynak güven puanı → aday öncelik; 10 artefakt | K2 → K3 → K5 | Eksik: tüm yeniden test ve güven puanı davranışı |
| `akilli-aday-puanlama.yml` | dispatch, paths push | contents:read | SCAN_BATCH=-1 discovery → gerçek ffprobe öncelik testi → teknik score → 4 artefakt | K2 → K3 → K5 | Skor/CSV uyumluluğu fixture; canlı kanıt yok |
| `birlesik-aday-raporu.yml` | dispatch, paths push | contents:read | cache/restore geçmiş → discovery → priority/general ffprobe → scoring → stability → birleşik onay raporu; 4 artefakt | K2 → K3 → K5 | CSV/JSON uyumluluğu fixture; gerçek geçmiş toplama yok |

**Dikkat:** K5 eski workflow'u 92 satırın tamamının `BLOCKED_NEEDS_BEHAVIOR_EVIDENCE` olmasını şart koşuyor. Dolayısıyla 92 satırın varlığı **92 davranışın kabul edildiği** anlamına gelmiyor. Bu sekiz kaynak arasında gerçek çapraz bağımlılıklar var; tek tek fixture geçmesi yeterli değil.

**Sıradaki:** K4 YAML'ın script/artefakt ayrıntılarını doğrula; sonra 99 dosyanın kalan 91'i için tetik/izin/çalışan script/çıktı sınıflandırmasını tamamla, 92 kapsam farkını kanıtla. Korunan listelere dokunma, üretim cron/yazma açma.
