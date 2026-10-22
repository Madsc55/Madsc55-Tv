# Madsc55-Tv — DEVAM NOTU

> Son doğrulama: 22 Ekim 2026, kod/test SHA `61bbf78214a63400083cf7d615c64a1b13547896`; 800/800 offline test + beş kapı, kurulum, rapor round-trip ve statik sözleşme kapısı başarılı. Ayrıntı en sondaki kayıt ve `K1_K4_K5_PENDING_VALIDATION_2026-10-22.json`. Gerçek kabul 0/92, 0/26, 0/22.

**Son paket:** 776 test ve bütün offline kapılar geçti. Mevcut toplu CLI'ye açık opt-in API+ZIP bayt doğrulaması bağlandı; gerçek GitHub sorgusunda güncel aynı-input çift bulunmadı. 0/92, 0/26, 0/22 korunur. Ayrıntı son kayıtta.


**Son paket:** 769 test ve bütün offline kapılar geçti; 11 statik sözleşme farkı 0'a indirildi. Ana K2 geçmiş kaynak paketi/tüketim bağlantısı yerelde doğrulandı. Gerçek 92/26/22 kabulü açık; ayrıntı son kayıtta.


**Son birleşik doğrulama:** 764 test + beş izole kapı + kurulum + beş rapor/K5 başarılı. İki süre farkı giderildi; dokuz artifact adı farkı incelemeye açık. Ayrıntı en sondaki operasyon sözleşmesi kaydında.


**En güncel doğrulanmış paket (22 Ekim 2026):** Kod/test/kanıt SHA `e4f68c0b6bf597da1ab21c5ebd8c9480d5b85991`; güncel main üzerinde **760/760 yerel test**, beş izole K kapısı, kurulum envanteri ve beş rapor/K5 round-trip başarılı. Ayrıntı en alttaki kayıtta. Tam kabuller değişmedi: 0/92, 0/26, 0/22.

**En yeni kayıt:** Yeni sohbet devri tamamlandı: SOHBET_DEVIR_2026-10-22_SON.md. Son doğrulanmış paket 757 test+5 kapı+5 rapor/K5; sonraki 3c228e7 modülü henüz test edilmedi. Önce son devir kaydını oku.

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
Son geliştirme commit SHA: bd641a057d9ff47a2daeeddbef7eab742779db93
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

## 22 Ekim 2026 — Birikmiş diagnostic ve 92-kapsam kodunun gerçek toplu doğrulaması
- Son kod/test commit SHA: bd641a057d9ff47a2daeeddbef7eab742779db93; taban da6700fc31b8378a19363cba7477b6a49f2a248f. Önceki turlarda checkout/DNS engeli nedeniyle çalıştırılmamış diagnostic ZIP, API origin ve pinned 92-scope sertleştirmeleri güncel `main` checkout'unda birlikte sınandı.
- İlk odak çalıştırmada 48 testten event alt senaryosu başarısız oldu: fixture `workflow_dispatch` değerini zaten aynı olan beyan edilmiş event üzerine yazıyordu. Gerçek uyuşmazlık üretmesi için `schedule` kullanıldı; doğrulayıcı değiştirilmedi. Aynı odak kümesi finalde 48/48 geçti.
- Nihai `python -m madsc.offline_gate`: 658/658 test ve beş izole K1–K5 kapısı success; 92+7 kaynak, 10 yardımcı komut ve 22 görev envanteri geçti. `git diff --check` temiz. Kanıt `docs/OFFLINE_REGRESSION_KANIT_658_2026-10-22.json`.
- Bu testler gerçek Actions koşusu değildir. Yeni/current-code diagnostic artifact yok; legacy 92 tarafında aynı-input v1 artifact ve bağımsız replacement execution çifti yok. Kabul 0/92, 0/26, 0/22 kaldı. Actions/live probe/production write/eski repo yazısı yapılmadı.
- Statik incelemede yedi eski workflow'un `CALISANLAR.m3u` yazıp tüm M3U/M3U8'i reddeden protected-write gate'i çağırdığı çelişki doğrulandı. K1 gevşetilmedi; korunan listeye yazılmadı. Bu yollar üretim eşdeğeri sayılamaz ve kullanıcı onayı + ayrı yayın tasarımı olmadan düzeltilemez.
- Sıradaki güvenli yerel iş: gerçek dış kanıt gerektirmeyen 92 kaynak davranış eşleme kayıtlarını, pinned source commit/blob kimliklerinden başlayarak aynı-input pair hazırlık raporunda fail-closed eksik kanıt durumlarına bağla. Gerçek run/artifact oluşmadan kabul üretme; korunan playlist yayın tasarımını yetkisiz uygulama.

## 22 Ekim 2026 — Yanlış depodaki düzeltmelerin Madsc55-Tv karşılıklarına aktarımı
- Kullanıcının düzeltmesi üzerine tek hedef Madsc55/Madsc55-Tv/main olarak yeniden doğrulandı. Önceki sohbette eski depoya yapılan commit/testler yeni sistemin ilerlemesi değildi; bu kayıt o hatayı gizlemez. Bu aktarım turunda eski depoya yazılmadı, eski workflowlar kopyalanmadı, hiçbir Actions tetiklenmedi.
- Başlangıç bd641a057d9ff47a2daeeddbef7eab742779db93 üzerinde mevcut 658 test ve beş izole kapı geçti. Diğer sohbetin yalnız notları değiştiren 644ec08a4d3ef28414b3014813b0652164b68c8d commit'i korundu; aktarım bu güncel tabana uygulandı.
- K1: FAVORILER/favorites/HEPSI metadata kök adları ortak audit/enforcement kapısına eklendi; src manifest kapısı aynı politikayı kullanır. allowed_root korunan üst dizin adını gizleyemez. Yeni dosya yazılmadan ret ve eski bayt korunumu sınandı. Nested EPG/logo/arşiv koruması zaten mevcuttu, tekrar kurulmadı; yeni regresyonlarla doğrulandı. K1 izole kapısı metadata/logo reddini de gerçekten çağırır.
- K5: mevcut retry_decision politikasına assess_failure_history bağlandı. En çok 10 sağlanan sayfa, gerçek integer kimlik/total, tekil kayıt, mevcut koşu/dal/tarih ve eski koşu sırası kontrol edilir. Yetersiz geçmiş sıfır hata sayılmaz; ikinci sayfadaki hatalar durdurur, sonraki koşular eski rerun'a yüklenmez. Yeni sistemin varsayılan üç hata eşiği korunur. Otomatik API fetch/scheduler kurulmadı; bu offline değerlendirici kimlik doğrulanmış production geçmişi kanıtı değildir. K5 izole kapısı 100 aktif koşu arkasındaki üç başarısızlığı iki sayfadan gerçekten değerlendirir.
- Mevcut legacy_99_bulk_audit, SHA'sı doğrulanmış her kaynak satırına job/step/line/if/reusable/gate-order bağlamı ekler. madsc/legacy_workflow_safety saf/offline işlevdir. Başka job'daki/sonraki/continue-on-error gate önceki yazmaya yetki sayılmaz; echo/test/GET metni ayrılır. K5 kapısına çapraz-job yanlış kabul regresyonu bağlandı. Gerçek 99 kaynak ağdan yeniden çalıştırılmadı; eski 24/18/6 sayıları yeni pinned kaynak sonucu diye kullanılmadı.
- Git diff/push yazıcısı yeni runtime'da olmadığı için eski Git referansı çözüm kodu ve eski Actions testleri bağımsız kopya olarak eklenmedi; uygulanabilir davranış mevcut yeni kapılara uyarlandı. Eski başarı artifact'leri yeni kanıt gibi gösterilmedi. Ayrıntılı kaynak-commit/yeni-dosya eşlemesi ve SHA256: docs/TRANSFER_K1_K5_KANIT_2026-10-22.json.
- Nihai toplu offline doğrulama: 670 test + beş izole K1–K5 kapısı başarılı; 92+7 kaynak, 10 yardımcı komut, 22 görev envanteri geçti. Git diff --check temiz. Başarısız test yok. Bu kod, test ve kanıt bu kaydın bulunduğu tek [skip ci] commitinde saklanır; commit SHA dosya geçmişinden ve son kullanıcı raporundan doğrulanabilir.
- Tam kabul 0/92, 0/26, 0/22 değişmedi. Workflow/cron/izinler, canlı kanal/EPG/yedek/yeni/favori/logo/arşiv dosyaları değiştirilmedi. Sonraki iş diğer sohbetin pinned aynı-input pair hazırlık işini ezmeden sürdürülmeli; history API kökeni ve gerçek eski/yeni bağımsız run/artifact kanıtı hâlâ eksik. Bu paket tüm eski düzeltmelerin aynen kopyalandığı veya üretime kurulduğu iddiası değildir.

