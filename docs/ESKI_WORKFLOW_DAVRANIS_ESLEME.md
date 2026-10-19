# İlk davranışsal eşleme — 8 kaynak workflow (19 Ekim 2026)

Kaynak salt-okunur dal: `Madsc55/madsc-tv@madsc/bes-sistem-toplu-birlestirme`. Bu dosya **kanıt haritası**, tamamlandı/taşındı onayı değildir. Tetik, izin, script ve veri aktarımı gerçek eski YAML içeriklerinden kontrol edildi.

| Eski workflow | Tetik | İzin | Önemli gerçek işler / bağımlılık | K1–K5 hedefi | Durum |
|---|---|---|---|---|---|
| `madsc-01-guvenlik.yml` | dispatch, workflow_call | contents:read, actions:read | 26 kural runtime kanıt kapısı; protected snapshot/check; 92 eşdeğerlik audit; çoklu regresyon ve toplu hata kapısı | K1 + K5 | Eksik: 26/26 gerçek enforcement |
| `madsc-02-kesif.yml` | cron 05:17/17:17 ve 06:00/18:00 UTC, dispatch, call | contents:read, actions:read | geçmiş restore → discovery archive before/after → gerçek keşif → logo/EPG join → dört aşama; geniş tarama; toplu test | K2 → K3/K5 | Eksik: canlı keşif ve geçmiş aktarımı |
| `madsc-03-kanal-test.yml` | cron 06:40 UTC, sınırlı push, dispatch, call | contents:read, actions:read | ffmpeg; gerçek aday medya ölçümü → scoring; ana liste 100'lü salt-okunur health; logo/EPG, IBO artefakt; 10 adımlı sonuç kapısı | K3 → K5, K1 | Eksik: gerçek ffprobe ve zamanlı kanıt |
| `madsc-04-arsiv-yedek.yml` | dispatch, workflow_call | contents:read, actions:read | isolated git restore → backup evidence → archive consistency → disaster recovery dry run; `CALISANLAR.m3u`/`YENILER.m3u` kopyada restore; offsite `DOGRULANMADI`, historical restore false; 4 regresyon, toplu hata kapısı | K4 → K5, K1 | Eksik: gerçek offsite ve tarihsel restore |
| `madsc-05-genel-bakim.yml` | workflow_call / dispatch, diğer kategorilere needs | contents:read, actions:read (çağrılan işler) | K1→K2→K3→K4 needs; önceki kategori artefaktları; 92 satırlık karar matrisi (tamamı BLOCKED); toplu sonuç ve hata listesi | K5 (K1–K4 bağımlı) | Eksik: gerçek koşu bazlı kabul |
| `aday-bekletme.yml` | dispatch, paths push | contents:read | yeni_kanal_tara → tekrar raporu → gelişmiş medya testi → aday bekletme → akıllı takvim → RETEST_LIMIT=5 yeniden test → kaynak güven puanı → aday öncelik; 10 artefakt | K2 → K3 → K5 | Eksik: tüm yeniden test ve güven puanı davranışı |
| `akilli-aday-puanlama.yml` | dispatch, paths push | contents:read | SCAN_BATCH=-1 discovery → gerçek ffprobe öncelik testi → teknik score → 4 artefakt | K2 → K3 → K5 | Skor/CSV uyumluluğu fixture; canlı kanıt yok |
| `birlesik-aday-raporu.yml` | dispatch, paths push | contents:read | cache/restore geçmiş → discovery → priority/general ffprobe → scoring → stability → birleşik onay raporu; 4 artefakt | K2 → K3 → K5 | CSV/JSON uyumluluğu fixture; gerçek geçmiş toplama yok |

**Dikkat:** K5 eski workflow'u 92 satırın tamamının `BLOCKED_NEEDS_BEHAVIOR_EVIDENCE` olmasını şart koşuyor. Dolayısıyla 92 satırın varlığı **92 davranışın kabul edildiği** anlamına gelmiyor. Bu sekiz kaynak arasında gerçek çapraz bağımlılıklar var; tek tek fixture geçmesi yeterli değil.

**Sıradaki:** 99 dosyanın kalan 91'i için tetik/izin/çalışan script/çıktı sınıflandırmasını tamamla, 92 kapsam farkını kanıtla. Korunan listelere dokunma, üretim cron/yazma açma.


## İkinci grup — 8 eski YAML (salt-okunur gerçek kaynak incelemesi)

| Workflow | Tetik ve izin | Script / davranış | Hedef ve açık kanıt |
|---|---|---|---|
| `kanal-kararlilik.yml` | dispatch + paths push; contents:read | cache/restore `KARARLILIK_GECMISI.json` → ffprobe `oncelikli_kanal_dogrula.py` → `kanal_kararlilik_takip.py` → cache/save ve artifact | K3→K5; gerçek zamanlı kalıcı geçmiş zinciri eksik |
| `genel-aday-medya-test.yml` | dispatch + paths push; contents:read | `SCAN_BATCH=-1` aday keşfi, ffprobe, `ADAY_TEST_GRUBU=0` gerçek video/ses testi, CSV+JSON artifact | K2→K3; canlı ffprobe kanıtı eksik |
| `aday-logo-epg-test.yml` | dispatch + paths push; contents:read | `candidate_epg_logo_join.py`, `CALISANLAR.m3u` SHA256 önce/sonra; 5 pilot EPG, playlist onaysız; artifact | K2→K3/K5, K1; kimlik/EPG canlı uyum kabulü eksik |
| `aday-yedekleme.yml` | dispatch + main push (command file); contents:read | `yedekler/teknik_adaylari_aktar.py` teknik aday yedek **taslak** M3U artifact, listeye push yok | K4 + K2; YEDEKLER'e yazma yetkisi çıkarılamaz |
| `felaket-kurtarma-tatbikati.yml` | dispatch + paths push; contents:read | `scripts/disaster_recovery_dry_run.py`, geçici restore raporu artifact | K4; offsite/tarihsel bağımsız geri yükleme kanıtı değil |
| `madsc-birlesik-kesif.yml` | dispatch + 06/18 UTC cron; **contents:write, actions:write**; main koşulu | failure gate → discovery archive before/after → `madsc_akilli_kesif.py` → logo/EPG join → dört aşama → `protected_write_gate.py` → `git push origin HEAD:main` | K1+K2+K5 **yüksek yazma riski**; eski izinleri yeniye taşımak yasak, gerçek yazma yolları denetlenecek |
| `epg-gunluk.yml` | dispatch + 03:25 UTC cron; **contents:write**; main koşulu | `build_epg.py`, `build_ibo_epg_test.py`, `epg_tv_readiness.py`; belirli EPG çıktıları `git add`, protected write gate ve `git push` | K1+K3+K5; korunan EPG değişikliği yasak, üretim yayını yeni sisteme otomatik aktarılmaz |
| `epg-pages.yml` | dispatch + başarılı `EPG Günlük Güncelleme` workflow_run(main); contents:read, **pages:write, id-token:write** | EPG XML doğrula, `_site` hazırla, Pages dağıtımı; başarılı eski workflow sonucuna bağlı | K3+K5; yeni Pages dağıtımı yetkilendirilmedi, IBO EPG cihaz uyumu kanıtlanmadı |

**İkinci grup sonucu:** 16/99 eski YAML dosyasının kaynak içeriği ayrıntılı incelendi; **83 dosya** ayrıntılı inceleme bekliyor. Bu bir davranış eşdeğerliği onayı değil. İzinli eski cron, push ve Pages işlemleri **yeni depoda açılmadı**. Eski workflow'lar kapatılmadı.
