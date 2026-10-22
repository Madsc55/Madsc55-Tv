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


## 23 Ekim 2026 — K1 trust-boundary genişletmesi
- İnceleme, önceki symlink kontrolünün `.github/workflows` dizinine ve tek tek girdilere baktığını; ancak depo kökü veya `.github` bileşeni symlink ise dizin dışına yönlendirme ihtimalini ayrıca kapatmadığını gösterdi.
- `madsc/workflow_consolidation.py` artık kök yolun symlink olmamasını, `.github` dizininin symlink olmamasını ve `.github/workflows` dizininin gerçek dizin olmasını da doğruluyor. Kod commit: `b1cf07e9bd000ebb638e191fc3bb2ae13893442c`.
- `tests/test_workflow_consolidation.py::test_symlinked_github_directory_rejected` eklendi; `.github` bileşeninin dış dizine yönlendirildiği geçici fixture'da fail-closed davranışı sınar. Test commit: `9a9c94f13ac7ac2552e33a3f5f367366f1d88c7f`.
- Test henüz çalıştırılmadı; bu değişiklikler için başarılı CI kanıtı yok. GitHub Actions dispatch yapılmadı.
- Son bilinen başarılı Actions run `39862697684` SHA `483bce535b585e5c750b7cfa54b87fb9f578d72c` üzerinde; yeni K1 trust-boundary değişikliği bu run'da yer almıyor.
- Kabul sayaçları değişmedi: 92 eski workflow 0/92, 26 güvenlik kuralı 0/26, 22 ana görev 0/22. Üretim verilerine müdahale edilmedi; PR #71 birleştirilmedi.


## 23 Ekim 2026 — K4/K1 offline CI kök neden düzeltmeleri
- Başarısız Actions run `39863302393` (SHA `38c2a467021235169ba616ae0d0f3e1286021ae9`) 970 test çalıştırdı ve 4 hata verdi.
- Üç backup testindeki kök neden: `backup_to_new_sandbox` hata rollback'inde `created_identity` kullanıyor ama destination dizini yaratıldıktan sonra bu kimlik hiç kaydedilmiyordu; asıl integrity ValueError hatasını NameError maskeliyordu. `madsc/backup.py` artık `destination.mkdir()` sonrası lstat ile (st_dev, st_ino) kimliğini kaydediyor ve yalnızca o dizini geri alıyor. Commit `42b72c462681b40543c2e91db816d1657730fcf1`.
- Dördüncü hata: fixture raporu rollback'i eşzamanlı değiştirilmiş dosyayı sadece device/inode ile tanıyordu; unlink/recreate sonrası inode reuse halinde başka işlem tarafından oluşturulan kanıtı silebilirdi. Temizleme artık device, inode, size, mtime_ns ve ctime_ns alanlarını birlikte karşılaştırıyor. Commit `a20a3159c1b6ab6d36d1656ddbbcaf1080401dbd`.
- K1/K4 kod değişiklikleriyle offline CI otomatik tetiklendi: run `39863482320`, commit `0d25b09bdc2d3e029c368376e700d7c14ced9ab3`; yazım anında queued. Sonucu gelmeden başarılı sayma.
- Bu iki düzeltme canlı dosyalara değil, rollback ve izole test verilerine ilişkindir. Üretim IPTV/EPG/favori/cihaz/yedek/arşiv verileri değişmedi; PR #71 birleştirilmedi.
- Kabul sayaçları değişmez: 92 workflow 0/92, 26 güvenlik kuralı 0/26, 22 ana görev 0/22.