## 22 Ekim 2026 — Sohbet devri: diagnostic outcome tür koruması
- Kanonik hedef yalnız `Madsc55/Madsc55-Tv` main; `Madsc55/madsc-tv` eski kaynak ve salt okunur. Paralel sohbetin K1–K5 ilerlemesini veya korunan üretim içeriklerini ezme. Her yeni işlemde HEAD ve blob SHA kontrol et.
- `madsc/legacy_pair_artifact.py` outcome `exit_code` için `type(...) is int`, `timed_out` için `type(...) is bool` kesin kontrolü eklendi: commit `ed345b90af6db0d7175286db1227608463d363d5`. JSON bool/int eşitlik karışıklığını reddeder.
- `tests/test_diagnostic_outcome_type_confusion.py` iki regresyon testi eklendi: commit `28b1f0852a8e0c3f8e2e1c92580b0d5b3a598b4e`. Bunlar henüz gerçek depo modülleriyle çalıştırılmadı.
- Bu sohbet içinde aynı kontrol mantığının izole kopyası üzerinde 4 unittest (geçerli failure, bool exit_code, integer timed_out, float exit_code) çalıştırıldı: 4/4 geçti. Bu sonuç depo testi veya full offline_gate kanıtı değildir.
- Bu devirden hemen önce HEAD `0bd40de657410a309949626f4f4dfcd61bfd3222` görüldü; diğer sohbet yeni K1–K5 transfer paketi ve 670 test + 5 offline kapı sonucunu not etmiş. Bu sonuç yalnız notta belirtilen kendi kaynak sürümüne aittir, bizim iki yeni commitin tamamını kapsadığı ayrıca kontrol edilmeli.
- Sonraki iş: güncel HEAD'de `python -m unittest tests.test_diagnostic_outcome_type_confusion tests.test_diagnostic_outcome_strictness tests.test_failure_diagnostic_api_fail_closed -v` ve `python -m madsc.offline_gate` çalıştır; gerçek sonuçları kaydet. Bağımsız legacy/replacement run-artifact aynı input kabul kanıtlarını üretmeden kabul artırma. Tam kabul 0/92, 0/26, 0/22.
- Actions dispatch/rerun, canlı probing, cihaz testi, merge ve PR #71 merge izinsiz yapılmaz. Korunan yayın/EPG/YEDEKLER/YENİLER/FAVORİLER/logo/arşivlere dokunma. Commitlerde [skip ci] kullan.

## 22 Ekim 2026 — 92 davranış için kaynak kimlikli pair hazırlığı
- Tek hedef Madsc55/Madsc55-Tv/main. a37086e tabanında başlayan paket, diğer sohbetin 28b1f08 ve 27ea4c81dcb8fee19ae28489c6dcf3e4100a3562 commitlerindeki diagnostic düzeltme/test/notları korunarak güncel main üzerine uygulandı. Önceki yayın denemesi main ilerlediğinde dalı değiştirmedi; yeni HEAD üzerine kaydedildi.
- Mevcut compare_provenance_bound_batch ve legacy_parity_cli genişletildi; yeni workflow/yazıcı/CLI yok. 92 satırda pinned eski repo/dal/commit/tree/workflow/blob/boyut, gözden geçirilecek beş merkezi replacement seçeneği, varsa aynı-input SHA256 ve altı bağımsız eksik kanıt alanı var. Yedi kapsam dışı workflow eklenmez; eksik çiftin input hash'i null kalır. Gerçek run/artifact uydurulmaz.
- 99 kaynak yol/blob/boyut digest'i sıralamadan bağımsız sabitlendi; pinned tree ve scope-script SHA da kontrol edilir. Biçimi geçerli fakat değiştirilmiş blob/boyut/yol/tree/script kimliği karşılaştırmadan önce reddedilir. Bu offline kaynak katalog bağıdır; API kökeni veya canlı yürütme doğrulaması değildir.
- Mevcut CLI ile docs/PARITY_PAIR_PREPARATION_2026-10-22.json üretildi: 92 kaynak kimliği bağlı hazırlık satırı, 92 eksik gerçek pair, sıfır kabul. Eşleşen fixture metadata'sında dahi API kökeni/artifact baytları/yan etki/gözden geçirme açık kalır. K5 izole kapısı bu 92-satır sözleşmesini gerçekten çağırır.
- İlk toplu denemede yeni test dosyasındaki kullanılmayan yanlış sınıf import'u 1 keşif hatası verdi (671 keşif kaydı); import kaldırıldı. Sonraki 675 ve 677 yerel testler geçti. Main yeniden ilerlediği için son dört eşzamanlı test de korunup nihai toplu python -m madsc.offline_gate çalıştırıldı: **679 test + beş izole K1–K5 kapısı success**; 92+7 kaynak, 10 yardımcı komut, 22 görev envanteri geçti. git diff --check temiz. Kanıt docs/PARITY_PAIR_PREPARATION_KANIT_2026-10-22.json; kaynak ve üretilen rapor SHA256'ları kayıtlı.
- Kod/test/rapor/notlar aynı [skip ci] commitinde; kendi SHA'sı dosya geçmişindedir. Actions/rerun/live probing, üretim dosyası, workflow/cron/izin, eski repo yazısı veya merge yok. Kabul **0/92, 0/26, 0/22** korunur.
- Sonraki iş 92 satırın replacement davranış eşlemelerini mevcut uygulanmış komut ve input/output role sözleşmelerine bağlamak; beş seçenekten otomatik onaylı eşleme türetmemek. Gerçek bağımsız eski/yeni aynı-input run/artifact ve yan etki kanıtları dış bağımlılık olarak açık.

## 22 Ekim 2026 — 92 hazırlık kaydı yeni workflow sözleşmelerine bağlandı
- Tek hedef Madsc55/Madsc55-Tv/main; taban **52117ac42f268ade64e48490edac8c6a0e624657**. compare_provenance_bound_batch mevcut replacement_workflow_root argümanı verilince güncel beş YAML'ı mevcut audit_parity_workflow_readiness ile okuyup karşılaştırma raporuna replacement_contract_catalog ekler. Kaynak dizin verilmezse checked=false ve catalog=null; eski çağrı uyumluluğu korunur.
- 92 satırdaki kaynak-kimlikli pair hazırlığı bu kataloğa açık checked referansıyla bağlanır. Üç izole tüketici/girdi/çıktı rolü (K1 guard, K4 restore, K5 içindeki K2 artifact üreticisi) ve iki harici/canlı input engeli (K2/K3) gerçek mevcut source hashleriyle raporlanır. Bu, 92 davranışın seçilmiş/onaylanmış yeni eşlemesi değildir: replacement_mapping_review_required her satırda true kalır. K1/K4/K5 sözleşmesini sırf ad eşleşmesiyle tüm eski işlere uygulama.
- K5 izole kapısı aynı rapor zincirini beş kaynak üzerinden çağırır. Kaynak dosya değişirse fresh blob/hash ve eksik rol durumu yenilenir; cached readiness dosyası onay olarak kullanılmaz. Eksik kaynak mevcut CLI output yazmadan reddedilir. Yeni workflow veya yazıcı eklenmedi; üretim kapıları gevşetilmedi.
- Dört yeni offline regresyon: argümansız kontrol yapıldı iddiasının reddi; beş gerçek source/3 izole+2 harici contract; değişen source blob ve kaybolan binding; eksik source halinde çıktı olmaması. Toplu python -m madsc.offline_gate **683 test ve beş izole K1–K5 success**; 92+7 kaynak, 10 yardımcı komut, 22 görev envanteri geçti. Başarısız test yok; git diff --check temiz.
- Mevcut legacy_parity_cli.run ile ağsız/boş gerçek-pair girdisi üzerinde rapor üretildi. docs/PAIR_REPLACEMENT_CONTRACT_KANIT_2026-10-22.json beş güncel sözleşmeyi, 92 checked referansı, CLI rapor SHA256'sını ve test edilen source hashlerini içerir. Gerçek execution/artifact uydurulmadı; 92 pair hâlâ eksik.
- Kod/test/kanıt/notlar aynı [skip ci] commitinde; kendi SHA'sı Git geçmişindedir. Actions/rerun/live probe, korunan kanal/EPG/yedek/favori/logo/arşiv, workflow/cron/izin, eski repo veya merge işlemi yok. Kabul 0/92, 0/26, 0/22 korunur.
- Sonraki somut iş: bağımsız pair verisi geldiğinde seçilen replacement tüketici ve input/output role sözleşmesinin eski davranışa gerçekten karşılık geldiğini kaynak-bağlı mapping kaydıyla doğrulamak; metadata match'i davranışsal kabul saymamak. K2/K3 ortak harici input, legacy v1 manifest/artifact ve bağımsız origin/bayt/yan etki kanıtları dış bağımlılık olarak açık.

## 22 Ekim 2026 — Seçilen davranış eşlemesi mevcut karşılaştırıcıya bağlandı
- Tek hedef Madsc55/Madsc55-Tv/main. Diğer sohbetin kaynak eşleme inceleyicisi ve sekiz testi korunarak 65109d7 tabanına uygulandı. Mevcut batch/CLI isteğe bağlı behavior_mappings alır; pinned legacy blob, güncel replacement blob, tüketici komutu ve input/output rolü birebir doğrulanır. Eksik kaynak, harici-input sözleşmesi, yanlış hedef ve ek approved alanı reddedilir; hatalı CLI girdisinde rapor yazılmaz.
- Bildirim gerçek eşleme incelemesi değildir. replacement_mapping_review_required=true kalır; gerçek incelenmiş eşleme ve doğrulanmış legacy pair sayısı sıfırdır. Fixture seçimi gerçek 92 davranışa otomatik atanmadı. Bağımsız yürütme/API/artifact baytları/yan etki kanıtı hâlâ gerekir.
- Yedi yeni regresyonla birleşik python -m madsc.offline_gate: **698 test + beş izole K1–K5 kapısı başarılı**; 92+7 kaynak, 10 yardımcı komut ve 22 görev envanteri geçti. git diff --check temiz. Kanıt docs/BEHAVIOR_MAPPING_BINDING_KANIT_2026-10-22.json. Kod/test/kanıt/notlar aynı [skip ci] commitinde; SHA dosya geçmişindedir.
- Actions, canlı test, üretim dosyası, eski repo, workflow/cron/izin veya PR değişikliği yok. Kabul 0/92, 0/26, 0/22 korunur. Sonraki iş bağımsız kaynak gerekçeli eşleme incelemesini mevcut pair zincirine taşımak; aynı-input gerçek yürütme kanıtı eksikliğini kabul saymamak.

