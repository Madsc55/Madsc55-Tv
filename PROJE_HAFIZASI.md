Warning: truncated output (original token count: 50357)
Total output lines: 1176

Warning: truncated output (original token count: 50279)
Total output lines: 1170

Warning: truncated output (original token count: 50803)
Total output lines: 1172

Warning: truncated output (original token count: 124047)
Total output lines: 2706

## K3 EPG/XMLTV güncellemesi — 2026-10-23
- `madsc/epg.py`: XMLTV programme öğesinde eksik/boş `channel` artık fail-closed; XMLTV'de tanımsız programme channel eşleşmeyi geçersiz kılar. M3U `tvg-id` değerleri kenar boşluklarından arındırılır.
- Regresyon testleri `tests/test_epg.py` içine eklendi. Kod `62211f43813ef87ec8a75329cf89506dcebac261`, test `4a3eee527902eea22a99afc9f82901ae3e837ed4`.
- Devir raporu: `docs/K3_EPG_FAIL_CLOSED_PROGRESS_2026-10-23.md`; görev defteri ve DEVAM_NOTU güncellendi.
- `[skip ci]` nedeniyle bu commit'ler için CI koşusu yok; test sonucu iddia edilmez. Canlı probe / Actions dispatch yapılmadı.
- Gerçek ffprobe/ffmpeg, bağımsız 6+ saat süreklilik, IBO Player Pro cihaz kabulü, Pages/EPG zinciri ve logo eşlemesi açık. K3 tamamlandı sayılmadı; 0/92, 0/26, 0/22 korunur.
- Üretim playlist/EPG/favoriler/cihaz/yedek/arşiv verileri değiştirilmedi; PR #71 birleştirilmedi.

---

# MADSC55 TV - Merkezi Proje Hafizasi

## Kalici calisma kurali (19 Ekim 2026)
Her islemden once eski depodaki DEVAM_NOTU.md, 810 dosya notu.md, AGENTS.md ve yapilacak isle ilgili diger butun kaynak notlar, kararlar ve kanitlar incelenir. Yalniz uc dosyayla sinirli kalinmaz. Okunmayan belge okunmus gibi gosterilmez. Yeni fikirler degerlendirilir.

## Tek not kayit noktasi
Kullanici 'notlara kaydet' dediginde yalnizca bu dosyaya tarihli kayit eklenir. Once mevcut kayitlar okunur ve korunur. Kayitlar karar, kaynaklar, yapilanlar, commit/test kaniti, eksikler ve siradaki isi kapsar. Eski kaynak notlar degistirilmez. Bu dosya kaynak notlarin tam kopyasi degil, merkezi karar ve ilerleme defteridir.

## Ilk durum
K1 guvenlik, K2 kesif, K3 kanal testi, K4 yedek, K5 bakim sifirdan kuruluyor. Eski 92 workflow tasinmayacak. IBO Player'da calistigi kullanici tarafindan dogrulanan kanal teknik testten kaldi diye silinmeyecek. Ana liste playlist.m3u8, EPG xmltv.xml. GitHub Actions calisma kaniti, 26 kuralin ve 92 islevin kabul kaniti, canli test ve bagimsiz yedek kaniti henuz tamamlanmadi. Uretime gecis kapali.

## 19 Ekim 2026 - K2/K3 IBO koruma entegrasyonu
Kaynaklar: DEVAM_NOTU.md, 810 dosya notu.md, AGENTS.md, GUVENLIK_KURALLARI.md, BES_SISTEM_TOPLU_IS_DEFTERI.md, IPTV_PROJE_HAFIZASI.md, yeni proje modulleri.
Yapilan: madsc/handoff.py, IBO kararlarini madsc/ibo_policy.py uzerinden aday degerlendirmesine bagliyor. Teknik test basarisiz + kullanici IBO WORKING sonucunda protected_working true, delete_allowed false kalir. tests/test_handoff.py icin regresyon senaryolari eklendi.
Commitler: 67db651e97cbf61fb1f2534a26a14a8d2d0aefea, 3e466bd80c299ccbd1337b25463595438c36f1df.
Kaniti bekleyen: GitHub Actions gercek run sonucu, gercek yayin/IBO cihaz testi, 26/26 kural ve 92/92 davranissal esdegerlik. Uretim yazma izni kapali.
Siradaki: guvenli K3 kanit modeli, uc asama ve sureklilik, K1 karar kapilari, K4 yedek/restore, K5 toplu kabul.

## 19 Ekim 2026 - BES SISTEM ARASI BAGIMLILIK VE TEK OTOMASYON KURALI
Kullanici karari: K1-K5'ten herhangi bir is yapilirken yalniz kendi notlari degil, etkiledigi diger kategorilerin DEVAM_NOTU.md, 810 dosya notu.md, AGENTS.md ve tum ilgili ek kaynak notlari incelenecek. K2'nin K3/K4/K5 baglantilari, K3'un IBO kararlari ve K4 yedekleri, K5 koordinasyonu bir arada degerlendirilecek. Eski otomasyonlarin gerekli islevleri bes yeni sisteme dagitilacak; 20-30 yeni bagimsiz gunluk tetikleyici olusturulmayacak. Bir gorevin tek sahibi, bagli gorevleri ve toplu kabul kaniti olacak. Yeni fikirler mevcut guvenlik ve kullanici onayi kapilarina uygun bicimde eklenebilir.
Kaynaklar: BES_SISTEM_GECIS_KONTROL.md, BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md, BES_SISTEM_TOPLU_IS_DEFTERI.md, docs/MADSC-IKI-TOPLU-KABUL-PLANI.md ve ana notlar.
Uygulama: madsc/dependencies.py gorev-kategori bagimlilik sozlesmesi ve tests/test_dependencies.py negatif/regresyon testleri. Commitler 62fc849d1874b3ef9d758617d90f0fb1696f7929, f7fbd5ba697651a466d60511be093727febe8254.
Sinir: Bu moduller henuz GitHub Actions gercek orkestrasyonu veya 92/92 esdegerlik degildir; cronlar acilmadi, eski workflowlar kapatilmadi, CI sonucu dogrulanmadi. Sonraki is: kategori raporlarina bagimlilik kanitini baglamak, besli tek toplu kabul ve 92 davranis matrisini gelistirmek.

## 19 Ekim 2026 - K5 bagimlilik denetimi
Kaynaklar: DEVAM_NOTU.md, 810 dosya notu.md, AGENTS.md, BES_SISTEM_TOPLU_IS_DEFTERI.md, BES_SISTEM_GECIS_KONTROL.md, BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md, docs/MADSC-IKI-TOPLU-KABUL-PLANI.md ve yeni sistem dosyalari.
Yapilan: madsc/core.py K5 izole raporuna K2-K3-K4-K5 baglanti kaniti, tek toplu plan, sifir ek bagimsiz tetik, zamanlayici ve eski workflow kapatma yasaklari eklendi. tests/test_core.py regresyon kontrolu eklendi. Commitler 1b8ecb13dcd730edeb4178f66fb42ff5d0bf8334 ve 7de9537a8687b3686fb536aeb09f03fab19a1e41.
Bekleyen: gercek Actions run kaniti, canli orkestrasyon, 92 islevin davranissal esdegerligi, 26 kural, K3 canli kanit ve K4 bagimsiz restore. Uretim degisikligi yok.

## 19 Ekim 2026 - Besli gercek Actions toplu zincir taslagi
Kaynaklar: DEVAM_NOTU.md, 810 dosya notu.md, AGENTS.md, BES_SISTEM_TOPLU_IS_DEFTERI.md, BES_SISTEM_GECIS_KONTROL.md, docs/MADSC-IKI-TOPLU-KABUL-PLANI.md ve yeni workflow dosyalari.
Yapilan: Var olan .github/workflows/madsc-05-bakim.yml manuel tetik ile K1>K2>K3>K4>K5 sirali needs baglantili islere ve son toplu-kabul isine donusturuldu. Her kategori salt-okunur fixture raporu artifact olarak saklanir. madsc/batch_acceptance.py bes kaniti eksik/tekrar/yanlis veya yazma iddiasi varsa reddeder. tests/test_batch_acceptance.py negatif testleri eklendi.
Commitler: 0acb780eec9e7441a7fbab91d969869dc6141bb3, 7b328951ca5dbebb1161467f538c5428347b5354, 4c3982c69e1733515ce6082277abe97ef381479e.
Sinir: Henuz gercek Actions run/job/artifact sonucu dogrulanmadi. Besli fixture basarisi 92/92 esdegerlik, 26/26 runtime kural, gercek yayin, IBO cihazi veya harici restore kaniti degildir. Cron acilmadi, eski 92 workflow kapatilmadi, uretim listeleri degismedi. Siradaki: gercek manuel toplu run kaniti ve eksik davranislarin kaynak notlara gore uygulanmasi.

## 19 Ekim 2026 - K3 toplu kabul IBO negatif testi
Kaynaklar: DEVAM_NOTU.md, 810 dosya notu.md, AGENTS.md, GUVENLIK_KURALLARI.md, BES_SISTEM_TOPLU_IS_DEFTERI.md ve K2/K3/K5 mevcut modulleri.
Yapilan: madsc/core.py K3 izole raporuna teknik test 503/0 saniye ve kullanici tarafindan acik WORKING olarak saglanan IBO karari senaryosu eklendi. protected_working korunur, delete_allowed ve production_change_allowed false. tests/test_core.py bu alanlari denetler. Commitler 57aea6605e377149d93a39eb8251f67cb8fd0b76, 8f7f88042d322d682ddf2032dfeb0ab86f5e26b5.
Bekleyen: Kod ve testler GitHub'a yazildi ancak Actions run tetikleme yetkisi mevcut araclarda bulunmuyor; bu nedenle calistirildi veya basarili denemez. Kullanici IBO cihazi gercekten test edilmedi; sentetik fixture. Eski repo ve korunan playlistler degismedi. Siradaki: toplu Actions run kanitini edinmek, 92 gorevin davranissal haritasini ilerletmek.

## 19 Ekim 2026 - Tek toplu kosuda tekrar testlerin giderilmesi
On kontrol: eski DEVAM_NOTU.md (18 Ekim son devir ve ilgili kayitlar), 810 dosya notu.md (son D2 konsolidasyon), AGENTS.md, OZELLIK_ENVANTERI.md, BES_SISTEM_TOPLU_IS_DEFTERI.md, BES_SISTEM_GECIS_KONTROL.md, BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md ve yeni K5 YAML incelendi. Iki dev not dosyasinin tum satirlari okunmus sayilmiyor.
Bulgu: K5'in K1-K5 sirali toplu YAML dosyasi ayni python unittest discover komutunu bes kategoride tekrar ediyordu. Degisiklik: .github/workflows/madsc-05-bakim.yml icinde tum regresyonlar yalniz K1'de calisiyor; K2-K5 yalniz kendi izole kategori kanitini uretiyor. needs sirasi K1>K2>K3>K4>K5 ve toplu-kabul korunuyor. Commit 748e86784bf1882b58030f6f0807f99f010a280d.
Kaniti bekleyen: GitHub Actions gercek run/job/artifact sonucu; 26/26 runtime kural, 92/92 davranissal esdegerlik, canli yayin, IBO cihaz ve harici restore. Cron ve uretim yazma acilmadi; eski 92 workflow degistirilmedi. Sonraki: yeni SHA'nin gercek Actions sonucunu dogrula, gorev bagimliliklarini ve davranis kanitlarini gelistir.

## 19 Ekim 2026 - Madsc55-Tv adlandirma ve gorev test kaydi
Yeni ozel deponun resmi adi Madsc55-Tv; eski madsc-tv yalniz salt okunur referanstir. Kullanici gorunen yeni sistem adlari Madsc55-Tv olacak, mevcut teknik dosya yollarina salt ad icin dokunulmayacak. Kod commit ed75d86847dbc3e510f87057b1ee14ee22504ba6 bos ve gecersiz toplu gorevleri reddeder; regresyon test commit 3398e089463b76dbd7364dff0f14db320692ba4a. Eski DEVAM_NOTU.md, 810 dosya notu.md, AGENTS.md, BES_SISTEM_TOPLU_IS_DEFTERI.md, BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md ve OZELLIK_ENVANTERI.md ilgili bolumleri kontrol edildi. Gercek yeni Actions run henuz dogrulanmadi; 26 kural ve 92 davranis kabul edilmis sayilmaz. Eski repo ve korunan listeler degismedi.

## 19 Ekim 2026 - Madsc55-Tv GitHub Actions gorunen adi
Yeni ozel repo .github/workflows/madsc-05-bakim.yml dosyasinin yalniz name basligi Madsc55-Tv - Besli Toplu Guvenlik ve Kabul olarak degistirildi. Commit efbca192608746f2524da8591740dc9956414579. Manuel workflow_dispatch, salt-okunur izinler, K1-K5 sirasi ve artifactler degismedi. Gercek Actions run sonucu henuz dogrulanmadi. Eski repo ve korunan listeler degismedi.

## 19 Ekim 2026 - K5 kabul izolasyon kaniti
madsc/batch_acceptance.py her K1-K5 raporunda checks.isolation=true ariyor ve checks tipini denetliyor. Kod commit: 8374f137aaddf18970c3fe644dd0aaaac2545d1e. Gercek GitHub Actions calistirma kaniti bekleniyor. Eski depo degismedi; cron ve otomatik uretim islemleri acilmadi.

