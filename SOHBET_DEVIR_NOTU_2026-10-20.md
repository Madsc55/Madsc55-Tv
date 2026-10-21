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


## 20 Ekim 2026 — YENI SOHBET DEPO KIMLIGI EK KURALI (KALICI)
- Kullanici eski ve yeni depolarin karistirilmasina kesin olarak itiraz etti. **Yeni yazilabilir proje yalniz `Madsc55/Madsc55-Tv` / `main`**. Eski `Madsc55/madsc-tv` / `madsc/bes-sistem-toplu-birlestirme` salt-okunur kaynak; acik izin olmadan eski depoda test/commit/workflow tetikleme yasak.
- `BIRLESIK_KALICI_CALISMA_KURALLARI.md` dosyasina mevcut 20 ilkeyi koruyan **EK KALICI KURAL 21** commit `67fc2135f80c7d82ae5a8764125e20af7cf6e97f` ile eklendi.
- Yeni sohbetin ilk islemi dogru depo/dal kimligini ve dort merkezi notu okumak; eski Actions testini yeni sistem kaniti diye sunmamak. Yeni sistem K1–K5'i eski notlar ve yeni notlarla birlikte gelistirmek, toplu kanitlamak. 0/92 davranissal esdegerlik ve 0/26 runtime guvenlik kabul sayaci kanitsiz degistirilmeyecek.
- Onceki hatanin kaydi: asistan yanlislikla eski `Madsc55/madsc-tv` dalina `87397714bd88ee02d75c51a22c2b8152b6ddd5b6` test commit'i yazdi. Bu **yeni sistem ilerlemesi degildir**; eski depoda yeni islem yapilmayacak.


## 8. 20 Ekim 2026 - SON SOHBET DEVRI: MUTLAKA OKU
- Kullanici yeni sohbette hicbir karar, kural, yapilan is, yapilacak is veya eski notun kaybolmamasini istiyor. Yeni sohbet ilk is bu dosya, BIRLESIK_KALICI_CALISMA_KURALLARI.md (20 ilke + 21. depo kimligi), PROJE_HAFIZASI.md, ESKI_SISTEM_NOTLARI.md, ilgili docs/eski_depo_not_arsivi/ kaynaklari, eski AGENTS/DEVAM/810 ve BES_SISTEM notlarini okumali. Okunmamis kaynak okunmus gibi sunulmaz. Once tamamlanan kaynak incelemesini tekrar etme; ilgili eksik kaynaklari ac.
- YALNIZ YAZILABILIR: Madsc55/Madsc55-Tv main. ESKI Madsc55/madsc-tv madsc/bes-sistem-toplu-birlestirme SALT OKUNUR. Kullanici onaysiz korunan CALISANLAR, YENILER, YEDEKLER, HEPSI, FAVORILER, playlist.m3u8, xmltv.xml, epg, logos/logolar, arsiv, cihaz favorileri, PR #71, cron veya eski workflow degisikligi yok.
- Besli sistem birlikte gelistirilir: K1 izin ve fail-closed guvenlik; K2 aday kesfi, fingerprint, tarihce; K3 kanal/ffprobe, ses/video, EPG/logo, IBO; K4 bagimsiz yedek ve geri yukleme; K5 koordinasyon, rapor, tek toplu kabul. Her is paketinde K1-K5 capraz etkilerini kontrol et. 99 YAML'i kopyalama, 92 davranisi bes sisteme gercek islevleriyle tasima. Tek tek kucuk commit/test yerine iliskili isleri toplu commit ve toplu CI yap.
- K2-K3-K5 ayni run_id, commit_sha, digest, aday sayisi ve url_sha256 capraz kanit zinciri calisiyor. K3 ffprobe ornekleri HALA SENTETIK; gercek yayin, canli sureklilik ve IBO cihaz kaniti YOK. K4 bagimsiz harici restore ve 26 runtime kural kabul kaniti YOK. Offline yesil Actions = uretim kabul degildir.
- Son basarili Actions: https://github.com/Madsc55/Madsc55-Tv/actions/runs/39413388267 (SUCCESS, SHA 81eb43be). Onceki 39412769302 SUCCESS. Ara commit kosulari iptal veya basarisiz olabilir; son basarili run esas alinir.
- Yeni madsc/progress_scorecard.py (commit 27ed5318), testler (868959f2), K5 workflow artifact entegrasyonu (81eb43be). PROJE_HAFIZASI.md son guncelleme commit 61ba08723334a9d0c8d6353046310c0c6c4d0d28. K5 ilerleme JSON artifact'i kaynak envanterini ve kabul sayaclarini ayri tutar.
- Genel %47 tamam / %53 kalan SADECE TARIHSEL REFERANS, her commit sonrasi hesaplanan gercek oran DEGIL. Kaynak envanteri: 99/99 YAML, 130/130 Python kaynak, 68/68 test dosyasi ilk inceleme. 92 eski davranistan DOGRULANMIS davranissal esdegerlik 0/92; 26 runtime guvenlik kabul 0/26. 26 hedefe karsin arivdeki GUVENLIK_KURALLARI.md sadece 24 numarali madde iceriyor; iki maddeyi uydurma. Yeni kanit olmadan yuzdeyi artirma, ama ilerlemeyi ayrik raporla.
- SIRADAKI SOMUT IS: (1) K1-K5 toplu CI son durumunu kontrol et. (2) Eski kaynak betik ile yeni esdegerini izole sentetik girdilerle gercekten calistirip diferansiyel davranissal test kur; eski kodu ve korunan dosyalari degistirme. (3) K2 adaylari icin guvenli, yetkilendirilmis, salt-okunur GERCEK teknik olcum toplama ve kaynak/provenance dogrulamasini K3/K5'e bagla; canli kanal kimligi/IBO kabulunu ayri tut. (4) 92 davranisin kabul matrisi, 26 guvenlik maddesi runtime kaniti, K4 harici backup/restore. (5) Her paket sonunda gercek commit, CI run, artifact ve eksikleri PROJE_HAFIZASI.md'ye kaydet.
- Bu devir ozeti sohbetlerin birebir tam transkripti DEGIL. Tam sohbet otomatik eksiksiz okunmus sayilmaz. Yeni sohbetin basinda once dosyalardan kanit topla, kullaniciya eski kararlarini tekrar anlattirma.