## 22 Ekim 2026 — Kullanıcının eski depodaki test ekranlarının yeni sistem karşılığı
- Kullanıcının paylaştığı ekranlardaki ebf7e25, d0ec63a, 28fe155, 1b4474d, ebb3550, 4bc7328 ve 17e9167 değişiklikleri mevcut aktarım kaydı ve yeni kod/testlerle karşılaştırıldı. Tek hedef Madsc55/Madsc55-Tv/main; eski depo değiştirilmedi. Eski kırmızı/yeşil run sonuçları yeni sisteme kanıt sayılmadı.
- Favori metadata/iç içe korunan yol K1 kapıları, K5 sayfalı eksik geçmiş reddi/current-run/rerun ayrımı ve job/step kaynak kapsamı mevcut yeni uygulamada doğrulandı. Bağımsız kategori kanıtının explicit true gereksinimi mevcut maintenance testiyle doğrulandı. Eski escaped-newline testi farklı workflow metnine körlemesine kopyalanmadı. Yeni runtime'da Git diff/push yayıncısı olmadığı için baseline seçenek enjeksiyonu düzeltmesi uygulanabilir bir üretim yolu olarak gösterilmedi.
- 0962bc188f712948a03971d012a7d7ad3b381742 üzerinde güncel yerel doğrulama: **698 test + beş izole K1–K5 kapısı başarılı**. Ayrıntı, kaynak SHA256, K etki matrisi ve açık bağımlılıklar docs/SCREENSHOT_TEST_TRANSFER_AUDIT_2026-10-22.json içinde. Bu paket mevcut aktarımı ekrana göre doğrular; yeni işlev/test sayısı artışı değildir.
- Actions başlatılmadı; üretim/korunan veri/eski repo/workflow değişmedi. Authenticated hata geçmişinin üretimde zorunlu kılındığı veya ekranlardaki eski kırmızı Actions'ın düzeldiği iddia edilmez. Kabul 0/92, 0/26, 0/22. Sonraki iş yeni sistemde bağımsız gerçek yürütme ve kaynak gerekçeli davranış eşlemesi kanıtını tamamlamaktır.

## 22 Ekim 2026 — Gerekçeli eşleme incelemesi pair zincirine bağlandı
- Tek hedef Madsc55/Madsc55-Tv/main; taban bf56ac1826d9e0d43a9e9c218e3865865b580b8d. Diğer sohbetin mevcut review_replacement_mappings işlevi lazy import ile mevcut provenance batch/CLI zincirinde kullanılır. İsteğe bağlı mapping_review_rows kaynak blob, seçilen replacement ve input/output rolü açısından behavior_mappings ile birebir bağlanır; kopuk veya kaynaksız inceleme rapor yazılmadan reddedilir. Yeni CLI/workflow/yazıcı yok.
- İnceleme gerekçesi ilgili pair_preparation satırına taşınır; supplied aday sayısı ayrı raporlanır. Bunlar bağımsız onay değildir: review_required=true, independently_reviewed=0, behavioral acceptance=0 kalır. Fixture eşlemesi gerçek legacy davranış incelemesi gibi kaydedilmedi.
- Dört yeni bütünleşik regresyon: gerekçenin aynı satıra taşınması, yanlış kaynak/rol/ek approved/duplicate/kaynaksız bildirim reddi, boş ve hiç verilmemiş inceleme ayrımı, mevcut CLI'nin hatalı incelemede çıktı yazmaması. python -m madsc.offline_gate: **702 test + beş izole K1–K5 kapısı başarılı**; 92+7 kaynak/10 yardımcı komut/22 görev envanteri geçti. git diff --check temiz. Kanıt docs/MAPPING_REVIEW_CHAIN_KANIT_2026-10-22.json.
- K1 çıktı koruması değişmedi; K2/K3 canlı input ve K4 yedek/restore yolu değişmedi; K5 karşılaştırma raporu genişledi. Actions, production, eski repo, workflow/cron/izin, PR değişmedi. Kod/test/kanıt/notlar aynı [skip ci] commitinde, SHA geçmiştedir. Kabul 0/92, 0/26, 0/22. Gerçek kaynak gerekçeli davranış incelemesi ve bağımsız aynı-input yürütme/API/artifact/yan etki kanıtları hâlâ açık; yeni sahte metadata ekleyerek kabul üretme.

## 22 Ekim 2026 — K5 sayfalı hata geçmişi sıra doğrulaması
- Tek hedef Madsc55/Madsc55-Tv/main, taban 37e52ab3647e9198e4ed2d207f47aaf81b87f59d. Eksik ve sırası bozuk supplied history eski success sınırını kullanarak RETRY_LATER verebiliyordu. Mevcut assess_failure_history artık filtrelemeden önce bütün aktif/tamamlanmış satırların timestamp/id sırasını sayfa içinde ve sayfalar arasında azalan olarak doğrular; bozuk aktif timestamp de reddedilir. Varsayılan üç hata eşiği ve sıralı prefix success sınırı politikası değişmedi.
- Beş regresyonun dördü düzeltme öncesi beklenen ValueError oluşmadığı için başarısızdı. Düzeltme sonrası toplu python -m madsc.offline_gate: **707 test + beş izole K1–K5 kapısı başarılı**; 92+7 kaynak, 10 yardımcı komut, 22 görev envanteri geçti. git diff --check temiz. Kanıt docs/FAILURE_HISTORY_ORDER_KANIT_2026-10-22.json.
- K5 retry kararı sıkılaştırıldı; K1 çıktı kapısı, K2/K3 keşif/kanal ve K4 yedek yolları değişmedi, beş izole kapı birlikte geçti. Actions/production/eski repo/workflow/cron/izin/PR değişikliği yok. Kod/test/kanıt/notlar aynı [skip ci] commitinde; SHA geçmiştedir. Sıra doğrulaması tek başına API kökenini veya atlanmış satır bulunmadığını kanıtlamaz; authenticated history ve gerçek bağımsız yürütme kanıtı hâlâ eksiktir. Kabul 0/92, 0/26, 0/22 korunur.

## 22 Ekim 2026 — replacement katalog bütünlüğü (MADSC55-TV)
- Yalnızca `Madsc55/Madsc55-Tv/main` değiştirildi; eski `madsc-tv` salt okunur kaynak olarak kaldı.
- `madsc/legacy_replacement_mapping_review.py` eksik veya tekrarlı K1–K5 kaynak kataloğunu fail-closed reddediyor; eşleme ancak beş merkezi workflow kaydı eksiksiz ve tekilse inceleniyor.
- `tests/test_legacy_replacement_mapping_review.py` fixture'ı beş merkezi workflow'u içeriyor; eksik/tekrarlı kayıt için iki regresyon testi eklendi.
- Commitler `cd2e667a63589a5f02e3d9d996fd6571b8a6772c`, `4943508c668a6e151070243e0596f1c00cd1584e`; ikisi de `[skip ci]`.
- Bu turda testler çalıştırılmadı; Actions `#482/#483` gerçek run ID/logları henüz bulunamadı. GitHub run numarası API run ID değildir. Üretim/EPG/playlist/yedek/favori/workflow/cron değiştirilmedi; gerçek kabul 0/92, 0/26, 0/22.

## 22 Ekim 2026 — mapping dosya bağları fail-closed
- `madsc/legacy_replacement_mapping_review.py` replacement `declared_file_binding` içindeki `input_path`, `output_label`, `output_path` değerlerini dolu string olarak doğrular; liste/boş değer kontrollü ValueError ile reddedilir.
- `tests/test_legacy_replacement_mapping_review.py` iki negatif regresyon senaryosu eklendi.
- Yeni `Madsc55/Madsc55-Tv/main` commitleri: `91e625b1fe1e0dd5c8a8c9e5aa14f326deb9ccc8`, `483c75c9374e258402f3ae28485d3ad01c5465e8` (`[skip ci]`). Testler bu turda çalıştırılmadı; Actions #482/#483 logları henüz doğrulanmadı. Üretim dosyaları, workflow'lar, eski repo değişmedi. Kabul 0/92, 0/26, 0/22.

## 22 Ekim 2026 — kontrollü süreç sözleşmesi mapping kapısı
- `madsc/legacy_replacement_mapping_review.py` statik adaylık için `controlled_process_contract_complete` alanını zorunlu kıldı; eksik alan fail-closed, false alan `mapping_contract_blocked`. Kaynak: `madsc/parity_workflow_readiness.py` güncel sözleşme satırları.
- `tests/test_legacy_replacement_mapping_review.py` beşli fixture'lara bu alanı ekledi, iki negatif regresyon testi oluşturuldu.
- Commitler `11e1f12a50ce91c412a2fb8d13db417f7753608c` ve `768150c2ed7d3af99f419001caa1d7d575d0c9c3` (`[skip ci]`). Bu turda CI ve offline test çalıştırılmadı. Üretim, Actions, eski depo değiştirilmedi. Kabul 0/92, 0/26, 0/22.

