# MADSC55-TV — YENİ SOHBETE DEVİR NOTU — 22 EKİM 2026

## Kesin hedef
- Yalnızca **Madsc55/Madsc55-Tv** deposu, **main** dalı. Eski **Madsc55/madsc-tv** yalnızca salt okunur karşılaştırma kaynağıdır.
- Bu not oluşturulurken main HEAD: **3c228e7340b090ae4edf49d3d7b49382a4ef6d69**. Yeni sohbetin ilk işi HEAD'i tekrar okumak ve eşzamanlı değişiklikleri kontrol etmektir.
- İki sohbetten gelen mevcut işlere dokunmadan devam et; tamamlanan işleri tekrarlama. Önce `IKI_SOHBET_BIRLESIK_DEVIR_2026-10-22.md`, `DEVAM_NOTU.md`, `PROJE_HAFIZASI.md`, `BIRLESIK_KALICI_CALISMA_KURALLARI.md` ve bu notu oku.

## Kullanıcının beklentisi
- Kullanıcı çok sayıda küçük, tek tek düzeltmeden yoruldu. **Toplu, sonuç odaklı gerçek K1–K5 kurulumunu bitirmeyi** istiyor. Gereksiz açıklama yapma; kısa Türkçe rapor, kanıtlı ilerleme ve gerçek test sonucu ver.
- Kullanıcıya yaklaşık **%60 tamamlandı / %40 kaldı** daha önce bildirilmişti. Bu bir **önceki genel ilerleme tahmini**; güncel GitHub kanıtlarıyla yeniden ölçülmedi. Asla %0 genel proje tamamlanması diye gösterme. **0/92**, yalnızca bağımsız davranışsal kabul sayısıdır.
- Ekran görüntüsündeki beşli hedef: K1 güvenlik (26 kural ve 8/18 görev), K2 keşif (kaynak arşivi/aday/tekrar), K3 kanal testi (üç aşama, altı saat, 75 aday, IBO), K4 EPG/logo (XMLTV, Pages pilotu), K5 arşiv/bakım (yedek, izole restore, 92 eski workflow). Mevcut repo teknik adlandırmasında K4 `madsc-04-yedek.yml` ve K5 `madsc-05-bakim.yml`; EPG/logo işleri diğer modüllere dağılmıştır. Bu farkı göz ardı etme.

## Şimdiye kadar doğrulanmış durum
- **5/5 ana workflow dosyası mevcut**: `.github/workflows/madsc-01-guvenlik.yml`, `madsc-02-kesif.yml`, `madsc-03-kanal-test.yml`, `madsc-04-yedek.yml`, `madsc-05-bakim.yml`. Hepsi manuel `workflow_dispatch` temelli; otomatik günlük üretim kanıtı yok.
- 10 yardımcı workflow komutunun beş ana workflow'a statik bağlanması envanterlenmiş; 99 eski YAML, 92 kapsam içi, 7 kapsam dışı. 22 görev defteri `docs/K1_K5_KANITLI_GOREV_DEFTERI.json`.
- Önceki offline gate kaydında 707 test ve beş izole fixture kapısı geçmişti, ancak **son commitler için yeniden çalıştırılmış değildir**. CI'de önceki `d6fe123` SHA üzerinde offline-tests success kanıtı var; bu güncel HEAD'i doğrulamaz.
- **Kabul 0/92 davranış, 0/26 güvenlik, 0/22 görev**; bunlar genel geliştirme yüzdesi değil. K2/K3 gerçek dış kaynak, K4 dış restore, K5 bağımsız aynı-input eski/yeni run/artifact SHA ve yan etki kanıtları açık. IBO Player Pro fiziksel cihaz testini kullanıcı yapacak.

