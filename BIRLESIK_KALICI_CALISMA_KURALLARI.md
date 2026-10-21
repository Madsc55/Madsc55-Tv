# Madsc55-Tv — Birleşik kalıcı çalışma sözleşmesi
Tarih: 20 Ekim 2026. Bu belge eski ve yeni notlardan çıkarılmış çalışma kurallarının tek giriş noktasıdır; kaynak notların yerine geçmez.

## Değiştirilemez kaynak ayrımı
- Yeni sistem: `Madsc55/Madsc55-Tv`, `main`. Eski sistem: `Madsc55/madsc-tv`, `madsc/bes-sistem-toplu-birlestirme`; yalnız salt okunur.
- Tarihsel talimatlar yeni üretim yazma yetkisi vermez. En yeni açık kullanıcı kararı ve veri koruma kuralları önceliklidir.

## Her işten önce zorunlu kaynak okuması
1. `ESKI_SISTEM_NOTLARI.md` ve ilgili özgün `docs/eski_depo_not_arsivi/` dosyaları.
2. `PROJE_HAFIZASI.md`, `SOHBET_DEVIR_NOTU_2026-10-20.md`, güncel ilgili karar/teknik belgeler.
3. Eski `AGENTS.md`, `DEVAM_NOTU.md`, `810 dosya notu.md`, `GUVENLIK_KURALLARI.md`, `BES_SISTEM_TOPLU_IS_DEFTERI.md`, `BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md` ve işe ilişkin diğer alt notlar.
4. Notlarda geçmiş hata, başarısız deneme, tekrar eden iş, korunan veri, tamamlanmış araştırma ve açık eksikleri belirle; mevcut kod ve testle karşılaştır. İlgili kaynağı okumadan okundu deme.
5. Sohbetler arası süreklilik için mevcut notları ve gerektiğinde önceki sohbet bağlamını kontrol et. Tüm sohbetlerin otomatik eksiksiz görüldüğünü varsayma.

## Beşli sistem: tek iş, çapraz etki, tek kabul
- K1 güvenlik ve izin kapıları; K2 keşif, geçmiş ve kaynak kanıtı; K3 kanal testi, IBO/EPG/kimlik; K4 yedekleme ve geri yükleme; K5 bakım, rapor ve toplu kabul.
- Her görevde K1–K5 etki ve bağımlılık matrisi çıkar. Bir iş K2, K3, K4, K5'i etkiliyorsa aynı iş paketinde hepsini uygula; K1 güvenlik kapısını da değerlendir. İlgili K'ler doğrulanmadan işi kapatma.
- Eski 99 YAML/92 otomasyonun mevcut incelemesini tekrarlama. Gerekli davranışları beş merkezi sisteme taşı; eski workflow'ları aynen kopyalama, gereksiz 20–30 bağımsız zamanlayıcı açma. Her davranış için tetikleyici, girdi/çıktı, yazma etkisi, bağımlılık ve kabul kanıtı izle.
- İnceleme, kod, birim testi, entegrasyon, gerçek veriyle davranışsal eşdeğerlik, runtime güvenlik ve üretim kabulü farklı seviyelerdir. Offline yeşil CI canlı başarı değildir. Kabul sayaçları doğrulanmadan 0/92 ve 0/26 olarak kalır.
- Küçük testleri ana teslim gibi sunma; bağlantılı büyük iş paketleri, toplu test ve açık kabul ölçütleri kullan. Commit, Actions run, artifact ve sonuçları kaydet.

## Veri ve kullanıcı kararlarını koruma
- Kullanıcı onayı olmadan canlı ana M3U listelerini (CALISANLAR, YENILER, YEDEKLER, HEPSI, FAVORILER), `playlist.m3u8`, `xmltv.xml`, `epg/`, `logos/`, `logolar/`, arşiv, cihaz favorileri ve PR #71'i değiştirme.
- Kullanıcının IBO Player'da çalıştığını doğruladığı kanalı teknik test olumsuz diye otomatik silme. EPG/XMLTV tvg-id uyumu, oynatıcı farkı ve gerçek cihaz kabulünü ayrı kanıtla.
- K4'te yedek/geri yükleme ve bağımsız harici depolama kanıtını ayır. K1 gerçek yazma yollarında zorunlu engel olmalı; K5 eksik kanıtı başarı diye sunmamalı.
- Canlı veriye yazmadan önce izole ve salt okunur doğrulama; gerekli izin ve geri dönüş kanıtı olmadan üretime geçme.

