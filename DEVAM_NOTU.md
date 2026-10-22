# Madsc55-Tv — DEVAM NOTU

Güncelleme: 22 Ekim 2026 (Europe/Stockholm).
Son geliştirme commit SHA: f222a81ce96901a8adc0dbc92a5213cf149500c9
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
