# HEPSI — Birleşik doğrulama devam kaydı (2026-10-23)

## Kanonik durum
- Depo: Madsc55/Madsc55-Tv.
- GitHub main kontrol edilen HEAD: `0a286ea23065cb43071026c75bebf899d0bd230d`.
- Son 6 Actions sorgusunda en son başarı `39861826787`, SHA `a4fbd23399318bde719db095de04ea3ee7d4913a`; bu güncel HEAD değildir. Yakın geçmişte birden çok başarısız/iptal koşusu da var. Actions yeniden tetiklenmedi.
- Kullanıcı ZIP'i mevcut main'den eski; ZIP'te görülen hatalar doğrudan güncel main hatası kabul edilmemeli.

## Güncel kaynak karşılaştırmasında görülen düzeltmeler
- `tests/test_candidate_probe_link.py` artık adaylara güvenli `name` metaverisi sağlıyor ve AST incelemesinde `ast.walk(parsed)` kullanıyor.
- `tests/test_handoff.py` süreklilik örnekleri 10:00, 16:00, 22:00 UTC; her aralık 6 saat.
- `tests/test_k5_head_observation.py` ve `tests/test_probe_target_gate.py` güncel kaynakta eski ZIP'teki yalın aday fixture'larından farklı; eski hata bunlara kopyalanmamalı.
- `tests/test_legacy_retest_differential_batch.py` test saati dondurma düzeltmesi GitHub commit `b72e23bad5495658bf1f1bfb42ff63782df9743a` ile kaydedildi.
- `tests/test_k3_live_manifest_source_snapshot.py` syntax düzeltmesi commit `8f138e30d536e686ceac7cb15af6928dceeadfae` ile kaydedildi.

## Eski ZIP yerel tarama sonucu (tarihsel; güncel main sonucu değildir)
- 150 test dosyası 10 modüllük gruplarla taranırken ZIP'in eski kodu nedeniyle hata grupları bulundu: aday metaverisi fixture'ları, K3 üç aşamalı süreklilik zaman aralıkları, K3 loader AST test beklentisi, K5/legacy test farkları.
- Güncel main dosyalarıyla karşılaştırınca bu bulguların bir kısmı zaten düzeltilmiş; ZIP sonuçları kanonik test kabulü değildir.
- Legacy differential hedefli test yerel ZIP'te 1/1 geçti; bu sadece ZIP kopyasında testtir.

## Kabul sayaçları — değişmedi
- 92 eski workflow davranışsal eşdeğerlik: 0/92 kabul.
- 26 güvenlik kuralı: 0/26 bağımsız kabul.
- 22 ana görev: 0/22 bağımsız kabul.
- Hiçbir kaynak dosyası veya CI sonucu, canlı üretim davranışını tek başına kanıtlamaz.

## Güvenlik ve sonraki işler
- Üretim IPTV/EPG/favoriler/cihaz verileri/yedekler/arşivler değiştirilmedi; PR #71 birleştirilmedi; Actions tetiklenmedi.
- Sıradaki adım: güncel main'in kaynak/test snapshot'ını tutarlı biçimde dışa aktarıp hedefli grupları tekrar çalıştırmak; son başarılı CI SHA'sı ile main HEAD arasındaki farkı belirlemek; kalan CI failure loglarını ve 99 workflow/92 davranış sözleşmesini kanıtla incelemek.

