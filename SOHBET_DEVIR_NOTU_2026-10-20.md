# Madsc55-Tv — Yeni sohbete devir notu (20 Ekim 2026)

> Bu dosya sohbetin kelimesi kelimesine tam transkripti değildir; bu sohbetten çıkan kararlar, doğrulanmış işler, önemli uyarılar ve sonraki adımların devamlılık özetidir. Ayrıntılı geçmiş için `PROJE_HAFIZASI.md`, `docs/ESDEGERLIK_ILK_KANIT_PAKETI.md`, `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` ve GitHub commit/Actions kayıtlarını oku.

## 1. Projenin doğru adı ve depo sınırı
- **Tek yeni/hedef depo:** `Madsc55/Madsc55-Tv`. Kullanıcı proje adının tam olarak **Madsc55-Tv** olmasını özellikle istedi. Başka yazım kullanma.
- **Eski depo:** `Madsc55/madsc-tv`, özellikle `madsc/bes-sistem-toplu-birlestirme` dalı, yalnızca **salt-okunur kaynak/referans**. Eski depoya yazma.
- Eski sistemin faydalı işlevlerini yeni K1–K5'e davranış kaybı olmadan entegre et; eski 99 workflow'u olduğu gibi kopyalama. Gereksiz tekrarları birleştir.
- Kullanıcı “Yap”, “Devam et”, “sırayla yap” dediğinde mümkün olduğunca doğrudan gerçek kod/test ilerlemesi yap; sadece plan ya da belge yazıp bitirme.

## 2. Beşli mimari
- **K1 Güvenlik:** izinler, korunan dosyalar, onay ve güvenlik kapıları.
- **K2 Keşif:** kaynak tarama, aday bulma, dedup, kaynak kanıtı.
- **K3 Kanal testleri:** ffprobe/ffmpeg video-ses, süreklilik, EPG/logo ve kimlik kanıtı.
- **K4 Arşiv/yedek:** güvenli yedek, bütünlük ve geri yükleme kanıtı.
- **K5 Genel bakım:** rapor, birleştirme, kabul ve koordinasyon.
- Amaç yeni sistemi gerçekten kurmak, eski 92 otomasyonun görevlerini doğru kategorilere geçirmek, davranışsal uyumluluğu ölçmek ve kanıtsız üretim onayı vermemek.

## 3. Kaynak incelemesi ile davranışsal kabulü ASLA karıştırma
- Önceki proje raporunda **99/99 YAML ilk kaynak incelemesi**, **130/130 Python kaynak incelemesi/envanteri**, **68/68 Python test dosyası incelemesi/envanteri** tamamlandı diye kaydedilmiş. Bu aşamaları sebepsiz yere tekrar başlatma veya eksik diye sunma.
- Daha ayrıntılı inceleme kapsamı (ör. 23/99 derin YAML) ve gerçek çalışma davranışı başka kabul seviyeleridir; tamamlanan ilk incelemeyi iptal etmez.
- **92 eski otomasyon için tam davranışsal eşdeğerlik: 0/92 doğrulanmış.**
- **26 güvenlik kuralı için çalışma zamanı kabulü: 0/26 doğrulanmış.**
- Yeşil offline/fixture CI = canlı yayın, üretim güvenliği, 92/92, 26/26 veya IBO cihaz onayı değildir.

## 4. Koruma kuralları
- Korunan ana M3U listeleri (CALISANLAR, YENILER, YEDEKLER, HEPSI, FAVORILER), `epg/`, `logolar/`, `logos/`, arşivler, cihaz favorileri ve PR #71 üzerinde izinsiz değişiklik yapma.
- Cron zamanlarını, eski workflow'ları ve IBO kararlarını sessizce değiştirme.
- Gerçek yayın/cihaz doğrulaması yapılmadan otomatik ana listeye ekleme veya “üretime hazır” sonucu verme.
- Kullanıcı tek tek çok sayıda commit/test yerine **birbiriyle ilişkili değişiklikleri tek toplu commit ve tek toplu CI** olarak istiyor. Önceki asistan bu tercihi birkaç kez ihlal etti; sonraki turda düzelt.