## Bu sohbetin son GitHub commitleri (hepsi [skip ci])
1. `6bc54827805d87a3118701cfd421db7b94008c81`: beş legacy adapter için sınır ve test paketi.
2. `23312ddcf03d4729b62d3e5cfc86bc33108ab9f6`: geçmiş/provenance/retest/izole aday kuyruğu + regresyon.
3. `2ea58e800156e3c99eb63f882f838045fc0714eb`: tarih normalizasyonu, köken, tekrar test ayrıştırma + regresyon.
4. `a39cdfa17ec9f513ad327f4ab2d0c49f6e15690b`: `docs/K1_K5_KURULUM_DURUMU_2026-10-22.md`, kurulum ile kabul ayrımı.
5. `3c228e7340b090ae4edf49d3d7b49382a4ef6d69`: `madsc/five_stage_installation.py` ve `tests/test_five_stage_installation.py`, 5 ana workflow, 10 yardımcı komut, 22 görev, 92 davranış için **read-only toplu durum denetimi**. Kod ve test GitHub'a kaydedildi ama **henüz çalıştırılmadı**.
- Bu notu ekleyen yeni commitin SHA'sı Git geçmişinden okunacak.

## Kesinlikle yapılmayacaklar
- Korunan ana kanal listeleri, YEDEKLER, YENİLER, FAVORİLER, cihaz favorileri, IPTV/EPG/logo/yedek/arşiv üretim verileri değiştirilmeyecek.
- Eski workflowlar kanıtsız kapatılmayacak, PR #71 veya başka PR main'e merge edilmeyecek, eski depoya yazılmayacak.
- Kullanıcı izni olmadan GitHub Actions dispatch/rerun, canlı kanal probe, IBO cihaz testi yapılmayacak.
- Kanıt olmadan kabul veya yüzde artırılmayacak. Commitler `[skip ci]`; her yazmada güncel main SHA lease kontrolü.

## Yeni sohbetin ilk işleri — toplu bitirme yaklaşımı
1. HEAD ve devir dosyalarını oku; mevcut `madsc/five_stage_installation.py` ile 22 görev, 5 ana workflow, 10 yardımcı workflow ve 92 eski otomasyon arasında somut boşlukları toplu çıkar.
2. Erişilebilir yerel checkout varsa `python -m madsc.offline_gate` çalıştır; yeni regresyonları da kapsayan **gerçek** sonuçları bildir. Actions tetikleme.
3. Önce eksik **gerçek davranış entegrasyonu ve K1–K5 uçtan uca çalışma** üzerine büyük tutarlı paket yap; sırf sınır ekleyen küçük commit zincirine dönme.
4. Canlı dış bağımlılıkları ve kullanıcı IBO testini ayrı engel olarak raporla; kanıt yoksa tamamlandı deme.
5. Yalnız `Madsc55-Tv/main` üzerinde SHA lease ile `[skip ci]` kaydet, devir notunu güncelle.

## Yeni sohbet başlangıç mesajı
“Madsc55/Madsc55-Tv main'deki `YENI_SOHBET_DEVIR_2026-10-22.md` dosyasını ve diğer üç devir/hafıza notunu oku. Son HEAD'den, iki sohbetin birleşik işlerini tekrar etmeden devam et. 5'li sistemi topluca bitirmeye odaklan, güncel offline testleri gerçekten çalıştır, gerçek eksikleri çöz, korunan verileri değiştirme, Actions başlatma ve [skip ci] ile kaydet. Önceki %60/%40 genel ilerleme tahmini ile 0/92 davranış kabulünü karıştırma.”


## Güncel diğer sohbetin toplu kanıtı ve tamamlayıcı son devir
1b30eeef71e73a5f0346efe46f2a0fd8028f7a0b ile 757 test, beş izole K kapısı ve beş gerçek geçici dosyanın K5 tüketimi başarılı; ayrıntı docs/FIVE_SYSTEM_BULK_VALIDATION_2026-10-22.json. Yukarıdaki 707 tarihsel bilgidir. 3c228e7 içindeki iki yeni dosya henüz bu sonuçla doğrulanmış sayılmaz. SOHBET_DEVIR_2026-10-22_SON.md bu sohbetin bütün paketlerini, hatalarını, kanıtlarını ve açık işleri topluca içerir; yeni sohbette önce onu ve güncel HEAD'i oku. Eşzamanlı iki devir korunmuştur; tüm kısıtlar geçerlidir.