## K5 devam — kararlılık geçmişi timestamp güvenliği (2026-10-23)
- Önceki birleşik aday raporu workflow düzeltmesi `Madsc55/madsc-tv` commit `ad57ba6eca0f06cef3f31dddf1563f367d197c04` için run `39863242921` başarıyla tamamlandı. Bu doğrulama workflow run'ın başarıyla bittiğini gösterir; cache'in sonraki run'da gerçekten restore edildiği henüz ayrı bir iki-run testiyle doğrulanmadı.
- Kaynak incelemesinde ek mantık hatası bulundu: geçmiş filtresi `age <= 7 days` kullanıyordu; gelecek tarihli gözlemde age negatif olduğu için kabul edilebiliyordu ve kararlılık aralığını yapay olarak uzatabilirdi. Saat dilimi olmayan timestamp'ler de güvenli biçimde ayrıştırılmıyordu.
- Düzeltme: `scripts/kararlilik_gecmis.py` içindeki `normalize_history()` yalnızca timezone-aware, geçmişte ve son 7 gün içinde olan gözlemleri tutuyor; bozuk/naive/future/eskimiş kayıtları hariç bırakıyor. Tracker bunu kullanıyor.
- Regresyon testleri `tests/test_kararlilik_gecmis.py` dosyasına eklendi (gelecek, naive, bozuk, eski, UTC offset ve 7 günlük sınır). Birleşik rapor workflow'una bu testleri ffmpeg kurulumu ve canlı aday işlemlerinden önce çalıştıran kapı eklendi.
- İlgili kaynak commit'leri: `f5ad1c7816f2722c9618f8a099462abce90e294d`, `2fbe6a0f5299ab120fc236bd10152f34222b08f4`, `d143692c78fc1b8748ad53778a37ec9587ac0c11`, `4a0d38c390d343299e289e03a558fca1e08a9d01`, `796ce918399e1cea60c44d3d856f0ec8187bd419`.
- Run `39863524500` (unified report workflow) queued at last check; run `39863499174` (stability tracker) in progress. Test result not yet confirmed. No behavioral acceptance counters changed; legacy 92 parity remains 0/92, runtime security 0/26, main task acceptance 0/22.


## K1–K5 devamı — K4 rollback hataları ve CI yeniden doğrulaması
- Run `39863302393` 970 test çalıştırdı; 4 hata: K4 backup/restore rollback testlerinde üç hata `backup_to_new_sandbox` içinde tanımsız `created_identity` nedeniyle gerçek integrity hatasının NameError ile maskelenmesi; K1 fixture report writer testinde eşzamanlı değiştirilmiş dosyanın rollback sırasında silinmesi.
- K4 düzeltmesi commit `42b72c462681b40543c2e91db816d1657730fcf1`: yeni sandbox backup dizini oluşturulduktan sonra lstat identity kaydedilir, başarısızlıkta yalnızca bu oluşturulan dizin rollback edilir.
- K1 düzeltmesi commit `a20a3159c1b6ab6d36d1656ddbbcaf1080401dbd`: rollback temizliği device/inode yanında size, mtime_ns, ctime_ns alanlarını da karşılaştırır; böylece eşzamanlı dosya replacement'ı korunur.
- İlk doğrulama CI koşusu `39863482320` yeni bir syntax hatası ortaya çıkardı: kaynak satırına gerçek satır sonu yerine literal `\\n` kaçışları girmişti. Bu hata commit `031a6978ce85d32256ab7dc800c9b7e57bac6189` ile düzeltildi.
- Ek regresyon assertion'ı `tests/test_fixture_report_writer.py` içine eklendi; güncel offline CI run `39863567977`, SHA `de82210cdea1281b8ad2d1f622925fa1d8d8c397`, kayıt anında in_progress. Sonuç gelmeden başarı kabul edilmez.
- Üretim yedekleri veya canlı kaynaklar üzerinde işlem yapılmadı; bütün kopyalama/rollback testleri izole fixture'lara yöneliktir. PR #71 birleştirilmedi.
- Kabul sayaçları değişmedi: 92 workflow 0/92, 26 güvenlik kuralı 0/26, 22 ana görev 0/22.


