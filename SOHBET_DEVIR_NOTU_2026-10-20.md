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


## K2 yapilacak: Internet genelinde canli kanal kesfi (kullanici istegi, 20 Ekim 2026)
Kanal kesfi sadece tekil URL ile sinirli olmayacak. Kamuya acik ve yasal/izinli M3U playlist, M3U8 HLS akisi, resmi canli TV yayin sitesi, resmi yayinci dizini, acik IPTV proje kaynaklari ve YouTube Live uzerindeki resmi/dogrulanmis canli kanal yayinlari da aday kaynak olarak arastirilacak. Bulunan adresler dogrudan uretim playlistine yazilmayacak. K2 kaynak/izin/kimlik/tekillik ve URL kaynagini kaydeder; K3 gercek teknik oynatilabilirlik, ses-video, EPG/logo ve IBO cihaz uyumlulugunu ayri dogrular; K5 sureklilik, tekrar kontrolu ve guvenli aday durumunu yonetir. YouTube sayfa URL'si dogrudan IPTV uyumlu kalici M3U8 kabul edilmeyecek; token/DRM/erisim ve yayin hakki kisitlari asilmayacak. Korunan CALISANLAR, YENILER, YEDEKLER, HEPSI, FAVORILER, EPG/logo listelerine otomatik yazma veya otomatik onay yok. Bu bir YAPILACAK IS maddesidir, mevcut kesif kapsami tamamlandi iddiasi degildir.

## 20 Ekim 2026 — Yeni sohbet icin guncel kanit ve sonraki grup
Basarili dogrudan eski-yeni fixture diferansiyelleri: aday puanlama #39337813130; EPG/logo #39338017857; 390 teknik retest #39338267421. Kodlar tests/test_candidate_differential.py, tests/test_legacy_epg_logo_differential.py, tests/test_legacy_390_differential.py. Bu tam workflow kabul degildir: 0/92 ve 0/26 korunur. Sonraki toplu kod grubu: P01-P06 aday oncelik, R01-R05 tekrar araligi, H01-H05 gecmis birlestirme, ardindan workflow artifact ve timeout farklari. K2 acik/izinli M3U/M3U8, canli TV sitesi ve resmi YouTube Live kesif backlogu unutulmayacak.


## 20 Ekim 2026 — K2 history kanit zinciri ve bagimsiz GitHub kaynagi (SON GUNCEL)
**Yalnizca Madsc55/Madsc55-Tv main yazilabilir.** Eski Madsc55/madsc-tv depoyu, eski workflow hatalarini, cronlari ve PR #71'i yeni depo ile karistirma. Korunan CALISANLAR/YENILER/YEDEKLER/HEPSI/FAVORILER, EPG/logo ve uretim yedekleri degistirilmedi.

Dogrulanmis GitHub Actions basarilari: #39339828805 H05 atomic history envelope/R05 offline HLS; #39339972513 read-only legacy history bridge; #39340660815 K2 core fixture bridge; #39340902966 K2-K3-K5 run_id/commit_sha/digest bagli history artifact aktarimi; #39341040464 manifest SHA256 source gate; #39341268096 GitHub run/artifact/ancestry provenance testleri; #39341601409 salt-okunur GitHub REST istemcisi; #39341835535 fail-closed kaynak CLI; #39342095390 strict ZIP/SHA256 extraction; #39342334826 birlesik dogrulama pipeline; #39342558278 ayri opt-in workflow kod regresyonu. Bunlar basarili *izole CI*; canli kaynak kabulune esit degil.