## 5. Bu sohbetin son doğrulanmış teknik ilerlemesi
- `madsc/legacy_scoring.py` eski video(20), ses(15), çözünürlük(3/7/10), HTTPS logo(5) puanlarını salt-okunur değerlendiriyor.
- `tests/test_legacy_source_score_vectors.py`: 10 eski kaynak temelli puan vektörü, 24 onay matrisi kombinasyonu, güvenli reddetme; Actions **#39331287407 SUCCESS**.
- `madsc/legacy_candidate_merge.py`: üç eski teknik rapor adından kanıt önceliği, URL üzerinden teknik kanıt birleştirme, HTTP(S) filtreleme, en yüksek puan, eşitlikte ilk kayıt, sıralama, 13 CSV alanı ve `ANA_LISTEYE_EKLENEBILIR=HAYIR` sözleşmesi.
- `tests/test_legacy_candidate_merge.py`: dedup, öncelik, eşitlik, geçersiz veri ve koruma testleri. Actions **#39331762156 COMPLETED SUCCESS**, önceki kod koşusu **#39331737878 SUCCESS**.
- Başarılı K1–K5 toplu fixture kabulü **#39329756380** (altı job SUCCESS). Eski iptal edilen ara commitlerin bu başarılı run'ın atası olduğu doğrulandı.
- Son hafıza güncellemesi commit **3686344d8815989a9236b5ccb1893be4f585339e**. Son kanıt dosyası `docs/ESDEGERLIK_ILK_KANIT_PAKETI.md`; son birleştirme kod/test commitleri **1492da6**, **583893c**, not commit **715d1e9**.
- Bu testler **eski betiğin gerçek çalıştırılmasıyla diferansiyel kabul değildir**. 0/92 hâlâ doğru.

## 6. Sıradaki işler — kaldığımız nokta
1. `scripts/akilli_aday_puanla.py` (eski depoda salt-okunur) ile yeni `madsc/legacy_candidate_merge.py` işlevini **aynı izole/sentetik CSV girdileriyle fiilen karşılaştıran diferansiyel test** kur. Çıktı satırları, kolonlar, UTF-8 BOM, sıralama, kanıt önceliği, JSON özet, hata/negatif senaryoları karşılaştır. Eski kodu korunan dosyalarda veya gerçek yayınlarda çalıştırma.
2. Eski `aday-logo-epg-test.yml` / `scripts/candidate_epg_logo_join.py` için pilot XMLTV 5 kanal, program sayısı, logo SHA, kimlik/onay reddi ve ana liste hash korumasını yeni K3 ile izole karşılaştır.
3. Eski `390-aday-tekrar-test.yml` / `yedekler/tekrar_test_390.py` için 10 worker (en fazla 12), ffprobe 22 sn timeout, ffmpeg 20 sn decode (45 sn timeout), CSV/M3U ve `if:always()` artifact davranışlarını K3'e uyarlayıp izole test et. Korunan `yedekler/` altına yazma, gerçek URL testini izinsiz başlatma.
4. K1–K5 handoff/kanıt zincirini genişlet, kalan eski işlevleri sırayla birleştir; 26 runtime güvenlik ve offsite restore/IBO cihaz kanıtlarını ayrı kabul et.
5. Kanıtları `docs/ESDEGERLIK_ILK_KANIT_PAKETI.md` ve `PROJE_HAFIZASI.md` dosyalarında güncelle; gerçek test sonuçlarını Actions run ID ile doğrula.

## 7. Sohbet devamlılığı
- Kullanıcı sohbetin dolup dolmadığını ve ne kadar süre kaldığını sordu. Asistan **sohbetin kalan bağlam kotasını, dolma zamanını veya uygulamanın vereceği uyarıyı göremez**; önceden kesin bir doluluk uyarısı sözü verme.
- Bu dosya yeni sohbet için bilinçli devir özeti. Sohbetin birebir tam arşivi değildir; birebir kayıt gerekiyorsa uygulamanın sohbet geçmişi/veri dışa aktarımı gerekir.
- Yeni sohbette önce **bu dosyayı**, `PROJE_HAFIZASI.md` ve ilgili eşdeğerlik kanıtlarını oku; tamamlanmış işleri tekrar yapma. Kullanıcının hedefini, kararlarını ve korumalarını esas al.


## 20 Ekim 2026 — Dogrulanmis son ilerleme
K3 legacy EPG/logo ve 390 aday tekrar testleri eklendi; Actions #39334663810 SUCCESS. K3 core kanit akisina entegrasyon commit 9c7055a7; Actions #39334973919 SUCCESS. K1 izole rapor yazma korumasi commit 7edeafcf; Actions #39335736344 SUCCESS. Bunlar fixture testleridir, uretim kabul kaniti degildir. 92 eski workflow tam davranissal esdegerlik 0/92, 26 runtime guvenlik kabulu 0/26. 47% yalnizca tahmini gelistirme puanidir. Sonraki adim K1 merkezi kanit entegrasyonu ve K2-K3-K5 birlestirmesidir. Onceki notlar korunacak; eski repo salt okunur; uretim listeleri, EPG, logo, yedek ve favoriler degismeyecek. Kullanici baglantili isler icin tek toplu commit ve CI tercih eder.
