# K3 kanal testi — devir notu (22 Ekim 2026)

## Sorumluluk ve koordinasyon
Bu sohbet yalnızca K3 kanal testleri ve ilgili K2→K3 kanıt bağlantısı üzerinde çalışır. K1/K5, K2/K4 ve beşli sistemin diğer sohbetlerinin dosyalarına dokunulmaz. Korunan üretim playlist, EPG, logo, favori, kanal listesi, arşiv ve yedek dosyaları değiştirilmez. PR #71 birleştirilmez. GitHub Actions canlı görevleri tetiklenmez; DNS veya canlı ağ ayarları değiştirilmez.

## Yapılanlar — GitHub commit'leri
- 7bcd162: Süreklilik ölçümleri 20.000 örnekle sınırlandı; ölçüm SHA256 anahtarları doğrulandı.
- 8c039a6: Limit ve hatalı SHA256 regresyon testleri.
- 052afce: K2 aday zarfı ile K3 üç aşamalı süreklilik raporu bağlandı.
- 5ac1d4c: Bağlantı ve yabancı kanıt reddi testleri.
- 99754e3: K3 rapor CLI'sına --continuity girişi eklendi; --probes ile karşılıklı dışlayıcı.
- 5cb58aa: CLI sözleşmesi ve mükerrer aday regresyon testleri.
- 16681cc: RFC3339 tarih biçimi kontrolü eklendi.
- 0ddce8d: Tarih biçimi regresyon testi.
- e45b0bc: RFC3339 regex kaçış hatası düzeltildi.
- 67f68ef: K2→K3 başarılı süreklilik örneğinde altı saatlik aşama aralığı düzeltildi.
- aa3293b: K3 zaman aralığı testleri ve 12 saatlik toplam pencere beklentisi güncellendi.
- 3fa0cc8: Saat dilimi normalizasyonu ve başarısız orta aşama testleri eklendi.

## Güncel kod sözleşmesi
- madsc/channel_test.py: evaluate_probe, evaluate_repeated_probes, evaluate_ffprobe_json, summarize_offline_probe_evidence, evaluate_three_stage_continuity, summarize_candidate_continuity.
- madsc/candidate_probe_link.py: link_candidate_probes, link_candidate_continuity ve izole rapor üreten CLI.
- Üç veya daha fazla örnek; her ardışık aşama arasında en az altı saat; RFC3339 saat dilimi; aynı kanal SHA256; tüm aşamalarda ön teknik geçiş.
- Bu raporlar **yalnızca offline, sağlanan kanıtın ön değerlendirmesidir**. Gerçek ağ kökeni, akış sürekliliği, kanal kimliği, IBO cihaz testi veya üretim onayı kanıtlanmış değildir.

## Test ve kabul durumu
Son görülen başarılı GitHub Offline Unit Tests çalışması 39800980208, HEAD 3edbb863 sürümüne aitti; yukarıdaki son K3 commit'lerini doğrulamaz. K3 testlerinin güncel HEAD üzerinde gerçekten çalıştırılması gerekiyor. Geçmiş 800/800 sayısı da güncel HEAD için kabul edilemez.
75 adayın gerçek ağ ölçümleri, uzun süreli ölçüm kökeni, cihazda IBO testi ve nihai üretim kabulü tamamlanmış değildir. Kullanıcıca çalıştığı doğrulanmış kanallar başarısız offline kanıta dayanarak silinmez.

## Devam sırası
1. Güncel HEAD üzerinde K3 odaklı unittest ve sonra bütün offline testleri çalıştır; başarısızlıkları gerçek çıktıya göre düzelt.
2. Özellikle altı saatlik **ardışık** aralık, RFC3339, farklı saat dilimleri, mükerrer adaylar, yetkisiz kanal kanıtı ve CLI'nin iki modunu kontrol et.
3. İzole fixture raporlarını doğrula; hiçbir canlı playlist/EPG dosyasına yazma.
4. Gerçek kanal ölçümleri ve IBO cihaz kabulü yapılmadıkça üretim onayı verme.
5. Her değişiklikten hemen önce ilgili dosyanın güncel SHA'sını oku; paralel sohbetlerle çakışma yaratma; commit mesajlarında [skip ci] kullan.