## 22 Ekim 2026 — K2/K3 harici kaynak mapping blokajı
- `madsc/legacy_replacement_mapping_review.py` K2 ve K3 için statik kaynak sözleşmesi alanları true olsa bile eşleme adayını `mapping_contract_blocked` tutar. Bu aşamaların harici/canlı girdileri bağımsız karşılaştırma olmadan kabul edilemez.
- `tests/test_legacy_replacement_mapping_review.py` K2 ve K3 için yanlışlıkla tüm flaglerin true olduğu negatif senaryoları ekledi.
- Yeni sistem commitleri `6e01ae808056e7ebac50d9ab95666bbe1d603fb3`, `2c6d680bbc39ee3e9d0467228670f8ddcf3c0f75` (`[skip ci]`). Bu turda testler yürütülmedi; Actions #482/#483 logları elde edilmedi. Üretim/EPG/yedek/favori/workflow/cron/legacy repo değiştirilmedi. Kabul 0/92, 0/26, 0/22.

## 22 Ekim 2026 — Beşli sistem toplu rapor üretimi ve K5 uçtan uca yerel kapısı
- Yalnız Madsc55/Madsc55-Tv/main; taban 2ea58e800156e3c99eb63f882f838045fc0714eb. Güncel diğer sohbet kodu korundu. Önceki yerel ortam kaybolduğu için yeni checkout alındı; geçmiş 707 testi güncel kodun kanıtı sayılmadı. Birleşik kaynakta ilk toplu test: 754 test, 1 failure/4 error. Eksik EXT M3U başlıklı üç test girdisi ve literal backslash-n içeren iki fixture düzeltildi. Preview testi mevcut büyük harfli ad sözleşmesiyle, virgüllü id/grup korunumu da doğrulanarak güncellendi. Üretim parser'ları gevşetilmedi.
- Mevcut offline_five_gate içine assess_report_roundtrip eklendi: gerçek core.run beş kategorinin raporlarını ayrı geçici artifact dizinlerine yazar; gerçek batch_acceptance.collect bunları K5 olarak okur; bütün dosya SHA256'ları tüketim öncesi/sonrası aynı olmalıdır. Mevcut offline_gate bu aşamayı artık zorunlu kılar; eksik/bozuk çıktı veya exception exit_code=5 ile yeşil unit test sonucunu engeller. Yeni workflow/zamanlayıcı/üretim yazıcısı yok.
- K1 korumalı rapor yazısı, K2 keşif ve geçmiş fixture'ı, K3 teknik/IBO/EPG fixture'ı, K4 izole restore ve K5 toplu tüketim aynı pakette yürütüldü. Üç yeni regresyon: gerçek beş rapor tüketimi ve byte korunumu; eksik üretici çıktısının reddi; başarılı unit testin bozuk roundtrip'i örtememesi. Geliştirme sırasında eksik dosya testinde yanlış exception beklentisi bir hata verdi; FileNotFoundError beklentisiyle düzeltildi.
- Nihai python -m madsc.offline_gate **757 test, beş izole K1–K5 kapısı, beş gerçek yerel rapor/K5 roundtrip ve 92+7/10 komut/22 görev envanteri başarılı**. git diff --check temiz. Kaynak hashleri, rapor hashleri, bütün görevlerin açık kanıt listesi ve yardımcı sözleşme farkları docs/FIVE_SYSTEM_BULK_VALIDATION_2026-10-22.json içinde.
- Tam bitmiş değildir: kurulumda 16 YAML vardır (beş ana + ekler); on yardımcı komut ana sisteme bağlıdır fakat 11 statik sözleşme farkı açık. 125 statik yazıcı çağrı adayı tümü runtime denetlendi sayılmaz. Defter 0 completed/7 in_progress/15 pending; kabul 0/92, 0/26, 0/22. Eski bağımsız aynı-input execution/artifact, canlı/zaman aralıklı K3, kullanıcının IBO cihaz testi, harici yedek/restore ve gerçek uçtan uca güvenlik kanıtları eksik. Gerçek kabul olmadan eski otomasyonları kapatma veya defteri completed yapma.
- Actions/merge/PR71/canlı probing/korunan IPTV-EPG-yedek-favori-logo-arşiv ve eski repo yazısı yapılmadı. Bu [skip ci] paketinin SHA'sı Git geçmişindedir. Sonraki iş rapordaki bağımsız dış kanıt engellerini ve 11 kaynak sözleşme farkını ana beşli sistem içinde çözmek; küçük fixture testlerini gerçek 92 davranış tamamlandı gibi sunmamak.

- Yayın sırasında diğer sohbetin yalnız docs/K1_K5_KURULUM_DURUMU_2026-10-22.md ekleyen a39cdfa commit'i geldi; içerik okundu ve korundu. Test edilen Python/test/workflow kaynakları değişmedi; dal eski HEAD üzerine zorlanmadı.


## 22 Ekim 2026 — Bu sohbetin son devri
Kullanıcı tüm ilerlemenin kaydedilip yeni sohbete geçilmesini istedi. Ayrıntılı toplu devir: SOHBET_DEVIR_2026-10-22_SON.md. Yanlış eski repo çalışması ve yeni sisteme aktarım, bütün ilgili commit/kanıt dosyaları, başarısız testler ve düzeltmeleri, 757 test+5 kapı+5 dosya/K5 doğrulaması, açık 11 sözleşme farkı ve 92/26/22 bağımsız kabul eksikleri kaydedildi. Bu devir hazırlanırken HEAD 3c228e7340b090ae4edf49d3d7b49382a4ef6d69; bu HEAD'in eklediği five_stage_installation modülü ve iki testi okundu ama çalıştırılmadı. İlk iş güncel HEAD'de bunları ve tam offline_gate'i doğrulamak. 757 testi sonraki kaynak sürümüne otomatik mal etme. Korunan veriler/eski repo/PR71/izinsiz Actions ve canlı test sınırları değişmedi; IBO testi kullanıcıda. Bu commit yalnız dokümandır, yeni test sonucu değildir.


## Eşzamanlı diğer devirle mutabakat
Devir yazılırken aeee8354c1e55f398c1f194650475d15769688bf yalnız YENI_SOHBET_DEVIR_2026-10-22.md ekledi; metin okundu ve korundu. O belgedeki 707 test bilgisi tarihsel kaldı: 1b30eee paketi 757 test+5 kapı+5 rapor/K5 ile doğrulandı, daha sonraki 3c228e7 dosyaları henüz sınanmadı. Diğer belgenin kullanıcı ekranından aktardığı K4 EPG/logo ve K5 arşiv/bakım hedefleri ile repo teknik K4 yedek/K5 bakım adlandırması arasındaki fark yeni sohbette açık görev eşlemesiyle uzlaştırılmalı; repo isimleri varsayımla değiştirilmemeli. Bu devir kaydı bütün önceki notları tamamlar.

## 22 Ekim 2026 — kurulum kapısı ve zamanlama regresyonu doğrulaması
- Son kod/test/kanıt commit SHA: `e4f68c0b6bf597da1ab21c5ebd8c9480d5b85991`; taban `554ec5f07a10dcf81041c1cc18a2081a04dc9e4c`. Eşzamanlı gelen `4fa9cf7` ve `554ec5f` kurulum-envanteri fail-closed testini ekledi/düzeltti; eski HEAD üzerine yazılmadı.
- Güncel kaynakta kurulum envanteri genel offline kapının zorunlu parçası olarak doğrulandı. Odaklı kurulum/offline/round-trip seti 14/14 geçti. Nihai `python -m madsc.offline_gate` sonucu 760/760 test, beş izole K1–K5 kapısı, kurulum envanteri, beş gerçek yerel rapor/K5 byte-koruyan round-trip ve 92+7/10 komut/22 görev envanteri başarılıdır.
- İlk tam koşu host yükü altında FIFO snapshot 2 saniye ve K1 workflow simülasyonu 10 saniye sınırında iki timeout verdi; ikisi izole tekrarında geçti. İkinci tam koşu, öldürülen alt süreç için PID numarasının yeniden kullanılmasını ayırt etmeyen `/proc` kontrolünde 1 saniyelik sınırı yaklaşık 10 ms aştı. Sadece bekleme süresini artıran ilk deneme yeterli olmadı.
- Nihai test düzeltmesi süreç kimliğini Linux `/proc/<pid>/stat` starttime alanına bağladı; yeniden kullanılan PID artık eski alt süreç sanılmıyor. Gerçek aynı süreç canlıysa test hâlâ kırmızı kalır. FIFO ve workflow simülasyonu test-harness zamanlama üst sınırları 5 ve 30 saniyeye çıkarıldı; üretim timeout/kill/fail-closed davranışı değiştirilmedi. Üç süreç-kapatma tekrarı ve iki ilgili sınır testi 5/5 geçti.
- Kanıt: `docs/FIVE_STAGE_INSTALLATION_GATE_KANIT_2026-10-22.json`. `git diff --check` temiz. GitHub Actions, canlı stream probing, cihaz testi, üretim yazma, eski depo yazısı, merge veya PR #71 işlemi yapılmadı; korunan veri değişmedi.
- Açık işler/engeller: gerçek 92 aynı-input çifti için bağımsız legacy ve replacement execution/artifact kökeni hâlâ yok; K2/K3 canlı/harici kaynaklar, IBO kullanıcı cihaz sonucu ve K4 bağımsız harici restore kanıtı eksik. Tam kabuller 0/92, 0/26, 0/22; fixture sonuçları bu sayaçları artırmaz.
- Sıradaki somut adım: `five_stage_installation` raporundaki 11 statik sözleşme farkını kaynak gerekçeleriyle gözden geçir; güvenle yerel çözülebilenleri beş ana workflow sözleşmesine taşı. Gerçek aynı-input/bağımsız run-artifact bulunmadan 92 davranış kabulü verme ve mevcut kanıt zincirini sahte metadata ile doldurma.