## CI sonucu — K4/K1 rollback düzeltmeleri doğrulandı
- GitHub Actions run `39863567977` başarılı: [MADSC55 — Offline Unit Tests](https://github.com/Madsc55/Madsc55-Tv/actions/runs/39863567977).
- Test edilen SHA: `de82210cdea1281b8ad2d1f622925fa1d8d8c397`; `tests_discovered=970`, `test_exit_code=0`, `timed_out=false`, `tests_passed=true`.
- K1–K5 izole fixture kapısı, beş sistem kurulum envanteri ve beş raporun K5 roundtrip'i başarılı; rapor baytları korunmuş.
- Güncel main bu test SHA'sından 2 commit ileride; compare sonucu yalnızca `PROJE_HAFIZASI.md` ve bu devir dokümanında değişiklik olduğunu gösteriyor. Bu nedenle kod/test ağacı test edilen SHA ile aynı.
- CI raporu yine `production_acceptance=false`, `legacy_92_behavioral_acceptance=0`, `runtime_security_26_acceptance=0`, `production_ready=false` diyor. Bu offline test başarısı canlı üretim veya eski workflow eşdeğerliği kabulü değildir.

## Son offline CI kontrolü — 2026-10-23
- Run `39863567977`, commit `de82210cdea1281b8ad2d1f622925fa1d8d8c397`: GitHub Actions `offline-tests` job `120120030978` tamamlandı ve `success` oldu.
- Bu sonuç K1/K4 rollback güvenlik düzeltmeleri ve fixture test kapısı içindir; eski 92 workflow'un davranışsal eşdeğerliği, 26 runtime güvenlik kuralı veya gerçek üretim kabulü anlamına gelmez.
- Ayrı K5 kaynak deposu `Madsc55/madsc-tv`: cache-save workflow run `39863242921` başarılıydı. Tarih geçmişi normalizasyonu ve ek test kapısını içeren run `39863524500` son kontrol anında `in_progress`; run bitmeden K5 tarih düzeltmesi için CI kabulü verilmez.
- K5 yeni testleri: gelecekteki timestamp, naive timestamp, bozuk/eski kayıt, UTC offset ve tam 7 günlük sınır; bunlar ayrı unit-test kapısı olarak workflow'da ffmpeg kurulumu ve canlı keşiften önce çalıştırılıyor.
- Kabul sayaçları aynı kalır: legacy behavior 0/92, runtime security 0/26, independent main tasks 0/22. Production acceptance false.

## K5 devam — CI doğrulaması ve Legacy Batch 06 (2026-10-23)
- Birleşik aday raporu run `39863524500` tamamlandı: success. Job logunda cache restore `kanal-kararlilik-39863242921` anahtarından başarılı; tarih regresyon testleri 5/5 geçti; güncellenmiş `KARARLILIK_GECMISI.json` `kanal-kararlilik-39863524500` anahtarıyla kaydedildi. Bu run, bir önceki geçmişin restore edilip yeni anahtar altında kaydedildiğini doğrular; bir sonraki ayrı run'ın yeni anahtarı restore etmesi için ayrıca takip gerekir.
- Aynı run: `tests/test_kararlilik_gecmis.py` 5 test, tümü başarılı: future/naive timestamp reddi, naive `now` reddi, malformed/old/non-mapping kayıtları dışlama, timezone offset -> UTC ve tam 7 günlük sınır.
- Batch 06'da üç eski workflow incelendi: `besinci-zaman-asimi-test.yml`, `dokuzuncu-akilli-tekrar-test.yml`, `onikinci-hata-siniflandirma-test.yml`. Davranış sözleşmeleri `docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_06_2026-10-23.md` içinde. Kümülatif statik inceleme 18/92; kabul 0/92.
- Dokuzuncu scheduler kaynağında belirsiz bir davranış riski belgelendi: naive timestamp `astimezone(UTC)` ile runner'ın yerel timezone'una göre yorumlanıyor; testlerde sabit timezone ve naive timestamp politikası eklenmeden eşdeğerlik kabul edilmemeli.
- Batch 06 doküman commit'i `f66b1b2df807a9b71dfdb53b919395402b4f9d95`.
- Kalan kabul sayaçları değişmedi: 92 workflow 0/92; runtime security 0/26; independent main tasks 0/22; production acceptance false. Üretim playlist/EPG/cihaz/yedekleri değiştirilmedi.

## K5/legacy devam — Batch 06 ve scheduler timezone düzeltmesi (2026-10-23)
- K5 birleşik rapor run `39863524500` başarıyla tamamlandı. Log doğrulaması: önceki kararlılık geçmişi cache key `kanal-kararlilik-39863242921` üzerinden restore edildi; `tests/test_kararlilik_gecmis.py` 5/5 geçti; yeni geçmiş `kanal-kararlilik-39863524500` anahtarıyla kaydedildi. Bu kanıt bir restore→update→save çevrimini gösterir; yeni kaydedilen key'in daha sonraki ayrı run tarafından restore edilmesi takip edilmelidir.
- Batch 06: `besinci-zaman-asimi-test.yml`, `dokuzuncu-akilli-tekrar-test.yml`, `onikinci-hata-siniflandirma-test.yml` statik kaynak incelemesi tamamlandı; belge `docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_06_2026-10-23.md`, commit `f66b1b2df807a9b71dfdb53b919395402b4f9d95`. Kümülatif inceleme 18/92; davranışsal kabul 0/92.
- Yeni gerçek bug düzeltildi: `akilli_tekrar_test_takvimi.py` naive `last_seen` timestamp'lerini runner yerel timezone'una göre yorumluyordu. Artık timezone bilgisi olmayan tarih, deterministik olarak `now` kabul ediliyor; böylece erken/yanlış due retry tetiklenmiyor. Test `test_akilli_tekrar_test_takvimi.py::test_naive_timestamp_does_not_use_runner_local_timezone` eklendi.
- Kod commit `b1fb904f8e1219adc505bb03d04ad3d590d481af`; test commit `87debd64e6b46ff8abb116830d95e2cf836af5c9`. Actions runs `39863903611` ve `39863903615` queued; `39863891832` ve `39863892845` in progress (son kontrol). Bu değişiklikler için başarı sonucu henüz doğrulanmadı.
- Kabul sayaçları değişmez: 92 workflow 0/92, runtime security 0/26, independent main tasks 0/22; production acceptance false.
- Scheduler timezone fix doğrulandı: Dokuzuncu Geliştirme Testi run `39863903611`, SHA `87debd64e6b46ff8abb116830d95e2cf836af5c9`, job `test` başarılı. Önceki kod commit'i `b1fb904f` için aynı test run `39863891832` da başarılı. Beş aşamalı toplu denetim run `39863903615` son kontrolde hâlâ in_progress; bağımsız geniş denetim sonucu bekleniyor.


## K1-03 — Python dosya yazma noktalarının statik envanteri
- Eklendi `madsc/write_callsite_audit.py`: Python AST üzerinden yazma/değiştirme API adaylarını salt-okunur tarar; dosya yolu, satır, fonksiyon, API ve aynı kapsamda yazmadan önce tanınan K1 guard çağrısı bulunup bulunmadığını raporlar.
- Eklendi `tests/test_write_callsite_audit.py`: güvenli/korumasız write callsite'ları, iç fonksiyondan dış fonksiyona guard sızmaması, read-only open, pathlib.open yazma modu ve bozuk Python sözdiziminin fail-closed davranışı test edilir.
- `madsc/offline_gate.py` içine statik envanter kapısı eklendi; test koşusunda tarama hatası offline gate'i başarısız yapar. Rapor `write_callsite_inventory` alanında dosya ve callsite listesini, kapsam sınırlamalarını açıklar. Bu analiz statik kanıttır; runtime enforcement veya tüm çağıran zincirlerinin güvenli olduğunun kanıtı değildir.
- İlk envanter raporu 97 Python dosyası tarandığını ve 58 dosya sistemi mutasyon adayı bulduğunu gösterdi. O koşu bir regresyon testi beklentisi (pathlib.open positional mode) nedeniyle başarısızdı; scanner gate'in kendisi geçiyordu. `bcd8245` bu mode parsing hatasını düzeltti ve yeni Actions run `39864090233` başlatıldı; sonuç henüz alınmadı.
- Dosya: `madsc/write_callsite_audit.py`; test: `tests/test_write_callsite_audit.py`; gate: `madsc/offline_gate.py`. Davranış sözleşmesi/CI sonucuna göre yeni devir notu eklenecek.
- Kabul sayaçları değişmez: runtime K1 0/26; legacy 92 workflow 0/92; 22 görev 0/22. Canlı IPTV/EPG/favori/cihaz/yedek/arşiv verilerine müdahale edilmedi; PR #71 birleştirilmedi.


## K1-03 — AST envanteri CI'da doğrulandı; envanterden somut yazma sınırı düzeltmesi
- Run `39864090233`, SHA `bcd8245a143abb5a24fc05b244127f28876c2ce2`, conclusion success. `tests_discovered=979`, `tests_passed=true`, beşli fixture gate ve tüm offline gate'ler başarılı.
- Aynı gate `madsc/` altındaki 97 Python dosyasını taradı ve 78 dosya sistemi mutasyon adayı raporladı. Her satır `review_required=true`; bu 78 satırın tamamı gerçek disk yazması demek değildir: genel `.replace()` gibi dinamik alıcı metotlar belirsiz adaydır. Rapor guard sırasını aynı fonksiyon kapsamıyla sınırlı bir heuristik olarak belirtir; 47 satırda önceki guard görülmemesi 47 kanıtlanmış açık anlamına gelmez. Shell/subprocess ve alias yolları ayrıca incelenmeli.
- İncelemede somut K1-03 sıralama sorunu bulundu: `madsc/core.py::run`, korunan bir rapor yolu için `reports/` dizinini K1 yol politikasını kontrol etmeden önce oluşturabiliyordu. Artık `enforce_write_paths` önce tam hedef yol üzerinde çağrılıyor; rapor dizini oluşturulmadan önce mevcut üst dizinlerin symlink olmadığı da doğrulanıyor. Kod commit `808f3881d1094748ade65d1b3da92b6ba53f5d16`.
- Regresyon testi `test_protected_report_rejected_before_reports_directory_creation`, `reports/playlist.m3u8` isteğinin reddedildiğini ve `reports/` dizininin hiç yaratılmadığını kontrol ediyor. Test commit `fe82f2f000c54b1a5a2547f9cac6d06ba4faa1f8`.
- Yeni K1 core düzeltmesi/testi için run `39864306236` queued; sonuç bekleniyor. Son başarılı run `39864090233` yalnızca SHA `bcd8245...` ve ondan önceki kod için geçerlidir.
- Kabul sayaçları değişmedi: K1 0/26, legacy 92 0/92, 22 ana görev 0/22. Üretim playlist/EPG/favori/cihaz/yedek/arşiv verileri değişmedi; PR #71 birleştirilmedi.


## K1-03 — Yeni offline gate CI ve ikinci hedef-yol düzeltmesi
- Run `39864306236`, SHA `fe82f2f000c54b1a5a2547f9cac6d06ba4faa1f8`, başarılı: 980 test keşfedildi, tests_passed true, five-stage fixture ve tüm offline gate'ler true. K1 AST taraması 97 Python dosyası/78 mutation adayı bildirdi.
- `madsc/core.py::run` korunan rapor hedefinde dizin yaratmadan önce `enforce_write_paths` çağırıyor ve rapor kökü üst dizinlerini symlink açısından kontrol ediyor; regresyon testi korunan `reports/playlist.m3u8` için `reports/` klasörünün oluşmadığını doğruluyor.
- Aynı AST incelemesi K5 `madsc/isolated_playlist_bundle.py::export_isolated_previews` içinde hedef dizin yaratılmadan önce K1 path policy çağrısının olmadığını gösterdi. Artık hedefin tam mutlak yoluna `enforce_write_paths` çağrısı `destination.mkdir` öncesine eklendi. Regresyon testi `FAVORILER` hedefinin hiç yaratılmadığını kontrol eder. Kod commit `1d48c0f64ab95f78855a79a20deb3f3d027f08d1`; test commit `90ba1b993ab81830252f69b78a380167529fb1c3`.
- Yeni CI run `39864450322` queued; sonuç bekleniyor. Başarı gelmeden bu yeni değişiklik kabul edilmez.
- Açık sayaçlar değişmez: K1 0/26, legacy 92 0/92, 22 görev 0/22. Canlı playlist/EPG/favori/cihaz/yedek/arşiv verileri değiştirilmedi; PR #71 birleştirilmedi.


## K1-03 son doğrulama ve ilk somut legacy workflow sözleşmesi
- Run `39864450322` başarılı; test edilen SHA `90ba1b993ab81830252f69b78a380167529fb1c3`. 981 test keşfedildi, tests_passed true, all_offline_gates_passed true. K1 AST taraması 97 Python dosyası/78 mutation adayı buldu; bu adayların tamamı review_required olarak kalır.
- CI raporu üretim kabulünü false tutar; `legacy_92_behavioral_equivalence_verified=false` ve `production_ready=false`. Beşli offline gate yeşil olması gerçek üretim kabulü değildir.
- Legacy workflow kaynak çözümlemesi: `.github/workflows/madsc-documentation-check.yml` için `docs/legacy-workflow-contracts/madsc-documentation-check.json` oluşturuldu. Sabit kaynak blob SHA `0678a8a201eb194503f9097265fe37e68b1e4d3d`; manuel `workflow_dispatch`, `contents: read`, üç dosya nonempty kontrolü, iki literal marker grep'i ve `CALISANLAR.m3u` ilk satırında `#EXTM3U` kontrolünü sırasıyla tanımlıyor. Komutlar playlist'i değiştirmez; yalnızca header satırını okur.
- Eşdeğer replacement workflow kanıtlanmadı, legacy/yeni run yok, davranışsal kabul false. Bu sözleşme kaynak anlamını kaydeder; 92 sayacını artırmaz. İzole replacement daha sonra fixture checkout üzerinde tasarlanmalı, korunan gerçek playlist'i kullanmamalı.
- Güncel main test edilen SHA'dan sonra yalnızca proje hafızası ve doküman değişiklikleriyle ilerledi; çalışma kodu/test ağacı CI ile aynı.
- Açık kabul sayaçları: K1 0/26, eski 92 workflow 0/92, ana görevler 0/22. Üretim verileri korunuyor; PR #71 birleştirilmedi.


## K1-03 — Fixture bundle preflight sırası
- AST callsite taramasında `madsc/fixture_report_writer.py::_prepare_fixture_root` içinde `reports.mkdir()` korunan JSON sidecar path politikasından önce gerçekleşebildiği görüldü.
- Artık `reports/` yaratılmadan önce `reports/turkish-tv-batch-validation.json` hedefi `enforce_write_paths` üzerinden kontrol ediliyor. Sabit M3U8 companion kendi exact-name local guard'ını kullanmaya devam ediyor. Kod commit `f5a7c080e94c550fbd741829cf117bb676a2c342`.
- `test_protected_fixture_root_rejected_before_reports_creation` korunan `FAVORILER` kökünde işlem reddedilirken `reports/` klasörünün oluşmadığını test ediyor. Test commit `6e1916ac9f791a0441bcd9cf7eb431ff8a5c3e4a`.
- Test run `39864659684` queued; sonuç bekleniyor.


## K1-03 final CI doğrulaması — 982 test
- Run `39864659684`, test SHA `6e1916ac9f791a0441bcd9cf7eb431ff8a5c3e4a`, conclusion success.
- `tests_discovered=982`, `tests_passed=true`, `five_stage_fixture_gate_passed=true`, `all_offline_gates_passed=true`.
- K1 write-callsite scanner: 97 Python dosyası, 78 mutation adayı; scanner kapısı başarılı. Adayların her biri review_required. Bu statik sonuç runtime enforcement kanıtı değildir.
- Bu run, `madsc/core.py` korunan hedefte mkdir öncesi K1 guard'ını ve `madsc/isolated_playlist_bundle.py` protected destination reddini ve `madsc/fixture_report_writer.py` protected root reddini test ediyor. `test_protected_fixture_root_rejected_before_reports_creation` ile `reports/` klasörünün korunan root'ta oluşmadığı doğrulandı.
- Main bu test SHA'sından sonra yalnızca `PROJE_HAFIZASI.md` ve bu devir notuyla ilerledi; kod/test ağacı aynı.
- CI raporu `legacy_92_behavioral_equivalence_verified=false`, `production_ready=false` tutuyor. Kabul sayaçları: K1 0/26 bağımsız kabul; legacy 0/92; ana görev 0/22.
- K5 için `docs/legacy-workflow-contracts/madsc-documentation-check.json` eski workflow kaynak semantiğini sabit SHA ile belgeliyor, ama replacement ve yürütme karşılaştırması yok; davranışsal eşdeğerlik kabul edilmedi.


## K3/K4 güncel devam — 23 Ekim 2026
- K3 XMLTV eşleşmesinde yinelenen channel ID'ler ve eksik ID/root fail-closed: `madsc/trial_epg_matching.py` + `madsc/epg.py`; regresyonlar CI run `39865719002` içinde doğrulandı (982 test).
- K4 sandbox kopyalama hedef tarafı da dirfd/no-follow ile sertleştirildi: `madsc/backup.py::_create_relative_file_nofollow` root inode identity kontrolü, descriptor-relative nested mkdir, O_NOFOLLOW/O_EXCL dosya oluşturma kullanır. Symlink'li hedef alt dizin, root inode uyuşmazlığı ve backslash yolu testleri eklendi. Run `39865933101` SHA `a4c70f7277be8aad73cdd95d027115b7bcab469d` başarılı: 990 test, five-stage fixture gate true, all offline gates true, AST scan 97 dosya/75 aday.
- Run `39863892845` için GitHub API 404; sonucu doğrulanamıyor. Bu yüzden son erişilebilir sonuçlar kullanıldı.
- K3 gerçek HLS/ffprobe workflow'ları `workflow_dispatch` gerektirir; bu GitHub bağlantısında workflow dispatch aracı bulunmadığı için canlı pilot bu oturumda başlatılmadı. IBO Player Pro cihaz kabulü yok. K4 harici storage ve bağımsız dış restore kanıtı da yok.
- Üretim kabulü false; 92 workflow 0/92, 26 runtime güvenlik kuralı 0/26, 22 ana görev 0/22. Üretim playlist/EPG/favori/yedekler değişmedi; eski depo ve PR #71'e dokunulmadı.


## 23 Ekim 2026 — K5 legacy workflow batch 07 (salt-okunur kaynak incelemesi)
- Yeni kaynak inceleme belgesi: `docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_07_2026-10-23.md`; commit `bf2db8d7e19898a91f1d3ac70baa3cc765c6e4d9`.
- Frozen `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7` üzerinde üç yeni workflow incelendi: `automatic-png-logos.yml`, `birlesik-durum-raporu.yml`, `genis-kanal-tarama.yml`. Workflow SHA'ları kaynak envanteriyle eşleşti; eski depoya yazılmadı.
- K1/K5 için kritik bulgu: `scripts/automatic_png_logos.py` korunan `CALISANLAR.m3u` dosyasını doğrudan `playlist.write_text(updated,...)` ile yazıyor. Workflow sonrasında diff görürse `git restore -- CALISANLAR.m3u` çalıştırıyor; write-then-restore, protected path'e hiç yazmama garantisi değildir. Replacement parity, izole fixture kopyası ve sıfır protected-path write ile kanıtlanmalı. Bu eski workflow çalıştırılmadı; playlist değişmedi.
- Birleşik durum workflow'u snapshot JSON'ları üretir ve sadece generated health report yazar; tarihsel snapshot'ı canlı durum gibi sunmamalı. Geniş kanal taraması 9 public M3U kaynağı ve ffprobe kullandığı için gerçek ağ/probe işidir; fixture/parity amaçlı tetiklenmedi.
- Statik inceleme toplamı 21/92; statik inceleme bekleyen 71. Bu kabul değildir: davranışsal parity 0/92, runtime güvenlik 0/26, ana görev kabulü 0/22, production_ready=false.


## K1 — dinamik dosya modu ve harici komut kapsamı (23 Ekim 2026)
- AST yazma envanterindeki iki kapsam boşluğu için düzeltme eklendi: değişken positional/keyword `open` modu artık `[dynamic mode]` olarak işaretleniyor; `subprocess.run/call/Popen/check_call/check_output`, `os.system` ve `os.popen` çağrıları harici yan etki inceleme adayı olarak sayılıyor.
- Kod commitleri: `c6affc2824a1c8e5288da16eff853f7bb690e1ca`, `d6f1ce5c98c85658336198b542d0a7ccb65a6394`. Regresyon testleri: `2a0796ebe98b03db88905534c6546153dd92020a`, `cb0a046252e1a75d119ae12e0af6c76028b3379c`.
- Bu sınıflar inceleme adaylarıdır; subprocess çağrısının mutlaka yazdığı iddia edilmez. CI combined-status sorgusu henüz status/check döndürmedi; 990 testlik eski run yeni SHA'lar için kanıt sayılmaz.
- K1 0/26, legacy parity 0/92, ana görev 0/22 ve production_ready=false korunur. 75 adayın tümünün sınıflandırılması henüz tamamlanmadı.


## 23 Ekim 2026 — K2 M3U metadata kimliği fail-closed sertleştirmesi
- `madsc/discovery_batch.py` artık aynı `#EXTINF` satırındaki yinelenen metadata alanlarını (büyük/küçük harf farkı dahil) aday kabul etmek yerine `duplicate_metadata_attribute` parse hatasıyla reddeder; metadata alan adları küçük harfe normalize edilir.
- Kod commitleri: `a83211a36e9ad1dd1c6047b74888970ddc33b381` (yinelenen alanları reddetme), `b0ab88f2ab2043ecbd24620bd76066a0cd924b45` (metadata anahtarlarını normalize etme).
- Regresyon commitleri: `b4b13f9de4913af05f5ddcc21e714fff8227c667` (yinelenen alan), `75d1fa756a232d4ee594bb5ae28faa01abba931b` (büyük/küçük harf uyumu).
- Doğrulama sınırı: workflow `workflow_dispatch` ile tetikleniyor; bu oturumda dispatch aracı kullanılmadı. Combined-status sorgusu yeni test commitleri için sonuç döndürmedi. Bu nedenle testler CI'da başarılı sayılmaz; eski 990-test baseline bu yeni SHA'ları kapsamaz.
- Etki: belirsiz `tvg-id` çakışmasının sessizce son değerle ezilmesi engellenir; tekil büyük harfli `TVG-ID` alanı da tanınır. K2-05/06/07/08 kabul durumları değiştirilmedi; gerçek kaynak/lisans, günlük eşdeğerlik ve bağımsız artifact SHA kanıtı hâlâ açık.
- Üretim playlist/EPG/favoriler/yedekler değişmedi; eski `Madsc55/madsc-tv` deposuna yazılmadı; canlı kaynak veya IBO cihaz testi yapılmadı.


## K1 — izole kanıt yazıcısında TOCTOU/rollback sertleştirmesi (23 Ekim 2026)
- `madsc/fixture_report_writer.py::_exclusive_bytes` tam yolu doğrudan açmak yerine her üst dizini `O_DIRECTORY|O_NOFOLLOW` + `dir_fd` ile açıyor; hedefi açık parent descriptor üzerinden `O_EXCL|O_NOFOLLOW` ile oluşturuyor. Hata temizliği aynı parent fd içindeki aynı inode/metadata ile sınırlı.
- Kod: `967977def72e1f184c7e2920d323401f4afb035b`. Testler: `6d9624592a93a885fddd5aaccab2cfcc5f8f1d95` (fsync hatasında kısmi dosya temizliği), `32fd75b48d334068efe5687b085daeb86603a0b4` (symlink parent kaçışı).
- GitHub'da kod/test dosyaları doğrulandı; bu SHA'lar için CI sonucu henüz doğrulanmadı. Önceki 990 testlik baseline yeni değişikliklerin kanıtı değildir.
- Bu, paylaşılan izole rapor yazıcısını sertleştirir; repository çapında tüm yazma noktaları kapısı veya 26 kural kabulü değildir. K1 0/26, production_ready=false.


## 23 Ekim 2026 — K2 aynı içerikli kaynakların oy şişirmesini engelleme
- `madsc/discovery_batch.py::corroborate_sources` her feed gövdesi için SHA-256 fingerprint çıkarır; birebir aynı içerik farklı kaynak etiketleriyle verilse bile `source_count` değerine yalnız bir oy ekler. Etiketler raporda görünür kalır; bu mekanizma yalnız birebir aynı gövdeyi saptar, farklı biçimlenmiş kopyaların bağımsızlığını kanıtlamaz.
- Kod commit: `3ea2415ba29b08994c892dca2cdcfd23b42bd9e5`. Regresyon testi commit: `70433a0079dff063187ce5c094cd5c70d4f828be`.
- CI durumu henüz doğrulanmadı; workflow dispatch aracı kullanılmadı ve yeni SHA için combined-status sonucu boş. Bu nedenle testler geçmiştir denmiyor. Sonraki iş: kaynak URL/kurum kökenini gerçek kanıtla modellemek ve yalnız farklı, doğrulanmış kökenleri bağımsız oy saymak.
- K2 kabul sayaçları değiştirilmedi; gerçek kaynak/lisans, günlük keşif eşdeğerliği ve artifact SHA kökeni açık. Üretim playlist/EPG/favoriler/yedekler ile eski depo değişmedi.


## K1 — AST open()/os.open() yanlış sınıflandırma düzeltmesi (23 Ekim 2026)
- Generic `*.open` dalı unqualified `open(path, mode)` için mode index 0 kullanabiliyor, `os.open(path, flags)` ise generic dalda erken dönüp flags denetimini atlayabiliyordu. `os.open/posix.open` şimdi ayrı ve önce inceleniyor; builtins/io/unqualified open mode index 1, Path.open mode index 0. Keyword `flags=` da ele alınıyor.
- Kod commitleri: `ccf5bfea56c9ebbd741d28afa9ed97482c57f513`, `5138e550e9ac2cba2cd7f8eec016a7c018aad999`. Test commit: `4eacdf0f70d7fb1bf0391a015216bde64e8516c3`.
- CI henüz doğrulanmadı; K1 kabulü 0/26 ve 75 adayın tamamının kapatıldığı iddia edilmiyor.


## 23 Ekim 2026 — K2 kaynak fingerprint biçim normalizasyonu
- `corroborate_sources` artık feed fingerprint'ini üretmeden önce UTF-8 BOM'u, CRLF/LF farkını, boş satırları ve satırların dış boşluklarını normalize eder. Aynı içeriğin yalnız aktarım biçimi değişti diye bağımsız kaynak oyu sayısı artmaz.
- Kod commitleri: `c1d29af73cbc0a08c82d93d31d8d83b8508986c9` (ilk normalizasyon), `3696f2c0221c1c571ec145b2fa2e97fdf07d9399` (kaçış düzeltmesi). Test commit: `e8eb0b34e60b612dc0d09b096dafa1e0123eaead`.
- Güncel dosya blobları yeniden okundu; canonical fingerprint kodu ve LF/CRLF+BOM regresyon testi depoda mevcut. Bu, yerel test çalıştırması veya CI başarısı değildir. CI combined status yeni test SHA'sı için boş; manuel workflow dispatch yapılmadı.
- Sınır: semantik olarak yeniden yazılmış feed kopyaları veya farklı URL'lerle yayımlanan aynı kaynak hâlâ gerçek kaynak URL/kökeni ile çözülmelidir. K2 gerçek kaynak/lisans, günlük keşif parity ve bağımsız artifact SHA kabulü açık kalır. Üretim dosyaları ve eski depo değişmedi.