## ZORUNLU AD VE DEPO KIMLIGI KONTROLU - 20 Ekim 2026
- Yeni sistemin TAM ve TEK dogru adi: **Madsc55-Tv**. GitHub sahibi/deposu: **Madsc55/Madsc55-Tv**. Yazilabilir tek dal: **main**.
- **Madsc-Tv**, **MADSC TV** veya **Madsc55/madsc-tv** yeni sistemin adi/depusu olarak kullanilamaz. Kisa, eksik veya eski adla proje tanitma; yeni sohbet baslik ve cevaplarinda **Madsc55-Tv** yaz.
- **Madsc55/madsc-tv** eski depodur; **madsc/bes-sistem-toplu-birlestirme** dali da dahil kesinlikle salt okunur. Kullanici acik izin vermedikce eski depoda commit, dosya degisikligi, Actions tetikleme veya workflow duzenlemesi YASAK.
- HER YENI SOHBETTE ilk GitHub yazma isleminden ONCE hedef repository_full_name=Madsc55/Madsc55-Tv ve branch=main oldugunu acikca dogrula. Adlar birbirine benziyor diye eski depoya yazma. Yanlis hedef saptanirsa yazma islemini durdur.
- Bu madde mevcut 21 kurali guclendirir; onceki korumalari kaldirmaz. Yeni sohbete devirde aynen korunur.



## YENI SOHBET DEVRI — 20 Ekim 2026 gece

Tek yazilabilir proje Madsc55-Tv, repo Madsc55/Madsc55-Tv, dal main. Eski Madsc55/madsc-tv ve madsc/bes-sistem-toplu-birlestirme SALT OKUNUR; Madsc55-Tv-Test'e dokunma. Ilk yazmadan once repo/dal kimligini dogrula.

Yeni sohbette once BIRLESIK_KALICI_CALISMA_KURALLARI.md (21 kural), PROJE_HAFIZASI.md, ESKI_SISTEM_NOTLARI.md, bu devir dosyasi ve ilgili arsivleri oku. Tum gecmis sohbetleri eksiksiz okudugunu iddia etme. K1 guvenlik, K2 kesif/gecmis, K3 kanal/EPG/logo/IBO, K4 yedek/restore, K5 orkestrasyon/rapor. Canli listeler, playlist.m3u8, xmltv.xml, epg, logolar, arsiv, FAVORILER, HEPSI, YEDEKLER ve PR #71 korunur. IBO onayli kanal otomatik silinmez.

Actions 2000/2000 kota dolu; sifir butce, kart yok. Onay ve kota olmadan workflow tetikleme; commitlerde [skip ci]. Kabul 0/92 eski davranis ve 0/26 runtime guvenlik. 99/99 YAML ilk envanter, 23/99 derin YAML, 130/130 Python, 68/68 test ilk envanter; %47/%53 tarihsel, gercek guncel ilerleme olcumu degil.

Bu sohbetlerde K1 K5 izole rapor yazimina baglandi; K4 bozuk restore negatif kontrolu; K2 real-source publisher ve verified-history pipeline K1 kontrolleri; K1 tam yerel cikti yolu kontrolu ve negatif testleri eklendi. Commitler: 6d32290d, 370608e6, bddf8f95, ccdb2576, 9c63d291, 03ec9f4e, 27a21ac7, 34c2cae4. PROJE_HAFIZASI.md son kaydinda bunlardan sonra verified-history traversal onarimi 6432d44d ve test dc68f298 da var. Kodun guncel GitHub main halini tekrar dogrula.

