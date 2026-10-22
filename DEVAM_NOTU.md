# Madsc55-Tv — DEVAM NOTU

**En yeni kayıt:** Kontrollü timeout/failure workflow bağlantısı; kod e10fcdc4c878305ca44e110b29ad88128cf16cb2; 632 yerel test ve beş izole K kapısı başarılı. Tanı artifact baytlarının bağımsız doğrulaması sonraki iştir. Güncel ayrıntılar dosyanın sonundadır.

## YENİ SOHBETE GEÇİŞ — önce bu özeti oku (22 Ekim 2026)

- Kullanıcı bu sohbetten yeni sohbete geçiyor. Geliştirmeyi baştan kurma; bu dosyanın güncel main sürümü, BIRLESIK_KALICI_CALISMA_KURALLARI.md ve PROJE_HAFIZASI.md son kayıtları başlangıç kaynağıdır. Yeni sohbette önce GitHub main HEAD'ini doğrula; otomatik görev arada ilerlemişse yeni kayıt üstün gelir. Önceki tüm sohbetlerin otomatik eksiksiz görüldüğünü varsayma.
- Tek yazılabilir hedef **Madsc55/Madsc55-Tv/main**. Bu geliştirme öncesi main: **c1fe77e309eaa6332c54add4d858058c7ee993de**. Son geliştirme kodu: **e10fcdc4c878305ca44e110b29ad88128cf16cb2**. Bu devir bir not kaydıdır, yeni kod/test değildir; kendi commit SHA'sı dosya geçmişindedir.
- Son test kanıtı: **632 yerel test + beş izole K1–K5 kapısı success**; kaynak 92+7, 10 yardımcı komut ve 22 görev envanteri geçti. docs/PARITY_CONTROLLED_TIMEOUT_KANIT_2026-10-22.json güncel kanıttır. GitHub Actions başlatılmadı.
- Tamamlanmış işleri tekrarlama: 92/99 kapsam mutabakatı; K1 rapor/summary/aktarım yazıcı korumaları; izole deneme playlist+JSON paketi; FIFO ve okuma sırasında değişen dosya reddi; gerçek dosyadan snapshot/manifest üreticileri; K1/K4/K5 default-false opt-in kancaları; kaynak Git blob/SHA256 + output role preflight'ının provenance CLI/API/artifact karşılaştırıcılarına bağlanması. Ön kontrol yalnız açık replacement_workflow_root argümanıyla devrededir; argüman yoksa checked=false. Bunlar gerçek legacy runtime kabulü değildir.
- **İlk sıradaki somut kod işi:** failure diagnostic artifact üyelerinin hash ve outcome JSON doğrulamasını mevcut provenance artifact/API zincirine bağla. K1/K4/K5 ölçülen timeout adaptörü ve workflow bağlantısını tekrar kurma; ayrıntılı sonraki adım son kayıtta.
- Açık dış kanıtlar: K2/K3 karşılaştırılabilir ortak input canlı ağ/harici geçmiş/aday kaynaklarına bağlı; eski 92 tarafta v1 manifest artifact eksik; opt-in gerçek run/artifact kökeni yok. 75 adayın zamanlı üç örnek/6+ saat ölçümleri, gerçek ffprobe/ffmpeg, kullanıcı IBO Player Pro cihaz sonucu, EPG/Pages/logo kimliği, bağımsız harici backup/restore ve VOD/arşiv/periyodik tetik kanıtları açık. **Tam kabuller 0/92, 0/26, 0/22**; fixture yeşilini bunlara ekleme ve genel bitiş yüzdesi uydurma.
- **Kesin korumalar:** canlı ana kanal listeleri/playlist, EPG/XMLTV, YEDEKLER, YENİLER, FAVORİLER, cihaz favorileri, logolar ve korunan arşivlere yazma. Eski Madsc55/madsc-tv salt okunur; eski depoya commit/Actions yapma, eski depoyu veya PR #71'i birleştirme; merge yapma. Kanıt olmadan eski otomasyon kapatma.
- **Test/kota:** güvenli yerel offline test ve kod/not kayıtları yetkili. GitHub Actions dispatch/rerun, canlı stream probing ve üretim yazma için ayrı açık izin yok; çalıştırma. Commitler [skip ci]. Her önemli gelişmeden sonra son kod SHA, yapılan iş, failure'lar, kanıtlar, kalanlar ve sonraki adımı bu dosya ve PROJE_HAFIZASI.md'ye kaydet. Eşzamanlı main değişirse yeniden oku, yeni commitleri ezme; yalnız erişilebilir commit/run kanıtını başarı say.
- **Otomatik devam doğrulandı:** saatlik Madsc55-Tv Otomatik Devam görevi 6ad2b2e925bc8191a91b01728e57d707 aktif; prompt en son kod/test ve sıradaki işe güncellendi. Güncel notu her tur okur. Sabah raporu görevi 6ad950197fbc8191b905c13fb344b920 aktif; Europe/Stockholm günlük 08:00 civarı, raporlama salt okunur. Yeni sohbet için aynı görevleri tekrar oluşturma. Saatlik tur, kesintisiz çalışma/bitiş garantisi değildir; görev sonuçları ilgili görev sohbetinde görünebilir, bu yeni sohbeti otomatik devraldığı iddia edilmez.
- Yeni sohbet başlangıç talimatı: “Madsc55/Madsc55-Tv main dalındaki DEVAM_NOTU.md dosyasının en üstündeki yeni sohbet özetini ve en son kayıtlarını oku. Güncel HEAD'i doğrula; yapılmış işleri tekrarlamadan ilk açık somut işten devam et. Tüm korumaları uygula, değişiklik ve kanıtları GitHub'a kaydet.”