## CI hata günlüklerinden kök neden doğrulaması
- En yeni incelenen başarısız Actions koşusu: `39861985074`, SHA `c40c765751aacde42c11cea32af9c12a85cc5c07`. Job logu: 958 test, `test_nfkc_normalization_precedes_protected_path_check` içinde tek failure; fullwidth `ａｒｔｉｆａｃｔｓ/report.json` yolunun reddedilmemesi.
- Bu CI SHA'sındaki `src/madsc_guard.py` NFKC normalize edip ardından kontrol ediyor, fakat orijinal yol ile normalize edilmiş yolun farklılığını reddetmiyordu. Böylece tam genişlikli `artifacts` bileşeni normalize sonrası izinli prefix'e dönüşebiliyordu.
- Güncel main bu açığı zaten kapatıyor: `7c2aae9d028bdebd5159a2f157141420b8cfc855` (`fix(k1): reject noncanonical Unicode output paths`) orijinal ve NFKC normalize edilmiş yol farklıysa `ValueError` fırlatıyor. Testi güncel main'de yeniden düzeltmeye çalışıp değişikliği tekrarlamadım.
- Karşılaştırma `c40c765... → main`: main 3 commit ileride; `src/madsc_guard.py` değişmiş. Güncel main için sonradan çalıştırılmış Actions sonucu henüz kanıtlanmadı. CI tekrar çalıştırılmadı.
- Eski failure'ın kök nedeni belirlendi ve mevcut main'de kodla giderilmiş; doğrulama için yeni CI sonucu bekliyor.

## K5 devam kontrolü — 2026-10-23
- Güncel main HEAD doğrulandı: fb4a738e1be8860acc9fcd508ec580511cfeb951.
- GitHub Actions run 39862185213, SHA fb4a738e1be8860acc9fcd508ec580511cfeb951: offline-tests başarılı.
- Job logu: tests_passed=true, all_offline_gates_passed=true.
- Aynı log açıkça production_acceptance=false, legacy_92_behavioral_acceptance=0, runtime_security_26_acceptance=0 raporluyor. Bu CI başarısı yalnızca offline regresyon ve izole kabul kapsamındadır; 92 workflow, 26 runtime kuralı veya üretim kabulü için kanıt sayılmaz.
- K1 noncanonical Unicode path testi Non-canonical Unicode output path hatasını açıkça bekleyecek şekilde güncellendi; bu değişiklik aynı başarılı run'ın kapsamındadır.
- Kaynak kodu/test kapısı için yeni hata görülmedi; kalan işler gerçek veri ve runtime kabul kanıtlarıdır. Üretim listeleri, EPG, cihaz verileri, yedekler ve eski depo değiştirilmedi.

## 23 Ekim 2026 — Güncel kod için CI başarı kanıtı doğrulandı
- Main HEAD bu not yazılırken `f7308de59eb3facc67095e769f8a57b9f1c43927`.
- GitHub Actions run `39862185213` başarılı ve test edilen SHA `fb4a738e1be8860acc9fcd508ec580511cfeb951`. Log çıktısı `tests_passed=true`, `five_stage_fixture_gate_passed=true`, `all_offline_gates_passed=true`, `five_stage_installation_inventory_passed=true`, `five_report_roundtrip_passed=true`; job conclusion success.
- Main ile bu başarılı SHA karşılaştırması: main 2 commit ileride, değişen dosyalar yalnızca `PROJE_HAFIZASI.md` ve `docs/HEPSI_BIRLESIK_DOGRULAMA_2026-10-23.md`; çalışma kodu/test dosyası değişmemiş. Bu nedenle mevcut main'in kod/test ağacı başarılı CI ile aynıdır, yalnızca notlar sonradan güncellenmiştir.
- CI raporu açıkça `runtime_rules_verified=false`, `legacy_92_behavioral_equivalence_verified=false`, `ibo_device_verified=false`, `external_restore_verified=false`, `production_ready=false`, `independent_execution_evidence=false` olarak kalıyor. Dolayısıyla bu başarılı koşu offline suite ve izole fixture kapılarını doğrular; üretim sertifikası veya eski 92 workflow eşdeğerliği değildir.
- Canlı üretim sistemine müdahale yapılmadı; Actions yeniden tetiklenmedi; PR #71 birleştirilmedi.
- Kabul sayaçları değişmez: 92 eski workflow 0/92, 26 güvenlik kuralı 0/26 bağımsız kabul, 22 ana görev 0/22 bağımsız kabul.