KRITIK: Guncel main icin offline toplu regresyonun gectigi kanitlanmadi. Yerel eski kopya guncel main sayilmaz; DNS nedeniyle dogrudan klon sorunu bildirildi. K1 tam yol on-kontrolu atomik guvenli yazma garantisi degil; TOCTOU, tum bagimsiz yazicilar ve repo kok siniri hala acik. Test calistirmadan yesil deme.

SIRADAKI: (1) kaynaklari ve kurallari dogrula, (2) guncel main'i izole ortamda ucretsiz offline toplu test et, (3) hatalari duzelt ve K1 yazicilarini sertlestir, (4) 92 eski davranisin diferansiyel esdegerligi ve 26 runtime guvenlik kabulunu gercek kanitla ilerlet, (5) K2/K3/K4/K5 gercek butunlesik kanitlarini olustur. Her degisikligi PROJE_HAFIZASI.md'ye commit SHA ile kaydet.


## SOHBET KAPANISI — 20 Ekim 2026, yeni sohbete aktarım
- Kullanıcı sohbet dolduğu için yeni sohbette hiçbir önemli iş/karar kaybolmadan devam edilmesini istedi. Doğru proje **Madsc55-Tv**, tek yazılabilir depo **Madsc55/Madsc55-Tv**, dal **main**. Eski depo kesinlikle salt okunur.
- Bu sohbetin son teyitli GitHub kod işleri: K1 `enforce_local_output_path` tam yol koruması, eksik `Path`/`tempfile`/guard import onarımları, `..` yol geçişi negatif testi, K2 gerçek geçmiş kaynak yayımlayıcısı ve doğrulanmış geçmiş akışına K1 ön kontrolü. Son güvenlik değişikliği `34c2cae4661e75ed0d982e8f23c7bf6b2e511876`, ilgili test `27a21ac7c75502a78f6a0bdbd2fef453a11c42a4`, hafıza `5a812a2b7820529dc1ca374852c57a1cc3b2e037`. Diğer sonradan eklenen işler için `PROJE_HAFIZASI.md` ve git main geçmişini ayrıca doğrula; bu satır tüm yeni commitlerin sonuncusu olduğu iddiası değildir.
- Kritik borç: **güncel main toplu offline regresyonu çalıştırılmış/başarılı değil**; önce güncel kaynakları doğrula, GitHub Actions kullanmadan ücretsiz yerel test et. İkinci borç: tüm gerçek dosya yazıcılarının merkezi K1 koruması, TOCTOU ve repo sınırı. Üçüncü: eski 92 workflow'un davranışsal eşdeğerliği 0/92, 26 runtime güvenlik kabulü 0/26; sayıları test kanıtı olmadan değiştirme.
- Actions 2000/2000 kota dolu; bütçe sıfır, kart yok, onaysız workflow tetikleme yok; commit mesajlarında `[skip ci]`. Üretim listeleri, EPG, logolar, yedekler, arşivler, IBO onaylı kanallar, PR #71 dokunulmaz. 21 birleşik kural, AGENTS, 810 ana/alt ve diğer arşiv notlarını kaynaklarıyla okuyarak ilerle; tamamını okuduğunu kanıtsız söyleme.
- Yeni sohbette ilk mesaj: 'Madsc55-Tv projemize GitHub main'deki SOHBET_DEVIR_NOTU_2026-10-20.md ve PROJE_HAFIZASI.md dosyalarını, BIRLESIK_KALICI_CALISMA_KURALLARI.md kurallarını okuyarak kaldığımız yerden devam et. Önce güncel main offline regresyonunu çöz; Actions tetikleme, üretime dokunma.'