## 19 Ekim 2026 - Kullanici onayli otomatik salt okunur test tetigi
Kullanici onayiyla yalniz yeni Madsc55-Tv deposunun .github/workflows/madsc-05-bakim.yml dosyasina push (main; madsc/**, tests/**, ilgili YAML) eklendi. workflow_dispatch korunuyor. K1-K5 needs zinciri, contents: read, persist-credentials: false, tek regresyon gecisi ve salt okunur raporlar aynen korundu. Kod commit d59286332a9f90d71e4e141424656a7d3c131c6e. Hafiza dosyasi degisimi tetik kapsaminda degil, gereksiz run olusturmaz. Cron/uretim yazma/eski 92 workflow degisimi yok. Gercek Actions run/job/artifact sonucunu ayrica dogrulamak gerekiyor; 26/26 ve 92/92 kanitlanmis sayilmaz.

## 19 Ekim 2026 - K1-K5 toplu hata teshisi, fail-closed kabul
Kullanici onayiyla .github/workflows/madsc-05-bakim.yml degistirildi. K1 regresyon hatasinda K1 kanit raporu yine uretilmeye calisilir; K2-K5 salt okunur kategori kontrolleri onceki kategorinin basarisizliginda da calisir (always ve not cancelled). Toplu kabul tum kategori sonuclarini degerlendirir; herhangi bir kategori veya kabul adimi basarisizsa genel job exit 1 ile basarisizdir. Kategori raporlari tek tek saklanir; uretim izni verilmez. Commit 5ae5d0dd044dfd9fc6392784cbec02e266da9dca. Otomatik push tetigi mevcut; gercek yeni Actions run/job/artifact sonucu henuz incelenmedi. Eski repo ve korunan veriler degismedi.

## 19 Ekim 2026 - GitHub Actions toplu sonuc gorunurlugu
Kullanici istegiyle .github/workflows/madsc-05-bakim.yml icinde toplu-kabul isine GITHUB_STEP_SUMMARY tablosu eklendi: K1-K5 ve kabul icin sonuc, genel basari/basarisizlik. reports/test-sonuclari.txt ayrica madsc-test-sonuclari artifact olarak saklanir. Herhangi bir kategori veya kabul basarisizsa genel is exit 1 olur, uretim onayi verilmez. Commit 65a3309e959674ce713b6267a00227c7d75d4281. Bu raporlama GitHub uzerinde otomatik, ancak baglanti ozel depodaki push run listesini dogrudan getiremediginden ChatGPT'nin sohbet disinda sonucu otomatik gordugu iddia edilemez. Yeni Actions kosusu dogrulanmayi bekliyor. Eski repo ve canli listeler degismedi.

## 19 Ekim 2026 - GitHub Actions gercek run sonucuna erisim cozuldu
GitHub baglantisinin mcp GitHub fetch GET yolu ile https://api.github.com/repos/Madsc55/Madsc55-Tv/actions/runs?per_page=10 adresi ozel depo izinleriyle basariyla okundu. Gercek kosular: #1 39180821171 failure (d592863), #2 39180936538 success (7814d23), #3 39181202379 success (5ae5d0d), #4 39181460550 success (65a3309). #4 jobs API sonucunda Guvenlik, Kesif, Kanal Testleri, Arsiv ve Yedek, Genel Bakim, Besli toplu kanit dogrulama hepsi success. Bu yalniz izole fixture ve workflow sonucudur; 26/26 gercek runtime kurali, 92/92 esdegerlik, IBO cihaz, harici restore ve uretim hazirligi iddiasi degildir. Kullanici yeni sohbetlerde dogrudan run listesini kontrol ettirebilir. Surekli arka plan izleme veya otonom duzeltme kendiliginden acilmis degildir. Eski depo degismedi.

## 19 Ekim 2026 - K4 manifest regresyonu
Yeni tests/test_backup.py icinde bos manifestin external_backup_verified ve restore_verified alanlarini false tutmasini denetleyen regresyon testi eklendi. Commit 29fa2225e08bb35d7904d0f7f46d320bb0d19b25. K4 canli yedek veya gercek restore olarak iddia edilmiyor. madsc/backup.py icin daha kati yol/symlink dogrulama degisikligi denendi fakat GitHub yazma araci guvenlik denetimi tarafindan engellendi; bu degisiklik UYGULANMADI. Yeni Actions kosusu sonucu henuz dogrulanmadi. Eski repo degismedi.

## 19 Ekim 2026 - K4 yol denetimi ve gercek Actions kontrolu
Gercek GitHub Actions #5 run 39181924806, commit 29fa222, completed/success olarak API uzerinden dogrulandi. K4 manifest kaynak dogrulamasina mutlak yol ve dogrudan sembolik baglanti reddi eklendi: aaf213b1c99dab2960617781899cd39a854d7ce8. tests/test_backup.py icine bunlarin regresyon testleri eklendi: 52ae1ddb1630dd2ea2b7f2a8b779eb6f415af875. Bu denetim ara dizin sembolik baglantilarini ayrica reddettigini iddia etmez; ek sertlestirme gerekir. GitHub Actions #6 39182087053 queued ve #7 39182095159 pending olarak goruldu; tamamlanmis basari kaniti yok. Eski depo ve canli veriler degismedi; gercek harici backup/restore kanitlanmadi.

## 19 Ekim 2026 - K4 ara dizin sembolik baglanti korumasi
Gercek Actions #6 39182087053 ve #7 39182095159 completed/success dogrulandi. K4 snapshot_manifest kaynak yolunun ara dizinlerindeki sembolik baglantilar da reddedilecek sekilde guclendirildi: ffc17d45caa593afa6992d8352480fc90211e5bb. tests/test_backup.py ara dizin symlink regresyonu eklendi: d8194e3021e2eaf9c98054e6938001e21520823b. Actions #8 39182332177 in_progress, #9 39182338181 queued; basari henuz dogrulanmadi. K4 halen izole manifest denetimi, harici yedek/restore degil. Eski repo ve canli veriler degismedi. Sonraki is #8/#9 testlerini kontrol etmek ve K1-K5 gercek kanit kapsamini gelistirmek.

## 19 Ekim 2026 - K2 kaynak testi ve Actions #10
GitHub Actions #8, #9 ve #10 basarili olarak dogrulandi. K2 UTF-8 BOM iceren M3U okuma regresyon testi d6f90cb1 commitinde eklendi. Onceki hafiza kaydi denemeleri engellenmisti; bu kayitla devir tamamlandi. Eski depo ve canli dosyalar degismedi. Sonraki adim K1-K5 gercek islev ve kanit kapsamini artirmak.

## 19 Ekim 2026 - K1 BOM butunluk regresyonu
K1 salt-okunur playlist butunluk denetimine UTF-8 BOM iceren M3U regresyon testi eklendi: 10151c3632fa3f3d0dff0a3d31786ce69bda1c9f. Dosyanin degismedigi ve kanal sayisinin dogru oldugu test ediliyor. Yeni Actions sonucu bekleniyor. Gercek 26 kural runtime onayi yok; eski depo degismedi.

## 19 Ekim 2026 - K3 devir
K3 sure olcum kontrolu commit 91d4236. Actions #12 son kontrolde devam ediyordu. K3 regresyon testi yazma denemesi engellendi; uygulanmadi. Sonraki is Actions #12 sonucunu kontrol etmek, testi eklemek ve besli sistem kurulumuna devam etmek. Eski depo degismedi.

## K3 regresyon devri - 19 Ekim 2026
Actions 12 basarili. K3 regresyon testi d4c8f8d commitinde eklendi. Actions 13 beklemede. Eski depo degismedi.

## 19 Ekim 2026 - K5 sinir testi
K5 tekrar deneme siniri icin test eklendi: 490fad5. K3 Actions 13 son kontrolde devam ediyor. K5 limit tip kontrolu degisikligi engellendi, uygulanmadi. Sonraki is yeni Actions sonuclarini dogrulamak. Eski depo degismedi.

## 19 Ekim 2026 - K5 tip kontrolu tamamlandi
Actions #13 39183103253 ve #14 39183173461 success dogrulandi. K5 retry limit bool, ondalik ve metin degerlerini reddeden tip kontrolu e3ec1f347c9ba26386febb58f41724f6c3981e01 ile eklendi. K5 regresyon testi fdf1477cd0d7c201a4ed0860dcb3575125976d88 ile eklendi. Actions #15 39183349096 in_progress, #16 39183356794 pending; sonuc bekleniyor. Eski depo ve canli listeler degismedi. Sonraki is Actions 15/16 sonucunu kontrol edip besli sistem kanit kapsamini genisletmek.

## 19 Ekim 2026 - Toplu kurulum yaklasimi
K1-K5 tek Actions workflow ve toplu kabulde zaten birlesik; kullanici istegi uzerine tek tek mikrotest yerine toplu islev paketlerine odaklanilacak. Actions #15 ve #16 success dogrulandi. Toplu kabulde JSON raporunun nesne olmasi zorunlu hale getirildi: 04d5f96. Hatali rapor sekilleri icin regresyon eklendi: 269115a. Bu iki degisikligin Actions sonuclari ayrica kontrol edilecek. Izole test basarisi uretim onayi veya 92 islev esdegerligi degildir. Eski depo degismedi.

## 19 Ekim 2026 - K2 toplu paket ilerleme
Actions 17 ve 18 son kontrolde calisiyor veya bekliyor. K2 URL metin turu kontrolu de197ec ile eklendi; yerel file URL reddi regresyonu c7bbc46 ile eklendi. EXTINF bicim sertlestirmesi bu denemede baglanti guvenlik engeline takildi ve uygulanmadi. Sonraki turda Actions sonuclarini dogrula; tekil mikrotestler yerine K1-K5 buyuk islev paketleri ve gercek kanit odagi sursun. Eski depo degismedi.

## 19 Ekim 2026 - K2 toplu durum
Actions 17, 19 ve 20 success; 18 cancelled, basarili sayilmadi. K2 aday satirlari liste bicimi dogrulamasi a0bc9bd ile eklendi. EXTINF ad dogrulamasi yazma denemesi yine engellendi, uygulanmadi. Yeni Actions sonucu ayrica kontrol edilmeli. Eski depo degismedi; izole testler uretim onayi degildir.

## 19 Ekim 2026 - Actions 18 aciklama ve K2 duzeltmesi
Actions #18 (39183571815) completed/cancelled, hic job kaydi yok; kesin iptal nedeni gorunmedi. Tekrar kuyrukta degil. Daha yeni #21 (39216738946) success. K2 EXTINF ad ve ayirac dogrulamasi 5aab945 ile, regresyon testi 4beb2c9 ile eklendi. Bu iki commitin Actions sonucu ayrica dogrulanmali. Eski depo degismedi; canli yayinlar etkilenmedi.

## 19 Ekim 2026 - K2 devir
Actions 22, 23 ve 24 basarili. K2 kanal adi tur kontrolu 11905cd ile eklendi. Eski depo degismedi. Sonraki is besli sistem toplu islev paketleri.

## 19 Ekim 2026 - K2 K3 toplu devir
Actions 22-24 basarili. K2-K3 handoff girdi bicimi kontrolu degisikligi guvenlik engeline takildi, uygulanmadi. Sonraki is handoff dogrulamasini tamamlamak ve toplu K1-K5 islevlerine devam etmek. Eski depo degismedi.

## 19 Ekim 2026 - K2 K3 veri devri
Probe kanit turu dogrulamasi 082a658 commitinde eklendi. Diger handoff dogrulama ve regresyon yazma denemeleri baglanti guvenlik engeline takildi. Yeni Actions sonucu dogrulanmali. Eski depo degismedi.

## 19 Ekim 2026 - K2 K3 engel giderildi
Actions 25 success. K2 K3 girdi bicimi dogrulamalari 83f0cf6, d2a7c48 ve 15b70ef ile eklendi. Toplu gecersiz veri regresyonu 7ed4c9a ile eklendi. Yeni Actions sonuclari kontrol edilmeli. Eski depo degismedi; uretim yetkisi verilmedi.

## 19 Ekim 2026 - K2 K3 Actions kontrolu
Actions 26 success; 27 ve 28 cancelled; 29 son kontrolde in_progress. K3 probe kaydi tur kontrolu yazma denemesi engellendi, uygulanmadi. Sonraki is 29 sonucunu kontrol edip K1-K5 gercek islev paketlerini topluca gelistirmek. Eski depo degismedi.

## 19 Ekim 2026 - K3 hata cozumu
Actions #29 failure: 53 testten 1'i, test_invalid_handoff_shapes_fail_closed (ibo=None) yanlis beklenti. None IBO verisi UNKNOWN olarak izinli; test df77ed4 ile duzeltildi. K3 probe kaydi bicim kontrolu a35793d ve regresyonu f03da40 eklendi. Yeni Actions sonucunu dogrula. Eski depo degismedi.

## 19 Ekim 2026 - K3 Actions kontrolu
Actions #30 success; #31 cancelled; #32 son kontrolde in_progress. K3 SHA256 kimlik bicimi kontrolu yazma denemesi guvenlik engeline takildi, uygulanmadi. Sonraki is #32 sonucunu dogrulamak ve buyuk islev paketlerine odaklanmak. Eski depo degismedi.

## 19 Ekim 2026 - K3 SHA256 tamamlama
Actions #33 success; #34 son kontrolde queued. K3 64 karakter kucuk harf hex dogrulamasi d2a41b8 commitinde tamamlandi. Gecersiz hex regresyonu ec329a3 eklendi. Yeni Actions sonucunu dogrula. Eski depo degismedi, uretim yazimi yok.

## 19 Ekim 2026 - K2 kaynak envanteri
Actions #34 success; #35 cancelled; #36 son kontrolde in_progress. K2 M3U kaynak kanal sayisi, kabul, tekrar ve ret sayimlari 382b036 ile eklendi; K2 toplu mutabakat kaniti 49cb5c0 ile eklendi. #36 ve yeni Actions kontrol edilmeli. Eski depo degismedi, uretim yazimi yok.

## 19 Ekim 2026 - K4 manifest regresyonu
Actions #39 success. K4 manifest yapisi ba05849, kayit bicimi d9d46a1 ve gecersiz manifest regresyonu df42919 eklendi. Yalnizca izole dosya dogrulamasi; harici yedek ve geri yukleme onayi yok. Yeni Actions sonucunu dogrula. Eski depo degismedi.

## 19 Ekim 2026 - K4 sandbox kopya kontrolu
Actions #42 success. K4 iki bagimsiz gecici dizindeki dosya kopyalarini SHA256 manifesti ile karsilastiriyor: 89bcd71. Bozulma testi 0addf94; besli toplu fixture kontrolune baglanti 6c1418a. Gercek dis yedek veya uretim geri yukleme yapilmadi. Son Actions kontrol edilmeli.

## 19 Ekim 2026 - K4 sandbox restore audit
Actions #45 success. K4 salt-okunur sandbox restore audit 60d3128, bozulma regresyonu 1f7b287, besli toplu kontrolde audit 9e99b98. Uretim geri yukleme ve dis yedek dogrulanmadi. Yeni Actions sonucunu bekle. Eski depo degismedi.

## 19 Ekim 2026 - GitHub Actions kesin kontrol
Actions #48 completed/success (9e99b98): Guvenlik, Kesif, Kanal Testleri, Arsiv ve Yedek, Genel Bakim ve Besli toplu kanit dogrulama 6/6 success. #46 success, #47 cancelled. URL: https://github.com/Madsc55/Madsc55-Tv/actions/runs/39221975909 . Izole fixture testleri; canli uretim dogrulamasi degil. Eski depo degismedi.

## 19 Ekim 2026 - K5 toplu hata raporu
Actions #48 6/6 success. K5 besli kategori hata ozeti b493951, regresyon f9f80aa, toplu fixture baglantisi 201c1cf. Sonraki is yeni Actions run bitince alt isleri kontrol etmek. Uretim yazimi ve eski depoda degisiklik yok.

## 19 Ekim 2026 - K3 XMLTV islev paketi
Actions #51 completed/success; 6/6 job success. Eski AGENTS, BES_SISTEM_TOPLU_IS_DEFTERI ve BES_SISTEM_GECIS_KONTROL tekrar incelendi. Yeni XMLTV salt okunur kanal/program envanteri ve tvg-id eslestirme 6e802eb; regresyon 3df6cff; K3 fixture entegrasyonu 5190659. IBO cihaz EPG kabul edilmis sayilmaz. Yeni Actions tamamlaninca alt isler kontrol edilmeli. Eski depo degismedi.

## 19 Ekim 2026 - Besli durum ve EPG zaman alanlari
Actions #54 completed/success ve 6/6 job success. K1-K5 izole testleri gecti; 92 legacy davranis esdegerligi, 26 kural runtime, 18 gorev, gercek kanal testleri, EPG Pages ve IBO cihaz onayi, harici restore halen acik. K3 XMLTV baslangic/bitis alani eksikligi sayimi 8310afa; regresyon 133b106. Yeni Actions tamamlaninca dogrula. Eski depo degismedi.

## 19 Ekim 2026 - Eski workflow gercek envanter baslangici
Actions #55 ve #56 completed/success. Eski dal `.github/workflows` GitHub API sayimi 99 YAML; eski belgede 92 yaziyor, fark arastirilacak. Bes eski besli hedef YAML haric 94 dosya. Tam 99 dosya adina gore GECICI kategori matrisi: 999ac62; dort kritik YAML tetik/izin/komut/bagimlilik incelemesi c63a73d. EPG gunluk uretimi, Pages workflow_run, VOD metadata cron ve eski bakim cron yeni fixture sistemiyle esdeger degil. Gercek esdegerlik tamamlanmadan cron acilmayacak, eski workflow kapatilmayacak. Eski depo salt okunur.

## 19 Ekim 2026 - Workflow envanteri ikinci dalga
GitHub Actions #57 success, #58 son kontrolde in_progress. Eski dalin 6 ek YAML dosyasinin gercek tetik/komut/artifact incelemesi 728aa4b. Toplam 10/99 ayrintili incelendi; 89 bekliyor. K2 gercek tarama ve K3 ffmpeg/IBO ile K4 restore dry-run esdegerlik acik. Eski repo salt okunur, yeni cron etkinlestirilmedi.

## 19 Ekim 2026 - Workflow envanteri ucuncu dalga
Actions #59 completed/success (728aa4b). 12 ek YAML dogrudan tetik/komut/artefakt icin incelendi, matris 68fc4a9. Toplam 22/99 ayrintili incelendi, 77 kaldi. Aday bekletme ve birlesik aday raporu K2-K3-K5 ortak bagimlilikli; yalniz dosya adina gore tek kategori yetersiz. Eski repo salt okunur; cron acilmadi, eski is kapatilmadi. Yeni Actions sonucu kontrol edilecek.

## 19 Ekim 2026 - Workflow envanteri dorduncu dalga
Actions #60 completed/success. 16 ek eski YAML dogrudan tetik, izin, komut ve rapor adimlari icin incelendi; matris 619d7a3. Toplam 38/99, 61 ayrintili inceleme kaldi. `madsc-birlesik-kesif.yml` contents:write ve kesif arsivi adimlari risk incelemesi gerektiriyor; izinsiz korunan dosya yazimi yapilmadi. Eski repo salt okunur; cron acilmadi, workflow kapatilmadi.

## 19 Ekim 2026 - Workflow envanteri besinci dalga
Actions #61 completed/success. 20 ek YAML tetik, izin ve temel komut icin incelendi: 88f5106. Toplam 58/99 ayrintili incelendi, 41 kaldi. IBO karar workflow'lari ve son-kontrol workflow'u contents:write tasiyor; gercek yazma yolu ve onay denetimi acik. Eski depo salt okunur; cron acilmadi, workflow kapatilmadi.

## 19 Ekim 2026 - Workflow envanteri altinci dalga
Actions #62 completed/success. 20 ek eski YAML tetik/izin/temel adimlari incelendi; matris 19a0163. Toplam 78/99 ayrintili incelendi, 21 kaldi. Uc asama, yedek, logo yayin workflow'larinda write izinleri goruldu; gercek yazma guvenligi acik. Yeni depoda cron ve uretim yazimi etkinlestirilmedi.

## 19 Ekim 2026 - Yazma yollari somut denetimi
Actions #63 completed/success. 6 kritik eski YAML'nin tam run/staging/push yolu okundu, rapor f7f04c3. Birlesik kesif sadece `madsc_kesif/` stage ediyor; EPG/logo join `if: false` ile kapali. Genis kaynak kontrolu sadece `madsc_genis_tarama/` stage edip basarida `madsc-uc-asama.yml` tetikliyor. Buna karsin 4 IBO karari workflow'u `CALISANLAR.m3u` dosyasini acikca git add edip protected_write_gate sonrasi main'e push etmeye calisiyor. Gate/script kodu ve kullanici onayi henuz tam dogrulanmadi, korunan liste yazmasi YASAK/etkinlestirilmedi. K2-K3-K5 ortak isleyis ve K3 gercek ffmpeg/canli stream esdegerligi ACIK. 78/99 workflow tetik/komut incelemesi, 21 kaldi. Eski repo salt okunur.

## 19 Ekim 2026 - YENI SOHBETE DEVIR / TEK KAYNAK

KULLANICI ISTEGI: Bu sohbet doldu; yeni sohbette kaldigimiz yerden hicbir is kaybolmadan DEVAM EDILECEK. Kullanici "Yap" dediginde sadece plan anlatmak degil, gercek GitHub inceleme/degisiklik, Actions sonucunu dogrulama ve not yazma isteniyor. Kisa ve somut Turkce cevap ver.

DEPOLAR: Yeni/yazilabilir PRIVATE `Madsc55/Madsc55-Tv` (main), Actions: https://github.com/Madsc55/Madsc55-Tv/actions . Eski `Madsc55/madsc-tv`, branch `madsc/bes-sistem-toplu-birlestirme`, KESINLIKLE SALT OKUNUR. Eski workflow kapatma, cron acma, korunan playlist degistirme, production commit/push YOK. Ilerleme kaydi SADECE yeni deponun `PROJE_HAFIZASI.md` dosyasina.

BELGELER: Eski depoda `DEVAM_NOTU.md`, `810 dosya notu.md`, `AGENTS.md`, `BES_SISTEM_TOPLU_IS_DEFTERI.md`, `BES_SISTEM_GECIS_KONTROL.md`; yeni depoda `PROJE_HAFIZASI.md` ve `madsc/LEGACY_WORKFLOW_ON_ENVANTER.md`. Ilk iki eski not cok buyuk; ilgili son kisimlari oku. Envanter dosyasi 99 eski YAML adini, gecici K1-K5 eslemelerini, ayrintili denetlenen dosyalari ve son yazma-yolu bulgularini icerir.

DOGRULANMIS DURUM: Eski .github/workflows dalinda 99 YAML sayildi, eski belgelerdeki 92 sayisiyla fark henuz aciklanmadi. 78/99 YAML dosyasinin tetik/izin/temel komutlari dogrudan okundu; **21 DOSYA KALDI**. Bu sadece envanter ilerlemesi, 78/99 davranissal esdegerlik DEGIL. Envanter commitleri: 999ac62, c63a73d, 728aa4b, 68fc4a9, 619d7a3, 88f5106, 19a0163, f7f04c3. Son f7f04c3 altinda 6 kritik workflow'un somut staging/push yollari incelendi. GitHub Actions #64 (SHA f7f04c3) completed/success; #63, #62, #61 de completed/success. Bunlar sadece yeni deponun izole fixture testleri; production kaniti degil. Sonraki degisiklikten sonra yeni Actions run ve tum K1-K5 + kabul job sonuclarini kontrol et.

ACIK GUVENLIK BULGULARI: `madsc-birlesik-kesif.yml` contents:write ama gorunen git stage sadece `madsc_kesif/`; EPG/logo join if:false. `madsc-genis-kaynak-kontrol.yml` contents:write ama gorunen stage `madsc_genis_tarama/`; basarida `madsc-uc-asama.yml` tetikliyor. DORT eski IBO karar workflow'u `CALISANLAR.m3u` icin git add ve `tools/protected_write_gate.py --base origin/main` ardindan main push deniyor; `YABANCI_KANALLAR.m3u` degisiklik diff engeli goruldu. **Gate scriptinin gercek mantigi, onay kosullari ve cagirdigi yazma scriptleri HENUZ dogrulanmadi**. contents:write tek basina ihlal kaniti degil; korunan liste yazma YASAK. IBO Player Pro WORKING kanali otomatik silinmeyecek; cihaz testi olmadan IBO dogrulamasi iddia edilmez.

ACIK ISLER: (1) Kalan 21 eski YAML dosyasinin gercek tetik/izin/komut/artefakt incelemesini tamamla ve 92/99 farkini acikla. (2) Eski `tools/protected_write_gate.py` ile IBO apply scriptlerinin gercek koruma/onay/yazma akisini **salt okunur** denetle; K1 26 kuralinin runtime kaniti henuz yok. (3) K2 kaynak tarama, K3 ffmpeg/canli stream, EPG XMLTV tvg-id eslestirme ve IBO cihazi, K4 gercek izole restore, K5 birlesik rapor ve K2-K3-K5 ortak bagimlilik zincirinin **davranissal** esdegerligini uygulama/test et. (4) Eski EPG gunluk uretim + Pages deploy + VOD metadata cron yeni fixture sistemine tasinmis DEGIL. (5) 18 ek gorev ve 26/26 gercek guvenlik kural kaniti kapatilmadi. (6) Tek .github/workflows/madsc-05-bakim.yml, sadece manual dispatch + filtreli push, cron YOK; K1-K5 + kabul testleri var, production_ready=false. Gereksiz minik test donguleri yerine anlamli toplu is yap.

MEVCUT YENI KOD: `madsc/core.py`, `madsc/dependencies.py`, `madsc/ibo_policy.py`, `madsc/backup.py`, `madsc/source_import.py`, `madsc/discovery.py`, `madsc/handoff.py`, `madsc/channel_test.py`, `madsc/maintenance.py`, `madsc/playlist.py`, `madsc/epg_inventory.py`, `madsc/batch_acceptance.py`, `tests/`. K2-K5 fixturelari K1 engelinden bagimsiz salt okunur calisabilir; production K1 fail-closed. Test raporlari gercek production/IBO cihaz/92 davranissal esdegerlik olarak sunulamaz.

SON KULLANICI SORUSU: "Aday bekletme, tekrar testleri, akilli puanlama, logo/EPG kontrolleri, birlesik raporlarin K2-K3-K5 entegrasyonu; birlesik kesif ve IBO write guvenligi; K3 canli yayin testleri de yapildi mi? Yap devam." DOGRU CEVAP: Envanter ve bazi somut yazma yollari incelendi; gercek entegrasyon, IBO gate dogrulamasi ve canli stream esdegerligi HENUZ YAPILMADI. Bunu yeni sohbette unutma. Ilk adim Actions son durumunu kontrol et, sonra 21 dosyayi ve gate kaynak kodunu topluca denetle, envanter + bu hafizayi guncelle, Actions'i dogrula.

## 19 Ekim 2026 - Yeni sohbet: Actions ve IBO yazma kodu salt-okunur denetimi
Actions #64 (39225970625, f7f04c3) completed/success; K1, K2, K3, K4, K5 ve toplu kabul 6/6 job success API ile dogrulandi. Bu fixture kanitidir, canli kabul degildir.
Eski dal tools/protected_write_gate.py dogrudan okundu: CALISANLAR.m3u ve diger korunan yollar, tum M3U/M3U8 degisiklikleri reddedilir; HEAD farki, staged, unstaged, untracked ve ignored kontrol edilir; hata fail-closed. Bu gate kullanici onayi dogrulamiyor, branch ruleset yerine gecmiyor.
Eski dalda scripts/apply_ibo_6115_second.py, apply_ibo_first_239_decisions.py, apply_ibo_decisions_group1.py, apply_ibo_second_voice.py okundu. Dordunun hepsi CALISANLAR.m3u dosyasina yazma kodu iceriyor; eski workflow'lardaki gate bu degisikligi reddetmelidir. Scriptler dosyaya yazmadan once cihazdan canli IBO WORKING dogrulamasi yapmiyor; sabit pozisyon/karar kullaniyor. Onay ve canli koruma esdegerligi saglanmadan etkinlestirilemez.
Kalan 21 YAML bu turda okunmadi: 78/99 inceleme durumu DEGİSMEDİ. 92/99 farki, K2-K3-K5 gercek entegrasyonu, canli K3 ve K4 harici restore acik. Eski depoya ve uretim listelerine yazilmadi. Sonraki is: 21 YAML'i topluca incele, sonra izole uygulama ve Actions kaniti.


## 19 Ekim 2026 – Yedinci dalga: 99/99 eski workflow YAML incelemesi tamamlandi

Eski `Madsc55/madsc-tv` deposunun `madsc/bes-sistem-toplu-birlestirme` dali salt okunur kullanilarak kalan 21 workflow YAML'i dogrudan okundu: `test-24`–`test-39` (16 adet), `test-kanal-adaylari.yml`, `toplu-sistem-kontrol.yml`, `yedekler-yeniler-medya-kontrol.yml`, `yeni-aday-on-test.yml`, `yeniler-guvenli-arama.yml` (5 adet). Tetik, contents izni, temel komut, artifact/medya kontrolu yeni `madsc/LEGACY_WORKFLOW_ON_ENVANTER.md` dosyasina eklendi (commit dd74178f7931cfe1465d7c6d570c9a4ed07d7857). 21'inin tamaminda `contents: read`; `test-31` dispatch-only. Son besli arasinda ffmpeg medya kontrolu ve kesif->tarama artifact zinciri bulunuyor.

**YAML inceleme sayaci 99/99; 21 kalmadi.** Bu, tum workflow'larin davranissal olarak yeni sisteme tasindigi anlamina GELMEZ. Eski belgelerdeki 92 sayisi ile 99 kaynak sayisi farki henuz aciklanmadi. K2-K3-K5 gercek entegrasyon, K3 canli yayin/IBO cihaz testi, K1 26 kural runtime kabul, K4 harici geri yukleme, production EPG/Pages/VOD halen acik. Eski depo ve korunan listeler degistirilmedi. Sonraki somut adim: bu davranissal eksikleri yeni depoda salt-okunur moduller/testlerle gelistirip Actions sonucunu dogrulamak.


## 19 Ekim 2026 – K2/K3/K5 salt-okunur aday koordinasyonunun ilk kodu

Yeni `madsc/candidate_coordination.py` eklendi (c550aa7): `classify_candidates` ile URL SHA256 aday tekillestirme, `evaluate_probe` ile saglanan teknik kanit degerlendirmesi, `retry_decision` ile basarisizlik esigi, salt-okunur skor/sirada bekletme raporu. `tests/test_candidate_coordination.py` (6ed2ed9) 5 regresyon senaryosu iceriyor: kanitsiz aday bekletme, onaysiz teknik gecis, tekrar esigi, fingerprint mismatch fail-closed, duplicate. Modulu kullanarak gercek ag istegi, cihaz IBO dogrulamasi, EPG/logo metadata join veya production yazma YAPILMADI; bunlar halen acik.

Actions #67 SHA 6ed2ed9 sorgu aninda pending; #66 SHA c550aa7 queued; #65 dd74178 completed/success (dokuman degisikligi). Yeni kod/test Actions basarisi henuz teyit edilmedi. Eski repo salt okunur. K1 26 runtime kural, K3 canli ffprobe, K4 harici restore ve production kabul halen acik.


## 19 Ekim 2026 – Aday puanlama + EPG/logo + IBO kanit birlestirme

Actions #66 (c550aa7) ve #67 (6ed2ed9) completed/success. `madsc/candidate_coordination.py` (e4d893f) genisletildi: opsiyonel XMLTV `tvg_id`/logo ID setleri, eslesme puanlari (+20 EPG, +10 logo), metadata eksiginde aday bekletme, saglanan IBO WORKING bilgisini silme yasağıyla koruma, toplam held_count ve metadata eslesme sayaclari. Yalniz saglanan veriler degerlendirilir; gercek EPG indirme/IBO cihaz sorgusu yok. `tests/test_candidate_coordination.py` (6689b8c) uc yeni regresyon testi eklendi: metadata puani ve bekletme, IBO WORKING korunmasi, tam metadata halinde bile production onayi olmamasi. Yeni Actions #68 ve #69 sorgu aninda in_progress/pending, sonuc teyidi bekleniyor. K5 rapor artefakt entegrasyonu, K3 gercek stream, K4 harici restore, K1 runtime kural kaniti halen acik. Eski depo ve korunan listeler degistirilmedi.


## 19 Ekim 2026 - K5 rapor entegrasyonu

K5 core.py icinde aday puanlama ve EPG/logo kanit sayaclari eklendi. Commit a4f5834. Uc yeni salt-okunur fixture kontrolu: candidate_k2_k3_k5_join, candidate_metadata_counts, candidate_report_read_only. Actions #68 success; #69 queued; #70 pending (sorgu aninda). Gercek yayin, cihaz IBO, K1 26 runtime kural, K4 harici restore ve uretim onayi halen acik. Eski depo ve korunan listeler degistirilmedi.


## 19 Ekim 2026 - K3 tekrarlanan kanit ve K4 bagimsiz restore fixture

Actions #69 ve #70 completed/success. `madsc/channel_test.py` tekrar olcumlerini ayni URL SHA256 ile kontrol eden evaluate_repeated_probes fonksiyonuyla genisletildi (cdabe5c); gercek ag olcumu iddiasi yok. `madsc/backup.py` uc ayri kaynak/yedek/restore klasorunun SHA256 manifestini karsilastiran verify_independent_restore fonksiyonuyla genisletildi (341d67e); gercek harici depolama kaniti yok. `tests/test_channel_test.py` (0ed9de8), `tests/test_backup.py` (3813cdf) dorder yeni regresyon senaryosu eklendi. `madsc/core.py` K3 ve K4 kategori fixture kabul kontrollerine baglandi (ab62827). Actions #75 sorgu aninda pending, #71 in_progress; ara commit run #72-74 cancelled gorundu, bu basari degildir. Eski depo, production listeler, cron degismedi. K1 26 runtime kural, gercek K3 ffprobe/IBO, K4 harici restore ve production kabul acik.


## 19 Ekim 2026 - Kisa devir ve test durumu

Actions #75 completed/success; #71 completed/success. #72-74 cancelled (neden kesin dogrulanmadi). K4 verify_independent_restore girdilerinde bos/gecersiz/tekrarlanan dosya adlari fail-closed reddedilir (66c85a0); test eklendi (ec92e41). Yeni commit Actions sonucu henüz dogrulanmadi. 99/99 eski workflow YAML ilk envanter tamam; davranissal entegrasyon tamam degil. K2-K3-K5 aday koordinasyonu, EPG/logo skor ve K5 fixture raporu kodlandi. K3 tekrar olcumleri ve K4 uc agac sandbox restore kontrolu fixture duzeyinde. K1 26 gercek runtime kural, K3 gercek yayin/IBO cihaz, K4 harici restore, production kabul acik. Eski Madsc55/madsc-tv dalina ve korunan listelere yazma YASAK. Yeni sohbet once bu dosyanin son bolumunu ve madsc/LEGACY_WORKFLOW_ON_ENVANTER.md dosyasini okusun; sonra Actions kontrol edip yeni Madsc55/Madsc55-Tv deposunda devam etsin.


## 19 Ekim 2026 - K3 ffprobe JSON kanit okuyucu

Actions #76 ve #77 completed/success. K3 madsc/channel_test.py icine saglanan ffprobe JSON streams ve duration degerlerini guvenli on degerlendiren evaluate_ffprobe_json eklendi (cc69c26). Gercek ag baglantisi veya 30 saniye kesintisiz oynatma iddiasi YOK; live_probe_executed_by_this_function false. tests/test_channel_test.py iki yeni regresyon testi (b6fe40a), madsc/core.py K3 fixture kabul kontrolu (9343e94) eklendi. Actions #80 pending, #79 in_progress, #78 cancelled sorgu aninda. K1 26 runtime kural, gercek K3 yayin olcumu, IBO cihaz ve K4 harici restore acik. Eski depo ve korunan listeler degismedi.


## 19 Ekim 2026 - K1 korunan yol on denetimi

Actions #79 ve #80 completed/success. K1 icin madsc/write_path_audit.py eklendi (af2aacd): onerilen depo yollarinda korunan liste, epg ve logo hedeflerini tespit eder; traversal ve mutlak yollari reddeder. Bu yalniz on denetimdir, gercek protected_write_gate runtime entegrasyonu DEGIL. tests/test_write_path_audit.py uc test (bbdac0a) ve madsc/core.py K1 fixture kaniti (03fc5b6) eklendi. Yeni Actions sonucu henuz teyit edilmedi. K1 26 gercek kural, K3 canli stream ve IBO cihaz, K4 harici restore acik. Eski depo ve korunan listeler degistirilmedi.


## 19 Ekim 2026 - K1 legacy write gate kural eslemesi

Actions #83 completed/success. Eski depodaki tools/protected_write_gate.py yalniz OKUNDU: exact korunan dosyalar, case-insensitive prefix ve herhangi .m3u/.m3u8 degisikligi engeli, git diff staged/unstaged/untracked/ignored kontrolu ve hata halinde fail-closed. Yeni madsc/write_path_audit.py yol politikasi bu kurallarla eslendi (1900248); test_write_path_audit.py guncellendi (b38eaea). Yeni audit gercek git push kapisi DEGIL; git_changed_paths ve 26 kural runtime kabul henuz uygulanmadi. Yeni Actions sonucu bekleniyor. K3 gercek yayin ve IBO, K4 harici restore acik. Eski depo ve korunan listeler degistirilmedi.


## 19 Ekim 2026 - YENI SOHBET DEVIR NOTU: Actions #159 basarili; K2-K3 metadata, K4 restore
BU BOLUM EN GUNCEL DEVIRDIR. Once bunu ve ilgili eski kaynak notlari oku; onceki tarihli durum satirlari tarihsel olup son durum degildir.

DEPO VE SINIRLAR: Yalniz yeni Madsc55/Madsc55-Tv deposunda gelistirme. Eski Madsc55/madsc-tv, DEVAM_NOTU.md, 810 dosya notu.md, AGENTS.md ve ilgili diger eski notlar kaynak olarak salt okunur. Her islemden once ilgili kaynaklari ve bu hafizayi oku; okunmayan not okunmus gibi gosterilmez. PR #71 birlestirme, main'e merge, eski workflow kapatma, cron acma, production yazma YOK. Ana kanal listeleri, YEDEKLER, YENILER, FAVORILER, cihaz favorileri, kanal URL/sira/EPG/logo/kimlikleri korunur. IBO Player'da calistigi kullanici tarafindan bildirilen kanal teknik testten kaldi diye silinmez; cihaz testini kullanici yapar. Testler topluca raporlansin; ara commit iptalleri son run basarisi sayilmaz.

SON ACTIONS KANITI (GitHub API ile 19 Ekim kontrol): #159 id 39263881587 commit 8c87ea6c COMPLETED/SUCCESS; #158 id 39262787933 commit 17227a2e SUCCESS; #157 id 39262748457 commit 66475404 SUCCESS; #156 id 39261378150 commit db562549 SUCCESS; #155 ve #154 cancelled (ara commitler). #150-#152, #146-#149 ve #142-#145 de success. Son run: https://github.com/Madsc55/Madsc55-Tv/actions/runs/39263881587 . Yeni sohbette ilk is en yeni Actions runlarini tekrar sorgulamak, hata varsa job adimlarini bulup duzeltmek.

K2-K3 YENI GELISMELER: madsc/discovery.py candidate kaydina name, tvg_id, tvg_logo, group_title ve url_sha256 koyuyor; source_import.py M3U/M3U8 EXTINF icindeki quoted comma alanlarini dogru ayiriyor; madsc/handoff.py bu alanlari salt-okunur K3 assessed raporuna tasiyor. Commitler: discovery 44b5eefc, source_import metadata fe6997f3, handoff b49c20c, test_handoff db562549, EXTINF quoted comma duzeltmesi 66475404, test_source_import 17227a2e, son M3U/M3U8 'TRT 1, HD' tam uctan uca test 8c87ea6c. Son #159 SUCCESS. Kanal adi/EPG kimligi/logo/grup tasinir, orijinal M3U/M3U8 byte'lari degismez. Bu gercek yayin testi veya IBO cihaz kaniti DEGIL. K3 handoff 'ibo_result_supplied' ile 'ibo_device_verified' ayrimini korur; cihaz kaniti yoksa ibo_device_verified=False. IBO WORKING + basarisiz teknik probe korunur, delete_allowed=False, production_change_allowed=False. Bu ayrim madsc/handoff.py f954d0c0, tests/test_handoff.py 734850cb, K3 fixture madsc/core.py 3dc14e6a ve tests/test_core.py 2d8e4f03 ile test edildi; Actions #141 ve #143 success.

K4 YENI GELISMELER: madsc/backup.py manifest kaynak kokunun symlink olmasini, bagimsiz restore agaclarinin symlink olmasini reddeder (a68ec6b6); tests/test_backup.py 064f9785. verify_sandbox_restore bos veya gecersiz isim listesiyle sahte basari uretmez (03ee6560; test 860a7138). K4 core.py bagimsiz restore fixture raporunda 'production_restore_verified=False', 'production_writes=False' ve kaynak/yedek/restore karsilastirma kanitini acik sinar (de6d5e75; test 4a8d8f35). tests/test_backup.py ic ice agac ve esdeger kok negatif testleri cbfac3b2; manifest duplicate/siralama ve yalniz listelenen dosyalarin kapsanmasi testleri 97621b61 ve a84bdbf6. Bunlar gercek harici yedekleme/production restore kaniti DEGIL. Manifestte bulunmayan dosyalarin eksikligini verify_manifest tek basina algilamaz; bu bilinen kapsam siniri.

K1/K5 VE GENEL DURUM: K1 protected path denetimleri ve statik workflow izin testleri var, ancak 26/26 gercek runtime guvenlik uygulama kaniti YOK. K5 besli sirali fixture kabul/rapor ve negatif artifact denetimleri var, fakat 92 (son envanterde 99) eski workflow'un davranissal birebir entegrasyonu KANITLANMADI. Fixture CI green = production hazir DEGIL. K3 gercek kesintisiz yayin testi, gercek IBO Player cihaz testi, EPG/logo gercek kaynak uyumu ve K4 harici restore halen acik. Production yetkileri kapali.

SIRADAKI IS: GitHub Actions son kosularini dogrula. K2-K3 metadata icin gercekci negatif/pozitif fixture kapsamindan sonra kaynak notlardaki 99 workflow davranis matrisi ve K1-K5 bagimliliklarini gercek entegrasyonla ilerlet; yalniz ufak test ekleyerek sonsuz oyalanma. Canli/prod degisiklikleri icin acik onay olmadan ilerleme. Her 'Yap' komutunda mumkunse gercek commit+test, kisa Turkce sonuc. 'Notlara kaydet' denirse SADECE bu PROJE_HAFIZASI.md dosyasina tarihli not ekle; eski kaynak notlari degistirme.


## 19 Ekim 2026 — ESKİ 810 DOSYA ENVANTERİ BULUNDU; İNCELEME SONRAYA BIRAKILDI
- Kaynak eski depo `Madsc55/madsc-tv`, dal `madsc/bes-sistem-toplu-birlestirme`; **salt okunur**. `810 dosya notu.md` bu dalın kökünde bulundu (eski `main` dalında aranması yanlış negatif sonuç vermişti). Bu dalın güncel Git ağacında 849 kayıt: 822 dosya ve 27 klasör; bu sayı eski 810'luk özgün manifestle karıştırılmamalı.
- `810 dosya notu.md` son devir kayıtlarına göre **özgün 810/810 dosya** envanterli; görsel olmayan **437/437** dosyanın D2 ilk içerik incelemesi önceki oturumlarda kayıtlı. Özgün 373 görsel kapsam dışı; önceki sayım D2=595, D1=215, D0=0, D3 davranışsal kabul=0. D2, her satırın ayrıntılı denetlendiği veya üretimde çalıştığı anlamına gelmez.
- `DEVAM_NOTU.md`, `AGENTS.md` ve `OZELLIK_ENVANTERI.md` ilgili kaynakları da doğrulandı. Tekrar inceleme yapmamak ve korunan listeleri değiştirmemek esastır.
- **YAPILACAK / ŞİMDİLİK ERTELENDİ:** Önceden mevcut 437 D2 metin/kod/veri kaydını kullanarak her dosyanın görevi, çağrı/bağımlılık zinciri, bulgusu, güvenlik etkisi, kanıt düzeyi ve açık işi için dosya bazlı nihai rapor hazırlamak; yalnız eksik kanıt gerektiğinde hedefli kaynak incelemek. 373 görseli açma/indirme/yeniden denetleme. 26 güvenlik kuralının gerçek uygulanması, 92 eski işlevin K1–K5 davranışsal eşdeğerliği, IBO cihaz, EPG ve harici restore kanıtları ayrı açık işlerdir; bunlar tamamlandı sayılmaz.
- **KULLANICI KARARI:** Bu aşamada yalnız notlara kaydet, raporu/incelemeyi şimdi sürdürme. Eski repo, PR #71, main merge, cron/production yazma ve korunan kanal listeleri değiştirilmeyecek. `Notlara kaydet` yalnız yeni deponun merkezi `PROJE_HAFIZASI.md` dosyasına yazılacak.


## 19 Ekim 2026 — KULLANICI KARARI: ESKİ DOSYA BULGULARI KURULUM SONU KONTROL LİSTESİ
- Kullanıcı eski 810 dosyanın işlevsel inceleme kayıtlarının korunmasını ve eksiklerin kurulum sonunda bu notlardan bulunmasını istiyor. Önceden yapılmış D2 ilk içerik incelemeleri tekrar sayılmayacak; ihtiyaç halinde eksik kanıt için hedefli inceleme yapılacak.
- Her somut bulgu merkezi hafızada dosya yolu, ilgili eski workflow/çağrı zinciri, K1–K5 karşılığı, eksik veya risk, kanıt/Actions run, durum (açık/doğrulandı/kapandı) ve kapanış şartıyla izlenecek. Kanıtsız tamamlandı işareti verilmeyecek.
- Kurulum sonunda bu kayıtlar üzerinden toplu eksik kontrolü ve kapanış raporu hazırlanacak. Mevcut 437 metin/kod/veri dosyası inceleme kaydı başlangıç kaynağı; görseller kullanıcı kararıyla kapsam dışı. Eski repo ve korunan listeler salt okunur; PR #71, main merge, üretim yazması veya eski workflow kapatma için izin yok.


## 19 Ekim 2026 — K2/K3 aday kanıt bağı doğrulaması (Actions sonucu bekleniyor)
- `madsc/candidate_coordination.py` içinde K2 aday URL SHA-256 parmak izleri artık 64 küçük harf hex olarak denetleniyor; K3 probe, tekrar sayısı ve kullanıcıdan sağlanan IBO kanıtı anahtarlarının yalnız keşifteki adaylara ait olması zorunlu. Yanlış/bağlantısız kanıt ValueError ile fail-closed; korunan listelere yazma yok. Commit `1d8220b1`.
- `tests/test_candidate_coordination.py` içine yanlış probe/tekrar/IBO kanıtı için negatif regresyon eklendi. Commit `3d442281`.
- GitHub Actions #160 (39265872644) queued, #161 (39265896149) pending kontrol anında; **başarı doğrulanmadı**. Kapanış şartı: #161 gerçek sonuç SUCCESS ve K2/K3/K5 ilgili fixture regresyonları geçmeli. IBO cihaz/gerçek yayın/production kanıtı değildir.


## 19 Ekim 2026 — K2/K3 kanıt zinciri #161 SUCCESS, K3 handoff yeni test bekliyor
- Actions #160 (39265872644) SUCCESS, #161 (39265896149) SUCCESS: K2 koordinasyonda yabancı probe/retry/IBO parmak izi reddi CI doğrulandı. Bu fixture düzeyi kanıt, gerçek cihaz/yayın kanıtı değil.
- `madsc/handoff.py` K2->K3 aktarımında aday listesinde olmayan probe veya IBO sonucu anahtarını artık reddeder (commit `be8675d2`). `tests/test_handoff.py` iki negatif regresyon ekler (commit `572518e6`). Korunan playlist ve production yazması yok.
- Kontrol anında #162 (39266283851) in_progress, #163 (39266301605) queued. **Yeni değişikliğin başarılı olduğu henüz doğrulanmadı.** Kapanış: #163 başarı sonucu ve ilgili testler. Eski 810 dosya incelemesi kurulum sonu kontrol listesinde bekliyor.


## 19 Ekim 2026 — K2-K3-K5 ortak kabul kanıtı
- #162 (39266283851) ve #163 (39266301605) SUCCESS: K2->K3 yabancı probe/IBO kanıtı reddi regresyonu geçti.
- `madsc/core.py` K5 fixture kabulüne K2 keşif -> K3 `assess_candidates` -> K5 `coordinate` aynı aday parmak izi, teknik statü, tvg-id ve salt-okunur karar tutarlılığı eklendi; commit `ba9ff6a6`. Bu ayrı sistemlerin gerçek production orkestrasyonu değildir, yalnız fixture çapraz kontrolüdür.
- Actions #164 (39267419274) kontrol anında queued. Sonucu doğrulanmadan tamamlandı denmeyecek. Korunan listeler, eski repo, PR #71 ve cron değiştirilmedi. Kapanış: #164 SUCCESS ve ardından eski 99 workflow davranışsal harita/gerçek kabul ayrı ilerlemeli.


## 19 Ekim 2026 — #164 SUCCESS ve dört eski workflow için gerçek davranış haritası (açık işler)
- Yeni K2-K3-K5 fixture tutarlılık commit `ba9ff6a6`, Actions #164 / 39267419274 **SUCCESS**. Bu yalnız fixture kabulü, üretim ve eski davranış eşdeğerliği değil.
- Eski `Madsc55/madsc-tv` / `madsc/bes-sistem-toplu-birlestirme` dalındaki dört YAML kaynak okunarak gerçek adım/artefakt incelemesi yapıldı; eski depoya yazılmadı:
  1. `.github/workflows/aday-bekletme.yml` (K2+K3+K5): `yeni_kanal_tara.py`, `aday_tekrar_raporu.py`, `gelismis_medya_testi.py`, `aday_bekletme.py`, `akilli_tekrar_test_takvimi.py`, `altinci_aday_tekrar_test.py` (RETEST_LIMIT=5), `kaynak_guven_puani.py`, `aday_oncelik_raporu.py`. Artefakt: 9 CSV/JSON/TXT yoluyla aday bekletme, geçmiş, güven, tekrar, medya ve öncelik. **AÇIK:** yeni K2-K3-K5'te zamanlı bekletme/persisted history/5'li retest/gerçek ffprobe/ayrı artefaktlar eşdeğerliği.
  2. `.github/workflows/akilli-aday-puanlama.yml` (K2+K3): `yeni_kanal_tara.py` SCAN_BATCH=-1; gerçek `scripts/oncelikli_kanal_dogrula.py` ffprobe; `scripts/akilli_aday_puanla.py`; 4 ayrı CSV/JSON rapor artefaktı. **AÇIK:** yeni sistem fixture skorundan bağımsız gerçek medya kanıtı, tarama kapsamı ve rapor parity.
  3. `.github/workflows/birlesik-aday-raporu.yml` (K2+K3+K5): cache restore ile `KARARLILIK_GECMISI.json`; tam aday keşfi; öncelikli+genel gerçek medya testleri; puanlama; `kanal_kararlilik_takip.py`; `birlesik_aday_raporu.py`; 4 çıktı artefaktı. **AÇIK:** uzunlamasına kararlılık cache zinciri, öncelikli/genel medya kapsamı, birleşik karar/rapor eşdeğerliği.
  4. `.github/workflows/madsc-birlesik-kesif.yml` (K1+K2+K3+K4+K5): cron UTC 06:00/18:00, `contents:write`+`actions:write`, yalnız main job, hata gate, `scripts/discovery_archive.py` before/after, `madsc_akilli_kesif.py`, `scripts/four_stage_discovery_report.py`; EPG join adımı `if: false` ile ertelenmiş. `madsc_kesif` artefaktı yanında `git push origin HEAD:main` yoluyla rapor yazma var; `tools/protected_write_gate.py --base origin/main` committen sonra, push'tan önce çağrılıyor. **AÇIK/YÜKSEK ÖNCELİK:** gerçek yazma hedefleri, koruma kapısının çalışma kanıtı, eski 2x günlük cron ve rapor arşivinin yeni salt-okunur sistemle çakışmadan karşılanması. Salt `contents:write` varlığı ihlal kanıtı değildir. Yeni cron, production yazması veya eski workflow emekliliği açılmayacak.
- Bu dört kayıt eski 99 workflow davranış haritasının **4 kaynak bazlı denetim girdisidir**; tüm 99 denetlendi veya eşdeğerliği tamamlandı iddiası yok. Kapanış için betiklerin gerçek çıktı şemaları, kalıcılık, zamanlama ve uçtan uca negatif/pozitif koşum kanıtları gerekir. IBO cihaz testi kullanıcıya aittir. Korunan listeler değişmedi.


## 19 Ekim 2026 — Eski aday puanlama, karar, arşiv ve koruma betikleri: kaynak denetimi
- Salt-okunur kaynaklar: eski dal `scripts/akilli_aday_puanla.py`, `scripts/birlesik_aday_raporu.py`, `scripts/discovery_archive.py`, `tools/protected_write_gate.py`. Bu dört betiğin kaynak içeriği incelendi; eski depoda işlem yapılmadı.
- `akilli_aday_puanla.py`: `YAYIN_URL` üzerinden CSV teknik kanıt birleştirme, görüntü 20 + ses 15 + çözünürlük 3/7/10 + HTTPS logo 5 puan; puanlama sadece adaydır, kimlik/kararlılık/IBO onayı ve listeye ekleme HAYIR. **AÇIK K2-K3:** yeni fixture skor formülü (50+EPG20+logo10-tekrar cezası) eski puan formülüne eşdeğer değil; ayrı puan şemaları/çıktı CSV ve JSON şeması, gerçek ffprobe ve rapor tüketicileri eşleştirilmeli. Aynı isimli skorun sessizce eşdeğer sayılması yasak.
- `birlesik_aday_raporu.py`: `AKILLI_ADAY_PUANLARI.csv` + `KARARLILIK_RAPORU.csv` URL join; bağımsız 24 saat kararlılığa +30 puan (100 üst sınırı); teknik/kararlılık/IBO-kimlik bekleme statüleri; `ANA_LISTEYE_EKLE=HAYIR`. **AÇIK K3-K5:** 24 saat geçmiş kanıtı, URL join ve çıktı alanları gerçek karşılaştırmalı testle doğrulanmalı; otomatik onay yok.
- `discovery_archive.py`: `madsc_kesif/gecmis.json` yoksa hata ile durur; `bulunan_kanal_arsivi.csv` ile URL kaynakları/ilk-son görülme, önce/sonra kalıcı kayıt; URL query'den token/auth/expires/signature/sig/hash anahtarları çıkarılarak eşleştirme. **AÇIK K2-K4-K5:** bu normalize anahtar ile yeni sistemin tam URL SHA-256 parmak izi farklı kimlik modeli; imzalı URL'lerin ayrı kanalları yanlış birleştirmemesi, gizli tokenların rapora sızmaması, kayıp geçmişin fail-closed olması ve uzun süreli kalıcılık kanıtlanmalı. Eski betik arşiv raporlarına yazar; korunan listelere yazdığı bu incelemede görülmedi.
- `protected_write_gate.py`: tam dosya ve klasör adları, her `.m3u/.m3u8` yolu, staged/unstaged/untracked/ignored dosyalar ile `base..HEAD` diff'ini engeller; kontrol başarısı GitHub branch ruleset yerine geçmez. **AÇIK K1:** gerçek GitHub Actions runtime gate + branch ruleset ve tüm workflow yazma yolları doğrulanmalı; eski workflow'daki push öncesi gate bu betiği çağırıyor ama yalnız kaynak kod okuması gerçek yürütme kanıtı değildir.
- Durum: Bu dört kaynak için **kod inceleme yapıldı, davranışsal eşdeğerlik açık**. Eski 99 YAML'ın tamamına genellenmez. Yeni üretim yazması/cron/PR #71/main merge yok.


## 19 Ekim 2026 — Eski teknik aday puanlama sözleşmesi ayrı modüle taşındı
- Eski `scripts/akilli_aday_puanla.py` içindeki görüntü +20, ses +15, çözünürlük +3/+7/+10, HTTPS logo +5 ve `TEKNIK_ADAY` / `EK_DOGRULAMA_GEREKLI` karar mantığı yeni depoda salt-okunur `madsc/legacy_scoring.py` fonksiyonuyla **ayrı sözleşme** olarak uygulandı (commit `5ab9cb42`). Mevcut K2/K3/K5 puanlama mantığına sessizce karıştırılmadı; gerçek yayın/kimlik/IBO/üretim onayı verilmez.
- `tests/test_legacy_scoring.py` eşik, durum, negatif veri ve iki skorun farklılığı için testler içerir (commit `1a0b250c`). Kontrol anında Actions #165 / 39268391099 in_progress, #166 / 39268413739 pending; **başarı henüz doğrulanmadı**.
- **AÇIK:** CSV kaynak birleştirme, eski rapor şemaları, URL kimlik modeli, 24 saat kararlılık ve gerçek ffprobe eşdeğerliği; modül eklemek 99 workflow davranış eşdeğerliği değildir. Korunan listeler/cron/PR #71/main merge değiştirilmedi.


## 19 Ekim 2026 — Eski 24 saat kararlılık kararının salt-okunur eşleştirmesi
- `madsc/legacy_scoring.py` içinde eski `scripts/birlesik_aday_raporu.py` kararının ayrı saf fonksiyonu eklendi: 24 saat kararlıysa +30, toplam 100 üst sınırı; teknik+kararlı `IBO_VE_KIMLIK_ONAYI_BEKLIYOR`, yalnız teknik `KARARLILIK_BEKLIYOR`, diğer `TEKNIK_DOGRULAMA_BEKLIYOR`; IBO/kullanıcı onayı YOK ve ana listeye ekleme HAYIR. Commit `0afe11a2`.
- `tests/test_legacy_scoring.py` durum/eşik/yanlış kanıt testleri eklendi; commit `2e6fd368`. Kontrol anında #166 queued, #167 pending, #168 queued: **test başarı sonucu henüz doğrulanmadı**.
- **AÇIK:** Gerçek 24 saat geçmiş verisini okuma ve bağımsız doğrulama, CSV `YAYIN_URL` join, rapor çıktısı şeması, gerçek ffprobe ve arşiv persistency. Saf fonksiyon yalnız verilen `stable_24h` kanıtını yorumlar; 24 saat izlendi iddiası yok. Korunan listeler/production/cron/PR #71/main merge değişmedi.


## 19 Ekim 2026 — Eski birleşik aday raporu CSV sözleşmesi (salt-okunur)
- Actions #166 / 39268413739 SUCCESS, #168 / 39268672688 SUCCESS; #167 CANCELLED (başarılı sayılmadı).
- Yeni `madsc/legacy_unified_report.py` eski `scripts/birlesik_aday_raporu.py` 10 alanlı çıktı CSV şemasını, `YAYIN_URL` eşleşmesini, kararlılık `EVET` yorumunu, puana göre azalan/kanala göre artan sıralamayı ve IBO/kullanıcı/ana liste onayını `YOK`/`HAYIR` olarak tutan **saf salt-okunur** görünüm olarak taşır (commit `3e964318`). `tests/test_legacy_unified_report.py` URL join, sıralama, boş rapor ve geçersiz kayıt regresyonlarını içerir (commit `c8f61448`).
- Kontrol anında Actions #169 / 39268992498 queued ve #170 / 39269024472 queued; yeni modül CI başarısı **henüz doğrulanmadı**.
- Bu kod CSV dosyalarını okumaz/yazmaz, gerçek 24 saat ölçümü veya cihaz onayı yapmaz; yalnız çağıranın verdiği satırları değerlendirir. **AÇIK:** dosya IO/artefakt paritesi, cache geçmişi güvenilirliği, gerçek ffprobe ve eski URL arşiv kimliği, bütün 99 workflow davranış eşdeğerliği. Korunan listeler ve eski repo değişmedi.


## 19 Ekim 2026 — Eski birleşik aday raporu CSV/JSON artefakt dışa aktarımı
- Actions #169 / 39268992498 SUCCESS, #170 / 39269024472 SUCCESS.
- `madsc/legacy_report_export.py` açıkça verilen iki CSV girdisini okuyup eski `BIRLESIK_ADAY_ONAY_RAPORU.csv` (UTF-8 BOM, 10 alan) ve `BIRLESIK_ADAY_OZET.json` raporlarını yalnız yeni ve boş **depo dışındaki** çıktı dizinine yazar; mevcut dizin üzerine yazmayı, repo içine yazmayı, eksik CSV başlığını reddeder. Commit `6eab20bd`. `tests/test_legacy_report_export.py` çıktı ve fail-closed durumlarını sınar; commit `f5365fc3`.
- Actions #171 / 39269514254 queued, #172 / 39269544435 pending; bu yeni değişikliklerin CI başarısı henüz doğrulanmadı.
- **AÇIK:** 24 saat kararlılık ölçümü yalnız CSV'de gelen `EVET` değerini yorumlar; bağımsız geçmiş doğrulaması, gerçek ffprobe, gerçek üretim iş akışı/artefakt yükleme ve 99 eski workflow eşdeğerliği kanıtlanmadı. Korunan listeler, eski depo, cron, PR #71 ve main merge değişmedi.


## 19 Ekim 2026 — Gerçek geçmiş zaman damgasıyla 24 saat kararlılık kararının kontrolü
- Actions #171 / 39269514254 SUCCESS, #172 / 39269544435 SUCCESS.
- Eski `scripts/kanal_kararlilik_takip.py` okundu. Eski sözleşme: zaman damgalı bağımsız VIDEO_SES_VAR ölçümleri arasında en az 24 saat; son ölçüm en fazla 24 saat eski; tüm son 7 günlük gözlemler başarılı; aynı zamanlı çelişkili durum reddedilir; tekrarlanan zaman damgası yeni gözlem sayılmaz; gelecek/naive zamanlar reddedilir; IBO/liste onayı verilmez.
- Yeni `madsc/legacy_stability.py` bu kararın salt-okunur saf değerlendirmesini uygular (commit `1ac34655`); `tests/test_legacy_stability.py` tekrar, hata, bayat veri, kısa aralık ve geçersiz zaman damgası testlerini içerir (commit `e2ab03bb`). Actions #173 / 39270210037 queued, #174 / 39270240380 pending; **CI sonucu henüz doğrulanmadı**.
- **AÇIK:** gerçek medya ölçümlerini toplamak, kalıcı geçmişi yazıp güvenle restore etmek, 24 saat boyunca fiilen izlemek ve rapor CSV ile otomatik bağlantı. Şu anda yalnız sağlanan geçmiş kanıtı değerlendirilir; canlı ağ/IBO cihaz testi yapılmadı. Korunan listeler/cron/main/PR #71/legacy repo değişmedi.


## 19 Ekim 2026 — 24 saat geçmiş kanıtı birleşik rapora bağlandı
- Actions #173 / 39270210037 SUCCESS ve #174 / 39270240380 SUCCESS.
- `madsc/legacy_unified_report.py` isteğe bağlı `history` ve `now` parametreleriyle `madsc/legacy_stability.py` zaman damgası değerlendirmesini rapora bağlar. Geçmiş verisi verilirse CSV'deki `24_SAAT_KARARLI=EVET` tek başına yeterli değildir; aynı `YAYIN_URL` için bağımsız iki başarılı gözlem, >=24 saat aralık, son 24 saatte tazelik ve son 7 günde hata olmaması gerekir. Eksik geçmiş/tekrar edilen ölçüm kararlılık puanını +30 artırmaz. Geriye dönük CSV-only yol ayrıca mevcuttur, `historical_evidence_source=csv_only` olarak işaretlenir ve gerçek kanıt sayılmaz. Commit `59b1527c`.
- `tests/test_legacy_unified_report.py` olumlu/eksik/tekrar/CSV yok senaryolarını test eder; commit `935e9659`. Actions #175 / 39270726045 in_progress, #176 / 39270756670 pending; yeni CI sonucu henüz doğrulanmadı.
- **AÇIK:** rapor dışa aktarımında gerçek JSON geçmişini dosyadan okuyup bu doğrulama yoluna bağlamak; geçmiş restore/persist; gerçek 24 saatlik medya ölçümü. `historical_stability_verified=True` yalnız **sağlanan geçmişin kurala uygun incelendiğini**, geçmişin sahada toplandığını değil belirtir. Korunan listeler, cron, PR #71, main merge ve eski repo değişmedi.


## 19 Ekim 2026 — CSV/JSON rapor dışa aktarımına tarihsel kanıt eklendi
- Actions #175 / 39270726045 SUCCESS ve #176 / 39270756670 SUCCESS.
- `madsc/legacy_report_export.py` artık isteğe bağlı `history_json` ve `now` kabul eder; `KARARLILIK_GECMISI.json` biçimindeki URL->gözlem listesi verildiğinde birleşik CSV'deki 24 saat kararlılık kararı gerçek zaman damgalı gözlemlerle çapraz kontrol edilir. Geçmiş yoksa eski CSV-only uyumluluk yolu sürer, JSON özetinde `historical_evidence_source=csv_only` olarak açıkça etiketlenir. Geçmiş JSON hatalıysa çıktı klasörü oluşturulmadan fail-closed. Commit `5bb03d3e`.
- `tests/test_legacy_report_export.py` geçerli geçmiş, eksik geçmişin +30 puan vermemesi ve hatalı geçmişte çıktı oluşturmama senaryolarını kapsar. Commit `c32cbe79`. Actions #177 / 39271468192 in_progress, #178 / 39271507933 pending; henüz başarı kanıtı yok.
- **AÇIK:** üretim pipeline'ında tarihsel JSON girdisinin zorunlu kılınması, güvenilir restore/persist, gerçek ffprobe ve 24 saat boyunca medya ölçümü; IBO cihaz testi kullanıcıda. Korunan listeler, eski depo, cron, PR #71 ve main merge değiştirilmedi.


## 19 Ekim 2026 — #178 hata düzeltmesi ve zorunlu geçmiş modu
- Actions #177 SUCCESS, #178 FAILURE; #178 için yeni eklenen CSV fixture'larında satır sonlarının yanlışlıkla `\\n` olarak kodlandığı görüldü. Test verisi gerçek `\n` satır sonuna düzeltildi (commit `dbbc7f27`). #179 CANCELLED.
- `madsc/legacy_report_export.py` `require_history=True` fail-closed seçeneği eklendi: JSON geçmişi olmadan rapor üretimini reddeder (commit `97d258f5`). Mevcut CSV-only geriye uyum modu varsayılan olarak sürer; güvenilir üretim pipeline'ında `require_history=True` kullanılmalıdır. Regresyon testi commit `d07720f8`.
- Actions #180 / 39271773115 queued, #181 / 39271798065 pending; başarı henüz doğrulanmadı. **AÇIK:** üretim pipeline'ına güvenli entegrasyon, kalıcı tarihsel kanıt ve gerçek medya testleri. Korunan listeler, eski repo, cron, main ve PR #71 değişmedi.


## 19 Ekim 2026 — #180/#181 gerçek log kök neden düzeltmesi
- Actions #180 ve #181 FAILURE. #181 job logu incelendi: K1 Güvenlik `test_export_history_corroborates_csv_claim` testinde `Missing YAYIN_URL header` hatası, diğer K2/K3/K4/K5 ve kabul jobları SUCCESS. Kök neden: `legacy_report_export.py` history JSON yolunu `sources` listesine ekleyip CSV okuyucusuyla **tüm** kaynakları okuması. `scores, stability = [load(path) for path in sources[:2]]` düzeltildi; history JSON ayrı `json.load` ile okunmaya devam eder, yol izolasyonu için `sources` listesinde kalır. Commit `a0e4a9d3`.
- Yeni commit sonrası Actions sonucu henüz doğrulanmadı. Korunan listeler, eski repo, PR #71, cron ve main merge değişmedi.


## 19 Ekim 2026 — #182 geçti; eski CSV şemasıyla doğrudan karşılaştırma
- Actions #182 / 39272207360 SUCCESS: JSON'un CSV okuyucusuna gitmesi hatası düzeltmesi CI ile doğrulandı.
- Eski depodaki `scripts/birlesik_aday_raporu.py` ve `scripts/akilli_aday_puanla.py` kaynakları tekrar okundu. Birleşik çıktıdaki 10 alan ve `AKILLI_ADAY_PUANLARI.csv` 13 alan şeması doğrulandı; `TEKNIK_KANIT`, `PUAN`, `YAYIN_URL`, `KAYNAK` alanları gerçek eski kaynaktan teyit edildi. Yeni raporun 10 alanlı sıralaması ve durum kararları kaynakla uyumlu. Eski skor scripti adayları URL'ye göre tekilleştirirken yeni birleşik görünüm aynı URL'yi iki kez raporlayabiliyordu; artık duplicate URL fail-closed reddediliyor (commit `05fba911`, test `35ad11b0`).
- Actions #183 / 39273289239 in_progress, #184 / 39273307180 pending; yeni commitlerin CI sonucu henüz doğrulanmadı. Bu kontrol gerçek saha ffprobe veya IBO cihaz testi değildir. Korunan listeler, cron, eski repo, main merge ve PR #71 değişmedi.


## 19 Ekim 2026 — #183/#184 geçti; geçmiş eşleştirme doğrulaması
- Actions #183 / 39273289239 SUCCESS ve #184 / 39273307180 SUCCESS.
- `madsc/legacy_unified_report.py` CSV kararlılık alanında yalnız `EVET`/`HAYIR` kabul eder; eksik/bilinmeyen değer fail-closed reddedilir. Sağlanan tarihsel URL->gözlem eşlemesinin URL anahtarları boş olmayan metin, değerleri liste olmalıdır. Commit `93c384af`. Regresyon testleri `de3e2c8f`.
- Actions #185 / 39273845451 queued ve #186 / 39273862210 queued; sonuç henüz doğrulanmadı. Gerçek medya testleri, kalıcı tarihsel kanıt, IBO cihaz onayı hâlâ açık. Korunan listeler, eski repo, cron, main merge ve PR #71 değişmedi.


## 19 Ekim 2026 — #185/#186 başarılı; tam tarihsel geçmiş doğrulaması
- Actions #185 / 39273845451 SUCCESS ve #186 / 39273862210 SUCCESS.
- Eski `scripts/kanal_kararlilik_takip.py` tekrar okundu: `KARARLILIK_GECMISI.json` URL->`[{at,state}]` biçimi ve bütün geçmişin doğrulanması teyit edildi. Yeni `madsc/legacy_unified_report.py` artık geçmiş JSON verildiğinde sadece rapordaki adayların değil, dosyadaki **tüm** URL gözlemlerinin zaman damgalarını ve çelişkilerini doğrular; alakasız URL'de bozuk kayıt varsa fail-closed. Commit `62f431d9`, test `3bfe3959`.
- Actions #187 / 39275828816 in_progress ve #188 / 39275852182 queued; sonuç henüz doğrulanmadı. Gerçek 24 saat ölçüm, kalıcı geçmiş ve IBO cihaz doğrulaması yapılmadı. Korunan listeler, eski repo, cron, main merge ve PR #71 değişmedi.


## 19 Ekim 2026 — #187/#188 başarılı; test edilmemiş geçmiş reddi
- Actions #187 / 39275828816 SUCCESS ve #188 / 39275852182 SUCCESS.
- Eski `scripts/kanal_kararlilik_takip.py` ölçüm oluştururken `TEST_EDILMEDI` durumunu reddeder. Yeni `madsc/legacy_stability.py` artık geçmiş JSON'da da bu değeri geçerli ölçüm saymaz, fail-closed hata verir (commit `f395017b`), regresyon testi `a764119a`. Böylece bozuk geçmişin rapor üretiminde sessizce kabulü önlenir.
- Actions #189 / 39276340033 in_progress; son commit testi henüz doğrulanmadı. Gerçek yayın testi, geçmiş kalıcı saklama ve IBO cihaz onayı hâlâ açık. Korunan listeler, eski repo, cron, main merge ve PR #71 değişmedi.


## 19 Ekim 2026 — #189/#190 başarılı; JSON tekrarlı anahtar engeli
- Actions #189 / 39276340033 SUCCESS ve #190 / 39276356175 SUCCESS.
- `legacy_stability.py` açık ölçüm zamanı yoksa reddi daha görünür kılındı (`ffcb4891`); `_time` zaten reddettiği için bu esasen ek koruyucu açıklıktır.
- Önemli: Python `json.load` tekrarlanan URL anahtarını sessizce son değerle değiştirir; `legacy_report_export.py` geçmiş JSON okurken `object_pairs_hook` ile tekrarlı anahtarı artık fail-closed reddeder (`4e007ce6`). Regresyon testi (`23bd96df`) rapor klasörü yaratılmadan reddi doğrular.
- Actions #191 / 39276798815 queued, #192 / 39276825565 cancelled, #193 / 39276846308 pending; yeni kod için henüz başarı teyidi yok. Korunan listeler, eski repo, cron, main merge ve PR #71 değişmedi. Gerçek medya/IBO testi yapılmadı.


## 19 Ekim 2026 — #191/#193 başarılı; CSV başlık çakışması
- Actions #191 / 39276798815 SUCCESS, #192 / 39276825565 CANCELLED, #193 / 39276846308 SUCCESS. İptal koşusu başarı sayılmadı.
- `legacy_report_export.py` CSV DictReader tekrarlanan sütun adlarında önceki değeri sessizce ezebildiği için skor veya kararlılık dosyasındaki tekrar eden CSV başlıklarını fail-closed reddeder (`c8330876`). Regresyon testi `3b4d1fde`; hatalı dosyada rapor klasörü açılmaz.
- Actions #194 / 39277187458 in_progress, #195 / 39277204007 pending; yeni değişikliklerin CI sonucu henüz doğrulanmadı. Korunan listeler, eski repo, cron, main merge ve PR #71 değişmedi. Gerçek medya/IBO cihaz testi yapılmadı.


## 19 Ekim 2026 — BEŞLİ SİSTEM TOPLU DEVİR VE KALDIĞIMIZ NOKTA (yeni sohbet başlangıç kaydı)

**Kimlik ve sınırlar:** Aktif yeni depo `Madsc55/Madsc55-Tv`; proje görünen adı **Madsc55-Tv**. Eski `Madsc55/madsc-tv` / `madsc/bes-sistem-toplu-birlestirme` yalnızca okuma ve davranış karşılaştırma kaynağı. `PROJE_HAFIZASI.md` tek merkezi not noktası. İşlemden önce `DEVAM_NOTU.md`, `810 dosya notu.md`, `AGENTS.md` ve ilgili tüm kaynakları oku. Korunan ana kanal listeleri, YEDEKLER, YENİLER, FAVORİLER, cihaz favorileri, EPG, logolar, URL/ID/sıra değiştirilmez. Main'e merge, PR #71 merge, cron/üretim yazması, kanıtsız eski otomasyon kapatma yok. IBO Player Pro cihaz testini kullanıcı yapacak; teknik testten kalan fakat IBO'da çalışan kanal korunacak, YEDEKLER kararı ancak onaylı süreçle uygulanacak.

**Genel hedef:** Eski 92 workflow'un gerçek davranışlarının K1–K5 içinde karşılanması. Eski dalda 99 YAML dosyası görüldüğü için 92/99 sayım farkı çözülmedi. 810/810 dosya envanteri; 437 görsel dışı dosyanın ilk incelemesi, 373 görsel kullanıcı isteğiyle kapsam dışı. Davranışsal 92/92 kabulü **yok**. CI'nin başarılı olması üretim veya cihaz testi değildir. Fail-fast yerine mümkün olduğunca tüm testleri çalıştırıp toplu raporla.

**K1 güvenlik:** `madsc/core.py` ile izole fixture yazma-yolu kontrolü, `madsc/write_path_audit.py` ve testler var. Eski `tools/protected_write_gate.py` korunan dosya/prefix ve .m3u/.m3u8 için git diff/staged/untracked/ignored kontrolleri yapıyor; yeni sistemde 26/26 güvenlik kuralının gerçek uygulaması, workflow permissions ve gerçek yazma yolları **henüz kanıtlanmadı**. Üretim yazma izni açılmayacak.

**K2 keşif/adayı bekletme:** .m3u + .m3u8 keşif fixture'ları, aday sınıflandırma, fingerprint, `madsc/candidate_coordination.py` (yalnız 64 küçük hex, yetim probe/IBO reddi), `madsc/handoff.py` aktarımı; eski aday bekletme/yeniden test/öncelik/kaynak güven puanı iş akışlarının tam davranışsal karşılığı **açık**. Eski `scripts/akilli_aday_puanla.py` teknik puan formülü `madsc/legacy_scoring.py` ile taşındı: video20, ses15, çözünürlük3/7/10, HTTPS logo5; teknik puan kimlik kanıtı değildir.

**K3 canlı yayın testi ve süreklilik:** `madsc/channel_test.py` izole ffprobe JSON/tekrarlı probe değerlendirmeleri var; gerçek canlı ağ/ffprobe ölçümü ve 24+ saat tarihsel kanıtın otomatik toplanması **henüz kanıtlanmadı**. `madsc/legacy_stability.py` yalnız sağlanan zaman damgalı geçmişi kontrol eder (7 gün pencere, en az iki ayrı başarılı VIDEO_SES_VAR gözlemi, >=24 saat açıklık, <=24 saat tazelik, pencere içinde hata yok). TEST_EDILMEDI ölçüm olarak reddedilir; geçmiş gerçek ölçüm yapılmış gibi gösterilmez. IBO cihaz testi kullanıcıda.

**K4 yedek/geri yükleme:** `madsc/backup.py` fixture snapshot/manifest, karşılaştırma, sandbox/bağımsız restore denetimleri var; gerçek dış konum yedeği, geri yükleme ve üretim bütünlük kanıtı **açık**. Korunan listelere dokunma.

**K5 bakım, koordinasyon ve birleşik rapor:** `madsc/maintenance.py`, `madsc/dependencies.py`, `madsc/core.py` K2→K3→K5 fixture kabulü ve `madsc/legacy_unified_report.py` mevcut. Eski raporun gerçek 10 sütun şeması ve `AKILLI_ADAY_PUANLARI.csv` 13 sütunu eski koddan doğrulandı. `madsc/legacy_report_export.py` CSV/JSON raporunu yalnız **yeni ve repo dışındaki** dizine açık istekle yazar; üretim listelerine yazmaz. `require_history=True` geçmiş yoksa durdurur; CSV-only uyumluluk modunda +30 kararlılık puanı CSV EVET'e dayanabilir, **doğrulanmış saha kanıtı değildir**. Gerçek raporlama akışına entegrasyon ve toplu üretim kabulü **açık**.

**Son düzeltmeler:** JSON geçmişi CSV olarak okuma hatası düzeltildi `a0e4a9d3`; yinelenen aday URL'si reddi `05fba911` + test `35ad11b0`; yanlış CSV kararlılık değerleri / geçmiş URL haritası `93c384af` + `de3e2c8f`; geçmişteki tüm URL kayıtlarını doğrulama `62f431d9` + `3bfe3959`; TEST_EDILMEDI geçmiş ölçümü reddi `f395017b` + `a764119a`; zaman damgası kontrolü `ffcb4891`; JSON yinelenen anahtar reddi `4e007ce6` + `23bd96df`; CSV yinelenen başlık reddi `c8330876` + `3b4d1fde`.

**En son CI kanıtı:** Actions #194 (39277187458) **SUCCESS**, #195 (39277204007) **SUCCESS**. #192 CANCELLED, başarı sayılmadı. En son yeni değişiklikler için başarılı fixture CI var; 26/26, 92/92, gerçek ffprobe, IBO, K4 bağımsız üretim restore kanıtı yok.

**Sıradaki iş sırası:** (1) 92 vs 99 workflow kapsam/harita farkını gerçek kaynaklarla kapat; (2) K2–K3–K5 aday keşfi → gerçek ölçüm zamanlı test → kararlılık → rapor zincirini gerçek eski veri şemalarıyla uçtan uca ve fail-closed doğrula; (3) K1 26 güvenlik kuralının workflow/izin/yazma kapısı gerçek uygulama kanıtı; (4) K4 bağımsız yedek/restore; (5) tüm testlerin tamamlandığı birleşik kabul raporu. Üretime geçiş veya korunan dosyalara yazma için ayrı açık onay gereklidir.


## 19 Ekim 2026 — 99 eski workflow tam dosya envanteri
- Eski salt-okunur `Madsc55/madsc-tv` dalı `madsc/bes-sistem-toplu-birlestirme`, commit `ca374df3b9585c0d76a078db9536150ebbc260f7`, tree `a88dfa874b6964dcaa4de7a8f9075af2f146acd8` REST üzerinden recursive ve `truncated=false` olarak tarandı. Toplam 849 tree girdisi içinde `.github/workflows/*.yml|yaml` sayısı **99**.
- Yeni depoda `docs/ESKI_WORKFLOW_99_ENVANTER.md` dosyasında **99/99 dosya adı** tek tek kaydedildi (commit `6df94d10`). Dosya adına göre gruplar: eski `madsc-01`..`madsc-05` = 5; `test-13`..`test-39` = 27; kalan = 67. Bu gruplama davranışsal inceleme değildir; eski 92 workflow iddiasıyla 99 YAML farkı **henüz çözülmedi**. Hiçbir eski workflow kapatılmadı.
- Son doğrulanmış yeni depo CI: #194 ve #195 SUCCESS. Envanter dokümantasyon commitinin CI sonucu ayrıca kontrol edilmeli. Sonraki iş: 99 dosyayı tetik, izin, çalıştırdığı script, okuma/yazma yolları ve K1–K5 bağımlılıklarına göre **davranışsal** sınıflandır; 92 kapsamını somut kanıtla belirle. Korunan listeler, eski depo, main merge, cron ve PR #71 değişmedi.


## 19 Ekim 2026 — ilk 8 eski workflow'un gerçek YAML davranış haritası
- Yeni `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` dosyası oluşturuldu (`c1246897`) ve K4 kaynağının ayrıntılarıyla güncellendi (`b1c09181`). Salt-okunur eski YAML'dan 5 eski toplu K1..K5 + `aday-bekletme`, `akilli-aday-puanlama`, `birlesik-aday-raporu` olmak üzere **8 dosyanın** tetikleri, permissions, script zincirleri, çapraz bağımlılıkları ve eksik gerçek kabul kanıtları kaydedildi. 99/99 dosya envanteri `docs/ESKI_WORKFLOW_99_ENVANTER.md` içinde, **91 dosyanın ayrıntılı eşlemesi açık**.
- Önemli bulgular: Eski K5'in 92 satırlık matrisi bilerek `BLOCKED_NEEDS_BEHAVIOR_EVIDENCE` bekliyor; 92/92 kabul değil. Eski K2 salt-okunur shadow cron (05:17/17:17 ve 06:00/18:00 UTC), yeni depoda cron açılmadı. Eski K3 gerçek ffmpeg/ffprobe ve 100 kanallık salt-okunur health ölçümü çalıştırıyordu; yeni fixture aynı saha kanıtı değil. Eski K4 offsite `DOGRULANMADI` ve historical recovery false olmasını **özellikle** şart koşuyor; bağımsız yedek/restore onaylanmış değil.
- Son doğrulanmış yeni CI #194/#195 SUCCESS; yeni yalnız dokümantasyon commitleri için yeni Actions koşusu görünmedi. Sıradaki: kalan 91 workflow'u YAML tetik/izin/script/artefakt ve K1–K5 işlevine göre eşle, 92/99 farkını gerçek kapsam kriteriyle çöz. Korunan listeler, eski depo, main merge, cron ve PR #71 değişmedi.


## 19 Ekim 2026 — ikinci 8 YAML davranış eşlemesi, 16/99
- Salt-okunur eski kaynaktan `kanal-kararlilik`, `genel-aday-medya-test`, `aday-logo-epg-test`, `aday-yedekleme`, `felaket-kurtarma-tatbikati`, `madsc-birlesik-kesif`, `epg-gunluk`, `epg-pages` YAML dosyaları incelendi; tetikler, izinler, script/artefakt zincirleri, K1–K5 karşılıkları ve eksikler `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` dosyasına eklendi (commit `cc6829e5`). **16/99 ayrıntılı dosya eşlendi, 83 açık.** 92/99 kapsam farkı ve davranışsal kabul hâlâ açık.
- Güvenlik: eski `madsc-birlesik-kesif.yml` contents:write/actions:write ve main'e `git push` içerir; eski `epg-gunluk.yml` contents:write ile EPG git push; `epg-pages.yml` pages:write/id-token:write ile workflow_run sonrası dağıtım. Bunlar yeni sisteme taşınmadı, cron/push/deploy açılmadı. `aday-yedekleme` yalnız artifact taslağı üretir, korunan YEDEKLER'e yazma onayı değildir.
- Son doğrulanmış yeni depo Actions #194/#195 SUCCESS; bu dokümantasyon değişikliğinin CI sonucu ayrıca doğrulanmadı. Sıradaki: kalan 83 YAML davranış eşlemesi, yazma yetkilerinin toplu risk envanteri, 92/99 farkının kanıtı. Korunan listeler, eski depo, main merge ve PR #71 değişmedi.


## 19 Ekim 2026 — üçüncü grup 12 workflow, toplam 28/99
- Eski salt-okunur dalda 12 ek YAML'ın gerçek tetik, izin, temel script/artefakt komutları incelendi ve `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` dosyasına eklendi (`27c9efac`). Toplam **28/99** kaynak YAML ilk davranış/komut eşlemesi; **71 açık**. Bu, 28 işlevin üretimde eşdeğer çalıştığı anlamına gelmez.
- Yeni riskler: `madsc-genis-kaynak-kontrol.yml` ve `madsc-son-kontrol.yml` contents:write/actions:write; tüm shell içi yazma yollarının satır satır incelenmesi gerekiyor. `madsc-arsiv-yedek-aktarim.yml` bilerek otomatik protected playlist değişikliğini kapalı tutuyor. `madsc-aylik-merkezi-denetim.yml` birçok K1–K5 kontrolünü birleştiriyor; yeni sistemin gerçek kabulü açık.
- Son doğrulanmış Actions #194/#195 SUCCESS; bu yeni dokümantasyon değişikliği için koşu sonucu henüz teyit edilmedi. 92/99 kapsam farkı, 26/26 kural, canlı K3, bağımsız K4, gerçek 92/92 kabul açık. Korunan listeler, eski depo, cron, main merge ve PR #71 değiştirilmedi.


## 19 Ekim 2026 — IBO kaynak YAML grubu, toplam 40/99
- 12 IBO eski workflow'u salt-okunur kaynak YAML'dan tetik/izin/script/staging/artefakt açısından incelendi. `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` güncellendi, commit `a0abf5a2`. **40/99** ilk davranış eşlemesi, **59** YAML kaldı. Bu üretim davranışsal kabulü değil.
- **8 yüksek yazma riskli eski IBO workflow:** `madsc-ibo-354-classify.yml`, `madsc-ibo-364-355-364.yml`, `madsc-ibo-398-16-49.yml`, `madsc-ibo-530-archive.yml`, `madsc-ibo-6115-second.yml`, `madsc-ibo-ilk-239.yml`, `madsc-ibo-kararlar-grup1.yml`, `madsc-ibo-second-voice.yml`. Hepsinde `contents:write`, `git add CALISANLAR.m3u`, `tools/protected_write_gate.py` ve `git push origin HEAD:main` bulunuyor. Gate çalışıp çalışmadığı / gerçekten push olduğu kanıtlanmadı. Korunan listeye yazma davranışı yeni sisteme aktarılmayacak; IBO cihaz testi kullanıcıda.
- Salt-okunur IBO medya test, EPG kimlik, yedek kalite artefakt işlevleri K2/K3/K4 kapsamında daha sonra gerçek davranışla doğrulanacak. Eski repo, korunan listeler, cron, main merge ve PR #71 değiştirilmedi. Son doğrulanmış yeni CI #194/#195 SUCCESS; yalnız dokümantasyon commitleri için yeni test sonucu yok.


## 19 Ekim 2026 — numaralı 27 test YAML tarandı, toplam 67/99
- Eski dalın `test-13` ile `test-39` arasındaki **27 workflow YAML** dosyasının tamamı salt-okunur açıldı; tetikler, permissions ve adım adları incelendi. `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` güncellendi, commit `cb55d60d`. Toplam **67/99 ilk eşleme**, **32 YAML kaldı**. Numaralı testlerin tümünde `contents:read`; `test-31` yalnız dispatch, diğerlerinde push/dispatch görüldü.
- Bunlar test YAML dosyalarıdır; fixture/denetim testinin varlığı canlı K3, K1 26/26 runtime güvenlik veya 92/92 davranışsal kabul kanıtı değildir. 92 vs 99 farkı hâlâ çözülmedi; 27 test dosyasını kanıtsız kapsam dışına atmayacağız. Korunan listeler, eski repo, cron, main merge ve PR #71 değişmedi.


## 19 Ekim 2026 — 99/99 eski YAML ilk kaynak incelemesi TAMAMLANDI
- Bu turda 32 kalan workflow'un 29'u (keşif, tekrar test, yedek, VOD, PNG logo, protected gate, kanal test) ve envanter karşılaştırmasıyla tespit edilen son 3 `aday-oncelik-kontrol.yml`, `sekizinci-tekrar-raporu-test.yml`, `test-kanal-adaylari.yml` salt-okunur YAML kaynaklarından açıldı. `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` güncellendi; commitler `7552c7cb`, `59e2e53f`. Böylece **99/99 eski YAML dosyasının ilk tetik/izin/komut odaklı incelemesi tamamlandı**. Tam script yan etki analizi, gerçek 92 davranış eşdeğerliği ve kabulü **tamamlanmadı**.
- Yeni yüksek riskli izin/yazma yolları: `madsc-turk-kanal-geri-sec`, `madsc-uc-asama`, `madsc-yedek-turk-ayir`, `madsc-yedekler-sayi-duzelt`, `vod-guncelle`, `publish-iptv-png-logos`. Eski `git push` ve protected gate kodları görüldü; hiçbir yeni üretim push/cron/deploy etkinleştirilmedi.
- **Öncelikli sonraki iş:** eski `scripts/five_category_92_workflow_audit.py` içinden 92 kapsamının 99 YAML'a göre nasıl tanımlandığını kanıtla; tüm yüksek izinli scriptlerin gerçek yazma yollarını denetle; sonra K2→K3→K5 gerçek uçtan uca işlev ve K1/K4 kabul kanıtları. Son doğrulanmış Actions #194/#195 SUCCESS, bu dokümantasyon değişiklikleri için yeni test sonucu görülmedi. Korunan listeler, eski repo, main merge ve PR #71 değişmedi.


## 19 Ekim 2026 — 92/99 sayım farkı kaynak kodla ÇÖZÜLDÜ
- Eski salt-okunur `scripts/five_category_92_workflow_audit.py` içindeki `inspect()` fonksiyonu doğrudan okundu. 99 YAML'dan 5 `madsc-01`..`madsc-05` yeni kategori workflow'u ile `k1-protected-write-tests.yml`, `madsc-hizli-on-kontrol.yml` isimli 2 yeni güvenlik CI YAML'ını bilinçli hariç tutuyor. **99−7=92** eski kapsam, `len(items)!=92` fail-closed kapısıyla kontrol ediliyor. Kanıt `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` dosyasına işlendi (commit `1899c96a`). Sayım farkı çözüldü.
- Bu 92 workflow'un her biri scriptte `behavioral_parity_verified=False` ve `migration_decision=BLOCKED_NEEDS_BEHAVIOR_EVIDENCE` durumunda. **92/92 gerçek davranışsal entegrasyon tamamlanmadı**; script adı benzerliği kanıt değil. Sıradaki somut iş: yüksek riskli yazma yollarının script seviyesinde denetimi ve K2→K3→K5 gerçek uçtan uca kanıt; K1 26/26 ve K4 bağımsız restore açık. Korunan listeler, eski repo, cron, main merge, PR #71 değişmedi.


## 19 Ekim 2026 — 8 eski IBO scriptinde GERÇEK protected playlist yazma yolu doğrulandı
- Eski repo `scripts/archive_backups_354_classified.py`, `archive_backups_355_364.py`, `archive_backups_16_49.py`, `archive_backups_399_onward.py`, `apply_ibo_6115_second.py`, `apply_ibo_first_239_decisions.py`, `apply_ibo_decisions_group1.py`, `apply_ibo_second_voice.py` salt-okunur incelendi. **Sekizinde de doğrudan `CALISANLAR.m3u` `write_text` mutasyonu var**; yalnız YAML git staging sinyali değil. Ayrıca IBO arşiv M3U/CSV/JSON dosyaları üretiliyor. Kaynak satır kanıtları `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` commit `2edac2ed` içinde.
- Kullanıcı korunan YEDEKLER ve ana listeyi değiştirmeyi yasakladığı için bu eski IBO scriptleri yeni K1–K5'te **BLOCKED / salt-okunur rapor alternatifi**. `protected_write_gate.py` commit öncesi çalışsa da Python scripti çalışma ağacını daha önce değiştirebilir; bu durum otomatik izin anlamına gelmez. Gerçek geçmiş git push veya güvenlik ihlali kanıtlanmadı. Eski depo, korunan listeler, cron, main merge ve PR #71 değişmedi.
- Sıradaki: diğer yüksek izinli eski betiklerin (Türk YEDEKLER ayırma, VOD, PNG, birleşik keşif) dolaylı/direkt yazma yollarını incele; K1'de fail-closed politika, K2→K3→K5 gerçek uçtan uca ve K4 offsite kabul hâlâ açık.


## 19 Ekim 2026 — 3 ek doğrudan korunan liste yazarı, K1 gate kaynak incelemesi
- Eski salt-okunur betikler `scripts/recover_turkish_backups.py` (CALISANLAR satır 78), `scripts/keep_turkish_backups.py` (satır 68), `scripts/sync_yedekler_category_count.py` (satır 18) doğrudan `CALISANLAR.m3u` `write_text` içeriyor. Önceki 8 IBO ile birlikte **11 somut protected playlist mutasyon betiği** belgelendi; hiçbiri çalıştırılmadı veya yeni sisteme yazma davranışıyla taşınmadı.
- `tools/genis_kaynak_taramasi.py` yalnız keşif/state/summary JSON ve CSV çıktı yazımı; `verification_pipeline.py` state/summary JSON yazımı gözlendi, alt komut etkisi açık. `tools/protected_write_gate.py` tam okundu: protected exact/prefix/M3U bloklama; base..HEAD+staged+unstaged+untracked+ignored; fail-closed dönüş. Tasarım, gerçek Actions/branch protection çalışması kanıtı değil. Kanıt `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` commit `159eed10`.
- Sıradaki: `vod-guncelle` ve PNG logo publish betik/inline yazma, birleşik keşif push, K1 gate testleri ve gerçek K2→K3→K5. Korunan listeler, eski repo, cron, main merge ve PR #71 değiştirilmedi.


## 19 Ekim 2026 — EPG/PNG/VOD/birleşik keşif yayımlama yolları (önceki kayıt engeli sonrası)
- Eski YAML + Python betikleri salt-okunur incelendi; kaynak satırları `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` commit `40784625` içinde. `vod-guncelle.yml`: `vod/guncel-bolumler.json` yazımı, cron+`contents:write`+git push. `publish-iptv-png-logos.yml`: `logos/duzeltilmis-*.png` üretimi ve git push; `protected_write_gate.py` `logos/` önekini reddeder. `epg-gunluk.yml`: `epg/` XMLTV ve rapor yazımı; gate `epg/` önekini reddeder. `madsc-birlesik-kesif.yml`: ffprobe keşif, `madsc_kesif/` rapor/state, `contents:write/actions:write`, runner git reset ve 10 denemeli `git push origin HEAD:main`; `madsc_kesif/` genel protected gate öneklerinde yok. Gerçek geçmiş başarılı push veya EPG/PNG deploy iddia edilmiyor.
- Actions son liste GET ile kontrol edildi: #195, #194, #193 SUCCESS, #192 CANCELLED; bu kayıtlar yeni doküman commitlerinin regresyon koştuğunu kanıtlamaz. Eski cron/push/yayımlama yeni sisteme etkinleştirilmedi; korunan dosyalar, eski depo, main merge ve PR #71 değiştirilmedi.


## 19 Ekim 2026 — K2→K3→K5 gerçek kod seviyesinde çapraz regresyon eklendi
- `tests/test_integration.py` dosyasına 2 yeni fixture-only unittest eklendi, commit `88e196b4`: (1) iki adayda K2 discovery SHA256→K3 assess→K5 coordinate kimlik/teknik durum tutarlılığı, IBO WORKING fakat teknik başarısız adayın korunması, diğer adayda EPG/logo puanı 80 ama manuel IBO onayı olmadan hold, hiç production write olmaması; (2) K2 adayları dışında orphan probe kanıtının hem K3 hem K5'te fail-closed ValueError olması.
- Bu **gerçek kod test kapsamı artışı** fakat network ffprobe/IBO cihaz/üretim 92 davranış kabulü değildir. GitHub Actions bu commit için henüz başarıyla doğrulanmadı; çalıştırıldı veya geçti denmeyecek. Korunan listeler, eski repo, main merge ve PR #71 değiştirilmedi.


## 19 Ekim 2026 — Actions #196 doğrulanmış sonuç
- GitHub Actions koşu #196, run id `39280750923`, HEAD `88e196b4`, run API sonucu `completed/success`. K1 Güvenlik, K2 Keşif, K3 Kanal Testleri, K5 Genel Bakım, Beşli toplu kanıt doğrulama job API `completed/success`. K1 `Tüm regresyon testlerini çalıştır` adımı `success` (iki yeni K2→K3→K5 testi bu commit'te).
- K4 Arşiv ve Yedek job API hâlâ `queued/null` döndürüyor, fakat `madsc-batch-k4` artifact mevcut (551 bayt) ve beşli toplu doğrulama `success`. Bu **API tutarsızlığı** sebebiyle K4 bireysel job başarı iddiası yok. Toplam 7 artifact mevcut.
- Bunlar fixture-only ve read-only testler; gerçek ffprobe yayın ağı, IBO cihaz onayı, 92 eski workflow davranışsal parity veya offsite production restore kanıtı değildir. Korunan listeler, eski repo, main merge, PR #71 değişmedi.


## 19 Ekim 2026 — K4 regresyon ve Actions #197 doğrulaması
- `tests/test_backup.py` içine bozulmuş yedek ve bozulmuş geri yükleme için iki salt-okunur fixture regresyon testi eklendi: commit `a8dec667572c4a2358543437ce282d22046465f0`. Korunan liste/gerçek backup yazılmadı.
- GitHub Actions #197 (run `39284758370`, head `a8dec667`) `completed/success`. Altı işin tamamı `completed/success`: K1 Güvenlik (Tüm regresyon testlerini çalıştır success), K2 Keşif, K3 Kanal Testleri, K4 Arşiv ve Yedek, K5 Genel Bakım ve Beşli toplu kanıt doğrulama. K4 job ve kanıt adımı bu kez ayrı ayrı success doğrulandı.
- Yalnız fixture/salt-okunur başarıdır; offsite restore, gerçek canlı ffprobe, IBO cihaz testi ve 92/92 parity henüz kanıtlanmadı. Eski depo, korunan listeler, cron, main merge ve PR #71 değiştirilmedi.


## 19 Ekim 2026 — K3 regresyon ve Actions #198
- `tests/test_channel_test.py` içine 3 salt-okunur fixture regresyonu eklendi: ses akışı eksikse NEEDS_REVIEW, bozuk ffprobe streams fail-closed, tekrarlı ölçümlerde tek hata stable sayılmıyor. Commit `928f2297c866cff4667cf822ca8df5fad0fbe4b9`.
- GitHub Actions #198 (`39306754708`) `completed/success`; altı işin tamamı `completed/success`, K1 tüm regresyon testleri adımı `success`.
- Gerçek ffprobe ağ ölçümü, IBO cihaz testi, K4 offsite restore ve 92/92 eski davranış eşdeğerliği hâlâ kanıtlanmadı. Eski repo, korunan listeler, cron, main merge ve PR #71 değişmedi.


## 19 Ekim 2026 — IBO koruma regresyonu ve Actions #199
- `tests/test_candidate_coordination.py` içine iki fixture testi eklendi: IBO WORKING + K3 başarısız + tam metadata halinde koruma/hold; IBO WORKING + eksik probe halinde koruma/hold. Commit `00370bc07f90ae8f369d56448a83cadb6962b5e8`.
- Actions #199 (run `39307239343`) `completed/success`; altı işin tamamı `completed/success`, failed step yok.
- Yalnızca sağlanan IBO sonuçları üzerinden fixture testi; gerçek IBO cihazı kullanıcı tarafından test edilecek. YEDEKLER'e otomatik yazılmadı, korunan listeler ve eski repo değişmedi. 92 workflow parity, canlı ağ ffprobe ve offsite restore henüz kanıtlanmadı.


## 19 Ekim 2026 — Birleşik rapor regresyonu ve Actions #200
- `tests/test_legacy_unified_report.py` içine 2 fixture regresyonu eklendi: yüksek puan ve CSV 24 saat kararlı iddiası dahi IBO/kullanıcı onayı olmadan ana listeye ekleme vermez; tekrar eden kararlılık URL kaydı fail-closed reddedilir. Commit `eebec564079d00dcc6105ccafaaef113d95a7eb4`.
- GitHub Actions #200 (run `39307617098`) `completed/success`, K1–K5 ve beşli toplu doğrulama dahil 6/6 job `completed/success`, başarısız step yok.
- Bu yalnızca salt-okunur fixture davranış testi; 92 legacy workflow parity, gerçek canlı yayın ölçümü, IBO cihaz onayı ve offsite restore henüz kanıtlanmadı. Korunan listeler, eski repo, main merge ve PR #71 değişmedi.


## 19 Ekim 2026 — 24 saat kararlılık sınır testleri ve Actions #201
- `tests/test_legacy_stability.py` içine iki regresyon testi eklendi: 24 saatlik span ve son ölçüm tazelik sınırları; saat dilimi eşdeğer ölçümlerin tekilleştirilmesi ve 7 günlük pencere dışında kalan gözlemlerin sayılmaması. Commit `710df79a10c41111cee908125e0ce9129436a214`.
- GitHub Actions #201 (run `39308382200`) `completed/success`; K1–K5 ve beşli toplu doğrulama dahil 6/6 iş `completed/success`, başarısız step yok.
- Testler salt-okunur sağlanan geçmiş verileridir; canlı ffprobe, IBO cihaz doğrulaması, offsite restore ve 92 eski workflow için davranışsal eşdeğerlik kanıtlanmadı. Korunan listeler, eski depo, main merge ve PR #71 değiştirilmedi.


## 19 Ekim 2026 — K4 iç içe dosya geri yükleme denetimi ve Actions #202
- `tests/test_backup.py` içine iki salt-okunur sandbox regresyonu eklendi: üç bağımsız ağaçta iç içe dosya bozulması/kaybı yakalanır; yedek ağaçtaki iç içe sembolik bağlantı reddedilir. Commit `327fc6fad49fa9b1c13350d01df487f0e8519e4a`.
- GitHub Actions #202 (run `39308991009`) `completed/success`; K1–K5 ve beşli toplu kanıt doğrulama 6/6 `completed/success`, başarısız step yok.
- Gerçek harici depolama geri yüklemesi veya üretim restore kanıtı değildir; canlı ffprobe, IBO cihaz doğrulaması ve 92 eski workflow davranışsal eşdeğerliği hâlâ kanıtlanmadı. Korunan listeler, eski depo ve PR #71 değişmedi.


## 19 Ekim 2026 — K2→K3 çoklu aday kanıt ayrımı ve Actions #203
- `tests/test_handoff.py` içine iki fixture regresyonu eklendi: iki adayın IBO ve probe kanıtları URL SHA256 ile ayrılır, birinin WORKING sonucu diğerine taşınmaz; boş keşifte bağlantısız IBO kanıtı reddedilir. Commit `b2ee7c51ad69ce35c9a67d972f422fbeb536add4`.
- GitHub Actions #203 (run `39309574845`) `completed/success`; K1–K5 ve beşli toplu kanıt doğrulama dahil 6/6 iş `completed/success`, başarısız step yok.
- Yalnızca fixture kanıtı; gerçek IBO cihazı, canlı ffprobe, offsite restore ve 92 workflow parity kanıtlanmadı. Korunan listeler, eski depo, main merge ve PR #71 değiştirilmedi.


## 19 Ekim 2026 — 99/92 kapsam uzlaştırması belge güncellemesi
- `docs/ESKI_WORKFLOW_99_ENVANTER.md` içine güncel kapsam notu eklendi, commit `4954f1ea51d79e7dda1f1a14b85c448d65e84d1e`.
- Eski salt-okunur audit tanımı 99 YAML içinden beş `madsc-01..05` koordinatörünü ve `k1-protected-write-tests.yml`, `madsc-hizli-on-kontrol.yml` dosyalarını hariç tutuyor: 99−7=92. 99/99 ilk kaynak incelemesi tamam; 92/92 gerçek davranışsal eşdeğerlik halen `BLOCKED_NEEDS_BEHAVIOR_EVIDENCE`.
- Bu yalnızca belge uzlaştırmasıdır; yeni Actions test koşusu tetiklendiği iddia edilmiyor. Korunan listeler, eski depo, cron/push, main merge ve PR #71 değiştirilmedi.


## 19 Ekim 2026 — 92 workflow davranışsal kabul kapısı matrisi
- `docs/KABUL_KAPILARI.md` güncellendi; K1–K5 için mevcut fixture/CI kanıtları ile eksik canlı/bağımsız kanıtlar ayrıldı. Commit `1bd769962ec3f12af78cfac5cdf85d15a1ba2d28`.
- 99/99 ilk YAML incelemesi ve 99−7=92 kapsam tanımı doğrulandı; 92 davranışsal parity onayı hâlâ 0/92. Her iş için tetik/izin, script ve yazma riski, artefakt şeması, K hedefi, negatif/pozitif test, canlı/bağımsız koşu ve kullanıcı onayı zinciri olmadan `BLOCKED_NEEDS_BEHAVIOR_EVIDENCE` kaldırılmayacak.
- Yalnızca belge değişikliği; yeni CI koşusunun çalıştığı/başarılı olduğu iddia edilmez. Korunan listeler, eski depo, cron/push, main merge ve PR #71 değiştirilmedi.


## 19 Ekim 2026 — 92 eski workflow için derin betik çözümlemesi başladı
- Kullanıcı 92 eski otomasyonun gerçek görevlerini ve ilişkilerini çözme yetkisi verdi; bu genel yetki korunan üretim dosyalarını otomatik değiştirme izni olarak yorumlanmadı.
- İlk kaynak zinciri `aday-bekletme.yml`: YAML ve çağrılan 8 gerçek Python dosyası eski `Madsc55/madsc-tv@madsc/bes-sistem-toplu-birlestirme` dalında salt-okunur açıldı. Dış keşif → tekrar raporu → medya testi → `gecmis.json` aday durumu → tekrar takvimi → RETEST_LIMIT=5 → kaynak güveni → öncelik raporu haritalandı.
- Ayrıntılı girdi/çıktı ve K2/K3/K5 eşlemesi `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` içine işlendi, commit `964125e6e2a933558927080edd84a429533c8f25`. Runner koşuları arasında geçmiş kalıcılığı ve 10 artefaktın gerçek şema/sonuç parity'si kanıt bekliyor. 92/92 parity onayı hâlâ 0/92.
- Yalnız belge güncellemesi; scriptler çalıştırılmadı, korunan listeler, eski depo, cron/push, main merge ve PR #71 değiştirilmedi.


## 19 Ekim 2026 — 99 YAML derin çözümleme ikinci grup
- Eski salt-okunur dalda 12 ek workflow YAML ve 13 çağrılan Python betiği kaynak olarak açıldı. Girdi/çıktı ve K1–K5 görev eşlemesi `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` içine kaydedildi, commit `4f977d38f76f626dc0e4e6113c43722dbbf29fdd`.
- Önceki `aday-bekletme.yml` (8 betik) ile toplam 13 benzersiz YAML derin çözümleme, 21 betik kaynak incelemesi; 86 YAML aynı derinlikte henüz incelenmedi. 13 içinde `madsc-01-guvenlik.yml` 92 kapsam dışında olduğundan, 92 kapsam için bu turlarda 12 YAML derin incelendi; 80 eski kapsam YAML aynı derinlikte bekliyor. İlk YAML taraması 99/99; davranışsal parity onayı 0/92.
- Önemli farklar: `kanal-kararlilik.yml` cache restore/save, `birlesik-aday-raporu.yml` K2→K3→K5 zinciri, `madsc-birlesik-kesif.yml` git push yazma riski, `vod-guncelle.yml` contents:write ve cron, felaket kurtarma yalnız Git kaynaklı sandbox. Betikler çalıştırılmadı; korunan listeler ve eski repo değiştirilmedi.


## 19 Ekim 2026 — 99 otomasyon tam çözümleme isteği ve kritik logo yazma riski
- Kullanıcı 99 YAML'ın görev, derin betik, kaynak kodu ve 92 eski davranış eşdeğerliği incelemesinin tamamını istedi. Eski kaynak ağaç commit `ca374df3` recursive GitHub tree ile doğrulandı: 849 toplam tree girdisi, 99 YAML, 198 Python. Bu 198 dosyanın hepsinin workflow giriş noktası olduğu iddia edilmiyor.
- İlk sekiz alfabetik YAML yeniden okundu. `automatic-png-logos.yml` için 3 gerçek betik kaynak incelemesi yapıldı. `scripts/automatic_png_logos.py` `CALISANLAR.m3u` üzerine `playlist.write_text(updated)` ile koşulsuz yerel yazma ve `logos/auto/*.png` dosyalarına yazma yapabiliyor; `contents:read` bunu engellemez. Ayrıntı `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` commit `6f4b9867585d4b64ccdd9a5e394c8ddd70b11b28`.
- Bu kaynak bulgusu üretimde çalıştırma veya başarılı push kanıtı değildir. Eski depo ve korunan listeler değiştirilmedi. 99/99 ilk YAML taraması tamam, derin inceleme sürüyor, parity 0/92.


## 19 Ekim 2026 — 10 ek eski YAML / 11 Python derin çözümlemesi
- `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` içine 10 YAML'ın gerçek adım, betik, girdi/çıktı ve risk haritası eklendi; commit `bf7e514270837f988e1e2f227b750f39f2c1e63c`.
- Özellikle `iptv-test.yml` → `iptv_test.py` kaynak kodunda `CALISANLAR.m3u` doğrudan `write_text` ile yeniden yazılıyor; `CALISMAYANLAR.txt` ve `TEST_RAPORU.csv` da üretiliyor. Salt-okunur GitHub token runner üzerindeki mutasyonu engellemez. Betik yeni sistemde korunan liste üzerinde çalıştırılmayacak.
- Derin kaynak çözümleme toplamı 23/99 YAML, 32 benzersiz Python betik; 76 YAML kaldı. 92 eski kapsamda 22/92 derin incelendi; parity 0/92. Eski repo ve korunan listeler değiştirilmedi; yeni CI koşusu iddia edilmiyor.


## 19 Ekim 2026 — YENİ SOHBETE DEVİR (GÜNCEL ANA REFERANS)
- Kullanıcı açıkça 99 otomasyonun her birinin gerçek kaynak davranışını çözmeyi, YAPILACAK/YAPILMAYACAK/KANIT BEKLEYEN kararlarını saklamayı ve K1–K5 sistemini kanıtla bitirmeyi istedi. Yeni sohbetten aynı yerden devam edilecek.
- **İLK OKUNACAK DOSYA:** `docs/YENI_SOHBET_DEVIR_2026-10-19.md` (commit `6d1c8dde40d0a7020eee9f6b650ea483140ae925`). Bu dosya repo ayrımı, yasaklar, önceki CI/test commitleri, derin incelenen 23 YAML adı, 32 Python, kritik korunan liste yazma risk…357 tokens truncated…olar, arşiv, yedek, workflow ve cron değiştirilmedi.

## 22 Ekim 2026 — Beşli sistem toplu rapor üretimi ve K5 uçtan uca yerel kapısı
- Yalnız Madsc55/Madsc55-Tv/main; taban 2ea58e800156e3c99eb63f882f838045fc0714eb. Güncel diğer sohbet kodu korundu. Önceki yerel ortam kaybolduğu için yeni checkout alındı; geçmiş 707 testi güncel kodun kanıtı sayılmadı. Birleşik kaynakta ilk toplu test: 754 test, 1 failure/4 error. Eksik EXT M3U başlıklı üç test girdisi ve literal backslash-n içeren iki fixture düzeltildi. Preview testi mevcut büyük harfli ad sözleşmesiyle, virgüllü id/grup korunumu da doğrulanarak güncellendi. Üretim parser'ları gevşetilmedi.
- Mevcut offline_five_gate içine assess_report_roundtrip eklendi: gerçek core.run beş kategorinin raporlarını ayrı geçici artifact dizinlerine yazar; gerçek batch_acceptance.collect bunları K5 olarak okur; bütün dosya SHA256'ları tüketim öncesi/sonrası aynı olmalıdır. Mevcut offline_gate bu aşamayı artık zorunlu kılar; eksik/bozuk çıktı veya exception exit_code=5 ile yeşil unit test sonucunu engeller. Yeni workflow/zamanlayıcı/üretim yazıcısı yok.
- K1 korumalı rapor yazısı, K2 keşif ve geçmiş fixture'ı, K3 teknik/IBO/EPG fixture'ı, K4 izole restore ve K5 toplu tüketim aynı pakette yürütüldü. Üç yeni regresyon: gerçek beş rapor tüketimi ve byte korunumu; eksik üretici çıktısının reddi; başarılı unit testin bozuk roundtrip'i örtememesi. Geliştirme sırasında eksik dosya testinde yanlış exception beklentisi bir hata verdi; FileNotFoundError beklentisiyle düzeltildi.
- Nihai python -m madsc.offline_gate **757 test, beş izole K1–K5 kapısı, beş gerçek yerel rapor/K5 roundtrip ve 92+7/10 komut/22 görev envanteri başarılı**. git diff --check temiz. Kaynak hashleri, rapor hashleri, bütün görevlerin açık kanıt listesi ve yardımcı sözleşme farkları docs/FIVE_SYSTEM_BULK_VALIDATION_2026-10-22.json içinde.
- Tam bitmiş değildir: kurulumda 16 YAML vardır (beş ana + ekler); on yardımcı komut ana sisteme bağlıdır fakat 11 statik sözleşme farkı açık. 125 statik yazıcı çağrı adayı tümü runtime denetlendi sayılmaz. Defter 0 completed/7 in_progress/15 pending; kabul 0/92, 0/26, 0/22. Eski bağımsız aynı-input execution/artifact, canlı/zaman aralıklı K3, kullanıcının IBO cihaz testi, harici yedek/restore ve gerçek uçtan uca güvenlik kanıtları eksik. Gerçek kabul olmadan eski otomasyonları kapatma veya defteri completed yapma.
- Actions/merge/PR71/canlı probing/korunan IPTV-EPG-yedek-favori-logo-arşiv ve eski repo yazısı yapılmadı. Bu [skip ci] paketinin SHA'sı Git geçmişindedir. Sonraki iş rapordaki bağımsız dış kanıt engellerini ve 11 kaynak sözleşme farkını ana beşli sistem içinde çözmek; küçük fixture testlerini gerçek 92 davranış tamamlandı gibi sunmamak.

- Yayın sırasında diğer sohbetin yalnız docs/K1_K5_KURULUM_DURUMU_2026-10-22.md ekleyen a39cdfa commit'i geldi; içerik okundu ve korundu. Test edilen Python/test/workflow kaynakları değişmedi; dal eski HEAD üzerine zorlanmadı.


## 22 Ekim 2026 — Bu sohbetin son devri
Kullanıcı tüm ilerlemenin kaydedilip yeni sohbete geçilmesini istedi. Ayrıntılı toplu devir: SOHBET_DEVIR_2026-10-22_SON.md. Yanlış eski repo çalışması ve yeni sisteme aktarım, bütün ilgili commit/kanıt dosyaları, başarısız testler ve düzeltmeleri, 757 test+5 kapı+5 dosya/K5 doğrulaması, açık 11 sözleşme farkı ve 92/26/22 bağımsız kabul eksikleri kaydedildi. Bu devir hazırlanırken HEAD 3c228e7340b090ae4edf49d3d7b49382a4ef6d69; bu HEAD'in eklediği five_stage_installation modülü ve iki testi okundu ama çalıştırılmadı. İlk iş güncel HEAD'de bunları ve tam offline_gate'i doğrulamak. 757 testi sonraki kaynak sürümüne otomatik mal etme. Korunan veriler/eski repo/PR71/izinsiz Actions ve canlı test sınırları değişmedi; IBO testi kullanıcıda. Bu commit yalnız dokümandır, yeni test sonucu değildir.


## Eşzamanlı diğer devirle mutabakat
Devir yazılırken aeee8354c1e55f398c1f194650475d15769688bf yalnız YENI_SOHBET_DEVIR_2026-10-22.md ekledi; metin okundu ve korundu. O belgedeki 707 test bilgisi tarihsel kaldı: 1b30eee paketi 757 test+5 kapı+5 rapor/K5 ile doğrulandı, daha sonraki 3c228e7 dosyaları henüz sınanmadı. Diğer belgenin kullanıcı ekranından aktardığı K4 EPG/logo ve K5 arşiv/bakım hedefleri ile repo teknik K4 yedek/K5 bakım adlandırması arasındaki fark yeni sohbette açık görev eşlemesiyle uzlaştırılmalı; repo isimleri varsayımla değiştirilmemeli. Bu devir kaydı bütün önceki notları tamamlar.

## 22 Ekim 2026 — kurulum envanteri kapısı doğrulandı, test kimliği sağlamlaştırıldı
- Güncel main tabanı `554ec5f07a10dcf81041c1cc18a2081a04dc9e4c`; kod/test/kanıt commit'i `e4f68c0b6bf597da1ab21c5ebd8c9480d5b85991`. Eşzamanlı main değişiklikleri okundu ve korundu; force/merge yapılmadı.
- `five_stage_installation` envanterinin istisna/drift halinde aggregate offline kapıyı exit code 6 ile kapattığı odaklı testte doğrulandı. 14/14 odaklı test geçti.
- Tam regresyonda önce iki host-yükü timeout'u, sonra PID yeniden kullanımına açık `/proc/<pid>` testi gözlendi. FIFO ve workflow testleri izole yeşildi. Süreç-kapatma testi PID ile birlikte Linux starttime değerini kaydedecek biçimde düzeltildi; böylece yeni bir sürece verilmiş aynı PID yanlış “descendant yaşıyor” sonucu üretmiyor. Gerçek süreç kimliği aynı kaldığı sürece Z/X/yok olma koşulu zorunlu.
- Test-harness sınırları FIFO için 2→5 saniye, workflow gövde simülasyonu için 10→30 saniye oldu. Uygulama timeout'u, SIGKILL process-group davranışı, çıktı kapıları ve üretim güvenlik politikası değişmedi. Üç ardışık süreç testi ve iki ilgili sınır testi 5/5; nihai toplu gate 760/760 ve bütün K1–K5 offline alt kapıları başarılı.
- Kanıt dosyası `docs/FIVE_STAGE_INSTALLATION_GATE_KANIT_2026-10-22.json`; kaynak SHA256'ları, başarısız ara denemeler ve 0/92–0/26–0/22 kabul durumu içerir.
- Dış/gerçek kabul engelleri değişmedi: eski 92 için bağımsız aynı-input execution/artifact çiftleri, K2/K3 canlı/harici kanıt, IBO cihaz sonucu ve K4 harici restore gerekir. Actions/production/eski repo/merge/PR71/korunan veri işlemi yapılmadı.
- Sonraki yerel iş: kurulum raporundaki 11 statik workflow sözleşme farkını kaynak davranış gerekçeleriyle ele almak; gerçek kanıt gerektiren satırları açık blocker olarak bırakmak.


## 22 Ekim 2026 — Güncel kurulum ve operasyon sözleşmeleri topluca doğrulandı
- Tek hedef Madsc55/Madsc55-Tv/main; taban 554ec5f07a10dcf81041c1cc18a2081a04dc9e4c. Sonraki kurulum modülü/kapı değişiklikleri ilk kez bu turda gerçek yerel toplu testle kapsandı.
- İlk 760 test: 1 failure/1 error. K1 preflight alt süreç başlatması 5 saniyeyi aştı; ilgili 15 test kod gevşetilmeden 0.868 saniyede geçti. Süreç sonlandırma testi toplu koşuda tekrar başarısızdı (763 test/1 failure). Kapsayıcı getpid kimliklerinin host /proc dizininde ilgisiz sync_share.sh/sites-preview süreçlerine karşılık geldiği gerçek tanı çıktısıyla bulundu. Test artık çocukların /proc/self/stat PID ve başlangıç zamanını kullanır, iki ayrı sürecin gerçekten başladığını zorunlu doğrular; üretim süreç öldürme kodu gevşetilmedi.
- K5 25 dakika eski kaynak audit + 15 dakika not birleştirme opt-in adımlarının 10 dakika job limiti altında kalması düzeltildi: job 45, adımlar 25/15 dakika. Bu üst sınır süre tüketimi değildir; dispatch yapılmadı. Opt-in rapor upload artık failure durumunda da always() && !cancelled() ile denenir; kaynaklar/izinler/cron/korunan veri değişmedi.
- Sözleşme denetimi süreyi yalnız ilgili komutun bulunduğu job ile karşılaştırır; ilgisiz uzun job komutu maskeleyemez. Komut, süre, rapor yolu, actions izni veya failure-upload kaybı contract_gate ve mevcut offline_gate başarısını engeller. Artifact ad farkı ayrı inceleme olarak görünür; otomatik eşdeğerlik verilmez. Yeni kapı entegrasyon regresyonu dahil dört test eklendi. Önceki süre fixture'ı gerçek komutu içermediğinden düzeltildi; eksik komut süre uyumluluğu sayılmıyor.
- Nihai python -m madsc.offline_gate: 764 test, beş izole K1–K5 kapısı, kurulum envanteri, 92+7 kaynak/10 yardımcı komut/22 görev ve beş gerçek yerel raporun K5 tüketimi başarılı. git diff --check temiz. Kanıt, test edilen kaynak SHA256 ve rapor hashleri: docs/FIVE_STAGE_CONTRACT_VALIDATION_2026-10-22.json.
- 11 statik farktan iki süre farkı giderildi; dokuz artifact isim değişikliği inceleme olarak açık. Bunlar çalışma zamanı byte zinciri kabulü değildir. Davranış 0/92, runtime güvenlik 0/26, görev tam kabulü 0/22 korunur. Korunan listeler/EPG/favoriler/yedek/logo/arşiv, eski depo, PR71 ve merge işlemi yok. Actions başlatılmadı; kullanıcının ilettiği izin kotayı harcamak için gereksiz tekrar gerekçesi sayılmadı. IBO cihaz testi kullanıcıda.
- Sıradaki bağlantılı iş: dokuz yeniden adlandırılan artifact için gerçek üretici/tüketici dosya ve byte zinciri ile bağımsız aynı-input eski/yeni run/artifact kanıtını bağlamak; eksik dış kaynağı fixture ile tamamlanmış göstermemek. K2/K3 canlı ölçüm ve bağımsız geçmiş, K4 dış backup/restore, K1 26 runtime kuralı ve K5 gerçek uçtan uca kabul açık. Kod/kanıt/notlar aynı [skip ci] commitindedir; kendi SHA'sı Git geçmişindedir.

- Yayın öncesi main e4f68c0b6bf597da1ab21c5ebd8c9480d5b85991 commitine ilerledi: FIFO/receipt test süreleri ve bağımsız 760-test kanıtı okundu/korundu. Aynı process testinin starttime ve beş saniye bekleme düzeltmesi procfs PID kimliği ve iki süreç zorunluluğu ile uzlaştırıldı. Son toplu test bu birleşik kaynaklar üzerinde yeniden çalıştırıldı.


## 22 Ekim 2026 — Dokuz artifact sözleşmesi ve ana K2 geçmiş zinciri
- Tek hedef Madsc55/Madsc55-Tv/main, taban 60031b9bc46728b7773ad8037fe398b3c1d50814. Önceki test/kanıt/notlar korundu. Paket SHA Git geçmişindedir; kod/test/kanıt/devir tek [skip ci] commitinde.
- Dokuz artifact adı farkı yalnız rapordan gizlenmedi: eski yardımcıların upload-artifact adları, dosya yolları ve ZIP common-root yerleşimi ana K2/K3/K5 işlerine opt-in upload adımları olarak eklendi. Mevcut birleşik paketler korundu; yeni workflow/job/cron açılmadı, yardımcılar kapatılmadı. Paket isimleri artık contract_gate tarafından zorunlu; silinirse toplu offline kapı başarısız olur. Statik sözleşme farkı 9→0; bu çalışma zamanı eşdeğerlik kabulü değildir.
- Somut K2 kopukluğu: tüketici madsc-k2-history-source beklerken ana K2 yalnız madsc-k2-isolated-evidence üretiyordu. Ana K2 artık kaynak çiftini eski tüketicinin beklediği ad ve iki kök ZIP üyesiyle saklar. Kaynak üretimi allow_history_source_publish, bağımsız eski kaynağı doğrulama allow_verified_history ile ayrı default-false izinlerdir; kaynak üretmek için zorunlu olarak eski manifest doğrulatılmaz. Hassas komutların açık izin regresyonu bu yeni iki ayrı flag'i zorunlu denetler.
- history_verified_pipeline/CLI açık source_workflow_path/--source-workflow seçeneği alır; yalnız eski gerçek-kaynak yardımcı workflow'u veya ana K2 kabul edilir. Varsayılan eski kaynak uyumluluğunu korur. Seçim API run.path ile birebir doğrulanır; K5 fixture CI ve keyfi workflow, doğrulamadan önce reddedilir. Manifest şeması, token zorunluluğu, repo/dal/başarı/ancestor/artifact kökeni ve bayt hash denetimleri gevşetilmedi.
- Gerçek yerel zincir testi publish_source → iki dosyalı ZIP → gerçek provenance client (API fixture) → gerçek downloader/extractor → gerçek verified pipeline → mevcut-run handoff çalıştırır; kaynak/paket baytları aynı kalır. Generic paket adı, yanlış workflow ve bozuk ZIP baytı çıktı üretmeden reddedilir; izinsiz workflow ağdan önce durur. Dokuz kaynak upload sözleşmesi birebir karşılaştırılır; source artifact adı kaldırıldığında contract gate kırmızı olur. Beş yeni test eklendi.
- Odaklı ilk set 38/38 geçti. İlk toplu 769 testte 1 failure: eski opt-in testi yayın komutunu eski doğrulama flag'inde bekliyordu. Test, yeni default-false yayın flag'ini ayrıca zorunlu kılacak biçimde güncellendi. Nihai python -m madsc.offline_gate: 769 test + beş izole K1–K5 kapısı + kurulum + beş gerçek yerel rapor/K5 + 92+7 kaynak/10 komut/22 görev envanteri başarılı; contract gaps=0; git diff --check temiz. Kanıt: docs/MAIN_ARTIFACT_CHAIN_KANIT_2026-10-22.json.
- Sınırlar: API cevapları ve geçmiş girdileri fixture'dır; gerçek Actions upload/download kökeni bu tur ölçülmedi. Statik 0 fark, eski 92 otomasyonun aynı-input bağımsız runtime kabulü değildir. Tam kabul 0/92, 0/26, 0/22 kalır. Korunan kanal/EPG/favori/logo/arşiv/yedek ve eski depo değiştirilmedi; Actions, canlı probe, merge/PR71 veya IBO cihaz işlemi yok. IBO kullanıcıdadır.
- Sıradaki gerçek engeller: bağımsız eski/yeni aynı-input yürütme ve artifact çiftleri; 26 kuralın gerçek writer yollarında runtime kanıtı; K2/K3 harici geçmiş ve zaman aralıklı medya ölçümleri; kullanıcı IBO testi; K4 bağımsız harici backup/restore. Bunlar fixture veya yeni test sayısı artırılarak tamamlanmış gösterilmeyecek. İzinli gerçek koşu için kaynak girdileri/manifest ve harici kanıt sağlanmadan genel sistem bitti denmeyecek.


## 22 Ekim 2026 — Gerçek pair toplama için API ve ZIP bayt zinciri mevcut toplu CLI'ye bağlandı
- Tek hedef Madsc55/Madsc55-Tv/main; taban cffae104160b69866b2da69d8b9130d99dd5649f. Önceki dokuz artifact entegrasyonu ve statik 0 fark korundu. Bu paketin SHA'sı Git geçmişindedir; tek [skip ci] kod/test/kanıt/devir kaydıdır.
- Kalan somut kopukluk giderildi: verify_provenance_pair_api ve verify_provenance_pair_artifacts daha önce ayrı çağrılardı. Mevcut github_legacy_pair_client artık verify_provenance_pair_evidence ile altı bağımsız API kaydı, iki sınırlı ZIP indirmesi, archive SHA256, strict manifest, same-input ve snapshot bağlarını tek zincirde doğrular. Yeni standalone script/workflow/zamanlayıcı yok.
- Mevcut legacy_parity_cli --verify-github-artifacts açık opt-in seçeneğiyle sağlanan pinned kapsam pair'lerini topluca doğrular; token yalnız GITHUB_TOKEN ortamından gelir. Varsayılan mod tamamen ağsız ve eski çıktı uyumludur. Boş pair veya provenance dışı snapshot bu modda reddedilir; eksik 91/92 satır başarılı kabul edilmez. Bütün supplied pair'ler doğrulanmadan çıktı yazılmaz; raporda supplied_pairs_verified ve her pair'in API/bayt kanıtı ayrı alanlardır. Davranışsal kabul 0 kalır.
- K1 rapor hedefini artık kaynak okumadan ve ağdan önce denetler; yazmadan hemen önce tekrar denetler ve exclusive open kullanır. ZIP indirmesi repo/id/token kontrolü, 30sn timeout ve 2MiB+1 bounded read ile sınırlıdır; diske ZIP/extract yazmaz. Signed storage redirect'inde GitHub Authorization başlığı silinir, HTTPS dışı redirect reddedilir.
- Yedi yeni testte gerçek mevcut CLI/karşılaştırıcı, gerçek downloader'ın yerel HTTP fixture'ı ve gerçek ZIP parser birlikte çalışır. Altı API okuması ve iki indirme doğrulanır; yanlış workflow blob'u indirmeden, bozuk ZIP çıktıdan önce, eksik token/korunan yol ağdan önce durur. HTTP redirect/token sızıntısı, büyük paket, bool id, varsayılan ağsız mod ve boş pair negatifleri denetlenir. Odaklı 16/16; nihai python -m madsc.offline_gate 776 test ve bütün offline alt kapılar başarılı. git diff --check temiz. Kanıt docs/PAIR_API_BYTE_CHAIN_KANIT_2026-10-22.json.
- Gerçek salt-okunur GitHub sorgusu da yapıldı: yeni depoda event=workflow_dispatch toplam 9, tamamı döndü; hepsi K5, 21 Ekim sürümleridir. Son 10 genel run yalnız offline unit CI'dır; bunlar güncel runtime pair kanıtı değildir. Son K5 run39686179902 ve eski discovery run39768459333 artifact metadata örnekleri okundu; yenide Ekim22 kaynak çifti yok, eski örnek main dalında olduğundan pinned legacy karşılaştırma dalına bağlanamaz. Bu örnekler aynı-input v1 manifest çifti sağlamaz. Eski deponun bütün artifact geçmişi tarandı denmez.
- Araç sınırları kaydedildi: repo-geneli artifact ve workflow-spesifik run URL'leri connector allowlist tarafından reddedildi; desteklenen run collection + artifact-by-run araçları kullanıldı. Artifact wrapper yalnız ilk sayfayı/total_count olmadan verir; tam artifact envanteri iddiası yok. Gerçek ZIP baytları bu üretim sorgusunda indirilmedi; metadata başarıları bayt doğrulaması sayılmadı. Sorgular test/Actions çalıştırmadı.
- Kullanım hazır olduğunda: python -m madsc.legacy_parity_cli --inventory docs/LEGACY_SOURCE_SCOPE.json --snapshots actual-pairs.json --output reports/parity-api-byte-proof.json --replacement-workflow-root . --verify-github-artifacts ; reports gerçek/mevcut güvenli dizin ve actual-pairs.json bağımsız gerçek origin/manifest kaydı olmalıdır. Bu komut gerçek pair bulunmadığı için bu tur üretim ağına karşı çalıştırılmadı; fixture testi gerçek kabul sayılmaz.
- Tam kabul 0/92, 0/26, 0/22. Korunan kanal/EPG/favori/yedek/logo/arşiv, eski repo, PR71, merge, Actions dispatch, canlı probing ve cihaz testi değişmedi/yapılmadı. IBO testi kullanıcıdadır. Gerçek aynı-input pair, semantik bağımsız inceleme/yan etki, K1 gerçek writer/runtime26, K2/K3 canlı/zamanlı ölçümler ve K4 harici restore açık. Sıradaki iş gerçek v1 pair kanıtını bu mevcut birleşik CLI'ye vermek; eski raporu yeni manifest gibi yeniden etiketlememek.


## 22 Ekim 2026 — GitHub istemcilerinde ortak token/yönlendirme koruması
- Kaynak tabanı 21a9146cd09feccb19084f78965652142ea82f31; bu bölümün bulunduğu commit kod/test/kanıt paketidir.
- K1 güvenlik çapraz etkisi: K2 geçmiş artifact indirmesi, GitHub köken JSON istemcisi, K5 eski kaynak denetimi ve legacy pair ZIP indirmesi aynı HTTPS yönlendirme politikasına bağlandı. API JSON başka origin'e yönlendirilirse ikinci bağlantıdan önce reddedilir. İmzalı artifact depolama adresine geçişte Authorization kaldırılır; geri yönlendirmede geri eklenmez. HTTP ve URL kullanıcı bilgisi reddedilir. Eski 99 kaynak denetimindeki sınırsız JSON okuma da 2 MiB sınırına bağlandı. K3/K4 tüketici ve veri biçimleri değişmedi, beşli entegrasyon geçti.
- Doğrulama: 19/19 odaklı test; gerçek urllib redirect dispatch sahte HTTPS yanıtlarıyla, ağsız sınandı. Nihai python -m madsc.offline_gate: 783/783 test, beş izole kapı, kurulum envanteri, beş rapor/K5 round-trip başarılı; statik sözleşme farkı 0. Kanıt: docs/GITHUB_TRANSPORT_KANIT_2026-10-22.json; değiştirilmiş kaynak SHA256 ve tam kapı sonucu içerir. Bu pakette başarısız test yok.
- Otomatik devam görevi 6ad2b2e925bc8191a91b01728e57d707 mevcut saatlik takviminde etkin doğrulandı. Eski 605 test/eski görev öncelikleri kaldırıldı; her çalışmada güncel main/devir esas alınacak, küçük paket sonrası güvenli bağlantılı işe devam edilecek. next_run_time araçta null döndü; kesin sonraki saat veya kesintisiz çalışma iddiası yok. Yinelenen görev oluşturulmadı.
- Gerçek kabul 0/92, 0/26, 0/22 olarak kaldı. Korunan üretim verisi, eski depo, PR71, merge ve cihaz testi değişmedi. Actions veya canlı probing çalıştırılmadı.
- Sıradaki somut işler: K1-03 gerçek yazıcı çağrı yollarının kalanlarını görev defteriyle eşleştir; K4 harici geri-yükleme kanıtının mevcut tüketicilere bağlanmasındaki gerçek eksikleri incele. Gerçek v1 bağımsız aynı-input pair bulunduğunda mevcut --verify-github-artifacts CLI'yi kullan; eski metadata taramasını sebep olmadan tekrarlama. Harici/cihaz kanıtı yoksa kabul artırma.


## 22 Ekim 2026 — K4 rapor hedefi işlem öncesi kontrolü
- Başlangıç main SHA: 54b76d5dd03fe41a017fd5c7b23834ef7d0a1d18. Kod commit: 7dd644cf307eed79394cd70be4a65d2fab1fe83d [skip ci].
- madsc/restore_drill.py: isolated-report-root için beklenen yol ve K1 yerel çıktı kapısı, run_drill çağrısından önce denetlenir. Normal --output hedefi de tatbikat başlamadan kontrol edilir; yazma öncesi mevcut kontrol korunur.
- Bu oturumda offline regresyon çalıştırılmadı; değişiklik henüz testle doğrulanmış değildir. Actions dispatch yok. 783 önceki SHA'nın sonucudur, yeni commit sonucu değildir.
- Açık işler: yeni SHA'da offline_gate, K4 hatalı yolun tatbikatı başlatmadığını gösteren negatif test, K4 kanıt dosyası TOCTOU incelemesi, K1-03 gerçek writer haritası ve bağımsız harici restore kanıtı. Kabul 0/92, 0/26, 0/22.
- Korunan IPTV/EPG/playlist/favoriler/logo/yedek/arşiv, eski depo, PR #71 ve cihaz testi değiştirilmedi. Sıradaki somut adım: K4 negatif testleri ve tam offline regresyon; engel varsa açıkça kaydet.


## 22 Ekim 2026 — K4 erken red negatif testleri
- Kod 7dd644cf307eed79394cd70be4a65d2fab1fe83d üzerine tests/test_restore_drill.py negatif testleri eklendi: commit 56ca20984f043263579179ee810b04b53f0304ef [skip ci]. Yanlış izole rapor adı ve mevcut normal çıktı hedefi, run_drill çağrılmadan reddedilmelidir. Önceki tekrar-yazma beklentisi K1 ProtectedWriteRejected ile eşleştirildi.
- Bu çalışma ortamında GitHub deposu yerel kopyalanamadı (github.com DNS erişimi yok). Testler çalıştırılmadı; yeşil sonuç veya 783 yeni test iddiası yok. Actions dispatch yapılmadı. Öncelik: erişilebilir ortamda python -m unittest tests.test_restore_drill ve python -m madsc.offline_gate doğrulaması, sonra K4 tüketici yarış koşulu incelemesi.
- Korunan veri, eski depo ve cihaz testi değişmedi; gerçek kabul 0/92, 0/26, 0/22.


## 22 Ekim 2026 — K4 kanıt okuyucu sertleştirme
- madsc/k4_evidence.py commit 37f74521295d84705a702da4d4b13d696f50fcb8 [skip ci]: çıktı yolu okumadan önce denetlenir; kanıt os.open/O_NOFOLLOW (varsa), fstat ile regular/single-link, 1 MiB bounded read kullanır. Symlink parent kontrolü korunur. Test commit 80972e5badcc47173df7f4d613891b268daeade5: mevcut çıktı, symlink ve büyük kanıt negatif senaryoları.
- Kod/test GitHub'a kaydedildi; bu turda yerel test ve offline_gate çalıştırılmadı, Actions tetiklenmedi. O_NOFOLLOW olmayan platformlarda yarış koruması sınırlıdır; parent değişimi yarışına karşı tam fd-tabanlı dizin zinciri henüz yoktur.
- Öncelik: test_restore_drill ve test_k4_evidence + tüm offline_gate çalıştırıp gerçek sonuçları kaydet; K1-03 gerçek writer denetimine devam et. Gerçek kabul 0/92, 0/26, 0/22; korunan veriye dokunulmadı.


## 22 Ekim 2026 — K4 son değişikliklerin devir özeti
- K4 kanıt doğrulayıcısı: d8e5e1925c7ea9994f3e0649b4640cf5569b038a; K4 pozitif ve tekrar-yazma testi: bc21ebd0954250b65b0ae4665d40775242ecee91. Sonraki DEVAM_NOTU.md kaydı: a3f8217081562177e25a3347ac899fff6fe25353.
- Kodun yeni sürümü için regresyon henüz çalıştırılmadı. github.com DNS erişimi bu çalışma ortamında yok; Actions tetiklenmedi. Gerçek kabul 0/92, 0/26, 0/22. Öncelik K4 odaklı testler ve offline_gate doğrulaması.


## 22 Ekim 2026 — K4 JSON/üst-dizin negatif testleri
- tests/test_k4_evidence.py commit b853106868f1cc13bc2172051c22bd71641ec7a8 [skip ci]: yinelenen files_checked JSON anahtarı ve sembolik bağlantılı kanıt üst dizini reddi; başarısız doğrulamada çıktı yokluğu. Kod davranışı değişmedi.
- Yerel ortam github.com DNS çözümleyemiyor; testler/offline_gate bu yeni SHA'da çalıştırılmadı, Actions dispatch yok. Gerçek kabul 0/92, 0/26, 0/22. Öncelik erişilebilir test koşucusunda odaklı testler ve tam offline_gate; test sonucu olmadan yeşil iddia edilmez.


## 22 Ekim 2026 — K4 hardlink negatif testi
- tests/test_k4_evidence.py commit 9facdef81be2553e145465e9c65cbff889b11b2f [skip ci]: kanıt dosyasının stat.st_nlink != 1 durumunda reddi ve çıktı yokluğu kontrolü; üretim verisine dokunulmadı.
- Bu oturumda git ls-remote github.com DNS çözümleme hatası verdi. Yerel testler/offline_gate çalıştırılmadı, GitHub Actions tetiklenmedi. Test sonucu doğrulanana kadar gerçek kabul 0/92, 0/26, 0/22 olarak kalır.


## 22 Ekim 2026 — K4 O_NOFOLLOW kapısı
- madsc/k4_evidence.py b0f1d0a49966608c8e63ad291f46a9fb043c2cd4 [skip ci]: os.O_NOFOLLOW yoksa kanıt okuma fail-closed. tests/test_k4_evidence.py eadb7e40a412679c30108a0260c6ada76fa12a71 [skip ci]: bu durumu ve çıktı üretilmediğini kontrol eden test.
- Yerel git ls-remote: github.com DNS çözümlenemiyor; testler ve offline_gate yeni HEAD üzerinde çalıştırılmadı. Actions tetiklenmedi. Üst dizin TOCTOU sertleştirmesi ve gerçek kabul kanıtı açık; 0/92, 0/26, 0/22.


## 22 Ekim 2026 — K4 sahte üretim iddiası reddi
- K4 verify(): production_ready=True/1 ve category='k3' gibi sahte alanları reddetme, opsiyonel category yoksa eski run_drill raporuyla uyum; kod c189cde33a47690373eddc6c502b4e14cfb82fd6, test afe19df9646868a0153a19c4c9895c4bf90c29d1 [skip ci].
- Yerel git ls-remote denemesi github.com DNS çözümleme hatasıyla başarısız. Bu SHA için test ve offline_gate doğrulaması yapılmadı, Actions tetiklenmedi. Gerçek kabul 0/92, 0/26, 0/22; korunan veriye dokunulmadı.

## 22 Ekim 2026 — K1/K4/K5 bekleyen değişiklikler 800 testle doğrulandı
- Güncel doğrulanan kod/test/kanıt: `61bbf78214a63400083cf7d615c64a1b13547896`; taban ve korunan eşzamanlı değişiklik: `5af20718f14be617e0c20b5fee797572d7924a6e`.
- Bekleyen K4 kanıt okuyucu/yazıcı sertleştirmeleri, K5 parity çıktısı ve playlist/source-import hattı ilk kez aynı güncel kaynakta topluca çalıştırıldı. Başlangıçta 44 odaklı testte 2 failure/1 error bulundu ve birlikte giderildi.
- Düzeltmeler: hardlink fixture'ında geçerli kaynak yeniden tek-link hale getirildi; eşzamanlı main playlist backslash reddi korundu; AST writer envanteri lexical-scope flag atamalarını ve doğru `fdopen` mode argümanını çözüyor. Salt-okunur fdopen çağrıları artık sahte dinamik writer adayı değil.
- Doğrulama: 44/44 odaklı; 800/800 tam offline; beş K kapısı, kurulum, gerçek yerel beş rapor/K5 byte round-trip, statik operasyon sözleşmesi 0 gap. Kanıt `docs/K1_K4_K5_PENDING_VALIDATION_2026-10-22.json`.
- K1 writer envanteri 130 aday/20 dinamik inceleme satırı gösteriyor; manuel/runtime doğrulama tamamlanmadı. Dış kanıt gerektiren gerçek 92 pair, 26 runtime kuralı, 22 görev, canlı K2/K3, IBO ve harici K4 restore açık. Kabul 0/92, 0/26, 0/22.
- Korunan IPTV/EPG/playlist/favori/logo/yedek/arşiv, eski repo ve PR71 değişmedi; Actions/canlı probe/merge/üretim yazısı yapılmadı. Sonraki iş 20 dinamik adayın komut etkisini güvenli statik sınıflandırma ile daraltmak.


## 22 Ekim 2026 — Bu sohbetin kapsamı K2 ve K4; ortak çalışma kaydı
- Kullanıcının son talimatı: bu sohbet yalnız K2 ve K4'e odaklanacak, diğer sohbetle çakışmayacak ve biten işleri tekrarlamayacak. Kullanıcı sohbet başlığını K2 ve K4 istedi; başlık değiştirme aracı yok, fiilen değiştirildi denmedi.
- Güncel main'de diğer sohbetin restore_drill erken hedef kontrolü zaten bulundu; yeniden uygulanmadı ve dosya değiştirilmedi. K1/K5, online pilot, parser ve playlist değişiklikleri korundu. 56f64fa test tabanından e6b9e396776f04f06dd7ab55e7528e3c93c764a8 yayın tabanına gelen üç commit incelendi; bu paketin dosyalarıyla çakışmıyor.
- K4 backup_to_new_sandbox / restore_to_new_sandbox: yeni kök hedef ve tüm üst dizinler kaynak içerik okunmadan ve mkdir öncesi merkezi K1 kapısından geçiyor. Korunan EPG/FAVORILER/YEDEKLER/logo/playlist hedefleri engelleniyor. Ortak fixture_report_writer yalnız K4'ün gerekli bağımlılığı olarak düzeltildi: korunan kök altında reports dizini bile oluşturulmadan ret; mevcut son yazma kontrolü korunuyor. Aynı korumayı kullanan K3/K5 raporları da test edildi, ilgili iş akışları değiştirilmedi.
- K2 atomic_write_pair: yalnız dosya adı yerine tam hedef/üst dizin ve mevcut regular/single-link dosya kontrolü, staging öncesi ve os.replace öncesi uygulanıyor. Geçerli atomik güncelleme semantiği korunuyor. History ZIP çıkarıcısı her iki belgenin history/channels şemasını dizin veya dosya oluşturmadan doğruluyor. Geçersiz şema artık yarım çıktı bırakmıyor.
- Son K2/K4 odaklı doğrulama 87/87 başarılı. Tam kapı 56f64fa tabanında 816 test çalıştırdı: 5 failure + 3 error nedeniyle BAŞARISIZ. Beş izole K kapısı ve beş rapor/K5 round-trip geçti. 816 başarılı test olarak sunulmayacak. Kanıt ve kaynak hashleri docs/K2_K4_WRITE_PREFLIGHT_2026-10-22.json içinde.
- Diğer sohbet için mevcut toplu engeller: workflow_consolidation.consolidation_plan yeni madsc-online-pilot-gates.yml dosyasını envanter dışı görüyor; bu kök hata beş offline kapı testini de düşürüyor. tests/test_playlist_previews.py içindeki test_import_to_five_playlists_end_to_end_offline ve test_offline_cli_emits_five_drafts_without_writing_files kaynakları gerçek satır sonu yerine literal \\n kullanıyor, Invalid playlist header alıyor. Bu aktif diğer-sohbet dosyaları bu pakette değiştirilmedi. Düzeltmeleri sonrasında tam kapı yeniden gerekli.
- Önceki /tmp çalışma ortamı kayboldu; yayımlanmamış geçici K4 değişiklikleri güncel main ile karşılaştırılarak yalnız eksik kısmı yeniden oluşturuldu. İlk geçici odaklı testte eski kapı çağrı beklentisi başarısızdı; reports mkdir öncesi ret beklentisiyle güncellendi ve 87 test geçti.
- Üretim verisi, eski depo, PR71, merge, Actions dispatch ve canlı probing yapılmadı. Gerçek kabul 0/92, 0/26, 0/22; harici restore/IBO/bağımsız runtime kanıtı açık. Sıradaki K2/K4 işi: mevcut geçmiş alım ve yedek kopyalama akışlarında değişen kaynak/yarım yazma temizliği sınırlarını incele; dış depolama kanıtı olmadan harici restore kabulü verme.


## 22 Ekim 2026 — K1/K2 güvenlik ve kaynak sınırları devamı
- Güncel HEAD iş başlangıcında `e5dd11fdf90c78d00cab4e0b2aeb2490288ae78c` olarak okundu; bu oturum sırasında main eşzamanlı ilerleyebileceği için her yazım öncesi hedef dosya SHA'sı yeniden alındı.
- K2 `madsc/discovery_batch.py`: `build_m3u8_preview` toplam aday sayısı 20.000 sınırı commit `6bd8599fc6a57f57fdc086eba76d4463a58b97dd`; iki kaynaktan 20.001 adayı reddeden test `cfa27f41942866547e559e3b78a498ecf80d5d2f`. Toplam kaynak metni 8.000.000 karakter ön sınırı commit `9040b89303decb2479117eb5d5de09ecdcd90d52`; aşımı kapsayan test `0d10eaed79476fea8ee922b3b815e205bd954a7e`.
- K1 `src/madsc_guard.py`: manifestte NFKC normalize edilerek Unicode eşdeğer yol tekrarlarının reddi `d608d2b2b5b5dc8d5d1d1b286cf00dd8fb4bd1d0`; regresyon testi `6a557e8c26c49b37353f68a4673697499e6e804e`. Manifestin tek dosya tanıtıcısı üzerinden, no-follow mümkünse etkin, regular file ve 1 MiB sınırlarıyla okunması `3ca39a754d1b1fea9871dab82e88b70b0dc2634d`; geçerli dosya ve dizin girdisi testleri `09f33b05da7140f80fcbb4e1923f0d88733c47da4`.
- Bu oturumdaki tüm yeni commit mesajlarında `[skip ci]` kullanıldı; GitHub Actions dispatch, canlı kaynak probe ve üretim dosyası yazımı yapılmadı. Bu yeni commitler için yerel test çalıştırması yapılmadı; GitHub Actions/yerel suite sonucu uydurulmayacak. K1 0/26, legacy davranış kabulü 0/92, görev kabulü 0/22 olarak kalır.
- Bir sonraki iş: güncel HEAD'de K1/K2 regresyonları ve tam `python -m madsc.offline_gate` erişilebilir checkout üzerinden topluca çalıştırılmalı; K1 CLI dosya okuma testleri ve K2 büyük giriş testleri test kaynaklarında bellek tüketimi açısından değerlendirilmeli. K2/K3 canlı kaynak, K4 harici restore, IBO cihaz ve gerçek 92 eşdeğerlik kanıtları ayrı blokajdır.


## 22 Ekim 2026 — K2 çapraz-kaynak mutabakat sınırı
- Güncel HEAD bu turun başında `1a949f4edf7e87f3bb0b5a693bba7f8932403213` idi; eşzamanlı değişiklikleri korumak için her yazımda hedef dosyanın güncel SHA'sı yeniden alındı.
- `madsc/discovery_batch.py` içindeki `corroborate_sources` da çoklu feed metnini ayrıştırmadan önce toplam 8.000.000 karakterle sınırlandırıldı: `c4444956257ff5c741e402bc7624e73d6412ecac`. İki büyük kaynağın toplam limit aşımını test eden regresyon eklendi: `38668683c808159f79f1ca908173c2886f3340ec`.
- Testler bu commitlerde çalıştırılmadı; Actions tetiklenmedi. Bu değişiklik K2'nin hem önizleme hem çapraz-kaynak oylama girişlerini ortak toplam kaynak sınırı altında tutmayı hedefler. Kabul sayaçları değişmedi: 0/92, 0/26, 0/22.


## 22 Ekim 2026 — K1 bozuk manifest fail-closed davranışı
- `src/madsc_guard.py` artık UTF-8/JSON ayrıştırma hatalarını ve manifest sözleşmesi ValueError durumlarını argparse hata çıkışına dönüştürüyor; kontrolsüz traceback yerine kapalı hata sonucu: `46a6e8fd802a7dd7eaa53be3fe5a0043edb13d1d`.
- Bozuk JSON girdisinin exit code 2 ile reddedilmesini kapsayan test: `1b8e023d42b1ba0958e774f198e77fe92f809cc9`.
- Testler çalıştırılmadı; Actions dispatch yok. Sonraki adım erişilebilir checkout'ta K1/K2 odaklı testler ve tam offline_gate. Kabul sayaçları değişmedi (0/26, 0/92, 0/22).


## 22 Ekim 2026 — K1 invalid UTF-8 negatif testi
- `tests/test_guard.py` içine geçersiz UTF-8 manifestinin CLI exit code 2 ile reddedildiğini doğrulayan test eklendi: `1c328a953449ae287460dcf86f0f62b63b53a2bf`.
- Başlangıç HEAD `6b5eb355bda7dedcf9b549c9fccd565ac3fbcfd3` olarak okundu. Test değişikliği yazımdan önce dosya SHA'sı yeniden alınarak yalnız test dosyasına uygulandı.
- Bu test çalıştırılmadı; yeni SHA üzerinde test sonucu iddia edilmiyor. Actions dispatch ve üretim yazımı yok. Kabul sayaçları 0/26, 0/92, 0/22 olarak kaldı.


## 22 Ekim 2026 — Offline gate log incelemesi ve K2 test düzeltmesi
- GitHub Actions geçmişi salt okunur incelendi: run `39861302612`, commit `6b5eb355bda7dedcf9b549c9fccd565ac3fbcfd3`, sonuç failure. `madsc.offline_gate` logunda 950 test, 5 failure ve 22 error görüldü; bu koşu bizim sonraki `[skip ci]` commitlerimizden önceki SHA'da çalışmış, yeni HEAD için doğrulama sayılmaz.
- K2 regresyon testinde hata bulundu: `test_corroboration_rejects_combined_source_text_before_parsing` girdileri M3U header içermediği için kaynak boyutu kapısına ulaşmadan parser hata veriyordu. Test girdilerine geçerli `#EXTM3U` header eklendi: `fe4936a854dfcbc047be38c84579b014de79e4ab`. Bu değişiklik henüz çalıştırılmadı.
- Eski workflow logunda ayrıca 2 K5 aday metadata mesajı uyuşmazlığı, 1 K3 continuity testi, 1 parity-consumer test uyuşmazlığı, 2 playlist-preview testi ve başka 22 hata grubunun bir kısmı görünüyor. Bunlar test/checkout bazında ayrıştırılmadan K1/K2 hatası sayılmamalı; güncel main üzerinde yeniden toplu gate gerekli. Actions yeniden çalıştırılmadı.


## 22 Ekim 2026 — K2 kaynak sınırı testindeki ikinci fixture hatası düzeltildi
- Güncel HEAD bu tur başında `f00a404cf67989be993f56c738715feb6ad1e47e` idi. Önceki test düzeltmesinde başlık satırında literal `\\n` kalmış; böylece M3U parser toplam-boyut korumasına gelmeden `Missing M3U header` verebiliyordu. Test satırı mevcut dosya biçimiyle uyumlu gerçek satır sonu kaçışına çevrildi: `196c0e5a502aa5e57cb6a95b025029a85727ece8`.
- Eski Actions run `39861302612` logu: 950 test, 5 failure, 22 error; bu run `6b5eb355...` SHA'sındadır ve güncel HEAD için kabul kanıtı değildir. Başarısız log içinde ayrıca candidate probe-link metadata beklentisi ve başka sohbetlerin K3/parity/playlist testleri vardı; bu turda yalnız doğrulanmış K2 fixture kusuru değiştirildi.
- Testler çalıştırılmadı ve Actions dispatch edilmedi. Yeni testin ve güncel offline gate'in başarılı olduğu iddia edilmez. Kabul 0/26, 0/92, 0/22 olarak kalır.


## 23 Ekim 2026 — K1 platform no-follow desteği fail-closed
- K1 manifest açılışında `O_NOFOLLOW` mevcut değilse eski kod sıfır bayrağıyla dosyayı açabiliyordu. Güvenlik beklentisiyle uyumsuz bu geri dönüş kaldırıldı; özellik yoksa CLI kontrollü hata koduyla kapanıyor: `a2371ec3edce83f459a102e7c5946ceda048e8c3`.
- `O_NOFOLLOW` desteği yokmuş gibi davranan negatif CLI testi eklendi: `d8b36cad942975bfd9c1536efd869b3685c4583e`.
- Actions listesinde HEAD `30ef98459b9ee69a70b051b8a3ef59262e7a89ec` için `39861703604` run pending görünüyordu; job henüz listelenebilir değildi. Bu run, bu turdaki [skip ci] değişikliklerini kapsamaz. K1/K2 testleri bu turda çalıştırılmadı; kabul sayıları 0/26, 0/92, 0/22 olarak kaldı.


## 23 Ekim 2026 — K1 no-follow platform fail-closed ve koordineli CI takibi
- K1 manifest guard'da `O_NOFOLLOW` bulunmadığında sıfır bayrağıyla devam etme geri dönüşü kaldırıldı: `a2371ec3edce83f459a102e7c5946ceda048e8c3`; platform desteği yokken reddetme testi: `d8b36cad942975bfd9c1536efd869b3685c4583e`.
- CI'da `bd9387ab` koşusu 956 testte 1 failure + 1 error verdi: K3 loader AST testinde `ast.Module` üzerinde doğrudan iterasyon, parity consumer testinde beklenen child exit code 1 eski kaldı. Sonraki sohbet commitleri bunları düzeltti: `tests/test_candidate_probe_link.py` artık `ast.walk(parsed)` kullanıyor; `tests/test_parity_consumer_cli.py` ölçülen exit code 2'yi bekliyor. Bu dosyalar bu turda tarafımdan değiştirilmedi.
- En son görülen Actions koşuları `39861818906` (`057e3fe1`, in_progress) ve `39861826787` (`a4fbd233`, pending) idi. Bu koşuların yeni K1 `a2371ec`/test `d8b36ca` commitlerini kapsadığı garanti değil; K1/K2 testleri için ayrı başarılı kanıt bekleniyor.
- Testler bu turda yerel çalıştırılmadı; Actions dispatch yapılmadı. Kabul sayaçları 0/26, 0/92, 0/22.


## 23 Ekim 2026 — K1 Unicode normalize-before-policy düzeltmesi ve CI koordinasyonu
- Actions run `39861826787` commit `a4fbd233` tamamlandı: success. Bu başarı eski SHA'daki 956 testlik koşudaki parity exit-code uyuşmazlığının sonraki test düzeltmesini kapsıyor; K1'in bu turdaki yeni değişikliklerini kapsamaz.
- K1'de NFKC yalnızca duplicate-path kontrolüne uygulanıyor, protected-path ve `artifacts/` prefix denetimi ham metinle çalışıyordu. Böylece fullwidth Unicode karakterleriyle yazılan korunan hedefler politika kontrolünü aşabilirdi. `validate_manifest` artık önce NFKC normalize edilmiş yolları hem güvenli yol hem izinli kök kontrolünden geçiriyor: `5a02fd322789b3c4b6b94bbe4262b48d3a0e665c`.
- Korunan playlist/EPG adlarının fullwidth taklitlerini ve normalize edilmemiş artifacts kökünü reddeden test: `ba46a1d3d8044f5cd5459cbf21ed888cb3bcba9f`.
- Bu turdaki yeni K1 testleri çalıştırılmadı; Actions yeniden başlatılmadı. Güncel HEAD bu eklerden sonra ayrıca doğrulanmalı. Kabul sayaçları 0/26, 0/92, 0/22 olarak kaldı.


## 23 Ekim 2026 — K1 Unicode test sonucu ve güncel düzeltme
- GitHub Actions run `39861985074`, SHA `c40c7657`, başarısız: 958 testte 1 failure. `test_nfkc_normalization_precedes_protected_path_check` içinde `ａｒｔｉｆａｃｔｓ/report.json` için ValueError beklenmiş fakat testin çalıştığı commit'te canonical spelling reddi henüz yokmuş.
- Güncel main'de bu gerçek sorun K1 kaynak kodunda zaten giderilmiş: commit `7c2aae9d028bdebd5159a2f157141420b8cfc855` Unicode NFKC eşdeğeri olan canonical olmayan tüm yolları açıkça reddediyor. Bu nedenle full-width artifacts kökünün ham yoldan dışarı çıkma riski de kapatılıyor. Bu yeni commit için Actions sonucu henüz yok; eski failure güncel HEAD kabulü sayılmaz.
- Son Actions listesinde güncel `7c2aae9` için yeni koşu görünmüyor; bu turda Actions başlatılmadı. Kabul sayaçları 0/26, 0/92, 0/22 olarak kalır. Sıradaki adım güncel HEAD'de tam offline gate ve K1/K2 odaklı testleri doğrulamak.


## 23 Ekim 2026 — Güncel offline gate başarılı
- Actions run `39862185213`, commit `fb4a738e1be8860acc9fcd508ec580511cfeb951`, job `offline-tests` başarıyla tamamlandı. Log raporu: `tests_discovered=958`, `test_exit_code=0`, `tests_passed=true`, `five_stage_fixture_gate_passed=true`, `all_offline_gates_passed=true`, beş rapor round-trip başarılı.
- Bu sonuç önceki K1 Unicode negatif testindeki 1 başarısızlığı kapatan sonraki test/kod durumu için gerçek CI kanıtıdır. Ancak raporda açıkça `production_acceptance=false`, `runtime_security_26_acceptance=0`, `legacy_92_behavioral_acceptance=0`; dolayısıyla offline suite yeşil olsa da üretim kabulü ve 26/92 kanıtları tamamlanmış sayılmaz.
- Bu turda yeni kod değişikliği yapılmadı; son doğrulanmış kanıt, yukarıdaki run ve SHA ile sınırlıdır. Actions yeniden çalıştırılmadı.


## 23 Ekim 2026 — K1 ortak kanıt yazıcısında O_NOFOLLOW fail-closed
- İnceleme, `madsc/fixture_report_writer.py::_exclusive_bytes` için bir güvenlik boşluğu buldu: `O_NOFOLLOW` mevcut değilse eski uygulama bu bayrağı atlayıp dosyayı açıyordu. K1 manifest CLI'daki fail-closed davranışı ortak kanıt yazıcısına da uygulandı; platform desteği yoksa yazma başlamadan `PermissionError`: `0d4dda4f4f87c47376989ee70701db2a3c0a4747`.
- Negatif test, `O_NOFOLLOW` desteği yokken dosyanın oluşmadığını doğruluyor: `b4166318466967fda4d9a4543882c949f4152ce0`.
- Önceki offline CI run `39862185213` 958 testi geçirdi; fakat HEAD daha sonra yalnız belge commitleriyle ilerledi. Bu yeni kod/test commitleri için henüz test sonucu yok. GitHub Actions bu turda başlatılmadı. Kabul: runtime K1 0/26, legacy 0/92, görev 0/22.


## 23 Ekim 2026 — K1 izole kanıt kökünde symlink ancestor reddi
- `madsc/fixture_report_writer.py` içindeki iki giriş noktası (`_prepare_fixture_root` ve `write_fixture_report`) artık yalnızca son kökün değil, tüm kök yolunun gerçek nonsymlink dizinlerden oluştuğunu `resolve(strict=True) == absolute_root` koşuluyla doğruluyor. Bu, son bileşeni normal görünse bile symlink parent üzerinden izole çıktı köküne erişilmesini reddeder: `1ddf9a2e4ae5b7158b2c26fefcb8ea192bb5590b`.
- Symlink ancestor üzerinden fixture raporu oluşturmaya karşı regresyon testi eklendi; rapor dizininin oluşmadığı da kontrol ediliyor: `942cf3df4ba021ee910300562a4b9ac17245a660`.
- Bu kod/test commitleri henüz CI'da çalıştırılmadı. Önceki doğrulanmış offline gate `39862185213` 958 testte başarılıydı ama yeni commitleri kapsamaz. Actions bu turda tetiklenmedi. Kabul: runtime K1 0/26, legacy 0/92, görev 0/22.

- Doğrulama talebi: Bu commit, yukarıdaki K1 writer/root hardening değişikliklerinden sonra standart push tabanlı offline CI'nın güncel main üzerinde çalışmasını istemek için oluşturuldu. Sonuç ancak Actions run tamamlandığında kabul edilecek; bu not testin çalıştığı veya geçtiği anlamına gelmez.


## 23 Ekim 2026 — K1 bundle rollback yarış güvenliği
- `madsc/fixture_report_writer.py::write_turkish_tv_test_bundle` hata anında önceden oluşturduğu playlist yolunu koşulsuz unlink ediyordu. Bir başka işlem bu yolun dosyasını arada değiştirmişse rollback o yeni dosyayı silebilirdi. Artık oluşturulan dosyanın `st_dev/st_ino` kimliği kaydediliyor ve yalnızca aynı inode hâlâ hedefteyse temizleniyor: `2c01a1b95614654e448c2aa3927736e59a191b14`.
- İkinci yazım hata verirken playlist yolunun başka içerikle değiştirilmesini simüle eden test eklendi; rollback'in bu içeriği koruması beklenir: `3e58e5875b08ba19aac661ced8ea28ba698f8258`.
- Önceki K1 root symlink/NOFOLLOW sertleştirmeleri ve bunların testleri korunuyor. Bu yeni kod/test henüz çalıştırılmadı. Sonraki push ile offline CI sonucu izlenecek; başarı olmadan kabul sayacı artırılmayacak. Runtime K1 0/26, legacy 0/92, görev 0/22.


## 23 Ekim 2026 — Beşli sistem için güncel regresyon kapısı yeniden doğrulanacak
- Önceki offline run `39863302393`, SHA `38c2a467`: 970 testte 4 error. Log kanıtı: K4 `backup_to_new_sandbox` rollback sırasında `created_identity` tanımsızdı; K1 bundle rollback testinde inode yeniden kullanımı yüzünden eşzamanlı replacement beklenmedik biçimde silinmişti.
- K4 hatası `42b72c462681b40543c2e91db816d1657730fcf1` ile destination dizininin inode kimliği oluşturma anında kaydedilerek düzeltildi. K1 rollback, yalnız kendi oluşturduğu inode'u silme korumasına alındı (`a20a3159c1b6ab6d36d1656ddbbcaf1080401dbd`) ve testte eski inode ayrı bir tutma adına taşınarak inode reuse olasılığı kaldırıldı (`e3ee2405d9dd3bc23ca567e43c26288fcab16d28`).
- Bu değişiklikler eski başarısız koşudan sonra geldi. Son kontrol anında bunları kapsayan yeni Actions koşusu henüz yoktu. Bu not commit'i CI tetikleyecek normal push commit'i olacak; test kabulü yalnız sonuç tamamlanınca verilecek.
- Beşli sistem hedefi: K1 güvenlik kapısı, K2 bounded discovery, K3 aday/EPG/oynatma kanıtı, K4 sandbox backup/restore, K5 entegrasyon ve 22 görev defteri tek offline gate'te. Offline fixture başarısı gerçek cihaz, canlı kaynak, harici yedek ve 92 otomasyon davranışsal eşdeğerliğinin yerine geçmez. Kabul sayaçları 0/26, 0/92, 0/22.


## 23 Ekim 2026 — Son CI hatası kök neden düzeltildi, tekrar test gerekli
- Run `39863482320`, SHA `0d25b09b`, 818 testte 37 import error ve 2 failure. Kök neden `madsc/fixture_report_writer.py` rollback inode-metadata karşılaştırmasında satır sonlarının literal `\\n` olarak kaynak dosyaya yazılmasıydı; bu, modülün import edilmesini engelledi ve birçok K1-K5 testi zincirleme düştü. Ek olarak testlerin offline-gate exit-code beklentileri, gate daha erken başarısız olduğu için yanlış sonuç gösterdi.
- Güncel main'deki `031a6978ce85d32256ab7dc800c9b7e57bac6189` bu sözdizimi sorununu düzeltiyor ve eşzamanlı replacement temizliğinde inode metadata karşılaştırmasını koruyor. K4 `backup_to_new_sandbox` created identity de `42b72c4` ile eklendi. K1 rollback testi inode reuse riskini önlemek için eski inode'u ayrı tutma adına taşıyor (`e3ee240`).
- Bu son düzeltmeler [skip ci] commitleri olduğundan yeni offline run gereklidir. Aşağıdaki commit güncel main üzerinde standart offline CI tetiklemesi içindir; sonucu tamamlanmadan yeşil kabul edilmeyecek.


## 23 Ekim 2026 — Beşli offline kapı yeniden yeşil
- Güncel run `39863567977`, commit `de82210cdea1281b8ad2d1f622925fa1d8d8c397`, conclusion `success`. Job `offline-tests` başarıyla tamamlandı. Rapor: `test_exit_code=0`, `tests_passed=true`, `five_stage_fixture_gate_passed=true`, `all_offline_gates_passed=true`.
- Önceki 818 test/37 import error zincirinin kök nedeni K1 writer'daki hatalı literal satır sonu sözdizimiydi. `031a697` ile syntax onarıldı; K4 backup sandbox created-inode kimliği `42b72c4` ile kaydedildi; K1 concurrent replacement rollback koruması ve test fixture düzeltmeleri `a20a315`, `e3ee240`, `de82210` commitleriyle tamamlandı. Son koşu bu birleşik durumu kapsıyor.
- Offline beşli fixture gate'in yeşil olması gerçek üretim kabulü değildir. Raporda `production_acceptance=false`, `runtime_security_26_acceptance=0`, `legacy_92_behavioral_acceptance=0`. K1 çalışma zamanı 26 kuralı, 92 workflow davranışsal eşdeğerliği ve K3/K4 gerçek cihaz/harici depolama kanıtları açık kalır.
- Actions bağlantısı: `https://github.com/Madsc55/Madsc55-Tv/actions/runs/39863567977`.


## 23 Ekim 2026 — Devam notu: beşli kapı ve sonraki kabul işi
- Son doğrulanmış offline run: `39863567977`, SHA `de82210cdea1281b8ad2d1f622925fa1d8d8c397`; test_exit_code 0, tests_passed true, five_stage_fixture_gate_passed true, all_offline_gates_passed true. Bu, fixture/offline doğrulamasıdır; üretim kabulü değildir.
- Güncel HEAD bu not öncesinde `aec1c096c27416fe9984a765970a5f94327d3fe0`. Write-path audit hâlâ açıkça `runtime_gate_enforced=false` döndürüyor: audit ve reusable guard mevcut, fakat tüm bağımsız GitHub Actions/direct push/yazma çağrılarını küresel olarak engellediği iddia edilemez. K1-03 için tüm writer callsite envanteri ve enforcement kanıtı eksik.
- Kanıt defteri `docs/K1_K5_KANITLI_GOREV_DEFTERI.json` 22 görevi ve her birinin gerekli kanıt anahtarlarını tanımlıyor. Gerçek dış kanıt gerektiren görevler (canlı kaynak, lisans, IBO cihazı, ffprobe/ffmpeg, harici yedek, 92 workflow davranış eşdeğerliği) offline fixture ile tamamlanmış sayılmamalı.
- Bu turda kaynak kodunda doğrulanmamış büyük bir değişiklik yapmak yerine, sonraki standart push için devir/CI notu eklendi. Sonuç beklenmeden kabul sayacı artırılmayacak. Açık sayaçlar: runtime K1 0/26; legacy workflow 0/92; görev kabulü 0/22.
- Öncelik sırası: (1) tüm writer callsite envanterini üret ve her callsite'ın merkezi guard'a gerçekten bağlı olup olmadığını işaretle; (2) K1-03 için statik test ekle; (3) K2 kaynak/lisans ve artifact provenance kanıtlarını ayır; (4) K3 gerçek cihaz/canlı ölçüm, K4 harici yedek/restore; (5) K5 92 YAML'ı görev/trigger/input/output/side effect/failure/retry/artifact eşdeğerliğiyle tek tek karşılaştır.


## 23 Ekim 2026 — K1 AST yazma noktası envanteri ve CI testi düzeltmesi
- Diğer çalışma kolunda `madsc/write_callsite_audit.py` eklendi: salt okunur AST taraması Python dosyalarındaki olası dosya sistemi mutasyonlarını listeliyor; her satırı review-required olarak bırakıyor ve runtime enforcement iddiasında bulunmuyor. Scope düzeltmesi, iç fonksiyondaki guard'ın dış fonksiyonu koruyor gibi sayılmasını önlüyor.
- Actions run `39863928836`, 975 testte 1 failure verdi. Hata davranış kodunda değil, yeni testin beklenen adlarında: tarayıcı `folder.mkdir` / `folder.unlink` nitelemelerini döndürürken test `mkdir` / `unlink` bekliyordu. Beklenti, gözlenen API sözleşmesiyle hizalandı: `166eb7135d7369d27e530ae2a5ac8ac5e7950c77`.
- Bu test düzeltmesi sonrası yeni CI koşusu bekleniyor. K1 callsite taraması statik aday envanteridir; shell/subprocess ve dinamik alias'lar için ayrı denetim ve tüm adayların tek tek disposition'ı gerekir. Runtime K1 0/26, legacy 0/92, görev 0/22.


## 23 Ekim 2026 — K1 yazma noktası envanteri devamı
- K1-03 için `madsc/write_callsite_audit.py` ve `tests/test_write_callsite_audit.py` eklendi; offline gate artık Python AST yazma-callsite taramasını da raporluyor.
- İlk rapor: 97 Python dosyası tarandı, 58 mutasyon adayı bulundu. Statik guard satırı sırası yalnızca inceleme yardımıdır; global/runtime enforcement kanıtı değildir. Shell/subprocess, dinamik alias ve çapraz-fonksiyon davranışları ayrıca incelenmeli.
- `pathlib.Path.open("w")` modu ilk testte tespit edilemedi; `bcd8245` ile Path.open için ilk positional argüman modu olarak okunuyor. Güncel CI run `39864090233` sonucu bekleniyor.
- Son bilinen doğrulanmış beşli CI: run `39863567977`, 970 test başarılı. Yeni tarama testinin geçişi ve tam gate raporu ayrıca doğrulanmalı.
- Açık kabul sayaçları: K1 0/26, legacy 0/92, ana görev 0/22. Üretim verilerine dokunma ve PR #71'i birleştirmeme sınırları aynen sürüyor.


## 23 Ekim 2026 — Yeni sohbet devir noktası: K1 AST writer audit
- En son doğrulanmış offline Actions run: `39864090233`, kod SHA `bcd8245a143abb5a24fc05b244127f28876c2ce2`, conclusion success. Değişiklik: `pathlib.Path.open` çağrılarında yazma modunu ilk positional argümandan da doğru okuyacak AST tarayıcı düzeltmesi. Önceki run `39864012010` aynı envanter testinde beklenen nitelikli çağrı adları uyuşmazlığından başarısız olmuştu; sonraki düzeltmelerden sonra yeni run yeşil.
- Main'in en son HEAD'i bu devir notu öncesinde `97a74e63230f14bfdfc764bb33fd55c541bdd1c5`; bu son commit belge-only ve [skip ci]. Son yeşil run kod SHA `bcd8245` üzerindedir; doküman-only HEAD ayrıca test edilmemiştir.
- K1 yazma noktası denetimi `madsc/write_callsite_audit.py` ve `tests/test_write_callsite_audit.py` ile read-only AST aday envanteri çıkarıyor. Dinamik/shell/subprocess writer'lar ve cross-function guard sözleşmeleri statik taramayla tam kanıtlanmaz; her aday için disposition ve kalan 20 dinamik writer adayının etki sınıflandırması sürmeli. Envanter global runtime enforcement değildir.
- Son notlar: K4 yedek kopyalamada `O_NOFOLLOW` eksikliği ve source-swap regresyon testleri `02e70ee` ile eklendi; bu testlerin kapsandığı kod sonrası başarılı run'ın ayrıntı kapsamı ayrıca logdan teyit edilmelidir. Korunan üretim IPTV/EPG/favori/yedek verilerine dokunma; PR #71'i merge etme; paralel sohbetlerin değişikliklerini tekrar etme/ezme.
- Kabul durumu değişmedi: runtime security 0/26, legacy workflow behavioral equivalence 0/92, task acceptance 0/22. Five-stage offline gate success, production acceptance false. Gerçek cihaz/live-source/IBO/ffprobe/harici backup ve 92 workflow eşdeğerliği için fixture testlerini gerçek kanıt yerine sayma.
- Yeni sohbette ilk iş: run `39864090233` log/artifact raporunu ve main HEAD `97a74e6` farkını doğrula; sonra K1 writer inventory'nin tüm satırlarını/20 dinamik adayını sınıflandır, K2 bounded source/provenance kontrollerini ve K3/K4 dış kanıt açıklarını diğer sohbetlerle çakışmadan ilerlet.

## 23 Ekim 2026 — K3/K4 beşli sistem doğrulama devri
- K4 kaynak dosyası güvenli açma: 46d04cfe0f59c6a11951862190d4aba3ec0dc26a ile O_NOFOLLOW/O_DIRECTORY ve dir_fd yoksa fail-closed; e293a0d62211a8cc96a6cccc82cbb350fd19371e ile sandbox backup/restore kopyalaması descriptor-relative nofollow + fstat kontrolüne bağlandı. Testler: 02e70ee607855111ba10bdcbed61a1d4c37afa0d (eksik güvenlik desteği, kaynak symlink-swap backup/restore).
- GitHub Actions run 39864090233, SHA bcd8245a143abb5a24fc05b244127f28876c2ce2: 979 offline test, five_stage_fixture_gate ve all_offline_gates başarıyla tamamlandı. Yeni K4 commitleri bu SHA'ya dahildir. Üretim kabulü false.
- DEVAM_NOTU.md'de ayrıntılı devir kaydı ve sonuç commit fd95ffe72f1c698311a143736e975a59472b7fd9 var. K1/K2/K5 paralel sohbetlerinin commitleri korunmuştur.
- 92 legacy workflow davranışsal kanıt 0/92; 26 bağımsız runtime güvenlik kabulü 0/26; 22 görev 0/22. K3 gerçek yayın/IBO Player Pro/EPG cihaz kanıtları, K4 harici backup ve bağımsız restore kabulü hâlâ açık; canlı yayınlara ve üretim verilerine yazılmadı.


## 23 Ekim 2026 — K1-03 callsite taraması ve core guard düzeltmesi
- CI run `39864090233` SHA `bcd8245` başarıyla tamamlandı: 979 test, beşli offline fixture kapısı ve offline gate'ler başarılı; AST raporu 97 Python dosyasında 78 mutation adayı buldu. Hepsi insan incelemesi gerektiriyor; bu sayı gerçek/korumasız yazma sayısı değildir ve lexical guard analizi proof değildir.
- AST envanterinden somut bir sıra hatası bulundu: `madsc/core.py::run`, `reports/playlist.m3u8` gibi korunan hedeflerde `reports/` klasörünü K1 kontrolünden önce yaratabiliyordu. `enforce_write_paths` artık mkdir öncesi tam hedefte çağrılır ve üst dizin symlink'leri kontrol edilir. Commit `808f388`; test `fe82f2f` korunan hedefin hiçbir klasör yaratmadığını doğrular.
- Güncel run `39864306236` bu fix/test için queued; sonucu beklemeden başarılı sayma.
- Kabul sayaçları: K1 0/26, legacy 0/92, görev 0/22. Üretim verileri korunur; PR #71 merge edilmez.


## 23 Ekim 2026 — K1 guard-before-mkdir uygulaması
- Run `39864306236` SHA `fe82f2f` başarılı: 980 test, K1-K5 offline fixture gate başarılı, AST envanteri 97 dosya/78 mutasyon adayı.
- `madsc/core.py::run` için korunan hedefi `reports/` oluşturmadan önce reddetme düzeltmesi CI'dan geçti.
- Aynı kural `madsc/isolated_playlist_bundle.py::export_isolated_previews` üzerine uygulandı: destination path K1 guard'dan geçmeden output directory yaratılmıyor. Test `FAVORILER` hedefinin yaratılmadığını doğrular. Kod `1d48c0f`, test `90ba1b9`.
- CI run `39864450322` bu son değişikliği test ediyor; sonuç bekleniyor.
- Kabul sayaçları K1 0/26, eski workflow 0/92, ana görevler 0/22. Üretim verileri korunur; PR #71 merge edilmez.


## 23 Ekim 2026 — K1-03 ve K5 legacy sözleşme kaydı
- Run `39864450322` SHA `90ba1b9` başarıyla tamamlandı: 981 test, tüm offline gate'ler başarılı, AST taraması 97 Python dosyası ve 78 mutation adayı. Kod/test ağacı sonraki main commit'lerinde değişmedi; yalnızca dokümanlar eklendi.
- K1: `madsc/core.py::run` ve `madsc/isolated_playlist_bundle.py::export_isolated_previews` artık K1 path policy'yi hedef klasörünü oluşturmadan önce uygular. Regresyonlar sırasıyla protected `reports/playlist.m3u8` ve `FAVORILER` dizininin yaratılmadığını test eder.
- K5: `docs/legacy-workflow-contracts/madsc-documentation-check.json` eski workflow'un sabit SHA ve altı komutunu belgeler. Replacement mapping ve execution parity kanıtı yok; kabul sayacı 0/92 kalır.
- Başarılı offline test üretim kabulü değildir. Açık sayaçlar K1 0/26, legacy 0/92, görev 0/22; canlı üretim verilerine müdahale yok; PR #71 merge edilmedi.


## 23 Ekim 2026 — Fixture writer guard sırası
- `madsc/fixture_report_writer.py::_prepare_fixture_root` artık sidecar JSON path'ini `reports/` dizinini oluşturmadan önce K1 policy ile denetler. Kod `f5a7c08`; `FAVORILER` kökünde klasör oluşmamasını doğrulayan test `6e1916a`.
- Run `39864659684` bu test için queued; CI sonucu gelmeden kabul etme.
- Daha önce başarılı run `39864450322`: 981 test, 97 Python dosyası/78 mutasyon adayı; runtime/production kabulü değil.
- K5 kaynak sözleşmesi `docs/legacy-workflow-contracts/madsc-documentation-check.json`; eşdeğerlik hâlâ doğrulanmadı.


## 23 Ekim 2026 — K1/K5 güncel doğrulama notu
- Run `39864659684` SHA `6e1916a` başarıyla tamamlandı: 982 test, beşli fixture gate ve tüm offline gate'ler başarılı. Güncel main'de sonraki değişiklikler yalnızca doküman; kod/test ağacı aynı.
- K1-03 statik tarama: 97 Python dosyası, 78 mutation adayı. Her aday review_required; lexical guard varlığı global enforcement kanıtı değildir.
- Üç guard-before-mkdir sınırı CI ile doğrulandı: `madsc/core.py::run`, `madsc/isolated_playlist_bundle.py::export_isolated_previews`, `madsc/fixture_report_writer.py::_prepare_fixture_root`.
- K5: `docs/legacy-workflow-contracts/madsc-documentation-check.json` kaynak workflow'un tetikleyici/izin/komutlarını belgeliyor; yeni replacement ve karşılaştırmalı execution kanıtı yok.
- Açık sayaçlar: K1 0/26, eski workflow eşdeğerliği 0/92, ana görevler 0/22. CI üretim onayı değildir; canlı veriler korunuyor ve PR #71 birleştirilmedi.


## 23 Ekim 2026 — K3 XMLTV ve K4 güvenli sandbox kopyalama güncellemesi
- K3: `madsc/trial_epg_matching.py` ve `madsc/epg.py` XMLTV root/empty ID/duplicate channel ID durumlarını fail-closed işler. Kod `939267f`, `9a1ebdc`; test `f48f04f`, `420d15d`. Run `39865719002` başarılı: 982 test ve beşli offline gate başarılı. Bu cihaz/IBO kabulü değildir.
- K4: `madsc/backup.py` sandbox destination nested directories/files artık descriptor-relative, O_NOFOLLOW/O_DIRECTORY ve O_EXCL ile açılır/oluşturulur; oluşturulan root inode'u tekrar kontrol edilir. Kod `e32d522`; testler `a5590c3`, `949c239`, `a4c70f7`. Run `39865918685` SHA `949c239`: 989 test başarılı. Run `39865933101` SHA `a4c70f7`: 990 test başarılı; five-stage fixture ve all offline gates true; AST taraması 97 dosya/75 aday. `production_ready=false`.
- Run `39863892845` halen doğrulanamadı: GitHub API 404. Son erişilebilir run `39865933101`.
- Gerçek K3 HLS/ffprobe ve IBO Player Pro workflow'ları manuel dispatch gerektiriyor; bu bağlantıda dispatch aracı yok, bu yüzden çalıştırılmış gibi gösterme. Harici backup/restore da henüz kanıtlanmadı. Üretim IPTV/EPG/favori/yedeklere yazma yok.
- Kabul sayaçları aynı: 0/92 legacy, 0/26 runtime security, 0/22 ana görev. PR #71 ve eski depo değişmedi.


## 23 Ekim 2026 — HEPSI yeni sohbet devri: 990 test ve gerçek kabul eksikleri
- Kanonik kapsamlı devir: `docs/HEPSI_YENI_SOHBET_DEVIR_2026-10-23.md` (oluşturma commit `b463c13fd75fefa470cc889cc229f04633044033`). Yeni sohbette önce bu dosyanın tamamını oku.
- Son CI `39865933101`, SHA `a4c70f7277be8aad73cdd95d027115b7bcab469d`: 990 test başarılı; K1–K5 fixture ve offline gate yeşil; production_ready=false. Test SHA'sından sonra yalnız devir/dokümanlar değişti.
- 22 ana görev: 7 in_progress, 15 pending, 0 completed. Eski 92 workflow: altı batch'te 18 statik kaynak incelemesi (%19,6), 74 statik kaynak incelemesi bekliyor; davranışsal eşdeğerlik 0/92. 26 runtime güvenlik kuralı kabulü 0/26; 22 görev bağımsız kabulü 0/22. İnformal toplam proje yüzdesi gerçek kabul oranıymış gibi söylenmemeli.
- K3: duplicate/eksik XMLTV ID fail-closed kod ve testleri güncel CI'ya dahil; gerçek HLS/IBO Player Pro/EPG cihaz kanıtı eksik. K4: descriptor-relative kaynak/hedef sandbox kopyalama testleri CI'da başarılı; harici backup ve bağımsız restore kanıtı eksik.
- K1: 97 Python dosyasında 75 AST mutasyon adayı manuel tasnif bekliyor. K5 92 workflow için birebir runtime parity, yan etki, artifact, retry/timeout ve reviewer kanıtı eksik.
- Eski depoya yazma, PR #71 merge, canlı IPTV/EPG/favori/cihaz/yedek/arşiv değişikliği ve izinsiz workflow_dispatch yapılmadı. Yeni sohbette HEAD ve Actions'ı tekrar doğrula; diğer paralel sohbetleri ezme.


## 23 Ekim 2026 — K5 legacy workflow batch 07 (salt-okunur kaynak incelemesi)
- Yeni kaynak inceleme belgesi: `docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_07_2026-10-23.md`; commit `bf2db8d7e19898a91f1d3ac70baa3cc765c6e4d9`.
- Frozen `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7` üzerinde üç yeni workflow incelendi: `automatic-png-logos.yml`, `birlesik-durum-raporu.yml`, `genis-kanal-tarama.yml`. Workflow SHA'ları kaynak envanteriyle eşleşti; eski depoya yazılmadı.
- K1/K5 için kritik bulgu: `scripts/automatic_png_logos.py` korunan `CALISANLAR.m3u` dosyasını doğrudan `playlist.write_text(updated,...)` ile yazıyor. Workflow sonrasında diff görürse `git restore -- CALISANLAR.m3u` çalıştırıyor; write-then-restore, protected path'e hiç yazmama garantisi değildir. Replacement parity, izole fixture kopyası ve sıfır protected-path write ile kanıtlanmalı. Bu eski workflow çalıştırılmadı; playlist değişmedi.
- Birleşik durum workflow'u snapshot JSON'ları üretir ve sadece generated health report yazar; tarihsel snapshot'ı canlı durum gibi sunmamalı. Geniş kanal taraması 9 public M3U kaynağı ve ffprobe kullandığı için gerçek ağ/probe işidir; fixture/parity amaçlı tetiklenmedi.
- Statik inceleme toplamı 21/92; statik inceleme bekleyen 71. Bu kabul değildir: davranışsal parity 0/92, runtime güvenlik 0/26, ana görev kabulü 0/22, production_ready=false.


## 23 Ekim 2026 — K1 AST yazma envanteri düzeltmeleri
`madsc/write_callsite_audit.py` artık sabit olmayan positional/keyword dosya açma modlarını (`open(path, mode_var)`, `path.open(mode_var)`) `dynamic mode` adayı olarak sayıyor; ayrıca `subprocess.run/call/Popen/check_call/check_output`, `os.system`, `os.popen` çağrılarını harici yan etki incelemesine alıyor. İlgili regresyonlar `tests/test_write_callsite_audit.py` içine eklendi.
Kod commitleri: `c6affc2824a1c8e5288da16eff853f7bb690e1ca`, `d6f1ce5c98c85658336198b542d0a7ccb65a6394`. Test commitleri: `2a0796ebe98b03db88905534c6546153dd92020a`, `cb0a046252e1a75d119ae12e0af6c76028b3379c`.
CI sonucu bu not yazılırken doğrulanamadı; combined status endpoint'i status/check döndürmedi. Eski 990-test sonucu bu commitleri kapsamıyor. K1 26 runtime kuralı kabulü 0/26; 75 eski adayın tümü kapanmış sayılmaz. Sonraki adım: yeni SHA için erişilebilir Actions sonucu kontrolü ve adayların tek tek gerçek etkisine göre sınıflandırılması.


## 23 Ekim 2026 — K4 kanıt gereksinimleri somutlaştırıldı
K4'ün mevcut `madsc/backup.py` ve `tests/test_backup.py` / `tests/test_backup_manifest_hardening.py` kaynakları okundu. Mevcut kod; no-follow/dirfd dosya erişimi, SHA-256 + boyut manifesti, symlink/hard-link/path traversal reddi, bağımsız sandbox kopyası ve üç ayrı ağaç üzerinde restore karşılaştırması sağlar. Sonuç alanları doğru biçimde `external_storage_proven=false` ve `production_restore_verified=false` bırakır.
Yeni `docs/K4_EXTERNAL_BACKUP_RESTORE_ACCEPTANCE_2026-10-23.md` belgesi harici sağlayıcı makbuzu, gerçek run kimliği, dosya başına SHA-256/byte, bağımsız restore ağacı ve reviewer kanıtı; ayrıca arşiv/VOD ve ayın 1'i/15'i tetik eşdeğerliği gereksinimlerini tanımlar. Kanıt defterinde K4-15/16 notları güncellendi. Commitler: `41773318afc7c1849724d1397e4990959051f5b7`, `3478b770b3d5ad28b181cca8641c5425a1ecaf38`.
Bu yalnızca kabul şartlarının kaydıdır, gerçek harici yedek/restore değildir. K4-15 pending, K4-16 in_progress, K4-17 ve K4-18 pending; 92/26/22 resmî sayaçları sırasıyla 0/92, 0/26, 0/22. Genel son doğrulanmış CI 990 test / Actions 39865933101 / SHA a4c70f7277be8aad73cdd95d027115b7bcab469d; bu belge değişiklikleri için yeni CI iddiası yoktur. Üretim dosyaları değişmedi, Actions dispatch yapılmadı.


## 23 Ekim 2026 — K2 M3U metadata kimliği sertleştirmesi
main üzerinde `madsc/discovery_batch.py` içindeki EXTINF metadata ayrıştırıcısı, yinelenen alan adlarını case-insensitive karşılaştırmayla reddedecek şekilde düzeltildi (`duplicate_metadata_attribute`) ve tekil metadata alan adları casefold edilerek okunuyor. Kod commitleri `a83211a36e9ad1dd1c6047b74888970ddc33b381`, `b0ab88f2ab2043ecbd24620bd76066a0cd924b45`; test commitleri `b4b13f9de4913af05f5ddcc21e714fff8227c667`, `75d1fa756a232d4ee594bb5ae28faa01abba931b`.
Yeni regresyonlar yinelenen `tvg-id`/`TVG-ID` çakışmasının reddini ve `TVG-ID`/`GROUP-TITLE` büyük harfli alanların doğru okunmasını kapsıyor. Bu commitler için CI sonucu doğrulanmadı: toplu workflow `workflow_dispatch` ile tetikleniyor ve bu oturumda dispatch yapılmadı; combined-status sorgusu boş döndü. 990-test eski baseline yeni SHA'lar için kanıt değil.
K2 kabul sayaçları ve görev durumları değişmedi. Gerçek kaynak/lisans, günlük keşif eşdeğerliği, bağımsız artifact provenance/SHA kanıtı açık. Üretim dosyaları, eski repo ve IBO cihazı etkilenmedi. Sonraki adım: yetkili CI çalıştırması/sonucu elde edilince regresyonları doğrula; ardından K2 kaynak kökeni ve differential parity işine devam et.


## 23 Ekim 2026 — K1 kanıt yazıcısının yarış koşulu ve rollback düzeltmesi
`madsc/fixture_report_writer.py::_exclusive_bytes` artık tüm mutlak üst dizin bileşenlerini `O_DIRECTORY|O_NOFOLLOW` + descriptor-relative `openat` biçiminde açar; hedefi `O_EXCL|O_NOFOLLOW` ile açık parent fd üzerinden oluşturur. Bu, kontrol ile dosya açma arasındaki symlink-parent yarış penceresini daraltır/kapatır. Başarısız yazımda cleanup yalnız aynı açık parent fd içindeki aynı inode/metadata eşleşmesini kaldırır.
Kod commit: `967977def72e1f184c7e2920d323401f4afb035b`. Regresyon commitleri: `6d9624592a93a885fddd5aaccab2cfcc5f8f1d95`, `32fd75b48d334068efe5687b085daeb86603a0b4`.
CI sonucu henüz doğrulanmadı; eski 990-test run bu değişiklikleri kapsamaz. K1 26 kural kabulü 0/26; tüm yazma noktalarının merkezi enforcement'a bağlı olduğu kanıtlanmış değil.


## 23 Ekim 2026 — K2 birebir aynı feed içeriklerinde oy şişirmeyi engelleme
`corroborate_sources` artık kaynak gövdesinin SHA-256 fingerprint'ini kullanıyor: birebir aynı M3U metni farklı kullanıcı etiketiyle verilirse kaynak listesi raporlanır ama `source_count` yalnız bir artar. Kod `3ea2415ba29b08994c892dca2cdcfd23b42bd9e5`; test `70433a0079dff063187ce5c094cd5c70d4f828be`. Bu, yalnız birebir aynı gövdeyi yakalar; farklı biçimlenmiş kopyaların bağımsızlığını veya kaynak lisansını kanıtlamaz. CI yeni SHA için doğrulanmadı; `workflow_dispatch` bu oturumda başlatılmadı. K2 kabul durumu değiştirilmedi. Sonraki: gerçek kaynak kökeni/URL kanıtı, günlük keşif parity ve artifact SHA doğrulaması.


## 23 Ekim 2026 — K1 AST open()/os.open() sınıflandırma düzeltmesi
Tarayıcıda generic `*.open` dalı unqualified `open(path, mode)` çağrısını Path.open gibi yorumlayabiliyor ve `os.open(path, flags)` flags kontrolünü yutabiliyordu. Kod bunu düzeltti: `os.open/posix.open` önce flags ile ele alınıyor; builtins/io/unqualified open mode index 1, Path.open index 0. Keyword `flags=` da inceleniyor. Kod commitleri `ccf5bfea56c9ebbd741d28afa9ed97482c57f513`, `5138e550e9ac2cba2cd7f8eec016a7c018aad999`; regresyon commit `4eacdf0f70d7fb1bf0391a015216bde64e8516c3`. CI sonucu henüz doğrulanmadı; K1 0/26.


## 23 Ekim 2026 — K2 kaynak fingerprint biçim normalizasyonu
- `corroborate_sources` artık feed fingerprint'ini üretmeden önce UTF-8 BOM'u, CRLF/LF farkını, boş satırları ve satırların dış boşluklarını normalize eder. Aynı içeriğin yalnız aktarım biçimi değişti diye bağımsız kaynak oyu sayısı artmaz.
- Kod commitleri: `c1d29af73cbc0a08c82d93d31d8d83b8508986c9` (ilk normalizasyon), `3696f2c0221c1c571ec145b2fa2e97fdf07d9399` (kaçış düzeltmesi). Test commit: `e8eb0b34e60b612dc0d09b096dafa1e0123eaead`.
- Güncel dosya blobları yeniden okundu; canonical fingerprint kodu ve LF/CRLF+BOM regresyon testi depoda mevcut. Bu, yerel test çalıştırması veya CI başarısı değildir. CI combined status yeni test SHA'sı için boş; manuel workflow dispatch yapılmadı.
- Sınır: semantik olarak yeniden yazılmış feed kopyaları veya farklı URL'lerle yayımlanan aynı kaynak hâlâ gerçek kaynak URL/kökeni ile çözülmelidir. K2 gerçek kaynak/lisans, günlük keşif parity ve bağımsız artifact SHA kabulü açık kalır. Üretim dosyaları ve eski depo değişmedi.


## 23 Ekim 2026 — K2 semantik feed fingerprint'i
- `corroborate_sources` artık ham metin biçimi yerine parse edilmiş kanal envanterinin sıralı imzasını (normalize URL SHA-256, kanal adı, tvg-id, logo ve grup) hash'liyor. Satır sırası, yorum satırları, BOM ve CRLF/LF farkları tek başına bağımsız kaynak oyu üretemez.
- Kod commit: `28a8d963798a85db7639890cb04bec544a3314b5`; test commit: `5c6e087387b731948d98ad699bca33d8521e3cdd`. Yeni test iki kanallı, yorum/sıra/BOM/CRLF farkı olan eşdeğer feed'lerin her aday için tek kaynak sayıldığını kontrol eder.
- Doğrulama sınırı: commit `e8eb0b34e60b612dc0d09b096dafa1e0123eaead` için offline Actions başarılı oldu. Daha yeni çalıştırmalar K5'te `test_manifest_serialization_failure_cleans_partial_bundle_and_preserves_source` hatasıyla başarısız oldu (`Invalid playlist header`) ve eşzamanlı push'lar bazı test çalıştırmalarını iptal etti. En son K2 test commit'i için başarılı CI sonucu henüz yok; testler yerelde çalıştırılmış sayılmaz.
- Bu semantik fingerprint yine de kısmi kopyaları, yeniden yazılmış metadata'yı veya aynı kaynağın farklı alt kümelerini kesin olarak tanımaz. Gerçek kaynak URL/köken/lisans, günlük keşif parity ve bağımsız artifact SHA kanıtı açık. K2 kabul sayaçları değişmedi; üretim playlist/EPG/favoriler/yedekler ve eski depo değişmedi.


## 23 Ekim 2026 — K2 semantik feed fingerprint'i
- `corroborate_sources` artık ham metin biçimi yerine parse edilmiş kanal envanterinin sıralı imzasını (normalize URL SHA-256, kanal adı, tvg-id, logo ve grup) hash'liyor. Satır sırası, yorum satırları, BOM ve CRLF/LF farkları tek başına bağımsız kaynak oyu üretemez.
- Kod commit: `28a8d963798a85db7639890cb04bec544a3314b5`; test commit: `5c6e087387b731948d98ad699bca33d8521e3cdd`. Yeni test iki kanallı, yorum/sıra/BOM/CRLF farkı olan eşdeğer feed'lerin her aday için tek kaynak sayıldığını kontrol eder.
- Doğrulama sınırı: commit `e8eb0b34e60b612dc0d09b096dafa1e0123eaead` için offline Actions başarılı oldu. Daha yeni çalıştırmalar K5'te `test_manifest_serialization_failure_cleans_partial_bundle_and_preserves_source` hatasıyla başarısız oldu (`Invalid playlist header`) ve eşzamanlı push'lar bazı test çalıştırmalarını iptal etti. En son K2 test commit'i için başarılı CI sonucu henüz yok; testler yerelde çalıştırılmış sayılmaz.
- Bu semantik fingerprint yine de kısmi kopyaları, yeniden yazılmış metadata'yı veya aynı kaynağın farklı alt kümelerini kesin olarak tanımaz. Gerçek kaynak URL/köken/lisans, günlük keşif parity ve bağımsız artifact SHA kanıtı açık. K2 kabul sayaçları değişmedi; üretim playlist/EPG/favoriler/yedekler ve eski depo değişmedi.


## 2026-10-23 K5 — Batch 12 devam kaydı
- Kaynak inceleme: `docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_12_2026-10-23.md`; eski `Madsc55/madsc-tv` deposunda arşiv/yedek, merkezi K1-K5 kanıt toplayıcı ve ana liste sağlık workflow'ları salt okunur incelendi.
- Yeni bulgu: `test_ana_liste_saglik.py::test_parallel_probe_results_keep_playlist_order` çok satırlı M3U fixture'ında çift kaçışlı newline kullanıyor; yeni depoda gerçek newline ve 12 satır parse edildiği assertion'ı ile düzelt. Eski depoya yazma.
- K5 izole export/manifest regresyonu Actions run `39868459061`, SHA `a0469c34ec9a8642acffdddfbda55dadf9d39aba`, `success`. Bu offline test kapısıdır; üretim/cihaz veya eski workflow parity kabulü değildir.
- Kümülatif statik kaynak incelemesi 36/92; 56 kaldı. Davranışsal parity 0/92, runtime güvenlik 0/26, ana görevler 0/22. K5-19 defteri ve `DEVAM_NOTU.md` güncellendi.
- Korunan playlist, EPG, favoriler, logolar, yedekler ve cihaz değişmedi; eski depo salt okunur kaldı; PR #71 merge edilmedi.


## 23 Ekim 2026 — K2 kaynak bağımsızlığı açıkça doğrulanmamış olarak işaretlendi
- `corroborate_sources` çıktısına `source_independence_verified: false` ve `source_count_semantics: distinct_semantic_feed_inventories_not_verified_origins` eklendi. Farklı semantik envanter sayıları, gerçek ayrı işletmeci/kaynak kökeni kanıtı olarak yorumlanamaz.
- Kod commit `e8e686bfa0f2bf31376bcf58230bc8b5aa212a6d`; regresyon testi commit `9c1c8a594849d730f75d9c050265df74b382b8ec`. K2-08 görev defterine CI ve sınırlar işlendi (`42841d5e`).
- Son bilinen tam offline CI başarısı `39868459061` (commit `a0469c34`); 1016 testlik paket sonraki K3 devir notunda raporlandı. Yeni açık `source_independence_verified` regresyonu için workflow `39868653542` çalışıyor; bu SHA için sonuç henüz doğrulanmadı.
- K2-05 gerçek kaynak URL/işletmeci/lisans mutabakatı, K2-06 günlük keşif/tetik eşdeğerliği ve K2-07 bağımsız gerçek artifact SHA kanıtı açık. Gerçek kaynak verisi olmadan kabul kapatılmadı; üretim verisi değiştirilmedi.


## K2 CI sonuç güncellemesi — 23 Ekim 2026
- Güncelleme: `source_independence_verified` korumasını içeren kod/test commit'i `9c1c8a594849d730f75d9c050265df74b382b8ec` için GitHub Actions run `39868653542` başarıyla tamamlandı: https://github.com/Madsc55/Madsc55-Tv/actions/runs/39868653542
- Böylece bu regresyon için önceki “CI bekleniyor” notu geçersizdir. Görev defterine başarılı koşum kanıtı eklendi. Bu başarı gerçek kaynak/lisans kanıtı veya günlük tetik eşdeğerliği anlamına gelmez; K2-05/06/07 ve gerçek kaynak davranış kabulü açık kalır.


## 23 Ekim 2026 — K1 lambda guard scope düzeltmesi
`_ScopeCalls` iç içe lambda gövdelerini taramadığı halde önceden varsayılan ziyaretçi lambda içine giriyor, ertelenmiş guard çağrısını dış fonksiyonun guard listesine katabiliyordu. `visit_Lambda` dış kapsamda artık erken dönüyor; çift tanımlı visitor temizlendi. Kod: `9bf7f9926ddab13c3bebc4ca108e8d2908ef8a6b`, `bbb975e650456ae29d89d5c66dbc4ce51e7c2f6a`; test: `3c3610e35eef121b6e876eccd62c50754fd7ee6e`. Son CI sonucu henüz doğrulanmadı. K1 0/26; üretim verisine dokunulmadı.


## 2026-10-23 K5 — Batches 13–15
- Raporlar `docs/LEGACY_WORKFLOW_BEHAVIOR_REVIEW_BATCH_13_2026-10-23.md` through `...BATCH_15...`; total frozen-source static review is 45/92, 47 remaining. No legacy repo write or live workflow dispatch.
- Batch 13 found the legacy combined discovery publisher has `contents: write` and `actions: write`, can commit reports and chain-dispatch the three-stage workflow; Friday health checks are warning-only, and docs checks are literal-string smoke tests.
- Batch 14 reviewed the manual broad-source scan with write permissions and downstream dispatch, static cutover preflight, and an IBO workflow placeholder that performs no actual classification.
- Batch 15 found three backup archive scripts rewrite `CALISANLAR.m3u` in the runner workspace; the protected-write gate rejects all M3U mutations, so these pushes should fail closed. User classification is not proof of identity or playback.
- `DEVAM_NOTU.md` and `docs/K1_K5_KANITLI_GOREV_DEFTERI.json` updated. Behavioral parity remains 0/92; runtime security 0/26; main-task acceptance 0/22. Offline K5 export tests succeeded on SHA `a0469c34ec9a8642acffdddfbda55dadf9d39aba` (Actions run `39868459061`) but this is not production or legacy-parity acceptance.


## 23 Ekim 2026 — K1 yeni disk mutation callsite kapsami
`madsc/write_callsite_audit.py` icin `os.open` taninmayan flags ifadesi false negative duzeltildi (`ab8d2d28`, test `f510ba4c`). Ayrica `os.fdopen` yazma modlari ve `tempfile` dosya/dizin olusturuculari statik inceleme adaylarina alindi (`946ab465`, test `3e3cc524`). Eski 75-aday envanteri genisleyen tarayici icin guncel sayi degildir; yeni full repo scan ve tek tek kanitli siniflandirma gereklidir. Yeni SHA CI sonucu dogrulanmadi; K1 0/26, production_ready=false.


## 23 Ekim 2026 — K2 metadata ve kaynak liste sınırı sertleştirmesi
- `madsc/discovery_batch.py::corroborate_sources` `known_urls` girdisini en fazla 20.000 öğeyle sınırlar (`8d116818`). Çok büyük giriş hatayla reddedilir.
- `parse_m3u` kimlik alanları (`tvg-id`, `tvg-logo`, `group-title`) yanlış veya tırnaksız yazıldığında sessizce metadata düşürmez: `invalid_metadata_attribute` üretir ve ilişkili URL'yi aday kataloğuna almaz. Kod `a5d0d3b4`, kaçış düzeltmesi `f82e0cb9`.
- İki regresyon testi `38d8209adce32f8d2afa964a6a32ed77c35959b8` commit'inde. Bu commitin doğrudan Actions koşusu iptal edildi; ancak onun iki commit ilerideki soyundan gelen `205ad1bf6f094a36600a0ad5872f228fc74fe850` commit'i için Actions `39869009399` başarıyla tamamlandı. GitHub compare sonucu `ahead`, ahead_by=2, behind_by=0 olarak doğrulandı.
- K2-08 görev defteri yeni kanıtla güncellendi; tamamlandı statüsüne geçirilmedi. K2-05 gerçek kaynak/lisans, K2-06 günlük tetik davranışsal eşdeğerlik, K2-07 bağımsız gerçek artifact köken/SHA kanıtı hâlâ açık. Korunan üretim dosyalarına, eski depoya ve IBO cihazına dokunulmadı.


## 23 Ekim 2026 — K2 hatalı EXTINF satırı sonrası toparlanma
- `madsc/discovery_batch.py` içindeki `parse_m3u`, kanal adı bulunmayan, boş başlıklı veya metadata tırnakları dengesiz olan EXTINF satırından sonra ilişkili URL'yi tüketerek gereksiz `orphan_url` tanısını önlüyor; sonraki geçerli kanal korunuyor. Kod `aa6cba2913d5a1c5ad368a4a7c6c76d10197149a`.
- Regresyon testi `1d222cde478962ccef73ec361834660dfc1af87f`. Tam bu commit'in Actions çalıştırması `39869955026` eşzamanlı push nedeniyle `cancelled`; başarılı test sonucu olarak sayma. Daha yeni soy commitlerin CI sonucu ayrıca kontrol edilmeli.
- K2-08 görev defterinde `in_progress` kaldı. Gerçek kaynak/lisans, günlük keşif eşdeğerliği ve bağımsız artifact SHA kabulü açık; üretim playlist/EPG/favoriler/yedekler ve eski depo değiştirilmedi.


## 23 Ekim 2026 — K2 UTF-8 giriş doğrulaması; IBO cihaz testi en son
- Kullanıcı kararı: IBO Player Pro cihaz doğrulaması **en sona bırakılacak**. Gerçek cihaz denemesini kullanıcı yapıp sonucu bildirecek; o zamana kadar `ibo_device_verified=false` ve cihaz kabulü açık kalır.
- Önceki K2 `orphan_url` regresyon düzeltmesi, daha sonraki commit `21410cc6101ca5fad8b4500a74e9c955f23e9ecd` için başarılı Actions `39870201168` ile doğrulandı.
- K2 `parse_m3u`, metin veya kaynak etiketindeki Unicode surrogate karakterleri UTF-8 olarak kodlanamayacağı için girişte `ValueError` ile reddediyor (`6ac6eef780e14559854740539d96cdd8dfd39912`). `parse_m3u`, `corroborate_sources` ve `build_m3u8_preview` yolları için regresyon testi eklendi (`a794aeca142581eb5a70db90ec4ae51d5a1b63de`). Bu yeni testin CI sonucu ilk kontrolde bekliyordu (`39870351806`), başarı iddia edilmez.
- Gerçek kaynak/lisans, günlük keşif eşdeğerliği, gerçek artifact köken/SHA ve K2-08 gerçek kaynak davranış kabulü açık. Korunan üretim verisi değiştirilmedi.


## 23 Ekim 2026 — K2 kaynak etiketleri denetimi; cihaz doğrulaması ertelendi
- Önceki Unicode surrogate regresyonu (`a794aeca`) daha sonraki `0524a7d0bca2a79da83d5abd47bb136169c9a7df` commit'inde başarılı GitHub Actions `39870389256` ile kapsandı; GitHub compare `ahead=5`, `behind=0`.
- `parse_m3u` kaynak köken etiketlerindeki ASCII kontrol karakterlerini (satır sonu, tab, NUL, DEL) reddediyor (`a9e193bd2ea8de8d8f0ce0be937042dbcce894b4`). Bu, rapor ve köken kayıtlarının kontrol karakterleriyle kirletilmesini engeller. Parser, kaynak mutabakatı ve önizleme için regresyon `e03b92d13a41a3e1d48e06c73981c1e7299473e1`; yeni CI sonucu henüz doğrulanmadı.
- K2-08 görev defterine kanıt işlendi, kabul kapatılmadı. Gerçek kaynak/lisans, günlük keşif eşdeğerliği ve gerçek artifact SHA kökeni hâlâ açık. IBO Player Pro cihaz testini en sonda kullanıcı yapacak; cihaz doğrulandı iddiası yok. Korunan üretim verisine dokunulmadı.


## 23 Ekim 2026 — K2 kaynak etiketinin URL mutabakatından önce doğrulanması
- Kaynak etiketindeki kontrol karakterleri ve UTF-8 surrogate kod noktaları `corroborate_sources` girişinde bilinen URL normalizasyonundan önce reddedilir. Gereksiz çift M3U ayrıştırması kaldırıldı. Son kod `eb4b3fc841852d09ede8599de2984985f710167d`; regresyon `bd0aab8bfb24596d20f9716cb7cbefcd1ce85387`.
- Önceki kaynak etiketi regresyonunun birebir SHA `e03b92d1` Actions `39870604494` sonucu `success`. Yeni `bd0aab8b` koşusu `39870812620` eşzamanlı push nedeniyle `cancelled`; yeni regresyon için başarılı CI henüz teyit edilmedi.
- K2-08 in_progress; K2-05/06/07 gerçek kaynak/lisans, günlük keşif eşdeğerliği ve gerçek artifact köken kanıtı açık. Cihaz doğrulaması en sona bırakıldı; IBO Player Pro denemesini kullanıcı yapacak. Üretim verisine dokunulmadı.


## 23 Ekim 2026 — K2 kaynak etiketi uzunluk sınırı
- `parse_m3u`, `corroborate_sources`, `build_m3u8_preview` kaynak köken etiketlerini 256 karakterle sınırlar; 257 ve üzeri reddedilir. Kod `b79ff7a8e6855911104ee5b38388a592c64b9e7f`, sınır regresyonu `91f32d6ebd7540c1bce2fb07628db6648299261b`.
- Önceki etiket doğrulama sırası regresyonu `bd0aab8b` daha sonraki `0e2d5e6844f93f4e04970f9992018d00ad593eaf` commit'i için başarılı Actions `39870824796` ile doğrulandı (compare ahead=3, behind=0). Yeni 256 karakter sınır testinin CI sonucu ilk kontrolde bekliyordu (`39870982558`); doğrulanmadan başarılı sayma.
- K2-08 in_progress; K2-05/06/07 gerçek kaynak/lisans, günlük keşif eşdeğerliği ve artifact köken kanıtı açık. Kullanıcı IBO Player Pro cihaz testini en son kendisi yapacak. Korunan üretim dosyaları değişmedi.


## 23 Ekim 2026 — K2 aynalanmış feed kaynak oyları
- `corroborate_sources` semantik feed fingerprint'i `tvg-id` bulunan kanallarda URL SHA-256 + tvg-id kimliğini kullanır; kanal adı, logo veya grup değişimi kopya feed'e ikinci oy vermez. `tvg-id` bulunmayan kanallarda isim+grup kimliği korunur. Kod `53f5850e1678ec6e2dcf639d15a22365478f9145`; iki regresyon `3cebc66d1d48b53ce7b2f9cd86b6f8ebb6bfe5d9`.
- Önceki 256 karakter kaynak etiketi regresyonu `91f32d6e`, sonraki `41a61d61b92f0e6c043abd969caeb01100df4b1b` commit'i için başarılı Actions `39871021673` ile kapsandı (compare ahead=7, behind=0). Yeni fingerprint regresyonu Actions `39871248968` ilk kontrolde bekliyordu; sonuç doğrulanmadan kabul kapatılmayacak.
- `source_independence_verified=false`; kaynak sayısı gerçek bağımsız yayıncı/lisans kanıtı değildir. K2-05/06/07/08 açık. IBO Player Pro cihaz testini en son kullanıcı yapacak; üretim dosyalarına dokunulmadı.


## 23 Ekim 2026 — K1–K5 evidence audit dosya-kimliği bağı ve 1058 test
- `madsc/five_stage_evidence_audit.py` descriptor tabanlı, `O_NOFOLLOW|O_NONBLOCK`, regular-file, tek hardlink ve 2 MiB sınırlı okuyucuya geçirildi. Okuma öncesi/sonrası `fstat` ile pathname `lstat` dev/inode/size/mtime/ctime/nlink bağı eşleşmeden kanıt JSON'u geçerli sayılmaz. Kod `2047d2c51a489e7bace618d6ea5d9910f93e2a00`; hardlink ve okuma sırasında dosya değiştirme testleri `ef076219cb9eecc9a084d94f19c115c78c5fd53a`.
- Temiz kaynak `2c0a3ebc2d7d36572e98e68792e2bdff2f82db7d`: ilk offline_gate 180 saniye timeout oldu ve kabul edilmedi; ardından doğrudan suite 1058/1058, tekrar offline_gate 1058/1058 ve beş izole K kapısı başarılı. Kurulum, 92+7 pinned kapsam, 10 yardımcı komut, 22 görev, statik contract ve beş rapor/K5 round-trip kapıları geçti.
- K1 callsite audit 99 dosya/141 statik aday raporluyor; tümü manuel disposition bekler ve 26/26 runtime kanıtı değildir. Kabul 0/92, 0/26, 0/22. Korunan üretim verileri/eski depo/PR71/merge/canlı probe/cihaz/harici restore değiştirilmedi; Actions dispatch yapılmadı.
- Sonraki iş: 141 adayda gerçek mutasyon, string `.replace`, salt-okunur descriptor ve subprocess etkilerini kaynak-bağlı sınıflandır; gerçek writer'larda merkezi K1 dominasyon/call-chain eksiklerini kapat. Dış aynı-input bağımsız run/artifact kanıtı olmadan parity kabulü verme.


## 23 Ekim 2026 — K2 bilinen URL girdisi sınırı
- `corroborate_sources` bilinen URL kümesindeki 8192 karakterden uzun veya UTF-8 surrogate içeren adresleri normalizasyondan önce reddeder. Kod `ea305e1650a19fd592064f71d4b3cbdfd94aa670`, regresyon `a11999c7bc6888e6ba46c86803cb3154f4182300`. Normal bilinen URL dışlama davranışı da test edilir.
- Önceki aynalanmış feed fingerprint testi `3cebc66d`, sonraki `a22684d4a259ccc986c2b4baa8fcb92ecbf02b10` commit'inde başarılı Actions `39871279885` ile kapsandı (compare ahead=2, behind=0). Yeni URL sınırı testinin CI sonucu ilk kontrolde bekliyordu (`39871566283`), doğrulanmadan başarılı denemez.
- K2-05/06/07/08 açık. IBO Player Pro cihaz doğrulaması en sonda kullanıcı tarafından yapılacak; üretim playlist/EPG/favori/yedekler değiştirilmedi.


## 23 Ekim 2026 — K2 bilinen URL kontrol karakterleri
- `corroborate_sources` bilinen URL kümesinde satır sonu, tab, NUL ve DEL gibi ASCII kontrol karakterlerini normalizasyondan önce reddeder. Kod `d64a03a07fb03e6af091f2929b7655dae4f9dfed`, regresyon `096eb6038d8cd6fa3fa3f0a75260c2bfab8c631a`.
- Önceki bilinen URL uzunluk/Unicode regresyonu `a11999c7`, sonraki `c59bd4bf6f86ed0acdf3dc39aeebfbbfebc1de7f` commit'inde başarılı Actions `39871569940` ile kapsandı (compare ahead=1, behind=0). Yeni kontrol karakteri testinin Actions `39871799412` sonucu ilk kontrolde bekliyordu; doğrulanmadan kabul kapatılmaz.
- K2-05/06/07/08 açık; gerçek kaynak/lisans, günlük keşif ve artifact köken kanıtı bekliyor. IBO Player Pro cihaz testini en son kullanıcı yapacak; üretim playlist, EPG, favori, yedekler değiştirilmedi.


## 23 Ekim 2026 — K2 bilinen kanalların kaynak oyu üretmesini önleme
- `corroborate_sources` feed fingerprint'i artık yalnızca `known_urls` dışındaki yeni kanal envanterinden hesaplar. Aynı yeni kanal, farklı eski/bilinen kanalları barındıran aynalanmış feed'lerde iki bağımsız oy almaz. Kod `f4ef8312ff713d32f729075260d7635d81823f4d`, regresyon `1100410d83c5f47e5947a08fce480705463a1bee`.
- Önceki kontrol karakteri regresyonu `096eb603` tam SHA için Actions `39871799412` sonucu `success`. Yeni bilinen-kanal kaynak oyu regresyonu Actions `39872022686` ilk kontrolde `pending`, başarılı CI henüz doğrulanmadı.
- Kaynak envanteri oyları gerçek yayıncı bağımsızlığını/lisansı kanıtlamaz (`source_independence_verified=false`). K2-05/06/07/08 açık. IBO Player Pro cihaz testini en son kullanıcı yapacak; üretim playlist/EPG/favori/yedekleri değiştirilmedi.


## 23 Ekim 2026 — K2 sohbet devri / yeni sohbet için son kayıt
- Doğru depo `Madsc55/Madsc55-Tv`, dal `main`; bu sohbet K2 sorumluluğundadır. K1–K5 paralel commit atıyor; CI push iptalleri ve 409 SHA çatışmaları görülebilir. Üretim playlist, EPG, favoriler, yedekler, arşivler, eski repo/PR değiştirilmemeli.
- K2: bilinen URL uzunluk/surrogate sınırı `ea305e16`, testi `a11999c7`, başarılı descendant CI `39871569940`; bilinen URL kontrol karakteri engeli `d64a03a0`, testi `096eb603`, başarılı exact CI `39871799412`.
- K2: bilinen kanalların kaynak fingerprint oylarını şişirmesini engelleyen kod `f4ef8312ff713d32f729075260d7635d81823f4d`, regresyon `1100410d83c5f47e5947a08fce480705463a1bee`. İlk Actions `39872022686` iptal edildi; en yeni başarılı descendant CI `39872866083`, SHA `07af92ae93c579eaf9f7ce68c969791c9b4b4172` (K1 düzeltmesi `b8d59ef8` sonrasındaki 2 commit, compare ahead=2/behind=0). Başarı yalnızca bu CI kapsamı için geçerli.
- K5: 1086 testli CI'da manifest byte integrity mismatch yakalandı; `madsc/isolated_ibo_archive_export.py` tek-sefer JSON byte serialization `74779167a5cafb8a5727ce51f5e37b5241b1dabc`, test `ee9873307fe2a57a4fe70cd865b8e7b143d2cbd5`. Ardından 1089 testte K1 write callsite audit `Path.chmod` adlandırma hatası bulundu, `madsc/write_callsite_audit.py` kod `b8d59ef8742646e870c3073d3944a00b9cea23fa` ile düzeltildi. Son CI `39872866083` başarılı descendant.
- Açık K2 görevleri: K2-05 gerçek kaynak ve lisans kanıtları; K2-06 günlük keşif / eski workflow davranışsal eşdeğerliği; K2-07 geçmiş artifact SHA-256 köken kanıtları; K2-08 gerçek kaynaklarla alternatif/duplicate kabulü. Gerçek yayıncı bağımsızlığı doğrulanmadı (`source_independence_verified=false`). Hiçbirini kanıtsız kapatma.
- **IBO Player Pro cihaz doğrulaması kesinlikle en sona bırakıldı**. Kullanıcı cihazda test edip sonucu bildirecek; cihazın doğrulandığı iddia edilmeyecek.
- Yeni sohbette önce `main` son commit ve Actions sonuçlarını kontrol et, başarısızlık varsa logları inceleyip düzelt, K2 açık işleri tekrarsız sürdür; paralel ajanların commit'lerini ezme.


## 23 Ekim 2026 — K1 callsite envanteri v2 ve doğrulama
- `write_callsite_audit` kaynak dosya ve çağrı ifadesi SHA-256 bağıyla gerçek aday/non-write disposition ayrımı üretir. Yalnız açık salt-okunur `os.open` bayrak birleşimleri ve literal-string köklü `.replace` zincirleri kapatılır; değişken bayraklar ile kullanıcı tanımlı olabilecek `strip/lower/replace` zincirleri fail-closed kalır.
- Kod/kapı/test zinciri: `9bb82d897959412c550307ffdaf9c95646db2431`, `57cc1d0ed05302bc5acdb7595bb88523bfb2ffa6`, `b353f3919ef374f3a33997b5b42bc701ee7c5a1a`, receiver sertleştirmesi `60f984d`/`9078e18`, son uyarlama `0d32b48b7f15c53050f2c5c85412eebffc34c533`.
- Temiz doğrulama: 1120/1120 test ve tüm offline kapılar başarılı; 100 dosya, 142 açık aday, 5 salt-okunur descriptor + 2 literal-string non-write disposition. Bu statik sonuç 26 runtime kuralı, 92 davranış parity'si veya 22 ana görev kabulü değildir; sayaçlar 0/26, 0/92, 0/22.
- Sonraki K1 işi değişken `os.open` bayraklarının lexical sabit atamalarını kaynak-bağlı çözümlemek, sonra gerçek writer/subprocess çağrılarında guard dominasyonu/call-chain kanıtıdır. Dış bağımsız execution/artifact kanıtı ve gerçek harici restore açık; IBO cihaz testi en son kullanıcı tarafından yapılacak.

- Son HEAD doğrulama düzeltmesi: temiz `5b8d0fb515df8865047a92cdfc12cd856f7c6595` checkout'unda eşzamanlı K2/K4/K5 commitleri dahil **1123/1123** test ve tüm offline kapılar başarılı. K1 envanteri 100 dosya / 142 açık aday / 7 kaynak-bağlı non-write disposition; kabul sayaçları değişmedi.


## 23 Ekim 2026 — K1 bayrak çözümleme ve doğrudan guard baskınlığı
- Tek, doğrudan ve çağrıdan önceki yerel `os.open` flag atamaları yalnız açık salt-okunur sabitlere çözümleniyor; dinamik kapsam ve belirsiz binding'ler fail-closed. Kod/test: `8bda1064e806948158f3fa890ba39498948513d1` / `c2ada47861fcd2c06abd8c58c34dac9f252e1e3d`.
- Doğrudan koşulsuz guard deyiminin sonraki yazma adayına lexical gövde içinde baskınlığı ayrı alanlarla kaydediliyor; koşullu/try içi guard baskın sayılmıyor. Kod/test: `97ecba41f2bc89462f40dd4e88533e06b3c00ce3` / `08aa6447dae79cfacca058f534bcb0cbd912a1c4`.
- Temiz uzak main doğrulaması: 1151/1151 test ve tüm offline/K1–K5 fixture kapıları başarılı; 100 dosya, 142 aday, 9 non-write disposition, 75 yapısal baskınlık. Bu statik sonuç çağrı zinciri, 0/26 runtime, 0/92 parity veya 0/22 görev kabulünü değiştirmez.
- Sıradaki K1 işi gerçek writer/subprocess satırlarının callee/caller sözleşmesini kaynak-hash-bağlı incelemek. Gerçek bağımsız execution/artifact, harici restore ve kullanıcı cihaz kanıtı gelmeden kabul verilmez; korunan üretim verisi değiştirilmedi.


## 23 Ekim 2026 — K1 artifact yazıcısı ve subprocess kanıt sınırı
- `artifact_transport` yazmaları koşulsuz iki K1 preflight'ı olan tek exclusive yardımcıya taşındı: `1d347f79173870b2313b6ec9ce9ed466569418ae`; regresyonlar `6aee0d5a70a72ac19fa0087fb08821700d7435da` ve `6cf0c3932bf521dbafff18787cec4ba034a2465b`.
- Subprocess adayları için shell/argv sözdizimi kaynak-bağlı kaydediliyor (`039826136d99fa9bf4a7d44b6b7661d1566209da`, `ff946c3b35f2efde1972dac64f09663e2d98e14e`). Altı aday shell-disabled görünse de komut etkisi 0/6 doğrulandı; tümü açık/fail-closed kaldı.
- Temiz son kod SHA'sında 1154/1154 test ve bütün offline K1–K5 kapıları başarılı; 140 aday, 9 disposition, 77 yapısal guard baskınlığı. İlk hedefli testteki yanlış exception beklentisi başarı sayılmadan düzeltildi.
- Kabul değişmedi: 0/92, 0/26, 0/22. Sıradaki iş gerçek subprocess etkileri ve writer caller/callee sözleşmeleri; dış kanıt ve en son kullanıcı cihaz testi bekleniyor.


## 23 Ekim 2026 — K1 subprocess argv ve doğrudan yerel çağıran bağı
- Güvenli tek-atamalı yerel subprocess argv çözümlemesi `5b79da4e60e89c098bf5416e2162ab53f5648467`, regresyonu `d1707ae589d56a36a600bf4a47ef84bcce28cc93`. Altı executable'ın beşi tanındı; gerçek komut etkisi 0/6 doğrulandı ve hiçbir aday kapatılmadı.
- Writer helper doğrudan çağıranları ve çağrı-noktası guard baskınlığı `1bc73b2abd6b0f9dc20d3d4636e0f7e6cd23dfdd`, fail-closed testleri `c16f25d230b411ac100411a113a125b0b8f6b3fa`. 104/140 adayda yerel çağıran, 16/140 adayda guarded çağıran var; tüm çağıranların kapandığı kanıt 0.
- Temiz son kod SHA'sında 1157/1157 test ve bütün offline K1–K5 kapıları başarılı. İlk argv testi gerçek bir çıkarım hatası yakaladı ve düzeltildikten sonra tam paket yeniden geçti.
- Kabul 0/92, 0/26, 0/22. Sonraki iş kısmi guarded çağıranların gerçek giriş yolları ile altı subprocess etkisini incelemek; statik kayıtları runtime/production kanıtı saymamak.


## 23 Ekim 2026 — K1 artifact transport TOCTOU kapısı
- `artifact_transport` K1 preflight ile gerçek create arasında `Path.open` kullanmıyor; ortak descriptor-relative `O_NOFOLLOW|O_EXCL` yazıcıya bağlı. Kod zinciri `ce830b31d3fde66ebd63c853de54c4268a304ebd` + `083ef2dd1e98d3ff8ccfbc708391d73365ac09d1`, yarış/audit testleri `40c58fbbb6ea4c7a14ed76b0e4f154b726f538bf` + `f8c32a3a2bdf278ac627571e4118dd5bc07821e7`.
- Temiz son `main` checkout'unda 83 hedefli ve 1190 tam offline test, beş izole kapı ve write-callsite audit başarılı. Parent dizini preflight sonrasında symlink ile değiştirilse bile dış hedefte dosya oluşmadı.
- Kabul sayaçları değişmedi: 0/92 parity, 0/26 runtime, 0/22 ana görev; fixture/statik testler production kanıtı değildir. Sıradaki K1 paketi kısmi guarded caller kapanışı ve altı subprocess gerçek etkisinin kaynak-bağlı/fail-closed disposition'ıdır. Gerçek bağımsız artifact/run, harici restore ve en son kullanıcı cihaz testi dış kanıt bekler.


## 23 Ekim 2026 — K1 subprocess stdio izolasyonu
- Altı subprocess çağrısının altısında stdin kapatıldı ve stdout/stderr capture/pipe sözleşmesi kaynak-bağlı audit alanlarıyla doğrulandı. Kod commitleri `869a5405056dc6c86c6fcf4b1055e7efab8987ef`, `509ae57ed135106a6988f12d68422c9215c74102`, `7c639daed7a0210c760e42c03172bd60c097295f`, `3dea21b0b6a44decca1f4020c248c053bd1a8c86`, `818d67a8b12a989667fd6271aa0d79397aca32ae`; test `fbb4b6a23ff044803723999eb98b6e396b21abe0`.
- Temiz uzak checkout: 95 hedefli ve 1220 tam offline test, beş izole K kapısı ve audit başarılı. `process_stdio_bounded_verified=6/6`; gerçek dış-komut read-only etki kanıtı `0/6`, dolayısıyla adaylar kapanmadı ve runtime kabulü verilmedi.
- Kabul 0/92, 0/26, 0/22. Sıradaki iş argv/cwd/env ve çıktı argümanlarının kaynak-hash-bağlı etki sınıflandırmasıdır; arbitrary parity komutu fail-closed kalır. Canlı EPG/cihaz, bağımsız artifact/run ve harici restore dış kanıt bekler.


## 23 Ekim 2026 — K1 subprocess etki sınıfları
- Güncel başlangıç `main` SHA `ae3778f0746def5635f9ad5fa55c7f8c00a37057`. Subprocess audit kodu `691a95b1a73da526325fe0d906491e6c117eac8d`, regresyonu `adf72bd893c97b7185ad6a4f1a5b2f259079587c`.
- Altı çağrı argv/dinamik argüman, literal seçenek, gerçek `curl` dosya çıktı seçeneği, cwd/env kökeni ve komut sınıfıyla kaynak-bağlı kaydedildi: 2 network client, 1 media inspector, 1 Python inline, 1 Python module, 1 caller-controlled. Hepsi fail-closed; `process_effect_verified_read_only=0/6`.
- Sonradan gelen K3 commitleri korunarak güncel uzak `dc354863e8a70a555a744dbd42e19f09fd6e31a0` içeriğinde 109 hedefli ve 1275 tam offline test başarılı; başarısız test yok. Beş izole kapı ve pinned 92 envanteri geçti fakat kabul 0/92, 0/26, 0/22 olarak kaldı. Bir yanlış blob SHA yazması 409 ile durdu ve güncel blobla güvenle tekrarlandı; başka commit ezilmedi. Actions/canlı probe/üretim veya korunan veri yazması yapılmadı.
- Sıradaki yerel K1 işi, kısmi guard'lı helper girişlerini okuma/yazma etkisine göre kaynak-hash-bağlı ayırmak ve caller closure kanıtı olmadan disposition vermemek. Gerçek bağımsız execution/artifact, harici restore ve en son kullanıcı cihaz kanıtı dış engel olarak açık.