## 22 Ekim 2026 — Güncel kurulum ve operasyon sözleşmeleri topluca doğrulandı
- Tek hedef Madsc55/Madsc55-Tv/main; taban 554ec5f07a10dcf81041c1cc18a2081a04dc9e4c. Sonraki kurulum modülü/kapı değişiklikleri ilk kez bu turda gerçek yerel toplu testle kapsandı.
- İlk 760 test: 1 failure/1 error. K1 preflight alt süreç başlatması 5 saniyeyi aştı; ilgili 15 test kod gevşetilmeden 0.868 saniyede geçti. Süreç sonlandırma testi toplu koşuda tekrar başarısızdı (763 test/1 failure). Kapsayıcı getpid kimliklerinin host /proc dizininde ilgisiz sync_share.sh/sites-preview süreçlerine karşılık geldiği gerçek tanı çıktısıyla bulundu. Test artık çocukların /proc/self/stat PID ve başlangıç zamanını kullanır, iki ayrı sürecin gerçekten başladığını zorunlu doğrular; üretim süreç öldürme kodu gevşetilmedi.
- K5 25 dakika eski kaynak audit + 15 dakika not birleştirme opt-in adımlarının 10 dakika job limiti altında kalması düzeltildi: job 45, adımlar 25/15 dakika. Bu üst sınır süre tüketimi değildir; dispatch yapılmadı. Opt-in rapor upload artık failure durumunda da always() && !cancelled() ile denenir; kaynaklar/izinler/cron/korunan veri değişmedi.
- Sözleşme denetimi süreyi yalnız ilgili komutun bulunduğu job ile karşılaştırır; ilgisiz uzun job komutu maskeleyemez. Komut, süre, rapor yolu, actions izni veya failure-upload kaybı contract_gate ve mevcut offline_gate başarısını engeller. Artifact ad farkı ayrı inceleme olarak görünür; otomatik eşdeğerlik verilmez. Yeni kapı entegrasyon regresyonu dahil dört test eklendi. Önceki süre fixture'ı gerçek komutu içermediğinden düzeltildi; eksik komut süre uyumluluğu sayılmıyor.
- Nihai python -m madsc.offline_gate: 764 test, beş izole K1–K5 kapısı, kurulum envanteri, 92+7 kaynak/10 yardımcı komut/22 görev ve beş gerçek yerel raporun K5 tüketimi başarılı. git diff --check temiz. Kanıt, test edilen kaynak SHA256 ve rapor hashleri: docs/FIVE_STAGE_CONTRACT_VALIDATION_2026-10-22.json.
- 11 statik farktan iki süre farkı giderildi; dokuz artifact isim değişikliği inceleme olarak açık. Bunlar çalışma zamanı byte zinciri kabulü değildir. Davranış 0/92, runtime güvenlik 0/26, görev tam kabulü 0/22 korunur. Korunan listeler/EPG/favoriler/yedek/logo/arşiv, eski depo, PR71 ve merge işlemi yok. Actions başlatılmadı; kullanıcının ilettiği izin kotayı harcamak için gereksiz tekrar gerekçesi sayılmadı. IBO cihaz testi kullanıcıda.
- Sıradaki bağlantılı iş: dokuz yeniden adlandırılan artifact için gerçek üretici/tüketici dosya ve byte zinciri ile bağımsız aynı-input eski/yeni run/artifact kanıtını bağlamak; eksik dış kaynağı fixture ile tamamlanmış göstermemek. K2/K3 canlı ölçüm ve bağımsız geçmiş, K4 dış backup/restore, K1 26 runtime kuralı ve K5 gerçek uçtan uca kabul açık. Kod/kanıt/notlar aynı [skip ci] commitindedir; kendi SHA'sı Git geçmişindedir.

- Yayın öncesi main e4f68c0b6bf597da1ab21c5ebd8c9480d5b85991 commitine ilerledi: FIFO/receipt test süreleri ve bağımsız 760-test kanıtı okundu/korundu. Aynı process testinin starttime ve beş saniye bekleme düzeltmesi procfs PID kimliği ve iki süreç zorunluluğu ile uzlaştırıldı. Son toplu test bu birleşik kaynaklar üzerinde yeniden çalıştırıldı.


## 22 Ekim 2026 — Dokuz artifact sözleşmesi ve ana K2 geçmiş zinciri
- Tek hedef Madsc55/Madsc55-Tv/main, taban 60031b9bc46728b7773ad8037fe398b3c1d50814. Önceki test/kanıt/notlar korundu. Paket SHA Git geçmişindedir; kod/test/kanıt/devir tek [skip ci] commitinde.
- Dokuz artifact adı farkı yalnız rapordan gizlenmedi: eski yardımcıların upload-artifact adları, dosya yolları ve ZIP common-root yerleşimi ana K2/K3/K5 işlerine opt-in upload adımları olarak eklendi. Mevcut birleşik paketler korundu; yeni workflow/job/cron açılmadı, yardımcılar kapatılmadı. Paket isimleri artık contract_gate tarafından zorunlu; silinirse toplu offline kapı başarısız olur. Statik sözleşme farkı 9→0; bu çalışma zamanı eşdeğerlik kabulü değildir.
- Somut K2 kopukluğu: tüketici madsc-k2-history-source beklerken ana K2 yalnız madsc-k2-isolated-evidence üretiyordu. Ana K2 artık kaynak çiftini eski tüketicinin beklediği ad ve iki kök ZIP üyesiyle saklar. Kaynak üretimi allow_history_source_publish, bağımsız eski kaynağı doğrulama allow_verified_history ile ayrı default-false izinlerdir; kaynak üretmek için zorunlu olarak eski manifest doğrulatılmaz. Hassas komutların açık izin regresyonu bu yeni iki ayrı flag'i zorunlu denetler.
- history_verified_pipeline/CLI açık source_workflow_path/--source-workflow seçeneği alır; yalnız eski gerçek-kaynak yardımcı workflow'u veya ana K2 kabul edilir. Varsayılan eski kaynak uyumluluğunu korur. Seçim API run.path ile birebir doğrulanır; K5 fixture CI ve keyfi workflow, doğrulamadan önce reddedilir. Manifest şeması, token zorunluluğu, repo/dal/başarı/ancestor/artifact kökeni ve bayt hash denetimleri gevşetilmedi.
- Gerçek yerel zincir testi publish_source → iki dosyalı ZIP → gerçek provenance client (API fixture) → gerçek downloader/extractor → gerçek verified pipeline → mevcut-run handoff çalıştırır; kaynak/paket baytları aynı kalır. Generic paket adı, yanlış workflow ve bozuk ZIP baytı çıktı üretmeden reddedilir; izinsiz workflow ağdan önce durur. Dokuz kaynak upload sözleşmesi birebir karşılaştırılır; source artifact adı kaldırıldığında contract gate kırmızı olur. Beş yeni test eklendi.
- Odaklı ilk set 38/38 geçti. İlk toplu 769 testte 1 failure: eski opt-in testi yayın komutunu eski doğrulama flag'inde bekliyordu. Test, yeni default-false yayın flag'ini ayrıca zorunlu kılacak biçimde güncellendi. Nihai python -m madsc.offline_gate: 769 test + beş izole K1–K5 kapısı + kurulum + beş gerçek yerel rapor/K5 + 92+7 kaynak/10 komut/22 görev envanteri başarılı; contract gaps=0; git diff --check temiz. Kanıt: docs/MAIN_ARTIFACT_CHAIN_KANIT_2026-10-22.json.
- Sınırlar: API cevapları ve geçmiş girdileri fixture'dır; gerçek Actions upload/download kökeni bu tur ölçülmedi. Statik 0 fark, eski 92 otomasyonun aynı-input bağımsız runtime kabulü değildir. Tam kabul 0/92, 0/26, 0/22 kalır. Korunan kanal/EPG/favori/logo/arşiv/yedek ve eski depo değiştirilmedi; Actions, canlı probe, merge/PR71 veya IBO cihaz işlemi yok. IBO kullanıcıdadır.
- Sıradaki gerçek engeller: bağımsız eski/yeni aynı-input yürütme ve artifact çiftleri; 26 kuralın gerçek writer yollarında runtime kanıtı; K2/K3 harici geçmiş ve zaman aralıklı medya ölçümleri; kullanıcı IBO testi; K4 bağımsız harici backup/restore. Bunlar fixture veya yeni test sayısı artırılarak tamamlanmış gösterilmeyecek. İzinli gerçek koşu için kaynak girdileri/manifest ve harici kanıt sağlanmadan genel sistem bitti denmeyecek.