## Not birleştirme ve geçmiş hatalardan öğrenme
- Kullanıcının isteği: eski sistemin tüm gerçek not/kararları `ESKI_SISTEM_NOTLARI.md` altında tek tam metin olarak erişilebilir olsun; yeni notlarla birlikte okunsun. Mevcut indeks tam fiziksel birleştirme değildir.
- 45 metin + 25 JSON/CSV kopyası arşivde doğrulanmış; kalan yapılandırılmış kaynakların karar/not sınıflaması eksik. 70 kaynak için üretilmiş birleştirme artifact'ı ile main'deki dosyayı karıştırma.
- Kaynakların tümünü okuduğunu veya birleştirmenin bittiğini kanıt olmadan iddia etme. Tamlık, kaynak yolu, hash, içerik ve GitHub sonuçlarını doğrulamadan hiçbir arşiv kopyasını silme.
- Geçmişteki yanlış varsayımları, tekrarlanan incelemeleri, başarısız testleri ve kararlardan sapmaları görevlerin ön koşulu olarak kontrol et.

## Devir ve kanıt disiplini
- Her önemli işin sonunda yapılanlar, yapılacaklar, yapılmayacaklar, başarısızlıklar, bağımlılıklar, riskler, kanıt linkleri ve sıradaki somut adım `PROJE_HAFIZASI.md` içine işlenir.
- Her yeni sohbette önce bu sözleşme ve kaynak notlar okunur. Kullanıcıya eski kararları tekrar anlattırma.
- Kanıtı olmayan iş 'tamamlandı' diye sunulmaz; queued/running test SUCCESS değildir.


## EK KALICI KURAL 21 — Yeni sohbetlerde Madsc55-Tv kimligini asla karistirma (20 Ekim 2026)
- **Aktif ve tek yazilabilir yeni proje:** `Madsc55/Madsc55-Tv`, dal `main`; proje adi **Madsc55-Tv**.
- **Eski, salt-okunur referans:** `Madsc55/madsc-tv` (ozellikle `madsc/bes-sistem-toplu-birlestirme`). Kullanici acikca istemedikce eski depoda test, commit, workflow tetikleme veya kod degisikligi YAPMA.
- Yeni sohbet baslangicinda, kod veya GitHub isleminden **once** depo sahibi/adi ve dali dogrula; `BIRLESIK_KALICI_CALISMA_KURALLARI.md`, `PROJE_HAFIZASI.md`, `ESKI_SISTEM_NOTLARI.md`, `SOHBET_DEVIR_NOTU_2026-10-20.md` dosyalarini ve ilgili kaynak notlarini oku.
- Eski depodaki Actions run/commit/test basarisi yeni Madsc55-Tv sisteminin ilerlemesi veya kabulu olarak sunulamaz. Her kanit icin dogru repo, dal, commit SHA ve run ID birlikte dogrulanir.
- Eski sistemin notlari, hatalari ve kazanilmis islevleri yeni K1–K5 sistemine bilgi kaynagidir; yeni sistemin gelistirmesi yalniz yeni depoda yapilir. Tamamlanan incelemeleri ve testleri gereksiz tekrarlama.
- Bu madde mevcut **20 calisma ilkesine ek** baglayici kuraldir; onceki ilkeleri kaldirmaz veya degistirmez. Yeni sohbet devir notuna da aktarilir.