Güncelleme: 22 Ekim 2026 (Europe/Stockholm).
Son geliştirme commit SHA: e10fcdc4c878305ca44e110b29ad88128cf16cb2
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

## Parity dosya okuma güvenliği — güncel kayıt
- Son kod commit SHA: 7635cbe28071df818ecdefb77cc43e40ea5ffb09; taban 53ca334a0eb7b209251f41b06909e5ebb0cfdf85. Eşzamanlı otomatik turdaki 51267b0 K2/K3 readiness geliştirmesi ve 53ca334 devir kaydı korunarak üzerine normal commit hazırlandı; eski HEAD'e zorla yazılmadı, merge yapılmadı.
- parity_manifest_cli ve parity_snapshot_writer FIFO açılışında fstat'a ulaşmadan bekliyordu. Gerçek FIFO alt süreç testi iki entrypoint'te de 2 saniye timeout verdi. O_NONBLOCK ile regular olmayan girdi artık beklemeden reddedilir.
- Gerçek dosya okuma sırasında değiştirildiğinde önceki iki negatif test hata atmadan kanıt üretildiğini gösterdi. Descriptor ve pathname dev/inode/size/mtime_ns/ctime_ns/nlink değerleri okuma sonunda denetleniyor; değişim, kaybolma veya aynı boyutta inode değiştirme tespit edilirse kanıt yazılmıyor. Bu metadata tutarlılık kontrolüdür; tam atomiklik veya execution boyunca input dondurma iddiası değildir.
- Başarısız test kaydı: FIFO manifest/snapshot alt vakalarında 2 ERROR (TimeoutExpired); input/output değişiminde 2 FAIL (ValueError gelmedi). Düzeltme sonrası hepsi geçti. Aynı boyutta dosya değiştirme de her iki entrypoint'te sınandı; ret durumlarında reports oluşmadı.
- Nihai birleşik yerel sonuç: python -m madsc.offline_gate, 598 test ve beş izole K kapısı success; 92+7 kapsam, 10 yardımcı komut ve 22 görev envanteri geçti. Kanıt docs/PARITY_FILE_READ_KANIT_2026-10-22.json. Paket14 dosyası otomatik turun ayrı kanıtı olarak aynen korundu.
- Kaydetme sırasında main değiştiği için ilk ref güncellemesi doğrulanamadı. Main yeniden okundu, yeni turun kod/testleri alınarak regresyon tekrarlandı ve güncel HEAD üzerine kaydedildi. Yalnız main'den erişilebilir son commitler ilerleme kanıtıdır.
- Önceki devirde K3 için yazılan external_delivery_or_notification_state_required ifadesi kaynak kod sınıfı değildir. Gerçek readiness kodundaki K3 engeli canlı stream probe/harici aday kaynağı; sınıf external_or_live_input_blocked'dır. K2 de canlı ağ/harici history girdisine bağlıdır. Bu ifadeleri delivery sistemi kurulmuş gibi yorumlama.
- Actions/live probe/cihaz/production write/eski depo yazısı yok. Korunan yayın listeleri, EPG, YEDEKLER/YENİLER/FAVORİLER ve PR #71 değişmedi; kabul 0/92, 0/26, 0/22.
- Sıradaki güvenli yerel iş: mevcut readiness'deki üç statik file binding kaydını parity manifest preflight doğrulamasına bağla; marker ya da yerel dosya hashini bağımsız runtime veya 92 kabulü sayma. Gerçek opt-in run/artifact kökeni ve legacy 92 v1 manifest eksikliği açık.