## 22 Ekim 2026 — Gerçek pair toplama için API ve ZIP bayt zinciri mevcut toplu CLI'ye bağlandı
- Tek hedef Madsc55/Madsc55-Tv/main; taban cffae104160b69866b2da69d8b9130d99dd5649f. Önceki dokuz artifact entegrasyonu ve statik 0 fark korundu. Bu paketin SHA'sı Git geçmişindedir; tek [skip ci] kod/test/kanıt/devir kaydıdır.
- Kalan somut kopukluk giderildi: verify_provenance_pair_api ve verify_provenance_pair_artifacts daha önce ayrı çağrılardı. Mevcut github_legacy_pair_client artık verify_provenance_pair_evidence ile altı bağımsız API kaydı, iki sınırlı ZIP indirmesi, archive SHA256, strict manifest, same-input ve snapshot bağlarını tek zincirde doğrular. Yeni standalone script/workflow/zamanlayıcı yok.
- Mevcut legacy_parity_cli --verify-github-artifacts açık opt-in seçeneğiyle sağlanan pinned kapsam pair'lerini topluca doğrular; token yalnız GITHUB_TOKEN ortamından gelir. Varsayılan mod tamamen ağsız ve eski çıktı uyumludur. Boş pair veya provenance dışı snapshot bu modda reddedilir; eksik 91/92 satır başarılı kabul edilmez. Bütün supplied pair'ler doğrulanmadan çıktı yazılmaz; raporda supplied_pairs_verified ve her pair'in API/bayt kanıtı ayrı alanlardır. Davranışsal kabul 0 kalır.
- K1 rapor hedefini artık kaynak okumadan ve ağdan önce denetler; yazmadan hemen önce tekrar denetler ve exclusive open kullanır. ZIP indirmesi repo/id/token kontrolü, 30sn timeout ve 2MiB+1 bounded read ile sınırlıdır; diske ZIP/extract yazmaz. Signed storage redirect'inde GitHub Authorization başlığı silinir, HTTPS dışı redirect reddedilir.
- Yedi yeni testte gerçek mevcut CLI/karşılaştırıcı, gerçek downloader'ın yerel HTTP fixture'ı ve gerçek ZIP parser birlikte çalışır. Altı API okuması ve iki indirme doğrulanır; yanlış workflow blob'u indirmeden, bozuk ZIP çıktıdan önce, eksik token/korunan yol ağdan önce durur. HTTP redirect/token sızıntısı, büyük paket, bool id, varsayılan ağsız mod ve boş pair negatifleri denetlenir. Odaklı 16/16; nihai python -m madsc.offline_gate 776 test ve bütün offline alt kapılar başarılı. git diff --check temiz. Kanıt docs/PAIR_API_BYTE_CHAIN_KANIT_2026-10-22.json.
- Gerçek salt-okunur GitHub sorgusu da yapıldı: yeni depoda event=workflow_dispatch toplam 9, tamamı döndü; hepsi K5, 21 Ekim sürümleridir. Son 10 genel run yalnız offline unit CI'dır; bunlar güncel runtime pair kanıtı değildir. Son K5 run39686179902 ve eski discovery run39768459333 artifact metadata örnekleri okundu; yenide Ekim22 kaynak çifti yok, eski örnek main dalında olduğundan pinned legacy karşılaştırma dalına bağlanamaz. Bu örnekler aynı-input v1 manifest çifti sağlamaz. Eski deponun bütün artifact geçmişi tarandı denmez.
- Araç sınırları kaydedildi: repo-geneli artifact ve workflow-spesifik run URL'leri connector allowlist tarafından reddedildi; desteklenen run collection + artifact-by-run araçları kullanıldı. Artifact wrapper yalnız ilk sayfayı/total_count olmadan verir; tam artifact envanteri iddiası yok. Gerçek ZIP baytları bu üretim sorgusunda indirilmedi; metadata başarıları bayt doğrulaması sayılmadı. Sorgular test/Actions çalıştırmadı.
- Kullanım hazır olduğunda: python -m madsc.legacy_parity_cli --inventory docs/LEGACY_SOURCE_SCOPE.json --snapshots actual-pairs.json --output reports/parity-api-byte-proof.json --replacement-workflow-root . --verify-github-artifacts ; reports gerçek/mevcut güvenli dizin ve actual-pairs.json bağımsız gerçek origin/manifest kaydı olmalıdır. Bu komut gerçek pair bulunmadığı için bu tur üretim ağına karşı çalıştırılmadı; fixture testi gerçek kabul sayılmaz.
- Tam kabul 0/92, 0/26, 0/22. Korunan kanal/EPG/favori/yedek/logo/arşiv, eski repo, PR71, merge, Actions dispatch, canlı probing ve cihaz testi değişmedi/yapılmadı. IBO testi kullanıcıdadır. Gerçek aynı-input pair, semantik bağımsız inceleme/yan etki, K1 gerçek writer/runtime26, K2/K3 canlı/zamanlı ölçümler ve K4 harici restore açık. Sıradaki iş gerçek v1 pair kanıtını bu mevcut birleşik CLI'ye vermek; eski raporu yeni manifest gibi yeniden etiketlememek.


## 22 Ekim 2026 — GitHub istemcilerinde ortak token/yönlendirme koruması
- Kaynak tabanı 21a9146cd09feccb19084f78965652142ea82f31; bu bölümün bulunduğu commit kod/test/kanıt paketidir.
- K1 güvenlik çapraz etkisi: K2 geçmiş artifact indirmesi, GitHub köken JSON istemcisi, K5 eski kaynak denetimi ve legacy pair ZIP indirmesi aynı HTTPS yönlendirme politikasına bağlandı. API JSON başka origin'e yönlendirilirse ikinci bağlantıdan önce reddedilir. İmzalı artifact depolama adresine geçişte Authorization kaldırılır; geri yönlendirmede geri eklenmez. HTTP ve URL kullanıcı bilgisi reddedilir. Eski 99 kaynak denetimindeki sınırsız JSON okuma da 2 MiB sınırına bağlandı. K3/K4 tüketici ve veri biçimleri değişmedi, beşli entegrasyon geçti.
- Doğrulama: 19/19 odaklı test; gerçek urllib redirect dispatch sahte HTTPS yanıtlarıyla, ağsız sınandı. Nihai python -m madsc.offline_gate: 783/783 test, beş izole kapı, kurulum envanteri, beş rapor/K5 round-trip başarılı; statik sözleşme farkı 0. Kanıt: docs/GITHUB_TRANSPORT_KANIT_2026-10-22.json; değiştirilmiş kaynak SHA256 ve tam kapı sonucu içerir. Bu pakette başarısız test yok.
- Otomatik devam görevi 6ad2b2e925bc8191a91b01728e57d707 mevcut saatlik takviminde etkin doğrulandı. Eski 605 test/eski görev öncelikleri kaldırıldı; her çalışmada güncel main/devir esas alınacak, küçük paket sonrası güvenli bağlantılı işe devam edilecek. next_run_time araçta null döndü; kesin sonraki saat veya kesintisiz çalışma iddiası yok. Yinelenen görev oluşturulmadı.
- Gerçek kabul 0/92, 0/26, 0/22 olarak kaldı. Korunan üretim verisi, eski depo, PR71, merge ve cihaz testi değişmedi. Actions veya canlı probing çalıştırılmadı.
- Sıradaki somut işler: K1-03 gerçek yazıcı çağrı yollarının kalanlarını görev defteriyle eşleştir; K4 harici geri-yükleme kanıtının mevcut tüketicilere bağlanmasındaki gerçek eksikleri incele. Gerçek v1 bağımsız aynı-input pair bulunduğunda mevcut --verify-github-artifacts CLI'yi kullan; eski metadata taramasını sebep olmadan tekrarlama. Harici/cihaz kanıtı yoksa kabul artırma.


## 22 Ekim 2026 — K4 rapor hedefi işlem öncesi kontrolü
- Başlangıç main SHA: 54b76d5dd03fe41a017fd5c7b23834ef7d0a1d18. Kod commit: 7dd644cf307eed79394cd70be4a65d2fab1fe83d [skip ci].
- madsc/restore_drill.py: isolated-report-root için beklenen yol ve K1 yerel çıktı kapısı, run_drill çağrısından önce denetlenir. Normal --output hedefi de tatbikat başlamadan kontrol edilir; yazma öncesi mevcut kontrol korunur.
- Bu oturumda offline regresyon çalıştırılmadı; değişiklik henüz testle doğrulanmış değildir. Actions dispatch yok. 783 önceki SHA'nın sonucudur, yeni commit sonucu değildir.
- Açık işler: yeni SHA'da offline_gate, K4 hatalı yolun tatbikatı başlatmadığını gösteren negatif test, K4 kanıt dosyası TOCTOU incelemesi, K1-03 gerçek writer haritası ve bağımsız harici restore kanıtı. Kabul 0/92, 0/26, 0/22.
- Korunan IPTV/EPG/playlist/favoriler/logo/yedek/arşiv, eski depo, PR #71 ve cihaz testi değiştirilmedi. Sıradaki somut adım: K4 negatif testleri ve tam offline regresyon; engel varsa açıkça kaydet.


## 22 Ekim 2026 — K4 erken red negatif testleri
- Kod 7dd644cf307eed79394cd70be4a65d2fab1fe83d üzerine tests/test_restore_drill.py negatif testleri eklendi: commit 56ca20984f043263579179ee810b04b53f0304ef [skip ci]. Yanlış izole rapor adı ve mevcut normal çıktı hedefi, run_drill çağrılmadan reddedilmelidir. Önceki tekrar-yazma beklentisi K1 ProtectedWriteRejected ile eşleştirildi.
- Bu çalışma ortamında GitHub deposu yerel kopyalanamadı (github.com DNS erişimi yok). Testler çalıştırılmadı; yeşil sonuç veya 783 yeni test iddiası yok. Actions dispatch yapılmadı. Öncelik: erişilebilir ortamda python -m unittest tests.test_restore_drill ve python -m madsc.offline_gate doğrulaması, sonra K4 tüketici yarış koşulu incelemesi.
- Korunan veri, eski depo ve cihaz testi değişmedi; gerçek kabul 0/92, 0/26, 0/22.


