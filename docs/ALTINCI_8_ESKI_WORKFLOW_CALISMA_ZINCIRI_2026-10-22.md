# Altıncı kaynak çözümlemesi: sekiz eski workflow (56/99)

Sabit kaynak: `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`. Aşağıdaki sekiz YAML'ın tam metni okundu. Bu statik YAML çözümlemesidir; çağrılan betiklerin yan etkileri ve çalışma zamanı eşdeğerliği ayrıca kanıtlanmalıdır.

| Workflow | K adayı | Tetikleme | Gerçek YAML yürütme zinciri | Kabulde korunacak davranış ve risk |
|---|---|---|---|---|
| `epg-gunluk.yml` | K1/K3 | Manuel + her gün 03:25 UTC cron | main branch koşulu; `build_epg.py` → `build_ibo_epg_test.py` → `epg_tv_readiness.py` → dört EPG dosyasını stage → protected gate → commit → pull --rebase → tekrar gate → push | **contents:write** ve üretim EPG yazımı; cron eşdeğerliği otomatik taşınamaz; güvenlik izni gerekli |
| `epg-pages.yml` | K3/K5 | Manuel + başarılı `EPG Günlük Güncelleme` workflow_run | XMLTV channel/programme doğrula; beş kanallı IBO pilotu doğrula; Pages artifact/deploy; yayımlanan XML SHA256 eşleşmesini en çok 20 kez denetle | **pages:write/id-token:write**; gerçek dış yayın yan etkisi; deploy ancak açık onayla; Pages SHA eşdeğerliği |
| `felaket-kurtarma-tatbikati.yml` | K1/K4 | Manuel + YAML/restore script push | `disaster_recovery_dry_run.py` geçici ortamda; `MADSC-FELAKET-KURTARMA-DOGRULAMA` JSON artifact; 8 dk | İzole tatbikat gerçek harici yedekten restore kanıtı değildir |
| `genel-aday-medya-test.yml` | K2/K3 | Manuel + betik/YAML push | ffmpeg; `SCAN_BATCH=-1` tarama; `ADAY_TEST_GRUBU=0` gerçek video/ses probe; iki rapor artifact; 40 dk | Sınırsız ağ taraması ve ffprobe, açık izin; gerçek ses/video raporları |
| `genis-kanal-tarama.yml` | K2/K3 | Manuel + genel-guncelleme komut dosyası main push | ffmpeg; `genis_kanal_tara.py`; always `GENIS-KANAL-TARAMA-RAPORU` CSV artifact; 55 dk | Çok kaynaklı canlı tarama; başarısızlıkta artifact korunumu |
| `ibo-bagimsiz-test-listesi.yml` | K2/K3 | Manuel + betik/YAML push | ffmpeg; `SCAN_BATCH=-1`; `ADAY_TEST_GRUBU=0`; `ibo_bagimsiz_test_listesi.py`; üç dosyalı bağımsız IBO M3U/CSV/JSON artifact; 40 dk | Ana listeye dokunmadan izole IBO listesi; gerçek yayın ölçümü ve kimlik eşlemesi |
| `ibo-epg-kimlik-denetimi.yml` | K1/K3 | Manuel + betik/YAML push | py_compile; `CALISANLAR.m3u` ile 5 kanallı XMLTV pilotunun `RUNNER_TEMP` altında karşılaştırılması; dört pozitif sayaç; 14 günlük artifact; 10 dk | `tvg-id`/XMLTV program eşleşmesi ve üretim listesinin salt okunurluğu |
| `ibo-yedek-kalite.yml` | K3/K4 | Manuel + betik/YAML push | ffmpeg; `ibo_yedek_kalite_tespit.py`; always tarihli CSV artifact; 25 dk | Gerçek yedek yayın kalitesi; hata durumunda rapor; harici backup/restore değildir |

## Zincir bağımlılıkları ve korunacak sınırlar

- `epg-gunluk` başarılı bitince `epg-pages` otomatik tetiklenebilir; bu **üretim yayını** zinciridir, salt okunur K1–K5 testine gizlice taşınmamalıdır.
- `epg-gunluk` yazma izni ile `epg-pages` dağıtım izni birbirinden farklıdır; beşli sistemin varsayılan `contents:read` koşulu bunları işlevsel olarak çalıştırmaz.
- `ibo-epg-kimlik-denetimi` dört sayacın pozitifliğini sınar; bütün kanalların doğru eşleştiğini garanti etmez.
- `genel-aday-medya-test`, `ibo-bagimsiz-test-listesi`, `genis-kanal-tarama` gerçek ağ testi gerektirir; mock/fixture CI başarısı davranışsal kabul değildir.

**Ayrıntılı statik YAML çözümlemesi: 56/99 (%56,6), kalan 43.** Davranışsal kabul **0/92**, güvenlik üretim kabulü **0/26**. GitHub Actions çalıştırılmadı, canlı yayın taranmadı, korunan dosyalar değiştirilmedi.
