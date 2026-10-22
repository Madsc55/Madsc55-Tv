# İkinci 12 eski workflow: tam YAML çalışma zinciri

Sabit kaynak `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`. Aşağıdaki **12 YAML dosyasının tüm metni** GitHub'dan salt okunur alındı; tetikleyiciler, step sırası, izinler, artifact ve koşullar incelendi. Çağrılan Python dosyalarının tam dolaylı çağrı grafiği bu belgenin kapsamı dışındadır.

| Workflow | Aday K | Tetikleyici | YAML'daki komut/step sırası | Çıktı ve izinler | Eksik davranışsal kanıt |
|---|---|---|---|---|---|
| epg-gunluk | K1/K3 | schedule 03:25 UTC + dispatch; main koşulu | build_epg → build_ibo_epg_test → epg_tv_readiness → git add → protected_write_gate → commit/pull/rebase/gate/push | EPG XML, IBO 5 XML, iki JSON; contents write | Gerçek EPG yazma/push, kapalı kalmalı |
| epg-pages | K3/K5 | workflow_run(success main) veya dispatch | XMLTV doğrula → _site üret → upload-pages-artifact → deploy-pages → HTTP SHA256 20 deneme | GitHub Pages canlı dağıtım; pages/id-token write | EPG yayını ve HTTP canlı doğrulama, onaysız çalıştırılmaz |
| felaket-kurtarma-tatbikati | K4/K1 | push/dispatch | disaster_recovery_dry_run.py | DISASTER-RECOVERY-REPORT.json; always/error | Geçici ortam tatbikatı, gerçek restore değil |
| genel-aday-medya-test | K2/K3 | push/dispatch | yeni_kanal_tara SCAN_BATCH=-1 → genel_aday_medya_test ADAY_TEST_GRUBU=0 | iki CSV/JSON artifact required | Gerçek ffprobe, izin yok |
| genis-kanal-tarama | K2/K3 | push/dispatch | genis_kanal_tara.py | GENIS_KANAL_TARAMA_RAPORU.csv always | Çok kaynak ve yayın testi |
| ibo-bagimsiz-test-listesi | K2/K3 | push/dispatch | yeni_kanal_tara → genel_aday_medya_test → ibo_bagimsiz_test_listesi | IBO_BAGIMSIZ_TEST_ADAYLARI.m3u, CSV, JSON | İzole IBO test listesi; ana listeye otomatik onay yok |
| ibo-epg-kimlik-denetimi | K3/K5 | push/dispatch | ibo_epg_kimlik_denetimi --playlist CALISANLAR --xmltv epg/ibo-test-epg.xml --output RUNNER_TEMP; dört pozitif sayaç assert | ibo_epg_identity_audit.json; 14 gün | XMLTV ID teknik eşleşmesi, cihaz testi değil |
| ibo-yedek-kalite | K3/K4 | push/dispatch | ibo_yedek_kalite_tespit.py | yedekler/IBO_YEDEK_KALITE_RAPORU_2026-10-09.csv always | Gerçek yedek yayın probe |
| iptv-test | K3/K1 | schedule Çarşamba 06:30 UTC + push/dispatch | iptv_test.py MADSC_TV_47_LISTE_ADAY.m3u | CALISANLAR.m3u, CALISMAYANLAR.txt, TEST_RAPORU.csv artifact always | CALISANLAR artifact olarak dahil: üretilme/değiştirilme semantiği ayrıca incelenmeli |
| kanal-kararlilik | K3/K5 | push/dispatch | cache restore → oncelikli_kanal_dogrula → kanal_kararlilik_takip → cache save | KARARLILIK_GECMISI.json cache; CSV/JSON artifacts | Günler arası geçmiş; cache hit/miss ve canlı probe eşdeğerliği |
| kaynak-puanlama-kontrol | K2/K5 | push/dispatch | py_compile kaynak_guven_puani → unittest discover test_kaynak_guven_puani | unit test sonuçları | Salt fixture testi, gerçek kaynak puanlama yürütmesi değil |
| madsc-11599-yedek-geri-yukle | K4 | dispatch | diagnose_11599_backups.py | stdout tanı | Adı geri yükle olsa da YAML restore yapmıyor; salt fark teşhisi |

## Yüksek öncelikli bulgular

1. `epg-gunluk` `contents:write` ve doğrudan `git push` içerir. `epg-pages` başarılı workflow_run sonrasında **gerçek GitHub Pages dağıtımı** ve 20 HTTP kontrolü yapar. Bunlar salt rapor üretimi değildir; onaysız yeni sistemde etkinleştirilmemeli.
2. `iptv-test` artifact kapsamına `CALISANLAR.m3u` ekler. Salt okunur workflow başlığı, çağrılan `iptv_test.py` dosyasının dosya yazmadığını ispatlamaz.
3. `madsc-11599-yedek-geri-yukle` adına rağmen YAML yalnızca `diagnose_11599_backups.py` çalıştırır; **gerçek geri yükleme komutu yoktur**.
4. `kanal-kararlilik` geçmişini GitHub Actions cache restore/save ile sürdürür; cache miss, günler arası kıyas ve rapor ayrıştırılmalı.
5. `ibo-epg-kimlik-denetimi` dört sayaç >0 kontrol eder; bu gerçek IBO Player cihaz doğrulaması değildir.

## İlerleme sınırı

Bu belge ikinci 12 workflow'u kaynak YAML düzeyinde çözümler. Önceki ilk 12 ile toplam **24 farklı workflow YAML** bu iki yürütme zinciri belgesinde ele alındı; diğer beş yüksek-risk workflow için ayrıca kaynak/komut ve betik raporları vardır (bir kısmı örtüşebilir). **92/92 davranışsal kabul yoktur: 0/92.** 26 güvenlik kuralı 0/26; 22 görev 0/22. Hiçbir Actions workflow tetiklenmedi; canlı yayın testi, GitHub Pages dağıtımı veya korunan dosya yazımı yapılmadı.