## 22 Ekim 2026 — K4 kanıt okuyucu sertleştirme
- madsc/k4_evidence.py commit 37f74521295d84705a702da4d4b13d696f50fcb8 [skip ci]: çıktı yolu okumadan önce denetlenir; kanıt os.open/O_NOFOLLOW (varsa), fstat ile regular/single-link, 1 MiB bounded read kullanır. Symlink parent kontrolü korunur. Test commit 80972e5badcc47173df7f4d613891b268daeade5: mevcut çıktı, symlink ve büyük kanıt negatif senaryoları.
- Kod/test GitHub'a kaydedildi; bu turda yerel test ve offline_gate çalıştırılmadı, Actions tetiklenmedi. O_NOFOLLOW olmayan platformlarda yarış koruması sınırlıdır; parent değişimi yarışına karşı tam fd-tabanlı dizin zinciri henüz yoktur.
- Öncelik: test_restore_drill ve test_k4_evidence + tüm offline_gate çalıştırıp gerçek sonuçları kaydet; K1-03 gerçek writer denetimine devam et. Gerçek kabul 0/92, 0/26, 0/22; korunan veriye dokunulmadı.


## 22 Ekim 2026 — K4 doğrulayıcı çıktısında ikinci kapı
- madsc/k4_evidence.py commit d8e5e1925c7ea9994f3e0649b4640cf5569b038a: parse/doğrulama sonrası çıktı yolunu tekrar denetle; os.open(O_EXCL|O_CREAT|O_NOFOLLOW varsa) ile tek seferlik çıktı oluştur. tests/test_k4_evidence.py commit bc21ebd0954250b65b0ae4665d40775242ecee91: geçerli kanıttan çıktı, production_ready=false, external_storage_proven=false ve ikinci yazmayı reddetme senaryosu.
- Yerel depo indirme github.com DNS hatası nedeniyle mümkün olmadı; bu yeni SHA için testler/offline_gate çalıştırılmış değildir, GitHub Actions tetiklenmedi. Elde doğrulanmış yeni test sonucu yoktur. Tam parent-ancestor TOCTOU koruması halen açık; K1 runtime kabul iddiası yok.
- Sonraki öncelik: erişilebilir çalıştırma ortamında test_restore_drill, test_k4_evidence ve python -m madsc.offline_gate; gerçek sonuçlar gelmeden 783 sayısını güncel sayma. Gerçek kabul 0/92, 0/26, 0/22. Korunan dosyalar, eski depo ve IBO cihaz testi değişmedi.


## 22 Ekim 2026 — K4 JSON/üst-dizin negatif testleri
- tests/test_k4_evidence.py commit b853106868f1cc13bc2172051c22bd71641ec7a8 [skip ci]: yinelenen files_checked JSON anahtarı ve sembolik bağlantılı kanıt üst dizini reddi; başarısız doğrulamada çıktı yokluğu. Kod davranışı değişmedi.
- Yerel ortam github.com DNS çözümleyemiyor; testler/offline_gate bu yeni SHA'da çalıştırılmadı, Actions dispatch yok. Gerçek kabul 0/92, 0/26, 0/22. Öncelik erişilebilir test koşucusunda odaklı testler ve tam offline_gate; test sonucu olmadan yeşil iddia edilmez.


## 22 Ekim 2026 — K4 hardlink negatif testi
- tests/test_k4_evidence.py commit 9facdef81be2553e145465e9c65cbff889b11b2f [skip ci]: kanıt dosyasının stat.st_nlink != 1 durumunda reddi ve çıktı yokluğu kontrolü; üretim verisine dokunulmadı.
- Bu oturumda git ls-remote github.com DNS çözümleme hatası verdi. Yerel testler/offline_gate çalıştırılmadı, GitHub Actions tetiklenmedi. Test sonucu doğrulanana kadar gerçek kabul 0/92, 0/26, 0/22 olarak kalır.


## 22 Ekim 2026 — K4 O_NOFOLLOW kapısı
- madsc/k4_evidence.py b0f1d0a49966608c8e63ad291f46a9fb043c2cd4 [skip ci]: os.O_NOFOLLOW yoksa kanıt okuma fail-closed. tests/test_k4_evidence.py eadb7e40a412679c30108a0260c6ada76fa12a71 [skip ci]: bu durumu ve çıktı üretilmediğini kontrol eden test.
- Yerel git ls-remote: github.com DNS çözümlenemiyor; testler ve offline_gate yeni HEAD üzerinde çalıştırılmadı. Actions tetiklenmedi. Üst dizin TOCTOU sertleştirmesi ve gerçek kabul kanıtı açık; 0/92, 0/26, 0/22.


## 22 Ekim 2026 — K4 sahte üretim iddiası reddi
- K4 verify(): production_ready=True/1 ve category='k3' gibi sahte alanları reddetme, opsiyonel category yoksa eski run_drill raporuyla uyum; kod c189cde33a47690373eddc6c502b4e14cfb82fd6, test afe19df9646868a0153a19c4c9895c4bf90c29d1 [skip ci].
- Yerel git ls-remote denemesi github.com DNS çözümleme hatasıyla başarısız. Bu SHA için test ve offline_gate doğrulaması yapılmadı, Actions tetiklenmedi. Gerçek kabul 0/92, 0/26, 0/22; korunan veriye dokunulmadı.


## 22 Ekim 2026 — K5 davranış karşılaştırma çıktısı, test bekliyor
- madsc/legacy_parity_cli.py commit 108de8e7c049bf8abab52fa69ae587133ba420f4: K5 karşılaştırma raporu exclusive os.open(O_CREAT|O_EXCL, varsa O_NOFOLLOW) ile açılıyor; ikinci yol kontrolü korunuyor. tests/test_legacy_parity_cli.py commit 1f4d31a03f3ca7b61bd06b28c4693bd3e3142867: ikinci kontrol sonrasında sembolik bağlantı değişiminde hedefin korunmasını denetleyen regresyon eklendi.
- Bu SHA için test sonucu yok; GitHub Actions tetiklenmedi. K5 gerçek davranış eşdeğerliği 0/92, 26 runtime güvenlik 0/26, görev kabulü 0/22. Öncelik test_legacy_parity_cli, tam offline_gate, sonra eksik gerçek eski/yeni çalışma çiftlerini toplu kanıtlama. Korunan veriye dokunulmadı.


## 22 Ekim 2026 — Playlist K2/K3→K5 güvenli taslak hattı
- madsc/playlist_previews.py: katalogdaki yinelenen source_index ve URL SHA256 reddi (db091a3f88e7ce515858310d70c6d754925eec5d); üretim yazısı/hazırlığı iddiası taşıyan kataloglar reddediliyor (88ceeb937285d5adc5433f659de67f2d62a2945a). Regresyon testleri tests/test_playlist_previews.py (c9a88cc750bf8c98272ef4ef23cca13f84583fd1 ve c8f5592d1399fc21b8a7b1c312451fbf49b18f59).
- Kod ve testler commit edildi, bu SHA için test yürütülmedi. Mevcut playlist/YEDEKLER/YENILER/FAVORILER/EPG değiştirilmedi; Actions tetiklenmedi. İzole taslak üretimi canlı otomatik playlist güncellemesinin kanıtı değildir. 92 davranışsal kabul, 26 runtime güvenlik kabulü ve 22 görev kabulü değişmedi.

## 22 Ekim 2026 — bekleyen K1/K4/K5 paketinin toplu doğrulaması
- Başlangıç main `adbaf72d6eb21b88d81c557ad0076a70ca617164`; eşzamanlı playlist kaçış düzeltmesi `5af20718f14be617e0c20b5fee797572d7924a6e` okundu ve korundu. Kod/test/kanıt commit'i `61bbf78214a63400083cf7d615c64a1b13547896` (`[skip ci]`).
- İlk odaklı 44 testte iki failure ve bir error bulundu: hardlink testi geçerli kaynağı hâlâ iki linkli bırakıyordu; literal backslash kaçışlı playlist adı reddedilmiyordu; K1 AST envanteri yerel `flags` değişkenindeki `O_CREAT` bitlerini ve `os.fdopen` modunun ikinci argümanını çözemiyordu. Üçü düzeltildi; eşzamanlı `5af2071` playlist düzeltmesi tekrar yazılmadı.
- K1 envanteri artık aynı lexical scope içindeki en yakın flag atamasını çözerek `os.open(..., flags)` yazıcılarını bulur; `os.fdopen(fd, mode)` gerçek ikinci argümana göre okuma/yazma ayrılır. Aday sayısı 130, dinamik inceleme 20; subprocess ve gerçekten dinamik çağrılar açık kalır. `all_writer_callsites_manually_verified=false`; bu 26/26 runtime kabulü değildir.
- K4 erken hedef reddi, O_NOFOLLOW, regular/single-link/bounded read, duplicate JSON, sahte production/category ve exclusive çıktı testleri; K5 parity/playlist ve source-import sınırları birlikte geçti. Odaklı sonuç 44/44. Nihai `python -m madsc.offline_gate`: **800/800**, beş izole K kapısı, kurulum envanteri, beş rapor/K5 round-trip, 92+7/10 komut/22 görev ve `static_gaps_total=0` başarılı. `git diff --check` temiz.
- Kanıt: `docs/K1_K4_K5_PENDING_VALIDATION_2026-10-22.json`. Actions dispatch/rerun, canlı stream probing, cihaz testi, üretim/korunan veri yazısı, eski depo, merge veya PR #71 işlemi yapılmadı.
- Açık kabul/engeller: 0/92, 0/26, 0/22. Gerçek aynı-input bağımsız legacy/replacement execution+artifact çifti, K2/K3 canlı/harici ölçümler, IBO cihaz sonucu, K4 bağımsız harici restore ve 20 dinamik writer/subprocess adayının gerçek runtime değerlendirmesi açık.
- Sıradaki somut yerel iş: 20 dinamik aday içinden K1 writer etkisi olabilen subprocess çağrılarını komut/argüman düzeyinde sınıflandır; yalnız salt-okunur probe/test çağrılarını ayrı işaretle, belirsiz veya üretim yazabilen çağrıları fail-closed inceleme olarak bırak. Harici kanıt olmadan kabul sayaçlarını artırma.


