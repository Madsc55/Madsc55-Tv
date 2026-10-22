# Madsc55-Tv — DEVAM NOTU

Güncelleme: 22 Ekim 2026 (Europe/Stockholm).
Son geliştirme commit SHA: 51267b0bee39522d2017381594827f4bf7d3265c
Bu notu kaydeden commit, yukarıdaki kod commit'inin doğrudan çocuğudur; kendi SHA'sı GitHub dosya geçmişindedir.

## Her yeni sohbette ilk adım
Bu dosyayı, BIRLESIK_KALICI_CALISMA_KURALLARI.md ve PROJE_HAFIZASI.md son bölümünü oku. GitHub main HEAD'ini doğrula. Tamamlanan inceleme ve testleri yeni sebep olmadan tekrarlama.

## Kullanıcının kalıcı görev ve sınırları
- Tek yazılabilir hedef: Madsc55/Madsc55-Tv, main. Main'in güncel durumundan K1–K5 eksiklerini topluca incele, kodları düzelt, yerel testleri çalıştır, ilerlemeyi GitHub'a kaydet. Engellenmedikçe çalışmayı sürdür, sonunda kanıtlı rapor ver.
- Eski 92 otomasyonun gerçek davranışsal entegrasyonunu doğrula; kaynak incelemesi veya fixture yeşil diye tamamlandı deme.
- Canlı kanal listelerini, EPG'yi, YEDEKLER, YENİLER, FAVORİLER ve cihaz favorilerini değiştirme. Logo/arşiv korumaları da geçerli.
- Eski Madsc55/madsc-tv salt okunur. Eski depoyu veya PR #71'i birleştirme; merge yapma.
- Her önemli geliştirmeden sonra bu dosyaya son kod commit SHA, tamamlananlar, başarısız testler, kalan görevler ve bir sonraki adımı yaz.
- Mevcut kota kararı: GitHub Actions için ayrıca açık izin gerekir; “devam/testleri çalıştır” tek başına bu izin değildir. Commitlerde [skip ci]; canlı probing ve üretim yazma yok.