## Manifest karşılaştırıcısında kaynak workflow ön kontrolü — güncel kayıt
- Son kod commit SHA: 7beab850d06fb40d491d233d8bc3108ea984782b; taban 436266996ba86e28dcef9951954a1e460d21a801. Otomatik readiness geliştirmesi ve önceki FIFO/mutasyon düzeltmeleri korundu.
- Readiness kayıtlarına gerçek workflow_blob_sha (Git blob), workflow_sha256 ve declared_file_binding {consumer_command,input_path,output_label,output_path} eklendi. preflight_replacement_execution, sunulmuş bir readiness JSON'una güvenmeden kaynak workflow'ları yeniden okur.
- Kaynak markerları + statik input/output kontratı, origin.workflow_blob_sha ve snapshot'ın beklenen output label'ı birlikte doğrulanır. Yanlış/eski kaynak blob, kaynak drift'i, eksik çıktı rolü ve ortak izole input sözleşmesi olmayan K2/K3 fail-closed reddedilir. K1/K4/K5 kapsamı statik kontrattır; gerçek yürütme kabulü değildir.
- compare_provenance_bound_pair/batch, API origin doğrulayıcısı ve artifact manifest doğrulayıcısı replacement_workflow_root açık argümanıyla aynı kapıyı kullanır. CLI: --replacement-workflow-root PATH yalnız madsc-legacy-provenance-pairs-v1 girdisinde geçerlidir. Kaynak kökü, iddia edilen koşunun workflow blob'u ile aynı baytları içermelidir; yeni main'den farklı tarihsel kaynakta ön kontrol reddedilir.
- Argüman yoksa replacement_workflow_contract_checked=false ve replacement_static_preflight=null olur. Batch açıkça kaç çiftin statik kontratının kontrol edildiğini raporlar. v1 manifest formatı korunur. Statik ön kontrol input baytını veya bağımsız runtime kökenini doğrulamaz; ilgili alanlar false kalır.
- Uçtan uca test gerçek src.madsc_guard komutunu geçici gerçek config baytlarıyla çalıştırdı; stdout -> dosya snapshot'ı -> manifest -> ZIP -> kaynak preflight zinciri geçti. Bu testte legacy taraf fixture, API testi fake fetcher kullandı; gerçek 92 legacy execution veya canlı API kabulü yok.
- Nihai yerel python -m madsc.offline_gate: 605 test, beş izole K kapısı, 92+7 kaynak kapsamı, 10 yardımcı komut ve 22 görev envanteri success. Bu pakette başarısız test yok; git diff --check temiz. Kanıt docs/PARITY_WORKFLOW_PREFLIGHT_KANIT_2026-10-22.json kaynak hashleri ve statik binding kayıtları dahil.
- Korunan listeler/EPG/yedek/yeni/favori, eski repo ve PR #71 değişmedi. Actions veya gerçek ağ/cihaz testi çalıştırılmadı. Kabul 0/92, 0/26, 0/22; statik preflight bunu artırmaz.
- Sıradaki güvenli yerel iş: yalnız opt-in K1/K4/K5 tüketicileri için işlem öncesi/sonrası input hash bağını kur; tüketici çalışırken değişen dosyadan manifest üretilmesin. Gerçek runtime/artifact kökeni için ayrı Actions izni, eski 92 v1 manifestleri için mevcut salt-okunur kanıt gerekir; K2/K3 harici/canlı girdi engelleri açık.

## 22 Ekim 2026 — Opt-in parity girdi hash kontrolü (yeni sohbet)
- Kod commitleri: ffa4262c1ffa27e3c5c463810d840055aaf4640f (K1), b26d613e18afc93522b88676eac41893962927f0 (K4), 79ba7859632a4b88b698c5d8c80091f079dc1ad4 (K5/K2). Başlangıç main d2d2ea8acb661ea23653c5b8365d3904e7302491.
- Yalnız allow_parity_evidence=true iken gerçek tüketici komutundan hemen önce sha256sum kaydı alınıyor; manifest öncesinde ve manifest sonrasında sha256sum --check --status ile değişen input reddediliyor. Varsayılan opt-in false korunuyor; ayrı workflow/Actions başlatılmadı.
- ÖNEMLİ: Bu turda offline test çalıştırılmadı; 605 test önceki commitin kanıtıdır, yeni kodun test başarısı değildir. YAML/kontrat ve toplu offline_gate testleri henüz doğrulanmalı. Kodun hash kontrolü input dosyasının atomik dondurulması veya gerçek legacy runtime parity kanıtı değildir.
- Sonraki adım: kaynak YAML'larını ve statik readiness testlerini doğrula, gerekli kontrat testlerini güncelle, tek toplu offline regresyon çalıştır, başarısızlık varsa düzelt. GitHub Actions için ayrı izin gerekir. Kabul 0/92, 0/26, 0/22.
- Korunan playlist/EPG/YEDEKLER/YENİLER/FAVORİLER/logo/arşiv, eski repo ve PR #71 değişmedi; merge yapılmadı.

## 22 Ekim 2026 — Hash sırası kontrat testi
- Kod/test commit: 0abc1e5ab3243eb0a4bfd7d5df268153e597067b. tests/test_parity_workflow_integration.py içinde K1/K4/K5 için girdi hash kaydı < gerçek tüketici < ilk hash doğrulaması < manifest CLI < ikinci hash doğrulaması < artifact upload sırasını statik olarak denetleyen test eklendi.
- Test çalıştırılmadı: yerel container GitHub DNS çözümlemesi başarısız (Could not resolve host: github.com); GitHub Actions kota izni olmadığı için dispatch/rerun yapılmadı. 605 eski kanıt yeni commit için geçerli sayılmaz.
- Sonraki adım: erişilebilir checkout ile tek offline_gate, statik test ve YAML doğrulaması; hataları düzeltip kanıt SHA'larıyla kaydet. Tam kabul 0/92, 0/26, 0/22. Korunan üretim verileri, eski repo ve PR #71 değişmedi.