## EK DEVIR NOTU — 21 Ekim 2026: kanal arama, sunum ve kategori kararları
- Kullanıcı kesin olarak istedi: K2 kanal keşfi, K3 test, EPG/logo eşleştirmesi ve K5 liste hazırlama tek bütünleşik akış olacak. Aranan kanalların gerçek/orijinal logoları bulunacak, kimlik ve erişim doğrulanmadan logo kesinleştirilmeyecek.
- Kanal görünen isimleri BÜYÜK HARF olacak (Türkçe harfler dahil); teknik olarak ölçülmüş çözünürlük etiketi SD/HD/FHD/QHD/4K eklenecek; ölçülmeyen çözünürlük tahmin edilmeyecek.
- Eski sistemdeki kategori adları, sırası ve düzeni korunacak. ÇALIŞAN, ÇALIŞMAYAN, YABANCI ve IBO PLAYER'DA ÇALIŞTIĞI KULLANICI TARAFINDAN ONAYLANAN kanallar ayrı sınıflandırılacak. Eski çalışan kanallar da teknik testlere dahil edilecek; IBO onaylı çalışan kanal geçici teknik başarısızlıkla silinmeyecek.
- Adaylar için üç aşamalı, aralarında en az altışar saat bulunan test planı ve IBO cihaz kabulünün teknik probe'dan ayrı tutulması gereklidir. Bunlar henüz gerçek üretim kabulü değildir.
- Gerçek GitHub main kodu: madsc/channel_presentation.py (commit 5bacc751dd9a5f28200fd01cd9fd9bfef5fcff83) ve tests/test_channel_presentation.py (c3ca362812cbe0abb416bb0f20c19125c24ce0b6). Mevcut modül yalnızca sağlanan ölçüm/logo kanıtlarını işler; kendi başına logo aramaz, yayın test etmez, M3U oluşturmaz, üretim listesine yazmaz. Bu entegrasyonlar AÇIK GÖREVLERDİR.
- Ortak K1-K5 rapor yazma koruması core.py commit 6276d524bef18a19ad730b3de36decb0398ea866 ve satır sonu düzeltmesi 079707f8d5d4379c152b3e9ccf887941b3ac0e8c; regresyon testleri bf62ffe87d675aec9cf88ae5efa93c6845faa58a. K5 görev sayımı commitleri 5269bbc1d4a96fbd9fe3443a82d6c73b097b6d47, 14a1ec13ab30958f8228e2f7fe3c8994b3bcd198, b09db057eda849ff54ff714a7a54eaa7ceb1654b.
- Test stratejisi: Kod entegrasyonlarını topluca tamamla; ücretsiz OFFLINE toplu test ve regresyonu yap; Actions kotası yenilenirse kullanıcının onayıyla TEK MERKEZİ toplu GitHub Actions doğrulaması yap. Şu an Actions 2000/2000 dakika, bütçe sıfır; Actions tetikleme.
- Korumalar: Eski depo salt okunur; canlı M3U listeleri, IBO onaylı kanallar, EPG, logo klasörleri, arşiv ve yedekler değiştirilmeyecek. Üretime yalnızca açık onay ve gerçek kabul kanıtıyla geçilecek.
- Dürüst ilerleme: 22 görev defterinde 5 in_progress, 17 pending, 0 completed. 92 davranışsal eşdeğerlik 0/92, 26 runtime güvenlik kabulü 0/26. Güncel main toplu regresyonu henüz doğrulanmadı. 12 günlük hedef kullanıcı isteği; teslim garantisi değildir.
- SONRAKİ ADIM: Yeni kanal sunum modülünü K2 discovery ve K3 probe/IBO akışına bağla; gerçek logo kaynak eşleştirmesi, kategori dönüşümü ve salt okunur ayrı M3U taslaklarını uygula. Eski kategori sıralamasını gerçek eski sistem dosyalarından doğrula; varsayma.


## 21 Ekim 2026 — beş otomasyon sınırı ve K2/K3 ilerlemesi
- KULLANICI KARARI: Sistem yalnızca BEŞ ana otomasyondan oluşacak (K1 güvenlik, K2 kanal keşfi/logo adayları, K3 kanal test/EPG/IBO doğrulama, K4 yedekleme, K5 bakım/koordinasyon/liste taslakları). Yardımcı Python modülleri bağımsız workflow veya altıncı otomasyon değildir. 92 eski görevin işlevleri bu beş ana yapıya aktarılacak; davranışsal eşdeğerlik henüz doğrulanmadı.
- Kanal adları Türkçe İ/I kurallarıyla büyük harf: madsc/channel_presentation.py commit 5defd45884bd241fafca2c1f165b85786522da03, test b2cbc6945417dcadf9708bca8cebad7182042cfa.
- madsc/channel_catalog.py K2 discovery -> kanal sunumu/IBO/logo/ölçüm bağlantısı commit c525bba6a276dba7d553a4fae398a096a3269301; test f6da4ed99f68566234bc195ba217d7cdc4c71e5d.
- K3 evaluate_probe üzerinden doğrulanmış teknik durum entegrasyonu commit 181e51d5b2b322aacff51d3b9e2bd1b727c74440; test d20cea8b4e54c871b6565594250cbc06c8f0264a. Teknik durum sadece verilen probe kanıtından gelir; kod canlı test YAPMAZ. IBO kullanıcı onayı ayrı ve korunur.
- Açık işler: gerçek eski kategori isim/sıra kaynaklarıyla tam eşleştirme, gerçek logo arama/kimlik doğrulama, 3 aşamalı zamana yayılmış teknik test, ayrı M3U taslakları, beşli workflow bağları ve tüm main için ücretsiz offline toplu regresyon. Actions çalıştırma, canlı listelere yazma.