## ZORUNLU AD VE DEPO KIMLIGI KONTROLU - 20 Ekim 2026
- Yeni sistemin TAM ve TEK dogru adi: **Madsc55-Tv**. GitHub sahibi/deposu: **Madsc55/Madsc55-Tv**. Yazilabilir tek dal: **main**.
- **Madsc-Tv**, **MADSC TV** veya **Madsc55/madsc-tv** yeni sistemin adi/depusu olarak kullanilamaz. Kisa, eksik veya eski adla proje tanitma; yeni sohbet baslik ve cevaplarinda **Madsc55-Tv** yaz.
- **Madsc55/madsc-tv** eski depodur; **madsc/bes-sistem-toplu-birlestirme** dali da dahil kesinlikle salt okunur. Kullanici acik izin vermedikce eski depoda commit, dosya degisikligi, Actions tetikleme veya workflow duzenlemesi YASAK.
- HER YENI SOHBETTE ilk GitHub yazma isleminden ONCE hedef repository_full_name=Madsc55/Madsc55-Tv ve branch=main oldugunu acikca dogrula. Adlar birbirine benziyor diye eski depoya yazma. Yanlis hedef saptanirsa yazma islemini durdur.
- Bu madde mevcut 21 kurali guclendirir; onceki korumalari kaldirmaz. Yeni sohbete devirde aynen korunur.


## BAGLAYICI TOPLU CALISMA VE ACTIONS KOTA SOZU — 21 Ekim 2026
- Kullanici onceki 12 gunluk parcali GitHub Actions surecinde 2.000 dakikalik aylik kotanin tuketilmesinden ve K1-K5 isinin bitmemesinden sikayet etti. Ayni yontem KESINLIKLE tekrarlanmayacak.
- Kullanici ACİK ve AYRI izin vermedikce GitHub Actions workflow_dispatch, rerun, otomatik tetikleme veya kota tuketen herhangi bir Actions calistirmasi YASAK. CI tetikleyebilen commitlerde [skip ci] kullan; workflow'lar manual workflow_dispatch-only kalmali. Bu kural kullanicinin "devam", "bitirelim", "testleri yap" sozleriyle izin verilmis sayilmaz.
- GitHub Actions dakikasi ile test sayisi farklidir: 2.000 dakika, 2.000 test demek degildir. Tek uzun job da kota tuketebilir. Izin verilen son dogrulamada dahi sure, job sayisi ve maliyet riski once aciklanir.
- Tum K1-K5 kaynaklari, bagimliliklari ve testleri guncel Madsc55/Madsc55-Tv main commit SHA ve dosya SHA'lariyla dogrulanarak yerelde toplanir. Python unit, guvenlik, K1-K5 entegrasyon ve fixture testleri mumkun oldugunca TEK TOPLU offline regresyonda calistirilir. Tek tek GitHub Actions calistirma, her duzeltmeden sonra CI baslatma ve yesil fixture'i production kabulu gibi gosterme YASAK.
- Toplu regresyonda hatalar bir arada listelenir, baglantili duzeltmeler birlikte yapilir, sonra yerel toplu regresyon tekrar edilir. Gereksiz mikro-gorevler, tekrar tekrar izin isteme ve kullaniciyi kucuk testlerle ugrastirma yerine gercek K1-K5 bitis kriterleri onceliklendirilir.
- Guvenli kaynak inceleme, main uzerinde izinli kod/test/not duzeltmeleri ve offline testler icin her adimda onay isteme; ama canli yayin/EPG/logo listelerine yazma, eski depoda degisiklik, canli ag testleri, kota veya dis sistem etkisi olan calistirmalar icin onceden acik onay gerekir. Bu kurallar mevcut korumalari gevsetmez.
- 92 eski otomasyon davranissal esdegerligi, 26 runtime guvenlik kurali ve bes sistemin tam kabulunu yalniz gercek kanitla bildir. 0/92 ve 0/26 mevcut kabul sayilari dogrulanmadan artirilmaz.
- YENI SOHBETTE bu bolum, bu sozler, onceki kullanici sikayeti, test/kota politikasi ve kaldigimiz somut durum mutlaka ilk once okunup uygulanir. Yeni sohbette yeniden ayni tartisma ve izin dongusu baslatilmaz.