## 22 Ekim 2026 — 3/3 statik hash sırası kontrolü
- Kaynak HEAD ddebbac51b15a16e6d86e67633a504f9c6ca8a0c üzerinde K1/K4/K5 YAML dosyaları GitHub'dan yeniden okunarak tam sıralama koşulları 3/3 sağlandı. Kanıt: docs/PARITY_HASH_ORDER_STATIC_KANIT_2026-10-22.json (commit de0baa35997eb7eadcab996291c339651ae9970e).
- Bu sonuç yalnızca statik string/konum kontrolüdür; Python unittest, YAML parser, offline_gate, GitHub Actions ve gerçek davranışsal parity testleri ÇALIŞTIRILMADI. Yerel git clone DNS engelli; Actions izinsiz tetiklenmedi. Sonraki iş erişilebilir yerel checkout ile gerçek toplu test, hata düzeltmesi ve güvenli kanıt.

## Manifest girdisi işlem öncesi digest kaydına bağlandı — güncel devam
- Son kod commit SHA: 788a4b76ed96677d0ec05cb90e2f4fe835b611f1; taban e1b4997b796d4f17a0f08e4b59cf9a9c8d548aa8. Diğer sohbetin ffa4262/b26d613/79ba785 hash kontrolleri ile 0abc1e5 statik sıra testi korunarak kullanıldı. Başlangıç 8883d5c üzerinde 605 test gerçekten çalıştırılıp geçti; ardından yeni main'deki test de alınarak final regresyon yapıldı. Önceki DNS/“test edilmedi” kayıtları o turların durumudur, güncel sonuç aşağıdadır.
- parity_manifest_cli --input-digest-receipt kaydını bounded/nonblocking/non-symlink okuyucuyla okur. Tam tek satır sha256sum biçimi, lowercase digest ve birebir input yolu zorunludur. Manifestte kullanılan input baytlarının SHA256'sı işlem öncesi kayıtla eşleşmezse henüz snapshot/manifest yazmadan reddedilir. Yanlış digest/yol, çok satır veya bozuk kayıt çıktı oluşturmaz. Argüman yoksa sonuç input_digest_receipt_matched=false; v1 manifest şeması korunur.
- K1/K4/K5 manifest komutları bu kaydı açıkça kullanıyor. İlgili değiştirilen adım adları Türkçeleştirildi. Default-false opt-in, read-only permission ve üç kaynak sözleşmesi korunur; readiness/preflight artık capture < consumer < snapshot < ilk check < manifest+receipt < ikinci check < upload sırasını da ister. Eksik receipt bağı statik ön kontrolden geçmez.
- Gerçek workflow consumer/run blokları temporary dizinde bash -e -o pipefail ile çalıştırıldı (GitHub Actions değil). Üç gerçek tüketici: K1 guard, K4 restore drill, K5/K2 artifact producer. Her biri stable, tüketici sonrası değişim, precheck sonrası/manifest öncesi değişim, manifest sonrası değişim ve opt-out senaryolarında sınandı.
- Stable girdide manifest SHA doğru. İlk iki değişim senaryosunda manifest yok; manifest sonrası değişimde yerel manifest kalır fakat başarısız son kontrol publish simülasyonuna geçirmez. Opt-out girdide digest kaydı/parity manifest yok. Yayınlama bu testte yalnız yerel simülasyon işaretidir; gerçek artifact upload veya legacy runtime değildir.
- Nihai python -m madsc.offline_gate: **610 test ve beş izole K1–K5 kapısı success**, 92+7 kaynak, 10 yardımcı komut ve 22 görev envanteri geçti. Yeni geliştirmede başarısız test yok; git diff --check temiz. Kanıt docs/PARITY_INPUT_RECEIPT_KANIT_2026-10-22.json; taban SHA, test edilen kaynak hashleri, readiness ve senaryolar dahil.
- Bu endpoint hash bağları tam atomik input dondurma veya geçici değiştirip geri alma saldırısının tam ispatı değildir. Bağımsız run/artifact ve execution boyunca değişmez girdi kökeni hâlâ ayrı kanıt ister. Korunan kanal/EPG/yedek/yeni/favori/logolar/arşiv, eski repo ve PR #71 değişmedi; merge/Actions/live probe yok. Kabul 0/92, 0/26, 0/22.
- Sonraki güvenli yerel iş: üç opt-in üreticinin başarısız tüketici ve timeout durumlarında gerçek exit-code/snapshot/hata artifact akışını koru; şu an başarı yolundaki sabit --exit-code 0 failure parity kanıtı değildir. Kaynak preflight ve input digest bağını tekrar kurma. Hata raporlamak başarı kapısını veya işin gerçek hata kodunu gizlememeli.

