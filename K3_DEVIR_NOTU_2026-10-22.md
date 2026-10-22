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