## Kalan somut öncelik
- 99 workflow'un salt kaynak envanteri mevcut `madsc/legacy_99_bulk_audit.py` tarafından kaynak SHA/bytes/komut/trigger/permissions/artifact satırlarıyla çıkarılıyor; ancak her workflow için eksik kanıt seti aynı: legacy execution, new execution, input/output comparison, side-effect comparison, failure/timeout comparison, reviewer approval. Bu yüzden 0/92 sayacı dürüstçe korunuyor.
- Sıradaki anlamlı iş, her workflow için ayrı bir behavior contract ve izole fixture kurmak; önce yan etkisiz/deterministik workflow'lardan başlayıp eski ve yeni çıktı/exit code/artifact/izin/timeout davranışını kıyaslamak. Canlı IPTV, EPG, cihaz ve yedek operasyonları için üretim izni/kanıtı olmadan çalıştırma yapılmamalı.


## 23 Ekim 2026 — K1 workflow envanterinde sembolik bağlantı koruması
- Yeni incelemede `madsc/workflow_consolidation.py` envanteri `Path.is_file()` ile kuruyordu; bu çağrı symlink hedefini takip edebilir ve beklenmeyen dış dosyayı workflow envanterine dahil edebilirdi.
- Envanter oluşturulmadan önce dizin girdileri listeleniyor ve herhangi bir sembolik bağlantı varsa `ValueError("Symlinked workflow entry")` ile fail-closed davranılıyor. Kod commit: `3d22c4ce3988357a6e38654a3c4cc5a9fe30cb17`.
- İzole regresyon testi eklendi: `tests/test_workflow_consolidation.py::test_symlinked_workflow_entry_rejected`, geçici dizinde dış dosyaya işaret eden workflow symlink'i oluşturur ve envanterin reddetmesini bekler. Test commit: `a25af57f4373299e25ced205bcea9bdb311b0f29`.
- Bu iki commit için test henüz çalıştırılmadı; başarılı CI iddiası yok. Actions dispatch yapılmadı.
- Üretim playlist/EPG/favori/cihaz/yedek/arşiv verilerine dokunulmadı; PR #71 birleştirilmedi.
- Kabul sayaçları değişmedi: 92 workflow 0/92, güvenlik 0/26, ana görevler 0/22. Önceki başarılı offline CI yalnızca kendi test ettiği SHA ve izole kapsam için geçerlidir.


## 23 Ekim 2026 — K1 symlink koruması için CI doğrulaması
- GitHub Actions run `39862697684` (`MADSC55 — Offline Unit Tests`) başarılı; test edilen SHA `483bce535b585e5c750b7cfa54b87fb9f578d72c`, yani K1 workflow inventory symlink koruması ve regresyon testinin eklendiği commit.
- Job `offline-tests` sonucu success; logda `tests_passed=true`, `five_stage_fixture_gate_passed=true`, `all_offline_gates_passed=true`.
- Mevcut main HEAD `930ba504fad8777622c7d00ad0ba90a208eb4ba7`; başarılı test SHA'sından sonraki değişiklikler yalnızca dokümantasyon/devir kaydı. Dolayısıyla kod ve test ağacı bu başarılı koşuyla aynıdır. Bu, offline suite için CI kanıtıdır; runtime/production kabulü değildir.
- Aynı CI raporu `runtime_rules_verified=false`, `legacy_92_behavioral_equivalence_verified=false`, `production_ready=false` olarak kalır.
- Kabul sayaçları değişmedi: eski 92 workflow 0/92, güvenlik kuralları 0/26 bağımsız kabul, 22 ana görev 0/22 bağımsız kabul.
- Canlı IPTV/EPG/favoriler/cihazlar/yedekler/arşivler değiştirilmedi; Actions yeniden tetiklenmedi; PR #71 birleştirilmedi.