## 22 Ekim 2026 — Failure/timeout snapshot regresyon testleri
- 823ab04e80a2e2842d49fbd2951eb92bd7c1bce8 commit'inde tests/test_parity_snapshot_writer.py içine iki yeni test eklendi: exit_code=23/timed_out=false ve exit_code=124/timed_out=true gerçek çıktı SHA256 korunumu; eksik failure log dosyası snapshot yazmadan fail-closed.
- Bu turda testler ÇALIŞTIRILMADI (container GitHub DNS engeli). Önceki 610 yerel test, bu yeni test commit'ini kapsamaz. Workflow tüketicilerindeki sabit --exit-code 0 henüz düzeltilmedi; failure/timeout opt-in akışını gerçek exit code ve log ile bağlamak ilk açık iştir. Actions izinsiz tetiklenmedi. Tam kabuller 0/92, 0/26, 0/22.

## 22 Ekim 2026 — Opt-in tüketici failure snapshot akışı
- Kod: K1 118bed0e6e8869291fc305cabe4b7119a58bc8b5; K4 86164e1cac9984f35ab17923e78fee9d78990a57; K5 903ea0d750acf70e161de9d37879c0a07ded39fc. Tüketici nonzero dönerse gerçek exit code yakalanır, opt-in ve çıktı mevcutsa nonzero snapshot denenir, ardından orijinal exit code ile workflow step başarısız olur. K1 pipefail tüketici status'u PIPESTATUS[0] ile alınır. Başarılı yolun eski snapshot/manifesti korunur.
- Test kodu: 13008e629292a675bd6f03aada7829060f6e8f56 ve b3fab67ce9b5ce3761570d6ff489fb5160a16cec. Statik nonzero snapshot sözleşmesi eklendi; opt-in adım sayımı consumer içindeki failure snapshot'tan ayrıldı.
- SINIR: Çıktı üretmeden hata veren K4/K5 için snapshot oluşturulmaz (fail-closed); timeout-minutes ile runner kesilirse snapshot garantisi yok, timed_out=true yolu henüz bağlanmadı. Yeni kod/testler henüz yerelde ÇALIŞTIRILMADI, son 610 test önceki commit kanıtıdır. Actions tetiklenmedi. Sonraki adım yerel toplu regresyon + failure/timeout uçtan uca test; hata olursa düzelt. Kabul 0/92, 0/26, 0/22; üretim ve eski depo korumaları değişmedi.

## 22 Ekim 2026 — Hata snapshot'ı başarısızken orijinal exit code korunumu
- K1 209c368b3c70827e60939aa77b96ff6465ccd171, K4 07341e60fbc22d271103b5f6f5ecb5aa3a7171a9, K5 3621d20ab53999697c1079437a15e6d0ba5f57f1: opt-in failure snapshot CLI kendisi başarısız olsa bile uyarı verip tüketicinin orijinal nonzero exit code'una ulaşılır. Test kontratı c89f62480844f9eb167c9e0cca44aae34e5235b5.
- Test henüz çalıştırılmadı: yerel git ls-remote de GitHub DNS hatası verdi. 610 eski test kanıtı bu commitleri kapsamaz. Workflow job timeout-minutes nedeniyle sert kesilme halinde timed_out=true snapshot garantisi yok; ayrı kontrollü yerel timeout tatbikatı ve test gerekiyor. Actions tetiklenmedi. Tam kabuller 0/92, 0/26, 0/22.

