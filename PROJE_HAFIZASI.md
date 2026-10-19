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