Notun yazıldığı anda main HEAD: bfb606865a408f1bb6d8351ed3ace6b610a8f263 (diğer sohbetler tarafından değişebilir).

## Ek ilerleme — 22 Ekim, son tur
- def4af8: Geçersiz adayların K2 pack() sınırında reddedildiği testlerde doğru aşama beklentisi.
- c70f243: Mükerrer aday testleri pack() sınırına uyarlandı.
- 4f7314a: Sahte kanıt zarfı, yanlış commit SHA ve aday/ölçüm kimlik uyuşmazlığı testleri eklendi.
- Yerel çalışma ortamında GitHub DNS çözümlemesi başarısız: `Could not resolve host: github.com`. Bu yüzden güncel testler çalıştırılamadı; yeşil kabul edilmemeli.
- GitHub'dan K3 kod ve test dosyalarının güncel içerikleri SHA ile tekrar okundu; paralel sohbetlerde değişen dosyalar için SHA tabanlı yazma sürdürüldü.

- b5018df: Aynı UTC anını farklı saat dilimiyle tekrarlayan ölçümler ve karışık kanal SHA256 aşamaları için regresyon testleri eklendi.
- GitHub Actions geçmişinde son görülen offline test çalışması 39800980208 başarılı, fakat HEAD 3edbb863 sürümüne ait; yeni K3 commit'lerinin doğrulaması değildir. Yeni Actions çalışması tetiklenmedi.

- 31b2fb2: K3 CLI kanıt dosyalarında üst dizin symlink reddi ve 16 MiB+1 baytla sınırlı okuma eklendi.
- b014281: CLI dosya okuma korumaları için regresyon sözleşmesi testi eklendi.
- Bu son değişikliklerin unittest sonucu henüz doğrulanmadı; gerçek canlı ölçüm veya üretim onayı yapılmadı.

## Paralel sohbet koordinasyonu — 22 Ekim son kontrol
- main son sekiz commit kontrol edildi: diğer sohbetlerde K1/K5 devir notları, K2→K3 zarf doğrulaması ve K3 regresyonları da ilerliyor. Bu sohbet bunları yeniden uygulamayacak.
- K3 bu sohbetin değişiklik alanı: madsc/candidate_probe_link.py, tests/test_candidate_probe_link.py ve bu devir notu; ortak madsc/channel_test.py üzerinde değişiklik öncesi güncel SHA ve son commit sahipliği yeniden kontrol edilecek.
- GitHub üzerinden commit ve blob SHA denetimi yapılıyor; sohbetler arasında gerçek zamanlı kilit veya mesajlaşma yok. Çakışma ihtimali sıfır değil.
- Açık güvenlik konusu: CLI kanıt okumasında dosya açıldıktan sonra descriptor/fstat doğrulaması; önceki yazma girişimi araç güvenlik kontrolünde engellendi, commit oluşmadı.

## Son devir — K3 CLI dosya koruması ve paralel commit çakışması
- 610a6ac488dfcea7766ced0ce57e4247cfbae1b4: K3 CLI seek edilemeyen kanıt girişlerini reddediyor.
- 38e7ab86c70c7a33994476066094b4c7aa8a5a33: seekable koruması için test sözleşmesi güncellendi.
- Önceki devir notu yazma girişimi, paralel sohbetin d686a73e8e7b15be0704a0d4200ddae93e087b5 commit'iyle eşzamanlı olduğu için 409 conflict aldı. O denemede not değişmedi; bu kayıt güncel SHA üzerinden yeniden yapılıyor.
- Seekable kontrolü, açılan dosyanın fstat ile normal dosya ve doğru boyutunun doğrulanmasının eşdeğeri değildir. Bu açık iş sürüyor.
- Güncel K3 testleri çalıştırılmadı. Canlı kanal testi, IBO cihaz doğrulaması ve üretim onayı yapılmadı. K1/K5 ve K2/K4 kapsamındaki çalışmaları tekrar etme.