## Bu pakette tamamlananlar
1. legacy_parity_cli ve legacy_99_bulk_audit çıktıları K1 enforce_local_output_path ile korunuyor: korunan dosya, symlink üst dizin ve mevcut hedef reddi. Audit ağ çağrısından önce hedefi kontrol ediyor; hedef üst klasör mevcut olmalı.
2. 92/99 sayım farkı kaynakla doğrulandı. Eski denetim beş merkezi workflow ile k1-protected-write-tests.yml ve madsc-hizli-on-kontrol.yml dosyalarını 92 kapsamından çıkarıyor.
3. Kaynak tree a88dfa874b6964dcaa4de7a8f9075af2f146acd8, commit ca374df3b9585c0d76a078db9536150ebbc260f7; eski denetim script blob SHA 9a35ecd797e5c1c595d6796cfffba6cd8a289853. Script içeriği ve tree kaydı eşleşti; 99 workflow yol/blob SHA docs/LEGACY_SOURCE_SCOPE.json içinde. Bu tur 99 YAML içeriği yeniden indirilmedi.
4. reconcile_legacy_scope kapsam değişimini reddediyor; offline_gate 92+7 ayrımını artık zorunlu denetliyor. Bu, davranışsal kabul değildir.
5. Yerel python -m madsc.offline_gate: 552 test başarılı; beş izole K kapısı success; 10 yardımcı komut ve 22 görev envanteri geçti. Kanıt: docs/K1_K5_OFFLINE_KANIT_2026-10-22.json (test edilen kaynak SHA256'ları dahil).

## Başarısız testler ve denemeler
- Bu pakette başarısız test yok. İlk düzeltmede 549, nihai kapsam paketiyle 552 test başarılı.
- GitHub tree sorgusunda slash içeren branch URL'si connector tarafından INVALID_ARGUMENT ile reddedildi; aynı sorgu tekrarlanmadı, belgelenmiş sabit tree SHA ile başarılı okundu.
- Son gözlenen Actions #39686179902 success, SHA d5d61317806dc7a00b762567695286e3779ceaf1; yeni kodun CI kanıtı değil. Bu tur Actions başlatılmadı.

## Açık işler / dürüst kabul durumu
- 92 davranış için tam kabul 0/92, runtime güvenlik 0/26, tam görev 0/22. Statik 99 kaynak envanteri ve 92 kapsam mutabakatı bu sayıları artırmaz.
- Eski/yeni aynı girdide gerçek execution çiftleri, artifact kökeni ve SHA, tetik/izin farkları, hata/timeout/retry ve yan etkiler karşılaştırılmalı. Mevcut snapshot karşılaştırıcısı provenance doğrulamıyor ve kabul vermiyor.
- K2 gerçek kaynak/lisans ve bağımsız geçmiş artifact kanıtı; K3 75 adayın zamanlı gerçek ölçümleri, üç örnek/6+ saat, ffprobe/ffmpeg, IBO kullanıcı cihaz sonucu, EPG/Pages ve görsel kimlik açık.
- K4 bağımsız harici yedek makbuzu ve hariciden izole restore, VOD/arşiv ve periyodik tetik kanıtı açık.
- K1 tüm yazıcıların çağrı noktaları ve 26 runtime kuralı; K5 gerçek uçtan uca kanıt zinciri açık.

## Sonraki somut adım
92 kapsamını yeniden araştırma: reconcile_legacy_scope ve pinned JSON kullan. K5 karşılaştırmalı kanıt çiftlerini bu 92 gerçek kaynak yoluna bağla; aynı girdi hashleri ve bağımsız köken doğrulamasının eksikliğini gider. Yeni rapor yazıcı ekleme; ortak K1 kapısını kullan. Gerçek cihaz/harici depolama kanıtını uydurma ve korunan üretim verilerine yazma. Mevcut kodun güvenle tamamlanabilen kısmını sürdür.

## İkinci önemli geliştirme — son kayıt
- Kod commit SHA: 268f16d304d4ce68fb9cbc201d51d34d793707c6. Önceki paket: 53ca22f2781d106139d52a20493e223b391418fd.
- history_origin_cli, batch_acceptance, handoff_acceptance ve legacy_notes_integrity ortak K1 çıkış kapısı + exclusive create kullanıyor. İlk üç komut korunan/mevcut/symlink hedefi kanıt işleme veya GitHub doğrulama başlamadan reddediyor. Çıktı üst klasörü mevcut olmalı.
- Son test: 554 test ve beş izole K1–K5 kapısı success; başarısız test yok. git diff --check temiz. Kanıt: docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET2.json. Önceki 552 sonucu önceki pakete aittir.
- Son CI artifact listesi yalnız metadata düzeyinde incelendi, 92 gerçek karşılaştırma kanıtı kabul edilmedi. Yeni Actions yok. Kabul sayıları 0/92, 0/26, 0/22.
- Sıradaki bağımsız yerel iş: tüm kalan yazma noktalarını çağrı zinciriyle denetle (özellikle ci_diagnostics --summary append ve canlı pilot rapor yazıcıları); onaysız canlı probing yapmadan gerçek yazma reddini fixture ile sına. Sonra 92 gerçek execution/artifact çiftlerinin köken ve girdi hash bağını tamamla. Bu tur tüm yazıcılar kapandı iddiası yok.
- Korunan yayın/EPG/yedek/favoriler ve eski depo değişmedi; PR #71 merge edilmedi. Bu kalıcı sınırlar sonraki sohbetlerde de geçerli.

## 22 Ekim 2026 — Otomatik devam ve sabah raporu
- Kullanıcı kalan işlerin otomatik sürdürülmesini ve sabah raporunu istedi. Mevcut saatlik ChatGPT görevi 6ad2b2e925bc8191a91b01728e57d707 güncellendi: Madsc55-Tv Otomatik Devam. Eski depoya yönelik talimat kaldırıldı; tek yazılabilir hedef Madsc55/Madsc55-Tv/main. Saatlik çalışma turu, kesintisiz çalışma garantisi değildir.
- Mevcut sabah görevi 6ad950197fbc8191b905c13fb344b920 güncellendi: Europe/Stockholm yaklaşık 08:00, flexible_schedule (saatin bir saat çevresinde). Sonuçları salt okunur doğrulayıp raporlar; geliştirme yapmaz. Mevcut günlük tekrarı korundu.
- Her geliştirme turu önce güncel main ve bu notu okur; tamamlanan işleri tekrarlamaz, kod/test ilerlemesini GitHub'a ve devir notuna kaydeder. Gece ara bildirim yerine kalıcı kayıt kullanır.
- Tüm korumalar geçerli: canlı kanal/EPG/yedek/yeni/favoriler değişmez, eski depoya yazılmaz, PR #71 merge edilmez; Actions/live probe ayrı izin olmadan çalıştırılmaz. Bitmiş veya kanıtlanmış olmayan kabul uydurulmaz.
- Son geliştirme SHA ve 554 test sonucu yukarıdaki kayıtta korunuyor; otomasyon kurmak yeni test veya geliştirme kanıtı değildir. Sonraki kod işi değişmedi: kalan yazıcıların K1 çağrı noktası denetimi.

## Üçüncü önemli geliştirme — güncel devam noktası
- Son kod commit SHA: e5222e2aff553c65c27e1678365a95fa6e40f39e. Başlangıç main: d70479db18814251247b7da6cae72520982a56b3. Bu notu kaydeden commit kodun doğrudan çocuğudur.
- Tamamlanan: CI JSON raporunda exclusive create, açık summary append için K1 protected/symlink/regular/hardlink kapısı ve O_NOFOLLOW/fstat; dört pilot JSON raporu mevcut ortak write_fixture_report üzerinden yazılıyor. K3 reason_counts tek yazıdan önce tamamlanıyor.
- progress_scorecard ve k5_channel_gate hedefi giriş işlemeden önce doğruluyor. artifact_transport/history_transport guard öncesi mkdir yapmıyor. History artifact indirme/extraction ve legacy rapor export hedefleri ortak K1 kapısında; üst klasör önceden mevcut olmalı.
- Başarısız test kaydı: LegacyReportExportTests.test_exports_separate_legacy_artifacts bir ara turda ERROR verdi; mevcut klasör reddinde eski ValueError sözleşmesi değişmişti. ValueError kontrolü korunarak düzeltildi, finalde geçti.
- Nihai test: python -m madsc.offline_gate, 562 test, K1/K2/K3/K4/K5 izole kapıları success; kaynak 92+7, 10 yardımcı komut ve 22 görev envanteri geçti. git diff --check temiz. Kanıt: docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET3.json, test edilen dosya SHA256 ve çözülen hata dahil. Ağ/Actions/cihaz testi yapılmadı.
- Gerçek dosya sınırları test edildi: mevcut summary ekleme; protected/symlink/hardlink/FIFO reddi; pilot rapor üzerine yazmama; guard reddinde klasör oluşturmama ve indirme çağırmama. Bu testler 26/26 tam runtime kabulü değildir; tüm yazıcılar tamamlandı denmez.
- Kalan ilk yerel iş: turkish_tv_batch_validation.py yalnız reports/ altındaki deneme M3U8 + JSON paketinin yazma yolunu güvenli ve tekil hale getir. Mevcut genel M3U yasağını gevşetme; korunan listelere yazma. Bu pakette bu dosya değiştirilmedi. Diğer kalan çağrı noktalarını da incele.
- Sonraki davranışsal iş: pinned 92 kaynak yoluna aynı girdi hashleri ve bağımsız execution/artifact kökeni bağlı eski/yeni karşılaştırma. 92/99 farkını tekrar araştırma; çözülmüş kapsam JSON'unu kullan.
- 0/92 tam legacy kabul, 0/26 tam runtime kabul, 0/22 görev kabulü korunuyor. IBO kullanıcı cihazı, 75 adayın zamanlı ölçümleri, EPG/Pages ve bağımsız harici restore kanıtları açık.
- Korunan yayın/EPG/yedek/yeni/favori verileri, eski repo ve PR #71 değişmedi. Saatlik otomasyon bu güncel kaydı başlangıç almalı; eski 554 sonucu güncel sonuç diye tekrarlamamalı.

## Dördüncü önemli geliştirme — toplu K3 kanıt yazıcısı
- Son kaydedilmiş kod commit SHA: fe40f60aa989c121144cdbdca0bdd38f7d67f607; başlangıç main 861932763c247b5402015e3bd33ab403854fddac.
- turkish_tv_batch_validation deneme M3U8 + JSON kanıt paketi ortak K1 yerel sınırlarına bağlandı. Genel M3U/M3U8 yasağı değiştirilmedi; yalnız sabit reports/MADSC55_TURKCE_TV_ADAY_DENEME.m3u8 yolu için dar, üretim izni vermeyen kapı var.
- İki dosya exclusive create ile yazılıyor; mevcut kanıt, symlink reports klasörü ve politika dışı M3U8 reddediliyor. JSON yazımı başarısız olursa bu çağrının oluşturduğu playlist geri alınıyor. Mevcut çıktı tarama/probe başlamadan reddediliyor.
- Yerel python -m madsc.offline_gate: 568 test ve K1–K5 izole kapıları başarılı. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET4.json. Ağ, Actions ve cihaz testi yapılmadı.
- Bu fixture sonucu 0/92, 0/26 ve 0/22 kabullerini değiştirmez. Korunan üretim playlist/EPG/yedek/favori dosyalarına dokunulmadı.
- Şu an üzerinde çalışılan sonraki iş: pinned 92 kapsamı için aynı input SHA256 ve ayrı execution/artifact kökenini zorunlu kılan karşılaştırma şeması. Gerçek GitHub origin doğrulaması olmadan acceptance verme.

## Beşinci önemli geliştirme — 92 workflow köken-bağlı karşılaştırma kontratı
- Son kod commit SHA: f222a81ce96901a8adc0dbc92a5213cf149500c9; taban fe40f60aa989c121144cdbdca0bdd38f7d67f607.
- compare_provenance_bound_batch yalnız reconcile_legacy_scope tarafından sabitlenen 92 yolu kabul ediyor. Yedi merkezi/kapsam dışı workflow kanıt çifti olarak verilemez.
- Her çift aynı input SHA256'yı kullanmalı. Legacy tarafı eski repo/dal/yol ve pinned git_blob_sha'ya; replacement tarafı yeni repo main ve beş merkezi workflow'dan birine bağlanıyor.
- Run id/attempt/head SHA ile artifact repository/run/head/id/SHA256 bağları ve iki tarafın ayrı execution/artifact kökenleri yapısal olarak zorunlu. Snapshot çıktı/yan etki/timeout/exit karşılaştırması bundan sonra bu bağın içinde yapılıyor.
- Offline metadata bağı gerçek GitHub API doğrulaması değildir: independent_origin_api_verified false, kabul 0/92 kalır. CLI yeni madsc-legacy-provenance-pairs-v1 şemasını tanır; eski snapshot modu geriye uyumlu fakat kabul vermez.
- Nihai yerel test: 570 test ve beş K kapısı success; docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET5.json. Başarısız test yok, git diff --check temiz; Actions/ağ/cihaz yok.
- Sıradaki somut iş: GitHub salt-okunur run ve artifact metadata doğrulamasını bu v1 kontratına bağlayan bağımsız verifier/client ekle. Gerçek legacy ve replacement run çifti bulunmadan 92 sayaçlarını artırma.
- Korunan listeler/EPG/yedek/yeni/favoriler, eski depo ve PR #71 değişmedi; merge ve Actions dispatch yapılmadı.

## Altıncı önemli geliştirme — bağımsız GitHub origin doğrulayıcısı
- Son kod commit SHA: 7b4855293564c1baafdca8246f932ca1a1e5986e; taban main 80bcb8dc4328351660d586730f9f4676307d4e6f.
- github_legacy_pair_client her execution için üç ayrı salt-okunur GitHub kaydı ister: run, run artifact listesi ve run head SHA'sındaki workflow blob'u. İki taraf için toplam altı API okuması yapar; dispatch/rerun/yazma yoktur.
- Repository, branch, workflow path, run id/attempt/head/event/conclusion, workflow blob SHA ve artifact id/name/run/head/SHA256 digest bağları fail-closed doğrulanır. Eksik digest, eksik pagination, yanlış blob veya repository reddedilir.
- İki origin API düzeyinde doğrulansa ve snapshot eşleşse bile behavioral_parity_accepted ve production_ready false kalır; reviewer/gerçek davranış kabulü ayrıca gerekir.
- Yerel toplu sonuç: 573 test ve K1–K5 izole kapıları başarılı. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET6.json. Başarısız unit test yok. Kapsamsız git diff --check bir kez signal 11 verdi; iki değişen dosyada scoped diff --check ve tam offline_gate geçti.
- Salt-okunur gerçek kontrol: yeni run 39686179902 artifactleri ve eski run 39590927353 artifactleri SHA256 digest taşıyor. Ancak eski run k1-protected-write-tests.yml, pinned 92 davranış kapsamının dışındaki yedi dosyadan biridir; bu iki run aynı-girdi 92 çifti değildir ve kabul verilmedi.
- Sıradaki somut iş: artifact içindeki manifestten input SHA256 ve snapshot bağını güvenli biçimde çıkarıp GitHub artifact digest/run origin doğrulamasına bağla. Sadece metadata içindeki beyanı aynı-girdi kanıtı sayma.
- Kabul sayaçları 0/92, 0/26 ve 0/22. Korunan veriler, eski depo ve PR #71 değişmedi; Actions başlatılmadı.

## Yedinci önemli geliştirme — artifact baytına bağlı aynı-girdi manifesti
- Son kod commit SHA: b1be6c247b769bc911773ed35d30b5991875b913; taban ca2b33fb45d188cbe2ce6a9ea164d677dc084e0e.
- legacy_pair_artifact, SHA256'sı API origin kaydına bağlı artifact ZIP'i sınırlı ve fail-closed okur. Yalnız tek madsc-parity-evidence.json kabul edilir; ekstra entry, symlink, büyük ZIP/manifest, aşırı sıkıştırma, bozuk/duplicate-key JSON reddedilir.
- Manifest repository/run/head/workflow_path, input_sha256 ve snapshot alanlarını execution origin beyanına bağlar. İki artifact manifesti aynı input SHA256 taşımadan pair karşılaştırması geçmez.
- Yerel sonuç: 576 test ve beş izole K kapısı success. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET7.json. Ağ/Actions/canlı probing yok.
- Bu, gelecek artifactlerin üretim kontratıdır; geçmiş run artifactleri bu manifest şemasıyla üretilmediği için geriye dönük 92 kabulü yaratmaz. behavioral_parity_accepted=false ve production_ready=false.
- Sıradaki somut iş: beşli workflow'ların opt-in parity artifact üretim yolunu bu manifest şemasına bağla; eski taraf için salt-okunur gerçek 92 run artifacti yoksa açık blocker olarak bırak. Actions izni olmadan çalıştırma.
- Kabul 0/92, 0/26, 0/22; korunan dosyalar/eski depo/PR #71 değişmedi.

## Sekizinci önemli geliştirme — K1 korumalı replacement manifest üreticisi
- Son kod commit SHA: c5a7060684e57f1e35d2b367e1757d5901dfcafb; taban f4198b56cd9e3e40c45797cb9ae74b934a1fa043.
- parity_manifest_writer gerçek input baytlarının SHA256'sından deterministik madsc-parity-artifact-v1 JSON üretir; snapshot şekli/digestleri mevcut fail-closed karşılaştırıcıyla doğrulanır. Çıktı yalnız reports/madsc-parity-evidence.json ve ortak K1 izole yazıcısı üzerinden exclusive-create/symlink/ancestor/root kontrolleriyle yazılır.
- Üretici yalnız Madsc55/Madsc55-Tv, main ve depoda gerçekten kurulu beş workflow yolunu kabul eder. Önceki replacement kontratındaki var olmayan K4/K5 adları madsc-04-arsiv-yedek.yml ve madsc-05-genel-bakim.yml düzeltilerek madsc-04-yedek.yml ve madsc-05-bakim.yml oldu. Eski adlar pinned legacy 92+7 kapsam dışlamasında aynen ve doğru biçimde kalır.
- Yerel python -m madsc.offline_gate: 580 test, beş izole K kapısı, 92+7 kapsam, 10 yardımcı komut ve 22 görev envanteri başarılı. Başarısız test yok; path-scoped git diff --check temiz. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET8.json.
- Actions, canlı probe, cihaz veya üretim yazması yapılmadı. Manifest üretimi artifact upload/origin doğrulaması veya parity kabulü değildir; sayaçlar 0/92, 0/26, 0/22.
- Açık engel: eski salt-okunur 92 workflow artifactlerinde v1 manifest üretimi yok. Gerçek aynı-girdi çifti için iki tarafta gerçek davranış girdisi ve snapshot üretimi gerekir; eski tarafa yazmadan bu tur tamamlanamaz.
- Sıradaki güvenli adım: replacement üreticisini gerçek davranış girdisi ve snapshotı olan açık opt-in job çağrılarına bağlayacak CLI/iş akışı kontratını ekle. Yalnız beyan edilen hash kabul etme; input baytını yerinde hashle. Actions izni olmadan çalıştırma ve legacy kabulü verme.

## Dokuzuncu önemli geliştirme — gerçek dosyadan opt-in manifest CLI
- Son kod commit SHA: 6b07cb1a7fa27e643e89cad6f1a7ffdb5a5d2c1a; taban e80291daf5225b60a1fa327610d5c88a0b9d138b.
- parity_manifest_cli beyan edilmiş bir input hash kabul etmez. Gerçek input ve snapshot dosyalarını read-only açar; O_NOFOLLOW (platformda varsa), fstat regular-file ve boyut sınırlarını uygular; input baytlarını kendisi SHA256 ile bağlar. Snapshot JSON duplicate key reddiyle okunur ve sıkı snapshot şemasından geçer.
- CLI repository/branch/run/head kimliğini GitHub runtime environment değişkenlerinden alabilir, workflow yolu açık argümandır ve gerçek beşli allowlist'ine tabidir. Çıktı yine sabit K1-korumalı reports/madsc-parity-evidence.json; artifact yüklemez, Actions başlatmaz, kabul vermez.
- İlk odak testinde test_real_file_bytes_are_hashed_and_written başarısız oldu: sabit test girdisinin beklenen SHA256 literal'i yanlıştı. Doğru hashlib sonucu yazıldı; odak testleri ve tam offline_gate geçti.
- Nihai yerel sonuç: 583 test ve beş K kapısı success; 92+7 kapsam, 10 yardımcı komut ve 22 görev envanteri geçti. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET9.json. Kabul 0/92, 0/26, 0/22.
- Açık: beş workflow'da gerçek davranış input/snapshot dosyalarını üreten ortak job sözleşmesi yok; mevcut fixture raporlarını davranış eşdeğerliği diye paketlemek yasak. Sıradaki adım, yalnız gerçek input/snapshot üretebilen workflow noktalarını statik eşleştirip güvenli opt-in entegrasyon planı/kontrat testi eklemek; Actions çalıştırmamak.

## Onuncu önemli geliştirme — ölçülmüş çıktı/yan-etki snapshot üreticisi
- Son kod commit SHA: 27c8b62165e511d09d42b319766a39d77994deb9; taban bedca31aef1998c51b23f468bf4bdd2950b9ea7c.
- parity_snapshot_writer ve CLI gerçek execution çıktı/yan-etki dosyalarını read-only açar, O_NOFOLLOW/fstat/2 MiB sınırı uygular ve SHA256'larını katı exit_code/timed_out/outputs/side_effects snapshot şemasına yazar. En az bir gerçek çıktı zorunlu; duplicate/control-character label, symlink, nonregular/büyük dosya ve mevcut snapshot reddedilir.
- Snapshot yalnız sabit reports/madsc-parity-snapshot.json yoluna ortak K1 izole writer ile exclusive create edilir; production_ready ve behavioral_parity_accepted false kalır.
- Uçtan uca offline test gerçek input baytı + gerçek çıktı baytı -> snapshot -> v1 manifest -> artifact ZIP digest/origin manifest doğrulamasını bağladı. Bu fixture origin/API veya 92 kabulü değildir.
- Nihai python -m madsc.offline_gate: 587 test, beş izole K kapısı, 92+7 kapsam, 10 yardımcı komut ve 22 görev envanteri başarılı. Başarısız test yok; değişen dosyalarda git diff --check temiz. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET10.json.
- Actions/live probe/production write/eski repo yazısı yok. Kabul sayaçları 0/92, 0/26, 0/22.
- Açık blocker: mevcut beş workflow ortak gerçek davranış input ve side-effect dosyası üretmiyor; fixture raporunu parity kanıtı diye yeniden adlandırmak yasak. Sonraki güvenli iş workflow job'larını read-only statik denetleyip hangi gerçek çıktının hangi input/side-effect kaydıyla bağlanabileceğini makine-okunur readiness raporunda fail-closed göstermek; eksik olanı acceptance saymamak.

## On birinci önemli geliştirme — beş workflow parity readiness denetimi
- Son kod commit SHA: 79ddf0e7bbec7cdb47fb1a79e285f35d5c5e9b02; taban f4f14fd668e37ca382f50c2991c4c1616ed7fbd9.
- parity_workflow_readiness tam olarak depoda kurulu beş merkezi workflow'u okur ve açık opt-in, opt-in koşulu, snapshot CLI, manifest CLI, manifest artifact upload ve üretici sırası işaretlerini fail-closed denetler. Workflow kaynak SHA256'larını rapora bağlar.
- Whole-line comment örnekleri readiness sayılmaz; symlink, nonregular, boş/büyük ve UTF-8 olmayan workflow kaynağı reddedilir. Rapor yalnız reports/parity-workflow-readiness.json yolunda ortak K1 exclusive writer ile yazılabilir.
- Gerçek mevcut sonuç: 0/5 workflow marker kontratı tamam. Bu dürüst blocker kaydıdır. Tam marker'lı sentetik test bile runtime_origin_verified, real_behavior_ready ve behavioral_parity_accepted alanlarını false/0 tutar.
- Nihai python -m madsc.offline_gate: 590 test ve beş izole K kapısı success; 92+7 kapsam, 10 yardımcı komut, 22 görev envanteri geçti. Başarısız test yok; path-scoped git diff --check temiz. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET11.json.
- Actions/live probe/production write/eski repo yazısı yok. Kabul 0/92, 0/26, 0/22.
- Açık blocker: gerçek beşli job'larda ortak input/snapshot/side-effect sözleşmesi ve legacy 92 v1 artifactleri yok. Sıradaki güvenli adım, yalnız izole/gerçek dosya çıktısı olan K1-K5 yollarında açık opt-in marker zincirini eklemek için ortak workflow sözleşmesini tasarlamak; ağ/canlı/korunan veri yollarını bu entegrasyona dahil etmemek ve Actions çalıştırmamak.

## On ikinci önemli geliştirme — K4 ve K5 gerçek dosya dilimlerinde opt-in zincir
- Son kod commit SHA: 03fbcdb42cad69ae69641f2d4033b8537ee0f7b6; taban 3409a2c7a50ec20ae215f207c0af053a0740be05.
- madsc-04-yedek.yml restore drill'i ve madsc-05-bakim.yml içindeki K2 handoff dilimi default false allow_parity_evidence girdisi aldı. Her iki zincir de yalnız açık opt-in ile snapshot -> manifest -> tek JSON artifact üretir; depo permissions read-only kalır.
- K4 manifest input'u restore_drill'in gerçekten tükettiği reports/k4-source/nested/sample.txt, ölçülen output reports/k4-restore-drill.json. K5/K2 diliminde input artifact_transport'un tükettiği reports/k2-input.m3u, output reports/k2-candidates.json. Testler üretici komut < snapshot < manifest < upload sırasını zorunlu kılar.
- K1, standalone K2 ve K3'e sahte ortak input marker'ı eklenmedi. Readiness sonucu marker kontratı 2/5, fakat runtime_origin_verified=0, real_behavior_ready=0 ve acceptance=0; workflow'lar bu tur çalıştırılmadı.
- Nihai python -m madsc.offline_gate: 593 test, beş izole K kapısı, 92+7 kapsam, 10 yardımcı komut ve 22 görev envanteri başarılı. Başarısız test yok; değişen dosyalarda git diff --check temiz. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET12.json.
- Actions/live probe/production write/eski repo yazısı yok. Kabul 0/92, 0/26, 0/22.
- Açık blocker: iki opt-in zincirin gerçek run/artifact kökeni henüz yok; Actions için ayrı izin gerekir. Eski read-only 92 artifactlerinde v1 manifest yok. Sıradaki güvenli yerel iş, K1/standalone K2/K3 için gerçek ve karşılaştırılabilir input bağının bulunup bulunmadığını statik komut/veri akışıyla sınıflandırmak; yoksa blocker bırakmak.

## On üçüncü önemli geliştirme — K1 guard gerçek input/output bağı
- Son kod commit SHA: 32db584bdeff7d2bc42bb54c68d7bf3c2aa3af17; taban e984ab5ddb8d043b974da93a74f7a625f0263af2.
- madsc-01-guvenlik.yml içindeki gerçek K1 guard'ın tükettiği config/shadow_manifest.json parity input oldu. Guard stdout'u bash pipefail + tee ile reports/k1-guard.txt dosyasına alınır; böylece hata kodu gizlenmeden gerçek çıktı snapshot içinde hashlenir.
- Default false allow_parity_evidence yalnız açık opt-in ile snapshot -> manifest -> reports/madsc-parity-evidence.json artifact zincirini çalıştırır. Permissions read-only, protected/production write yok. Readiness marker kontratı 3/5 oldu; runtime ve acceptance hâlâ 0.
- Standalone K2 ve K3 dosya tabanlı ortak karşılaştırılabilir girdi sunmuyor; mevcut yollar canlı/harici/örtük girdili olduğundan sahte marker eklenmedi.
- Odak test komutunda olmayan tests.test_madsc_guard modülü çağrıldığı için bir ImportError kaydedildi; gerçek tests.test_guard ile odak 18/18 ve ardından tam offline_gate geçti.
- Nihai python -m madsc.offline_gate: 593 test ve beş izole K kapısı success; 92+7 kapsam, 10 yardımcı komut ve 22 görev envanteri başarılı. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET13.json. Actions çalıştırılmadı; kabul 0/92, 0/26, 0/22.
- Sıradaki güvenli yerel adım: K2/K3 blocker sınıflamasını makine-okunur dataflow raporuna bağlamak ve readiness denetçisinin marker eksikliğini gerçek input sınıfıyla açıklamasını sağlamak. Canlı/harici input için Actions veya probing yapma.

## On dördüncü önemli geliştirme — parity input veri-akışı sınıflaması
- Son kod commit SHA: 51267b0bee39522d2017381594827f4bf7d3265c; taban 2d584f703aabb3f7ab5c2af17c2683e5c3dd1f13.
- parity_workflow_readiness artık K1, K4 ve K5 için gerçek tüketici komutu, tüketilen input ve üretilen output tokenlarını parity snapshot/manifest sırasından bağımsız olarak doğrular. Üç yol `isolated_file_bound`; marker mevcut olsa bile tüketici input'u kayarsa bağ fail-closed bozulur.
- Standalone K2 `live_stream_sources_required`, standalone K3 `external_delivery_or_notification_state_required` olarak makine-okunur `external_or_live_input_blocked` sınıfındadır. Fixture input veya sahte runtime kanıtı üretilmedi.
- Odak 7/7 ve nihai `python -m madsc.offline_gate` 594/594 test başarılı; beş izole K fixture kapısı, 92+7 kapsam, 10 yardımcı komut ve 22 görev envanteri geçti. Başarısız test yok; `git diff --check` temiz. Kanıt `docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET14.json`.
- Actions/live probe/production write/eski repo yazısı yok. Statik file binding 3/5; runtime origin ve gerçek behavior ready 0, kabul 0/92, 0/26, 0/22.
- Açık blocker: üç opt-in zincirin bağımsız gerçek run/artifact kökeni için ayrıca Actions izni gerekir; eski read-only 92 artifactlerinde v1 manifest yok. K2/K3 canlı veya harici girdiyi yetkisiz kullanmadan karşılaştırılabilir ortak gerçek dosyaya bağlanamıyor.
- Sıradaki güvenli yerel adım: readiness JSON şemasını ve üç statik bağın kaynak SHA/input/output alanlarını parity manifest karşılaştırıcısının preflight doğrulamasına bağlamak; bu işlem runtime/acceptance üretmemeli ve Actions çalıştırmamalı.