## 23 Ekim 2026 — Eski workflow davranış sözleşmesi şablonu
- Eklendi: `docs/LEGACY_WORKFLOW_BEHAVIOR_CONTRACT_TEMPLATE_2026-10-23.json` (commit `8da05d2ad09b7fb2f1923b6f359cb878b8f68ff8`).
- Şablon; sabitlenmiş eski/yeni kaynak blob kimlikleri, tetikleyiciler, girdiler, sırayla komutlar, izinler, timeout/exit code, çıktılar/artifact'lar, kalıcı yan etkiler, ağ/destructive davranış, iptal/tekrar çalıştırma ve idempotency alanlarını içerir. İzole test planı ve iki taraftaki çalıştırma kanıtı, çıktı/yan etki/hata-zaman aşımı karşılaştırması ve bağımsız inceleme zorunludur.
- Şablon yalnızca inceleme başlangıcıdır; hiçbir workflow'a otomatik eşdeğerlik atamaz. 99 workflow için gerçek değerler kaynak dosyası ve kanıtlarla doldurulmalıdır. Canlı/üretim verilerine erişim, yetki olmadan yasaktır.
- Bu commit dokümantasyondur ve `[skip ci]` kullanılmıştır; yeni test koşusu oluşmadı. Önceki başarılı Actions run `39862697684` SHA `483bce535b585e5c750b7cfa54b87fb9f578d72c` için geçerlidir, yeni dokümantasyon commit'ini test etmiş sayılmaz.
- Güncel workflow consolidation symlink kodu/testi commit'leri `3d22c4c` ve `a25af57` için ayrıca başarılı CI kanıtı henüz yoktur.
- Kabul sayaçları değişmedi: 92 legacy 0/92, güvenlik 0/26 bağımsız kabul, ana görevler 0/22.

## K5 devam — Legacy davranış incelemesi Batch 05 (2026-10-23)
- İncelenen üç kaynak workflow: altinci-aday-tekrar-test.yml, birlesik-aday-raporu.yml, genel-aday-medya-test.yml.
- Ayrıntılı sözleşmeler docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_05_2026-10-23.md dosyasına kaydedildi.
- Kümülatif statik kaynak incelemesi: 15/92; davranışsal kabul 0/92 (sayaç değiştirilmedi).
- Birleşik rapor workflow'unda cache restore key var; ancak bu tek başına yeni geçmişin sonraki çalıştırmaya kaydedildiğini kanıtlamaz. İki çalıştırmalı cache persistence testi açık.
- Altıncı aday tekrar testinde due schedule, en fazla 5 aday, HLS doğrulaması ve hata sonrası artifact davranışı; genel medya testinde ilk 30 aday, 6 worker, 16s ffprobe timeout ve zorunlu artifact kabul kanıtı gerektiriyor.
- Önceki EPG fix commit 483bce535b585e5c750b7cfa54b87fb9f578d72 için run 39862697684 başarılı. Ayrı test commit c865c1a5 başarısız olmuştu; bu yüzden kod commit'i başarılı olan run ile doğrulandı, test commit'i için regresyonun tekrar ayrıca onaylanması gerekir.
- Production acceptance false; 92 eski workflow, 26 runtime güvenlik kuralı ve 22 ana görev kabulü açık.

## Düzeltme — birleşik aday raporunda kararlılık geçmişinin kaydedilmesi
- Eski kaynak depodaki `.github/workflows/birlesik-aday-raporu.yml` incelendi ve somut bir eksik doğrulandı: workflow geçmişi `actions/cache/restore@v4` ile geri yüklüyor, `scripts/kanal_kararlilik_takip.py` dosyayı güncelliyor, ancak aynı workflow içinde cache/save adımı yoktu.
- Düzeltme kaynak depoya kaydedildi: `Madsc55/madsc-tv` commit `ad57ba6eca0f06cef3f31dddf1563f367d197c04`. `Stability evidence` adımından sonra `actions/cache/save@v4` eklendi; `KARARLILIK_GECMISI.json`, `kanal-kararlilik-${{ github.run_id }}` anahtarıyla kaydediliyor. Böylece sonraki çalıştırmanın `kanal-kararlilik-` restore prefix'iyle bu geçmişi bulabilmesi amaçlanıyor.
- Kaynak commit `ad57ba6eca0f` için Birlesik Aday Onay Raporu run `39863242921` tetiklendi ve son kontrolde queued durumundaydı; cache'in iki ardışık çalıştırmada gerçekten geri yüklenmesi henüz doğrulanmadı.
- Bu değişiklik donmuş karşılaştırma tabanı `ca374df3b9585c0d76a078db9536150ebbc260f7` üzerinde bir sonraki kaynak revizyonudur; baseline içeriği geriye dönük değiştirilmedi. Davranışsal parity kabulü bu nedenle hâlâ 0/92.