## 21 Ekim 2026 — K5 M3U taslak entegrasyonu
- K2/K3 katalogda yabanci kanal fingerprint ile probe kaniti verilmesi engellendi: madsc/channel_catalog.py 7d3baf9af000d41141dda0ad5340ea569938efbb; test fa4986420752135a6e39ec8234f44ce96c595f0f.
- K5 madsc/playlist_previews.py salt okunur bellek ici 5 ayri taslak olusturur: IBO_ONAYLI_CALISAN, CALISAN_ADAY, CALISMAYAN_ADAY, YABANCI, TEST_BEKLIYOR. Mevcut eski group-title metadata'sini korur, buyuk harf gorunen ad ve dogrulanmis logo alanlarini tasir; kaynak URL fingerprint eslesmesini zorunlu kilar, M3U metadata enjeksiyonunu reddeder. Commitler 69ac99355d596e4dd8ffdfef9f99aebc93d6f7e7, ded0334e464ef80a7af0fa60ba49b17c907d66a0; test 06f3c1293fed36e7666c2305da3a9025855bd07a.
- Bu BES TASLAK DOSYASI bes AYRI OTOMASYON degildir. K5 yardimci fonksiyonu dosya YAZMAZ, canli listeleri DEGISTIRMEZ, kanal probe/IBO cihaz testi YAPMAZ. Eski kategori ad/sira tam kabul ve canli logo aramasi halen acik. GitHub Actions ve guncel main offline tum regresyon calistirilmadi.


## 21 Ekim 2026 — tek K2/K3/K5 kanal akis girisi
- madsc/five_system_channel_flow.py: build_offline_channel_previews() K2 discovery, K3 supplied probe/IBO/logo/olcum kanitlari ve K5 bellek ici M3U taslaklarini TEK cagriyla birlestirir. Commit 06a154f7554e0b6dce2a96765998f6e7a837422e; entegrasyon testleri tests/test_five_system_channel_flow.py commit ba7c17dbd557727275cd9633bd052286eb611584.
- Beş ANA otomasyon siniri korunur. Bu Python fonksiyonu yeni workflow degildir. K1 uretim yazma yasagi, K4 onizlemede yedekleme baslatmama, IBO onayli kanali teknik hataya ragmen koruma, eski group-title metadata'sini saklama ve test bekleyenleri ayri tutma test dosyasina islendi.
- Test dosyalari GitHub main'e eklendi ancak offline toplu regresyonun CALISTIGI/GECTIGI henüz kanitlanmadi. Gercek kaynak logo aramasi, EPG ve eski kategori tam esdegerligi, canli 3 asamali test ve IBO cihaz onayi bekliyor. GitHub Actions tetiklenmedi, uretim listelerine dokunulmadi.


## 21 Ekim 2026 — az calisilan K4/K1 geri yukleme guvenlik baglantisi
- Kullanici ekran goruntusundeki 5 kademe tablosuna gore en az ilerlenen isi, bagli gorevleriyle birlikte bitirmeyi istedi. K4 bagimsiz restore kaniti ve 92 eski davranis esdegerligi en buyuk aciklar arasindadir. 92/92 HEDEF, gecerli kabul 0/92.
- madsc/k4_restore_gate.py commit 43940302fccf516d8c19eb4b1540f2743687436b: uc farkli mevcut sandbox klasorunde source/backup/restored hash ve byte boyutu karsilastirmasini madsc.backup.verify_independent_restore ile yapar, mismatch halinde HALT_AND_INVESTIGATE verir. Uretime yazmaz, gercek dis depolama kaniti ve production restore onayi vermez.
- tests/test_k4_restore_gate.py commit 02a8931c769a0bc53b76bd8e4a3b6dc7a0c338c6: eslesen kopya, bozuk kopya, ic ice klasor red senaryolari. Dosya commitleri gercektir; testler henuz calistirilmis sayilmaz.
- Devam: ucretsiz guncel main offline toplu regresyon, K4 gercek bagimsiz harici depolama ve restore kabul kaniti, K1 runtime 26 kural ve eski 92 davranis esdegerlik matrisi. Actions tetikleme, uretim listelerini degistirme.


## 21 Ekim 2026 — K4 manifest güvenlik onarımı
- madsc/backup.py, control karakterli ve supheli kaynak dosya yollarini reddeder; verify_manifest ayni path'in tekrarini kabul etmez. Commit d170404c44a8a4d64cf2f4825e733003999bdfca.
- tests/test_backup_manifest_hardening.py: kontrol karakteri, tekrar eden manifest girdisi, normal manifest kabul testi. Commit 36be2ea87c0778141eabe6ea14b588c3d40958cc.
- Bunlar gercek main commitleridir. GitHub Actions calistirilmadi, guncel main toplu offline test sonucu henuz yok. Eski repo ve uretim listeleri degistirilmedi. K4 gercek harici restore ve 92/92 esdegerlik hala tamamlanmadi.


## 21 Ekim 2026 — K4 rapor yazicilarina K1 guvenlik baglantisi
- Repo tree incelemesinde madsc/restore_drill.py ve madsc/k4_evidence.py rapor cikisinda mkdir ve write_text kullaniyordu. K1 enforce_local_output_path + open('x') on kontrol/ozel yeni dosya olusturma eklendi. Commitler e9dc9103805a81908a872d10e0de5b29a85ae521, 5ff86c1f2861778c1310126908237d42c46b43be.
- tests/test_k4_report_output_safety.py: mevcut restore raporunu ezmeme ve CALISANLAR.m3u korumali hedefini reddetme senaryolari. Commit cfee0332b3e3bd43c5bf15b6ca89cff4e5d7b460.
- On kontroller TOCTOU/tum bagimsiz yazicilar icin tam guvence degildir; global 26 runtime kabul ve 92 davranissal esdegerlik tamamlanmadi. Testler commit edildi, fakat guncel main toplu offline regresyonu calistirilmis degildir. Actions tetiklenmedi; uretim listelerine dokunulmadi.