## K3 açık güvenlik eksiği düzeltmesi
- 956d147: CLI kanıt dosyası açıldıktan sonra os.fstat(handle.fileno()) ile normal dosya türü ve 16 MiB üst sınırı doğrulanıyor. Önceki seekable kontrolü kaldırıldı; mevcut yol symlink ve sınırlı okuma kontrolleri korunuyor.
- 5d087c5: Test sözleşmesi fstat, stat.S_ISREG ve açılmış dosya boyutu kontrolüne uyarlandı.
- Henüz yerel/CI unittest sonucu alınmadı. Dosya açılışında TOCTOU ve O_NOFOLLOW ile atomik açma konusu ayrıca değerlendirilmeli; fstat tek başına yol değiştirme yarışını çözmez.

## K3 dosya açılışı sertleştirmesi
- d372f58: Kanıt girdisi os.open ile O_NOFOLLOW (destekleniyorsa) kullanılarak açılıyor, os.fdopen üzerinden fstat kontrolü ve 16 MiB sınırlı okuma sürüyor.
- 134c3ee: O_NOFOLLOW/os.open kaynak sözleşmesi regresyon testi eklendi.
- Üst dizin bileşenleri için atomik dirfd/openat yürüyüşü uygulanmadı; yarış koşullarının tamamen kapandığı iddia edilmemeli. Güncel testler çalıştırılmadı.

## K3 O_NOFOLLOW zorunlu kılındı
- 70c8ce6: O_NOFOLLOW mevcut değilse kanıt girdisi okunmuyor; zayıf os.O_RDONLY fallback kaldırıldı.
- 9cc93fd: K3 CLI fail-closed O_NOFOLLOW kaynak sözleşmesi testi güncellendi.
- Linux/GitHub Actions ortamında destek beklenir; diğer platformlarda CLI bilinçli olarak hata verir. Üst dizin yarışları hâlâ tam atomik korunmuyor.
- Testlerin güncel HEAD üzerinde çalıştığı henüz kanıtlanmadı; canlı/IBO doğrulaması yok.

## K3 son değişiklikler
- c43318f: Kanıt dosyası açılışında O_NONBLOCK bayrağı eklendi.
- 48fe6f9: Açılış bayraklarına ilişkin test beklentisi güncellendi.
- Son commitler için test çalıştırması henüz doğrulanmadı.

## K3 yürütülebilir dosya okuma testleri
- 03b82dc: CLI içindeki kanıt yükleyicisi load_evidence(path) olarak ayrıldı; CLI aynı işlevi kullanıyor.
- 5026751: Normal JSON, tekrarlanan JSON anahtarı, symlink ve 16 MiB üstü dosya için doğrudan yükleyici testleri eklendi.
- Yeni testler henüz CI/yerel ortamda çalıştırılmadı; başarılı oldukları iddia edilmemeli. Üst dizinlerin atomik açılması ve gerçek kanal/IBO ölçümleri hâlâ açık.

## K3 yükleyici regresyon onarımı
- acb6cf1: CLI testinde eski load() beklentisi load_evidence() olarak düzeltildi.
- c8d4e62: Ayrılan load_evidence işlevine eksik json ve _unique_json_pairs importları eklendi; olası NameError giderildi.
- Bu düzeltmeler kaynak incelemesiyle belirlendi; güncel test çalıştırması henüz doğrulanmadı.

## K3 sözdizimi onarımı
- b2a0c20: load_evidence ayrıştırma işleminden kalan yanlış girintiler düzeltildi; modülün import edilmesini engelleyen kaynak hatası giderildi.
- Bu değişiklik GitHub'a yazıldı ancak mevcut HEAD üzerinde Python unittest/CI sonucu henüz alınmadı.