## 22 Ekim 2026 — Bu sohbetin kapsamı K2 ve K4; ortak çalışma kaydı
- Kullanıcının son talimatı: bu sohbet yalnız K2 ve K4'e odaklanacak, diğer sohbetle çakışmayacak ve biten işleri tekrarlamayacak. Kullanıcı sohbet başlığını K2 ve K4 istedi; başlık değiştirme aracı yok, fiilen değiştirildi denmedi.
- Güncel main'de diğer sohbetin restore_drill erken hedef kontrolü zaten bulundu; yeniden uygulanmadı ve dosya değiştirilmedi. K1/K5, online pilot, parser ve playlist değişiklikleri korundu. 56f64fa test tabanından e6b9e396776f04f06dd7ab55e7528e3c93c764a8 yayın tabanına gelen üç commit incelendi; bu paketin dosyalarıyla çakışmıyor.
- K4 backup_to_new_sandbox / restore_to_new_sandbox: yeni kök hedef ve tüm üst dizinler kaynak içerik okunmadan ve mkdir öncesi merkezi K1 kapısından geçiyor. Korunan EPG/FAVORILER/YEDEKLER/logo/playlist hedefleri engelleniyor. Ortak fixture_report_writer yalnız K4'ün gerekli bağımlılığı olarak düzeltildi: korunan kök altında reports dizini bile oluşturulmadan ret; mevcut son yazma kontrolü korunuyor. Aynı korumayı kullanan K3/K5 raporları da test edildi, ilgili iş akışları değiştirilmedi.
- K2 atomic_write_pair: yalnız dosya adı yerine tam hedef/üst dizin ve mevcut regular/single-link dosya kontrolü, staging öncesi ve os.replace öncesi uygulanıyor. Geçerli atomik güncelleme semantiği korunuyor. History ZIP çıkarıcısı her iki belgenin history/channels şemasını dizin veya dosya oluşturmadan doğruluyor. Geçersiz şema artık yarım çıktı bırakmıyor.
- Son K2/K4 odaklı doğrulama 87/87 başarılı. Tam kapı 56f64fa tabanında 816 test çalıştırdı: 5 failure + 3 error nedeniyle BAŞARISIZ. Beş izole K kapısı ve beş rapor/K5 round-trip geçti. 816 başarılı test olarak sunulmayacak. Kanıt ve kaynak hashleri docs/K2_K4_WRITE_PREFLIGHT_2026-10-22.json içinde.
- Diğer sohbet için mevcut toplu engeller: workflow_consolidation.consolidation_plan yeni madsc-online-pilot-gates.yml dosyasını envanter dışı görüyor; bu kök hata beş offline kapı testini de düşürüyor. tests/test_playlist_previews.py içindeki test_import_to_five_playlists_end_to_end_offline ve test_offline_cli_emits_five_drafts_without_writing_files kaynakları gerçek satır sonu yerine literal \\n kullanıyor, Invalid playlist header alıyor. Bu aktif diğer-sohbet dosyaları bu pakette değiştirilmedi. Düzeltmeleri sonrasında tam kapı yeniden gerekli.
- Önceki /tmp çalışma ortamı kayboldu; yayımlanmamış geçici K4 değişiklikleri güncel main ile karşılaştırılarak yalnız eksik kısmı yeniden oluşturuldu. İlk geçici odaklı testte eski kapı çağrı beklentisi başarısızdı; reports mkdir öncesi ret beklentisiyle güncellendi ve 87 test geçti.
- Üretim verisi, eski depo, PR71, merge, Actions dispatch ve canlı probing yapılmadı. Gerçek kabul 0/92, 0/26, 0/22; harici restore/IBO/bağımsız runtime kanıtı açık. Sıradaki K2/K4 işi: mevcut geçmiş alım ve yedek kopyalama akışlarında değişen kaynak/yarım yazma temizliği sınırlarını incele; dış depolama kanıtı olmadan harici restore kabulü verme.

## 23 Ekim 2026 — K4 manifest root alias koruması
- Güncel main incelendi; K4 snapshot_manifest() yalnızca son dizin bileşeninin symlink olup olmadığını denetliyordu. Gerçek bir dizine symlink üst dizin üzerinden ulaşılması doğrudan manifest snapshot çağrısında kabul edilebilirdi.
- Kod düzeltmesi: d23c4e54e6882b01bba1440ac38e61d8abb180b4 — snapshot_manifest() artık kök dizinin ve tüm üst dizinlerin symlink olmadığını, ayrıca kökün kanonik mutlak yolla eşleştiğini kontrol ediyor.
- Negatif regresyon testi: c53875f29dc0d605d24295e642dcc75f9ab358ee — gerçek köke symlink üst dizinden erişildiğinde manifest snapshot reddedilmeli.
- Test çalıştırılmadı; Actions yeniden tetiklenmedi ([skip ci]). Dolayısıyla kod/test sonucu doğrulanmayı bekliyor.
- Canlı playlist, EPG, favoriler, cihaz verileri, üretim yedekleri ve arşivler değiştirilmedi. Harici backup/restore ve K3 IBO cihaz kabulü açık. Kabul sayaçları değişmedi: 0/92, 0/26, 0/22.

## 23 Ekim 2026 — K4 sandbox rollback yarış koşulu
- İncelemede backup_to_new_sandbox() ve restore_to_new_sandbox() hata sırasında yalnızca destination yoluna bakarak shutil.rmtree(destination) çağırıyordu. Hata anında aynı yol başka bir işlem tarafından başka bir dizinle değiştirilirse, cleanup bu işleme ait olmayan dizini silebilirdi.
- Kod commit d3ce6cb5eeb962473dfd0cc95ec05d84e679d0b6: her iki işlem de oluşturduğu dizinin (st_dev, st_ino) kimliğini kaydediyor; rollback yalnızca hedef hâlâ aynı gerçek dizin inode'uysa kaldırıyor.
- Negatif test commit 34028a822c9d38738a7edcf35a84913e3c0b17c4: hem backup hem restore sırasında hedef dizin eşzamanlı değiştirilirse, yeni dizindeki sentinel dosyasının korunması doğrulanacak.
- Testler çalıştırılmadı; bu commit'lerde [skip ci] kullanıldığı için otomatik CI sonucu beklenmiyor. Bu yüzden doğrulanmış başarı iddiası yok.
- Önceki root-symlink koruması ve testi: d23c4e54e6882b01bba1440ac38e61d8abb180b4 / c53875f29dc0d605d24295e642dcc75f9ab358ee.
- Canlı IPTV/EPG/favoriler/cihazlar/üretim yedekleri/arşivler değiştirilmedi. Harici yedek ve üretim geri yükleme kabulü açık. Sayaçlar değişmedi: 0/92 workflow, 0/26 güvenlik kuralı, 0/22 ana görev.

## 23 Ekim 2026 — K4 manifest symlink TOCTOU sertleştirmesi
- snapshot_manifest() önceden symlink kontrolleri sonrası Path.open() ile açıyordu; kontrol ile açılış arasında bir bileşen symlink ile değiştirilirse TOCTOU riski kalıyordu.
- Kod commit: cca807332bf900d9d70206c4a8261acfb1c21cdf. Yeni _open_relative_file_nofollow() root ve her alt dizini O_DIRECTORY|O_NOFOLLOW ile dir_fd üzerinden açıyor, son dosyayı da O_NOFOLLOW ile açıyor; fstat ile normal dosya ve nlink==1 kontrolü korunuyor. Manifest yolu çözülmüş hedeften değil, doğrulanmış istenen göreli yoldan yazılıyor.
- Test commit: 0ad1566d25799edb610745a60a76ce24e27a466c. Final symlink reddi, ara dizin symlink reddi ve nested göreli yol korunması için üç test eklendi.
- Testler çalıştırılmadı; commit mesajlarında [skip ci] olduğu için CI otomatik tetiklenmedi. Kod ve test sonucu doğrulanmayı bekliyor.
- Önceki sandbox rollback inode-koruması d3ce6cb5eeb962473dfd0cc95ec05d84e679d0b6; testler 34028a822c9d38738a7edcf35a84913e3c0b17c4.
- Üretim playlist/EPG/favoriler/cihaz verileri ve yedekler değiştirilmedi. Gerçek harici backup/restore ve K3 cihaz kabulü açık. Kabul sayaçları: 0/92 workflow, 0/26 runtime güvenlik kuralı, 0/22 ana görev.