## 22 Ekim 2026 — Gerçek süreç gözlemi ve K1 pipe hata düzeltmesi
- Son kod commit SHA: 09e3b31ddc86c0a01ba9ea1bff153416705319c5. Başlangıç main c6e74cc53f21aae486cda7f191e3a11836ef87f8. Eşzamanlı failure snapshot kodu korundu ve ilk kez bu pakette toplu yerel regresyondan geçirildi.
- madsc.parity_process.observe_process gerçek returncode/stdout/stderr ölçüyor; monotonic timeout, shell kullanmayan argv, iki pipe eşzamanlı okuma, akış başına 1 MiB sınırı ve process-group temizliği var. Normal exit 124 timeout sayılmıyor. Gerçek timeout stderr çıktısı mevcut snapshot yazıcısına bağlanarak test edildi. Çıktı taşmasında eksik kanıt üretilmez. Bu API komut yetkilendirmesi veya üretim koruma sandbox'ı değildir; çağıran güvenli komutu seçmeli.
- K1 consumer PIPESTATUS artık hem tüketici hem tee sonucunu koruyor: tüketici başarılı olsa bile tee failure yeşile dönmez; tüketici failure önceliği korunur.
- İlk offline_gate 621 testte 7 failure verdi: altı girdi-mutasyon alt senaryosu yeni consumer içindeki failure snapshot komutunu yanlışlıkla başarı adımı seçiyordu; standalone başarı snapshot seçimi düzeltildi. Bir descendant kapanış testi OS sinyal yarışı nedeniyle erken okuyordu; 1 saniyelik sınırlı kapanış kontrolü eklendi. Başarısızlıklar gizlenmedi.
- Nihai python -m madsc.offline_gate: 621 test ve beş izole K1–K5 kapısı success; 92+7 kaynak, 10 yardımcı komut, 22 görev envanteri geçti. git diff --check temiz. Kanıt docs/PARITY_PROCESS_KANIT_2026-10-22.json; test edilen kaynak hashleri kayıtlı. Actions/ağ/cihaz testi yapılmadı.
- ÖNEMLİ AÇIK: süreç gözlem API'si henüz workflow tüketicilerine bağlanmadı. K1/K4/K5 mevcut failure snapshot akışı yalnız mevcut normal çıktı için çalışıyor; gerçek timeout workflow snapshot ve her koşulda failure artifact yükleme garantisi yok. Sonraki somut iş: dar consumer CLI adaptörü + stdout/stderr tanı rollerini snapshot/preflight'a bağla; opt-in workflow adımlarında ölçülen sonuçla manifest/artifact üret, artifact sonrasında orijinal nonzero sonucu geri ver. Sabit exit-code 0'dan timeout kabulü türetme.
- K2/K3 ortak harici input, legacy v1 artifact/provenance, 75 aday ölçümü, cihaz ve bağımsız restore kanıtları açık. Tam kabuller 0/92, 0/26, 0/22. Korunan kanal/EPG/YEDEKLER/YENİLER/FAVORİLER, eski repo ve PR #71 değişmedi; merge/Actions yok.

## 22 Ekim 2026 — Bash failure exit yerel 3/3 senaryo
- Yeni unittest: tests/test_parity_workflow_integration.py, commit e6d6322a49d50dec6edca9133dfaf7bcce27ac89 (önceki taslak 917ab692 sözdizimi hatası aynı dosyada düzeltilmiştir).
- Yerel Python subprocess ile Bash shell-fixture 3/3 geçti: consumer=23 snapshot=0 -> exit 23; consumer=23 snapshot=31 -> exit 23; consumer=124 snapshot=31 -> exit 124. Bu test yalnız shell exit propagation semantiğidir; gerçek workflow/CLI timeout testi değildir. Tam repo 610+ unittest bu commit için çalıştırılmadı; yerel GitHub DNS engeli sürüyor.
- Sonraki iş: gerçek timeout flag'i ve consumer failure çıktı kanıtını test et; full offline suite erişilebilir checkout üzerinde çalıştır. GitHub Actions tetiklenmedi. Tam kabuller 0/92, 0/26, 0/22.

## 22 Ekim 2026 — GNU timeout kontrollü yerel doğrulama
- tests/test_parity_workflow_integration.py içinde GNU timeout gerçek kesme regresyonu eklendi: cc875429213ab2f1dcf255f5fbe0c7361a56a4d0. Yerelde `timeout 0.1s bash -c 'sleep 2'` gerçekten çalıştırıldı, snapshot komutu exit 31 verdiğinde son exit 124 olarak korundu. Önceki 23/0, 23/31, 124/31 yerel shell kontrolleri de 3/3 tekrar çalıştırıldı.
- SINIR: Bu sadece Bash/GNU timeout kontrolü; GitHub Actions job timeout-minutes tarafından kesilme halinde snapshot üretimi doğrulanmadı. Repo genel 610+ regresyonu bu committe çalıştırılmadı; git ls-remote GitHub DNS çözemedi. Eski 92 davranış kabulü 0/92, güvenlik 0/26, görev 0/22. Actions tetiklenmedi. Sıradaki iş: gerçek workflow timeout davranışı ve güvenli offline suite.

## 22 Ekim 2026 — Başarısız tüketici snapshot artifact kalıcılığı
- K1 b9f713453b14e35d27197b06f2de66494fb48534; K4 b3e899b41d4ff9e6094f5dd88557a5d93329c151; K5/K2 879fea336ca8e2b307a7e3fb734b40ea07282376. failure() && !cancelled() && allow_parity_evidence=true koşullu ayrı upload-artifact@v4 adımları eklendi; hata sırasında oluşan reports/madsc-parity-snapshot.json saklanabilir. if-no-files-found: ignore; çıktı/snapshot yoksa kabul veya sahte kanıt üretilmez.
- Test kontratı 5d4301c801b7a85ab0aae561ba75bd7b8f52fc9a: her üç workflow için ayrı failure artifact adı, opt-in ve failure koşulu, path, upload, fail-closed olmayan opsiyonel yükleme sırası. Yeni testler ve Actions bu turda ÇALIŞTIRILMADI. Önceki 610 test bunları kapsamaz. Gerçek GitHub job timeout kesilmesinde snapshot garantisi yok. Tam kabuller 0/92, 0/26, 0/22. Korunan içeriklere dokunulmadı.