Yeni kodlar:
- madsc/history_pair_store.py: iki legacy gecmis JSON'un tek SHA256 zarfinda atomik izole saklanmasi.
- madsc/history_pair_bridge.py, madsc/legacy_history_merge.py, madsc/legacy_history_provenance.py: eski gecmis salt-okunur import/merge ve provenance fixture.
- madsc/hls_segment_window.py: cevrimdisi HLS segment pencere farki, gercek medya decode veya canli akis testi degil.
- madsc/history_handoff.py, madsc/history_transport.py: K2-K3-K5 ayni run_id, commit SHA ve digest kanit zinciri, test artifact'lari workflow madsc-05-bakim.yml uzerinde bagli.
- madsc/history_source_gate.py: VERIFIED_SOURCE manifest, iki JSON SHA256 ve kaynak kimligi denetimi; tek basina bagimsiz kimlik kaniti degil.
- madsc/github_history_origin.py ve madsc/github_history_client.py: GitHub REST run, artifact, compare API uzerinden bagimsiz provenance; commit soy karari ve artifact kontrolu.
- madsc/history_artifact_download.py: yalnizca beklenen iki JSON, SHA256 ve ZIP sinirlari.
- madsc/history_origin_cli.py, madsc/history_verified_pipeline.py: salt-okunur verified source to handoff; kaynak/token yoksa fail closed.
- madsc/history_verified_workflow.py ve .github/workflows/madsc-k2-verified-history.yml: elle tetiklenen AYRI gercek kaynak dogrulama isi, manifest bulunmazsa bilerek basarisiz, otomatik fixture fallback yok; ana besli zincir etkilenmez.

Son kod commitleri: 783a6da6, 48035507, d5a49cee, 824b2ce8, baab856a, ed75b154, 164bced5, e157fb66. Bunlarin CI basarilari yukarida. Uretim esdegerlik 0/92, runtime guvenlik kabul 0/26; tam M3U8 canli akim/ses/video ve EPG/logo dogrulamasi YAPILACAK.

ONEMLI ACIK IS: Gercek history source artifact'i henuz yok/entegre degil. Manifest hashleri manifestten geldiginden bagimsiz yayinci imzasi sayilmaz. GitHub workflow gercek artifact kaydini dogrulayabilmek icin once guvenilir source artifact uretimi, GitHub API metadata semasinin gercek cevapla entegrasyon testi, ZIP indirimi ve kaynak kaydi tasarlanacak. Gercek artifact olmadan workflow'u basarili ilan etme. K2 izinli acik M3U/M3U8 ve resmi yayin kesfi, K3 ffprobe/ffmpeg gercek medya, K5 tekrar kontrolu backlogu korunur. Sonraki sohbet once bu notu ve PROJE_HAFIZASI.md'yi okusun; onceki isleri yeniden yapmasin.


## 20 Ekim 2026 — Eski sistem tum metin notlari yeni sisteme aktarildi
Eski Madsc55/madsc-tv dalindaki tum 45 Markdown/TXT belge docs/eski_depo_not_arsivi/ altina ayni dosya yollariyla alindi; kaynak/hedef Git blob SHA 45/45 eslesti. AGENTS.md, 810 dosya notu.md, DEVAM_NOTU.md, GUVENLIK_KURALLARI.md, OZELLIK_ENVANTERI.md ve tum alt metin notlari var. Arsiv rehberi docs/eski_depo_not_arsivi/ARSIV_REHBERI.md. 810 inceleme sayaci veya 92 esdegerlik kabulu degismedi. Eski depo salt okunur.