## 21 Ekim 2026 — K4 kanit girisi symlink guvenligi
- madsc/k4_evidence.py artik kanit dosyasinin ust klasorlerinde symlink olmasini da reddeder; commit 26288a26904103e9e0dfe4d2ba3a833efbb7ccdb.
- tests/test_k4_report_output_safety.py symlink ust klasor testini kapsar; commit d5d37aaef6554fb8c5c00bc8d1abb92cfba54ee7.
- Bu iki commit testleri CALISTIRMAZ; guncel main offline toplu regresyon hala calistirilmis degildir. K1 26 runtime kabul ve 92 legacy davranissal esdegerlik tamamlanmadi. GitHub Actions ve canli yayin dosyalari degismedi.


## 21 Ekim 2026 — K3 uc asamali test kaniti
- madsc/k3_three_stage_gate.py commit 3c0b5a7377e669d755cea3c6cd0fee7b1326d945: tek kanal fingerprint'i icin tam uc supplied probe, UTC zaman damgasi ve ardarda >=6 saat fark kosulu; tum uc sample preliminary pass degilse uc asamali preliminary kabul yok.
- tests/test_k3_three_stage_gate.py commit 3ba405dc4b278f6f935493885813e165c9fd1b74: normal uc ornek, yetersiz sure, farkli kanal, basarisiz test, timezone olmayan timestamp senaryolari.
- Modul CANLI yayin test ETMEZ, cihaz IBO onayi vermez, timestamp kaynagini bagimsiz dogrulamaz, zamanlayici veya yeni otomasyon olusturmaz. Guncel main toplu offline regresyonu hala CALISTIRILMADI; gercek 92/92 ve 26/26 kabul 0.


## 21 Ekim 2026 — K3 uc asamali kanit K2/K5 baglantisi
- madsc/channel_catalog.py, istege bagli three_stage kanit haritasi alir, her kanal icin assess_three_stage_probes() ile dogrular, fingerprint karismasini reddeder. Teknik status hala bagimsiz tek probe kanitindan gelir; uc asamali supplied veri tek basina CALISAN yapmaz. Commit 0ef172394050f6429cdb0a95dc8f0631ad372f12.
- madsc/five_system_channel_flow.py three_stage parametresini K2/K3 kataloga aktarir; commit f7a0398f469ef82950c6d7ef5d572c2877db0371.
- tests/test_five_system_channel_flow.py iki entegrasyon senaryosu: uc asamali preliminary sonuc uretim kabulune donusmez; yanlis kanal fingerprint reddedilir. Commit 2dccf629fff2b44362f8820dcd5436ec1fed60af.
- Gercek uc asamali CANLI testler, IBO cihaz onayi ve main offline toplu regresyon henuz yapilmadi. 5 otomasyon siniri korundu; Actions ve canli listeler degistirilmedi.


## 21 Ekim 2026 — K1-K2 URL kontrol karakteri engeli
- madsc/discovery.py normalize_url, ham URL'deki ASCII kontrol karakterlerini urlsplit/strip oncesi reddeder; commitler bf1c967b4089868d696c6a61ff3ba12ed30e95d3 ve 2746cbf9a61051a94cbee1bb5e3cbc8c17a6ea6c.
- tests/test_discovery.py M3U satir enjeksiyonu, CR/LF/TAB ve katalog reddi regresyonlarini kapsar; commit a917cce0b7e64c6d236384488bd6e7060b743522.
- Kod commitleri gercektir; guncel main toplu offline test calistirilmadi. 92 eski davranis esdegerligi, 26 runtime guvenlik kabul ve harici restore aciktir. Actions calistirilmadi, uretim listelerine dokunulmadi.


## 21 Ekim 2026 — gercek yerel K3 offline test yurutu
- Container /mnt/data/madsc_current_k3 icinde K3 uc-asama modulunun kaynak kopyasi ile bes unittest gercekten calistirildi: Ran 5 tests, OK (5/5).
- madsc/k3_three_stage_gate.py yerel git hash-object fe33fbc5f43d1b4eec5900767ac5edd5f5591b3c; GitHub main tree SHA ayni. Diger kopyalanan kaynak/test dosyalarinin SHA'lari main ile esit oldugu kanitlanmadi; bu nedenle tum main testi veya tam K3 test kabul sonucu DEGILDIR.
- GitHub'a dogrudan git clone DNS basarisiz (github.com host resolve edilemiyor). Testler yalniz izole yerel K3 kopyasinda, Actions/network probe/production yazmasi olmadan calistirildi.
- Siradaki kritik is: guncel main'in eksiksiz kaynak ve test kopyasini olusturup SHA eslesmesini dogrulamak; python -m madsc.offline_gate ile tam regresyonu calistirmak. 92/92 ve 26/26 kabul degismedi.


