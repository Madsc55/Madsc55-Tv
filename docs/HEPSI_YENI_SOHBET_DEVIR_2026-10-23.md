# MADSC55-TV — HEPSI yeni sohbet devir ve eksikler raporu
**Tarih:** 23 Ekim 2026 (Avrupa/Stockholm; teknik run timestamps GitHub UTC).  
**Kanonik repo:** `Madsc55/Madsc55-Tv`, dal `main`.  
**Okunan kayıtlar:** `DEVAM_NOTU.md`, `PROJE_HAFIZASI.md`, `docs/HEPSI_BIRLESIK_DOGRULAMA_2026-10-23.md`, `docs/K1_K5_KANITLI_GOREV_DEFTERI.json`.  
**Referans main HEAD (notu oluşturmadan önce):** `4b4c34d7cafffc34e47029f0d8d4683a9efbff59`. Bu notun commit'i HEAD'i değiştirecektir; devamında HEAD'i tekrar oku.

## Kesin doğrulama
- En son doğrulanmış `MADSC55 — Offline Unit Tests`: GitHub Actions [39865933101](https://github.com/Madsc55/Madsc55-Tv/actions/runs/39865933101), test edilen SHA `a4c70f7277be8aad73cdd95d027115b7bcab469d`; job success; logda **990 keşfedilen test**, `tests_passed=true`, `five_stage_fixture_gate_passed=true`, `all_offline_gates_passed=true`, `production_ready=false`. K1 AST raporu: 97 Python dosyası, **75 yazma/mutasyon adayı**; tüm adaylar manuel inceleme ister.
- `a4c70f7..4b4c34d` karşılaştırmasında kod/test değil sadece `DEVAM_NOTU.md`, `PROJE_HAFIZASI.md` ve `docs/HEPSI_BIRLESIK_DOGRULAMA_2026-10-23.md` değişti. Dolayısıyla o noktada mevcut çalışma kod/test ağacı başarılı CI SHA ile aynıydı.
- Önceki run `39864090233`: 979 offline test ve K1–K5 izole kapıları başarılı; artık eski baseline.
- Kullanıcının işaret ettiği `39863892845` run ID'si API'de 404; sonuç doğrulanamadı. Bu ID için başarı/başarısızlık iddia etme.
- GitHub CI tetiklemelerinden hiçbiri manuel workflow_dispatch olarak yapılmadı; kod/test push'ları otomatik offline unit-tests çalıştırdı.

## İlerleme yüzdelerini dürüst yorumlama
- Offline test kapısı: **990/990 = %100 başarılı** (yalnızca suite kapsamı, üretim kabulü değil).
- 22 kanıtlı ana görev defterinde: **0 completed, 7 in_progress, 15 pending**; dolayısıyla **0/22 resmî kabul**, **22/22 nihai kabul eksik**. 7 işte ilerleme var; hepsinin sıfırdan yapılması gerekmiyor.
- 92 eski otomasyon: **0/92 davranışsal eşdeğerlik kabulü**. Altı kaynak davranışı inceleme belgesinde toplam **18/92 (%19,6) statik kaynak incelemesi** mevcut; **74/92 (%80,4)** statik inceleme bekliyor. Statik inceleme ile kanıtlı parity farklıdır.
- 26 runtime güvenlik kuralı: **0/26 bağımsız kabul**. K1 offline testler ve statik AST tarama bunu ikame etmez.
- Tek bir tüm-proje % tamamlandı rakamı, ağırlıklı önceden tanımlı iş kapsamı olmadan güvenilir biçimde hesaplanamaz. Offline %100 başarı ile üretim kabulünü birleştirme.

## 5 sistemin gerçek durumu
### K1 — Güvenlik
- Yazma hedefi guard-before-mkdir, sembolik bağlantılı workflow ve `.github` güven sınırı denetimleri, fail-closed manifest/parsing korumaları, AST yazma çağrısı envanteri ve regresyonlar mevcut.
- `madsc/write_callsite_audit.py` raporunda 97 dosya/75 mutasyon adayı mevcut. `replace()` gibi genel API adayları sahte pozitif olabilir; tek tek sınıflandır ve shell/subprocess/dinamik yazmaları ayrıca gözden geçir. 26 çalışma zamanı kuralının bağımsız enforcement kanıtı hâlâ 0.
- Korunan playlist, EPG, favoriler, cihaz, logo, yedek/arşiv verilerine hiçbir izinsiz yazma yapma.

### K2 — Keşif
- Bounded M3U kaynak ayrıştırma, aday fingerprint/SHA ve paylaşılan K2/K3 snapshot kontrolü, alternatif/duplicate ve artefact provenance mekanizmaları izole testlerle doğrulanmış.
- Gerçek kaynak ve lisans teyidi, günlük keşif davranışının eski sistemle eşdeğerliği, gerçek kaynaktan bağımsız artifact origin zinciri açık.

### K3 — Kanal sürekliliği ve EPG
- `madsc/trial_epg_matching.py` ve `madsc/epg.py` artık XMLTV `<tv>` kökü, eksik/boş kanal ID ve duplicate ID durumunda fail-closed. Kod commit'leri `939267f`, `9a1ebdc`; test commitleri `f48f04f`, `420d15d`. CI run `39865719002` başarılı.
- İzole K3 URL/fingerprint, >=6 saat aralıklı üç test, manifest/probe tanılama mevcut. Gerçek üç ölçümün bağımsız kökeni, ffprobe/ffmpeg ile gerçek video/ses, IBO Player Pro cihazında EPG/XMLTV ve Pages dağıtımı henüz doğrulanmadı.
- K3 gerçek pilot workflow'ları `.github/workflows/madsc-k3-live-manifest-pilot.yml` ve `madsc-k3-turkish-tv-video.yml` yalnız `workflow_dispatch` tetikleyicisine sahip. Bu GitHub bağlantısında dispatch/POST aracı yok. Açık yetki olmadan live probe veya cihaz erişimi yapma.

### K4 — Yedekleme ve geri yükleme
- Kaynak okuma tarafında `_open_relative_file_nofollow` descriptor-relative nofollow/dirfd + regular file/fstat/nlink kontrolleri var. Hedef yazma tarafı `_create_relative_file_nofollow` ile `O_NOFOLLOW/O_DIRECTORY`, descriptor-relative nested `os.mkdir`, `O_EXCL` ve destination inode tekrar kontrolü üzerinden yapılıyor; symlink/paths negatif testleri mevcut.
- Kod commit'leri `e32d522`, `949c239`; test commitleri `a5590c3`, `a4c70f7`. Son run `39865933101`: 990 test başarılı.
- Sandbox backup/restore eşleşmesi, **harici** storage'a yazımın ve ondan bağımsız izolasyonda restore'un gerçekten yapıldığını kanıtlamaz. Haricî yedek, bağımsız restore makbuzu, 1/15 günlük takvim eşdeğerliği, arşiv/VOD kabulü açık.

### K5 — Birleştirme / bakım
- 5 izole kapı + K5 tarafından 5 raporun tüketimi offline doğrulandı. 99 workflow YAML kaynak envanteri var; 92'si eski davranışsal eşdeğerlik kapsamı. Altı dokümanda 18 eski workflow'un statik davranış incelemesi yapıldı: `docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_01_2026-10-23.md` ... `_06_2026-10-23.md`. Bir örnek sabit kaynak sözleşmesi: `docs/legacy-workflow-contracts/madsc-documentation-check.json`.
- 92 eski otomasyonun hiçbiri için tam legacy ve replacement runtime, input/output, yan etki, timeout/retry/artifact, bağımsız reviewer kanıt paketi kapatılmadı: **0/92**.

## 22 ana görevin durum dökümü
- `docs/K1_K5_KANITLI_GOREV_DEFTERI.json`: 22 kayıt.
- **in_progress**: K1-03, K2-07, K2-08, K3-10, K3-13, K4-16, K5-19 (7 adet).
- **pending**: K1-01, K1-02, K1-04, K2-05, K2-06, K3-09, K3-11, K3-12, K3-14, K4-15, K4-17, K4-18, K5-20, K5-21, K5-22 (15 adet).
- **completed**: 0. Durumları gerçek bağımsız kanıt olmadan tamamlandıya çevirme.

## Kesinlikle korunacak sınırlar
1. Yalnız `Madsc55/Madsc55-Tv` repo, `main`; eski `Madsc55/madsc-tv` deposunu yalnız okumak gerekiyorsa oku, **yazma**.
2. Yeni yazmadan hemen önce canlı HEAD ve hedef dosya blob SHA'sını yeniden doğrula; paralel K1/K2/K5 ve K3/K4 sohbetlerinden gelen değişikliklerin üzerine yazma. `[skip ci]` sadece devir/dokümanlarda; CI sonucuna ihtiyaç varsa kod/test commit için normal push'un tetiklediği workflow'u doğrula. Bilerek manuel Actions dispatch/rerun yapma.
3. `CALISANLAR.m3u`, XMLTV/EPG, `FAVORILER`, `YENILER`, `YEDEKLER`, `HEPSI`, logolar, gerçek cihaz ve üretim arşiv/yedeklerini değiştirme; PR #71'i merge etme.
4. İzole testlerin başarılı olması gerçek servis, oynatıcı, EPG veya üretim onayı anlamına gelmez. Sayaçları yalnız bağımsız kabul kanıtıyla yükselt.

## Yeni sohbette öncelik
1. Bu dosyayı ve `DEVAM_NOTU.md`, `PROJE_HAFIZASI.md` en son kayıtlarını oku; güncel `main` HEAD ve GitHub Actions sonuçlarını doğrula.
2. K1 75 yazma adayının önce gerçek disk/yazma etkisi bulunanlarını sınıflandır; yan etkileri kritik olan korumasız path'ler için izolasyon/negatif regresyon testleri ekle. K3/K4 yeniden düzeltmelerini tekrarlama.
3. K5'in 18/92 statik inceleme sonrası 74 workflow için yeni üçlü gruplar halinde kaynak anlamını kaydet; statik incelemeyi kabul sayma. Üretim dışı görevlerde eski ve yeni scriptleri aynı sabit fixture'da differential çalıştır.
4. K3 gerçek yayın/IBO/EPG için yalnız yetkili, kaynağı belli dış cihaz ve bağımsız ölçüm kanıtları; K4 için harici yedek ve restore kaydı olmadan kabul verme.
5. 26 kural/22 görev ve 92 parity kabul defterlerini gerçek kanıtlarla güncelle; 5 sistemin uçtan uca aynı güvenli raporu oluşturduğunu kanıtla.
6. Her değişikliğin ardından CI logunu ve test edilen SHA'yı kaydet, yanlış başaran iddiasından kaçın; düzenli devir notu bırak.

**Yeni sohbet başlangıç istemi**: `Madsc55/Madsc55-Tv main üzerinde docs/HEPSI_YENI_SOHBET_DEVIR_2026-10-23.md, DEVAM_NOTU.md, PROJE_HAFIZASI.md son kayıtlarını oku; HEAD ve Actions'ı doğrula. K1–K5 kodunu tekrarlamadan geliştir; önce K1 75 yazma adayının kök neden incelemesini, K5 74 workflow statik incelemesini ve K3/K4 gerçek kanıt eksiklerini ilerlet; testleri doğrula, notları güncelle. Korunan üretim dosyalarına dokunma, eski depoya yazma, PR #71'i merge etme. Resmî kabul sayaçları 0/92, 0/26, 0/22.`


## 23 Ekim 2026 — Sohbet devri ek kaydı (EPG ve son CI)

- Kullanıcı: K1–K5 beşli sistemi topluca bitirmeye odaklan; diğer sohbetlerin devirlerini ve güncel GitHub kanıtlarını kontrol et. IBO Player Pro üzerinde EPG'nin gerçek görüntüleme kabulünü kullanıcı yapacak; asistan EPG kodunu, raporlamayı ve güvenli testleri üstlenecek.
- Ana depo `Madsc55/Madsc55-Tv`, `main` kontrol anındaki HEAD `9885b537ef3d` (kısa SHA); başka K1–K5 işçileri eşzamanlı commit yapıyor, yeni sohbette HEAD tekrar okunmalı. Son görülen ana CI: `40002212175` başarılı (`9b950286d905`), daha yeni `40002248915` ve `40002229536` iptal edilmiş; bunlar HEAD kabul kanıtı değildir.
- Ayrı EPG deposu `Madsc55/madsc-tv` (`main`). EPG dosyası `epg/madsc-epg.xml`; Pages yayın akışı onu köke `madsc-epg.xml` olarak kopyalıyor. EPG raporu 23 Ekim: 1.039 liste girdisi, 730 eşleşen, 309 eşleşmeyen, 583 kullanılabilir liste girdisi, 8.600 program. Cihaz/İsveç doğrulaması bekliyor.
- EPG commit'leri: `a9dba704` sıkıştırılmış/açılmış indirme boyut sınırı; `d1c60773` bozuk gzip hata yönetimi; `10b7377c` eksik `tvg-id` ayrıştırmalı rapor; `7022d2d0` çevrimdışı regresyon testleri; `97c784bf` günlük üretim öncesi test kapısı; `bf424bcf` salt-okunur bağımsız EPG CI. `bf424bcf` için Actions `40002039822` **başarılı**. Bu CI başarıları gerçek günlük yayın veya IBO cihaz kabulü anlamına gelmez.
- ÖNEMLİ: Bu EPG değişiklikleri ayrı `Madsc55/madsc-tv` deposunda yapılmıştır; ana beşli sistem deposuyla karıştırma. Korunan canlı IPTV/EPG listelerine doğrudan yazma. Kullanıcı EPG'yi IBO Player Pro'da doğrulayacak.
- Sonraki işler: Ana depoda 92 workflow davranışsal parity, K1 gerçek yazma riskleri, K3 gerçek yayın/EPG, K4 harici restore, K5 arşiv kabulünü bağımsız kanıtlarla ilerlet. Önceki kabul sayaçlarını kanıt olmadan yükseltme. EPG tarafında 309 eşleşmeyenin kaynak/kimlik ayrımını güvenli biçimde araştır, yeni günlük test kapısının gerçek üretim koşusunda çalıştığını doğrula.
- PR #71'i birleştirme; kullanıcı dosyaları, favoriler, logolar, yedekler ve arşivleri koru. `[skip ci]` commit'lerini test edilmiş sayma.