## 22 Ekim 2026 — K1/K4/K5 kontrollü timeout ve failure kanıt zinciri
- Son kod commit SHA: e10fcdc4c878305ca44e110b29ad88128cf16cb2. Başlangıç main c1fe77e309eaa6332c54add4d858058c7ee993de; eşzamanlı failure artifact adımı ve GNU timeout regresyon testi korundu/geliştirildi. Bu not commit'inin kendi SHA'sı GitHub geçmişindedir.
- Yeni madsc.parity_consumer_cli yalnız üç sabit izole tüketiciyi shell kullanmadan çalıştırır. Varsayılan workflow opt-in false; açıkken ölçülen çıkış kodu, gerçek timeout flag'i, stdout/stderr ve outcome JSON kaydedilir. Normal çocuk exit124 timeout sayılmaz. Kontrollü üst sınır 120 saniye, job sınırı 10 dakika. Normal çıktı oluşmadan hata veren K5 için de tanı snapshot'ı var; eksik normal rapor uydurulmaz.
- Tüketici nonzero adımı başarısız kalır; continue-on-error yok. Mevcut failed-consumer-snapshot artifact adı korundu, ham stdout/stderr ve outcome eklenerek consumer failure koşuluna daraltıldı. always/!cancelled kanıt zinciri ön hash kontrolü -> manifest -> son hash kontrolü -> upload sırasını önceki adımın success sonucuna bağlar. Hash değişiminde manifest yayınlanmaz; ayrı tanı artifact'i saklanabilir. Normal başarı yolu mevcut dosya snapshot'ını kullanır.
- Failure static preflight yalnız üç tanı rolünün tamamı ve ölçülen tüketici kaynak kontratı varsa ilerler; başarı rolüyle hata kanıtı ikame edilemez. Bu hâlâ statik kontrol: tanı artifact baytlarının GitHub kökeni/indirme/hash doğrulaması bu pakette tamamlanmadı; tam davranışsal kabul yok.
- Process observer timeout sonrası pipe EOF bekleyişi readiness + sınırlı cleanup deadline ile düzeltildi; alt süreç sinyalinin asenkron teslimi eksik kanıt veya sınırsız beklemeye dönüşmemeli. Çıktı taşması, spawn/preflight/writer hatası tamamlanmış ölçüm diye sunulmaz.
- Gerçek yerel testler: üç workflow shell gövdesinde timeout -> exit124/timed_out=true -> manifest -> statik preflight; K1 gerçek stderr ardından timeout; normal exit124/timed_out=false; K1/K5 gerçek nonzero ve K5 normal çıktı yokluğu; failure manifest öncesi/sonrası input mutasyonu; mevcut hedefte süreç başlatmama; writer hatasında consumer exit korunumu; eksik tanı rolü reddi. Mevcut başarı/opt-out/üç input mutasyon regresyonları da geçti.
- Nihai python -m madsc.offline_gate: 632 test ve beş izole K1–K5 kapısı success; 92+7 kaynak, 10 yardımcı komut, 22 görev envanteri geçti. Üç YAML parse ve job içi step id tekilliği geçti; git diff --check temiz. Bu pakette başarısız test yok; önce 629, sonra mutation testiyle 630, eşzamanlı iki test korununca 632. Önceki 621/7-failure kaydı tarihsel olarak korunur. Kanıt docs/PARITY_CONTROLLED_TIMEOUT_KANIT_2026-10-22.json, test edilen kaynak SHA256'ları içerir.
- Sınırlar: Actions dispatch/rerun, canlı probing, cihaz testi veya eski repo çalıştırması yapılmadı. GitHub koşullarının gerçek runtime sonucu yok. Sert job timeout, iptal veya runner kaybında upload garantisi verilemez. Girdi endpoint hashleri atomik freeze kanıtı değildir. Tam kabul 0/92, 0/26, 0/22.
- Sonraki somut yerel iş: failure snapshot'ındaki process_stdout/process_stderr/process_outcome hashlerini gerçek diagnostic artifact üyeleriyle doğrulayan bounded ZIP/receipt kontrolünü mevcut provenance artifact/API zincirine bağla. Outcome JSON exit_code/timed_out ile manifesti eşleştir; missing/mutated/duplicate/symlink/oversize üyeyi reddet; yalnız manifest JSON'u eşleşti diye tanı baytları doğrulandı deme. Ardından eski/yeni aynı input ve ayrı GitHub execution/artifact çiftleri hâlâ dış kanıt bekler.
- Korunan kanal listeleri, EPG, YEDEKLER, YENİLER, FAVORİLER, cihaz favorileri, logo/arşivler değişmedi. Eski repo salt okunur, merge ve PR #71 merge yok. Sonraki tur güncel main ve bu kayıttan devam etmeli; tamamlanan timeout adaptörünü yeniden kurmamalı.