## 20 Ekim 2026 — ESKI DEPO TUM METIN/NOT ARSIVI TAMAMLANDI (DOGRULANDI)
Kullanici onceligi: Madsc55/madsc-tv deposunun madsc/bes-sistem-toplu-birlestirme dalindaki AGENTS, 810 dosya ana notu, alt notlar, devam, devir, guvenlik, ozellik envanteri, planlar, raporlar ve karar kayitlarini yeni Madsc55/Madsc55-Tv main deposuna birebir tasimak. **TAMAMLANDI**: eski Git tree uzerindeki tum 45 adet .md/.txt/.rst metin dosyasi, orijinal goreli yollariyla docs/eski_depo_not_arsivi/ altina salt-okunur tarihsel kopya olarak eklendi. Eski ve yeni tree SHA eslestirmesi 45/45; eksik 0, farkli 0. Eski depo degismedi, uretim listeleri degismedi.
Aktarim commitleri: 4d044ba690e1ea35e6135dd81560d5da9acd246a (AGENTS, 810 dosya notu, DEVAM_NOTU, guvenlik ve envanter), a31ad4853cdee935d4016a4c549c1bddeb147211 (16 ana/alt plan), 4bb6e93188b514d20615a8845dac77f9f0a9badb (8 kontrol), 387a44030f2fd15d0bf246607b0739e47e764955 (8 kesif/IBO/rapor), 6de30b7d906c9e1087594a15a83df7f828c91667 (8 IBO/yedek/VOD).
Yeni sohbet okuma sirasi: (1) docs/eski_depo_not_arsivi/AGENTS.md; (2) docs/eski_depo_not_arsivi/OZELLIK_ENVANTERI.md ve GUVENLIK_KURALLARI.md; (3) docs/eski_depo_not_arsivi/DEVAM_NOTU.md'nin guncel devir bolumu, docs/eski_depo_not_arsivi/810 dosya notu.md'nin en son ilerleme bolumleri; (4) PROJE_HAFIZASI.md ve SOHBET_DEVIR_NOTU_2026-10-20.md; (5) ilgili alt notlar ve guncel GitHub Actions. Eski notlardaki eski repo/dal yazma talimatlari tarihsel baglamdir: yeni gelistirme yalniz Madsc55/Madsc55-Tv main, eski depo salt okunur. Yeni ve daha guncel kullanici karari eski tarihsel karardan ustundur. Ozellikle YEDEKLER'e otomatik ekleme izni daha sonra iptal edilmistir. IBO cihaz onayi ile ffprobe/fixture CI karistirilmaz.
**Kapsam siniri:** 45/45 tum metin/not dosyalarinin tasinmasidir; 810 adet tum kaynak/veri/gorsel dosyasinin tasindigi veya 810/810 derin icerik denetimi yapildigi iddiasi degildir. 810 inceleme sayaci eski defterdeki tekil kayitlardan devam eder. 92 workflow davranissal kabul 0/92, 26 runtime guvenlik kabul 0/26; bu sayaclar aktarimdan degismedi. Mevcut yeni notlar uzerine yazilmadi, yalniz ekleme yapildi.
Sonraki is: 45 arşiv notunun icinden ilgili kurallari ve tamamlanmis isleri oncelikle okuyarak K1-K5 gercek esdegerlik, kaynak/provenance ve izinli M3U8 kesif eksiklerini gider; tamamlanmis testleri tekrarlama.


## 20 Ekim 2026 — Yeni sohbet: not aktarimi onceligi yeniden teyit edildi
Kullanici eski sistemdeki AGENTS, 810 ana/alt notlari ve diger tum notlarin yeni sistemde kullanilmasini, kaldigi yerin kalici kaydedilmesini tekrar istedi. Arsiv rehberi ve merkezi hafiza yeniden okundu. Onceki dogrulanmis Git tree karsilastirmasi: 45/45 .md/.txt/.rst metin/not dosyasi yeni docs/eski_depo_not_arsivi/ altinda birebir SHA eslesmesiyle bulunuyor; ayni notlar ikinci kez kopyalanmayacak. Bu tur bagimsiz tum-tree SHA taramasi yapilmadi; onceki kanit esas alindi. 810 kaynak dosyanin tamami tasinmis sayilmaz; tarihsel 769/769 gorev/not taramasi ile 810/810 derin inceleme farklidir. Eski depo salt okunur; korunan playlist, EPG, logo, favori, yedek ve cronlara dokunulmaz. Siradaki adim: kaynak tree envanterini yeniden dogrulayip metin-not kapsami disinda kalan gorev/karar kaydi niteligindeki JSON/CSV belgelerini tek tek belirlemek, gerekiyorsa salt-okunur tarihsel arsiv olarak eklemek; tamamlanan 45 dosyayi yeniden kopyalamamak. 92/92 davranissal kabul 0/92, 26/26 runtime kabul 0/26. Bu kayit belge/devir guncellemesidir, CI veya uretim kabul kaniti degildir.


## AÇIK İŞ — Eski sistem notlarının eksiksiz tek dosyada birleştirilmesi (20 Ekim 2026)

