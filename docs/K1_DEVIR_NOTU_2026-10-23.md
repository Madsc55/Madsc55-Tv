# K1 DEVIR NOTU — 23 Ekim 2026

## Yeni sohbet için görev
K1 (güvenlik, dosya yazma kapısı, mutation callsite AST envanteri, izinler, runtime kabul) çalışmalarına kaldığı yerden devam et. Kullanıcı tekrar tekrar “K1 de kalan yapılması gereken her şeyi yap hataları düzelt” dedi. Gerçek kod/test düzeltmeleri yap, sadece durum raporu verme.

## Depo ve sınırlar
- Yazılabilir depo: https://github.com/Madsc55/Madsc55-Tv ; dal: main.
- Diğer K2–K5 ekipleri main üzerinde eşzamanlı çalışıyor. Her dosyayı yazmadan hemen önce güncel SHA ile çek; 409 conflict halinde yeniden çekip birleştir.
- K1 alanında kal: madsc/write_path_audit.py, madsc/write_callsite_audit.py, tests/test_write_path_audit.py, tests/test_write_callsite_audit.py ve K1 notları.
- Üretim playlistlerine, EPG, logo, arşiv, favori ve yedeklere dokunma: CALISANLAR, YENILER, YEDEKLER, HEPSI, FAVORILER, playlist.m3u8, xmltv.xml vb.
- GitHub Actions manuel dispatch/rerun ve üretim yazımı ayrı açık yetki olmadan yapma. Önceki K1 commit mesajları [skip ci] içeriyordu.
- tools/protected_write_gate.py korunan .m3u/.m3u8 dosyalarını engelliyor; legacy workflow çatışmasını gate gevşeterek aşma. docs/K1_KORUNAN_YAZMA_KAPISI_CELISKI_2026-10-22.md dosyasını incele.
- Statik/offline test başarısı, 26 gerçek runtime güvenlik kabul kontrolünün kanıtı değildir. K1'i bu kanıtlar olmadan tamamlandı sayma.

## Bu sohbetlerde K1 için yapılanlar
AST tarayıcısı: definition-time/lambda default mutation taraması, xattr/special-file API, dynamic os.open flags, starred open modes, FIFO .py dosyalarını reddetme, shutil copymode/copystat/copyfileobj, os.sendfile/copy_file_range/splice, os.spawn*/posix_spawn*, os.exec* aileleri, csv writerow/writerows/writeheader, metadata setxattr/removexattr/utime ve ilgili regresyon testleri.
Yol koruması: Unicode NFKC uyumlu slash/backslash alias engelleme, C1 Unicode kontrol karakterleri, U+2028/U+2029 satır/paragraf ayraçları ve yerel çıktı yollarında belirsiz karakterleri reddetme; ilgili regresyon testleri.
Önemli son commitler:
- d72b1c2 os descriptor transfer yazma çağrıları
- 90ed6c7 descriptor transfer testleri
- fc69ae6 OS spawn/posix_spawn envanteri
- b907bb6 spawn testleri
- 4cef6e0 os.exec ailesi
- 0efef7a exec testleri
- 6ba3722 serializer/metadata metotları
- 7049a67 serializer/metadata testleri
- 5e1e131, d8451a7, 4a415e8 Unicode path separator düzeltmeleri
- 8d2d9f2 Unicode separator testi
- e3bdc0c Unicode Cc kontrol karakterleri
- b15d312 C1 testi
- f2dbd62 Unicode Zl/Zp koruması
- f76a664 Zl/Zp testi
- 13939a2 yerel çıktı karakterleri koruması
- 1c03ef0 yerel çıktı testi

## En son doğrulama
23 Ekim 2026, yaklaşık 10:21 (+02:00) sonrasında GitHub Actions sorgusunda:
- 39924407034, SHA 7f0e0187, success.
- 39924305569, SHA 34100654, failure.
Bu CI'ların son K1 commitlerini kapsadığını varsayma; SHA karşılaştır.
Önceki başarılı koşular: 39924099937, 39924060060, 39924018905. Bir önceki başarısız CI'da K3 kaynak içe aktarma testinde unmatched quote/comma hatası görülmüştü; K1 dışına müdahale etmeden logları kontrol et.
Son K1 dosya SHA'ları kontrol edildiğinde:
- madsc/write_path_audit.py blob da917df1323990ac2781429acfc568887d804f1e (son değişiklik 13939a2)
- tests/test_write_path_audit.py blob 75383df836c55e5a5a82f667a6e8c166878770a3 (son değişiklik 1c03ef0).
Yeni sohbette bunları yeniden çek; main ilerliyor.

