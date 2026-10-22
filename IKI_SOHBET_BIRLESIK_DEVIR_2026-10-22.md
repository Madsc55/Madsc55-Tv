# MADSC55-TV — İki sohbetin birleşik devir kaydı (22 Ekim 2026)

## Kaynak ve çalışma ilkesi
- Kanonik depo: `Madsc55/Madsc55-Tv`, `main`. Bu not hazırlanırken başlangıç HEAD: `ec0d253ad70233686094a6cd34d1ba94da730603`. **Yeni sohbette ilk iş HEAD'i tekrar oku.**
- İki sohbet de aynı `main` üzerinde ilerledi. Git geçmişi birleşiktir; sohbet metinleri otomatik olarak birleştirilmiş değildir. İlerleme için `DEVAM_NOTU.md`, `PROJE_HAFIZASI.md` ve bu notu beraber oku. Eski sohbetlerdeki her ayrıntının eksiksiz taşındığını varsayma.
- Eşzamanlı düzenleme riski: her dosya yazımından önce güncel `main` ve blob SHA oku, SHA ile güncelle, çatışma olursa tekrar oku ve uzlaştır. Tamamlanmış özelliği tekrar yazma. Kullanıcı artık tek yeni sohbette devam etmek istiyor.
- Eski `Madsc55/madsc-tv` yalnızca okunur; eski repo veya PR #71 **birleştirilmez**. Canlı kanal listeleri, EPG/XMLTV, YEDEKLER, YENİLER, FAVORİLER, cihaz favorileri, logo/arşiv ve diğer korunan üretim verileri **değiştirilmez**.
- İzinsiz Actions dispatch/rerun, canlı probing veya cihaz testi yapma. Commit mesajlarında `[skip ci]` kullan.

## İki sohbetin birleşik teknik ilerlemesi
- 99 workflow envanteri, 92 eski otomasyon ve K1–K5 izole kapıları için kaynak/statik doğrulama çalışmaları; 26 güvenlik kuralı ve 22 görev envanteri mevcut. Statik envanter kabul yerine geçmez.
- K1/K4/K5 opt-in parity workflow entegrasyonu, input SHA256 kontrolü, snapshot/manifest/receipt zinciri, başarısız tüketici tanı artifact yüklemesi ve güvenli çıkış kodu koruma geliştirildi.
- `madsc/parity_consumer_cli.py` ve süreç gözlemleyici kontrollü gerçek timeout ile stdout/stderr/outcome ölçüyor; normal exit 124 otomatik timeout sayılmıyor. Sert GitHub job timeout veya runner kaybında artifact garantisi yok.
- `madsc/legacy_pair_artifact.py` içinde diagnostic ZIP baytları, SHA256, üyeler, outcome ve snapshot semantiği; `madsc/github_legacy_pair_client.py` içinde GitHub run/artifact/workflow blob kökeni doğrulaması bulunuyor. Bu, gerçek eski/yeni davranışsal eşdeğerlik kabulü değildir.
- Diğer sohbetten `tests/test_diagnostic_outcome_strictness.py` commit `71ba4aeb3e79456855ac8392b09ee9fe3740f0d3` (duplicate JSON keys, timeout conclusion ve consumer identity olumsuz testleri).
- Bu sohbetten `tests/test_failure_diagnostic_api_fail_closed.py` commitleri `2aa79162627663cb8b11c7efbaba2765a47dfc34`, `2345cb166509786459366d88be9cd428ef2e1985`, `e34b9481c888173f7b943c4ff05f959040bfdef5`: 12 API olumsuz alt senaryo (run attempt, run ID, head SHA, digest, missing/duplicate/expired artifact, workflow blob SHA, listing count, run status/conclusion/repository).
- Son **kayıtlı ve o kaynak sürümüne ait** `python -m madsc.offline_gate`: 632 test ve beş K1–K5 izole kapısı başarılı. Sonraki iki sohbet commitlerinin tamamı için tam suite **yeniden çalıştırılmadı**. GitHub checkout denemelerinde DNS (`Could not resolve host: github.com`) engeli vardı; GitHub connector üzerinden dosya/commit işlemleri mümkün oldu.

## Gerçek kabul ve sıradaki işler
- Davranışsal kabul **0/92**, güvenlik kabulü **0/26**, görev kabulü **0/22**. Kanıt olmadan artırma veya üretim hazır deme.
- 1. Yeni HEAD'den iki sohbetin test dosyalarını ve kanıt modüllerini oku; `python -m unittest tests.test_failure_diagnostic_api_fail_closed tests.test_diagnostic_outcome_strictness -v` ve `python -m madsc.offline_gate` erişilebilir checkout üzerinde çalıştır. Başarı iddiası yalnız gerçek sonuçla.
- 2. Diagnostic ZIP + GitHub API doğrulayıcılarında kalan negatif sınır durumlarını, dosya boyutu, bağımsız run/artifact kökeni ve workflow step davranışıyla karşılaştır. Var olan kapsamı tekrar üretme.
- 3. Aynı girdi için eski/yeni **bağımsız gerçek çalışma** ve artifact çiftlerini doğrula; dış kanıt yoksa kabulü bloke tut. K2/K3 gerçek dış kaynak blokajlarını ayrıca kaydet.
- 4. Her anlamlı değişiklikte devir/hafıza notlarını güncelle; GitHub main ve dosya SHA çakışmalarını izle.

## Yeni sohbet için tek komut
“`Madsc55/Madsc55-Tv` `main` dalında `IKI_SOHBET_BIRLESIK_DEVIR_2026-10-22.md`, `DEVAM_NOTU.md` ve `PROJE_HAFIZASI.md` dosyalarını oku. İki sohbetin birleşik HEAD'inden devam et. Çakışma kontrolü yap, son testleri gerçek ortamda çalıştır, eksikleri düzelt, [skip ci] ile kaydet. Korunan yayın dosyalarına ve eski depoya dokunma; PR #71'i birleştirme; izinsiz Actions başlatma; kabulü kanıtsız artırma.”

## Nihai birleştirme teyidi — diğer sohbet tamamlandı
- Kullanıcı diğer sohbetin çalışmasının bittiğini teyit etti. Son GitHub HEAD kontrolünde `ccda375bde9e6e06650dc14b64a726346c6bb135` görüldü; daha yeni başka sohbet commit'i henüz görünmüyor. Herhangi bir eksik sohbet mesajının otomatik taşındığı iddia edilmez.
- `DEVAM_NOTU.md` diğer sohbetin `71ba4ae` diagnostic outcome strictness testlerini ve bu sohbetin `e34b948` API run-state testlerini birlikte içeriyor. Bu belge ikisini de kapsar; hiçbir eski değişiklik üzerine yazılmadı.
- Yeni sohbette artık **tek kanonik çalışma akışı** kullan: önce güncel HEAD'i oku, bu belgeyi ve iki ana notu oku, yeni testleri gerçekten çalıştır, kanıt yoksa kabulü değiştirme. Mevcut test engeli ve 0/92, 0/26, 0/22 sınırları aynen geçerlidir.