## 22 Ekim 2026 — Failure diagnostic artifact regresyon testi (yeni sohbet)
- Test commit: 21b82e923c9e644c7d6299175dde937731c14414; tests/test_failure_diagnostic_artifact_regression.py eklendi. Mevcut madsc/legacy_pair_artifact.py ve github_legacy_pair_client.py içinde tanı ZIP baytı + API köken doğrulayıcıları main üzerinde bulundu; tekrar yazılmadı.
- Yeni test vakaları: failure exit23, measured timeout exit124, missing/duplicate/mutated ZIP üyesi, outcome exit uyuşmazlığı, ayrı artifact ID zorunluluğu, symlink ve oversized entry reddi. Bu testlerin başarıyla çalıştığı iddia edilmez.
- Bu tur yerel git ls-remote https://github.com/Madsc55/Madsc55-Tv.git HEAD komutu DNS nedeniyle başarısız: Could not resolve host: github.com. Bu yüzden tam repo checkout, yeni unittest ve python -m madsc.offline_gate ÇALIŞTIRILAMADI. Önceki 632 test sonucu yeni commit'i kapsamaz. GitHub Actions tetiklenmedi.
- Sonraki ilk iş: erişilebilir checkout üzerinde python -m unittest tests.test_failure_diagnostic_artifact_regression -v ve python -m madsc.offline_gate; varsa hataları düzelt, sonra bağımsız diagnostic artifact API origin/digest entegrasyonunu uçtan uca test et. ZIP ve outcome gerçek artifact kökeni olmadan kabul verme.
- Tam kabul 0/92, 0/26, 0/22; korunan yayın/EPG/YEDEKLER/YENİLER/FAVORİLER/logolar/arşivlere yazma, eski repo ve PR #71 merge yasağı geçerli. Eşzamanlı sohbetlerde yeni main HEAD kontrolü zorunlu.

## 22 Ekim 2026 — Paralel sohbet çakışma denetimi ve tanı API regresyonu
- main HEAD okunarak çalışıldı; önceki diagnostic ZIP/API doğrulayıcıları ve testleri tekrar yazılmadı. Ayrı tests/test_failure_diagnostic_api_fail_closed.py eklendi: commit 2aa79162627663cb8b11c7efbaba2765a47dfc34. Dört negatif senaryo: API run_attempt, artifact workflow_run.id, artifact workflow_run.head_sha ve artifact digest uyuşmazlığı ValueError ile reddedilmeli.
- Bu yeni test henüz ÇALIŞTIRILMADI; mevcut 632 test kanıtına eklenemez. GitHub Actions izinsiz tetiklenmedi. Başka sohbet main üzerinde eşzamanlı çalışıyor: her sonraki işlem öncesi HEAD ve dosya SHA yeniden okunmalı, var olan çalışma ezilmemeli. Kabul 0/92, 0/26, 0/22.


## 22 Ekim 2026 — Diagnostic outcome strictness regresyonu
- Yeni test commit 71ba4aeb3e79456855ac8392b09ee9fe3740f0d3; tests/test_diagnostic_outcome_strictness.py içinde duplicate JSON key, timeout conclusion/measurement mismatch ve yanlış consumer identity için üç fail-closed senaryo eklendi. Mevcut diagnostic ZIP/API testleri tekrar yazılmadı.
- Yerel GitHub git ls-remote hâlâ DNS 'Could not resolve host: github.com' verdi. Yeni testler ve tam offline_gate ÇALIŞTIRILMADI; 632 önceki test bu commit'i kapsamaz. GitHub Actions/üretim tetiklenmedi.
- Sonraki iş: erişilebilir checkout üzerinde python -m unittest tests.test_diagnostic_outcome_strictness -v ve python -m madsc.offline_gate; başarısızlıkları düzelt, gerçek diagnostic artifact API/byte doğrulamasını bağımsız execution kanıtıyla sınamaya devam et. Kabul 0/92, 0/26, 0/22; tüm korumalar geçerli. Paralel sohbet için her yazmadan önce main/dosya SHA yeniden okunmalı.

## 22 Ekim 2026 — Paralel çalışma: diagnostic API run-state regresyonu
- Kendi tests/test_failure_diagnostic_api_fail_closed.py dosyasına dört yeni fail-closed API negatif senaryo eklendi: e34b9481c888173f7b943c4ff05f959040bfdef5. total_count uyuşmazlığı, run.status in_progress, run.conclusion success ve run.repository.full_name uyuşmazlığı. Önceki sekizle toplam 12 negatif alt senaryo tanımlı.
- Testler henüz çalıştırılmadı; `git ls-remote` GitHub DNS çözümleme hatası verdi. 632 test önceki kaynak sürümüne aittir. Başka sohbetin güncel kodu yeniden yazılmadı; sonraki turda HEAD ve dosya SHA yeniden doğrulanmalı. GitHub Actions tetiklenmedi. Kabul 0/92, 0/26, 0/22.