**Kullanıcının açık talebi:** Eski `Madsc55/madsc-tv` deposundaki bütün eski notları ve JSON/CSV içindeki tarihsel karar/not kayıtlarını yeni `Madsc55/Madsc55-Tv` deposunda **yalnız `ESKI_SISTEM_NOTLARI.md`** adlı tek tam metin dosyasında toplamak. Eski kaynaklardan hiçbir notu kaybetmemek. Bu iş **TAMAMLANMADI** ve yapılacak işler listesinde öncelikli kalmalı.

**Doğrulanmış mevcut durum:** Eski depodaki 45 `.md/.txt/.rst` dosyasının SHA-eşleşen kopyaları `docs/eski_depo_not_arsivi/` altında bulunuyor. Ayrıca 25 JSON/CSV tarihsel karar/inceleme kaydı aynı arşivde kaynak SHA eşleşmesiyle korunuyor. `ESKI_SISTEM_NOTLARI.md` şimdilik yalnız ana indeks/giriş noktası; bütün notların tam metnini içermiyor. Kalan JSON/CSV kayıtlarının not/karar içeriği açısından ayrıştırılması bitmedi. **70 kaynak dosyasının tamamının baştan sona okunup öğrenildiği iddia edilmez.**

**Yapılacaklar:** (1) Eski Git ağacındaki bütün JSON/CSV kayıtlarını ve gerektiğinde başka dosya türlerindeki tarihsel not/karar bilgilerini tek tek sınıflandır; bot/workflow ve canlı üretim verilerini not sanma. (2) Gerçek not ve karar içeriğini eksiksiz aktar, kaynak yolu ve içerik hash'iyle izle. (3) API'nin büyük dosya sınırını aşmak için güvenli, parça/parça çalışan birleştirme yöntemi kullan; `scripts/birlestir_eski_sistem_notlari.py` aracını incele, düzelt ve gerçekten çalıştır. (4) Tek `ESKI_SISTEM_NOTLARI.md` dosyasının **tam metin** ve bütün kaynaklarla birebir uyumlu olduğunu test et. (5) Ancak doğrulama sonrasında yeni depodaki gereksiz ayrı eski not kopyalarını temizle; silmeden önce tam metnin kaybolmadığından emin ol. (6) Yeni sistemde iş yaparken eski notları ilgili konularda oku; tarihsel kararları güncel kullanıcı talimatlarıyla karıştırma.

**Koruma:** Eski depo salt okunur. Yeni depoda botlar, 99 workflow, 92 davranışsal kabul, 26 güvenlik kuralı, M3U listeleri, EPG, logo, yedekler ve cihaz favorileri bu not birleştirme işi sırasında değiştirilmez. 92/92 ve 26/26 başarı iddiası yapılmaz. GitHub'a büyük/engellenen içerik yazma denemeleri daha önce başarısız oldu; güvenlik kontrolünü atlatmaya çalışma, güvenli alternatif yöntemi kullan. **Birleştirme tamamlandı denmeden önce GitHub'da sonuç doğrulanmalı.**


## KALICI ÇALIŞMA KURALI — Eski ve yeni notları birlikte esas al (20 Ekim 2026)

**Kullanıcının kesin talimatı:** Yeni MADSC TV sistemi kurulurken, geliştirilirken, değiştirilirken ve test edilirken **hem eski sistemden aktarılmış bütün notlar hem de yeni sistemin güncel notları birlikte incelenerek** ilerlenir. Sadece yeni notlara bakıp eski kararları, geçmiş hataları, incelemeleri, 810 dosya notlarını, AGENTS yönergelerini, alt notları, güvenlik ve kabul kayıtlarını görmezden gelmek yasaktır. İlgili işe başlamadan önce `ESKI_SISTEM_NOTLARI.md` ana girişini, gerekirse `docs/eski_depo_not_arsivi/` altındaki özgün tam metinleri, `PROJE_HAFIZASI.md`, bu devir notunu ve konuya ilişkin yeni notları oku. Eski notlarda yer alan tarihsel bilgi/kararları mevcut kod ve gerçek testlerle karşılaştır; çelişkide en yeni açık kullanıcı kararı ve koruma kuralları önceliklidir. Okunmayan notları okunmuş gibi, test edilmeyen işleri tamamlanmış gibi gösterme. Eski notların tek dosyada fiziksel birleştirilmesi tamamlanana kadar kaynak arşivden yararlanmaya devam et. **Bu kural bütün sonraki sohbetler ve iş aşamaları için geçerlidir.**