## 21 Ekim 2026 — K4 buyuk dosya bellek siniri
- madsc/backup.py snapshot_manifest: read_bytes ile tum dosyayi RAM'e alma kaldirildi; 1 MiB bloklar ile streaming SHA256 ve byte sayimi yapiliyor. Commit 830e7aa3fb470314873aa77bb6a66df07f54c3df.
- tests/test_backup_manifest_hardening.py: 1 MiB'den buyuk dosyada hash/byte eslesmesi ve sonradan degisen baytin tespiti. Commit 4c658fc2e7c105418361edc520e8a7f173ba154e.
- Testler GitHub main'e yazildi fakat guncel main K4 testleri veya toplu offline regresyon henuz CALISTIRILMADI. Eski 92 davranis kabul 0/92, 26 guvenlik runtime kabul 0/26. GitHub Actions yok, eski repo ve canli playlist degisikligi yok.


## 21 Ekim 2026 — K4 manifest testleri gercekten calistirildi
- GitHub main madsc/backup.py blob SHA 6f4bacbc759fb3da24ca143d69eb7d3656b1a50b ve tests/test_backup_manifest_hardening.py blob SHA e73a7c724532b4c1e2760b9f3aed6effee35b0fe. /mnt/data/madsc_k4_offline/ altinda birebir kopyalarin git hash-object ciktilari ayni.
- python -m unittest discover -s tests -v: Ran 4 tests, OK. Testler kontrol karakteri, yinelenen manifest girdisi, cok bloklu hash/tahrifat ve normal manifest senaryolaridir. Yalniz bu iki main dosyasi icin dogrulanmis lokal K4 alt-kume testidir.
- Ayrica onceki /mnt/data/madsc_current_k3 lokal 5 test tekrar calistirildi: Ran 5 tests, OK. Ancak tam main repo test paketi indirilemedi/kurulamadi; tam K1-K5 offline gate calistirilmadi. 92/92 davranissal ve 26/26 runtime kabul 0.
- GitHub Actions tetiklenmedi; uretim listeleri, eski repo ve canli URL'ler degistirilmedi.


## 21 Ekim 2026 — toplu test odagi ve gercek 9 offline test
- Yerel /mnt/data/madsc_batch_verified icinde K3+K4 icin python -m unittest discover -s tests -v calistirildi: 9 tests, OK (K4:4; K3:5). GitHub Actions, network probe ve production yazmasi yok.
- K4 madsc/backup.py SHA 6f4bacbc759fb3da24ca143d69eb7d3656b1a50b ve tests/test_backup_manifest_hardening.py SHA e73a7c724532b4c1e2760b9f3aed6effee35b0fe main ile AYNI. K4 dort testin guncel kaynak eslesmesi kanitli.
- K3 madsc/k3_three_stage_gate.py SHA fe33fbc5f43d1b4eec5900767ac5edd5f5591b3c ve tests/test_k3_three_stage_gate.py SHA 622873e54243558f5ea6961c5f2cea6dc4c3c059 main ile AYNI; ancak bagimli madsc/channel_test.py yerel SHA 6ad313c7c9f80625c2896aef648c16e5d3bdb2f1, main SHA fa2abdb2fe8b23805359b3312a65d30f468c4514; bu nedenle 5 K3 testi main tum bagimliliklariyla dogrulanmis sayilmaz.
- Tam main 81 test dosyasini ve tum bagimliliklari iceren eksiksiz offline gate henuz CALISTIRILMADI. 92/92 davranissal ve 26/26 runtime guvenlik kabul hala 0. Bundan sonra parcali yeni ozellikler yerine main'in SHA-dogrulanmis eksiksiz kopyasini ve tek toplu offline regresyonu ONCELIKLENDIR. Eski repo/canli listeler korunur, Actions calistirilmaz.


## 21 Ekim 2026 — toplu K1-K5 incelemesi ve K2-K3-K5 orphan evidence onarimi
- GitHub main recursive tree 14ffaf87906c45a728440ff8bc1b2ca3189d4c69 aninda 262 blob, 81 tests/test_*.py dosyasi ve 15 yml workflow goruldu. Bu 15 workflow eski depodaki 99 otomasyonla ayni envanter DEGILDIR.
- K2/K3 katalog denetiminde measurements/logos/ibo_results/probes icin bilinmeyen fingerprint reddi vardi, ancak three_stage haritasi kontrol disindaydi. madsc/channel_catalog.py bu besinci haritayi da ayni reddetme kuralina ekledi; commit 04393d734333aaa1a211d6182312866c65e0ad98. tests/test_five_system_channel_flow.py orphan three_stage regresyonu commit 7e35123973169f721643e09b2e06b3958bcdbffa.
- Bu son degisiklik icin main toplu offline regresyonu CALISTIRILMADI. Yerel git clone github.com DNS hatasi devam ediyor; eski 9 test guncel tum main kapsaminda kabul sayilmaz. Bundan sonra hedef main tum kaynak/test dosyalarini SHA ile dogrulanmis yerel kopyaya aktarip python -m madsc.offline_gate calistirmak; K1-K5 toplu hata listesi cikarip beraber duzeltmek.
- 92 legacy davranissal kabul 0/92, 26 runtime guvenlik kabul 0/26. Actions calistirma, eski repo ve production playlist yazma.