## K3 özel dosya ve üst dizin testleri
- b5b9cb1: FIFO kanıt girdisinin beklemeden reddedilmesi ve symlink üst dizin girdisinin reddedilmesi için yürütülebilir regresyon testleri eklendi.
- Bu testler henüz çalıştırılmadı. Gerçek zamanlı üst dizin değiştirme yarışına karşı atomik koruma ayrıca gerekli.

## K3 modül yükleme testi
- 16f0d0a: Python AST sözdizimi ve load_evidence import regresyon testi eklendi.
- Güncel testler henüz çalıştırılmadı; önceki not yazımı paralel commit nedeniyle 409 ile başarısız olmuştu.

## K3 bozuk kanıt girdisi testleri
- fe48436: Eksik JSON ve geçersiz UTF-8 içeren kanıt dosyalarının reddedilmesini kontrol eden test eklendi.
- Güncel testler henüz çalıştırılmadı; üretim kanalları ve canlı veri değiştirilmedi.

## K3 UTF-8 regresyon testi düzeltmesi
- b2bc426: Geçersiz UTF-8 testi artık kaçış karakterleri yerine gerçek 0xff baytını bytes([255]) ile kullanıyor.
- Test sonucu henüz doğrulanmadı; canlı kanal veya üretim dosyaları değiştirilmedi.

## K3 güvenli açma desteği regresyonu
- 1282551: O_NOFOLLOW geçersiz olduğunda yükleyicinin reddetmesini sınayan test eklendi.
- 60ef3ec: O_NOFOLLOW desteği geçerli int değilse ValueError ile fail-closed davranışına geçildi.
- 9140300: Kaynak sözleşmesi ve regresyon testi yeni açık hata beklentisine uyarlandı.
- Bu commitlerin unittest sonucu henüz doğrulanmadı; üretim onayı verilmedi.

## K3 dizin dosya tanıtıcısıyla yol açma
- 92e0f45: Kanıt dosyası yolunun her bileşeni dir_fd ve O_NOFOLLOW kullanılarak açılıyor; dosya türü ve boyutu açılmış descriptor üzerinde doğrulanıyor.
- f74e2db: Eski yol kontrolü kaynak beklentileri yeni dirfd tasarımına uyarlandı.
- Bu değişiklikler için unittest/CI doğrulaması henüz yok; üretim onayı verilmedi.

## K3 dizin kanıtı negatif testi
- ecd85c1: Kanıt dosyası olarak dizin verilirse yükleyicinin hata üretmesini kontrol eden test eklendi.
- Test henüz CI veya unittest ile çalıştırılmadı; son dirfd değişikliğinin gerçek regresyon çalıştırması önceliklidir.

## K3 güvenli açma hata türü düzeltmesi
- 90c9202: Dirfd yol açma sırasında oluşan OSError artık ValueError olarak raporlanıyor; önceki symlink reddi testleriyle hata sözleşmesi tutarlı.
- e18cb02: Dizin girdisi testinin beklediği hata açık mesajla kesinleştirildi.
- Henüz yeni unittest/CI çalışması doğrulanmadı. Kod ve test commitleri [skip ci] ile gönderildi.

## K3 izole yürütme doğrulaması (2026-10-22)
- Güncel load_evidence uygulamasının izole edilmiş kopyası üzerinde Python unittest ile 9 senaryo çalıştırıldı: normal JSON, duplicate key, symlink dosya, symlink üst dizin, dizin, FIFO, geçersiz UTF-8, 16 MiB üzeri dosya, eksik dosya. Sonuç: 9/9 başarılı.
- Bu test depo HEAD veya tam K3/K2 entegrasyon testi DEĞİLDİR; izole kopya ve yerel duplicate-key yardımcı işlevi kullanıldı. CI yeşil sonucu iddia edilmemelidir.
- Sonraki öncelik: tam depo unittest/Actions doğrulaması, kalan test sözleşmeleri ve K2/K3 entegrasyonu.