## KESİN DEPO ADLANDIRMA DÜZELTMESİ — 20 Ekim 2026

**Kullanıcının açık düzeltmesi:** `Madsc55/madsc-tv` = **ESKİ SİSTEM** (yalnız tarihsel kaynak, salt okunur); `Madsc55/Madsc55-Tv` = **YENİ SİSTEM** (geliştirilecek asıl sistem). Yeni sisteme yanlışlıkla "MADSC TV" ya da eski deponun adını verme. Yeni sistemden söz ederken **Madsc55-Tv** adını kullan. Eski sistem notları yeni sistemin notlarıyla birlikte incelenerek iş yürütülür. Bu ayrım tüm sonraki sohbetlerde ve GitHub işlemlerinde korunmalıdır.


## YENI SOHBETE KESIN DEVIR — 20 Ekim 2026 (son guncelleme)
Kullanici istegi: Bu sohbetin tum onemli taleplerini, kararlarini, yapilanlari, yapilacaklari ve hatalardan cikarilan dersleri yeni sohbette kaybetmeden devam ettir. Kullanici, tekrar tekrar anlatmak zorunda kalmasindan ve besli sistemin parca parca gelistirilmesinden rahatsiz. Bu devir ozetidir; butun sohbetlerin kelimesi kelimesine kopyasi oldugu iddia edilmez.

### Ilk okunacaklar ve baglayici kurallar
1. BIRLESIK_KALICI_CALISMA_KURALLARI.md — 20 maddelik ilkelerle birlikte eski/yeni kaynak inceleme, besli capraz entegrasyon, notlardan gecmis hata ogrenme, veri koruma ve kanit disiplini. Olusturma commit 8aad8b00ff77a093bf2ef3bfef1d3fe4de7ad44d.
2. PROJE_HAFIZASI.md — merkezi tarihli karar ve ilerleme defteri; ilk 8 kural commit 3ccb0a4e3ed0f1ba744d1b963240d844ddc7ad2a; 12 ek kural commit 3d5ceb5867e139f3bb713dddb05e33710eccc341; birlesik belge indeksi commit ce1ea123c1bd667afaa8a89740915f8d13efea51.
3. ESKI_SISTEM_NOTLARI.md ve docs/eski_depo_not_arsivi/ altindaki ilgili ozgun notlar; AGENTS.md, DEVAM_NOTU.md, 810 dosya notu.md, GUVENLIK_KURALLARI.md, BES_SISTEM_TOPLU_IS_DEFTERI.md, BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md ve gorevle ilgili tum diger eski/yeni notlar.
4. Bu SOHBET_DEVIR_NOTU_2026-10-20.md ve mevcut kod, test, Actions kayitlari.

### Kullanici kararlarinin ozeti
- Yeni sistemin adi ve deposu YALNIZ Madsc55-Tv / Madsc55/Madsc55-Tv. Eski Madsc55/madsc-tv salt okunur kaynak. Isimleri karistirma.
- Her gorevde etkilenen K1 guvenlik, K2 kesif/gecmis, K3 kanal test/IBO/EPG, K4 yedek/restore, K5 bakim/koordinasyon islerini BIRLIKTE uygula ve birlikte dogrula. Sadece bir K'de minik test yapmak veya bes CI isinin yesil olmasi gercek capraz entegrasyon degildir.
- Her ise ilgili ESKI VE YENI notlari okuyarak basla. Notlarin asil amaci gecmis eksikleri, yanlislari, tekrar eden isleri ve alinmis kararlari anlamak ve yeni sistemde bunlari duzeltmektir. Onceden yapilan incelemeleri tekrarlama. Okunmamis belgeyi okunmus gosterme.
- Sohbetten sohbete karar, talep, yapilan/yapilacak/yapilmayacak, risk, kanit ve siradaki somut isleri tasiyacak notlari tut. Her sohbetin otomatik eksiksiz goruldugunu iddia etme.
- Kullanici toplu, gercek uygulama ve kabul istiyor; tekrar tekrar kucuk test/commit ve sadece plan/soz istemiyor. 'Soz degil kanit' — commit SHA, Actions sonucu, artifact, davranissal kabul ayrimini goster.
- Korunan playlist, EPG, logo, arsiv, cihaz favorileri ve kullanici IBO calisiyor kararlarini koru; izinsiz canli yazma/silme yapma.
- Eski sistemin TUM gercek notlarini ve kararlarini yeni sistemde ESKI_SISTEM_NOTLARI.md adli TEK TAM METIN dosyada birlestirme ACIK ONCELIKLI IS. Simdiki dosya indeks; tam fiziksel birlesme degil. 45 metin + 25 JSON/CSV arsiv kaynagi SHA ile korunuyor; kalan yapilandirilmis kayitlar siniflandirilacak, kaynak butunlugu kanitlanacak; dogrulanmadan kaynak silinmeyecek. Onceki buyuk GitHub dosyasi engellerini guvenli parcalama ile coz.