## Kalan işler
1. Güncel main HEAD, son CI run/job/log ve K1 testlerinin sonuçlarını doğrula; hata varsa kaynağını ayır.
2. K1 guard ve AST audit kodunda gerçek eksikleri incele; güvenlik açığı bulunca kod+regresyon testi birlikte düzelt.
3. Korunan yazma kapısının gerçek workflow davranışıyla çelişkisini onay olmadan production'a dokunmadan belgeleyip güvenli çözüm tasarla.
4. K1 runtime 26 kabul kontrolü için gerçek ortam kanıtları topla; yoksa eksik olarak açıkça belirt.
5. Diğer K sistemlerinin değişikliklerini koru; her commit SHA ve CI kapsamını dürüst raporla.

## GitHub connector
functions.exec ile tools.mcp__GitHub__fetch_file({repository_full_name:"Madsc55/Madsc55-Tv",path}), update_file({repository_full_name,path,sha,branch:"main",content,message:"... [skip ci]"}), fetch({url:"https://api.github.com/repos/Madsc55/Madsc55-Tv/actions/runs?per_page=5"}). GitHub connector kullan; yerel git network erişimi varsayma.


## EK DEVİR — 23 Ekim 2026, son sohbet
Kullanıcı yeni sohbete geçmek için tüm ilerlemeyi not almamızı istedi. Önceki bölümlerdeki daha eski CI durumunun yerine aşağıdaki güncel durum kullanılmalı.

Bu sohbetin K1 kod ve test commitleri:
- 4b59190444c8f5410d8f69f8c351a68cb311ae8b: allowed_root lexical traversal, kontrol karakteri ve Unicode noncharacter reddi.
- d6770782e0596aa55554274c0f34e4294194e89d: allowed_root regresyon testi.
- 492307bfe8e34df642570b0e2e45f3b47bebc8a7: K3 izole deneme playlist istisnasında relative/traversing root reddi.
- 9dbbe4ad619ce71a4452130ce43af2ef722718d7: bu davranışın testi.
- fd865bad12ceb340f5bb846a423ac55416d4d8c7: izole playlist hedef yolunda lexical traversal reddi.
- a44f2bb10fcfaf9620590185559c52d8d70f3ef9: bu davranışın testi.

CI doğrulaması: 39959033394 success, SHA 5c9951cfc7776755f0b368424d6aa5ee768da9b3; a44f2bb bu commitin atasıdır. Ancak son sorguda 39959626099 (fa7b9d3c) FAILURE, 39959609860 (e330de54) FAILURE, 39959574944 (cad3c38f) SUCCESS. Yeni sohbette önce güncel main SHA'yı ve başarısız koşuların jobs/logs'unu kontrol et, ilgili sorunu izole biçimde düzelt. Bu sonuçlar yalnızca ilgili commitleri doğrular.

K1 için halen kanıt bekleyenler: 26 gerçek runtime güvenlik kabulünün tamamı (son bilinen 0/26), tüm gerçek yazma callsite'larının zorunlu K1 gate kapsamına alınması, K2 92 legacy workflow davranışsal eşdeğerliği (son bilinen 0/92), K4 bağımsız harici yedek ve restore, genel 22 kabul (son bilinen 0/22). production_ready=false korunmalı; kanıt olmadan yükseltilmemeli.

Sınırlar: çalışan 1.039 IPTV kanalına, M3U, EPG, logo, favori, VOD, arşiv, yedek ve cihazlara dokunma; legacy depo read-only; PR #71 merge etme; Actions manuel dispatch/rerun yapma; sadece güvenli izole kod/test değişiklikleri ve [skip ci] commit. Diğer K2–K5 ajanları aynı main üzerinde eşzamanlı olabilir.