## 21 Ekim 2026 — K3 bagimlilik SHA uyusmazligi giderildi ve 9/9 gercek test
- /mnt/data/madsc_batch_verified/madsc/channel_test.py yerel kopyasi guncel main SHA fa2abdb2fe8b23805359b3312a65d30f468c4514 ile birebir eslendi (git hash-object dogrulandi).
- Ayni yerel ortamda python -m unittest discover -s tests -v tekrar CALISTIRILDI: Ran 9 tests in 0.020s; OK. K3 5/5, K4 4/4. Ilgili diger 4 modul/test blob SHA'lari onceki devir notunda dogrulanmisti. Test kapsaminda sadece bu 9 test var; tum 81 test dosyasini iceren guncel main tam regresyonu degil.
- Ayrica main katalogdaki orphan three_stage reddi kod/test commitleri 04393d734333aaa1a211d6182312866c65e0ad98 ve 7e35123973169f721643e09b2e06b3958bcdbffa. Bu yeni test 9 testin arasinda DEGILDIR.
- Gercek 92 legacy davranis kabul 0/92 ve 26 runtime guvenlik kabul 0/26. Actions, production playlist, eski repo degistirilmedi. Sonraki hedef tam main SHA-verified offline regresyon; eksik kaynaklar GitHub connector ile alinabilir ama container git clone DNS engeli suruyor.


## 21 Ekim 2026 — K1-K2-K5 metadata enjeksiyonu erken reddi
- madsc/discovery.py classify_candidates artik name, tvg_id, tvg_logo, group_title alanlarindaki ASCII control karakterlerini aday kabulunden ONCE reddeder; tek bozuk aday tum M3U preview islemini durdurmak yerine rejected'a girer. Commit d012589c33d030a94aa531701a3a105e4f599e96.
- tests/test_discovery.py dort metadata alani icin enjeksiyon reddi ve guvenli diger adayin kalmasi testi eklendi. Commit 18e168f18f9470516ecd0200f18d28f51e974dae.
- Son iki commit icin yeni testler HENUZ CALISTIRILMADI; tam main offline regresyonu hala yok. 92/92 behavioral acceptance 0, 26/26 runtime security acceptance 0. Actions ve canli liste yazmasi yok. Oncelik: eksiksiz SHA-dogrulanmis main kopyasi ve K1-K5 tum testleri topluca calistirmak.


## 21 Ekim 2026 — KULLANICIYA VERILEN BAGLAYICI SOZLER / YENI SOHBETE ZORUNLU DEVIR
Kullanici 12 gunluk parcali GitHub Actions denemeleri sonucu aylik 2000 dakika kotasinin tukendigini, buna ragmen sistemin bitmedigini ve her adimda ayri test/izin ile ugrastirilmak istemedigini belirtti. Asistan su sozleri verdi ve bu sozler BIRLESIK_KALICI_CALISMA_KURALLARI.md dosyasina da BAGLAYICI kural olarak yazildi:
1. Kullanici acik izin vermeden GitHub Actions ASLA calistirilmayacak; "devam" onay degildir; [skip ci] kullan.
2. K1-K5'in tum Python/guvenlik/entegrasyon testleri eksiksiz guncel main kaynagi ve bagimliliklari SHA ile dogrulandiktan sonra TEK TOPLU yerel offline regresyon olarak calistirilacak.
3. Hatalar toplu listelenip topluca duzeltilecek; her dosya icin ayri Actions yok; gereksiz kucuk test/izin dongusu yok.
4. CI ancak yerel testler gecip gercekten gerekiyorsa, kullanici acikca onaylarsa, job/sure/kota riski anlatilarak son asamada kullanilabilir.
5. Canli IPTV stream probe, production list/EPG/logo yazmasi, eski repo degisikligi yok; bunlar ayri acik onay gerektirir.
6. Kabul rakamlari uydurulmaz: 92 davranissal esdegerlik 0/92, 26 runtime guvenlik 0/26; K1-K5 bitmedi. Onceden gercekten calisan SHA-dogrulanmis K3-K4 9/9 offline test var; tam main 81 test dosyali regresyon CALISTIRILMADI. Son K2/K3/K5 orphan evidence ve metadata injection degisikliklerinin testleri HENUZ CALISTIRILMADI.
Yeni sohbette ilk is kurallari ve bu devir notunu oku, Madsc55/Madsc55-Tv main hedefini teyit et, eksiksiz offline toplu regresyon engelini kaldir. Kullaniciya ayni sozleri yeniden verdirtme.