### En son teknik ilerleme ve kanit
- K1 write_path_audit.py casefold-duplicate korumasi; commit f4b7e83ff829e18c7d2335b806508e0e1fdfc7cb; CI 39349540574 SUCCESS. Gercek yazma kapisina tam baglandigi kanitlanmadi.
- K2 history_real_source_publish.py SHA256 kaynak/cikti dogrulama ve kaynak degisirse fail-closed; commitler 0fbd349849e047191119f52407efe64f40542a76 ve 340a37a6e10353e37c2829a86c9f98c5acba3f89; test 3256d9ab4f2a265b91cd7ccd67e57549b6d2ffb9; CI 39350454947 SUCCESS. Gercek bagimsiz dogrulanmis kaynak yok; uretim kabul yok.
- K4 madsc/restore_drill.py gercek izole backup + restore + SHA256 dogrulama; commit 5f88dd9e4e1b50d2e7dcf61affcd8b386a45a51a; test ff0be3425165faf7bcce075e42974d3cd4aad624; madsc-05-bakim.yml entegrasyon commit 51b8730cca605dacbdeec7ab16fed065f029ca20. Actions 39350699732 COMPLETED SUCCESS, https://github.com/Madsc55/Madsc55-Tv/actions/runs/39350699732. Bu yalniz izole CI restore tatbikatidir; harici depolama veya gercek uretim restore kaniti degildir.
- Eski 99 YAML ilk kaynak envanteri var; 92 davranissal esdegerlik KABUL 0/92; 26 guvenlik runtime kabul 0/26. Yesil fixture CI bu sayilari degistirmez.
- Eski notlar birlestirme artifact'i 70 kaynagi kapsamis, fakat main'deki ESKI_SISTEM_NOTLARI.md tek tam metin degil. Birlestirme hala ACIK.

### Yeni sohbetin somut is sirasi
1. Yukaridaki belgeleri, ilgili ozgun eski/yeni notlari ve kodu oku; gecmis hata ve eksik matrisini cikar, daha once tamamlanan arastirmayi yeniden baslatma.
2. K1–K5 etkilerini birlikte kapsayan tek bir gercek orkestrasyon/entegrasyon is paketi uygula; K1 yazma kapisi, K2 kesif/gecmis, K3 test/IBO korumasi, K4 gercek izole restore, K5 fail-closed toplu kabul arasindaki baglantilari somut kod ve toplu testle kanitla. Gercek uretim kaniti olmayan noktalari ayri acik tut.
3. Eski notlarin tam metin tek dosya birlestirmesini, kalan JSON/CSV karar kayitlarini ve kaynak hash/tamlik kontrolunu bitir; arsiv kaynaklarini silme.
4. 92 davranissal esdegerlik ve 26 runtime guvenlik kabulunu gercek kanitlarla ilerlet; kanit olmadan tamamlandi deme.
5. Tum ilerlemeyi PROJE_HAFIZASI.md'ye kaydet ve bir sonraki sohbete tekrar devret.
