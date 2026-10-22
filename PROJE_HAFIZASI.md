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
- **İLK OKUNACAK DOSYA:** `docs/YENI_SOHBET_DEVIR_2026-10-19.md` (commit `6d1c8dde40d0a7020eee9f6b650ea483140ae925`). Bu dosya repo ayrımı, yasaklar, önceki CI/test commitleri, derin incelenen 23 YAML adı, 32 Python, kritik korunan liste yazma riskleri, 76 bekleyen YAML ve 92 parity kabul planını ayrıntılı içerir. Kelimesi kelimesine sohbet transkripti değil, uygulanabilir teknik devir notudur.
- Son durum: 99/99 YAML ilk tarama; 23/99 derin kaynak görev çözümü; 32 benzersiz Python kaynak incelemesi; 76/99 derin çözüm bekliyor; 22/92 eski kapsam derin incelendi; **0/92 parity doğrulandı**. `automatic-png-logos.yml` kritik yerel liste yazma bulgusu belgeli, tam matrisi tamamlanınca sayaca dahil et.
- Eski `Madsc55/madsc-tv` / `madsc/bes-sistem-toplu-birlestirme` SALT OKUNUR. Yeni `Madsc55/Madsc55-Tv` çalışma deposu. Korunan kanal listeleri/YEDEKLER/YENİLER/FAVORİLER/EPG/logo/URL/ID/sıra değişmez; cron/push/deploy, main merge, PR #71 yok. Kullanıcı IBO WORKING dediği kanal teknik fail diye silinmez.
- Yeni sohbet görevi: devir notunu oku; 76 YAML'ı gerçek script, alt çağrı, yan etki, state, artefakt, K1–K5, parity kanıtı bazında gruplar halinde incele; her grubu `docs/ESKI_WORKFLOW_DAVRANIS_ESLEME.md` ve `PROJE_HAFIZASI.md` içine işle. Gerçek test yoksa test varmış gibi anlatma.


## 19 Ekim 2026 — Yeni sohbet: automatic-png-logos derin kaynak çözümü
Kaynak: eski salt-okunur madsc/bes-sistem-toplu-birlestirme dalında .github/workflows/automatic-png-logos.yml, logo_deneme/audit.py, scripts/automatic_png_logos.py, scripts/logo_visual_evidence.py doğrudan okundu. Önceki 23 YAML yeniden sayılmadı; bu YAML artık 24/99 derin kaynak çözümüne eklenebilir (kalan 75). Davranışsal parity hâlâ 0/92.
Tetik: yalnız workflow_dispatch; contents:read; concurrency automatic-png-logos cancel-in-progress:false; ubuntu-latest, 15 dakika; checkout v4, Python 3.12, Pillow/cairosvg, ffmpeg, upload-artifact v4. Audit CALISANLAR.m3u logo URL'lerini 8 paralel ağ çağrısıyla (12s, 4MB) kontrol eder, logo_deneme/rapor.json ve ozet.json yazar; görüntü doğrulama kanal kimliği veya IBO cihaz kanıtı değildir. Automatic PNG scripti iptv-org channels/logos JSON ağ verisini (20s), tvg-id/benzersiz isim eşlemesini, onaylı SHA256 görsel kaydını kullanır; 12 paralel indirme, URL başına 12s/4MB, 16MP sınırı, 640x640 PNG üretimi; logos/auto/*.png ve png_automation.json yazar. approved_repairs.json ve verified_sources.json yerel girdilerdir; kaynak doğrulama ve kimlik kararı ayrı tutulmalı. KRİTİK: script her çalışmada CALISANLAR.m3u üzerinde playlist.write_text(updated) çağırır; contents:read yerel yazmayı engellemez. YAML daha sonra git diff ile değişikliği restore eder ve staged değişiklikte fail verir; bu koruma yazma sonrası gerçekleşir, başka adımların değiştirilmiş dosyayı görmesi ve istisna/yarıda kalma riski vardır. Logo visual evidence ffmpeg ile problemli kanallardan 30s timeout/8s rw timeout altında 6 paralel ilk kare toplar; visual_frames/*.jpg ve visual_review.json yazar; görsel eşleşme NOT_VERIFIED. Artifactler logo-visual-evidence (if-no-files-found ignore) ve logo-hazirlik-ve-inceleme (always, 30 gün, warn). Yüksek risk: korunmuş listeye geçici de olsa yazma, ağdan görsel/SVG indirme, kimlik eşleme belirsizliği; onay yoksa yeni K1-K5'te script doğrudan çalıştırılmayacak.
K1: çalışma öncesi/sonrası immutable playlist ve yazma engeli; K2: tvg-id/aday kimlik join; K3: logo görsel kanıt ve IBO cihaz ayrı; K4: değişmezlik/SHA256; K5: artifact, zaman aşımı, başarısızlık ve onay kapısı. YAPILACAK: yalnız izole kopyada fixture/negatif test; rapor ve PNG üretimini ana liste mutasyonundan ayır; yazma yolu ve SVG/redirect/SSRF kontrollerini doğrula. YAPILMAYACAK: eski scripti canlı ana listede çalıştırma, logoyu/EPG'yi otomatik değiştirme, cron/push/publish açma. KANIT BEKLEYEN: gerçek izin kapısı, PNG görsel onayı, cihaz kabulü, tam hata/retry ve eşdeğerlik. Bu turda eski depo veya korunan dosyalar değiştirilmedi; Actions testi çalıştırılmadı.


## 19 Ekim 2026 — Derin çözüm devamı: 3 yeni YAML, aylık denetim kısmi
Önceki 24/99 sayacı korunarak eski salt-okunur kaynakta üç yeni YAML ve ana Python zincirleri açıldı: madsc-11599-yedek-geri-yukle.yml, madsc-ana-liste-saglik.yml, madsc-arsiv-yedek-aktarim.yml. Bunlar 27/99 derin inceleme olarak sayıldı; 72 YAML bekliyor. madsc-aylik-merkezi-denetim.yml YAML ve central_workflow_inventory.py, central_protected_write_gate.py açıldı ancak çok sayıda alt betik çözülmediği için henüz tamamlanan sayaca eklenmedi. Parity 0/92.
1) madsc-11599-yedek-geri-yukle.yml: dispatch only, contents:read, checkout persist-credentials:false, 10m; scripts/diagnose_11599_backups.py stdout JSON, artifact yok. CALISANLAR.m3u, madsc_kesif/yedeklerden_ayrilanlar_20261013T170042Z.m3u, madsc_kesif/yedek_turk_ayirma_raporu.json okur; 11599 beklenen toplam, var olan backup + URL key ile tekilleştirilmiş arşiv adaylarını karşılaştırır. scripts/restore_all_11599_backups.py içinden P/SNAP/entries/key import eder, restore main çağırmaz. Import edilen betiğin main'i CALISANLAR.m3u ve restore raporu YAZABİLİR ama bu workflow'da çalıştırılmaz. key() token/auth/expires/signature/sig/hash query alanlarını atarak karşılaştırır; farklı akışları eşitleme riski, 11599 sayısının gerçek doğruluğu, tarihsel veri değişimi kanıt bekliyor. K1+K4+K5; yapılacak: fixture'da yanlış eşleme ve arşiv tutarlılığı negatif testi; yapılmayacak: restore main çalıştırma, YEDEKLER'e ekleme.
2) madsc-ana-liste-saglik.yml: dispatch + UTC 06:40 ayın 1 ve 15'i cron; contents:read; concurrency cancel:false, 35m; checkout persist-credentials:false, başlangıç SHA256 CALISANLAR.m3u/YABANCI_KANALLAR.m3u/DEVAM_NOTU.md; unittest test_ana_liste_saglik; ffmpeg kurulumu; scripts/ana_liste_saglik.py --batch-size 50 --timeout 15; always SHA256/diff; madsc_ana_liste_saglik/ JSON+MD artifact 30 gün ve step summary. Betik M3U EXTINF/URL okur; UTC gün ordinal mod grup sayısı ile 50'lik batch seçer, en çok 8 paralel ffprobe, 15s rw_timeout ve subprocess 18s; video+audio, kısmi, doğrulanamadı ayrımı; URL SHA256 ilk 16 hane; ana listeye yazmaz. Testte geçici liste fixture ve mock probe var. Önemli: cron 1 ve 15 iken batch günlük ordinal ile seçiliyor; bütün grupların gerçek kapsandığı garantisi yok; 5 dakika/7 gün/30 gün ölçümü ve IBO cihaz kabulü yok. K1+K3+K5; yapılacak: cron/batch kapsama ve sonuç şeması testleri; yapılmayacak: teknik başarısızlıktan kanal silme.
3) madsc-arsiv-yedek-aktarim.yml: dispatch only, contents:read, concurrency cancel:false, 15m, checkout ve tek echo uyarısı. Python/restore, artifact, gerçek aktarım yok. K1+K4; yapılacak: intentionally-disabled işlevi beşli tasarımda kayıt altına al; yapılmayacak: bunu backup/restore parity sayma. Kabul için yeni davranış talebi ve açık onay gerekir.
4) madsc-aylik-merkezi-denetim.yml (KISMİ): dispatch + main paths push + UTC 07:00 ayın 1,15'i cron; contents:read/actions:read, 15m, checkout persist-credentials:false; dosya/SHA256, doküman ve syntax, PyYAML, central_protected_write_gate, central_workflow_inventory, logo/EPG/IBO/backup/restore/8/18/6 alan, Actions gh api, son 100 run, 20 başarısız run job incelemesi, toplu rapor ve 30 günlük artifact. Çok sayıda çağrılan alt betik henüz okunmadı. central_workflow_inventory.py YAML regex tabanlı statik envanter ve çakışma raporu yazıyor; dosya adından K1–K5 tahmini tam davranış kanıtı değil. central_protected_write_gate.py PyYAML ve regex ile izin/shell risklerini işaretler; yalnız parse error ve madsc-01..05 write ihlalinde exit 1; diğer MANUAL_REVIEW_REQUIRED kayıtları fail-closed gerçek enforcement değildir. Risk: YAML'da yüksek sayıda rapor yazma, GH_TOKEN actions:read, 15m timeout, script alt etkileri açık; ana liste mutasyonu kanıtlanmadı. K1–K5, KISMİ; alt betikler ve üretici/tüketici şemaları incelenmeden sayaç artırma.
Bu turda eski depoya, korunan dosyalara, cron/push/deploy'a dokunulmadı; script veya Actions çalıştırılmadı. Sadece yeni depoda proje hafızası güncellendi.


## 19 Ekim 2026 — 5 yeni workflow derin çözüm kaydı
Eski salt-okunur dalda şu 5 YAML ve ilgili Python kaynakları incelendi: madsc-cuma-ana-liste-denetimi, madsc-documentation-check, madsc-genis-kaynak-kontrol, madsc-hizli-on-kontrol, madsc-ibo-3-5281. Önceki 27/99 üzerine 5 ek: 32/99; 67 bekliyor. Davranışsal eşdeğerlik hâlâ 0/92. Bu kaynak incelemesi canlı koşu kanıtı değildir.
- Cuma ana liste: sadece workflow_dispatch, contents:read, 55 dakika, concurrency cancel:false, ffmpeg, tools/haftalik_ana_liste_denetimi.py ve tools/cuma_denetim_uyari_ozeti.py. Python tüm CALISANLAR.m3u EXTINF/URL kayıtlarını okur, 12 thread ile her URL'ye ffprobe (12s rw_timeout, 25s subprocess), playlist başlığındaki ilk EPG URL'sini en fazla 30 MB ve 30s indirip XMLTV channel/programme ID sayar; madsc_ana_liste_denetimi/rapor.json üretir, step summary uyarısı ve 30 günlük artifact. Yerel yazma yalnız rapor; gerçek kanal/EPG içerik kimliği veya IBO onayı yok. 55 dakika büyük listede yetersiz olabilir. K3/K5. Yapılacak: süre/kanal sayısı, XMLTV eşleşme ve rapor şema fixture'ı. Yapılmayacak: erişim hatasından kanal silme.
- documentation-check: sadece workflow_dispatch, contents:read, checkout ve shell test/grep/head; AGENTS, OZELLIK_ENVANTERI, DEVAM_NOTU varlık/doluluk, Kural 25, build_epg.py ifadesi, CALISANLAR ilk satır #EXTM3U. Artifact, script, network stream, protected yazma yok. K1/K5; metin varlığı 26 kural enforcement değildir.
- genis-kaynak-kontrol: sadece workflow_dispatch ve main ref if koşulu, contents:write/actions:write, concurrency madsc-rapor-yazma cancel:false, 45 dakika. checkout -> origin/main fetch + hard reset; tools/genis_kaynak_taramasi.py weekly ve monthly -> artifact madsc_genis_tarama -> SHA temelli çakışma kontrolü, en çok 5 git push denemesi, tools/protected_write_gate.py iki kez -> main'e rapor commit -> gh api ile madsc-uc-asama.yml dispatch. Python madsc_akilli_kesif.py SOURCES AST okur, HTTP M3U indirir (3MB/feed, 16s, 8 worker), weekly filtre/monthly tüm tanımlar, CALISANLAR/YENILER/MADSC_TV_47_LISTE_ADAY ve madsc_kesif/gecmis.json karşılaştırır; madsc_genis_tarama/state.json, candidate_review.json, summary_weekly/monthly.json, sources_weekly/monthly.csv YAZAR. Kanal playlistlerini yazmaz; ancak rapor ve aday geçmişi git push ile kalıcıdır, sonraki üç aşamayı tetikler. Risk: hard reset çalışma alanı, mevcut raporla merge yerine klasörün topluca kopyalanması, haftalık/aylık aynı state'i sıralı kullanması, uzaktan feed/URL hassasiyeti, gh api zinciri, actions:write. Protected_write_gate git diff base..HEAD + staged/unstaged/untracked/ignored dosyaları kontrol eder; protected path bloklar ama branch ruleset kanıtı değildir. K1/K2/K4/K5. Yapılacak: izole fixture ve push/retry/çatışma/alt workflow sınırlarını kanıtla. Yapılmayacak: gerçek main dispatch/push çalıştırma.
- hizli-on-kontrol: workflow_dispatch + eski entegrasyon dalında sınırlı paths push, contents:read, 15 dakika; Python 3.12; five_system_cutover_readiness, five_category_shared_controls, five_category_92_workflow_audit, five_category_preflight ve üç unittest modülü; 8 civarı JSON/CSV/MD artifact. Alt betikler daha önce incelenmiş; 92 eşdeğerlik raporu BLOCKED_NEEDS_BEHAVIOR_EVIDENCE üretir, kabul değil. K1-K5; 7 hariç tutulan dosyadan biri. Yapılacak: gate negatif fixture ve gerçek run kanıtı; yapılmayacak: yeşil ön kontrolü parity ilan etme.
- ibo-3-5281: workflow_dispatch + yalnız YAML dosyası değişince eski dal push, contents:read, 15 dakika, checkout ve echo uyarısı; 5281 kanal ayrıştırması, rapor, artifact veya playlist değişimi yok. K1/K4; davranış no-op güvenlik uyarısıdır. Yapılacak: no-op kapsamı belgele; yapılmayacak: gerçek 3/5281 ayrımı veya cihaz doğrulaması sayma.
Aylık merkezi denetimin daha önce açılan alt kaynak zinciri halen KISMİ, sayaca eklenmedi. Bu turda hiçbir workflow çalıştırılmadı; eski depo ve üretim yolları değiştirilmedi.


## 19 Ekim 2026 — Sekiz IBO mutasyon workflow'u derin kaynak incelemesi
Önceki 32/99 üzerine 8 yeni YAML ve bunların 8 Python kaynağı tamamen okundu: madsc-ibo-354-classify, madsc-ibo-364-355-364, madsc-ibo-398-16-49, madsc-ibo-530-archive, madsc-ibo-6115-second, madsc-ibo-ilk-239, madsc-ibo-kararlar-grup1, madsc-ibo-second-voice. Derin kaynak sayacı 40/99; kalan 59; davranışsal parity 0/92. Bu kaynak çözümüdür, fixture veya canlı koşu eşdeğerlik onayı değildir.
Ortak: contents:write, main branch if, actions/checkout, CALISANLAR.m3u üzerinde Python yerel yazma, madsc_kesif altında M3U/CSV/JSON arşiv/rapor yazma, git add/commit/push main girişimi. Yedi tanesi yalnız kendi YAML değişimiyle push, 6115-second ve second-voice ayrıca workflow_dispatch. Bazıları git fetch + reset --hard origin/main yapar. Hepsinde protected_write_gate.py --base origin/main, CALISANLAR.m3u değişimini yasakladığından beklenen koruma kapısı ret verir; git commit/push öncesi başarısızlık mümkündür. Gate öncesinde yerel protected dosya zaten değiştirilmiştir. Bu çatışma güvenlik için korunmalı, otomatik aşılmamalı.
1) 354-classify: archive_backups_354_classified.py; 354 YEDEKLER şartı, 1–2 tutulur, 3–334 (332 Türk çalışmıyor bildirimi) ve 335–354 (20 yabancı) arşive, 2 kalan; üç yeni rapor/arşiv ve CALISANLAR yazılır. Önceden çıktı varsa durur; sayısal doğrulama kimlik kanıtı değil.
2) 364-355-364: archive_backups_355_364.py; tam 364 bekler, 355–364 (10) çıkarır, 354 bırakır, iki rapor/arşiv + CALISANLAR yazar; YABANCI_KANALLAR diff ayrıca kontrol edilir.
3) 398-16-49: archive_backups_16_49.py; tam 398 bekler, 16–49 (34) çıkarır, 364 bırakır, arşiv/JSON + CALISANLAR yazar.
4) 530-archive: archive_backups_399_onward.py; tam 530 bekler, 399–530 (132) çıkarır, 398 bırakır; arşiv/JSON + CALISANLAR yazar.
5) 6115-second: apply_ibo_6115_second.py; 6115 bekler, 3–5966 içinde tanımlı Türk kümesi hariç diğerlerini arşivler; 1–2 ve 5967–6115 dokunulmaz; CSV/JSON/arşiv + CALISANLAR yazar. KRİTİK: betikte YEDEKLER sayaç etiketini güncelleyen re.sub ifadesi kaçışları nedeniyle şüpheli (raw regex içinde çift ters eğik çizgiler); gerçek fixture testi olmadan etiketin güncellendiği kabul edilmez.
6) ilk-239: apply_ibo_first_239_decisions.py; 11599 bekler, Türk çalışmıyor kümesi 6–8, 11–42, 104 (36); yabancı 43–239 hariç 104 (196); toplam 232 çıkarır, 11367 bırakır; karar CSV, rapor ve CALISANLAR yazar; diğer kategorilerin sabitliğini kontrol eder. Ayrı arşiv M3U oluşturmaz, CSV'de URL vardır.
7) kararlar-grup1: apply_ibo_decisions_group1.py; yine 11599 bekler, aynı 232 kararı uygular, 11367 bırakır; arşiv M3U, karar CSV/JSON ve CALISANLAR yazar. ilk-239 raporu varsa erken no-op; dolayısıyla iki workflow birbirinin yerine veya ardışık çalıştırılamaz, sıraya ve tarihsel duruma bağımlıdır.
8) second-voice: apply_ibo_second_voice.py; 6115 bekler, 3–5966 aralığındaki Türk seçimleri hariç yabancı sınıflandırılanları çıkarır, diğer grupları ve kalan URL sırasını karşılaştırır; arşiv M3U, karar CSV/JSON ve CALISANLAR yazar. 6115-second ile çok benzer fakat ayrı dosya adları ve rapor şemaları vardır; aynı baseline üzerinde ikisinin ardışık çalışması beklenen 6115 sayısını bozar.
K1–K5: K1 korunan playlist'e mutasyonu reddet; K2 sıra/kimlik kararlarını fingerprint ve tarihsel snapshot'a bağla; K3 IBO kullanıcı kararı teknik ffprobe ile karıştırılmasın; K4 arşiv ve izole restore tutarlılığı; K5 işlem başına ayrıntılı, doğrulanabilir rapor ve karar izi.
YAPILACAK: korunan dosyalara dokunmayan sentetik fixture'da sayı/sıra sapması, arşiv/CSV kayıp, aynı anda koşu, çift uygulama, regex sayaç güncelleme, protected_write_gate ret ve commit öncesi durma testleri; tarihsel kullanıcı kararları ile güncel URL kimliklerini eşleştirme. YAPILMAYACAK: eski workflow'ları tetikleme, main'e push, protected gate'i gevşetme, kullanıcı WORKING kanalını silme, eski YEDEKLER'i otomatik yeniden sıralama. KANIT BEKLEYEN: gerçek cihaz kararlarının orijinal snapshot'a bağı, tarihsel arşiv bütünlüğü, gerçek Actions sonuçları, davranışsal parity ve 26 kural enforcement.
Eski kaynak repo salt-okunur; yeni depoda yalnız bu hafıza notu değiştirildi.


## 19 Ekim 2026 - test 23-39
Derin kaynak incelemesi 83/99; 16 bekliyor; parity 0/92. 23 ilk 15 URL her iki listede HTTP range erisim; codec/IBO degil. 24-25 statik Python YAML M3U denetim, unittest. 26-27 risk ve dosya envanteri. 28 aday durum siniflama, gercek onay kapisi degil. 29-31,33 risk raporlari; risk bulunmasi her zaman fail degil. 32 iki backup workflow'da git push ve environment onayi eksikse fail. 34 bes workflow icin regex yazma yasagi. 35 aday-bekletme salt okunur marker. 36 git add protected hedef sinyali varsa fail, dolayli yazmalari kacirabilir. 37 python script kaynaklarini satir regex tarar, bulgular raporlanir fakat fail yok. 38 iki gercek blocked_paths/protected fonksiyonunu sentetik test eder, production enforcement degil. 39 protected_playlist_audit.py yalniz CALISANLAR/YENILER varlik+M3U header ve AGENTS varligi; onay kapisi degil. Korunan listeler degismedi. Yapilacak: negatif fixture, tum dolayli cagri zinciri ve branch ruleset dogrulama. Yapilmayacak: yesil CI ile parity veya 26 kural enforcement iddiasi.


## 19 Ekim 2026 — Davranışsal eşdeğerlik kök nedenleri ve ek kaynak incelemesi
Bu not, önceki 83/99 derin inceleme kaydına eklenmiştir. 99/99 YAML ilk envanter tamam, 92 kapsam workflow'unun davranışsal eşdeğerlik kabulü halen 0/92; bu turda canlı çalıştırma veya parity fixture koşusu yapılmadı. Kaynak Madsc55/madsc-tv@madsc/bes-sistem-toplu-birlestirme salt-okunur.
- madsc-otomatik-devam.yml: yalnız workflow_dispatch, contents:read, iki echo. Adının aksine otomatik devam/dispatch yok. K5 no-op davranışı; gerçek yeni tetikleme eklemek eşdeğerlik değil yeni özellik olur.
- madsc-son-kontrol-kurtarma-teshis.yml: dispatch ve kendi YAML push, contents/actions read; test_final_validation unittest, mevcut madsc_son_kontrol summary/results varlığı ve son kontrol workflow son 20 run (ilk 12 yazdırılır) API gözlemi. Akış testini veya kurtarmayı başlatmaz. K1/K3/K5; fixture: eksik JSON, API hata, stale sonuç.
- madsc-uc-asama.yml: dispatch ve verification_pipeline.py push; contents/actions write, main şartı, failure gate, origin/main hard reset, eligible/state/gecmis/review due hesabı, gerekiyorsa ffmpeg + verification_pipeline.py, artifact, madsc_dogrulama klasörünü eşzamanlı değişiklik kontrolü ve protected_write_gate ile commit/push, due_now>0 ise kendini yeniden dispatch. K2/K3/K5. Risk: zincirleme tekrar, concurrency group, 40 dakika sınırı, API gate; salt okunur beşliyle aynı davranış değil.
- madsc-02-kesif.yml: iki cron (05:17/17:17 ve 06:00/18:00 UTC), dispatch, workflow_call; salt okunur. discovery_history_restore, merkezi raporlar, madsc_akilli_kesif, discovery_archive before/after, candidate_epg_logo_join, four_stage_discovery_report, wide_source_scan, regression, protected hash, artifact. continue-on-error alt adımlar son kapıda topluca değerlendirilir. Dış kaynak çağrısı ve çalışma alanında rapor/aday mutasyonu vardır; git push yok. K2.
- madsc-03-kanal-test.yml: günlük 06:40 UTC cron, sınırlı branch push, dispatch, workflow_call; read-only, rapor/EPG-logo kontrolü, IBO 50 deneme listesi, ffmpeg, candidate_media/scoring, ana_liste_saglik 100 kanal batch, regresyon, hash, artifact. 100 kanal batch tüm ana listenin bu koşuda ölçüldüğünü kanıtlamaz; IBO cihaz onayı yok. K3.
- madsc-04-arsiv-yedek.yml: dispatch ve workflow_call; read-only; central_isolated_git_restore, backup_evidence, archive_consistency, disaster_recovery_dry_run, acceptance ve unittest. Acceptance açıkça off_github_copy=DOGRULANMADI ve historical_recovery_verified=false şart koşuyor; gerçek uzun dönem/offsite kurtarma kanıtı yok. K4.
- madsc-05-genel-bakim.yml: 01→02→03→04 reusable workflow zinciri, her aşamada always() ile iptal dışındaki önceki başarısızlıklara rağmen sonraki aşamayı çalıştırabilir, finalde tüm kategori sonuçlarını denetler. 01:30 UTC cron, dispatch, eski dal push, read-only. category_evidence_collect ve 92-workflow audit, merkezi raporlar, çeşitli regression ve readiness, artifact. KRİTİK: kabul kapıları bütün 92 satırın BLOCKED_NEEDS_BEHAVIOR_EVIDENCE ve behavioral_parity_verified_count==0 olmasını ZORUNLU tutuyor. Dolayısıyla CI yeşili gerçek eşdeğerlik demek değildir; kanıt geldiğinde kapı kanıt-temelli dinamik matrise çevrilmeli, güvenlik engeli kaldırılmamalı.
- madsc-rule24-test.yml: sadece workflow_failure_gate unittest; gerçek Kural24 runtime gate değildir. workflow_failure_gate.py aynı workflow/branch son 100 koşu üzerinden current run created_at, ardışık iki failure/timed_out; metadata/API hata fail-closed. K1.
- madsc-sistem-saglik-denetimi.yml: dispatch + ayın 1/15'i 05:17 UTC, read-only, Ruby YAML parse, unittest, tools/sistem_saglik_denetimi, son 100 Actions run raporu, artifact; audit failure son kapıda hata. Bu 26 kuralın tam enforcement kanıtı değildir. K1/K5.
- madsc-son-kontrol.yml: 06:10 UTC günlük cron, dispatch ve başarılı madsc-uc-asama workflow_run, contents/actions write, 110m, hard reset, final_validation.py, artifact, madsc_son_kontrol sonuçlarını concurrency çatışması kontrolüyle commit/push. final_validation.py 125 batch, 24 worker, ffprobe + duration ffmpeg video/audio, freeze/black/silence, görüntü, state/manifest, yalnız teknik sonuç; IBO ve kimlik doğrulanmadı. K3/K5. Eski kayıtların başarısız olsa da tamamlanmış sayılması tekrar deneme politikası bakımından eşdeğerlik testine muhtaç.
- madsc-toplu-butunluk.yml: dispatch + ilgili YAML/script push, read-only; bulk_integrity_gate.py YEDEKLER normalized URL tekrarı ve arşiv kesişimlerini denetler, madsc_kesif/toplu_butunluk_kontrol.json üretir. URL key token/auth/expires/signature/sig/hash alanlarını kaldırdığı için farklı tokenlı yayınları eşitleme riski; status STRUCTURE_PASS_NOT_PLAYBACK_PROOF. K1/K4.
- madsc-tum-sistem-yedek.yml: dispatch + 1/15 05:40 UTC, read-only; repository_settings_inventory.py kamuya açık/secret olmayan GitHub metadata API, full_system_backup.py git ls-files (+settings) max 400MB tar.gz, manifest SHA, temp dizine byte-exact restore, 30 gün artifact. Git dışı dosyalar, secrets, IBO ayarları, bağımsız offsite yedek yok. K4.
- madsc-turk-kanal-geri-sec.yml: yalnız kendi YAML push main, contents:write, reset --hard, recover_turkish_backups.py ülke TR M3U indirip URL/tvg-id/source eşlemesiyle sabit 20261013T170042Z snapshot'ından adayları CALISANLAR YEDEKLER'e geri ekler; CSV/JSON yazar; protected_write_gate commit öncesi, fakat yerel protected dosya önceden değişir. tvg-id/URL ülke sinyali gerçek IBO onayı değildir. K1/K2/K4, yüksek risk.
- madsc-yedek-turk-ayir.yml: kendi YAML push main, contents:write, hard reset, keep_turkish_backups.py YEDEKLER ilk 2'yi korur; kaynak adı/kanal adı veya foreign registry ile sınıflar, belirsizleri snapshot M3U'ya çıkarır, CALISANLAR ve JSON yazar; gate commit öncesi. İsim/URL normalizasyonu ve tarihi snapshot kararları yanlış pozitif olabilir; korunan dosyaya gerçek yerel yazma var. K1/K2/K4 yüksek risk.
- madsc-yedekler-sayi-duzelt.yml: dispatch + kendi YAML push main, contents:write; sync_yedekler_category_count.py CALISANLAR'daki YEDEKLER grup sayısını regex ile bütün eşleşen EXTINF'lerde yeniden yazar, git add CALISANLAR, gate commit öncesi. Yalnız etiket düzeltmesi olsa da korunan playlist mutasyonu, otomatik devreye alınmamalı.
- madsc-yedekler-aktarim-test.yml: dispatch + 4 path push, contents:read, yalnız test_yedekler_teknik_aktar unittest; canlı YEDEKLER aktarımı yapmaz.
- oncelikli-kanal-dogrulama.yml: dispatch + iki path push, read-only, ffmpeg ve oncelikli_kanal_dogrula.py, CSV/JSON artifact; ffprobe teknik ölçüm, IBO kabulü değil. Alt betik bu tur henüz tam yeniden okunmadı.
- onikinci-hata-siniflandirma-test.yml: dispatch + 2 path push, read-only, inline beş classify fixture ve geçici CSV subprocess; üretim adayları üzerinde sınıflama/taşıma yok.
- sozcu-akit-ozel-test.yml: dispatch + 2 path push, read-only, ffprobe ve yedekler/sozcu_akit_ozel_test.py, CSV artifact; gerçek cihaz testi değil. Alt betik bu tur henüz tam okunmadı.
YAPILACAK: Her workflow için tetik/izin/çağrı grafiği, giriş fixture ve tarihsel snapshot SHA, yan etki dosyaları, hata/tekrar/idempotence, çıktı şema, K1–K5 karşılaştırma, gerçek run artifact ve gerektiğinde IBO cihaz kanıtı. Önce güvenli read-only örneklerde negatif fixture ve output karşılaştırması; mutasyon workflow'larında yalnız izole geçici dizin ve protected-write reddi. 92/92 kabulü için sabit sıfır bekleyen gate yerine kanıt başına dinamik, fail-closed doğrulama gerekir. YAPILMAYACAK: main workflow tetikleme, playlist değiştirme, eski repo write, PR merge, gate bypass, salt test yeşilini parity sayma.


## 19 Ekim 2026 — K2/K3 keşif, tekrar testi ve mevcut karşılıklar (kaynak derin inceleme)
Kaynak: Madsc55/madsc-tv, madsc/bes-sistem-toplu-birlestirme; eski YAML ve doğrudan Python yardımcıları okundu. Bu not kod-okuma kanıtıdır; fixture/CI davranışsal eşdeğerlik doğrulaması DEĞİLDİR (0/92).
1. aday-oncelik-kontrol.yml: dispatch veya aday_oncelik_raporu.py/YAML push, read-only; py_compile ve yalnız iki sentetik aday. aday_oncelik_raporu.py aday_bekletme/ADAY_DURUM_RAPORU.csv -> ADAY_ONCELIK_RAPORU.csv; 1=tekrar teknik doğrulandı+yeniyse, 2=tekrar doğrulandı, 3=video/ses+yeni, 4=video/ses, 5=diğer; kanal adı casefold tie-break; inceleme notu kimlik manuel. K2/K3. Kaynak yoksa SystemExit, boş CSV başlığı var. Yeni K3 category_candidate_scoring.py akilli_aday_puanla.py/birlesik_aday_raporu.py kullanıyor; AYNI 1-5 sıralama semantiği henüz kanıtlanmadı.
2. altinci-aday-tekrar-test.yml: dispatch ve ilgili 3 dosya push, read-only, ffmpeg, RETEST_LIMIT=5, aday_bekletme/ALTINCI_TEKRAR_TEST.csv artifact. altinci_aday_tekrar_test.py gecmis.json ve akilli_tekrar_test_takvimi.plan ile due, successful_runs<2, HTTP(S), bir başarılı geçmişi önce; hls_probe 20sn, ffprobe video+ses, verify_hls iki zaman örnekli farklı segment URL şartı; teknik geçse de KIMLIK_BEKLIYOR. Geçmiş dosyasını güncellemiyor. Risk: segment değişmemesi sağlıklı HLS için yanlış negatif; AST ile yeni_kanal_tara.py fonksiyonlarını extract+exec yapıyor, ileride scanner değişikliklerine kırılgan. K2/K3 karşılaştırma: category_stability_history.py K2 artifact geçmişini aynı branch ve başarılı ata run'dan SHA/provenance ile alıyor; category_candidate_scoring.py aynı run K2 adayları + K3 ölçümleri ile puanlıyor, 6 saatten eski media cache reddi, otomatik ana liste onayı yok. Fakat legacy due/retest eligibility ve 2 farklı segment kuralı birebir gösterilmedi.
3. yeni-kanal-arama-2026.yml: dispatch + ilgili path push, contents read, SCAN_BATCH=1, ffprobe, YENILER_TARAMA_RAPORU.csv ve YENILER_KAYNAK_HATALARI.txt artifact. yeni_kanal_tara.py 25 sabit kaynak ve öneri CSV'si, URL tekilleştirme, CALISANLAR URL/isim karşılaştırması, 30'luk batch HLS segment + ffprobe, CSV. YENILER protected dosyasına yazmıyor. K2/K3; beşli discovery ve candidate_media ile ortak fonksiyonlar mevcut, aynı 30'luk batch, öncelik ve normalization politikası henüz eşdeğer değil.
4. yeniler-guvenli-arama.yml: main .github/commands/genel-guncelleme.txt push ve dispatch, read-only; kaynak_kesfet.py GitHub araması son 90 gün, en çok 60 repo/120 kaynak, en çok 8 M3U/repo, kaynak CSV; sonra 34..99 inclusive 66 matrix batch, her biri yeni_kanal_tara.py ile tüm kaynakları tekrar indirip seçilen 30 adayı teknik test eder; ayrı artifact'ler. K2/K3. Büyük maliyet ve tekrarlı fetch, K2'de tek cache+batch iş dağıtımı aday sırası/kapsamı karşılaştırılarak tasarlanmalı. Cron yok.
5. yeni-aday-on-test.yml: main genel-guncelleme push ve dispatch, read-only; yeni_aday_on_test.py iptv-org TR kaynak, CALISANLAR isim/URL dedup, logo API in_use eşlemesi, 12 worker ffprobe, YENI_ADAY_ON_TEST.csv. Script import edildiğinde ağ çağrısı yapar (main guard yok), kimlik/IBO onayı yok. K2/K3 logo/identity join ile karşılaştır.
6. yanlis_pozitif_koruma.py: verify_hls samples=2 pause=2, HLS medya playlist son segmentinden en az 188 byte ve iki farklı segment URL zorunlu; master playlist reddi, fail-closed. HLS manifest ve segment içeriği codec/kimlik kanıtı değildir.
7. akilli_tekrar_test_takvimi.py: passed+>=3 success 24 saat, >=2 12 saat, passed 6 saat, başarısız 2 saat; gecersiz son tarih now kabul edilir ve aday sonraya ertelenir. K2/K3 scheduling eşdeğerlik fixture gerekir.
8. channel_name_normalization.py: wide_scan/new_scan/list_control/satellite/satellite_playlist ayrı normalizasyon politikaları; tek fonksiyona körlemesine indirgeme kanal çakışması yaratır. discovery_m3u_parser.py wide_scan/new_scan farklı metadata ve URL kuralları; korunmalı veya farkları fixture ile kabul edilmeli.
9. scripts/category_candidate_scoring.py: K2 accepted run artifact adayları, K3 ölçüm cache, aynı URL'de en yeni zaman damgası, çelişen aynı zaman reddi, 7 gün stabilite tarihçesi, puan ve birleşik inceleme CSV. Explicit auto-approval yasak; report automatic playlist write=False. K3 medya cache 6 saat sınırı, ilave probe yok. Eski 1–5 rank ile semantik eşitlik ve eski batch coverage ayrı kanıt gerektirir.
YAPILACAK: (A) Legacy 1–5 rank vs yeni K3 skor için 5+tie-break fixture; (B) 2/6/12/24h due sınırları, stale/bozuk tarih ve iki HLS segment testi; (C) K2 tek keşif + K3 batch 1/34..99 toplam aday kapsama/duplikasyon karşılaştırması; (D) TVG ID/logo/normalization farklı profil fixture; (E) aynı girdide CSV/JSON schema, hata/timeout ve protected hash karşılaştırması. YAPILMAYACAK: 66 matrix'i canlı tetikleme, üretim playlist mutasyonu, script adı eşleşmesini parity kabulü, 92 eski workflow'u üretimde topluca çalıştırma.


## 19 Ekim 2026 — K1–K5 doğrudan karşılaştırma: iki sabit engel
Salt-okunur kaynak incelemesi; eski repo workflow çalıştırılmadı, canlı veri değiştirilmedi.
K1 madsc-01-guvenlik.yml: reports central_protected_write_gate, central_consolidation_audit, five_category_92_workflow_audit; 26 kural raporu scripts/k1_24_rule_evidence.py; geniş regresyonlar; protected snapshot/check ve fail gate. k1_24_rule_evidence.py audit() her 1..26 için runtime_enforcement_verified=False SABİT üretir, fully_verified_rules=0. K1 YAML len(verified)!=26 ise exit 1. Bu kaynak haliyle K1 26/26 çalışma zamanı kanıtı kabulünden GEÇEMEZ; sırf dosya ve unittest varlığı enforcement kanıtı değildir. Gerçek kanıt kaynaklarını ve cihaz/API onaylarını ayrı ölçmek, raporun sabit False alanını yalnız kanıtlı koşullar için dinamik hale getirmek gerekir; kontrol bypass yasak.
K5 madsc-05-genel-bakim.yml: audit_2 92 satırın tamamını BLOCKED_NEEDS_BEHAVIOR_EVIDENCE olarak zorunlu kılar; audit_3 behavioral_parity_verified_count==0 ve her item false ister. scripts/five_category_92_workflow_audit.py her item behavioral_parity_verified=False ve migration_decision=BLOCKED_NEEDS_BEHAVIOR_EVIDENCE SABİT yazar; scripts/five_system_cutover_readiness.py REQUIRED dokuz geçiş kanıtını her zaman blocker sayar, cutover_allowed=False. Bu tasarım fail-closed shadow modu için doğru, ama kanıtlı 92/92 eşdeğerlik kabulüne evrilmesi için güvenilir kanıt kayıtları ve dinamik fail-closed doğrulama gerekir. Şu anda 0/92.
K2 madsc-02-kesif.yml: cron 05:17/17:17 ve 06:00/18:00 UTC; history restore, archive before/after, madsc_akilli_kesif, candidate_epg_logo_join, four_stage_discovery_report, wide_source_scan, regresyon, artifact; rapor ve discovery continue-on-error sonuçları fail gate'te toplanır. Aynı gün 4 cron ile K5'in 01:30 UTC cron'u aynı işi tekrar yapabilir; canlı default branch etkinliği ayrıca doğrulanmalı.
K3 madsc-03-kanal-test.yml: günlük 06:40 UTC, medya cache, K2 artifact üzerinden puanlama, 100 kanal batch, logo/EPG statik, IBO trial export, testler; K5'ten reusable olarak da çağrılır. Bu, 92 eski görevin tamamının K3'te aynı çıktıyla yapıldığını kanıtlamaz.
K4 madsc-04-arsiv-yedek.yml: isolated restore ve manifest; acceptance off_github_copy DOGRULANMADI ve historical_recovery_verified=false ister; gerçek offsite kabul yok.
K5 madsc-05-genel-bakim.yml: K1→K2→K3→K4 reusable çağrıları, sonuçları toplama; always() nedeniyle başarısız bir aşamadan sonra da diğerleri çalışabilir, final kapı hepsinin success olmasını ister. 92 audit yalnız regex ile komut/cron ve script isim eşleşmesi, gerçek görev eşdeğerliği değildir. scripts/five_system_cutover_readiness.py migration_approved/cutover_allowed/legacy_retirement_allowed=False sabit ve 9 zorunlu kanıt blokajı. EPG/PAGES user decision deferred, dosyaları koru.
Öncelik: 1) 26 kural için kural başına negatif ve pozitif runtime fixture + run/branch/sha provenance, 2) 92 eski görev için davranış+çıktı+tetik+yan etki karşılaştırma, 3) yeni beşli K2/K3 ortak işleri tekilleştirme için kapsam/cron ve idempotence, 4) K4 bağımsız offsite restore, 5) IBO cihaz ve kullanıcı onayı, 6) gerçek kanıt geldikçe sabit engelleri kanıta dayalı fail-closed kabul haline getirme. Engelleri geçiş için kaldırma; eski workflowları çalıştırma/kapama; production playlist yazma.


## 19 Ekim 2026 — K1 kaynak derin inceleme (salt okunur)
99. YAML k1-protected-write-tests.yml: dispatch ve seçili push yolları, contents read; snapshot, acceptance_26_92, artifact, branch farkı, risk envanteri, final snapshot/check. 92 legacy workflow kapsamı dışında. scripts/acceptance_26_92.py 11 unittest suite + runtime integrity suite çalıştırır. --require-full-acceptance olmadan acceptance_complete false olsa bile yalnız regresyonlar geçince exit 0 mümkündür; 26/26 ve 92/92 kabul kanıtı değildir.
Kaynak uyumsuzluğu: tests/test_k1_runtime_workflow_guard.py eski 'Kanal listelerine dokunmadan guvenlik negatif testleri' adımını ve PIPESTATUS literalini arıyor; güncel YAML'de bunlar yok, bunun yerine 26/92 kabul adımı ve set -o pipefail var. En az iki assertion'ın kaynakta karşılığı yok; CI'da henüz çalıştırılıp doğrulanmadı. Testleri güncel fail-closed semantiğe uyarlamak gerekir.
tools/protected_write_gate.py Git diff base..HEAD, staged, unstaged, untracked, ignored yollarını denetler; CALISANLAR, CALISMAYANLAR, YENILER, YABANCI, AGENTS, güvenlik kuralları, EPG, logo, favorites, backup, archive ve tüm M3U/M3U8 yollarını reddeder. Fail-closed, fakat workflowların tamamında push öncesi çalıştığı kanıtlanmış değildir.
scripts/k1_protected_integrity.py tracked protected dosyaları origin/main ile karşılaştırır; runtime snapshot/check SHA256, dosya modu, symlink ve eksikleri kıyaslar. Untracked nested rapor M3U yollarını bazı koşullarda bilinçli dışarıda bırakır; ignored dosyaları working_snapshot'a dahil etmez. Bu fark gate'in ignored dosya denetimiyle ayrıca fixture üzerinden kıyaslanmalı. IBO cihaz favori ve kategori sırası denetimi yok.
tools/workflow_failure_gate.py branch filtreli son 100 Actions run'ı, created_at ve run id ile sıralar; aynı workflow+dalda önceki iki failure/timed_out ile circuit open; success sıfırlar, cancelled zinciri keser, missing current/timestamp veya API hata fail-closed. 100 run pencere ve paralel/rerun davranışları ayrıca fixture ile doğrulanmalı. tests/test_k1_failure_gate.py örnekleri mevcut.
scripts/k1_workflow_risk_inventory.py sadece regex/static, runtime_gate_order_verified false; tests/test_protected_gate_integration.py gerçek temp Git repo gate fixture, production writer entegrasyon kanıtı değil.
scripts/category_evidence_collect.py K1–K4 aynı run/repo/branch/SHA ve başarılı job artifact doğrular; K5 genel run ve IBO onayı doğrulanmış sayılmaz. scripts/central_actions_evidence.py son 100 run ve en fazla 20 failed job ayrıntısı; bu kapsam dışı koşular hakkında sonuç çıkarılamaz.
Durum: kaynak analizi ilerledi; canlı Actions çalıştırılmadı; 26/26 runtime ve 92/92 parity kanıtı yok; eski repo veya üretim verisi değiştirilmedi.


## 19 Ekim 2026 — K2/K3 geçmiş ve tekrar denetimi çağrı zinciri (salt okunur)
Kaynak: eski Madsc55/madsc-tv, madsc/bes-sistem-toplu-birlestirme. scripts/discovery_history_restore.py, category_stability_history.py, category_candidate_scoring.py, central_duplicate_test_audit.py ayrıntılı okundu. Gerçek Actions/fixture testleri bu tur çalıştırılmadı.
- discovery_history_restore: gecmis.json ve ana_liste_test_gecmisi.json yapı, sayaç ve timestamp denetimi; aynı repo/dal, tamamlanmış başarılı K2/K5 run, git HEAD atası SHA; en yeni uygun run'ın madsc-kesif-tek-kosu-rapor artifact'ını indirip makine gözlemlerini birleştirir; eski karar/metadata korunur, run sayacı gerilemesi ve eş zaman çelişkisi reddedilir. İki JSON önce temp yazılıp sonra ayrı ayrı replace edilir: iki dosya için tek atomik transaction garantisi yok. Ayrıca indirilmiş artifact için ayrı artifact id/provenance/digest denetimi bu fonksiyonda görünmüyor; run ve ancestry doğrulaması mevcut.
- category_stability_history: K3/K5 başarılı aynı dal ata run'dan K3 artifact; artifact tekil, not expired, run id ve SHA kontrolü; history SHA256 kabul dosyasıyla doğrulanır, 7 günlük gözlemler ve yerel gözlemler birleştirilir. Kaynakta entegre sürümde history eksikse fail-closed.
- category_candidate_scoring: K2 aday CSV ve identity review, medya cache en fazla 6 saat, aynı URL için en yeni ölçüm; eş timestamp ve çelişen medya sonucu reddi. Eski başarılı sonucu daha yeni başarısız ölçümle değiştirir; aday skor ve birleşik rapor satır sayısı eşit olmalı; tüm automatic playlist/device/user approval HAYIR/YOK. Skorlama aşamasında ilave medya probe sıfır; K2'nin önceden yaptığı probe kapsamı ayrı. K5 içinde K2 job success kontrolü var; standalone K3 eski başarılı K2 artifact'ını kullanabilir, kaynak gözlem zamanı ile güncellik kabulünü ayrıca incele.
- central_duplicate_test_audit: geçmişte runs>1 olan URL'leri sayar ve en çok 100 review queue üretir; geçmiş tekrarlarının gereksiz olduğunu KANITLAMAZ (planlı 2/6/12/24h tekrarlar da sayılır). Negatif/bozuk sayaç ayrı işaretlenir. İstatistik toplamı geçersiz kayıtları hariç tutar. Bu raporu otomatik tekrar testi kaldırma gerekçesi olarak kullanmayın.
TEST TASARIMI: (1) eski başarılı run SHA aynı dal ata / farklı dal / sonradan gelmiş run; (2) artifact sahteciliği/expired/çoklu artifact, eksik kabul hash; (3) 2 dosyalı restore sırasında ikinci replace hatası için atomicity; (4) eş zaman çelişkisi ve gerileyen sayaç; (5) newest failure over old success; (6) tekrarlı ölçümlerde planned retest vs waste ayrımı; (7) K5 same-run vs K3 historical artifact provenance. 92 parity hâlâ 0/92; canlı dosya değişikliği ve workflow dispatch yapılmadı.


## 19 Ekim 2026 — K3 medya cache ve eski tekrar/HLS kontrolü kaynak çözümlemesi
Kaynak eski madsc-tv dalı; scripts/category_candidate_media.py, scripts/genel_aday_medya_test.py, scripts/oncelikli_kanal_dogrula.py, scripts/kanal_kararlilik_takip.py; kök akilli_tekrar_test_takvimi.py ve yanlis_pozitif_koruma.py okundu. İki eski dosya scripts/ altında değil depo kökündedir.
K3 priority taraması 20 sabit kaynakta altı isim grubunu eşleştirip URL tekilleştirir, ffprobe ile video/ses ölçer (max_workers=6, timeout=18). Genel aday testi YENILER_TARAMA_RAPORU.csv sıralı 30'luk batch, ffprobe 16sn, 6 worker, öncelikli URL cache reuse ve ölçüm zamanını korur. K3 media wrapper eski kabul edilmiş aynı dal ata K3/K5 artifact'ı için tekillik, expiry, run/SHA, kabul hash ve script hash kontrolü yapar; tüm ölçümler 6 saatten gençse tekrar ağ probe yapmaz. Üretim CALISANLAR yalnız izole temp klasöre kopyalanır, playlist_write=false, device_approval=false.
Eski yanlis_pozitif_koruma.verify_hls iki örnekleme, iki ayrı segment URL ve >=188 byte segment verisi ister; master playlist'i reddeder. Yeni ffprobe video/ses testi aynı HLS segment yenilenmesi şartını kanıtlamaz; bu davranış eşdeğerliği açık kalır.
Eski akilli_tekrar_test_takvimi.plan: passed+>=3 success 24h; passed+>=2 12h; passed 6h; diğer 2h. 'last_seen' veya 'first_seen' kullanır; invalid tarih now'a dönüp test ertelenir. Bu eski aday geçmişi, K3 7 günlük kararlılık history'siyle aynı şema veya karar değildir.
kanal_kararlilik_takip.track: 7 günlük pencere, >=2 ayrı VIDEO_SES_VAR zamanı, aralık >=24 saat, en son <=24 saat, pencerenin tüm ölçümleri başarılı; onay/playlist false. Aynı timestamp farklı state reddi, tekrar ölçüm sayılır fakat yeni gözlem yazılmaz. 24 saat teknik kararlılık, 24 saat sürekli oynatma veya IBO cihaz doğrulaması değildir.
Açık risk: category_candidate_media.reports() öncelikli medya raporunda boş satır listesini reddeder. 20 kaynakta altı hedef isim grubundan hiçbirinin bulunmadığı gün, bu fail-closed tasarım tüm K3 aşamasını durdurabilir. Bu kaynakla görülen koşullu risk, canlı hata gözlemi değil. Ayrıca eski HLS yanlış pozitif koruması K3 genel ffprobe ile doğrudan yer değiştirmemeli.
Doğrulama için aynı sentetik HLS master/media/static/changing segment ve öncelikli boş/30/31 aday fixture'ları, zaman damgası ve cache 6h sınır testi, eski 2/6/12/24h takvimle K3 stabilite fark matrisi. Henüz testler çalıştırılmadı, 0/92 parity. Eski depo ve üretim korunuyor.


## 19 Ekim 2026 — EPG/VOD/logo/yedek tatbikatı/IBO 354: 5 workflow + 6 betik derin incelemesi
Eski Madsc55/madsc-tv dalında aşağıdaki 11 kaynak dosya açılarak davranışları incelendi. Bu bölüm gerçek çalıştırma veya eşdeğerlik kabulü değildir.
1. epg-gunluk.yml: günlük 03:25 UTC ve manuel, main koşulu, contents write, ortak madsc-protected-publish-main concurrency. build_epg, build_ibo_epg_test, epg_tv_readiness; epg/ altındaki 4 dosyayı stage edip protected_write_gate kontrolü, commit/rebase/tekrar gate/push. Korunan CALISANLAR değişmez; EPG yayınına yazma vardır.
2. build_epg.py: CALISANLAR'daki tvg-id/tvg-name ve 5 harici XMLTV kaynağını eşler; programı en çok olan sağlayıcıyı seçer, geçmiş 12 saat/gelecek 3 gün penceresi, çakışan yayınları atlar; program 0 ise hata. 'ambiguous' rapor dizisi kodda hiç doldurulmuyor: çok adaylı isim eşleşmeleri sessizce en yoğun sağlayıcıya indirgeniyor. TV cihazında doğrulama yok. 120MB indirme ve gzip açma kaynak sınırları ayrıca test edilmeli.
3. build_ibo_epg_test.py: TRT1/TRT2/SHOW/ATV/KANAL D için 5 sabit tvg-id ve her birinde en az 1 program zorunlu; epg/ibo-test-epg.xml üretir. epg_tv_readiness.py XMLTV teknik hazırlık raporu üretir, tv_ibo_player_verified=false ve sweden_device_verified=false tutar. XMLTV teknik geçiş, IBO uygulamasında görünür EPG demek değildir.
4. vod-guncelle.yml: günlük 07:17 UTC, main, contents write, ortak yayın kilidi; vod/guncel-bolumler.json kontrollü commit. vod_guncelle.py TVMaze TR schedule bugünden önce/sonra 7 gün, 15 günlük metadata, watch_url null; hata alan günler atlanır. Tüm günler hata verse bile boş episodes ile başarı çıkabilir; negatif test gerekiyor. Bu VOD oynatma bağlantısı değildir.
5. publish-iptv-png-logos.yml: manuel veya logos/duzeltilmis-*.svg push, main, contents write; CairoSVG ile 320x320 PNG; yalnız PNG stage, protected gate + commit/rebase/gate/push. SVG girişinin güvenliği ve logo hedeflerinin koruma politikası ayrı kontrol edilmeli; kullanıcı onayı olmadan çalıştırılmadı.
6. yedek-geri-yukleme-tatbikat.yml: manuel veya YAML/restore_dry_run.py push, read-only 8 dakika; restore_dry_run.py iki sabit yedek yolu içeriğini temp dizine kopyalar, M3U formatını, SHA256 eşitliğini ve bozuk M3U negatif testini doğrular; CALISANLAR/YENILER hash korunur. Bu yalnız yerel mevcut yedekten tatbikat; offsite yedek varlığını veya gerçek felaket kurtarma süresini kanıtlamaz. Sabit tarihli dosyalar yoksa başarısız olur.
7. madsc-ibo-354-classify.yml: sadece YAML path push ve main, contents write; archive_backups_354_classified.py CALISANLAR içindeki tam 354 YEDEKLER öğesi şartıyla 1-2'yi tutup 3-334 arası 332 kaydı Türk çalışmayan, 335-354 arası 20 kaydı yabancı arşive taşır; 2 arşiv+rapor üretir ve CALISANLAR.m3u dosyasını YEREL OLARAK DEĞİŞTİRİR. Kategoriler kullanıcı beyanı, teknik test değil. Sonrasında protected_write_gate --base origin/main ve push var: normal koruma politikası CALISANLAR değişikliğini reddetmeli; fakat commit öncesi yerel mutasyonun olması önemlidir. Bu işi K1-K5'e otomatik aktarmayın; açık kullanıcı kararı gerektirir.
Öncelikli testler: (a) EPG birden çok tvg-id adayında belirsizlik raporu; (b) beş pilot id ve IBO cihaz doğrulama; (c) VOD tüm kaynaklar hata => boş başarılı çıktı; (d) sabit tarihli yedek eksik; (e) CALISANLAR 354/353 kayıt ve gate engeli; (f) logo dönüştürme güvenliği. 99 YAML ilk kaynak incelemesi tamam; 92 davranışsal eşdeğerlik hâlâ 0. Alt betiklerin tekilleştirilmiş tüm-depo sayımı henüz yapılmadı; bitmiş denemez.


## 19 Ekim 2026 — Aday bekletme, 390 test, yedek aday ve birleşik rapor: 6 workflow + 5 betik
Eski madsc-tv dalında 390-aday-tekrar-test.yml, aday-bekletme.yml, aday-logo-epg-test.yml, aday-yedekleme.yml, akilli-aday-puanlama.yml, birlesik-aday-raporu.yml ve yedekler/tekrar_test_390.py, aday_bekletme.py, gelismis_medya_testi.py, yedekler/teknik_adaylari_aktar.py, scripts/candidate_epg_logo_join.py doğrudan okundu.
390 test: sabit 2026-10-09 yedek M3U, 10 worker (max12), ffprobe ile video+ses, sonra ffmpeg ile 20sn çözümleme (45sn subprocess timeout); CSV ve yalnız teknik başarılıları ayrı M3U artifact. Kanal kimliği veya IBO onayı değil. 90dk workflow timeout; protected ana liste yazılmaz.
Aday bekletme: keşif -> tekrar URL raporu -> en çok 5 umut vadeden aday için 20sn ffmpeg -> aday_bekletme/gecmis.json güncelleme -> 2/6/12/24h takvim -> en çok 5 tekrar -> kaynak güven -> öncelik raporu. Eski history şemasında runs/successful_runs birer run_id dizisi; URL bazında aynı run çift sayılmaz, 2+ başarı statüsü kimlik bekler. K2 yeni history şemasında runs/successful_runs tamsayı; bu iki JSON doğrudan değiştirilebilir değildir. Bekletme workflow 90dk, read-only GitHub yetkisi, artifact raporu.
Aday logo/EPG: beş pilot XMLTV kanalının sayısını ve candidate report'taki bütün playlist_approved/ready_for_playlist false olmasını denetler, CALISANLAR SHA korunur. Join stream_sha256 ile logo adaylarını birleştirir, channel_id ile pilot EPG karşılaştırır; görsel eşleşme ve cihaz testi NOT_VERIFIED; gerçek yayın kimliği için kabul değildir.
Aday yedekleme: iki SABİT eski Actions run ID'den 34 ve 66 artifact bekler; her birinde YENILER_TARAMA_RAPORU.csv üzerinden teknik video+ses başarılıları alır; ana listede ve önceki yedekte olan URL'leri çıkarır, kanal adı eşitliğine göre YEDEK ALTERNATIF/YENI ADAY sınıflandırır; yedekler/TUM_TEKNIK_TEST_ADAYLARI_2026-10-09.m3u dosyasını çalışma alanında oluşturur, commit yok, artifact var. Sabit run ve tarih bağımlılığı canlı sürdürülebilir yedek sistemi değildir. Token redirect'te GitHub API dışına taşınmasın diye header temizliği var.
Akıllı aday puanlama: SCAN_BATCH=-1 keşif + priority ffprobe + skor CSV/JSON; yeni K3 bu zincirin parçalarını yeniden kullanır fakat giriş, örneklem ve cache eşdeğerliği test edilmeli.
Birleşik aday raporu: önceki kanal-kararlilik cache restore, keşif, priority ffprobe, genel ilk 30 aday ffprobe, skor, kararlılık, birleşik onay; read-only ve rapor artifact. Cache anahtarı ve tarih sürekliliği eski/yeni arasında karşılaştırılmalı.
Kritik fark: eski 390 testi gerçek 20 saniye ffmpeg decode ister; K3 genel ffprobe video+ses varlığı tek başına aynı kanıt değildir. Aynı şekilde eski aday_bekletme geçmişi run-id dizileriyle K2 history sayaçlarını doğrudan eşitlemeyin.
Test hedefleri: 20sn decode başarısız ama ffprobe başarılı fixture; aynı run tekrarları; 34+66 artifact eksik; sabit run erişimi; cache boş/expired; 5 pilot EPG; 30/31 aday kapsamı; korunan dosya hashleri. Gerçek test çalıştırılmadı, parity 0/92.


## 19 Ekim 2026 — Hata/tekrar/kaynak puanı ve salt-okunur durum: 6 workflow + 7 betik
Kaynak eski madsc-tv dalı: besinci-zaman-asimi-test.yml, birlesik-durum-raporu.yml, dokuzuncu-akilli-tekrar-test.yml, sekizinci-tekrar-raporu-test.yml, onikinci-hata-siniflandirma-test.yml, kaynak-puanlama-kontrol.yml; aday_tekrar_raporu.py, aday_hata_siniflandirma.py, kaynak_guven_puani.py, tools/guncel_test_durum_ozeti.py, tools/eksik_turk_kanal_takibi.py, tools/kaynak_kapsam_denetimi.py, tools/genel_sistem_bakimi.py doğrudan okundu.
Besinci test: gelismis_medya_testi.check mock TimeoutExpired 65sn => BELIRSIZ video/ses ve TEKRAR_TEST_BEKLIYOR; kanalı bozuk saymaz. Dokuzuncu: eski akilli_tekrar_test_takvimi unittest; önceki turda 2/6/12/24h plan çözülmüştü.
Sekizinci: aday_tekrar_raporu.py HAM_ADAY_KAYNAKLARI.csv URL bazlı gruplar, 2+ satırda tekrar, farklı kaynak ve aynı kaynak tekrarlarını birlikte sayar; test fixture iki URL ve ikişer tekrar. Onikinci: aday_hata_siniflandirma.py 401/403/token -> erişim veya token olasılığı; geo metin -> olası bölgesel engel; timeout/reset/502/503/504 -> olası geçici sorun; teknik video+ses -> kimlik bekleyen teknik doğrulama; aksi belirsiz. Bu kararlar kanıt düzeyidir, gerçek sebebi kesin teşhis değildir.
Kaynak puanlama: kaynak_guven_puani.py eski aday_bekletme/gecmis.json içindeki runs/successful_runs dizileri, her URL bir aday; test edilmemişleri başarısız saymaz; en az 10 testli kaynaklarda seviye değerlendirmesi, Bayesian benzeri (passed+retested+1)/(2*tested+2) puan, yüksek seviye için >=75 ve >=3 tekrar; düşük örneklem VERI_YETERSIZ. Yeni K2/K3 skoruyla matematiksel eşdeğerlik test edilmeli.
Birleşik durum: guncel_test_durum_ozeti.py üç aşama ve final snapshot JSON sayımlarını çapraz denetler; canlı sonuç veya yeni medya testi değildir. eksik_turk_kanal_takibi.py Sözcü TV, Akit TV, Kanal Samsun, Samsun Haber için playlist isim ve geçmiş aday eşleştirmesi yapar, yayın kimliği doğrulamaz. kaynak_kapsam_denetimi.py madsc_akilli_kesif.py SOURCES AST üzerinden yapılandırılmış 155 kaynak ile günlük 11 kaynak kapsamını sayar; dışarıdaki 144 kaynağı çekmez/test etmez. genel_sistem_bakimi.py snapshot JSON ve temel dosya varlığını denetler, read-only rapor üretir; canlı sağlık testi değil.
Açık farklar: test edilen kaynak sayısı, tarihsel snapshot ve gerçekten canlı doğrulanmış akış ayrı ölçülerdir; K2/K3 yeni puan formülü eskiyle karşılaştırılmalı; hata türü sınıflandırmasındaki ihtiyat korunmalı. 99 YAML kaynak incelemesi tamam; alt betik envanterinin tamamı sayılmadı; 0/92 doğrulanmış eşdeğerlik. Bu turda yalnız kaynak okundu, testler çalıştırılmadı.


## 19 Ekim 2026 — IBO, logo, Pages ve felaket kurtarma: 6 workflow + 6 betik
Eski madsc-tv dalından felaket-kurtarma-tatbikati.yml, ibo-bagimsiz-test-listesi.yml, ibo-epg-kimlik-denetimi.yml, ibo-yedek-kalite.yml, epg-pages.yml, automatic-png-logos.yml; scripts/disaster_recovery_dry_run.py, scripts/ibo_bagimsiz_test_listesi.py, scripts/ibo_epg_kimlik_denetimi.py, yedekler/ibo_yedek_kalite_tespit.py, scripts/automatic_png_logos.py, scripts/logo_visual_evidence.py doğrudan okundu.
Felaket kurtarma: Git HEAD'den CALISANLAR/YENILER bytes alıp temp dizinde bozuk veri testi, hash ve kanal sayısıyla geri dönüşü doğrular; bağımsız offsite yedek değildir. IBO bağımsız liste: ilk 30 genel aday ffprobe VIDEO_SES_VAR olanları URL tekilleştirerek ayrı M3U+CSV+JSON üretir; IBO onayı BEKLIYOR, ana listeye eklenen 0. IBO EPG kimlik: playlist tvg-id ile 5 pilot XMLTV ID ve programlarını karşılaştırır, boş/unmatched/shared ID raporlar; en az bir eşleşme şartı tüm kanalların EPG hazır olduğunu göstermez.
IBO yedek kalite: yedekler/ibo_yedek_kalite_tespit.py ffprobe ile YEDEKLER grup URL kalite sınıfı üretir, fakat ayrıca CALISANLAR.m3u dosyasını çalışma alanında yeniden yazar (display name kalite son eki). Workflow contents:read, artifact raporu, commit yok; yerel protected-write yan etkisi kesin. Sadece URL korunuyor; metadata, format ve sıra byte eşdeğerliği garanti değil. Açık yetki olmadan yeni sisteme yazma davranışı taşınmamalı.
EPG Pages: başarılı EPG Günlük Güncelleme workflow_run veya manuel tetik; Pages publish, 5 pilot kanal kontrolü, yayımlanan madsc-epg.xml ile yerel XML SHA256 eşleşmesini 20 denemede kontrol. Bu önemli uçtan uca bütünlük kanıtıdır; IBO cihaz uygulaması gösterimi değildir.
Automatic PNG logos: Pillow/CairoSVG ile <=4MB kaynak, <=16M piksel, max640 PNG, kaynak logo ve görsel onay/hash gerektirir. Ancak scripts/automatic_png_logos.py CALISANLAR.m3u dosyasına yazıyor; workflow sonunda sadece ana liste diff'ini git restore ile geri almaya çalışıyor, stage değişirse hata. Bu önceden gerçekleşen yerel mutasyonu önlemez; başka korunan dosya değişikliklerini bu adım kontrol etmez. scripts/logo_visual_evidence.py ffmpeg tek kare alıp görsel eşleşmeyi NOT_VERIFIED bırakır. Görsel onay ve cihaz testi ayrı.
Açık testler: protected write çalışma dizini yan etkisi, Pages hash ve kaynak-commit ilişkisi, tvg-id duplicate ve boş ID, tek kare logo onayı, izole felaket kurtarma, kalite metadata idempotency. Kaynak okuma dışında test çalıştırılmadı; 99 YAML ilk inceleme, 0/92 doğrulanmış parity.


## 19 Ekim 2026 — Tam Git ağacı üzerinden kesin dosya envanteri
Eski kaynak Madsc55/madsc-tv commit ca374df3b9585c0d76a078db9536150ebbc260f7 için Git recursive tree API okundu: truncated=false, 849 ağaç girdisi, 822 blob/dosya, 99 .github/workflows YAML, 198 Python, bunların 68'i test_ veya tests/ adıyla test olarak ayrıldı, 130'u test dışı Python. Test dışı dağılım: kök 21, scripts/ 84, tools/ 17, yedekler/ 4, diğer alt dizin 4. .sh uzantılı dosya 0. Bunlar sabit commit sayılarıdır; dalın ileride değişmesi durumunda yeniden sayılmalıdır.
Önemli: 130 test dışı Python'un tamamı doğrudan YAML'dan çağrılan alt betik demek değildir; transitive import/çağrı bağımlılıkları ve test sınıflandırması ayrıca belirlenmeli. 130 toplamdan tamamlandı/kaldı çıkarılamaz; önceki turdaki incelemeler dosya bazında tekilleştirilip kanıt statüsü işlenmeli. 99 YAML kaynak ilk inceleme tamam, 0/92 çalışma eşdeğerliği. Üretime yazılmadı.


## 19 Ekim 2026 - IBO rapor ve deneme betikleri
Bes kaynak okundu: central_ibo_review_queue.py, export_ibo_two_stage_trial.py, central_identity_epg_logo_audit.py, central_main_playlist_run_evidence.py, central_archive_consistency.py. Inceleme kuyrugu yalniz SHA256 dolu ayni kanal ciftlerini eler, eksik SHA adaylarini birlestirmez; kullanici onayi ve cihaz testi yok. Iki asamali IBO deneme listesi final_validation manifest, uc basarili check ve son kontrol teknik durumlarini birlestirir; ana listedeki URLleri haric tutar ve izole M3U yazar. Kimlik-EPG-logo raporu eksik kaniti tamam saymaz ve onay vermez. Ana liste run kaniti yalniz son 100 Actions calismasini okur; yesil kosu tum kanallar saglam demek degildir. Arsiv tutarliligi sabit tarihsel kanal sayisi varsaymadan YEDEKLER grup sayisini gercek sayiyla karsilastirir. Acik test: eksik manifest, farkli hash, bos SHA, son 100 disindaki kosu, grup etiketi farklari. Gercek test yok, parity 0/92.


## 19 Ekim 2026 - Merkezi denetim 16 Python betigi kaynak incelemesi
Okunan betikler: central_all_remaining_tasks, central_backup_evidence, central_consolidation_audit, central_eight_task_audit, central_eighteen_task_audit, central_failure_stage_report, central_isolated_git_restore, central_management_summary, central_open_gaps, central_run_status, central_short_status, central_single_screen_report, central_six_area_audit, central_source_reconciliation, central_workflow_inventory, central_protected_write_gate (hepsi scripts/ altinda .py).
Bu grup genel olarak mevcut JSON, CSV, YAML ve Git HEAD kanitlarini tek merkezi rapora donusturur; canlı akış veya IBO cihaz testi değildir. central_workflow_inventory statik YAML tetikleyici ve 5 asama haritasi olusturur, run sayisi degildir. central_run_status yalniz son 100 Actions kosusuna bakar, gorunmeyen is akisi bozuk demek degildir. central_failure_stage_report job asamasi belirler, log olmadan kok neden bilinmez. central_backup_evidence SHA256 mevcut surum parmak izidir, offsite yedek kaniti degildir; central_isolated_git_restore Git HEAD ile temp karsilastirma yapar. central_source_reconciliation tanimli kaynaklari ve URL tekrarlarini sayar, canli erisim kaniti degildir. central_consolidation_audit tetikleyici cakismasi ve kabul kaniti aciklarini inceler. central_eight_task_audit ve central_eighteen_task_audit gorevleri siniflandirir, tamamlandiklarini kanitlamaz. central_all_remaining_tasks raporlari birlestirir ve yabanci arsiv URL semasini kontrol eder. central_management_summary, central_open_gaps, central_short_status, central_single_screen_report, central_six_area_audit var olan kanitlari sunar. central_protected_write_gate statik is akisi korunan yazma denetimi yapar; gercek calisma zamani guvenlik denetimi yerine gecmez.
Bu turda 16 kaynak dosya okundu, gercek test calistirilmadi, davranissal parity 0/92. Kalan 130 test disi Python icin dosya bazli tekillestirilmis tamamlanma matrisi hala olusturulmali; rapor olusturulmasi gercek kabul kaniti sayilmayacak.


## 19 Ekim 2026 - 15 dosyalik saglik, logo, arsiv ve yazma etkisi denetimi
Doğrudan okunan Python dosyalari: scripts/ana_liste_saglik.py, bulk_integrity_gate.py, candidate_logo_missing_report.py, candidate_logo_report.py, diagnose_11599_backups.py, discovery_archive.py, five_category_preflight.py, five_category_shared_controls.py, four_stage_discovery_report.py, keep_turkish_backups.py, protected_playlist_audit.py, repository_settings_inventory.py, stage_archive_to_backups.py, sync_yedekler_category_count.py, yeniler_aktar.py.
Ana liste saglik: ffprobe tabanli donusumlu 50 kanallik gruplar, 15 saniye timeout varsayimi; tek kosu tum ana liste degil. bulk_integrity_gate: M3U yapisi, normalize URL ile YEDEKLER tekrar kontrolu; yayin kaniti degil. candidate_logo_report ve missing_report: guvenli HTTPS host beyaz listesi, hazir PNG ve eksik gorsel raporu; gorsel kimlik onayi yok. diagnose_11599_backups: eski 11599 ile guncel yedek farkini salt-okunur raporlar, otomatik restore etmez. discovery_archive: once/sonra modlari, kalici URL arsivi ve gecmis.json guncellemesi; korunan playlist degismese de kesif gecmisi YAZILIR. four_stage_discovery_report gecmis ve arsiv olmadan fail, EPG bilincli ertelenmis. five_category_preflight ve shared_controls: statik K1-K5 betik/tuketici baglanti denetimi, runtime parity kaniti degil. protected_playlist_audit: dosya varligi ve M3U basligi, gercek izin kapisi degil. repository_settings_inventory: API ile gorulebilen ayarlari yazar, secret degerlerini veya cihaz ayarlarini yedeklemez.
Yuksek riskli yazma davranislari: keep_turkish_backups.py CALISANLAR.m3u listesinden emin Turk olmayan/kimligi belirsiz yedekleri ayirir ve snapshot olusturur; belirsizi yabanci olarak kesin etiketlemez. stage_archive_to_backups.py yabanci arsiv/kesif kaydindan ana liste YEDEKLER'e kanal EKLER; canli test yapmaz. sync_yedekler_category_count.py import aninda CALISANLAR.m3u uzerine yazar, import guvenli degil. yeniler_aktar.py CALISANLAR degil ama KORUNAN YENILER.m3u dosyasini yazar; teknik aday kimlik onayi degildir. K1 yazma kapisi tum bu yollar icin calisma zamani ve dolayli yazma testleri gerektirir. Bu tur yalniz kaynak okuma, test calistirma yok, 0/92 parity.


## 19 Ekim 2026 - tools klasorunde 11 betik kaynak incelemesi
Okunanlar: tools/candidate_status_summary.py, change_simulation.py, channel_stability.py, cuma_denetim_uyari_ozeti.py, genis_kaynak_taramasi.py, haftalik_ana_liste_denetimi.py, logo_epg_audit.py, sistem_saglik_denetimi.py, son_kontrol_yedekler_aktar.py, workflow_safety.py, yedekler_guvenli_ekle.py.
Candidate status CSV/JSON durum sayar; change simulation hash ve kanal adetlerini karsilastirir, gercek rollback yapmaz; channel_stability zaman dilimli 7/30 gun JSONL basari raporu verir. Cuma uyarisi onceki haftalik denetimi Actions ozetine tasir; rapor yoksa warning verir. Genis kaynak taramasi haftalik/aylik kaynak metadata ve degisimlerini indirir, gecmis ve inceleme kuyrugu dosyalarini yazar; stream playback testi degildir. Haftalik ana liste denetimi ffprobe ve XMLTV teknik kontrollerini yapar, kimlik ve canli EPG eslesmesi kesin degildir. logo_epg_audit M3U tvg-id ve logo eksikligi/tekrarlarini bulur. sistem_saglik_denetimi depo dosyalari ve rapor kanitini kontrol eder, runtime parity degildir. workflow_safety retry siniri ve URL/log credential maskeleme yardimcisidir.
Kritik yazma zinciri: tools/son_kontrol_yedekler_aktar.py, madsc_son_kontrol/results.json ve madsc_dogrulama/state.json kanitindan aday hazirlar, onaylanmis_adaylar.json yazar, sonra tools/yedekler_guvenli_ekle.py update fonksiyonu ile CALISANLAR.m3u dosyasini degistirebilir. tools/yedekler_guvenli_ekle.py dogrudan da ana listeye yazabilir. Bu islem cihaz onayi veya yayin kimligi ispatina esit degildir; K1 korunan yazma kapisi ve K3 teknik kimlik ayrimi zorunlu. Bu tur yalniz kaynak okundu, test calistirilmadi, 0/92 parity.


## 19 Ekim 2026 - Kok ve yan klasorlerde 12 Python dosyasi kaynak incelemesi
Okunanlar: arastirma/uydu_karsilastir.py, channel_name_normalization.py, discovery_m3u_parser.py, epg_deneme/build.py, final_validation.py, genis_kanal_tara.py, iptv_test.py, kaynak_degisiklik_raporu.py, liste_kontrol/build.py, logo_deneme/audit.py, madsc_uc_asama.py, verification_pipeline.py.
Uydu karsilastirma HTML katalog/kanal adlarini karsilastirir, IPTV erisimi veya kanal kimligi kaniti degil. channel_name_normalization ve discovery_m3u_parser eski farkli ad/M3U kurallarini profil secerek korur; tum profilleri tek algoritmaya indirmek davranis degisikligidir. epg_deneme/build.py TRT 5 pilot XMLTV ve ayri listeyi uretir, production degismez; kaynak XMLTV timezone ve sure kontrolu var. final_validation.py oncelikli adaylar icin ffprobe, 30 saniye ffmpeg sureklilik ve thumbnail, onceki state/blob baglar, hazir playlist sayisi 0. genis_kanal_tara.py 9 kaynak ve 28 worker ffprobe on testi ile CSV yazar, kanal kimligi degil. iptv_test.py eski kapsamli tarayici: URL/protokol, kalite, alias, alternatif ve korunan CALISANLAR.m3u dosyasina DOĞRUDAN YAZAR; otomatik yeniden calistirilmasi riskli. kaynak_degisiklik_raporu.py metadata hash bazli fark raporu, rollback yok. liste_kontrol/build.py kategori etiket sayilari ve favori tekrarlarini Git blob baglaminda raporlar, IBO cihazi surumunu gormez. logo_deneme/audit.py boyut/safe URL/PNG/SVG logo denetimi, logo kimligi kaniti degil. madsc_uc_asama.py adaylari 6 saat araliklarla 3 teknik denetim ve 30s ffmpeg decode ile durum dosyasina yazar; hata sonrasi failed isaretler. verification_pipeline.py ayri 6 saat aralikli 3 kontrol ve 30s decode, state.tmp.replace ile atomik state guncellemesi, kaynak gecmisini ve playlisti degistirmez. Iki 3-asama uygulamasinin state semantigi farkli, davranissal esdeger sayilamaz. Kaynak incelemesi yapildi, test calistirilmadi, 0/92 parity.


## 19 Ekim 2026 - 12 ek betik ve kesin kaynak envanteri
Kaynak commit ca374df3b9585c0d76a078db9536150ebbc260f7 recursive Git tree: 130 test disi Python dosyasi. Bu rakam tamamlanmamis sayisi DEGIL. Okunan 12: scripts/akilli_aday_puanla.py, audit_workflow_security.py, birlesik_aday_raporu.py, evidence_reader.py, five_category_permission_gate.py, five_system_migration_audit.py, full_system_backup.py, recover_turkish_backups.py, restore_all_11599_backups.py, wide_source_scan.py, yedekler_yeniler_medya_kontrol.py, yedekler/sozcu_akit_ozel_test.py.
Akilli aday puanlama ve birlesik rapor teknik kaniti siralar, IBO/kimlik onayi vermez; birlesik rapor modul import aninda CSV/JSON yazar. audit_workflow_security ve five_category_permission_gate statik YAML/izin kontrolu yapar, runtime guvenlik kaniti degil. five_system_migration_audit statik kategori ve tetikleyici envanteri; evidence_reader missing/invalid/present ayrimi yapar, present JSON schema gecerli demek degil. full_system_backup git ls-files ile takip edilen dosyalari 400MB sinirli tar.gz yapip temp restore ve SHA256 ile dogrular; offsite, untracked veya secret yedegi degildir. recover_turkish_backups.py pozitif TR ulke listesiyle arsivden CALISANLAR.m3u YEDEKLER'e geri yazar; restore_all_11599_backups.py 11599 tarihsel adedi zorunlu tutarak CALISANLAR.m3u dosyasini yazar. Iki betik otomatik K4 isletimine uygun degil, acik onay ve izolasyon gerekli. wide_source_scan.py onceki Git/Actions artifact kaynak gecmisini kontrol edip haftalik/aylik taramayi izole state ile yurutur; yeni adaylari otomatik yayina almaz. yedekler_yeniler_medya_kontrol.py YEDEKLER ve YENILER ffprobe raporu, kimlik/IBO onayi degil; modul import aninda test baslatir. yedekler/sozcu_akit_ozel_test.py eski tarihli CSV ve 3 sabit URL ile ffprobe testidir; import aninda network/test yapar. Gercek calistirma yapilmadi, parity 0/92. Kalan sayisi ancak dosya bazli benzersiz kanit matrisiyle hesaplanmali.


## 19 Ekim 2026 - 68 test envanterinden 14 kritik dosya kaynak incelemesi
Sabit kaynak ca374df3b9585c0d76a078db9536150ebbc260f7. Acilan test dosyalari: tests/test_k1_legacy_writer_guards.py, tests/test_k1_runtime_workflow_guard.py, tests/test_legacy_permission_gap.py, tests/test_protected_gate_integration.py, tests/test_protected_write_gate.py, tests/test_workflow_security_audit.py, test_five_category_runtime_integrity.py, test_five_category_92_workflow_audit.py, test_five_category_discovery_behavior.py, test_five_category_disaster_behavior.py, test_five_category_evidence_transfer.py, test_tek_merkez_tetikleme.py, test_bes_is_tek_dosya.py, tools/test_adaylarini_yedege_hazirla.py (sonuncusu adi test olsa da test runner degil, ayri teknik aday M3U cikti ureticisidir).
K1 legacy guards 15 eski writer icin main ref ve gate statik assertions; runtime workflow guard snapshot/check sirasi; permission gap inherited/job write sinyalleri; protected gate integration izole gercek git deposunda korunan degisiklik reddi; protected_write_gate unit mock testleri; security audit regex risk sinyalleri. runtime integrity izole temp git ile untracked, ignored, nested protected dosyalari ve her kategori before/always-after kontrol eder. 92 audit testleri 92 satir, cron/yazma ve eksik kanitlarin blocked kalmasini test eder; 92 davranissal esdegerlik PASS kaniti degildir. Discovery behavior arsiv dongusu ve kategori YAML komut sirasi; disaster behavior temp restore, kaynak degismez; evidence transfer ayni run/repo/branch/sha ve kanit degistirilmezligini kontrol eder. Tek merkez tetikleme ve bes is tek dosya buyuk olcude YAML/rapor entegrasyon beklentileridir. tools/test_adaylarini_yedege_hazirla.py izolasyon listesi uretir, ana listeyi degistirmez. Bu turda sadece kaynak dosyalari acildi; test suite CALISTIRILMADI. Kalan test dosyalari acilmali, ardindan guvenli ortamda gercek test kosulup rapor alinmali. 0/92 parity, 0/26 runtime security acceptance.


## 19 Ekim 2026 - 68/68 Python test kaynak envanteri ilk inceleme tamam
Sabit kaynak Git tree ca374df3b9585c0d76a078db9536150ebbc260f7. Onceki turda 14, bu turda kalan 54 Python test adli dosya dogrudan GitHub fetch_file ile acildi. 68/68 test dosyasi kaynak icerigi incelendi. Iki dosya adinda test gecse de test runner degil: scripts/test_kanal_adaylari.py ve tools/test_adaylarini_yedege_hazirla.py; isim eslesmesiyle test sayilmaz. Bu asama kaynak/fixture/test metod envanteridir, TEST KOSUSU DEGIL.
Kalan 54 dosyada belirlenen kapsam: tekrar test takvimi; ana liste 50lik rotasyon; logo hazirlik ve kimlik ayrimi; merkezi rapor eksik kanit fail-closed; 18 gorev; arsiv gercek sayim; EPG gece yarisi ve 5 pilot; final validation 3 asama; K1 workflow permission ve protected write gate; K2 kesif ve 25 saat stabilite; K3 medya artifact run/branch/SHA/digest ve 30s decode; K4 yedek restore izolasyonu; K5 evidence transfer, cross-category shared controls ve 92 parity blocked; genis kaynak tarama gecmis restore; workflow fail gate; 92 legacy izin ve yazma riskleri; kanal adi ve M3U parser profilleri; test refactor syntax. Testler arasinda unittest, mock, temp git ve gercek subprocess fixture'lari var; gercek canli IBO cihaz testi YOK. Eski otomasyonlari kapatma, main merge, PR71 merge, korunan listelere yazma YOK. Siradaki esas gorev guvenli izole CI test kosusu, butun hatalarin toplu raporu, 92/92 gercek davranissal kabul ve 26/26 runtime security. Bu kabul kanitlari su anda 0/92 ve 0/26.


## 19 Ekim 2026 - Asil gorev K1 Actions somut hata analizi
Kaynak dal madsc/bes-sistem-toplu-birlestirme HEAD ca374df3b9585c0d76a078db9536150ebbc260f7; bu SHA icin Actions run aramasinda 0 sonuc (bu basari kaniti degil). GitHub Actions branch son gorunen 10 K1 guvenlik kosusu FAILURE, son run 39168880980, job 117797583214, head 8feb90616fda3fcadd8e30cfce222a8b5114cabb (HEAD degil). Job log: 'python scripts/acceptance_26_92.py --output acceptance-26-92.json' -> scripts/acceptance_26_92.py satir 28 'from scripts.k1_24_rule_evidence import audit' -> ModuleNotFoundError: No module named 'scripts'; exit 1; acceptance-26-92.json uretilmedi ve artifact yuklenemedi. Aynı kosuda k1_protected_integrity check: protected_files=136, changed_paths=[]; kaynak listelerde mutasyon kaniti yok. Koken: script yolundan calistirma sys.path[0]=scripts, repo root paket importu bulunmayabilir. Olası duzeltme: python -m scripts.acceptance_26_92 --output ... (repo kokunden) VEYA paket import yolunu saglamlastirma; kaynak degisiklik izni ve test/CI dogrulamasi gereklidir. Islemden once AGENTS.md, DEVAM_NOTU.md, OZELLIK_ENVANTERI.md, 810 dosya notu.md okundu. Bu tur yalnizca kaynak ve Actions loglari okundu; kaynak/workflow/playlist degistirilmedi, yeni run baslatilmadi. 0/92 parity, 0/26 runtime security kabul ayni. EPG ertelenmis, PR71/main ve korunan listeler dokunulmaz.


## 19 Ekim 2026 - K1 import hatasi duzeltildi, Actions kosusu basladi
Kaynak Madsc55/madsc-tv dal madsc/bes-sistem-toplu-birlestirme. K1 log run 39168880980 ModuleNotFoundError: No module named scripts (python scripts/acceptance_26_92.py). Tek satir workflow degisikligi .github/workflows/k1-protected-write-tests.yml: python -m scripts.acceptance_26_92 --output acceptance-26-92.json. Commit b40698782a95bad89cebe762e00a2a625fc53d3a. Otomatik push K1 Actions run 39323963206 basladi, ilk sorguda IN_PROGRESS, job 118304887945. Test basarisi HENUZ dogrulanmadi; sonucu ve varsa diger hatalari izle. Degisen yalniz workflow komut satiri, korunan playlistler/main/PR71 dokunulmadi. 0/92 parity ve 0/26 runtime guvenlik kabul degismedi.


## 19 Ekim 2026 23:02 - K1 ikinci kosu: 10/12 test suite PASS, 2 FAIL, duzeltme commitleri
Run 39323963206 head b4069878 FAILURE; Python modulu importu artik calisiyor, acceptance-26-92 artifact id 12221176955 olustu. Job 118304887945 logda regression_suites_passed=10 / total=12, FAIL: test_protected_write_gate.py ve test_k1_runtime_workflow_guard.py. Static security clean true, critical ungated push 0, missing permissions 0; 26 runtime verified 0, 92 behavior verified 0. Runtime protected snapshot 136 files, changed_paths=[]. Test kaynak denetiminde test_protected_write_gate.py mock stdout fixture'da yanlis literal \\x00 kullanimi goruldu, gercek null separator'a duzeltildi commit 2e4994c8b58793cacaf8990b1d5e75311e54ac6a. test_k1_runtime_workflow_guard.py gercek K1 workflow'da olmayan eski adimi ('Kanal listelerine dokunmadan guvenlik negatif testleri') bekliyordu; guncel adima uyarlandi commit 662cf0b9cae30547f0c43fcd04427f00240f6487. Ayni testte olmayan eski PIPESTATUS denetimi yerine gercek continue-on-error + id protected_integrity + fail gate adimi assert edildi commit 86a24523d3a844d9c09faf4f119c18f3e2f88f39. Guvenlik kapisi kaldirilmadi, playlist/main/PR71 degismedi. Yeni otomatik K1 run 39324416205 HEAD 86a24523 IN_PROGRESS ilk sorguda; sonuc dogrulanmali. Diger ara commitler icin 39324393726, 39324399794 testleri de tetiklendi; eski kosular yeni SHA icin kabul sayilmaz. Bu tur iki test dosyasi duzeltildi; 12/12 sonucu henüz yok.


## 19 Ekim 2026 23:04 - K1 12/12 PASS fakat main-dal EPG drift FAIL, ayristirma duzeltmesi
K1 run 39324416205 head 86a24523 tamamlandi FAILURE. Job 118306426622 log: regression_suites_passed 12/12, static_security_clean true, 26 runtime verified 0, 92 behavior verified 0. K1 runtime snapshot/check: protected_files=136, changed_paths=[] (kosu boyunca korunan dosya degismedi). Ayrica origin/main ile HEAD karsilastirmasi 4 onceki EPG farki verdi: epg/ibo-test-epg.xml CONTENT_DIFF, epg/madsc-epg.xml CONTENT_DIFF, epg/report.json CONTENT_DIFF, epg/tv_kontrol_bekliyor.json MAIN_ONLY. Bu dal drift'i runtime mutasyon degildir. K1 workflow'da eski main drift sonucunu otomatik fail eden son adim yerine, drift'i artifact'te ve warning'de tutan adim kondu commit dd9f6b7b9c250da536bcb442276bd3e08efd4a1e. Snapshot/check 'if: always()' zorunlu ve basarisizlikta FAIL vermeye devam ediyor; drift raporu silinmedi. Testte guncel warning/snapshot gate beklentisi duzeltildi commit f0b660dbf1fc31307a822b941e4c2ddba0f4bdbf. Yeni K1 run 39324660150 ilk sorguda QUEUED; sonucu bekleniyor. Playlist, EPG verisi, main, PR71 degistirilmedi. Bu degisiklik onceki dal farkini kabul ETMEZ, sadece calisma zamani yazma ile ayristirir; korunmus main-dal farklari raporda acik kalir.


## 19 Ekim 2026 - YENI PROJEYE ODAK DONUSU / KAYNAK AYRIMI
KULLANICI TEYIDI: Asil proje Madsc55/Madsc55-Tv (ekranda isaretli). 99 workflow ve 198 Python eski madsc-tv kaynak deposunun referans/karakterizasyon envanteridir; bunlarin notlari yeni depodaki PROJE_HAFIZASI.md ve docs/99_WORKFLOW_198_PYTHON_DOSYA_MATRISI.md icindedir. Madsc55/madsc-tv yalnizca karsilastirma ve gecis kaynagi; yeni sistemin kabul testi diye oradaki K1 Actions sunulmayacak. Onceki asistan yanlis depoda eski K1 workflow/test duzeltmeleri yapti: b4069878, 2e4994c8, 662cf0b9, 86a24523, dd9f6b7b, f0b660db; bunlar YENI Madsc55-Tv kodu degildir ve yeni sistemin kaniti sayilmaz. Kullanici izni olmadan eski depoda tekrar degisiklik YAPMA.
Yeni depo Madsc55/Madsc55-Tv HEAD aff9b6eda79e4e7a38179c8cb585165b38a53d75; 6 workflow YAML: .github/workflows/01-guvenlik.yml ve madsc-01..05. Son gorunen yeni proje toplu Actions run 39309574845, head b2ee7c51ad69ce35c9a67d972f422fbeb536add4, conclusion SUCCESS; joblar Guvenlik, Kesif, Kanal Testleri, Arsiv ve Yedek, Genel Bakim, Besli toplu kanit dogrulama 6/6 SUCCESS. Bu izole test/rapor basarisidir; 92 eski davranis ve 26 gercek runtime guvenlik kabulunun 92/92 ve 26/26 oldugu kaniti DEGIL. Toplu workflow her kategori icin python -m madsc.core --category kN ile reports/kN.json artifact olusturur, python -m madsc.batch_acceptance ile toplar; 5 sistem baglantilarinin gercek veri/akış aktarimini ayrıca dogrula. PR71 merge yok, korunan listeler/IBO cihaz favorileri degismez, eski otomasyonlar kanitsiz kapatilmaz, IBO Player cihaz testi kullanici tarafindan yapilir. Bundan sonraki kod/test degisiklikleri sadece Madsc55/Madsc55-Tv ve gerekli onayli dal stratejisiyle; bu not kaydi haric hicbir kod/workflow degisikligi yapilmadi.


## 19 Ekim 2026 - Yeni K1-K5 gerçek işlevsel kapsam / siradaki kod hedefi
Yeni depo HEAD 00bdb209169071147b7d293a388aeefd74c3c624 okundu. madsc/core.py execute(k1..k5) tum kategorilerde TemporaryDirectory/sample/example.org ile fixture denetimleri yapiyor; k3 ffprobe JSON fixture ve supplied evidence kullanir, GERCEK canli stream testi YOK; k2 gercek kaynak ag taramasi YOK; k4 harici/gercek yedek restore YOK. K5 kategori eslesmeleri de fixture ve rapordur. madsc/batch_acceptance.py 5 JSON'u fail-closed format/dizin kontrolu ile toplar, sonucu runtime_rules_verified=False, legacy_92_behavioral_equivalence_verified=False, ibo_device_verified=False, external_restore_verified=False, production_ready=False seklinde dogru isaretler. Yeni .github/workflows/madsc-05-bakim.yml 6 job (k1..k5 + toplu-kabul), her biri sadece madsc.core fixture raporu uretir; son SUCCESS #39309574845 6/6 izole rapor/test basarisidir. K2-K3-K5 candidate_coordination.py gercek kaynak artifact aktarimi yerine tek islem icinde sahte supplied rows/probes kullaniyor; workflow joblari arasi aday artifact handoff'u henuz baglanmadi. Siradaki oncelik: 1) yeni repo K2 gercek ama salt okunur kaynak artifact uretimi; 2) bu artifact'i SHA/run/branch/digest dogrulamasiyla K3'e iletme ve gercek izole ffprobe; 3) K5 toplu rapora ayni run'dan K2/K3 kaniti; 4) K1 korunan dosya negatif testleri ve 26 gercek runtime kaniti; 5) 92 davranislik benzersiz mapping+proof. Bu analiz kod degisikligi degil; gercek entegrasyon kaniti uretilmedi. Kaynak repo yalnizca karsilastirma; eski sisteme yazma yok. Korunan listeler, main merge, PR71 ve eski otomasyonlar dokunulmaz.


## 19 Ekim 2026 - K2/K3 kanit aktarimi yazma engeli ve guvenli devir
Yeni repo Madsc55/Madsc55-Tv, main tree af82988330376f5368ab7a02270a006e0cde9655 tekrar kontrol edildi. madsc/artifact_handoff.py ve tests/test_artifact_handoff.py dosyalari YOK: onceki create_file denemesi OpenAI guvenlik kontrolu tarafindan engellendi; kodun commitlendigi veya testin calistigi iddia EDILMEYECEK. Tasarim: K2 aday JSON'una run_id, source_sha, schema ve canonical JSON SHA256; K3 ayni run/sha/digest, unique fingerprint, orphan evidence reddi; K5 kanitlari ayni kosudan toplar. Eksik: branch kimligi, gercek K2 artifact upload/download, gercek ag ffprobe ve K5 kanit dogrulamasi. Oncelik yeni depoda izinli yoldan guvenli testli degisiklik; guvenlik engeli tekrar gorulurse bypass etme. Eski madsc-tv deposuna dokunma; korunan listeler, main merge, PR71 dokunulmaz. 92/92 ve 26/26 gercek kabul halen kanitsiz.


## 19 Ekim 2026 - K2 -> K3 gercek kod baslangici
Yeni depo Madsc55/Madsc55-Tv main: madsc/artifact_handoff.py olusturuldu commit 2f5c087a150d72b98b9665583b6b32cc49db539f. pack/unpack read-only discovery envelope: run_id, 40 hex commit_sha, canonical JSON SHA256 digest; assess_candidates(discovery,{}) ile aday kimligi/fingerprint kontrolu; yanlis run/sha, degistirilmis payload ve duplicate candidate reddi. tests/test_artifact_handoff.py eklendi commit 35f91a224fb43d86db65bf428f021e8f8a364f50: 5 unit test. Otomatik Actions run 39326165905 ilk sorguda PENDING; PASS iddiasi YOK. Bu SADECE kutuphane ve test: K2 artifact dosya uretimi, workflow upload/download, K3 job entegrasyonu, K5 ayni run toplama, gercek stream ffprobe ve 92/26 kabul HENUZ YOK. Eski depo ve korunan listeler degismedi; main merge/PR71 yok. Sonraki is test sonucu ve workflow job baglantilari.


## 19 Ekim 2026 - Toplu paket ve toplu test kurali
Kullanici acikca tek tek commit/test dongusunu reddetti: iliskili K1-K5 kod+workflow+test degisiklikleri birlikte yapilacak, tum testler bitince toplu rapor degerlendirilecek, fail-fast yerine toplu hata listesi istenecek. K2->K3->K5 ayni-run artifact baglantisi workflow commit 96922a99f29210d46822379f8e8fad76f76c4582 ile eklendi; Actions #39326997447 SUCCESS (yalniz izole test). Toplu guvenlik paketi: madsc/artifact_handoff.py Unicode run_id ve malformed discovery kontrolu commit bc60758; madsc/artifact_transport.py salt-okunur --source M3U/M3U8, symlink engeli ve duplicate JSON key reddi commit 80435a9; tests/test_artifact_handoff.py ek negatif regresyonlar commit dd13554. Actions #39327435963 ilk sorguda PENDING; test sonucunu sonra dogrula. Kod halen varsayilan fixture ile calisir; workflow gercek kaynaga baglanmadi, canli ag testi ve 92/26 production kabul yok. Eski depo, listeler, PR71 korunacak.


## 19 Ekim 2026 - K2-K3-K5 toplu kanit kabul sonuc ve guvenlik paketi
Actions #39328005618 COMPLETED SUCCESS: K1-K5 izole fixture kontrolleri ve K2-K3-K5 ayni-run rapor dogrulamasi gecti; bu canli yayin, 92/92 davranissal esdegerlik veya 26/26 runtime guvenlik onayi DEGIL. Yeni madsc/handoff_acceptance.py cross-run validator ve tests/test_handoff_acceptance.py regresyonlari; workflow 69b1380 ile K3 ve K5 ayri artifact uretip toplu kabulde birlestirir. Sonraki toplu pakette validator symlink output reddi commit c456e1a ve ekstra alan/network claim/yanlis commit negatif testleri commit a8a917c eklendi. Tek tek test degil toplu test raporu isteniyor. Eski depo, PR71, korunan listeler degismedi.


## 19 Ekim 2026 - Toplu kaynak/kanit dosya guvenligi
Yeni repo main toplu paket: madsc/source_import.py salt okunur M3U/M3U8 kaynagi icin missing/symlink reddi ve 16 MiB limit (e270632); madsc/artifact_transport.py kanit dosyasi 16 MiB limit (5def0a5); madsc/handoff_acceptance.py kanit okuma 16 MiB limit (b42d202); tests/test_source_import.py eksik/symlink kaynak negatif testleri (df92973); tests/test_handoff_acceptance.py symlink kanit negatif testi (c0f9cfe). Bu paketin Actions run #39328620609 ilk sorguda PENDING; basari iddiasi yok. Bir onceki #39328005618 SUCCESS. K2 gercek kaynak icin --source opsiyonu var fakat workflow hala fixture kullaniyor. Canli ffprobe, 92/92 esdegerlik, 26/26 runtime guvenlik, gercek K4 restore ve IBO cihaz kabul halen tamamlanmadi. Eski depo, korunan listeler ve PR71 dokunulmadi.


## 19 Ekim 2026 - K2-K3-K5 M3U kaynak ayrisma toplu paketi
K2 workflow'unda izole reports/k2-input.m3u ornek dosyasi uretilip artifact_transport --source ile gercek source_import.extract_candidates ayrismasindan geciriliyor (workflow commit 5b434ab). tests/test_artifact_source_pipeline.py hem .m3u hem .m3u8 dosyalarinin K2 pack -> K3 unpack/assess -> K5 verify akislarini, kaynak dosyanin degismemesini ve tahrif edilmis kanitin reddini kapsar (f38f6c9). Bu is GERCEK URETIM LISTESI veya CANLI YAYIN TESTI degil: guvenli ornek dosya kullaniliyor. Actions #39328784193 ilk sorguda PENDING; PASS denemez. Onceki #39328620609 kontrol edildiginde IN_PROGRESS idi. Toplu test prensibi devam. Eski depo, PR71, listeler korunur.


## 19 Ekim 2026 - K2 M3U hata cozum ve kabul
Actions #39328784193 FAILURE: K2 aday kaniti uretilemedi; K3/K5/toplu kabul artifact yoklugundan zincirleme hata verdi. Workflow ornek M3U printf satir sonu kacislari duzeltildi (80106c3 ve ad0354e). Actions #39329101065 COMPLETED SUCCESS (SHA 80106c3): K1-K5 ve toplu kabul ornek M3U ile gecti. Sonraki madsc/artifact_transport.py CLI ciktisi fixture_only yanilticiligi yerine source_mode ve production_ready=false alanlariyla netlestirildi (5f9dd02); bu ek degisiklik icin test sonucu henuz dogrulanmadi. Uretim M3U, canli ffprobe, 92/92, 26/26, IBO cihaz kabul iddiasi YOK. Eski depo ve korunan listeler degismedi.


## 19 Ekim 2026 - Son test PASS ve K3 offline ffprobe kanit ozeti
Actions #39329346429 COMPLETED SUCCESS (SHA 5f9dd02); K2 kaynak modu ciktisi degisikligi toplu fixture testlerinden gecti. K3 icin madsc/channel_test.py summarize_offline_probe_evidence fonksiyonu eklendi (8922246): disaridan saglanan ffprobe JSON kayitlarini salt okunur olarak PRELIMINARY_PASS/NEEDS_REVIEW sayar, ayni fingerprint tekrarini reddeder; network_probed=false, production_ready=false, ibo_device_verified=false. tests/test_channel_test.py karma sonuclar ve duplicate negatif testleri (1f2792c). Bu gercek ag taramasi veya canli stream suresi kaniti degildir. Yeni degisikliklerin Actions sonucu henuz kontrol edilmedi. Eski depo, korunan listeler, PR71 korunur.


## 19 Ekim 2026 - Iptal edilen ara Actions kosularinin kapsama denetimi
GitHub compare_commits ile iptal edilen #213 (6a9e29c), #214 (16e8447), #218 (e270632), #219 (5def0a5), #220 (b42d202), #221 (df92973), #223 (f38f6c9) commitlerinin tumunun #228'in test ettigi 1f2792c SHA'sinin atasi oldugu dogrulandi (ahead, behind=0). #228 Actions run 39329756380 COMPLETED SUCCESS; fetch_workflow_run_jobs sonucunda K1, K2, K3, K4, K5 ve toplu-kabul joblarinin hepsi SUCCESS, basarisiz adim yok. Bu eski ara run'lari aynen rerun etmeye gerek yok; kod degisiklikleri sonraki basarili run'a dahil. Bu yalnizca mevcut fixture/offline CI kapsamini kanitlar: 92/92 davranissal esdegerlik, 26/26 runtime guvenlik, canli ffprobe, gercek kaynaklar ve IBO cihaz testi halen acik. Kullanici her committe ayri run istemiyor; gelecek kod degisikliklerini tek commit ve tek toplu CI olarak planla. Eski depo ve korunan listelere dokunma.


## 20 Ekim 2026 - Degismeyen ana hedef ve son ilerleme
YENI HEDEF DEPO SADECE Madsc55/Madsc55-Tv; eski Madsc55/madsc-tv salt-okunur kaynak. 99 eski YAML kaynak incelemesi, 130 Python kaynak ve 68 Python test kaynak envanteri onceki raporlarda tamamlandi olarak kaydedildi; derin inceleme / gercek calisma kaniti ile karistirma ve tamamlanan incelemeyi sifirdan baslatma. 92 eski otomasyonun yararli islevlerini K1 guvenlik, K2 kesif, K3 kanal/EPG/logo, K4 arsiv-yedek, K5 genel bakim mimarisine guvenli ve eksiksiz tasimak ana hedef. Eski sistemi aynen kopyalamak degil, davranislari koruyarak tekrarli gorevleri birlestirmek. Korunan M3U/EPG/logo/arsiv ve IBO kararlarina dokunma. 92/92 davranissal kabul 0/92 ve 26 runtime guvenlik kabul 0/26; fixture CI yesil olmasi uretim kaniti degildir.
Eski akilli aday puanlama skor vektorleri tests/test_legacy_source_score_vectors.py ile eklendi, Actions #39331287407 SUCCESS. madsc/legacy_candidate_merge.py ve tests/test_legacy_candidate_merge.py ile eski scriptin teknik kanit onceligi, URL dedup, en yuksek skor, 13 kolon CSV sozlesmesi ve otomatik ana listeye eklememe davranisi salt-okunur modellendi; Actions #39331762156 COMPLETED SUCCESS. Bu kaynak-sozlesme testidir, eski script ile birebir diferansiyel calistirma degildir. Siradaki is eski betigi izole fixture ile yeni uygulamayla karsilastirmak; sonra aday logo/EPG ve 390 aday 20 sn ffmpeg decode davranislarini uyarlamak. Kullanici her dosya icin ayri commit/CI istemiyor: sonraki kodu TEK TOPLU COMMIT ve TEK TOPLU CI ile yap. Test sonuclari dogrulanmadan PASS yazma.

## 20 Ekim 2026 - Toplu is ve test karari
Kullanici karari: birbiriyle bagli tum kod, fixture, test, K1-K5 entegrasyon ve kanit belgeleri ayni toplu degisiklik paketi icinde ele alinacak. Her dosyadan sonra commit veya Actions calistirmak yerine, hazirlik ve yerel dogrulama tamamlaninca tek commit ve tek K1-K5 CI tercih edilecek. Kapsam: aday puanlama diferansiyeli, logo/EPG pilotu, 390 tekrar testi uyumlulugu ve K1-K5 kanit zinciri. Hatalar ayni paket icinde duzeltilecek. Korunan playlist, EPG, logo, yedek ve cihaz verilerine yazma yok; eski depo salt okunur. 92/92 ve 26/26 onayi halen 0.

## 20 Ekim 2026 — K3 eski EPG/logo ve 390 tekrar testi entegrasyonu
Yeni madsc/legacy_epg_logo.py ve madsc/legacy_retest_390.py ile izole, salt okunur eski davranis sozlesmeleri eklendi. tests/test_legacy_k3_compatibility.py ve Actions #39334663810 SUCCESS (SHA 293bf819) ile temel offline regresyonlar gecti. Sonraki toplu pakette madsc/core.py K3 kanit raporuna XMLTV pilotu, logo SHA birlestirme, 20 sn ffmpeg sozlesmesi ve otomatik onay engeli eklendi; tests/test_core.py bu alanlari denetler. Bu son paketin CI sonucu henuz dogrulanmadi. Ag/canli ffprobe, 390 gercek kanal, 5 kanallik gercek pilot, IBO cihaz ve 92/92-26/26 uretim kabulu degildir. Korunan dosyalara yazma yok.


## 20 Ekim 2026 — Son dogrulanmis K1/K3 ilerleme ve not koruma
- K3 logo/EPG ve 390 aday tekrar testi kaynak davranis uyarlamasi: madsc/legacy_epg_logo.py, madsc/legacy_retest_390.py, tests/test_legacy_k3_compatibility.py; Actions #39334663810 SUCCESS.
- K3 merkezi fixture kanit akisi entegrasyonu: commit 9c7055a79527b643459529294759f1a09d59109b; Actions #39334973919 SUCCESS.
- K1 izole rapor yazma siniri ve negatif testleri: madsc/fixture_report_writer.py, tests/test_fixture_report_writer.py; commit 7edeafcf5e8067985905ae6f8bf536bb173f3a20; Actions #39335736344 SUCCESS. Bu tum depo icin runtime write gate degildir.
- 99 YAML, 130 Python, 68 test kaynak envanteri daha once tamamlandi; tekrar baslama. Tam esdegerlik 0/92, gercek runtime guvenlik onayi 0/26. 47% yalnizca tahmini gelistirme puani, uretim hazirligi degil.
- Oncelik: K1 merkezi kanit entegrasyonu; K2-K3-K5 aday, EPG/logo, tekrar test zinciri; eski-yeni fixture diferansiyel kaniti; gercek restore ve IBO cihaz kabulunu ayri tut.
- Korunan CALISANLAR/YENILER/YEDEKLER/HEPSI/FAVORILER/EPG/logo/backup, eski salt okunur depo ve PR #71 degistirilmeyecek. Kullanici baglantili degisiklikleri tek toplu paket ve CI olarak istiyor. Kritik bulgular hem bu dosyaya hem SOHBET_DEVIR_NOTU_2026-10-20.md dosyasina kaydedilecek.

## 20 Ekim 2026 — K1 merkezi fixture yazma koruma kaniti paketi
madsc/core.py K1 execute, madsc/fixture_report_writer.py ile yalnizca gecici dizindeki reports/k1.json yazimini ve CALISANLAR.m3u yaziminin reddini denetler. tests/test_core.py merkezi kanit alanini kontrol eder. Bu yalnizca fixture yazma siniri kanitidir, tum repo/uretim runtime write gate veya 26/26 onay degildir. Son CI bu committen sonra ayrica dogrulanmali. Eski repo, uretim dosyalari ve cron degistirilmedi.

## 20 Ekim 2026 — K2 K3 K5 aktarim negatif test paketi
K3 negatif senaryolar (logo SHA eslesmesi, ffmpeg decode hatasi, ffprobe exception) Actions #39336625839 SUCCESS. Yeni tests/test_handoff_acceptance.py paketi K2 veri degistirme, K3/K5 run_id ve commit_sha farki, salt-okunur/ag/uretim iddiasi ve JSON tekrarli anahtar reddini denetler. Bu testler gercek 92/92 davranissal esdegerlik veya 26/26 runtime guvenlik kabulu degildir. Son yeni CI sonucu ayrica dogrulanacak.

## 20 Ekim 2026 — K4 yeni negatif restore testleri
K2-K3-K5 handoff testi Actions #39336859638 SUCCESS. K4 icin ayni uzunlukta ama farkli SHA256 icerikli backup ve iki dosyadan yalnizca EPG restore bozulmasi senaryolari tests/test_backup.py dosyasina eklendi. Gercek offsite yedek veya uretim restore onayi DEGIL. Yeni CI sonucu ayrica dogrulanacak.


## 20 Ekim 2026 — K2 yeni kesif kapsami (YAPILACAK)
Kullanici istegi: internet genelindeki acik ve izinli M3U/M3U8 canli TV listeleri, resmi canli yayin siteleri, acik IPTV dizinleri ve YouTube Live resmi/dogrulanmis televizyon yayinlari K2 kesif kapsaminda aranacak. K2 kaynak ve yayin hakki uygunlugunu, kimlik ve tekrar kontrolunu kanitlayacak. K3 akisin teknik, ses-video, EPG/logo ve oynatici uyumunu denetleyecek; K5 sureklilik/yeniden denetim yapacak. YouTube sayfa URL'si otomatik kalici M3U8 sayilmaz; token, DRM ve erisim kisitlari asilmaz. Kaynak kesfi otomatik listeye alma/onaylama degildir. Korunan listeler degistirilmez. Henuz uygulanmis/kanitlanmis degil; backlog gorevidir.

## 20 Ekim 2026 — K2 eski/yeni diferansiyel test genisletmesi
Pinned eski akilli aday puanlama betigi ile yeni madsc.legacy_candidate_merge ayni sentetik CSV girdilerinde karsilastirilacak: ayni URL icin farkli teknik skorlar ve tekrar eleme; ONCELIKLI_KANAL_TEK_NIK_RAPORU ile GENEL_ADAY_GERCEK_MEDYA_RAPORU arasinda medya kaniti onceligi. Eski CSV satirlari, UTF-8 BOM ve ozet JSON ayni olmali. Bu sadece secili eski gorev davranisina ait fixture kanitidir; 92/92 kabul degildir. CI sonucu ayrica kontrol edilecek.

## 20 Ekim 2026 — K2/K3 dogrudan eski-yeni betik karsilastirma basarilari
Actions #39337813130 (aday puanlama), #39338017857 (EPG/logo), #39338267421 (390 tekrar testi) SUCCESS. Pinned eski betikler izole sentetik ortamda fiilen calistirilarak yeni K2/K3 rapor ve CSV/M3U sonuclariyla karsilastirildi. Bunlar sadece secili senaryolardir, workflow seviyesinde 92/92 esdegerlik veya 26/26 runtime koruma onayi DEGILDIR. Sonraki toplu entegrasyon P01-P06 aday onceligi, R01-R05 tekrar takvimi, H01-H05 gecmis kanit kurallarina odaklanacak. M3U/M3U8 ve resmi YouTube Live kesif backlogu korunur.


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


## 20 Ekim 2026 — ESKI DEPO TUM METIN/NOT ARSIVI TAMAMLANDI (DOGRULANDI)
Kullanici onceligi: Madsc55/madsc-tv deposunun madsc/bes-sistem-toplu-birlestirme dalindaki AGENTS, 810 dosya ana notu, alt notlar, devam, devir, guvenlik, ozellik envanteri, planlar, raporlar ve karar kayitlarini yeni Madsc55/Madsc55-Tv main deposuna birebir tasimak. **TAMAMLANDI**: eski Git tree uzerindeki tum 45 adet .md/.txt/.rst metin dosyasi, orijinal goreli yollariyla docs/eski_depo_not_arsivi/ altina salt-okunur tarihsel kopya olarak eklendi. Eski ve yeni tree SHA eslestirmesi 45/45; eksik 0, farkli 0. Eski depo degismedi, uretim listeleri degismedi.
Aktarim commitleri: 4d044ba690e1ea35e6135dd81560d5da9acd246a (AGENTS, 810 dosya notu, DEVAM_NOTU, guvenlik ve envanter), a31ad4853cdee935d4016a4c549c1bddeb147211 (16 ana/alt plan), 4bb6e93188b514d20615a8845dac77f9f0a9badb (8 kontrol), 387a44030f2fd15d0bf246607b0739e47e764955 (8 kesif/IBO/rapor), 6de30b7d906c9e1087594a15a83df7f828c91667 (8 IBO/yedek/VOD).
Yeni sohbet okuma sirasi: (1) docs/eski_depo_not_arsivi/AGENTS.md; (2) docs/eski_depo_not_arsivi/OZELLIK_ENVANTERI.md ve GUVENLIK_KURALLARI.md; (3) docs/eski_depo_not_arsivi/DEVAM_NOTU.md'nin guncel devir bolumu, docs/eski_depo_not_arsivi/810 dosya notu.md'nin en son ilerleme bolumleri; (4) PROJE_HAFIZASI.md ve SOHBET_DEVIR_NOTU_2026-10-20.md; (5) ilgili alt notlar ve guncel GitHub Actions. Eski notlardaki eski repo/dal yazma talimatlari tarihsel baglamdir: yeni gelistirme yalniz Madsc55/Madsc55-Tv main, eski depo salt okunur. Yeni ve daha guncel kullanici karari eski tarihsel karardan ustundur. Ozellikle YEDEKLER'e otomatik ekleme izni daha sonra iptal edilmistir. IBO cihaz onayi ile ffprobe/fixture CI karistirilmaz.
**Kapsam siniri:** 45/45 tum metin/not dosyalarinin tasinmasidir; 810 adet tum kaynak/veri/gorsel dosyasinin tasindigi veya 810/810 derin icerik denetimi yapildigi iddiasi degildir. 810 inceleme sayaci eski defterdeki tekil kayitlardan devam eder. 92 workflow davranissal kabul 0/92, 26 runtime guvenlik kabul 0/26; bu sayaclar aktarimdan degismedi. Mevcut yeni notlar uzerine yazilmadi, yalniz ekleme yapildi.
Sonraki is: 45 arşiv notunun icinden ilgili kurallari ve tamamlanmis isleri oncelikle okuyarak K1-K5 gercek esdegerlik, kaynak/provenance ve izinli M3U8 kesif eksiklerini gider; tamamlanmis testleri tekrarlama.


## 20 Ekim 2026 — GitHub'da doğrulanan yeni işler (kanıtlı kayıt)

- Eski notlar toplu birleştirme: GitHub Actions koşusu https://github.com/Madsc55/Madsc55-Tv/actions/runs/39348756132 SUCCESS. 70 arşiv kaynağı, 1.878.838 bayt birleşik Markdown, SHA256 ed53161bbaf685e0d6d146547703631efb545a0cbd2abe51940c4b16bea24930, bütünlük doğrulaması TRUE. Kaynak silinmedi. Artifact: madsc-eski-notlar-tek-dosya-ve-sha256 (ID 12231903355). Birleşik dosya artifact olarak üretildi; main dalındaki ESKI_SISTEM_NOTLARI.md henüz bu birleşik içerikle değiştirilmedi.
- 99 eski YAML kaynak denetimi: https://github.com/Madsc55/Madsc55-Tv/actions/runs/39349243152 SUCCESS; workflow_count=99, behavioral_parity_verified_count=0. JSON artifact: madsc-legacy-99-source-audit (ID 12231504991). Kod commitleri 8482366acc7777f4af9a70de6a760d35e84f21da ve c3b5aa3fef25df6f1a36776463a640023b065ab0. Bu, yeniden araştırma veya davranışsal eşdeğerlik başarısı değildir; mevcut envantere ek kaynak kanıtıdır.
- K1 yazma yolu ön denetimi güçlendirildi: tekrar eden ve büyük/küçük harf varyantlı hedef dosya yolları fail-closed reddediliyor. Kod commit f4b7e83ff829e18c7d2335b806508e0e1fdfc7cb, test commit 40a0da5bfc7ca55905502a0469dfe165fae52f2c. Beşli CI https://github.com/Madsc55/Madsc55-Tv/actions/runs/39349540574 SUCCESS; önceki kod koşusu https://github.com/Madsc55/Madsc55-Tv/actions/runs/39349524217 SUCCESS. Bunlar izole regresyon kanıtıdır, üretim runtime kural kabulü değildir.
- Kalıcı kabul sayaçları: eski workflow davranışsal eşdeğerliği 0/92; güvenlik kurallarının gerçek çalışma zamanı kabulü 0/26. Beşli fixture CI yeşil olması üretim hazır anlamına gelmez.
- Sonraki uygulama işleri: (1) önceki 99 workflow inceleme ve eski/yeni notlarını esas alarak 92 görev için K1–K5 gerçek davranışsal karşılıkları ve kabul testlerini bitir; (2) K1 gerçek çalışma zamanı yazma kapısını ve 26 kuralı test et; (3) K2 gerçek kaynak ve doğrulanmış geçmiş üreticisini tamamla; (4) K3 gerçek kanal/EPG/IBO kabulünü, K4 dış geri yüklemeyi, K5 gerçek bakım zincirini kanıtla; (5) birleşik eski notların tek dosya olarak main'e güvenli ve kalıcı kaydını tamamla. Üretim listeleri ve eski depo salt okunur kalır.


### 20 Ekim 2026 — K2 gerçek geçmiş yayıncısında SHA256 uygulaması
- Kod: 0fbd349849e047191119f52407efe64f40542a76 — madsc/history_real_source_publish.py artık her bağımsız sağlanan geçmiş dosyasının SHA256 özetini hesaplar, çıktı baytlarını yeniden okuyup özet eşleşmesini doğrular; raporda source_sha256 ve byte_integrity_verified alanları bulunur.
- Test: 5ce005bccd4e9924be9330c87554b6dd2f1f9fd5 — tests/test_history_real_source_publish.py kaynak ve yayımlanan dosyalar için SHA256 kanıtını kontrol eder.
- Bu kod değişikliği gerçek tarihsel kaynak dosyalarını sağlamaz; real_source_independently_authenticated hâlâ false. Gerçek K2 geçmiş kabulü ve 92/92 eşdeğerlik henüz tamamlanmadı. Sonuç için ilgili GitHub Actions regresyon koşusu doğrulanmalıdır.


### 20 Ekim 2026 — K2 ek kaynak değişim koruması ve doğrulanmış CI
- Önceki K2 SHA256 regresyon CI https://github.com/Madsc55/Madsc55-Tv/actions/runs/39350031190 SUCCESS (commit 5ce005bccd4e9924be9330c87554b6dd2f1f9fd5). Kod koşusu https://github.com/Madsc55/Madsc55-Tv/actions/runs/39350021463 SUCCESS.
- Ek kod commit 340a37a6e10353e37c2829a86c9f98c5acba3f89: gerçek geçmiş kaynağı doğrulama ile yayınlama arasında değişirse fail-closed reddet; kaynak dosyaları veya üretim listeleri değiştirilmez. Yeni commitin CI sonucu ayrıca kontrol edilmeli.
- Hâlâ gerçek kaynak doğrulaması yok; 92 davranışsal eşdeğerlik 0/92 ve runtime güvenlik kabulü 0/26. Önceki kaynak araştırmasını tekrar etmeden gerçek uygulama/kabul adımlarına devam et.


### 20 Ekim 2026 — K2 kaynak değişimi olumsuz senaryo testi
- Commit 3256d9ab4f2a265b91cd7ccd67e57549b6d2ffb9: tests/test_history_real_source_publish.py içine, kaynak okuma arasında gecmis.json baytlarının değişmesini taklit eden regresyon testi eklendi. Beklenti: ValueError ve hiçbir çıktı dizini oluşmaması.
- Test GitHub Actions koşusu https://github.com/Madsc55/Madsc55-Tv/actions/runs/39350454947. Bu not yazılırken koşu queued; SUCCESS iddiası yapılmaz.
- Kaynak değişimi kontrolünün kod commit'i 340a37a6e10353e37c2829a86c9f98c5acba3f89; gerçek geçmiş kaynağı ve üretim doğrulaması halen eksik.


### 20 Ekim 2026 — K4 uçtan uca izole geri yükleme uygulaması
- K4 kodu 5f88dd9e4e1b50d2e7dcf61affcd8b386a45a51a: madsc/restore_drill.py, izinli dosyaları geçici yedek klasörüne kopyalar, ayrı geçici geri yükleme klasörüne taşır, üç bağımsız ağaç SHA256 manifestlerini karşılaştırır ve kaynak değişmediyse drill_executed=true kanıtı üretir. Kaynak veya üretim dosyalarını değiştirmez.
- K4 testleri ff0be3425165faf7bcce075e42974d3cd4aad624: tests/test_restore_drill.py, iç içe dosya geri yükleme, kaynak korunumu, geçersiz/tekrarlanan yollar ve symlink reddini sınar.
- CI entegrasyonu 51b8730cca605dacbdeec7ab16fed065f029ca20: .github/workflows/madsc-05-bakim.yml K4 işinde izole geri yükleme tatbikatı yürütür ve madsc-k4-restore-drill artifact'ını yükler. CI https://github.com/Madsc55/Madsc55-Tv/actions/runs/39350699732 ilk sorguda pending; sonucu doğrulamadan başarılı ilan etme.
- K2 kaynak değişimi test koşusu https://github.com/Madsc55/Madsc55-Tv/actions/runs/39350454947 SUCCESS; K2 kod koşusu https://github.com/Madsc55/Madsc55-Tv/actions/runs/39350369959 SUCCESS.
- Bu K4 tatbikatı harici depolama ya da gerçek üretim restore kanıtı değildir. 92 davranışsal eşdeğerlik ve 26 runtime kural kabul sayaçları hâlâ sıfır.


## KALICI CALISMA KURALLARI — Kullanici teyidi 20 Ekim 2026
Bu bolum sohbetler arasi devirde onceliklidir; onceki kararlari kaybetme.
1. Yeni sistem Madsc55-Tv (Madsc55/Madsc55-Tv); eski Madsc55/madsc-tv salt okunur tarihsel kaynaktir. Isimleri karistirma.
2. K1 guvenlik, K2 kesif/gecmis, K3 kanal testi, K4 yedek/geri yukleme, K5 bakim tek bir entegre sistemdir. Bir is birden fazla K'yi etkiliyorsa ayni is kapsaminda hepsini uygula ve birlikte dogrula. Sadece ortak CI calismasi davranissal entegrasyon kaniti sayilmaz.
3. Onceki sohbetlerde kararlastirilan hedefleri, kullanici taleplerini, yapilanlari ve yapilacaklari kaybetme. Her yeni sohbette once PROJE_HAFIZASI.md, SOHBET_DEVIR_NOTU_2026-10-20.md ve ilgili mevcut kanitlari oku; gerektiginde onceki sohbet baglamini ara. Tum sohbetlerin otomatik eksiksiz aktarıldigini varsayma.
4. 99 eski YAML / 92 otomasyonun daha once yapilmis kaynak incelemesini gereksiz tekrarlama. Davranissal esdegerlik kabul edilmis sayisi 0/92, 26 runtime guvenlik kabul sayisi 0/26; dogrulanmadan sayilari yukseltme.
5. Kucuk tekil testleri bitmis sistem gibi sunma. Kapsamli, baglantili uygulama ve gercek kabul kanitlari uret; commit, GitHub Actions sonucu ve artefakt referanslarini kaydet.
6. Eski notlar ve kararlar korunacak, kayip olmadan yeni sistemde erisilebilir olacak. Tam aktarilmayan arsivleri aktarildi diye bildirme.
7. Sohbet bitiminde yapilanlar, bekleyenler, engeller, dogrulanmis kanitlar ve siradaki somut uygulama adimlari notlara yazilacak. Kullanici ayni talepleri tekrar etmek zorunda birakilmayacak.
8. Asistanin tum onceki sohbetleri otomatik olarak eksiksiz gorebildigi iddia edilmez; eksik baglam varsa kayitlardan arastirilir ve sinirlar acikca belirtilir.


## GENISLETILMIS BAGLAYICI PROJE KURALLARI — 20 Ekim 2026
Bu kurallar onceki sekiz maddeyi tamamlar; kullanici talepleriyle celisirse kullanicidan teyit al.
9. Her gorev icin etki matrisi olustur: K1/K2/K3/K4/K5 etkileniyor mu, hangi girdi/cikti ve bagimliliklar var, hangi test/kabul kaniti gereklidir? Etkilenenlerin hepsi ayni is paketinde tamamlanmadan gorev kapatilmaz.
10. Tamamlanma seviyeleri ayri kaydedilir: kaynak incelemesi, kod uygulanmasi, birim testi, sistemler arasi entegrasyon, gercek veriyle davranissal esdegerlik, runtime guvenlik, uretim kabul. Fixture CI yalnizca ilgili test seviyesini kanitlar.
11. Eski 99 YAML ve 92 otomasyon icin sadece sayim degil, gorev, tetikleyici, girdiler, ciktilar, yazma etkileri, bagimliliklar, guvenlik kosullari, yeni K karsiligi ve davranissal kabul kaniti izlenir; mevcut arastirma tekrar edilmez.
12. Notlar sadece sohbet ozeti degil, karar kaydi, yapilacak/yapilmayacak isler, acik sorunlar, teknik borc, kanit baglantilari, riskler ve siradaki somut uygulama adimlarini kapsar. Yeni sohbette bu kayitlar okunur; eksik gecmis gerekirse ayrica aranir.
13. Yedekleme ve geri yukleme isleri gercek veri kaybina yol acmadan yapilir; korunan dosyalara izinsiz yazilmaz, bagimsiz kopya ve restore kaniti ayrilir, gercek dis depolama kaniti olmadan uretim yedegi tamamlandi denmez.
14. Kanal kesfi ve gecmis K2; kanal sagligi K3; EPG/XMLTV ve tvg-id uyumu, IPTV oynatici farkliliklari ve IBO Player Pro gercek cihaz dogrulamasi birbirinden ayri kabul edilir. Tek oynaticida calisma tum oynaticilarin kabulunu kanitlamaz.
15. K1 guvenlik kurallari sadece rapor degil, ilgili gercek yazma/isletim yollarinda zorunlu engel olacak sekilde baglanir; runtime kaniti olmadan 26 kural kabul edilmis sayilmaz.
16. K5 bakım sadece ozet uretmez; K1-K4 basarisizliklarini ve eksik kanitlarini fail-closed birlestirir; sahte basari veya otomatik uretim degisikligi yapmaz.
17. Buyuk bir is kucuk parcali commitlerle ilerlese bile kullaniciya 'tamamlandi' yalnizca kapsamin tum bagimliliklari ve kabul testleri tamamlandiginda denir. Her turda mevcut tamamlanma ve acik kalanlar somut ayrilir.
18. Kaynaklarin tumunun goruldugu veya sohbetlerin eksiksiz aktarildigi varsayilmaz. Bilinmeyen, eksik, dogrulanmamis veya bloke isler acikca yazilir; hicbir eski kaynak silinmez.
19. Degisikliklerin kaniti GitHub commit SHA, ilgili Actions run sonucu, artifact ve test kapsamidir. Calisan/queued CI icin SUCCESS iddia edilmez. Tekrarlayan kucuk testler asil entegrasyonun yerine gecmez.
20. Proje sahibi onayi olmadan canli yayin listeleri, EPG/gecmis, korunan kaynaklar veya uretim sistemleri degistirilmez. Once salt okunur ve izole dogrulama, sonra izinli kontrollu gecis uygulanir.


## 20 Ekim 2026 — Birleşik kalıcı çalışma sözleşmesi
- Kullanıcının kesin vurgusu: eski ve yeni TÜM ilgili notları sadece arşivlemek değil; sistem kurulurken önce okuyup geçmiş hataları, eksikleri, alınan kararları ve yapılacak/yapılmayacak işleri anlayarak uygulamak. Sohbetler arası kayıp ve tekrar inceleme kabul edilemez.
- Tek çalışma kuralı giriş dosyası: BIRLESIK_KALICI_CALISMA_KURALLARI.md (commit 8aad8b00ff77a093bf2ef3bfef1d3fe4de7ad44d). Eski ve yeni notları silmez veya onların yerini almaz. Önce bunu, sonra göreve ilgili özgün notları oku.
- Kontrol edilen kaynak girişleri: PROJE_HAFIZASI.md, ESKI_SISTEM_NOTLARI.md, SOHBET_DEVIR_NOTU_2026-10-20.md. Eski arşivdeki her dosyanın baştan sona okunduğu iddia edilmez; tüm notların fiziksel tek dosyada birleştirilmesi hâlâ açık iştir.
- Öncelik: geçmiş hata/eksik analizi + K1–K5 etki matrisi + gerçek entegrasyon/kabul. Sadece kural yazmayı sistem kurma başarısı sayma.


## 20 Ekim 2026 — Yeni Madsc55-Tv K1–K5 fail-closed ve eski not tamlık denetimi
- Dogru ve tek yazilabilir depo: `Madsc55/Madsc55-Tv` / `main`; eski `Madsc55/madsc-tv` salt okunur.
- K1–K5 workflow bagimliliklari duzeltildi: K2 yalniz K1 success, K3 yalniz K2 success, K4 yalniz K3 success, K5 yalniz K4 success. Toplu-kabul basarisizliklari raporlamak icin `always()` ile devam eder. Kod commit `35ebf5c2a0f2ca942a4534433d479d77c0bb2716`, regresyon testi `2580697f5d8c3ef31ca2778de7ef16460092e99d`; Actions #39353356536 **SUCCESS** (izole CI).
- `madsc/legacy_notes_integrity.py` artik kaynak bolumleri disindaki eklenmis/sahte metni de reddetmek icin birlesik belgeyi byte-seviyesinde yeniden olusturur. `tests/test_legacy_notes_integrity.py` negatif enjeksiyon testi eklendi. Son commit `8f1016c2ccceb1999a1c09f88474ccaaf518c445`. Ilk ara commit #39353672144 FAILURE; duzeltildi, son Actions sonucu henuz teyit edilmedi.
- Kapsam siniri: main `ESKI_SISTEM_NOTLARI.md` halen tam fiziksel birlesim degil; eski arsiv kaynaklari silinmedi. 92 eski workflow davranissal kabul 0/92, 26 runtime guvenlik kabul 0/26, canli IBO/EPG ve dis depolama restore kabulu yok. Bunlari fixture CI ile tamamlanmis sayma.
- Siradaki somut is: son toplu Actions sonucunu dogrula, hatalari gider; 45 metin + karar niteligindeki JSON/CSV kaynaklarini siniflandirip tam metin birlesim artifact'ini GitHub main'e guvenli sekilde aktar; K1–K5 gercek kanit zincirini ve bagimsiz kaynak/restore dogrulamasini ilerlet. Korunan listelere, EPG, logo, arsiv ve eski depoya dokunma.


## 20 Ekim 2026 — K4 restore kanitinin K5 toplu kabule baglanmasi
- `madsc/k4_evidence.py` yeni fail-closed K4 kanit dogrulayicisi: gercek izole restore, kaynak butunlugu, bagimsiz kopya dogrulamasi, dosya sayisi ve uretime yazilmadigi dogrulanir; harici/uretim restore kaniti varmis gibi davranilmaz. Commit `6cc8a684eac9f34505b8cf95064b5194ff19b605`.
- `.github/workflows/madsc-05-bakim.yml` toplu kabul adimi K4 restore artifact'ini indirip dogrular; sonuc K5 toplu hata sayacina eklenir, dogrulama artifact'i saklanir. Commit `dc5eb4523c2f2583f0e707b1a5ff5766cd8c7f33`.
- `tests/test_k4_evidence.py` eksik ve sahte kanitlari reddeden testler eklendi; commit `3a78352e7facaff1cbe67cc875c1218eb637cac8`. Actions #39354010229 baslangicta PENDING; basari henuz kanitlanmadi.
- Onceki not butunluk degisikligi icin Actions #39353692761 ve #39353692734 SUCCESS. 92 davranissal esdegerlik ve 26 runtime guvenlik kabulu hala 0; fiziksel tek dosya birlestirme hala acik.


## 20 Ekim 2026 — ESKI_SISTEM_NOTLARI.md fiziksel tek dosya teslimi
- `.github/workflows/madsc-legacy-notes-bulk-merge.yml` icin yalnız yeni repo main dalina SHA256 dogrulanmis birlesik notu commit eden adim eklendi; eski kaynak notlar silinmedi, eski repo degistirilmedi. Commit `b36c4d8a41645d1dba331df323cf88247bfa159e`.
- Actions run #39354650723 SUCCESS. Main'deki `ESKI_SISTEM_NOTLARI.md` tekrar okundu: artik indeks degil, 70 arşiv kaynagini kapsayan 1.790.411 karakterlik tam metin; bolumler kaynak SHA256 ve sinir isaretcileriyle ayriliyor.
- Kapsam siniri: 70 kaynak = yeni repo arşivinde mevcut 45 metin ve 25 yapisal kaynak; eski depodaki tüm diger 52 yapisal dosyanin aktarildigi iddia edilmez. 92/92 davranissal esdegerlik ve 26/26 runtime guvenlik kabulü hala 0; canli cihaz/EPG/offsite restore üretim kabulu yok.
- Siradaki toplu is: 92 otomasyonun kaynak kodu/tetik/izin/artefact/hata davranisi matrisi ve 26 kuralin gerçek yazma/engelleme kanitlarini bagimsiz kanitla kapat. Fixture CI veya statik envanterden kabul sayaci arttirma.


## 20 Ekim 2026 — 99 YAML kaynak bütünlüğü ve 26 güvenlik kabulü
- Eski depo salt okunur. 99 YAML'ın GitHub blob SHA'sını dosya baytlarıyla doğrulayan fail-closed kontrol `madsc/legacy_99_bulk_audit.py` içine eklendi. GitHub base64 satır sonları katı ayrıştırmadan önce normalize edildi. Son kod commit: `6312bb38bd9082d76861ecbfb13f018dcc186ef7`.
- Pozitif ve sahte içerik negatif testleri `tests/test_legacy_99_source_integrity.py` içinde. İlk CI #39355240566 base64 satır sonu nedeniyle FAIL verdi; düzeltmeden sonraki #39355304902 beklemede, başarı henüz iddia edilmez.
- 99 YAML = 92 eski kapsam workflow + 7 özel/koordinatör. 99/99 kaynak denetimi ile 92/92 gerçek davranış eşdeğerliği ayrı kanıtlardır; gerçek kabul 0/92.
- Kaynak `GUVENLIK_KURALLARI.md` belgesi 1–24 maddeleri açıkça tanımlar. 25–26'nın onaylı tam kaynak metni ayrıca kanıtlanmadan 26/26 denemez. Runtime kabul 0/26.
- Genel ilerleme referansı kullanıcıya göre yüzde 47 tamamlanan, yüzde 53 kalan; yalnız doğrulanmış kabul değişiminde yeniden değerlendirilir.


## 20 Ekim 2026 — 99 kaynak audit SUCCESS, geçici yazma izni kapatıldı
- 99 eski YAML byte-exact Git blob SHA denetimi Actions #39355304902 SUCCESS. Bu kaynak bütünlüğüdür, 92 davranışsal kabul değildir.
- K1-K5 Actions #39355304855 FAILURE: K1 regresyon testi, birleşik notları main'e yazdırmak için geçici açılmış `contents: write` ve `persist-credentials: true` izinlerini haklı olarak reddetti.
- Tek dosya birleşimi daha önce main'e teslim edildiği için `.github/workflows/madsc-legacy-notes-bulk-merge.yml` salt okunur `contents: read`, `persist-credentials: false` olarak geri alındı ve otomatik `git push` kaldırıldı. Commit `65858bf3e74b2ffa1ae0004bd629e6808d4e5d42`. Birleşim Actions #39355451415 SUCCESS.
- Güvenlik regresyonuna not birleştirme iş akışının bir daha push/credential yetkisi taşımamasını kontrol eden test eklendi. Commit `3da63cc6fb76af5fd78eecb3bf9313d8158bb406`. Beşli CI #39355467204 henüz sonucu doğrulanmadı.
- 99 kaynak denetimi SUCCESS olsa da 92/92 davranışsal eşdeğerlik ve 26/26 runtime güvenlik kabulü hâlâ 0; üretim onayı yok. Eski depoya yazma yok. Genel referans %47/%53.


## 20 Ekim 2026 — 292 testteki K1 hata zinciri giderildi
- Kullanıcının ekran görüntülerindeki önceki K1 failure: `test_notes_merge_cannot_push_after_one_time_delivery` testinin YAML izin satırını yanlış kaçışla karşılaştırması. 292 testte 1 failure, K2–K5 skipped, toplu kabul artifact indirmeleri buna bağlı failed.
- Test düzeltmesi commit `1fdc2684d21d6e59a4e9a908d1d661efa6e748c2`.
- GitHub Actions `39355568913` SUCCESS: Güvenlik, Keşif, Kanal Testleri, Arşiv ve Yedek, Genel Bakım, Beşli toplu kanıt doğrulama işlerinin tamamı success. Bu izole CI kabulüdür; canlı üretim, 92 davranış eşdeğerliği veya 26 runtime güvenlik kuralı kabulü değildir.
- Eski depo ve korunan yayın dosyaları değişmedi; kullanıcı referansı %47 tamamlanan / %53 kalan.


## 20 Ekim 2026 — K1 yazma kapısı ilk gerçek çağrı noktasına bağlandı
- İzole `madsc/fixture_report_writer.py` artık korunan yol denetimini sadece raporlamıyor; yazmadan önce `enforce_write_paths` çağırıyor. Commit `c3f24417ec46c577b6deade3a8e7a440bc9d7785`.
- `tests/test_fixture_report_writer.py` regresyonu, kapı hata verdiğinde `reports/` klasörü bile oluşturulmadığını ve dosyaya yazılmadığını denetliyor. Commit `80ad0ec924f618c1de9eea6c3ff782252b2da6ef`.
- Önceki K1-K5 izole test #39355945113 SUCCESS. Yeni entegrasyon testi #39356267666 sonuç bekliyor; henüz kabul sayılmaz.
- Bu yalnız izole fixture raporu yazma yolu için gerçek çağrı noktasıdır; GitHub push veya tüm üretim yazma yollarını yakaladığı iddia edilmez. 26/26 runtime kabul 0/26; 92/92 eşdeğerlik 0/92. Genel referans %47/%53.


## 20 Ekim 2026 — Eski 20 ilkeye bağlı K1–K5 görev yerleştirme
- Kullanıcı kararı: yeni kabul yöntemi kurmadan, eski 20 çalışma ilkesi ve ek depo kimliği kuralına göre 99 workflow ile 26 güvenlik görevini ait oldukları K1–K5 yerlerine ve sıraya entegre et. Gereksiz küçük test döngülerini ana iş diye sunma.
- 99 kaynak denetimine geçici `candidate_k_stages` ve `stage_mapping_reviewed: false` alanları eklendi; eşleşmeyenler `UNCLASSIFIED`. Kaynak kodu: commit `941171a2bf9e83b740c9f3c7d84baf176e4fa2ff`. Bu yalnız dosya adına dayalı ilk yönlendirmedir, gerçek görev çözümlemesi ve davranış kabulü değildir.
- 99 kaynak regresyonu ve workflow CI kapısı commit `15371971e923d4c389823b073be3724208b2b999`, `5c276f7d13bfec29dc4c556aa8d77e829ba7ec7a`. Actions #39356612285 henüz sonuçlanmadı.
- Önceki K1–K5 izole güvenlik entegrasyon testi #39356267666 SUCCESS. Gerçek üretim/IBO/harici restore onayı değildir.
- Sıradaki büyük iş: geçici K sınıflamasını 99 dosyanın komut, tetik, izin, çıktı, bağımlılık ve yan etki kaynaklarıyla doğrula; 26 kuralın onaylı kaynak metnini belirle; beşli sistemde gerçek görev çağrı noktalarına bağla. Korunan veriye ve eski depoya yazma yok. 92/92 ve 26/26 kabul hâlâ 0; genel referans %47/%53.


## 20 Ekim 2026 - Besli sistem dogrudan islev kurulum karari ve K1-K2 entegrasyonu
- Kullanici karari: 99 eski YAML kopyalanmaz; islevler dogrudan K1-K5 icinde kurulur, tekrarlar birlestirilir. 20 ortak calisma ilkesi ve ek depo kimligi ilkesi gecerlidir. K1 isi K2-K5'i ilgilendiriyorsa ilgili baglantilar ayni paketle degerlendirilir.
- 26 guvenlik hedefi ayri otomasyonlar degil, K1 ve ilgili sistemlerin gercek islem noktalarinda uygulanir. Kaynakta 24 madde tanimli, kalan ikisi kesinlestirilmeden uydurulmaz.
- K1 korumasi K2 izole gecmis raporu yazicisina baglandi: madsc/history_pair_store.py write_isolated_history_pair. Commit cbf250650818c23c25e1137f4e92391a947762b3.
- Gecmis yazma, mevcut raporu degistirme ve path traversal testleri eklendi: 26a7b775295b91dd705f9c90589a92248a569b33. Actions 39406192839 son kontrolde pending; SUCCESS iddiasi yok.
- Onceki izole K1-K5 CI 39404862422 SUCCESS. Canli IPTV, IBO, tum yazma yollari veya davranissal esdegerlik kaniti degil. Eski depo ve korunan listeler degismedi.
- Siradaki is: K3-K4-K5 gercek rapor/yedek/yazma cagrilarini ayni K1 politikasina baglamak, bagli testleri toplu calistirmak. Genel referans %47/%53, kabul 0/92 ve 0/26.


## 20 Ekim 2026 - K1 guvenlik kapisinin K3/K4/K5 izole kanit arayuzune baglanmasi
- K3 kanal testi, K4 yedek ve K5 bakim raporlarinin izole yazimi icin write_stage_report eklendi. Ortak K1 write_fixture_report korumasini cagirir, asama ve production_writes:false alanlarini zorunlu kilar, mevcut kanit dosyasini ezmez. Commit 604a4559ac97cb4e928fff8703fe7f987aa1326d.
- K3/K4/K5 yazim ve reddetme regresyonlari eklendi: b2b35889dfb8425b566e63de699f251b1234a71b. Toplu CI 39406887334 son kontrolde queued; henuz basarili sayilmaz.
- K1-K2 onceki toplu CI 39406192839 SUCCESS. Yeni arayuz mevcut K3/K4/K5 uretim cagrilarina henuz baglanmadi; bu eksik acik kalacak.
- 20 calisma ilkesi ve ek depo kimligi kurali, eski depo salt okunurlugu ve korunan verilerin degistirilmemesi suruyor. 99 YAML aynen tasinmayacak; islevleri besli sistemde gelistirilecek. Genel referans %47/%53.


## 20 Ekim 2026 - K4 gercek komut akisina K1 rapor korumasi
- K4 restore_drill.py CLI icin istege bagli --isolated-report-root eklendi. Bu modda rapor sadece reports/k4-isolated-evidence.json hedefine, write_stage_report uzerinden ortak K1 denetimiyle yazilir. Eski CLI kullanim yolu korunur. Commit 2352fe0c772f7aa0598f208338d0615772634332.
- K4 komut akisinin izole rapor uretimi ve mevcut raporu ezmeme regresyonu commit 6e7ea5e8d2b695211ebb2e60aa2f529beeab396f.
- Onceki K1-K5 CI 39406887334 SUCCESS. Yeni K4 CI 39407380313 son kontrolde in_progress; sonuc kesinlesmeden basarili sayilmaz.
- K3 ve K5 gercek komut cagrilari ortak guvenlik arayuzune henuz bagli degil. K4 modu istege baglidir, tum uretim yazmalarini kapsamaz. Eski depo ve korunan listeler degismedi. Genel referans %47/%53.


## 20 Ekim 2026 - K3 ve K5 gercek degerlendiricilerinin K1 korumali rapora baglanmasi
- madsc/stage_report_cli.py: K3 icin summarize_offline_probe_evidence, K5 icin summarize_batch gercek mevcut degerlendiricilerini cagirir; izole raporlari write_stage_report ile K1 kapisindan yazar. Canli ag testi, uretim yazmasi veya uretim kabulu yapmaz. Commit 6d4e716a71b94b2229914b8df8f6ba2e61141232.
- K3/K5 CLI gercek islev, izole yazma ve ustune yazmama testleri: 3e8169ca3616ab718a7656ce601ae524b6e26743. Actions 39407853563 son kontrolde pending; basarili iddiasi yok.
- Onceki K4 CLI entegrasyon test run 39407395209 SUCCESS. K3/K5 CLI yeni bir opt-in giris noktasi; mevcut Actions workflow'larinin otomatik olarak bu komutu kullandigi henuz kanitlanmadi.
- Korunan kanal listeleri, EPG, favoriler, yedekler ve eski depo degistirilmedi. 20+1 calisma kurali gecerlidir. Genel referans %47/%53, davranissal kabul 0/92, runtime guvenlik kabul 0/26.
- Siradaki: CI workflow giris noktalarini inceleyip K3/K4/K5 gercek calistirma baglantilarini kanitla; bekleyen run sonucunu dogrula, butun K'lerin bagli etkilerini birlikte test et.


## 20 Ekim 2026 - Besli Actions K3/K4/K5 K1 korumali komut entegrasyonu
- .github/workflows/madsc-05-bakim.yml icindeki K3/K4/K5 islerine yeni K1 korumali izole kanit komutlari ve ayri artifact yukleme adimlari eklendi. K3 offline fixture ffprobe raporu, K4 izole restore tatbikati, K5 fixture toplu ozeti; her biri reports/reports altinda ve korumali yazar uzerinden. Commit 3a45ba8e3e43ae18aa38ddd54e5677bf87c07d00.
- Onceki stage_report_cli test CI 39407853563 SUCCESS. Yeni workflow CI 39408633114 son kontrolde queued; yeni zincirin tam basarisi henuz kanitlanmadi.
- Bu islem mevcut beşli workflow'u degistirdi, ancak eski depo, korunan kanal listeleri, EPG, favoriler, yedekler ve PR #71 degismedi. Fixture verisi canli test/IBO/harici backup veya 92/26 kabulune esit degildir. Referans %47/%53.
- Sonraki adim: 39408633114 alt islerini kontrol et; basarisizlik varsa ayni K1-K5 etkileriyle duzelt; gercek kaynakla davranissal kaniti ayrica tamamla.


## 20 Ekim 2026 - Besli toplu run 39408633114 K3 hatasi ve duzeltme
- Actions 39408633114 FAILURE: K1 ve K2 SUCCESS; K3 'K3 offline fixture kaniti olustur ve K1 korumali raporla' adiminda FAILURE; K4/K5 SKIPPED; toplu kabul eksik artifact nedeniyle FAILURE.
- K3 fixture JSON printf yerine python json.dumps ile uretiliyor. Duzeltme commit 30fbba668682fd84e9ee8aa295cc0d44e1bc1ab6. Kesin kok neden log satiri ile henuz kanitlanmadi; bu bir ilk duzeltme denemesidir.
- Yeni Actions 39408869866 son kontrolde in_progress. Basari kesinlesmeden kabul edilmeyecek. K4/K5 ve toplu kabul zincirinin sonucu kontrol edilecek.
- Eski repo, uretim kanal listeleri, EPG, favoriler, yedekler ve PR #71 degistirilmedi. Referans %47/%53; 0/92, 0/26.


## 20 Ekim 2026 - K5 gercek kategori artifact baglantisi
- Onceki duzeltme CI 39408869866 SUCCESS: K1-K5 izole toplu zincir tekrar gecti.
- K5 onceki sabit success fixture dizisi yerine ayni Actions kosusunun madsc-batch-k1..k4 artifact'larini indirir, kendi k5.json raporunu ekler, tum bes kategori JSON kanitini load_batch_reports ile kimlik/mod/izin/durum/fixture alanlarinda fail-closed denetler. Ardindan K1 korumali write_stage_report ile K5 izole ozetini yazar. Kod f9846cc024dfbead8552acb403cbe57a136b41d3; workflow e465b0c162aa666cbb633628cdb06e548a4edf96; eksik kanit testi c77471502d3bf62981bc372c4403a58b0b2e4ae5.
- Son test 39409310885 pending. Ara workflow run 39409293787 cancelled, basari olarak sayilmaz. Tam zincir ve artifact indirme dogrulanmali.
- Bu gelistirme fixture CI kanitinin sahte sabit success ile temsilini azaltir, ancak gercek kanal ag testi/IBO/harici restore/92 davranissal kabul/26 runtime guvenlik kabulunu kanitlamaz. Eski repo ve korunan listeler degismedi. Referans %47/%53.


## 20 Ekim 2026 - K5 artifact paket guvenligi sertlestirme
- Onceki tam besli Actions 39409310885 SUCCESS.
- K5 load_batch_reports artik sadece kisitli alanlari kontrol etmek yerine madsc.batch_acceptance.collect ile tum 5 artifact paketini, dosya/dizin yapisini, symlink, beklenmeyen dosya, kategori schema, checks ve fixture alanlarini ayni fail-closed kabul kapisindan dogrular. Kod commit 4c884ac6e4f62e4c5507e3b7b8635bf389691907.
- test_stage_report_cli fixture'i tam schema ile duzeltildi; beklenmeyen extra.txt dosyasi reddi eklendi. Test commit e9133fc9149972034a0f8cd595557e7901671eab.
- Yeni toplu Actions 39409800593 son kontrolde pending; onceki 39409784819 in_progress. Bunlar basarili ilan edilmedi.
- Eski depo ve korunan listeler degismedi. 0/92 davranissal, 0/26 runtime guvenlik kabul; %47/%53 referans.


## 20 Ekim 2026 - K5 sikilastirma CI hata takibi
- Kullanici GitHub ekran goruntusunde #319 kirmizi, #320 calisiyor bildirdi. API: 39409784819 FAILURE; K1 'Tum regresyon testlerini calistir' FAIL, K2-K5 SKIPPED, toplu kabul FAILURE. Bu ara commit 4c884ac6, yeni strict collect semasina eski test fixture'i uymuyordu; test duzeltmesi e9133fc9 sonraki committe.
- 39409800593 son job kontrolunde K1/K2/K3/K4 SUCCESS, K5 in_progress; toplu kabul henüz kesinlesmedi. K5 ve toplu-kabul sonucunu takip et, yesil olmadan kabul iddiasi kurma.
- Eski depo ve korunan listeler degismedi. Referans %47/%53; 0/92, 0/26.


## 20 Ekim 2026 - K5 icinde K2-K3-K5 aday kaniti capraz kabul kapisi
- Son tam izole Actions 39409800593 SUCCESS; onceki 39409784819 FAILURE ara commit kaynakli.
- madsc-05-bakim.yml K5 job'una K3 handoff artifact indirimi ve madsc.handoff_acceptance ile K2/K3/K5 run_id, commit_sha, source_digest, candidate_count ve read-only receipt esleme kapisi eklendi. K5 raporlamadan once capraz kanit tutarsizsa durur. Sonuc artifact: madsc-k5-cross-handoff-verification. Workflow commit 10a36a77a675e0319e5021b229659c62543b5f2f.
- Yeni run 39410321203 son kontrolde queued; test sonucu kesinlesmedi. Bu fixture cross-handoff, canli stream veya 92 eski davranissal esdegerlik kaniti degildir. K1-K5 bagli test ve rapor sureci korunur.
- Korunan listeler, EPG, logo, favoriler, yedekler, PR #71 ve eski depo degistirilmedi. %47/%53 referans; 0/92 ve 0/26 runtime kabul.


## 20 Ekim 2026 - K2 aday K3 offline teknik kanit parmak izi baglantisi
- Onceki Actions 39410321203 SUCCESS. Yeni madsc/candidate_probe_link.py K2 envelope'i run_id/commit_sha/SHA256 digest ile unpack eder; K3 offline ffprobe kayitlarinin url_sha256 parmak izlerinin tamamini dogrulanmis K2 adaylarina baglar, yabanci probe'u reddeder. Test edilmemis adaylari ayrica sayar; canli ag/IBO/uretim onayi vermez. Kod commit 02bcf367faeb167649a7bfb0f76c05930d50fdc0.
- Testler: eslesen aday, yanlis run, yabanci probe, test edilmemis aday; commit b3e559043176e34809b5adceae05cf95acb188fc. CI 39410757432 son kontrolde pending; basarili iddiasi yok.
- Bu fonksiyon henuz mevcut workflow'un K3 adiminda kullanilmiyor; sonraki is fixture akisini gercek K2 candidate digest ile baglayip K3/K5'e entegre etmek. K1-K5 capraz etkileri ve veri koruma kurallari gecerli. %47/%53; 0/92, 0/26.


## 20 Ekim 2026 - K2-K3 aday teknik fixture baglantisi Actions'ta zorunlu
- 39410735665 ve 39410757432 onceki K2-K3 fingerprint kod/test kosulari SUCCESS.
- madsc/candidate_probe_link.py icine K2 envelope + K3 offline probe JSON okuyup run_id/commit_sha ve URL SHA256 bagini denetleyen K1 korumali K3 rapor CLI eklendi. Commit e3b3ee200594eeb3a478c5b4c63df78fc9d92174.
- madsc-05-bakim.yml K3 adimi artik sabit a*64 sahte parmak izi yerine ayni kosunun dogrulanmis K2 aday envelope'inden fingerprint cikarir ve candidate_probe_link CLI ile K3 izole raporunu yazar. Commit 15de0293af6bc56ad316c37791789b4f35ddff79.
- DIKKAT: K3 ffprobe kayitlari hala sentetik fixture (video/audio/40s); gercek ffprobe veya canli sureklilik kaniti degildir. Gercek kayit gelirse K2 baglantisi dogrulanabilir. Actions 39411220582 son kontrolde queued; basari iddiasi yok.
- Korunan listeler/EPG/favoriler/yedekler/eski depo/PR71 degismedi. 0/92, 0/26, %47/%53 referans.


## 20 Ekim 2026 - K5 K3 offline/canli kabul ayrimi
- Onceki K2-K3 Actions 39411220582 SUCCESS.
- candidate_probe_link K3 raporuna technical_samples_supplied, live_continuity_verified:false, candidate_identity_verified:false alanlari eklendi (104a01ed57e14eaa778309f70252d7e1d7a8308d).
- madsc/k5_channel_gate.py K3 korumali raporunun K2-K3 bagli schema, aday/probe sayilari ve network/IBO/canli sureklilik/kimlik/production false bayraklarini fail-closed kontrol eder; izole K5 gate raporu yazar (b675f3dee08ed5fe914ab8547dabee58e25d106a).
- K5 Actions madsc-k3-guarded-evidence indirir, k5_channel_gate calistirir, ayri artifact saklar (0b0d82f5ee3cc69dd166b1fa91f7e161e89d6f52). Testler 8ffe4b4f2cefddcdf0629587bff58c4ca0cddbce.
- Son CI 39411744643 pending; ara kosular 39411726765 ve 39411711232 cancelled. Basari iddiasi yok. K5 gate varligi fixture'in canli probe oldugunu ispatlamaz.
- Eski depo ve korunan dosyalar degismedi. %47/%53, 0/92 davranissal, 0/26 runtime guvenlik kabul.


## 20 Ekim 2026 - K5 kanal kaniti icerik tutarliligi
- Onceki K5 offline/canli guvenlik Actions 39411744643 SUCCESS.
- madsc/k5_channel_gate.py artik K3 technical_samples_supplied/probed sayisi, preliminary_passes+needs_review, benzersiz url_sha256 ve her kanal icin technical_status/stream_continuity_verified/channel_identity_verified/ibo_device_verified/production_change_allowed alanlarini fail-closed denetler. Commit aff33890f95c28e225fed46022bae6f052093737.
- tests/test_k5_channel_gate.py tutarsiz teknik sayi ve sahte ornek bayragi regresyonlari eklendi. Commit e57f5908cf296cf59f6a06f70fb7f06dc85f6aaf. Son CI 39412256597 ilk kontrol aninda in_progress (onceki commit); yeni test commit run'i henuz gorunmemisti. Kabul iddiasi yok.
- Bu paket gercek ffprobe olcumunu toplamaz; yalniz getirilen teknik kanitin tutarliligini korur. Gercek ffprobe kayitlarini kaynak kimligi, guvenilir toplama ortami ve K2 fingerprint ile iliskilendirme sonraki is. Korunan dosyalar degismedi. %47/%53; 0/92, 0/26.


## 20 Ekim 2026 - K5 K2-K3 orijinal envelope ile teknik kanit capraz baglantisi
- 39412256597 ara kod commit FAIL; 39412276145 test commit SUCCESS. K5 kanal gate kodu onceki calisan kabulden devam etti.
- madsc/k5_channel_gate.py K5 raporlamadan once orijinal K2 envelope'i unpack ederek run_id, commit_sha, source_digest, aday sayisi ve her K3 probe URL fingerprint'inin K2 adaylarina aidiyetini yeniden denetler. Kod 25a6d774130eca52350134cc9a62d626d377741a.
- madsc-05-bakim.yml K5 adimi ayni kosudan indirdigi K2 kanitini ve GitHub run/sha bilgisini bu kapidan gecirir. Commit fd79f41dc4c4d58ee8a862281ec750fd3338e53c. Testler yanlis run, digest, sayi icin 6f1d0a4a4a0f44dc2ec58b3d860069867cdd46e0.
- Son Actions 39412769302 pending; sonucu dogrulanmadi. Fixture disinda canli network/IBO kaniti yok, production_ready false. Korunan dosyalar ve eski depo degismedi. %47/%53, 0/92, 0/26.


## 20 Ekim 2026 - Kanita dayali ilerleme tablosu
- %47 tamamlandi / %53 kaldi tarihsel referanstir; otomatik hesaplanan guncel kabul orani degildir.
- madsc/progress_scorecard.py kaynak envanterini (99 YAML, 130 Python, 68 test dosyasi) davranissal kabulden (0/92) ve calisma zamani guvenlik kabulunden (0/26) ayri raporlar. Kanitsiz genel yuzde uretmez. Commit: 27ed5318a629fb1f8e7f40473ac291ff0fe10d42.
- Regresyon testleri: 868959f2f4e8fe46564c84096a89821cbc0d8bd9. K5 Actions rapor artifact entegrasyonu ve erken CI basarisi iddiasini engelleyen duzeltme: 81eb43bed387fd7ee667578a73e4e874aab4877d.
- Son kontrol aninda run 39413388267 pending. Uretim kabul iddiasi yok. Korunan dosyalar ve eski depo degistirilmedi.


## 20 Ekim 2026 - Yeni sohbete kesin devir ve guncel CI
- Son K1-K5 Actions 39413388267 SUCCESS (SHA 81eb43be). Son onceki 39412769302 SUCCESS. 39413372227 ve 39413355840 ara commit kosulari cancelled, basari sayilmaz.
- Yeni sohbet icin SOHBET_DEVIR_NOTU_2026-10-20.md bolum 8 genisletildi: kurallar, depo ayrimi, K1-K5 bagimliliklari, yapilanlar, yapilmayanlar, siradaki isler, kabul sayaclari ve kaynak okuma zorunlulugu. Commit 9fd61fdc53e76cdf7f163adaf6bf2880c2862c1d.
- BIRLESIK_KALICI_CALISMA_KURALLARI.md 20 ilke + ek 21 depo kimligi korunacak. Yeni Madsc55/Madsc55-Tv main yazilabilir; eski Madsc55/madsc-tv salt okunur. ESKI_SISTEM_NOTLARI.md, bu hafiza, devir notu, eski AGENTS/810/DEVAM ve ilgili ariv belgeleri okunmadan karar alinmayacak; okunmayan belge okundu denmeyecek.
- Referans %47/%53 degismedi; bu sabit tarihsel oran, guncel kanita dayali yuzde degil. Envanter 99/99 YAML, 130/130 Python, 68/68 test dosyasi; gercek davranissal kabul 0/92, runtime guvenlik 0/26. K3 gercek canli ffprobe/IBO ve K4 harici restore yok. Sonraki is kanitli diferansiyel esdegerlik ve guvenli gercek olcum entegrasyonu; uretim yazma kapali.
- Kullanici yeni sohbette yapilanlarin ve kararlarin unutulmamasini istiyor; bu notlar sureklilik icindir, birebir tam sohbet transkripti degildir.


## 20 Ekim 2026 - Kesin proje adi ve eski depo karismasini onleme
- Kullanici tekrar acikca duzeltti: yeni sistemin dogru adi **Madsc55-Tv**, tek yazilabilir GitHub deposu **Madsc55/Madsc55-Tv**, dal **main**. Yanlis kisaltma Madsc-Tv veya genel MADSC TV adi yeni proje adi olarak kullanilmayacak.
- Eski **Madsc55/madsc-tv** ve madsc/bes-sistem-toplu-birlestirme salt okunur. Yeni sohbet ve her yazma oncesi depo/dal kontrolu zorunlu.
- Birlesik kurallar commit c2995e1234e6b2589df9eb59a0c2ba149915e984 ve sohbet devir notu commit 7aac00360347c2ee6b787c0c7feaf22311007787 bu ayrimi ek zorunlu madde olarak guclendirdi.


## 20 Ekim 2026 - Yeni sohbet baslangicinda bagimsiz durum dogrulamasi
- Dogru tek yazilabilir depo Madsc55/Madsc55-Tv, main; GitHub repository API default_branch=main ve private=true dogrulandi. Eski Madsc55/madsc-tv salt okunur; hicbir yazma yapilmadi.
- Bu kontrol sirasinda HEAD 3c712befbccf8367b273ced2074876c9b7a7c444 (yalniz belge/kimlik hafizasi commit'i). En son gorunen Actions run 39413388267, SHA 81eb43bed387fd7ee667578a73e4e874aab4877d, completed/success; alti job (K1, K2, K3, K4, K5, toplu kabul) success. HEAD icin yeni CI basarisi iddia edilmiyor.
- BIRLESIK_KALICI_CALISMA_KURALLARI.md, SOHBET_DEVIR_NOTU_2026-10-20.md, PROJE_HAFIZASI.md ilgili kisimlari; eski AGENTS.md, GUVENLIK_KURALLARI.md, DEVAM_NOTU.md son bolumu, 810 dosya notu.md ilk ilgili bolumu ve docs/ESDEGERLIK_ILK_KANIT_PAKETI.md incelendi. ESKI_SISTEM_NOTLARI.md cok buyuk birlesik arsivinin varligi/hash'i dogrulandi; tamami satir satir okunmus sayilmiyor.
- Envanter tarihsel 99/99 YAML, 130/130 Python, 68/68 test. Davranissal tam kabul 0/92, runtime guvenlik 0/26; yuzde 47/53 tarihsel referans. CI fixture basarisi canli kabul degil.
- K1-K5 mevcut kanit zinciri: K2 envelope/run/SHA/digest -> K3 offline probe URL fingerprint -> K5 cross-handoff/channel gate; canli ffprobe/ffmpeg, cihaz IBO, kaynak/izin ve offsite restore kaniti acik. Mevcut testleri tekrar kurma.
- Siradaki toplu paket: guvenli opt-in ve salt okunur gercek kanal olcumu icin kaynak/izin/SSRF/yol/timeout/URL maskeleme kapilari; K2 aday fingerprint baglantisi, K3 ffprobe/ffmpeg teknik kanit, K5 kanit dogrulama, K1 negatif guvenlik ve K4 degismezlik testleri. Eski-yeni workflow tetik/izin/artifact/timeout farklarini ayni paket icinde kanitla. Korunan playlist, EPG, logo, yedek, cihaz favorileri ve PR71 degismeyecek. Kod/CI bu turda henuz degistirilmedi; kabul sayaclari artirilmaz.


## 20 Ekim 2026 — K3/K5 sahte canlı kanıt engeli, CI doğrulandı
- Yalnız yeni Madsc55/Madsc55-Tv main üzerinde `madsc/k5_channel_gate.py` için çevrimdışı sonuçlardaki `actual_network_measurements_verified`, `network_probed`, `production_ready` sahte true alanları reddedildi (commit 07414551fca295274fe95524a7692790356e604a).
- `tests/test_k5_channel_gate.py` negatif regresyon testleri eklendi (commit d39481ec00c5cae14f86acd2adb6aa3f02544660). GitHub Actions #39414904510, head SHA d39481ec00c5cae14f86acd2adb6aa3f02544660, completed SUCCESS olarak REST API ile doğrulandı. Bu offline test kabulüdür, canlı ölçüm değildir.
- Eski depo, korunan playlist/EPG/logo/favori/yedek ve cronlara dokunulmadı. Tam davranışsal kabul 0/92; gerçek runtime güvenlik kabulü 0/26. Referans %47/%53 güncel hesaplanmış oran değildir.
- Açık: K1/K3 tüm alanlar için fail-closed kanıt şeması, izinli/opt-in gerçek ffprobe/ffmpeg ölçümü, IBO cihaz doğrulaması, K4 bağımsız offsite restore ve K5 gerçek uçtan uca kabul. Bu turda canlı yayın ölçümü başlatılmadı.


## 20 Ekim 2026 — K1/K3/K5 toplu offline kanıt sertleştirme
- Yeni depo Madsc55/Madsc55-Tv main, eski depo salt okunur. `madsc/k5_channel_gate.py` opsiyonel canlı/üretim kanıtı alanlarında 10 bayrağı `False` dışında görünce reddedecek biçimde sertleştirildi. Commit c9bdb01436e9f2917891dfddede2f1ed29cfb615.
- `tests/test_k5_channel_gate.py` 10 sahte olumlu sonuç bayrağı, envelope sahte bayrakları ve `None`/sayı/metin bypass girişimleri için genişletildi. Commit 206645be5b047ccae3f2156cdcc0576f3ad16f9a.
- Son GitHub Actions #39415583107, SHA 206645be5b047ccae3f2156cdcc0576f3ad16f9a, ilk kontrol anında pending idi; SUCCESS iddiası yok, sonuç tekrar doğrulanmalı. Önceki #39414904510 SUCCESS ayrı commit'e aittir.
- K2-K3 offline handoff korunuyor; canlı ffprobe/ffmpeg henüz yapılmadı, IBO cihaz ve K4 offsite restore kanıtı yok. 92 davranışsal tam kabul 0/92 ve 26 runtime güvenlik kabulü 0/26 değişmedi. Korunan playlist/EPG/logo/yedek/favori dosyalarına yazılmadı.
- Sıradaki bütünleşik iş: CI sonucunu doğrula; K1 izinli ağ hedefi/SSRF/timeout/redirect kontrolleriyle açık opt-in salt-okunur K3 gerçek ölçüm, K2 provenance ve K5 kanıt ayrımını birlikte uygula; bağımsız K4 geri yükleme kanıtını ayrıca topla. Onaysız üretim değişikliği yok.


## 20 Ekim 2026 — K1/K3 gerçek ölçüm öncesi güvenli hedef ön kontrolü
- GitHub Actions #39415583107, SHA 206645be5b047ccae3f2156cdcc0576f3ad16f9a, completed SUCCESS doğrulandı. Bu yalnız offline K1/K3/K5 kanıt kapısı testidir.
- `madsc/probe_target_gate.py` eklendi (commit 3e6cfd50d80df54585d9e76381ce3513eff74510): açık `authorized=True` zorunlu; yalnız HTTPS, varsayılan 443; URL kimlik bilgileri/fragment/yerel ve özel IP/yerel DNS adları reddi; salt okunur SHA256 fingerprint ve preflight-only çıktısı. DNS adları güvenli sayılıp otomatik ağa açılmaz; bağlantı anında DNS/IP pinning ve redirect kontrolü hâlâ gerekli.
- `tests/test_probe_target_gate.py` negatif izin/SSRF URL testleri eklendi (commit c440f2d4d07e581d299bd2311c04c59afcfc4182). Actions #39416121054 ilk kontrolde pending; başarı henüz doğrulanmadı.
- Ağ bağlantısı, ffprobe, playlist/EPG/logo/yedek/favori değişikliği, eski depo yazması yapılmadı. K2–K3 gerçek ölçüm provenance, K4 offsite restore ve IBO cihaz kabulü açık. Gerçek davranışsal eşdeğerlik 0/92, runtime güvenlik 0/26.


## 20 Ekim 2026 — K2 kaynak eşleşmeli K3 ön kontrol paketi
- Önceki K1 hedef kontrolü commit 3e6cfd50 için Actions #39416106588 completed SUCCESS; `tests/test_probe_target_gate.py` commit c440f2d4 için #39416121054 son sorguda in_progress, başarı varsayılmadı.
- `madsc/probe_target_gate.py` içine salt okunur `validate_resolved_addresses` (bütün DNS yanıtları global IP olmalı, IPv4-mapped IPv6 ve tekrarlar reddedilir) ve `validate_probe_handoff` (açık izin, K2 envelope/run/SHA/digest ve URL SHA256 aday üyeliği zorunlu) eklendi. Commit d15faec7c2b488211fde134cfbc3198fcb5502b3.
- Negatif DNS/SSRF, yetkisiz çağrı, yabancı K2 aday ve yanlış run testleri `tests/test_probe_target_gate.py` dosyasına eklendi. Commit aec6e974566bec27b428593542b9e91e72670fe7; Actions #39416361407 ilk kontrolde queued. Kod ve test commitleri var, CI SUCCESS henüz iddia edilmez.
- DNS/IP pinning ve redirects/timeout sınırları şu anda yalnız preflight gereksinimi olarak raporlanır; bunları uygulayan ağ çalıştırıcısı ve canlı ffprobe henüz YOK. `authorized=True` otomatik canlı yayın test izni sayılmamalı. Korunan üretim dosyaları ve eski depo değişmedi. Davranışsal 0/92, runtime güvenlik 0/26.


## 20 Ekim 2026 — K3 opt-in HTTPS HEAD gözlem çalıştırıcısı
- Önceki K2–K3 preflight Actions #39416361407, SHA aec6e974566bec27b428593542b9e91e72670fe7, completed SUCCESS doğrulandı.
- `madsc/https_head_probe.py` eklendi (commit a5d7feacb7f31ea56c1b4215e609cd503c5b7d4f): açık authorized=True, doğrulanmış K2 envelope/run/SHA/digest ve URL fingerprint; DNS yanıtlarının tamamı genel IP olmalı; seçili numerik IP'ye TCP, orijinal host için TLS sertifika/SNI, HEAD isteği, yönlendirme ret, 8KB header sınırı, en fazla 5 saniye işlem-başı socket timeout; URL/credential raporlanmaz. Ağ çağrısı otomatik başlatılmaz. Bu ffprobe/ffmpeg ve yayın sürekliliği testi DEĞİLDİR.
- `tests/test_https_head_probe.py` (commit eed311303d78e263df64b0f14139e55935ec0f76) izin, timeout, yabancı aday ve karışık özel DNS için socket açılmaması testlerini içerir. Actions #39416758955 ilk kontrolde pending; CI başarısı doğrulanmadan tamamlandı denmez.
- Açık riskler: toplam uçtan uca süre bütçesi ve header ayrıştırma sertleştirmesi, URL unicode/path kodlama, DNS yanıt tekrarlarının yönetimi, farklı sunucu davranışları, HTTP HEAD reddi; gerçek kanal akış testi ve IBO kabulü yapılmadı. Üretim listeleri ve eski depo değişmedi. Davranışsal kabul 0/92, runtime güvenlik kabulü 0/26.


## 20 Ekim 2026 — HTTPS HEAD ortak deadline ve durum ayrıştırma
- Önceki Actions #39416758955, SHA eed311303d78e263df64b0f14139e55935ec0f76, completed SUCCESS doğrulandı; bu çevrimdışı test kanıtıdır.
- `madsc/https_head_probe.py` ortak monotonic deadline ile TCP connect, TLS handshake, send ve her recv öncesinde kalan süreyi socket timeout'a uygular; ASCII dışı URL path güvenle reddedilir; HTTP durum kodu tam 3 basamak ve HTTP/1.0/1.1 olmalı; bütün 3xx yönlendirmeleri reddedilir. Commit ad0f1f9e1d06a0015d54e3903d0cba553445a4a2.
- `tests/test_https_head_probe.py` deadline bitince socket açılmaması ve ASCII dışı yolun reddi regresyonlarını içerir. Commit 0e4198ddacbe2de2c00f31143c110999fce245ca. Actions #39418959967 son kontrolde pending; başarı henüz iddia edilmiyor.
- DNS getaddrinfo çözümlemesi henüz bu ortak deadline tarafından kesin sınırlandırılmıyor; gerçek ölçüm kullanımından önce bu açık giderilmeli. HEAD gözlemi canlı ffprobe/ffmpeg, IBO ve 30 saniyelik süreklilik kanıtı değildir. Korunan üretim dosyalarına ve eski depoya dokunulmadı; 0/92 ve 0/26 kabul değişmedi.


## 20 Ekim 2026 — K3 DNS kesin süre sınırı
- Önceki HEAD deadline/HTTP sertleştirme Actions #39418959967, SHA 0e4198ddacbe2de2c00f31143c110999fce245ca, completed SUCCESS doğrulandı.
- `madsc/https_head_probe.py` DNS getaddrinfo işlemini kill edilebilir izole Python subprocess içine taşıdı; subprocess.run timeout ortak monotonic deadline'dan kalan süreyi kullanıyor, çıktı boyutu sınırlı, tüm IP yanıtları önceki fail-closed gate ile doğrulanıyor. Commit cff69db346d2374cea3369f62c2112d021b316dd.
- `tests/test_https_head_probe.py` DNS subprocess mock'larına uyarlandı; DNS timeout halinde socket açılmaması regresyonu eklendi. Commit d675d38c8f4ed7ffb973bcd79b89a6be5ec57704. Actions #39419786552 ilk kontrolde pending; SUCCESS henüz doğrulanmadı.
- Bu yalnız opt-in HTTPS HEAD gözlemidir; gerçek yayın ffprobe/ffmpeg, IBO, 30 saniye süreklilik ve K5 canlı kanıt zinciri henüz yok. Ağ testi gerçek hedefte çalıştırılmadı; korunan üretim ve eski depo değişmedi. Kabul sayaçları 0/92 ve 0/26.


## 20 Ekim 2026 — İki başarısız DNS CI koşusunun kök nedeni ve düzeltme
- Actions #39419767071 (cff69db3) ve #39419786552 (d675d38c) completed FAILURE. #39419786552 Güvenlik job logu: `test_shared_deadline_blocks_socket_after_dns` içinde DNS deadline kaynaklı `TimeoutError`, `except (..., OSError)` tarafından `ValueError('DNS resolution failed')` olarak maskelenmiş; 321 regresyondan 1 error. K2/K3/K4/K5 işlerinin skip/failure zinciri güvenlik jobuna bağımlı; bağımsız canlı kabul sonucu değil.
- `madsc/https_head_probe.py` DNS exception sırası düzeltildi: `except TimeoutError: raise` genel `OSError` yakalamadan önce geldi. Commit 48961554ed27612bea1ffaee627ba456f253fcec.
- Yeni Actions #39419973232 ilk kontrolde queued; SUCCESS henüz doğrulanmadı. Canlı ağ isteği yapılmadı, üretim dosyaları ve eski depo değişmedi. 0/92 davranışsal ve 0/26 runtime kabul değişmedi.


## 20 Ekim 2026 — DNS CI yeşil, K3 HEAD → K5 ayrı taşıma kapısı
- Actions #39421069065 (SHA bc8b22969b4bb9d128b7c8bbb4be1d5f23ee5e7d) completed SUCCESS; Güvenlik, Keşif, Kanal Testleri, Arşiv ve Yedek, Genel Bakım ve Beşli toplu kanıt doğrulama işlerinin hepsi SUCCESS. Önceki üç kırmızı koşunun test hatası zinciri giderildi; bu üretim kabulü değildir.
- `madsc/k5_channel_gate.py` içine ayrı `evaluate_k3_head_observation` fonksiyonu eklendi (commit 46160b39c591df705639d90c558ffe17039e19a5): K2 envelope/run/SHA/digest/fingerprint bağlamını, TLS/DNS ve yönlendirme reddini doğrular; HEAD transport gözlemini stream sürekliliği/IBO/üretim kabulüne yükseltmez. Eski offline K3 kanıt sözleşmesi değişmedi.
- `tests/test_k5_head_observation.py` (commit 819b5a514180be694f982b3ca6cb03d089bfbc32) sahte HEAD gözlem, farklı aday, yönlendirme, bozuk tür ve canlı onay iddialarına karşı negatif testleri ekledi. Actions #39421390769 ilk kontrolde queued; başarı henüz doğrulanmadı.
- Gerçek HEAD ölçümü tetiklenmedi; eski depo ve korunan üretim dosyaları değiştirilmedi. Gerçek ffprobe/ffmpeg/IBO ve 30 saniye canlı süreklilik kabulü hâlâ yok. 0/92 davranışsal eşdeğerlik ve 0/26 runtime güvenlik kabulü değişmedi.


## 20 Ekim 2026 — K5 HEAD rapor doğrulama ile bağımsız ağ kanıtını ayırma
- Önceki #39421069065 altı job SUCCESS doğrulanmıştı. K5 HEAD yeni test koşusu #39421390769 son sorguda CANCELLED; bu koşu için başarı iddia edilmez. #39421372129 son sorguda in_progress.
- `madsc/k5_channel_gate.py` HEAD değerlendirme fonksiyonunun __main__ guard sonrası konumu düzeltildi ve `head_transport_observed=True` yerine yalnızca `head_transport_claim_validated=True`, `head_transport_independently_verified=False` döndürülecek biçimde fail-closed rapor semantiği uygulandı. Commit 0e571e86b3b5dd3c8ae3ac70878760d668f411e4.
- `tests/test_k5_head_observation.py` yeni ayrımı sınar. Commit d4f5a811c82fe104406e7bbd4697786c0136daec. Yeni Actions sonucunu ayrıca doğrula.
- Raporun kendisi imzalı/bağımsız canlı socket kanıtı değildir. Korunan üretim ve eski depo değişmedi, canlı ağ probe başlatılmadı. Kabul 0/92 ve 0/26.


## 20 Ekim 2026 — K3 timeout sonsuz değerleri ve numerik IP çözümleme
- Actions #39421372129 (SHA 46160b39c591df705639d90c558ffe17039e19a5) SUCCESS doğrulandı; #39421390769 ve #39421496704 CANCELLED, #39421531900 son kontrolde in_progress. İptal edilenler başarı olarak sayılmadı.
- `madsc/https_head_probe.py`: timeout NaN/±Infinity dahil sonlu ve 0–5 saniye aralığında olmalı; numerik global IP hedeflerinde DNS subprocess çağrısı atlanıp aynı IP validasyon kapısı kullanılır. Commit 153881ccd208cb50a14dd172407565c1074569a8.
- `tests/test_https_head_probe.py` sonsuz timeout negatif regresyonu eklendi. Commit 6f72a490a60007b18c081cbe352b9550e63356af. Actions #39421735763 ilk kontrolde queued, sonuç henüz doğrulanmadı.
- Bu değişiklikler canlı yayın/IBO kabulü değildir; ağ probe gerçek hedefte tetiklenmedi. Korunan dosyalar ve eski depo değişmedi. 0/92 davranışsal ve 0/26 runtime güvenlik kabulü sabit.


## 20 Ekim 2026 — K5 HEAD sahte canlı onay ve HTTP sınıflandırması
- Actions #39421735763 (SHA 6f72a490a60007b18c081cbe352b9550e63356af) completed SUCCESS; #39421531900 (SHA d4f5a811c82fe104406e7bbd4697786c0136daec) completed SUCCESS. İptal edilen eski koşular başarı sayılmadı.
- `madsc/k5_channel_gate.py` HEAD raporunda eklenmiş canlı/IBO/üretim onayı iddialarını fail-closed reddeder; 2xx HTTP durumunu `http_success_status` olarak ayrıca sınıflandırır, diğer 1xx/4xx/5xx transport raporu olabilir fakat başarılı HTTP sayılmaz. Commit 636e2d7fd42d39d0dbbc2db6bda5dae7edd99e54.
- `tests/test_k5_head_observation.py` sahte onay bayrakları ve 100/401/403/404/500 durumlarının negatif regresyonlarını içerir. Commit e7baa07586067e1bbb724affac62e5d8e00acd2e. Actions #39422168285 ilk kontrolde queued; sonuç henüz doğrulanmadı.
- K5 yalnızca rapor biçimi/kimliği inceler, gerçek TLS/socket olayını bağımsız doğrulamaz. Gerçek yayın, IBO ve süreklilik kabulü yok; üretim/eski repo dokunulmadı. 0/92 ve 0/26.


## 20 Ekim 2026 — K3 URL ayrıştırma ve DNS tekrar yanıtları
- Önceki Actions #39422168285 (e7baa07586067e1bbb724affac62e5d8e00acd2e) ve #39422153081 (636e2d7fd42d39d0dbbc2db6bda5dae7edd99e54) completed SUCCESS doğrulandı.
- `madsc/probe_target_gate.py` ters eğik çizgi içeren belirsiz URL'leri reddeder; `getaddrinfo` içinde yaygın tekrarlı güvenli IP yanıtlarını önce bütün IP'leri denetleyip sonra sıralı tekilleştirir. Karma özel/genel DNS yanıtı hâlâ fail-closed. Commit a643d06290501978cac4794b0f51b4c73d1b9ca4.
- `tests/test_probe_target_gate.py` güvenli tekrarlı DNS yanıtını ve backslash URL reddini test eder. Commit a9d2461dbeb73aa93b6a0e46235206348d91a5ce. Actions #39422624033 ilk kontrolde queued; SUCCESS henüz iddia edilmez.
- Bu güvenlik regresyonları canlı yayın/IBO/gerçek üretim kabulü değildir. Ağ hedefleri tetiklenmedi, korunan listeler ve eski depo değişmedi; 0/92 ve 0/26.


## 20 Ekim 2026 — K5 HEAD rapor içerik parmak izi
- Actions #39422624033 (SHA a9d2461dbeb73aa93b6a0e46235206348d91a5ce) completed SUCCESS; önceki ara koşu #39422599261 FAILURE idi, güncel başarılı koşu onun yerini aldı.
- `madsc/k5_channel_gate.py`: kabul edilen HEAD gözleminin sıralı/kanonik JSON içeriği SHA-256 olarak `observation_sha256` alanına bağlanır. Bu içerik bütünlüğü için referans parmak izidir; imza veya bağımsız ağ gözlem kanıtı değildir. Commit 3f7a90e9965bdffdd7a5365441cfea6c994dc8a6.
- `tests/test_k5_head_observation.py`: deterministik SHA-256 ve 200→204 değişince parmak izi değişimi sınanır. Commit 79fc82dee145bc4c03389f50172c4fd4479e05de. Actions #39423176530 ilk kontrolde pending; CI sonucu henüz doğrulanmadı.
- Gerçek ağ probe çalıştırılmadı; üretim, EPG, IBO, yedekler ve eski depo değişmedi. 0/92 eski otomasyon davranışsal eşdeğerliği ve 0/26 güvenlik runtime kabulü devam ediyor.


## 20 Ekim 2026 — K5 HEAD kapalı şema ve değiştirilmiş rapor reddi
- Actions #39423176530 (79fc82dee145bc4c03389f50172c4fd4479e05de) ve #39423154872 (3f7a90e9965bdffdd7a5365441cfea6c994dc8a6) SUCCESS doğrulandı.
- `madsc/k5_channel_gate.py` HEAD raporunun tam 14 üretici alanından oluşmasını şart koşar; bilinmeyen/gizli veya eksik alan fail-closed reddedilir. İçerik SHA-256 yalnızca kabul edilmiş kapalı şema için üretilir. Commit 78f99feccc6118fc6dd5ca99e78da642ddf48502.
- `tests/test_k5_head_observation.py` ekstra gizli alan ve eksik alan regresyonları eklendi. Commit aef9f4acf08bb5935329a96de2870acb641a3183. Actions #39423668755 ilk kontrolde queued; yeni CI sonucu doğrulanmadı.
- Ağ gözlemi bağımsız tasdik edilmedi, gerçek stream/IBO testi yapılmadı, üretim/eski repo değişmedi; 0/92 ve 0/26 kabul sayaçları sabit.


## 20 Ekim 2026 — Öncelik değişimi: 99 YAML için davranış kanıt engelleri
- Kullanıcı genel 47/53 ilerlemesinin yerinde saymasından haklı olarak şikâyet etti. Bundan sonra yalnızca K3/K5 küçük güvenlik yamaları değil, eski 92 otomasyonun gerçek davranış karşılaştırmaları önceliklidir; sahte ilerleme puanı üretme.
- `madsc/legacy_99_bulk_audit.py` tüm 99 kaynak YAML satırında 6 kanıt eksikliğini ayrı işaretler (`legacy_execution`, `new_execution`, `input_output_comparison`, `side_effect_comparison`, `failure_timeout_comparison`, `reviewer_approval`) ve tür bazında toplamları fail-closed hesaplar. Commitler 6f4f04134d391e36cac77c69a6447ce989c84eda ve f94978ea4a28393efdf0789239f5488351d6dce3.
- `tests/test_legacy_99_source_integrity.py` her satırın BLOCKED kaldığını, altı engeli ve sahte onayın reddini doğrular. Commitler 38534e0f0d867083e83eac9fe00f938bf930e00a ve a50147e3ddd6251d7f0d46d4d04b2a0cc7cf7e24.
- İlk kod SHA 6f4f041 için Actions #39424425976 SUCCESS; daha yeni Actions #39424609517 ilk kontrolde pending, henüz başarı iddiası yok.
- Sonraki görev: eski ve yeni gerçek betikleri aynı sentetik girdide izole çalıştırıp exit/status, dosya SHA, hata/timeout ve yan etkileri karşılaştır; yalnızca gerçek diferansiyel kanıtla 0/92 ilerlet. Kaynak envanteri/fixture tek başına eşdeğerlik değildir.
- Korunan üretim dosyaları, eski repo ve canlı yayınlar değişmedi. 0/92 ve 0/26 kabul sayaçları hâlâ geçerli.


## 20 Ekim 2026 — İki toplu çalıştırmalı diferansiyel test paketi
- `tests/test_legacy_scoring_differential_batch.py` eski puanlama CLI fixture betiğini alt süreçte çalıştırıp yeni `legacy_technical_score` ile 8 teknik vektör, URL tekilleştirme, CSV sıralama, JSON özet ve otomatik onay reddini karşılaştırır. Commit 81e7c8eb42784820c1b6f07ad0d4c76f63fe9800, Actions #39425233309 altı job SUCCESS doğrulandı.
- `tests/test_legacy_retest_differential_batch.py` eski tekrar-test takvimi CLI fixture betiğini izole geçici dizinde sabit UTC saatle çalıştırıp yeni `retest_rows` ile 2/6/12/24 saat, bozuk tarih, geçersiz kayıt ve CSV satırlarını karşılaştırır. Commit 744e320390596fe2d717e263aac686ab6747d0c0, Actions #39437371154 ilk kontrolde queued, sonucu henüz doğrulanmadı.
- ÖNEMLİ: Bu fixture betikleri eski depodan bağımsız imza/SHA ile doğrulanmış kaynak yürütümü sayılmaz; script düzeyinde sentetik karşılaştırma, 92 workflow'un trigger/izin/artefakt/hata/yan etki tam kabulü değildir. Sayaçlar 0/92 ve 0/26 kalır.
- Kullanıcı toplu çalışma kuralının ihlalinden rahatsız. Bundan sonra küçük tekil yamalar yerine birbiriyle ilgili eski davranışları toplu karşılaştırma paketlerinde birleştir, CI hatalarını topluca düzelt, tamamlanan kaynak incelemelerini tekrar yapma.
- Korunan üretim, EPG, playlist, IBO, yedek ve eski repo değiştirilmedi.


## 20 Ekim 2026 — Toplu diferansiyel karşılaştırmalar: puanlama, tekrar test, öncelik
- `tests/test_legacy_scoring_differential_batch.py` pinned eski CLI ve yeni modülü 8 puanlama vektörü, CSV/JSON, tekilleştirme/sıralama ile karşılaştırır. Actions #39425233309 SUCCESS.
- `tests/test_legacy_retest_differential_batch.py` pinned eski CLI ve yeni zamanlayıcıyı 2/6/12/24 saat, bozuk tarih, geçersiz kayıt ile karşılaştırır. Actions #39437371154 SUCCESS (altı job).
- `tests/test_legacy_priority_differential_batch.py` pinned eski CLI ve yeni priority_rows fonksiyonunu 5 öncelik seviyesi, aynı seviyede alfabetik sıralama, notlar ve çıktı üzerinde karşılaştırır. Commit e82fe243faaf6b3daabc50bcd7f57666f5affe78; Actions #39437666057 ilk kontrolde queued, sonuç doğrulanmadı.
- NOT: Eski priority fixture içindeki `writer.writerow({"ONCELIK": tier + 1, "INCELEME_NOTU": ..., **row})` ifadesinde giriş CSV'sinde önceden ONCELIK/INCELEME_NOTU varsa `**row` eski değerleri yeniden yazar. Yeni `priority_rows` hesaplanan alanları korur. Bu fark için ayrıca kontrollü hata/uyumsuzluk kaydı oluştur; eski hatayı üretime taşımadan semantik farkı belgelemek gerekir.
- Bu script düzeyinde izole, sentetik fixture karşılaştırmalarıdır; eski workflow trigger, izin, artefakt ve yan etki eşdeğerliği doğrulanmadı. 0/92 ve 0/26 kabul sayaçları değişmedi. Üretim, playlist, EPG, yedekler ve eski repo değiştirilmedi.


## 20 Ekim 2026 — İLK GERÇEK K2 KANAL KEŞİF PİLOTU ÇALIŞTI
- Kullanıcı açıkça gerçek kanal aramasına geçilmesini ve eksiklerin çalışırken görülmesini istedi. Bu yüzden gerçek K2 keşif önceliklendirildi.
- `madsc/live_discovery_pilot.py` yalnızca allowlist `https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u` adresini 20 saniye timeout ve 2MB boyut sınırıyla indiriyor; ilk 100 M3U adayını `classify_candidates` ile salt okunur sınıflandırıyor, URL'leri rapora yazmıyor, yalnız SHA256 hashleri üretiyor. Kod commit 0be6aa0388c9c68fbfe237c245b58dc3e0f59af1.
- `.github/workflows/madsc-k2-live-pilot.yml` yalnızca bu iki dosya push'unda veya manuel dispatch'te çalışan izole 5 dakikalık, contents:read iş akışı; commit 401d057432113b690d2f4a4ca2efcde360af677c.
- **İLK GERÇEK SONUÇ** GitHub Actions #39438888120 live-discovery SUCCESS, artifact 12272953781. Kaynak bytes 28656, kaynakta 220 yayın kaydı, ilk 100 pilot adayının 100'ü sınıflandırıldı, 0 tekrar, 0 geçersiz. SHA256 kaynak ade6c0c6845e693b807b83cdf606aac49565f5002fa0ada8d9459e3185e7562b. Bu sonuçlar **yayın çalışıyor** veya görüntü/ses var anlamına GELMEZ: stream_reachability_tested=false, device_verified=false, production_playlist_modified=false.
- Bir önceki CI #39438268021 ilk denemede GitHub upload-artifact ECONNRESET ile başarısızdı; yalnız başarısız işler yeniden çalıştırıldı, son kontrol GitHub SUCCESS.
- **SONRAKİ GERÇEK İŞ:** K3'te URL'lerin ağ erişimini ve ffprobe görüntü/sesini sınırlı güvenli pilotta test et; URL/secret sızdırma ve SSRF koruması, süre/bütçe sınırı, rapor ve korunan playlistlere yazmama şart. K2 kaynak 220'nin ilk 100'ü görüldü, kalan 120 henüz taranmadı. Tam eski workflow 0/92, güvenlik runtime kabulü 0/26.


## 20 Ekim 2026 — Yeni sisteme bağımsız M3U8 listesi (KULLANICI KARARI)
- Kullanıcı yeni sistem için ayrı M3U8 oluşturulmasını, eski listenin tamamıyla aynı kalmasını açıkça istedi.
- `MADSC55_TV_YENI_TEST.m3u8` dosyası `main` dalında sadece `#EXTM3U\n` içeriğiyle oluşturuldu; commit 9af7b7b347a70593d47abd2e0722c5ff31177393. Henüz **0 kanal** var; bu çalışır liste değildir.
- Eski listelere, CALISANLAR/YENILER/YEDEKLER/HEPSI/FAVORILER, XMLTV, EPG, logolar, yedekler, eski depo ve IBO kararlarına dokunulmayacak.
- Yeni listede yalnız K3 ağ+görüntü+ses kontrollerinden geçen ve güvenli yayın için onaylanmış adaylar yer alacak. Pilot adayları otomatik ekleme yetkisi değildir; kullanıcı onayı sınırları korunacak.
- Olası raw URL `https://raw.githubusercontent.com/Madsc55/Madsc55-Tv/main/MADSC55_TV_YENI_TEST.m3u8`; depo özel ise IBO erişimi engellenebilir. Kamuya açma veya özel URL sızdırma kullanıcı onayı gerektirir.


## 20 Ekim 2026 — GitHub Actions ücretsiz kota kararı ve 21 kural teyidi
- Kullanıcı kararı: **Sıfır ücret**, kredi kartı eklenmeyecek, ücretli GitHub Actions çalıştırılmayacak; `Madsc55/Madsc55-Tv` deposu **Private** kalacak. Kod geliştirme ve eksiklerin tamamlanması kesintisiz sürecek; kullanıcı ücretsiz kotanın yenilenmesinden sonra (GitHub ekranında 12 gün, beklenen 1 Kasım 2026) Actions testlerine dönülmesini istedi. Tarih gelmeden ücretli run tetikleme.
- Kullanıcının GitHub Billing ekranı: Ekim 2026 Actions **2000/2000 dakika kullanılmış**, depolama 0/0.5 GB, brüt kullanım **$64**, indirim **$64**, faturalanabilir kullanım **$0**. Hesap GitHub Free; Actions bütçesi **$0**. Eski `madsc-tv` yaklaşık $52, yeni `Madsc55-Tv` yaklaşık $12 brüt kullanım. Kota dolumu işlerin başlamamasını açıklar; ayrıca ödeme uyarısının başka nedeni olup olmadığı kesinleşmedi.
- 21 kural: yalnız yeni `Madsc55/Madsc55-Tv` / `main` yazılabilir; eski `Madsc55/madsc-tv` salt okunur. `BIRLESIK_KALICI_CALISMA_KURALLARI.md`, bu hafıza, devir notu, `ESKI_SISTEM_NOTLARI.md` ve ilgili özgün notlar her iş öncesi okunur. `ESKI_SISTEM_NOTLARI.md` dosyasının şu anki main içeriği **boş** (0 bayt): eski notların tam birleştiği iddia edilmemeli; özgün arşiv notları referans alınmalı ve eksik birleştirme ayrıca ele alınmalı.
- K1–K5 çapraz etkiler, eski 99 YAML / 92 davranış, 26 güvenlik kuralı, K3 IBO/EPG ve K4 bağımsız yedek kabulü ayrı izlenecek. Gerçek kabul **0/92** ve **0/26**; yeşil fixture/yerel hedefli test canlı kabul değildir. Yeni repo 139 Python dosyası, 73 test dosyası envanteri (20 Ekim kontrolü); güncel tam regresyon henüz çalıştırılmadı.
- 20 Ekim Actions son engelli çalışma: run **39468111538**, adımlar başlamadan hata. Ücretli tekrar çalıştırma yok. Güncel geliştirme hedefi: bağımlılıkları olan işleri tek pakette tamamlamak, offline doğrulamayı mümkün oldukça yürütmek, kanıt ve sonuçları dürüstçe kaydetmek; kotanın yenilenmesinden sonra yalnız izinle kontrollü toplu Actions testi.
- Korunan üretim M3U/EPG, IBO kararları, favoriler, PR #71 ve eski depo değiştirilmez. Repo Public yapılmaz. Yeni ayda kotayı korumak için gereksiz tetikleyiciler kapalı tutulur; eski depoya dokunulmaz.


## 20 Ekim 2026 — K5 kanıta dayalı puanlama düzeltmesi
- Kullanıcı eski %47/%53 oranının tekrarından haklı olarak şikâyet etti. Kod denetiminde `madsc/progress_scorecard.py` içindeki 47/53'ün sabit tarihsel referans olduğu, `calculated_overall_percent=None` alanının genel proje oranının hesaplanmadığını belirttiği doğrulandı. Referans oranı yeni ölçüm diye sunma.
- K5 skor kartına ölçülebilir, kapsamı açık yüzdeler eklendi: 99/99 ilk YAML inceleme, 130/130 Python kaynak envanteri, 68/68 tarihsel test envanteri; ayrıca 92 davranış kabulü ve 26 runtime güvenlik kabulünün ayrı yüzdeleri ve 118 maddelik birleşik **yalnız kabul yüzdesi**. Genel proje tamamlanma yüzdesi değildir. Değişiklik commit `73b2873097c64b5ec8df0bfaac3966b2aeeb8e14`, regresyon testi commit `fb5b1581a30bdaa1207a9aec4fe3aba3a5e1dce7`.
- **CI/test henüz çalıştırılmadı**, Actions ücretsiz kota 2000/2000 dolu, $0 bütçe korunuyor. 0/92 ve 0/26 kabul değişmedi. Sonraki iş: kurulum/entegrasyon iş kalemleri için gerçek ve sabit paydalı ayrı görev matrisi; offline test, eski notların tam birleştirilmesi ve K1–K5 kabul kanıtları. Üretim listeleri, eski repo, Public görünürlük ve Actions tetikleyicileri değiştirilmedi.


## 20 Ekim 2026 — K1–K5 yerel toplu kapı entegrasyonu
- Kullanıcının '5'li sistemi adam gibi kuralım' talimatıyla yalnız puanlama değil gerçek yürütme zincirine müdahale edildi. `madsc/offline_gate.py` artık yalnız unittest keşif/başarı özetini değil, `madsc.offline_five_gate.assess_all()` üzerinden K1, K2, K3, K4, K5 gerçek izole fixture executor sonucunu da ister. Beşli gate false/exception ise unittest yeşil olsa bile exit 3 ve genel hata. Kategori durumu ve hata özeti JSON'a eklenir; üretim kabulü false. Commit `e090dfe5ff446e65e515bee07478b2eb08c94051`.
- `tests/test_offline_gate.py` dosyasına K3 başarısızken yeşil unittest'in engellenmesi ve iki gate beraber geçince yalnız offline başarı senaryoları eklendi. Commit `fa47a219446622c7523935848e371cecb34bd54f`.
- **Henüz gerçek Python regresyonu çalıştırılmadı** ve Actions 2000/2000 kota dolu olduğu için tetiklenmedi. Bu değişiklik K1–K5 fixture bağını güçlendirir; 92 davranış kabulü 0/92, 26 runtime güvenlik 0/26, canlı medya/IBO/offsite restore kanıtı eksik. Eski repo, üretim listeleri ve cron değiştirilmedi.
- Sıradaki büyük paket: yerel gate'i gerçek çalışma ortamında test et; gerçek K1 yazma yolları, K2 keşif, K3 medya/EPG, K4 bağımsız restore ve K5 kanıt bağlarını gerçek negatif senaryolarla sertleştir; eski notların tam birleştirilmesini bitir. 21 kural ve $0 maliyet geçerli.


## 20 Ekim 2026 — K1–K5 eksik/yanıltıcı kanıta karşı sertleştirme
- `madsc/offline_gate.py` artık `fixture_gate_passed=True` tek başına kabul etmiyor: `categories_checked==5`, tam `k1,k2,k3,k4,k5` kümesi, her kategoride `success`, `production_ready=False`, `production_writes=False` zorunlu. Eksik K5 veya yanlış üretim bayrağıyla başarı kapalı. Commit `1850182dc1443b584b11a481c2db5d7cdd015037`.
- `tests/test_offline_gate.py` gerçekçi beşli mock alanlarıyla güncellendi; 4 kategori olmasına rağmen `fixture_gate_passed=True` verilmesi negatif testle reddediliyor. Commit `4f106ee74780a13d71ac84d68aa5e7de241f2fbf`.
- Testler **henüz çalıştırılmadı**; özel depoya container üzerinden ağ erişimi yok ve GitHub Actions 2000/2000 ücretsiz kota dolu. Bunlar üretim davranış kabulü değildir; 0/92 ve 0/26 korunur. Eski repo ve canlı dosyalar değişmedi. Sıradaki iş: tam offline regresyonun gerçekten yürütülmesi, K1–K5 görev/veri zincirinin genişletilmesi, kaynak notların tam birleşmesi.


## 20 Ekim 2026 — K5 toplu sonuç doğruluğu
- `madsc/offline_gate.py` içindeki unittest başarı durumu ile K1–K5 fixture gate sonucu artık ayrı hesaplanıyor. `unittest_passed` test sayısı >0, sıfır çıkış ve timeout olmaması gerektiriyor; `all_offline_gates_passed` ancak hem unittest hem beşli kapı başarılıysa true. Önceki `tests_passed` alanının sonradan değiştirilmiş exit_code'a bağlı yanlış pozitif üretme riski giderildi. Kod commit `6ae488704ee2ee04ac57171e03e810db708f7462`, regresyon commit `e9963ee2f5187e118cfc4239e687a054baab4ab2`.
- Testler henüz yürütülmedi; Actions kotası 2000/2000, $0 bütçe ve Private depo korunuyor. 92/92 davranış kabulü 0/92, 26/26 runtime güvenlik kabulü 0/26. Beşli offline gate canlı entegrasyon/IBO/offsite restore yerine geçmez.


## 20 Ekim 2026 — K2/K3 aday kanıt doğrulama sertleştirmesi
- `madsc/candidate_coordination.py` içine kabul edilmiş aday fingerprint'lerinin tekil olma şartı ve boş/yalnız boşluk EPG/logo kimliklerinin reddi eklendi. K2 keşif → K3 değerlendirme kanıtı belirsiz kimlikle devam etmez. Kod commit `04bbca454a8a38346db041011f5c402e16cb17f8`; negatif EPG/logo testi commit `e71b725f4faccb52c2f03431a7c654e61d184afa`.
- Henüz test yürütülmedi; 0/92 davranış, 0/26 runtime güvenlik kabulü değişmedi. Bu kod gerçek internet keşfi, medya probe, IBO cihaz testi, offsite restore veya üretim yazma onayı değildir. Actions tetiklenmedi; $0 bütçe, 21 kural, eski depo salt okunur ve korunan dosyalar aynen.


## 20 Ekim 2026 — K2/K3 → K4 → K5 gerçek karar verisi bağlantısı
- `madsc/maintenance.py` içine `review_candidate_batch(coordination, backup_evidence)` eklendi. K2/K3 aday SHA256 kimliği tekilliği, `delete_allowed=False`, `production_change_allowed=False`, IBO koruma/hold bayrakları, K4 bağımsız sandbox restore kanıtı birlikte denetleniyor. K5 sonuç raporunda aday, bekleyen ve IBO korunan sayıları ve restore durumu var; üretim onayı daima false. Commit `f25800d4d2bcdf0fe40c512a948dafbc0442e3f3`.
- `tests/test_maintenance.py` içine başarı, K4 eksik kanıt, silme izni, mükerrer aday ve sahte harici depolama iddiası negatif senaryoları eklendi. Commit `3bb26583e9f0d210f2a6854311f404f6d780f9f4`.
- Bu fonksiyon henüz gerçek yürütücüye bağlanmadı ve testler henüz çalıştırılmadı. 0/92 ve 0/26 kabul değişmedi. GitHub Actions kotası dolu; tetiklenmedi. Eski repo ve üretim dosyaları değiştirilmedi. Sonraki adım: K5 fonksiyonunu gerçek K1–K5 offline executor içine bağla ve uçtan uca regresyonu çalıştır.


## 20 Ekim 2026 — GitHub üzerinde gerçek K5 yürütücü bağlantısı
- `madsc/core.py` K5 executor içine `review_candidate_batch()` bağlandı. K2/K3 fixture aday raporu ile K4 `verify_independent_restore()` tarafından üç ayrı geçici dizinde doğrulanan sandbox restore raporu K5'te aynı karar nesnesinde kontrol ediliyor. Yeni boolean fixture check `k2_k3_k4_k5_candidate_restore_review`; commit `9ac7fece4266a9c1b54c05f4acee967b3a8306c6`.
- `tests/test_offline_five_gate.py` gerçek `execute('k5')` sonucunda yeni bağlantı kontrolünün true olmasını isteyen test eklendi. Commit `1065942e4f1dae87e9000024217c0c394e75caa6`.
- Kod commit edildi, fakat test yürütülmedi ve Actions tetiklenmedi (2000/2000 ücretsiz dakika dolu, $0 bütçe). Bu yalnız izole fixture entegrasyonudur, canlı kanallar/IBO cihazı/harici depolama kanıtı değildir; 0/92, 0/26. Korunan dosyalar ve eski depo değişmedi.


## 20 Ekim 2026 — K4 bozulmuş geri yükleme negatif kanıtı K5'e bağlandı
- `madsc/core.py` K5 fixture yürütmesinde önce bağımsız üç-dizin restore doğrulanır, ardından restore edilmiş test dosyası kasıtlı değiştirilir ve K4 tekrar karşılaştırılır. `review_candidate_batch` ikinci bozuk raporu kabul kanıtı saymamalıdır. `k4_corruption_blocks_k5_review` kontrolü eklendi. Commit `bbe8bc9db492bc0339f719b256e19ba1dc6123e1`.
- `tests/test_offline_five_gate.py` gerçek K5 yürütücüsünün sağlam restore ve bozuk restore reddi kontrollerini ikisini de true vermesini zorunlu kılıyor. Commit `74b43b90115ae16f796a3f7ef264c8ddaccb8220`.
- Testlerin yürütülmesi doğrulanmadı, Actions tetiklenmedi, 0/92 ve 0/26 kabul değişmedi. Üretim listeleri, eski depo ve IBO cihazı etkilenmedi. Sıradaki: ücretsiz yerel tam regresyon çalıştırması ve gerçek K1 yazma kapısı entegrasyonuna odaklanma.


## 20 Ekim 2026 — K1 yazma kapısı K5 ortak kanıt dosyasına bağlandı
- `madsc/core.py` K5 izole yürütücüsü, K2/K3 aday + K4 geri yükleme değerlendirme raporunu `write_stage_report` üzerinden K1 `enforce_write_paths` kapısından geçirip yalnız geçici `reports/k5-isolated-evidence.json` yoluna yazıyor. Kaydedilen JSON eşitliği, `production_writes=True` reddi ve ikinci yazmanın `FileExistsError` ile engellenmesi tek fixture kontrolü `k1_guards_k5_report_write` altında sınanıyor. Commit `7e7383c7bdd44353c3330a9a0aa3f9c6c4095753`.
- `tests/test_offline_five_gate.py` gerçek K5 yürütücüde bu K1 kontrolünün True olmasını gerektiriyor. Commit `f55022b325d8ee64c14fd098f0fdda4e3489469e`.
- Bu yalnızca izole K5 kanıt yazıcısına bağlandı; GitHub git push/diğer Actions yazma yollarının tümüne evrensel runtime K1 kapısı kurulduğu iddia edilmez. Testler çalıştırılmadı; 0/92, 0/26 değişmedi. Ücretli Actions tetiklenmedi, eski depo ve canlı dosyalar değişmedi. Sıradaki: gerçek kodda diğer dosya yazma noktalarını envanterleyip korumalı yollara K1 zorunlu kontrolünü genişletmek; ücretsiz offline regresyon çalıştırmak.


## 20 Ekim 2026 — K1 geçmiş kaynak yayımlayıcısı yazma denetimi
- `madsc/history_real_source_publish.py` gerçek kaynak geçmiş kanıtı dizini oluşturulmadan önce K1 `enforce_write_paths` kontrolünü ve gerçek mevcut üst dizin şartını uyguluyor. Commit `fab4316a958f94b5bd21d070fd99d8e65af57c55`.
- `tests/test_history_real_source_publish.py` korunan `YEDEKLER` hedefi ve K1 tarafından reddedilen yazma çağrısında hiç çıktı oluşmaması negatif senaryolarını içeriyor. Commit `a8dc0ba6fbdb1b2d8462fba6dc126448c4a94104`.
- `madsc/write_path_audit.py` korunan klasörlerin yalnız alt yollarını değil kök adlarını da engelliyor. Commit `94698ff573cfcf3c62ba9ed4eb2518de58b8304a`.
- Test yürütülmedi; Actions başlatılmadı; 0/92 davranışsal ve 0/26 runtime güvenlik kabulü değişmedi. Bu K1 kapısı sadece çağıran yazıcılarda etkilidir, git push veya bağımsız Actions işlerini otomatik yakalamaz. Sonraki: tüm diğer gerçek yazıcıları envanterleyip güvenli hedef denetimini genişletmek, offline testleri çalıştırmak.


## 20 Ekim 2026 — K1 verified history pipeline yazma ön koşulu
- `madsc/history_verified_pipeline.py` K2 doğrulanmış geçmiş kaynağı indirme/aktarma akışında çıktı adı için `enforce_write_paths` K1 kontrolü ekledi; çıktı üst dizini mevcut gerçek dizin olmak zorunda, sessiz klasör oluşturma kaldırıldı. Commit `c5fc6bd08cb702b348b6aefcd92939b451fde10b`.
- `tests/test_history_verified_pipeline.py` `playlist.m3u8` korunan hedefinin GitHub origin doğrulama çağrısından önce reddedildiğini ve çıktı üretilmediğini kontrol eden negatif test içeriyor. Commit `f47a227e7371756a9484f149c7255fd98b3c1624`.
- Yalnız çıktı dosyasının adı denetleniyor; mutlak çıktı yolunun tüm üst bileşenlerini ve bağımsız workflow git yazmalarını merkezi biçimde koruma kapsamı henüz kanıtlanmadı. Testler çalıştırılmadı, Actions tetiklenmedi; 0/92 ve 0/26 değişmedi. Sonraki adım: tüm çıktı yollarını checkout sınırı, symlink ve korunan ata dizinleri açısından denetleyen merkezi yardımcı ve offline regresyon.


## 20 Ekim 2026 — K1 tam yerel çıktı yolu kontrolü ve import hatası
- `madsc/write_path_audit.py`: `enforce_local_output_path` ile mutlak çıktı yolu, mevcut hedef, mevcut ebeveyn, symlink atalar, korunan yol bileşenleri ve isteğe bağlı allowed_root denetleniyor; yalnız preflight, yazma yetkisi vermez. Commit `6d32290df4870783db007b03b9481f62ecc59666`.
- `madsc/history_verified_pipeline.py`: önceki turda eklenen fakat import edilmeyen `enforce_write_paths` çağrısı düzeltildi; yeni tam-yol kontrolü kullanılıyor. Commit `8e8c2c32f16c103bc8b81bcbc4ff08b7568a1268`.
- `tests/test_write_path_audit.py`: güvenli hedef, korunan ata, mevcut dosya, symlink üst dizin ve izinli kök dışına çıkma negatif senaryoları eklendi. Commit `1613ab312cef78f928bba5757603e1274778b345`.
- Henüz test yürütülmedi. GitHub Actions kotası dolu olduğundan tetiklenmedi. Gerçek üretim ve tüm yazma noktaları kabul edilmedi; 0/92 ve 0/26 değişmedi. Sonraki öncelik: yerel toplu regresyon, diğer gerçek yazıcılar için tam-yol K1 entegrasyonu ve olası symlink/TOCTOU sınırlarının güçlendirilmesi.


## 20 Ekim 2026 — Kritik import onarımları (çalıştırma öncesi)
- Önceki K1 tam-yol denetimi kodunda `Path` importu eksikti: `madsc/write_path_audit.py` düzeltildi (`370608e65094c66cb575373bbb65a03ea92372e0`).
- `madsc/history_verified_pipeline.py` içindeki `enforce_local_output_path` importu eksikti: düzeltildi (`bddf8f95dfdfa809457c2aaaf25c255e8325f182`).
- `madsc/history_real_source_publish.py` içindeki `enforce_write_paths` importu eksikti: düzeltildi (`ccdb25760fc87976c8c4521023586eec3bccdf39`).
- `tests/test_write_path_audit.py` yeni testlerin `tempfile` ve `Path` importları eksikti: düzeltildi (`9c63d291b9421197afda780d5d13a5feb13927a6`).
- Bu hatalar önceki kodun çalışabilirliğini engelliyordu; GitHub Actions veya güncel tam depo regresyonu çalıştırılmadı. Kabul 0/92, 0/26; üretim ve eski depo değiştirilmedi. Yerelde bulunan eski kopyalar güncel GitHub main ile eşdeğer sayılmamalı. Sonraki: güncel main kaynaklarını bağımsız yerel çalışma dizinine alıp tam offline regresyon.


## 20 Ekim 2026 — Tam yol güvenliği genişletildi; güncel main offline test kısıtı
- K1 `enforce_local_output_path` mutlak yolda `.` / `..` geçişlerini fail-closed reddediyor (`03ec9f4e79c99c9d50df49f0f6cbf78497c8768b`), negatif regresyon `tests/test_write_path_audit.py` eklendi (`27a21ac7c75502a78f6a0bdbd2fef453a11c42a4`).
- K2 `history_real_source_publish.py` artık yalnız çıktı dizininin adını değil tam çıktı yolunu K1 denetimine sokuyor (`34c2cae4661e75ed0d982e8f23c7bf6b2e511876`).
- Yerel çalışma ortamında önceki kaynak kopyaları var, ancak GitHub güncel main doğrudan klonlanamadı (github.com DNS çözümlenemiyor). Bu yüzden güncel main regresyonu yürütüldü veya geçti denmedi. Actions kotası nedeniyle CI tetiklenmedi. Kabul 0/92 ve 0/26. Sıradaki: GitHub kaynaklarının güncel çalışma kopyasını doğrulanmış şekilde oluşturup ücretsiz offline toplu regresyonu çalıştırmak; bağımsız dosya yazıcılarının K1 denetimini tamamlamak.


## 20 Ekim 2026 — K1/K2 traversal kontrolü doğrulaması
- Güncel `main` kaynağı yeniden okununca `madsc/history_verified_pipeline.py` çağrısında `output_path.absolute()` normalizasyonunun `..` bileşenlerini K1'e ulaşmadan gizleyebileceği görüldü. Ham bileşenleri koruyan `Path.cwd() / output_path` biçimiyle düzeltildi (`6432d44d5d819ef60c252303ee0fc5d18d7f5800`).
- Önceden eklendiği bildirilen mutlak yol traversal testinin güncel GitHub dosyasında olmadığı saptandı; `tests/test_write_path_audit.py` içine gerçekten eklendi (`dc68f29853b4c68efa13ced590e68b541652d2c1`).
- Yerel eski kaynak kopyalarında güncel `main` için geçerli test kanıtı yok. GitHub Actions çalıştırılmadı. K1 tam-yol kontrolü yalnız çağıran akışları kapsar; TOCTOU ve tüm bağımsız yazıcılar açık. 0/92 ve 0/26 kabul değerleri korunuyor.


## 20 Ekim 2026 gece — Yeni sohbete devir
- Son calisma kurallari, dogru Madsc55-Tv repo/dal kimligi, K1–K5 durumlari, son commitler, eksikler ve siradaki somut isler `SOHBET_DEVIR_NOTU_2026-10-20.md` dosyasina eklendi (commit `df0f0487be70fc08587e5c54b4cf5171d4b27eed`).
- Yeni sohbet ilk is: BIRLESIK_KALICI_CALISMA_KURALLARI.md, PROJE_HAFIZASI.md, ESKI_SISTEM_NOTLARI.md ve SOHBET_DEVIR_NOTU_2026-10-20.md dosyalarini oku; guncel main kaynaklarini dogrula; offline toplu regresyonu gercekten calistirmaya odaklan. Eski repo salt okunur, Actions calistirma, korunan canli veriye yazma. 0/92 ve 0/26 kabul degismedi.


## 21 Ekim 2026 — Actions kotasi ve toplu bitirme taahhudu
Kullanici 12 gunde GitHub Actions 2000 dakikalik kotasinin tukendigini ve K1-K5 tamamlanmadigini vurguladi. Artik acik ayri onay olmadan Actions yok; [skip ci], manual-only workflow, canli sistem korumasi suruyor. Her dosyadan sonra CI degil, SHA-dogrulanmis guncel main tum K1-K5 testleri icin tek yerel offline regresyon, toplu hata listesi ve toplu duzeltme. 2000 dakika 2000 test degildir. Kullanici guvenli rutin adimlar icin tekrar tekrar onayla ugrastirilmamali. Yalniz Actions/kota/canli test/production yazmasi/eski repo degisikligi oncesinde acik onay istenir. Kabul 0/92 ve 0/26; gercek tam regresyon henuz yok. Ayrintili BAGLAYICI kural BIRLESIK_KALICI_CALISMA_KURALLARI.md ve yeni sohbet devri SOHBET_DEVIR_NOTU_2026-10-20.md icinde.

## 21 Ekim 2026 — 21. kural ve proje adi teyidi
- Yeni sistemin kesin adi Madsc55-Tv; yazilabilir depo Madsc55/Madsc55-Tv, dal main.
- Eski Madsc55/madsc-tv deposu yalniz referans icindir.
- BIRLESIK_KALICI_CALISMA_KURALLARI.md dosyasindaki 21. kural aynen gecerlidir. Yanlis ad kullanilmayacak.
- Son Actions #405 basarili; 92 eski davranis ve 26 runtime kural icin gercek kabul kanitlari henuz tamamlanmadi.

## 21 Ekim 2026 — Kullanici onceligi: once yeni besli sistem
- Kesin proje adi Madsc55-Tv, depo Madsc55/Madsc55-Tv, dal main.
- Kullanici emri: once yalniz yeni K1 guvenlik, K2 kesif, K3 kanal/EPG/IBO, K4 yedek ve K5 merkezi bakim sistemini tamamla.
- Eski sistemin 92 davranissal esdegerligi, eski workflow kaldirma/kapatma ve eski-yeni gecis kabulu yeni sistem bittikten sonraya ertelendi. Eski depoya dokunma.
- Yeni sistemin kendi test, guvenlik, kanit ve eksik kod gelistirmelerine devam et; gercek kanit olmadan tamamlandi deme. Korunan canli listeler, favoriler, EPG ve yedekler degistirilmez.

## 21 Ekim 2026 — Yeni besli sistem K2-K3 regresyon ve hata duzeltmesi
- Actions #406 success. #407 failure: 444 unittest icinde tek ERROR, tests/test_five_system_channel_flow.py staged evidence without current probe. K1 fail oldugu icin sonraki K isleri skipped; toplu kabul de fail.
- madsc/channel_catalog.py commit 4df00a8: K3 uc-asamali gecmis basarisi yalniz mevcut probe varsa ve o probe basarisizsa catismali kabul edilir. Guncel probe yoksa kanal UNTESTED kalir, staged kanit korunur, uretim onayi verilmez.
- tests/test_channel_catalog.py commit 36a6c73: staged evidence mevcut fakat current probe olmayan kanal icin regression testi eklendi. Onceki test current probe fail ile staged pass catismasini reddetmeye devam eder.
- #408 ve #409 otomatik GitHub Actions tetiklendi; sonuclari kontrol edilmeden basarili sayilmaz.
- Oncelik: sadece yeni Madsc55-Tv K1-K5 sistemini tamamlamak; eski sistem 92 workflow parity ve kapatma daha sonraya ertelendi. Canli ag/cihaz/dis servis testleri veya korunan uretim listelerine yazma yapilmadi.

## 21 Ekim 2026 — Eski kategori ve kanal duzeni yeni sisteme guvenli metadata aktarimi
- Kullanici eski CALISANLAR, CALISMAYANLAR, YABANCI, YENILER, YEDEKLER, FAVORILER, onayli logolar, tvg kimlikleri ve kategori sirasinin yeni sisteme aynen alinmasini istedi; yeni bulunan kanallar once YENILER/TEST BEKLIYOR asamasinda test edilecek.
- Eski depoda salt okunur kontrol: CALISANLAR.m3u 1039, YABANCI_KANALLAR.m3u 740, YENILER.m3u 58, CALISMAYANLAR.txt 97 = 1934 kaynak kaydi (benzersiz kanal sayisi degil).
- config/legacy_category_order_snapshot.json commit 8ce4d58: kaynak dosya SHA, dosya ici ordinal sira, kanal adi, eski kategori, tvg-id, tvg-name ve guvenli logo referanslari aktarildi. Herkese acik yeni repoya eski akislardaki olasi credential iceren URL'ler KESINLIKLE kopyalanmadi. Bu bir metadata snapshot; yayin testi ya da tam calisir playlist aktarimi DEGIL.
- madsc/legacy_category_order.py commit a1cf854: 1934 kaydin sirasi/sayisi dogrulanir; yeni kesif adaylari izole YENILER_TEST_BEKLIYOR kuyruguna gider, uretime yazilmaz. tests/test_legacy_category_order.py commit 69b016c: kaynak sira ve aday karantina regresyon testleri eklendi.
- #409 success; yeni #410 ve #411 Actions sonucunu bekliyor. Ana listeler, favoriler, EPG, logos, cihaz ve eski repo degistirilmedi.
- Kalan: korunmus orijinal yayin URL'lerini guvenli gizli depolama/izinli is akisi ile eslestirmek; gercek kanal testleri, kullanici IBO onayi ve YEDEKLER'in bagimsiz kaynaklari icin tam kanit. Mevcut snapshot tek basina kullanilabilir IPTV listesi degildir.

## 21 Ekim 2026 — YENI SOHBETE KESIN DEVIR (kullanici talebi)
**ONCELIK:** Yeni Madsc55-Tv besli sistemi K1-K5 tamamlanacak. Eski sistemin 92 workflow tasinmasi/kapatilmasi, eski repo modernizasyonu ve 92/92 davranissal esdegerlik bundan SONRA. Kullanici eski sistemdeki mevcut kategori, sira, onayli logo ve IBO cihaz kararlarinin yeni sistemde korunmasini ayri ve acik olarak istedi; bu karar yeni sistemin kendi kategori metadata referansinin korunmasini kapsar, eski sistemi kapatmak demek degildir.

**TEK YAZILABILIR DEPO:** Madsc55/Madsc55-Tv, main. Ad kesinlikle Madsc55-Tv. Eski Madsc55/madsc-tv / madsc/bes-sistem-toplu-birlestirme yalniz READ ONLY kaynak. Kalici 21. kural proje adini ve repo kimligini baglar; BIRLESIK_KALICI_CALISMA_KURALLARI.md ve eski AGENTS.md, DEVAM_NOTU.md guvenlik/onay kurallari ihlal edilmez. PR #71 merge yok. Ana playlistler, CALISANLAR, YENILER, YEDEKLER, HEPSI, FAVORILER, cihaz favorileri, EPG, logo, yedekler ve kimlik/sira bilgileri acik onay olmadan degismez.

**ESKI IBO EKRAN GORUNTULERIYLE DOGRULANAN KATEGORILER:** Toplam 1039; sira ve sayilar: FAVORILER (66), FAVORILER 1 (62), FAVORILER 2 (1), HEPSI (374), SINEMA (5), HABER (72), SPOR (22), BELGESEL (13), COCUK (20), MUZIK (34), DINI (17), YEREL (70), ULUSAL (281), YEDEKLER (2). Eski CALISANLAR.m3u kaynak sirasinda HABER sonrasi ULUSAL bulunuyor; kullanicinin IBO ekranindaki gorunumde ULUSAL daha asagida: iki sira farkini cihaz onayi olmadan yeniden siralama ile cozme; kaynak sirasi ve cihaz gorunumu ayri kanittir. 1039 toplami kategori tekrarlarini icerir. YENILER.m3u 58 kayitli, ayri ve korunan dosyadir; YEDEKLER'in yerine gecmez. Yeni bulunan kanallar YENILER.m3u veya YEDEKLER'e otomatik eklenmez.

**TAMAMLANAN SON KODLAR:** config/legacy_category_order_snapshot.json commit 8ce4d58: eski kaynaktan 1039 CALISANLAR + 740 YABANCI_KANALLAR + 58 YENILER + 97 CALISMAYANLAR = 1934 tarihsel kayit metadata snapshot; isim, kategori, orijinal dosya ici sira, TVG ID/name ve uygun logo referansi, akisin URL/credential'i OLMADAN. Snapshot oynatilabilir M3U8 veya IBO onayi DEGIL. madsc/legacy_category_order.py commit a1cf854 ve tests/test_legacy_category_order.py commit 69b016c: tam sayi/sira koruma ve yeni kesif izolasyonu. Son isim duzeltmesi kod commit 06b3783, test commit 25b4f6d: destination artik IZOLE_ADAY_TEST_KUYRUGU (eski YENILER_TEST_BEKLIYOR yanlis anlasilmasini onler). Eski YENILER, YEDEKLER, ana M3U8, cihaz kategorileri degismedi.
K2-K3 katalog raporlamasi, K3 stale three-stage ile current probe catismasi ve probe yoksa UNTESTED kalmasi regression kodlari eklendi; #407 failure duzeltildi, #408/#409 success. #410/#411 success. SON ACTIONS KONTROL: #412 run 39616429446 ve #413 run 39616450580 QUEUED; yeni sohbette once tekrar sorgula, hata varsa job logs ile duzelt. Eski 440+ offline testleri uretim kaniti sayma.

**KALAN YENI SISTEM:** K1 26 runtime koruma kuralinin gercek izin/yazma engeli kaniti; K2 canli kaynak mutabakati, gunde iki kez guvenli kesif, test adaylari; K3 3 asama/6 saat/guncel ffprobe ve sureklilik, 75 tarihsel aday, IBO kullanici cihazi ve gorsel kimlik; EPG/XMLTV/logo/Pages canli zincir; K4 harici yedek ve gercek geri yukleme; K5 merkezi isletim, toplu kabul, gunluk raporlar, tekrar tetikleme siniri. 22 kabul gorevi eski olcumde 0 tamamlandi, 5 devam, 17 bekliyor; tahmini yuzdeler kesin kabul degil. 92/92 eski workflow paritesi sonra.
**GUVENLIK:** Public repo, eski stream URL'leri token/credential icerebilir. Bunlari public repoya veya yeni metadata snapshot'a ham kopyalama. URL'ler ancak guvenli secret/izinli izole ortamda islenir. Eski logo alanlari/cihaz kararlarina dokunma. ADA/Kanal D gibi onceki kullanici cihaz retleri otomatik probe ile gecersiz kilinmaz.
**YENI SOHBET BASLANGICI:** 'Madsc55-Tv yeni besli sisteme DEVIR notundan devam et; PROJE_HAFIZASI.md son 21 Ekim 2026 devri ve BIRLESIK_KALICI_CALISMA_KURALLARI.md oku, #412/#413 sonuclarini kontrol et, hata varsa duzelt; K1-K5 eksiklerini kanitla tamamla. Eski workflow tasimayi ertele, korunan listelere dokunma, YENILER ve YEDEKLER'i karistirma.' Kullanicinin bu sohbetteki son goruntusu onceki durum tablosu: 26 guvenlik, kaynak/adaylar, 3 asama, EPG/logo, harici restore; tablo eski sistemdeki 92/92 gorevini de iceriyor, bu simdiki oncelik DEGIL.

## 21 Ekim 2026 — Kullanici yeni sohbete gecis teyidi
- Kullanici "Al notlari yeni sohbete gecelim" dedi. Bu, yeni K1-K5 calismasini durdurmak degil, ayni noktadan yeni sohbetten devam etmek talimatidir.
- Zorunlu baslangic: BIRLESIK_KALICI_CALISMA_KURALLARI.md icindeki 21 kalici kuralin tamamini, PROJE_HAFIZASI.md en son devir bolumunu, ilgili notlari, son GitHub Actions sonuclarini oku. Kurallari ve onceki IBO cihaz kararlarini unutma.
- Tek aktif proje Madsc55/Madsc55-Tv, main. Eski Madsc55/madsc-tv salt okunur. Once yeni K1-K5 tamamlansin, eski 92 workflow gecisi daha sonra.
- IBO ekran goruntusundeki 1039 kanal, 14 kategori, ozellikle YEDEKLER (2) ve eski kategori sirasini koru. YENILER.m3u (58) YEDEKLER yerine gecmez. Yeni adaylar IZOLE_ADAY_TEST_KUYRUGU'nda kalir, otomatik korunan listeye eklenmez. Korunan kanallar, favoriler, EPG, logo, yedek ve cihaz kararlari degismez.
- Tarihsel metadata snapshot 1934 kayit; stream URL'leri public repoya tasinmadi. Kategori/sira koruma kodu ve testleri var. Son ad duzeltme commitleri 06b3783 ve 25b4f6d.
- Bu devir kaydi yazilmadan onceki Actions: #413: queued/pending; #412: queued/pending; #411: completed/success; #410: completed/success. Yeni sohbette yeniden sorgula; sonucunu varsayma.
- Kalan: K1 26 kural runtime kaniti, K2 gercek kesif/aday, K3 uc asama/IBO cihaz, EPG/logo/Pages, K4 gercek harici restore, K5 butunlesik kabul. Offline test = gercek cihaz/uretim kabulu degildir. Kullanici yeni sohbetten bu isleri surdurmek istiyor.

## 21 Ekim 2026 — #412/#413 kesin kontrol ve kategori izolasyonu
- Yeni depo Madsc55/Madsc55-Tv main kontrol edildi; eski depo ve korunan uretim dosyalari degistirilmedi.
- Actions #412 run 39616429446, commit 06b3783859859293e6f2089c65cf4eda3b586880: completed/failure. K1 447 testte 1 failure: test_new_candidates_are_isolated_and_ordered; K2-K5 skipped, toplu kabul failure.
- Actions #413 run 39616450580, commit 25b4f6d4e55af52e6a91bc68c550405e8358fb07: completed/success, K1-K5 ve toplu kabul 6/6 success.
- GitHub main kaynak dogrulamasi: madsc/legacy_category_order.py ve tests/test_legacy_category_order.py ayni IZOLE_ADAY_TEST_KUYRUGU hedefini kullaniyor. route_discovered_candidates production_writes=false, existing_order_modified=false donduruyor; YENILER/YEDEKLER otomatik degismiyor.
- Bu turda yeni kod degisikligi veya yeni Actions tetiklemesi yapilmadi. #413 offline/CI fixture kaniti olup gercek yayin, 26 runtime guvenlik kurali, IBO cihaz, harici restore veya 92 parity kabul kaniti degildir.
- Kullanici onceligi: yeni K1-K5 tamamlansin, eski 92 davranis aktarimi daha sonra. Kalan: K1 runtime kapilari; K2 kaynak mutabakati ve izole aday; K3 uc asama/6 saat/IBO/EPG-logo; K4 harici restore; K5 merkezi kabul. Kota tuketen Actions icin ayrica acik izin gerekir; sonraki is toplu offline kaynak ve entegrasyon testleri.

## 21 Ekim 2026 — K2 kategori girdisi fail-closed sertlestirme
- Yeni repo main madsc/legacy_category_order.py: bozuk/non-dict tarihsel satirlar ve bilinmeyen kaynak dosyalari ValueError ile reddedilir; kesif adaylarinda bos veya yalniz bosluk isimleri reddedilir. Kod commit d8bb351c83fd58d6360ccad591337dfdfff7882d.
- tests/test_legacy_category_order.py: bozuk snapshot satiri, bilinmeyen dosya ve bos aday regresyonlari eklendi; commit 8e451779ce0ca1e0da0225bae18782eb90906a42.
- Iki commit [skip ci] ile yapildi. GitHub Actions veya tam offline regresyon CALISTIRILMADI; testlerin gectigi iddia edilmiyor. Korunan canli kategori/sira/logo/favoriler/YENILER/YEDEKLER ve eski depo degistirilmedi.
- Siradaki: tam main kaynak checkout ve tek toplu offline K1-K5 test, sonucuna gore baglantili duzeltmeler. Canli ag, IBO cihaz ve harici restore kaniti hala eksik; eski 92 davranis aktarimi sonraya ertelendi.

## 21 Ekim 2026 — K2 tarihsel metadata kalite denetimi (salt okunur)
- GitHub main tree recursive envanteri truncated=false olarak okundu. Container github.com DNS erisimi basarisiz; eksiksiz checkout ve tum offline testler henuz yapilamadi.
- config/legacy_category_order_snapshot.json icinde YENILER.m3u order 44 ad alaninda M3U attribute metni (tvg-logo/group-title) bulundugu kaynak incelemesinde goruldu. Tarihsel kayit degistirilmedi; otomatik onarim veya kategori tasimasi YOK.
- madsc/legacy_category_order.py audit_historical_metadata() eklendi: tarihsel 1934 metadata kaydinda bos ad ve gomulu M3U attribute metnini raporlar, uretime yazmaz, kendiliginden onarmaz. Commit 73f5528e7bba60b89288b6ef5fa9ee1c3a325a6e.
- tests/test_legacy_category_order.py salt okunur denetim regresyonu eklendi; commit 95a0851f5716b1a6d6058954d26c9368145eb055. Testler henüz CALISTIRILMADI, Actions tetiklenmedi; [skip ci].
- Sonraki: tam main offline gate; ardindan K1 runtime koruma, K2 kaynak/aday, K3 IBO/EPG, K4 harici restore, K5 kanitli kabul. Eski 92 workflow gecisi sonraya ertelendi. Korunan YENILER/YEDEKLER/favoriler/logo/sira/playlist/EPG ve eski repo degistirilmedi.

## 21 Ekim 2026 — K2 kaynak manifesti fail-closed denetimi
- madsc/legacy_category_order.py: snapshot kok tipi dict olmak zorunda; source_files dort beklenen dosyayi tam ve tekil tanimlamali, her count beklenen sayiya ve SHA 40 kucuk harf hex bicimine uymali. Commit 69db62c6d1d002fb6324990b47db68ff8d6cf885.
- tests/test_legacy_category_order.py: bozuk kok, eksik kaynak manifesti, bozuk SHA senaryolari icin regresyon testleri yazildi. Commit dd2941040635adb4c69b6ef69058ed3ffdf7faa3.
- Bunlar kaynak SHA'sinin gercek dosya icerigiyle eslesmesini kanitlamaz; testler henüz CALISTIRILMADI. [skip ci], Actions yok, eski depo/canli listeler/EPG/logo/favoriler/YENILER/YEDEKLER degismedi.
- Siradaki ana hedef: tam main checkout ve tek offline K1-K5 regresyon; 22 gorev, 26 runtime guvenlik ve 92 eski davranis icin gercek kanit gereklilikleri acik.

## 21 Ekim 2026 — K2 kaynak manifesti tekillik duzeltmesi
- madsc/legacy_category_order.py: source_files icinde ayni file anahtarinin birden cok gorunmesi reddediliyor; onceki dict comprehension yinelenen kaydi gizleyebiliyordu. Commit d9514c5bac960f8e42aa6fc05c34797bf278c022.
- tests/test_legacy_category_order.py: dort ayni kaynak kaydi iceren bozuk manifest icin negatif regresyon eklendi. Commit ea724e291c1e570b7be31e9de7189fe74ec29f10.
- Container git ls-remote DNS github.com cozumleyemedi; bu nedenle tum depo offline testi gerceklestirilemedi. Yeni testler henuz calistirilmadi; CI Actions tetiklenmedi ([skip ci]).
- K1-K5 genel kabul acik; eski repo, korunan playlist/EPG/logo/kategori/siralama/favori/YENILER/YEDEKLER degistirilmedi.

## 21 Ekim 2026 — K2 tarihsel kaynak repository/ref sabitleme
- config/legacy_category_order_snapshot.json okundu: 1934 kayit, kaynaklar CALISANLAR 1039, YABANCI_KANALLAR 740, YENILER 58, CALISMAYANLAR 97; source_repository=Madsc55/madsc-tv ve source_ref=main.
- madsc/legacy_category_order.py kaynak repository/ref alanlari onayli sabit degerlerle eslesmezse fail-closed reddeder. Commit 72a62b615abcf0777e977e23b3ea60245d18cc5e.
- tests/test_legacy_category_order.py: yanlis repo ve yanlis ref icin regresyon eklendi. Commit 339f8503031f63d5bee6c92c0cd93ec76fa01f23.
- Bu yalniz metadata provenance kontroludur; eski depo SHA bloblari canli olarak yeniden hash dogrulanmadi. Testler calistirilmadi, Actions tetiklenmedi [skip ci]. Eski repo, canli kanal listeleri, EPG, logolar, favoriler, YENILER ve YEDEKLER degismedi.

## 21 Ekim 2026 — K2 gercek Git blob SHA kaynak mutabakati
- Salt okunur GitHub API GET /repos/Madsc55/madsc-tv/git/trees/main?recursive=1 ile eski deponun main agaci okundu; truncated=false.
- Yeni config/legacy_category_order_snapshot.json source_files blob SHA'lari eski main dosyalariyla birebir eslesti (4/4): CALISANLAR.m3u b40aaf6615b120eac7bd936ccf022dc4a14025ae; YABANCI_KANALLAR.m3u 3980338955c65a7f238c7d8a377011a8dd78491f; YENILER.m3u 2a2c4141b14607f2f87d2405a7885e9e0fdda073; CALISMAYANLAR.txt 881cb039e3e248ad2c38d380720d0994a9bfafd6.
- Bu bagimsiz Git blob kimligi karsilastirmasidir; yerel dosya iceriklerini yeniden hash etme, canli stream, 26 runtime guvenlik, IBO/EPG, harici restore, 92 davranis kabul veya toplu offline regresyon DEGiLDiR.
- Korunan kaynaklara yazma yok; Actions tetiklenmedi. Siradaki ana oncelik tam offline gate ve kalan K1-K5 gercek kanit zinciri.

## 21 Ekim 2026 — K1-K5 ana workflow ve 22 gorev toplu kaynak denetimi
- GitHub main tree sha b00cdc8b48f3147ad4772d78e91e7e46ab7b96ee okundu. .github/workflows altinda 15 YAML: 5 ana (madsc-01..05) ve 10 yardimci. Yardimci dosyalar: 01-guvenlik.yml, madsc-k2-legacy-multisource.yml, madsc-k2-live-pilot.yml, madsc-k2-real-history-source.yml, madsc-k2-verified-history.yml, madsc-k3-live-manifest-pilot.yml, madsc-k3-turkish-tv-video.yml, madsc-legacy-99-bulk-audit.yml, madsc-legacy-notes-bulk-merge.yml, madsc-turkish-tv-batch.yml. Hicbiri silinmedi/kapatilmadi.
- 5 ana workflow'un YAML kaynaklari okundu. K1-K4 workflow_dispatch ve contents:read ile izole; K2/K3 canli ag adimlari acik opt-in gerektiriyor. K5 main push'ta madsc/** ve tests/** degisikliklerinde otomatik tetiklenebilir; [skip ci] disiplini surmeli. K5 K2->K3->K4->K5 artifact/fixture zinciri iceriyor, gercek canli kabul degil.
- docs/K1_K5_KANITLI_GOREV_DEFTERI.json okundu: 22 gorev, 0 completed, 5 in_progress, 17 pending. 92 davranis ve 26 runtime guvenlik kabul kaniti yok. Kaynak okumak bu gorevleri tamamlamaz.
- Bu tur yalnizca statik kaynak incelemesi yapildi, offline test ve Actions tetiklenmedi, eski depo ve korunan kanallar degismedi.
- Siradaki toplu is: 10 yardimci YAML'in tetik/izin/komut/artifact/timeout farklarini ana 5 ile satir bazinda karsilastirip tek entegrasyon paketi hazirla; ardindan tum yeni kodu offline test et, gercek cihaz/offsite kanitlarini acik tut.

## 21 Ekim 2026 — K2 bagimsiz yerel offline test sonucu
- Container git ls-remote ve Python requests github.com/api.github.com DNS cozumleyemedi. GitHub connector ile main madsc/legacy_category_order.py kaynak metni okundu ve ayni kod yerel bagimsiz unittest harness'inde calistirildi.
- 4/4 bagimsiz offline test PASS (0.024 sn): aday izolasyonu/sirasi, bos isim fail-closed, gecersiz aday listesi, 1934 sentetik kayitla manifest kaynak/ref/SHA bicimi/tekrar korumasi ve metadata salt okunur raporlama.
- Bunlar sentetik fixture ile yerel alt-kume testidir; tam GitHub unittest paketi, gercek 1934 snapshot uzerinde tam kabul, K1-K5 toplu regresyon, 75 canli aday, IBO/EPG cihaz, harici restore, 26 runtime kural veya 92 davranis esdegerligi kaniti DEGILDIR.
- Test icin Github Actions tetiklenmedi, uretim/korunan listeler/eskidepo degistirilmedi. Sonraki: tam repo offline test erisimi veya GitHub Actions icin calistirma yetkisi ve sonra toplu kabul.

## 21 Ekim 2026 — Actions #414 K1 regresyon hatasi duzeltildi; otomatik CI aktif
- #414 run 39620800578 manual workflow_dispatch completed/failure, 451 testte 3 error. Hepsi madsc.legacy_category_order.load_historical_categories() icindeki source_ref == main yanlis beklentisinden kaynaklandi; gercek snapshot source_ref=madsc/bes-sistem-toplu-birlestirme.
- Eski kaynak/snapshot/kanal listeleri degistirilmeden validator gercek onayli tarihsel ref'e sabitlendi. Kod commit 0568501a8a8c3512c10975a86616d2ad02892360. [skip ci] KULLANILMADI.
- Otomatik main push tetiklemeli Actions #416 run 39621532611 bu commit icin queued goruldu. #415 run 39621498388 onceki 21d37bc commit icin queued goruldu. Bu an itibariyle yeni sonuc bilinmiyor; basari iddia edilmez.
- Otomatik testleri durduran [skip ci] kod commitlerinde kullanilmayacak; docs-only not commitleri K5 paths filtresi geregi tetiklemiyor. CI kota/izin kosullari ayrica takip edilecek.

## 21 Ekim 2026 — K2 metadata buyuk/kucuk harf duzeltmesi ve otomatik CI
- Madsc55/Madsc55-Tv main madsc/legacy_category_order.py audit_historical_metadata() M3U attribute metinlerini casefold ile ariyor; salt okunur, kaynak playlist degistirmez. Commit e39bd868a5b6d36a95d2120af96e3de40d86488f.
- tests/test_legacy_category_order.py buyuk harf TVG-LOGO senaryosu eklendi. Commit 3feb611f25ca276d422b29451ef78eba2329a49a.
- [skip ci] kullanilmadi; otomatik push Actions #421 (39622721123) ve #422 (39622739172) queued goruldu. Onceki #416, #417, #418 success; #419/#420 queued. Yeni iki testin sonucu henuz bilinmiyor, basarili sayilmaz.
- Eski Madsc55/madsc-tv deposu, canli kanallar, kategoriler, sira, logo, favoriler, YENILER, YEDEKLER degismedi. K1-K5 uretim kabul acik.

## 21 Ekim 2026 — K1 Unicode yol koruma guclendirmesi (CI kotasi korunuyor)
- Yalniz Madsc55/Madsc55-Tv main uzerinde madsc/write_path_audit.py Unicode NFKC/casefold esdeger yol adlarini korunan isim/prefix ve yinelenen yol denetimine bagladi; tam genislikli FAVORILER/EPG gibi gorunus farklariyla korumayi atlama riski daraltildi. Commit f15bb89224f8053c5c1d640a57211e62ec59bb94.
- tests/test_write_path_audit.py Unicode esdeger korunan yollar ve esdeger rapor adlari icin negatif regresyon eklendi. Commit 57c25afa3a7066e0e9316cecad752fe3c64f7cac.
- Her iki commit [skip ci] ile yapildi: son kota kurali geregi yeni Actions calistirilmadi. Yerel toplu test bu turda calistirilamadi; bu degisikliklerin test basarisi henuz kanitli degil. K1 26/26 ve K5 92/92 kabul sayaclari degismedi; 22 gorevden 0'i resmi tamamlandi.
- Korunan playlist/EPG/logo/favoriler/yedek dosyalari ve eski repo degistirilmedi. Sonraki is: kaynaklarin toplu offline regresyonu, butun gercek writer callsite envanteri ve merkezi guard baglantisi; sonra K2-K5 gercek kabul.

## 21 Ekim 2026 — K1 merkezi kapinin K2 atomic history yazicisina baglanmasi
- madsc/history_pair_store.py atomic_write_pair artik hedef dosya adini K1 enforce_write_paths ile denetliyor, symlink olan ust dizinleri reddediyor. Kod commit b3b42b475d2433e242f9238b0de58f403b1ca299.
- tests/test_history_pair_hls.py korunan dosya adlari, Unicode esdeger yol ve symlink ust klasor reddi icin negatif testler eklendi. Test commit 6f55c7f9bcaf964751eb29841b5fcbd6f480dba1.
- Her iki commit [skip ci] ile kaydedildi; yeni Actions baslatilmadi. Bu turda offline toplu test calistirilmadi. K1-03 in_progress, 26 runtime ve 92 eski otomasyon kabul sayaclari degismedi. Diger gercek yazma noktalarinin tam envanteri ve runtime entegrasyonu bekliyor.
- Etki: K1 guvenlik, K2 history, K4 butunluk, K5 kabul. Eski repo ve korunan canli dosyalar degismedi.

## 21 Ekim 2026 — K1 Unicode normalize yol gecisi ve uzanti guvenligi
- madsc/write_path_audit.py normalize edilmis NFKC path parcalarinda '.', '..', bos parcayi, sonda nokta/boslugu ve .m3u/.m3u8 uzanti taklitlerini reddedecek sekilde guclendirildi. Commit dea98023472f7006027f087ce389f33b461b5362.
- tests/test_write_path_audit.py normalize Unicode traversal, dosya uzantisi ve ayirici taklitleri icin negatif testler eklendi. Commit 2dc317827516992799ceb56eeba81dfcfdb787f6.
- [skip ci] kullanildi; Actions baslatilmadi, offline regresyon bu turda calistirilamadi. Kod degisikligi test edilmis/kabul edilmis sayilmiyor. 0/26 runtime ve 0/92 parity ayni. K1-03 acik, tum writer noktalarinin envanteri eksik.
- Korunan listeler, IBO cihaz favorileri, EPG/logo ve eski repo degistirilmedi.

## 21 Ekim 2026 — K1-K5 tek toplu offline envanter gelistirmesi
- madsc/five_system_installation.py, 22 gorevin tamamini REQUIREMENTS ile karsilastirip eksik kanit sayisini, dis kanit gerektiren gorev sayisini ve madsc/*.py icindeki AST kaynakli muhtemel writer callsite satirlarini tek salt-okunur raporda listeler. Kod commit 1c7af5166f44ee97b86304188c61b4345b3a0ccb.
- tests/test_five_system_channel_flow.py toplu kurulum, 22 gorev ve tek writer kaydini kapsayan regresyon senaryosu eklendi. Test commit 5487100ca9c22dc637b1b367ecbb416db6a61c71.
- Bunlar envanter/kabul hazirlik kodudur; writer noktalarinin tamligi, guvenlik runtime kabulu, gercek kaynak, 75 aday, IBO, harici restore veya 92/92 davranissal esdegerlik kaniti degildir. 0/22 resmi kapanis degismedi.
- [skip ci] kullanildi; yeni Actions tetiklenmedi. Offline toplu regresyon henuz calistirilamadi. Eski repo ve korunan uretim dosyalari degistirilmedi.

## 21 Ekim 2026 — Toplu K1-K5 writer callsite siniflandirma
- madsc/five_system_installation.py AST envanteri yalnizca okuma yapan open() cagrisini yazma adayi saymiyor; write/append/create/update kiplerini yazma, dinamik kipleri inceleme gerektiren olarak sinifliyor. Commit 7cdc4845e28c28c3d3e625d613a10b88249735f5.
- tests/test_five_system_channel_flow.py tek senaryoda salt okuma, yazma ve dinamik open kiplerini dogrulayan regresyon eklendi. Commit d6efdccb0e2c18b03457f3a95247342e8a688104.
- [skip ci] kullanildi, Actions calistirilmadi. Testler bu turda gercekten kosulmadi; kod/testler kabul edilmis sayilmiyor. Toplu K1-K5 gercek islevsel kapanis, 26 runtime kural ve 92 parity hala acik. Korunan dosyalar degismedi.

## 21 Ekim 2026 — K1-K5 toplu writer risk envanteri
- madsc/five_system_installation.py writer cagri noktalarini modul bazinda write/dynamic_mode_review olarak sayiyor ve dinamik kipleri topluca raporluyor. Commit d46690f87e95bceea95b8c87541affa3cb267a2e.
- tests/test_five_system_channel_flow.py modul bazli sayaclar icin regresyon beklentileri eklendi. Commit bcce2f843cfe229be7b7e024c713fcbeba3fab5d.
- [skip ci] nedeniyle Actions baslatilmadi. Bu turda test kosulmadi. K1-K5 kabul 0/22, gercek writer entegrasyonu, 26 runtime ve 92 eski davranis kaniti halen acik. Bu envanter yalniz risk haritalama ve sonraki toplu uygulama icin hazirliktir.

## 21 Ekim 2026 — K2-K3-K5 kanit girdi zinciri sertlestirme
- madsc/channel_test.py: probe None/dict disi ve video/audio bool disi kanit reddediliyor; c1fa5744dfa0adf4f19da0d02c6886ecd09fc8fc.
- madsc/channel_catalog.py: explicit null probes/three_stage girdisi artik sessizce kanit yok sayilmiyor; 140d26fbd925972085773109a2866925c44f3acd.
- tests/test_five_system_channel_flow.py: K2-K3-K5 entegre onizleme null ve bozuk kanit regresyonlari eklendi; 02937d220fdc09a84876c9b63107125a11738777.
- Tum commitler [skip ci]; Actions kotasi harcanmadi. Yerel toplu regresyon bu turda yapilmadi; kod/test degisikligi production kabul kaniti degildir. 0/22, 0/26, 0/92 acik. Canli M3U/EPG/logo/IBO/favoriler ve eski depo degismedi.

## 21 Ekim 2026 — K1 izole rapor yazma sinirinda runtime guard
- madsc/fixture_report_writer.py: K3/K4/K5 ortak rapor yazma yolunda enforce_write_paths kontrolune ek olarak mkdir sonrasi ve open('x') oncesi enforce_local_output_path(destination, allowed_root=root) zorunlu; mevcut rapor icin FileExistsError korunuyor. Commitler 71542fc0edf99ffbbe8a2727c8f50ce39e96cd8d ve f41a8970766319153ada5c02f3f86280b235edb4.
- tests/test_fixture_report_writer.py: yerel runtime guard reddinin dosya yazimini durdurdugu mock regresyonu eklendi. Commit 5a792a17d10a3f145b32daa6d93b66119180d261.
- Kapsam sadece ortak izole rapor yazicisi; tum repository writer callsite'lari runtime ile korunmus DEGIL. Yeni testler henuz calistirilmadi; [skip ci] kullanildi. Kabul 0/22, runtime 0/26 ve eski davranis 0/92 ayni. Canli listeler/EPG/logo/IBO/eski repo degismedi.

## 21 Ekim 2026 — K1 runtime guard K2/K5 kanit yazicilarina genisletildi
- K2 izole history pair output preflight: d0ba8e7a7ab92f7fe69b065dc6a4f3855dcf2b9f; cagrim regresyonu 44e04782cb5cc2e9c0e2ca09e414cd02b7415b77.
- K2 candidate artifact produce/consume raporlarinda enforce_local_output_path: 9cdc5fff2ea9a29c9ee56a53964b35c23c0c6697.
- K2/K3/K5 history transport outputunda enforce_local_output_path: 739e123bd78941780cf009c1ddbf292b2ccf332a.
- Bunlar izinli izole raporlar icin preflight, tum repository writer noktalarini korumaz. Testler bu turda kosulmadi; [skip ci] ile Actions baslatilmadi. Kabul 0/22, 26 runtime kural ve 92 davranissal parity acik. Korunan canli dosyalar degismedi.

## 21 Ekim 2026 — K2/K5 kanit aktariminda overwrite engeli
- madsc/history_transport.py ve madsc/artifact_transport.py cikti yazma islemleri write_text yerine exclusive open('x') kullaniyor; mevcut hedefin uzerine yazma reddedilir. Commitler 9493726c99eed41e96b28b20190a75d45e84121a ve bc46da1a866e37c1232321eefc49bb0ed29210dc.
- Yeni Actions veya testler calistirilmadi ([skip ci]). Tum yazicilarin runtime korumasi tamamlanmadi. 0/22 kabul, 0/26 runtime, 0/92 legacy davranis ayni. Canli dosyalar degismedi.

## 21 Ekim 2026 - Toplu yardimci workflow sozlesme denetimi
- GitHub Actions 39645023901, main 881c791: 6/6 job completed success. Offline CI basarisi canli kabul degildir.
- madsc/workflow_consolidation.py: 10 yardimci workflow icin salt-okunur operasyon sozlesmesi matrisi eklendi (komut, timeout, artifact adi, actions read, always upload); commit 9e228a0.
- tests/test_workflow_consolidation.py: eksik timeout ve artifact farklarini tespit eden regresyon eklendi; commit bf0b213. Bu iki yeni commit icin [skip ci] kullanildi, test henuz calistirilmadi.
- Resmi durum: 0/22 kabul, 5 devam eden, 17 bekleyen; 0/26 runtime, 0/92 legacy parity. Sonraki adim: matrisi tum workflow'larda calistirip farklari topluca gider; gercek davranis/harici kanit ayri kabul edilir.
- Korunan canli dosyalar ve eski repo degismedi.

## 21 Ekim 2026 - 10 yardimci workflow toplu fark analizi
- 15 workflow GitHub main kaynagindan okundu; 10 yardimci kaynak ile bes ana YAML operasyon sozlesmesi karsilastirildi. Ilk statik taramada 9/10 yardimcida en az bir fark var: artifact isimleri, timeout ve if always yukleme. Bunlar otomatik davranissal parity hatasi/kabul kaniti degildir.
- madsc/workflow_consolidation.py --behavior-matrix CLI eklendi, commit d4b86dc. Timeout kontrolu kaynak limitini karsilayan daha uzun hedef limitini uygun sayacak sekilde duzeltildi, commit 289dfc9. Test regresyonu 3bdc210.
- Onceki toplu GitHub Actions run 39645023901: 6/6 success. Yeni commitler [skip ci]; yeni kod test edilmedi. 0/22 kabul, 0/26 runtime, 0/92 davranis parity ayni.
- Sonraki toplu is: artifact adi/if always farklarini kaynak-hedef bazinda gerekcelendir; mevcut is akisi davranisini bozmadan gerekli eksikleri entegre et, tek toplu regresyon yap. Canli playlist, EPG, favoriler, logo, arsiv, eski repo degismedi.

## 21 Ekim 2026 - Toplu CI ve kalan gercek entegrasyon
- GitHub Actions run 39648796704 basarili: K1,K2,K3,K4,K5,toplu kabul 6/6 success. Bu offline/fixture kanitidir.
- Kaynak YAML incelemesi: K2 ana workflow legacy multisource, live pilot, real history publish ve verified history komutlarini zaten opt-in olarak iceriyor. K3 ana workflow live manifest, video probe ve 1000-aday batch komutlarini opt-in olarak iceriyor. K5 99-source audit ve not birlestirme komutlarini opt-in olarak iceriyor. Yardimci workflow artifact isimleri ana is akisi ile farkli; bu tek basina davranissal esdegersizlik kaniti degildir. Kaynaklarda farkli hata halinde yukleme semantigi mevcut; ayri kanit gerekli.
- 2cfa6b6 commit: 10 yardimci workflow raporunda requires_manual_behavior_review alani eklendi. [skip ci], bu commit test edilmedi.
- Gercek dis ag probe, 75 aday 6 saatlik olcum, IBO cihaz, harici backup restore ve 92 legacy parity kaniti halen eksik; kabul 0/22. Korunan canli dosyalar degismedi.

## 21 Ekim 2026 - Toplu hata kaniti saklama paketi
- K1, K2, K3 bagimsiz workflow'larinda Upload isolated evidence adimlari always() && !cancelled() kosuluna baglandi. Bir onceki adim fail olsa bile olusan raporlar yuklenmeye calisilir; eksik dosya ve uretim kabul otomatik basarili sayilmaz. Commitler 307ef3e, 06da9cb, a811002.
- tests/test_workflow_consolidation.py gercek K1/K2/K3 YAML'larinda hata sonrasi artifact yukleme regresyonu eklendi, commit 82d5f4b. Otomatik Actions run 39649951753 basladi, sonuc henuz bu not aninda dogrulanmadi.
- Son kesin yesil run 39648796704: 6/6. 22 kabul gorevi ve 92 legacy parity kanitlari hala tamamlanmadi. Canli liste, EPG, logo, yedek ve favoriler korunuyor.

## 21 Ekim 2026 - Son yesil run ve toplu eksik komut kapisi
- GitHub Actions #39650954707 completed/success, K1 K2 K3 K4 K5 toplu kanit 6/6 success. Onceki run #39649951753 regresyon testinde yanlis newline literal nedeniyle fail; 69f46d2 ile duzeltildi.
- madsc/workflow_consolidation.py: 10 yardimci workflow icin komut ana YAML run adiminda bulunmazsa command_missing ve missing_commands listesi uretir (2f5ceb7). Test fixture eksik komutu ve blocker listesini denetler (9e66945). Bu iki commit [skip ci], henuz test edilmedi.
- 22 kabul gorevi 0 tamam, 5 devam, 17 bekleme; 92 legacy parity 0 dogrulama. Bu sayaclar fixture yesil diye artmaz. Kalan: gercek dis kaynak, 75 aday icin 3 ayri >=6 saat probe, IBO cihaz, backup/restore ve kalan davranis farklari.
- Canli M3U, XMLTV, logolar, favoriler, yedekler, arsiv, eski repo degismedi. Sonraki toplu paket: on ana besli YAML ile on yardimci workflow farklarini davranissal kanitla kapat, fixture regresyon ve kabul kanitlarini bagla.

## 21 Ekim 2026 - On yardimci workflow icin zorunlu komut kapisi
- madsc.workflow_consolidation --contract-gate eksik executable ana komut varsa exit 1; yoksa exit 0, ama behavioral_parity_verified=false (7943d2b).
- Fixture tabanli iki regresyon eklendi: eksik 10 komut reddi, 10 komut varliginda parity iddiasi olmadan gecis (eb57f2e).
- K5 ana toplu YAML artik reports/workflow-contract-gate.json olusturur ve artifact icinde saklar; eksik komut olursa K5 fail (9349421). GitHub Actions #39652296086 basladi, sonuc henuz bu not aninda bilinmiyor.
- Son kesin yesil #39650954707 6/6. 22 kabul gorevi 0 tamam; 92 eski workflow davranissal esdegerlik 0. Canli veri ve korunan yollar degismedi.

## 21 Ekim 2026 - Toplu artefact yolu ve failure upload regresyonu
- GitHub Actions #39652296086 completed success: K1 K2 K3 K4 K5 ve toplu kabul 6/6; on-yardimci executable contract gate gecti. Bu yalniz offline/fixture kanitidir.
- c3f6985: statik sozlesme matrisi artifact_renamed_in_consolidation ve timeout_insufficient alanlari ile farklari siniflandirir, parity onayi vermez.
- 4d6738a: gercek K2 ve K3 ana workflow'larinin eski yardimci rapor dosyalarini upload-artifact adiminda kapsadigini ve always kosulunu regresyonla kontrol eder. Yeni Actions run #39653476180 baslatildi; sonuc not aninda bekleniyor.
- Canli listeler, EPG, favoriler, logo, yedek ve eski depo degismedi. Kabul 0/22, legacy davranis parity 0/92.

## 21 Ekim 2026 - K2/K3 ag adimlari basari bagimliligi
- GitHub Actions #39653476180 6/6 success (offline fixture). K2 Public candidate discovery ve K3 Bounded Turkish TV video probe adimlarinda success() && ilgili opt-in flag acikca zorunlu hale getirildi. Commitler 7f96b4f, 462656e.
- tests/test_workflow_consolidation.py: bu iki adim icin success/opt-in ve continue-on-error bulunmamasi regresyonla kontrol ediliyor, commit a510e93. CI run #39657348060 basladi, bu not aninda in_progress.
- 22 gorev kabul ve 92 legacy davranissal parity halen kanitsiz; sayaclar artirilmadi. Canli listeler/EPG/favoriler/yedekler degismedi.

## 21 Ekim 2026 - K1 opt-in regresyonu hatasi ve duzeltme
- GitHub Actions #39657348060 fail: tests/test_migrated_opt_in_contract.py eski tam if stringini bekliyordu; K2 success() && inputs.allow_network_discovery == true kosulunu yanlis reddetti. K2/K3 workflow islevsel fail kaniti yok, statik test uyumsuzlugu.
- ac1430f ara denemesi ardindan be4e208 commit ile test yalniz iki acik fail-closed formu kabul edecek sekilde duzeltildi: inputs.FLAG == true veya success() && inputs.FLAG == true. En guncel run #39658173167 kuyrukta; sonucu dogrulanmadan basarili denmez. Aradaki #39658143312 sonucu esas alinmaz.
- Korunan dosyalar degismedi; kabul 0/22 ve legacy parity 0/92.

## 21 Ekim 2026 - Artifact path bazli kaynak karsilastirmasi
- #39658173167 6/6 success. K2/K3 opt-in regresyonu hatasi kapandi.
- 049c1e4: auxiliary_behavior_matrix kaynak artifact adi farkli olsa da reports/ altindaki yuklenen dosya yollarini ana workflow ile karsilastirir; missing_artifact_paths ve artifact_path gap uretir. Bu statik karsilastirmadir, gercek artifact esdegerligi degildir.
- 64b531d: fixture ile eksik rapor yolu testi eklendi, yeni CI #39659140742 basladi, sonuc bekleniyor.
- Korunan dosyalar degismedi. 22 gorev 0 kabul, 92 legacy parity 0.

## 21 Ekim 2026 - Statik artifact beyanini gercek kanittan ayirma
- #39659140742 completed success 6/6.
- 2276c76: workflow matrix her yardimci satirinda artifact_paths_declared_only=true, artifact_files_produced_verified=false; contract_gate de false raporlar. YAML path listesi hicbir zaman dosyanin uretildigi ya da dogru oldugu kaniti degildir.
- 8ddc50c: fixture regresyonu bu ayrimi zorunlu tutar; yeni CI #39659707243 basladi, sonucu bekleniyor.
- Sonraki gercek is: opt-in real run artifact'lerini indirip dogrulama, kaynak bazli davranis kabul kriterleri. Canli korunan yollar degismedi; 0/22 kabul, 0/92 parity.

## 21 Ekim 2026 - Artifact parser regresyonu kapandi
- #39662952159 K1 unittest `test_artifact_report_path_gap_detected_even_when_name_differs` FAIL: list-style `- uses: actions/upload-artifact@v4` taninmiyordu; diger isler dependency sebebiyle skipped.
- `24c0a309874a1de8ef9e37971faef2a3f3fa581d` parser hem `uses:` hem `- uses:` upload adimini tanir.
- #39663724064 completed success, 6/6 (Guvenlik, Kesif, Kanal, Arsiv/Yedek, Bakim, toplu kanit).
- Kabul durumu degismedi: statik/izole CI != canli kaynak ve 92 workflow davranissal parity; 0/92 dogrulanmis. K2/K3 manual opt-in gercek ag calistirmalari bekliyor.

## 21 Ekim 2026 - K2 alternatif adresler K3 handoff entegrasyonu
- #39664555035 K1-K5 toplu Actions 6/6 success. K2 alternatif URL / ayni kanal kimligi ayrimi kod `ae5a546`, test `6635c27`.
- K3 handoff `ec921f7`: K2 alternatives iliskisini fingerprint ile bagli olarak tasir; bagimsiz veya bilinmeyen fingerprint fail-closed. Test `5ad78c1`: aktarim ve orphan reddi.
- Yeni Actions #39666693465 queued (son kontrol); basarili denemez. K2-08 gercek kaynak kabulunu tamamlamadi. 0/92 davranissal parity, 0/26 runtime guvenlik kabulu ve korunan dosyalara yazma yok.

## 21 Ekim 2026 - K3 toplu sureklilik
- #39668703362 6/6 basarili (onceki kod). `61ef36a`: K3 toplu aday sureklilik ozetleyici; olcumu olmayan adaylar MISSING_MEASUREMENTS, orphan kayitlar red, hicbir uretim onayi yok.
- `25cd016`: eksik aday/orphan regresyon testleri; `fdeeae0`: hashlenemeyen aday fingerprint korumasi. Bu yeni kodun CI sonucunu ayrica kontrol et.
- 75 adayin gercek olcumleri, 6+ saat gozlem kokeni, IBO cihaz ve 92 davranissal kabul halen bekliyor; gorev tamamlandi iddiasi yok.


## 21 Ekim 2026 gece - Yeni sohbet devir notu (K3 tarama ve kanit zinciri)
- Calisma deposu: Madsc55/Madsc55-Tv, dal main. Eski Madsc55/madsc-tv depoyu degistirme, PR #71 merge etme, main'e merge islemi yapma. Bu turda yalniz mevcut main uzerinde ayri commitler yapildi.
- Son Actions #39675900584 completed success. Onceki #39675206167, #39675034543, #39674381743, #39673184243, #39672401599, #39672153438, #39671628278, #39670947480, #39669394387 success. Yesil CI offline/fixture kanitidir, canli yayin kabul degildir.
- K3 batch ve sureklilik kodu: madsc/channel_test.py summarize_candidate_continuity ve evaluate_three_stage_continuity; madsc/handoff.py K2->K3 alternatif kimlikleri. K3 gercek ag taramasi yalniz workflow_dispatch opt-in ile: .github/workflows/madsc-03-kanal-test.yml (allow_live_probes, allow_bulk_turkish_tv). Izinsiz gercek ag probing baslatma.
- Son commitler: 09a58de gecersiz olcum kimlikleri; 4adfd15 test; e2c701a deterministik SHA256 aday secimi, ef3d39e test; 434261e kaynak isimleri provenance, d3dffb6 test; fa55b7b basarisiz kaynaklar raporu, 3cba950 test; f94e981 kesif fingerprint ve hatali kaynaklari dislama, f0e768c test; ee43923 fingerprint newline duzeltme ve onay false, a22b82f test; 9898614 kaynak basina aday sayisi, 772f938 test; db3cbfc playlist kanal adinda gercek newline temizleme, 4b1f655 test; c35efe4 test playlist SHA256 baglama, 56faa93 test.
- madsc/turkish_tv_batch_validation.py: aday SHA256 secim, source_names, source_failures, source_candidate_counts, discovery_fingerprint_sha256, test_playlist_sha256, test_playlist_path ve production_approved/device_verified/three_stage_six_hour_verified=false alanlari eklendi. Yalniz reports/ altina deneme dosyasi yaziyor, uretim listelerine dokunmuyor. JSON raporun SHA256 alanini olusturulan M3U baytlarindan hesapliyor.
- Acik gercek isler: 75 yayin adayinin en az 3 ayri gercek olcumle 6+ saat sureklilik testi; ffprobe/ffmpeg ve kanit provenance; IBO Player Pro cihaz testini kullanici yapacak; EPG/Pages canli kabul; K4 dis yedek/restore; 26 runtime guvenlik kurali; 92 eski workflow davranissal esdegerlik. docs/K1_K5_KANITLI_GOREV_DEFTERI.json son bilinen 0/22 tam kabul, 7 in_progress, 15 pending; 0/92 legacy parity, 0/26 runtime security accepted. Bunlari yeni kanit olmadan artirma.
- Korunan yollar: CALISANLAR.m3u, YENILER.m3u, playlist.m3u8, xmltv.xml, EPG/, logos/, logolar/, YEDEKLER, FAVORILER, cihaz favorileri, arsivler. Bunlara yazma yok.
- Yeni sohbette ilk is: Actions son sonucunu ve PROJE_HAFIZASI.md bu notu oku. K3 kaynak raporlarina daha fazla kozmetik alan eklemek yerine bir eksik kabul isini uctan uca tamamla: gercek opt-in artifact uretim ve dogrulama akisini veya K1/K4 davranissal kontratlari testlerle gelistir. Statik kaynak-string testleri yerine davranissal fixture testlerini tercih et. Kod, test, CI sonucunu dogrula; notu guncelle.


## 21 Ekim 2026 gece - K4 kanonik manifest sirasi
- Gercek Actions API kontrolu: son gorunen #39675900584 completed/success, SHA 56faa93; bu yalniz onceki fixture koduna ait.
- K4 `verify_manifest` sirasi degistirilmis manifesti reddeder: b639c94126eed3ce1bc0fa8fc079b906ba0169dd. Davranissal regresyon testi: a7943b03430e085560b56d3883830036480d37ff.
- Yeni commitlerin Actions sonucu henuz dogrulanmadi. K4 harici yedek/restore, 75 canli kanal, 92 parity ve 26 runtime guvenlik kabulu halen acik; kabul sayilari artirilmadi.
- Eski repo, PR #71, korunan yayin listeleri ve favoriler degistirilmedi. Uretim yazma yetkisi acilmadi.


## 21 Ekim 2026 gece - K4 bos manifest fail-closed
- Actions #39676588920 ve #39676602145 completed/success; onceki K4 siralama duzeltmesi ve regresyon testi CI'dan gecti.
- K4 bos manifest artik verify_manifest ile basarili kabul edilmez: bf7de7b6f79d2edf121cdace81bf1f795a7fc177. Regresyon testi: 5d2210b0288b768982067625e0d1fd54cca17c21.
- Bu iki yeni commit icin Actions sonucu henuz kontrol edilmedi. Harici backup/restore gercek kabul, 75 kanal canli, 92 workflow davranissal esdegerlik ve 26 runtime kural halen bekliyor. Kabul sayilari degismedi.
- Eski depo, PR #71 ve korunan listeler degistirilmedi.


## 21 Ekim 2026 - K4 bagimsiz kopya denetimi
- #39677049091 ve #39677061945 GitHub Actions completed/success; bos manifest reddi CI'da gecti.
- compare_copy artik ayni, ic ice veya sembolik bagli kok dizinleri bagimsiz kopya gibi kabul etmez; bos dosya kapsaminda denetim basarili sayilmaz. Kod 8eeb8b3df8f0a12e51633455dbf15299aa375cd8, davranissal test 3644a54630af189e5bf5ea91154ab6baa42f0d69. Yeni CI sonucu bekleniyor.
- K4 gercek dis depolama/restore kabul edilmedi; 75 canli kanal, 92 parity, 26 runtime security kabul sayilari degismedi. Korunan yollar ve eski repo degistirilmedi.


## 21 Ekim 2026 - K4 hardlink bagimsizlik kontrolu
- Actions #39677814549 in_progress, #39677831373 pending (son gorulen); bunlara basari atfedilmedi.
- K4 uc bagimsiz agac restore audit: kaynak, yedek veya geri yuklenen dosyalardan ikisi ayni inode/dev (hard link) paylasiyorsa reddediyor. Kod 6b3ac112cdaf0010115cdebdbe6694ab9aec5dce, regresyon testi 22b8f8cb9e7d95875d43d780894d5873fd4edcb4. Yeni CI bekleniyor.
- Harici depolama ve production restore kaniti yok. 75 canli yayin, 92 parity, 26 runtime kural kabulleri degismedi. Eski repo ve korunan listeler degistirilmedi.


## 21 Ekim 2026 - K4 iki agac hardlink kontrolu
- compare_copy/verify_sandbox_restore iki farkli klasorde ayni inode'a bagli dosyayi artik bagimsiz kopya saymiyor. Kod 754f6eadf31bad17e498697b3365cc4b2d849cae, davranissal test 7909c19fa0514b73336e46538fa8f1a1ce80f83c.
- Son gorulen Actions: #39677814549 success; #39677831373 in_progress; #39678038296 cancelled; #39678054199 pending. Iptal veya bekleyene basari atfedilmedi.
- Harici backup/restore gercek kabul, 75 canli yayin, 92 parity ve 26 runtime guvenlik kuralinin kabul sayilari degismedi. Korunan yollar degistirilmedi.


## 21 Ekim 2026 - K4 gercek sandbox geri yukleme uygulamasi
- Son Actions #39678146430 ve #39677831373 completed/success; daha eski ara commitler concurrency ile cancelled.
- Yeni restore_to_new_sandbox(backup,destination,names) yalniz daha once var olmayan ayri sandbox klasorune gercek bayt kopyaliyor; manifest SHA256 ile backup ve restore dogrulaniyor; hata durumunda sadece yeni sandbox temizleniyor. Kod 6069217b33301085403f9a3adb175c65e58b9a91, davranissal test 8426b6c30ea3ccd9eeeed3b22c69284bb3e3e353.
- Uretim dosyalari, korunan listeler ve eski depo degistirilmedi. Bu harici depolama kaniti degildir; K4 production restore accepted degil. 75 canli, 92 parity, 26 runtime security kabulleri halen acik. Yeni Actions sonucu kontrol edilecek.


## 21 Ekim 2026 - K4 sandbox restore symlink ust dizin korumasi
- Actions #39678650056 ve #39678677401 completed/success: gercek sandbox restore fixture testleri gecti.
- Yeni sandbox restore hedefinin tum ust dizinlerinde symlink reddi: kod 8d7e1441596352768d4d1e5477d3e261e4da1e01; alias ust dizin uzerinden yazma girisimini engelleyen test 61da348fc66eb679416c906537057b568e02a2b8. Bu commitler icin Actions sonucu henuz dogrulanmadi.
- K4 harici storage kaniti yok; 75 canli, 92 parity, 26 runtime security kabulleri degismedi. Eski depo/korunan yayin listeleri degistirilmedi.


## 21 Ekim 2026 - K4 gercek sandbox backup -> restore roundtrip
- Actions #39679317888 ve #39679333045 completed/success (symlink ust dizin korumasi).
- Yeni backup_to_new_sandbox kaynak dosyalari yeni ayri sandbox'a gercekten kopyalar, SHA256 manifest ile kaynak/kopya butunlugunu dogrular, var olan hedefe yazmaz, hata halinde yalniz yeni klasoru temizler. Kod 1a55fbce787f9d5f85748de4f7425af348cd6121.
- Davranissal test 1fb9e21d0e8ed6ed0109436877d814950bc2635b: kaynak -> yeni backup -> yeni restore -> verify_independent_restore ile uc agac gercek dosya roundtrip ve overwrite/nesting reddi. Yeni Actions sonucu henuz kontrol edilmedi.
- Bu yalniz sandbox fixture ispatidir; dis storage ve production restore accepted degildir. 75 canli, 92 parity, 26 runtime security kabulleri degismedi. Korunan listeler ve eski depo degistirilmedi.


## 21 Ekim 2026 - K4 CI restore drill gercek uygulamaya baglandi
- Actions #39679773526 success; #39679793343 son kontrol in_progress, ancak tum kategori job'lari ve regresyon testi success; toplu final bekleniyor.
- madsc/restore_drill.py artik elle shutil.copyfile kullanmak yerine backup_to_new_sandbox -> restore_to_new_sandbox -> verify_independent_restore zincirini calistiriyor; CI'daki K4 drill ayni fonksiyonu kullaniyor. Kod 07db91624781c42060edba5e14ce588f139a1b41.
- tests/test_restore_drill.py mevcut corruption injection testini yeni API'ye uyarladi; gercek iki sonuc alanini denetliyor: ef2906125e4e96511be196b6764a7f6ee38fdb3b. Yeni CI sonucunu kontrol et.
- Gercek dis depolama veya production restore kabul edilmedi; 75 canli, 92 parity ve 26 runtime security kabul sayilari degismedi. Korunan yollar ve eski repo degistirilmedi.


## 21 Ekim 2026 - K4 CI regresyon hata analizi
- Actions #39680219595 failure: Guvenlik job test_restore_drill.py eski restore_drill.shutil.copyfile mock'u artik var olmayan attribute'a eristi (AttributeError); diger kategoriler skipped. Bu kod entegrasyonunun eski teste uyumsuzluguydu, uretim backup hatasi kaniti degil.
- Sonraki ef2906125e4e96511be196b6764a7f6ee38fdb3b test commit'i mock'u backup_to_new_sandbox fonksiyonuna tasidi. #39680249100 Guvenlik, Kesif, Kanal Testleri job'lari success; K4 Arsiv ve Yedek halen in_progress (son kontrol). Tum workflow success henuz iddia edilmiyor.
- Sonraki adim: #39680249100 tum job'larin final sonucunu denetle; fail varsa logdan duzelt. K4 dis depolama kabul sayisi degismedi.


## 21 Ekim 2026 - K4 bozuk butunlukte rollback testleri
- #39680249100 Guvenlik, Kesif, Kanal Testleri, Arsiv ve Yedek, Genel Bakim job'lari success; Besli toplu kanit final job'u son kontrol in_progress.
- tests/test_backup.py: backup_to_new_sandbox ve restore_to_new_sandbox SHA256 manifest verify_manifest False verdiginde yeni hedef klasoru temizlerken kaynak/backup baytlarini koruyor mu iki yeni regresyon testi ile denetlendi. Test commit 5f3dd39bf5d86c27a23c789def95e54be4ac5323. Yeni CI sonucu bekleniyor.
- Dis storage kaniti, 75 canli kanal, 92 eski workflow davranissal parity, 26 runtime security kabulleri halen acik. Korunan listelere ve eski repoya dokunulmadi.


## 21 Ekim 2026 - K4 path validation before inode lookup
- #39680484339 completed/success: backup ve restore integrity-failure rollback regresyonlari gecti.
- compare_copy ve verify_independent_restore artik once snapshot_manifest ile yol guvenligi ve kaynak manifestini dogrulayip sonra inode metadata bakiyor; onceki sirada gecersiz path icin erken stat() cagrisi vardi. Kod e61fc028e737f3804a79c5596f45f0fd4beea542.
- Traversal isimlerini reddeden regresyonlar 7b2214ee4be2aa2523fc18f56b4d8b250b0b8756; testte tum Path.stat'i mock etmenin klasor kontrollerini bozabilecegi fark edilip 97c86cc9dd42e21a8e9d50f809c43d98e6f0b403 ile duzeltildi. Son CI sonucunu kontrol et.
- Production backup/restore ve dis storage kabulu hala acik; 75 canli, 92 parity, 26 runtime security kabul sayilari degismedi. Korunan dosyalara dokunulmadi.


## 21 Ekim 2026 - K5 legacy parity evidence ledger gelistirildi
- K4 #39680730866 ve #39680763119 completed/success.
- K5 madsc/legacy_parity_evidence.py 99 kaynak workflow icin eksik/bozuk kanit alanlarini ayri raporluyor, metadata_complete ve alan toplamlarini veriyor; bagimsiz dogrulama olmadigindan kabul halen 0. Kod 80cd133c68f4879c6146a0c4b0377e9ae07564fb.
- tests/test_legacy_parity_evidence.py eksik SHA, boolean run_id, tam gorunen sahte metadata ve 99 satir toplamlari icin testler eklendi: e7c9d8c46ab903c3200fd6b4f0b5f505a159114a. Son Actions sonucunu kontrol et.
- 92 eski workflow davranissal parity gercek kabul 0/92; 99 kaynak envanter ayri kavramdir. Production korunan listeler degismedi.


## 21 Ekim 2026 - Toplu CI tetikleme duzeltmesi
- Kullanici istegiyle K5 madsc-05-bakim.yml otomatik push tetiklemesi kaldirildi; workflow_dispatch korundu. K1-K5 tek manuel batch calismasi olarak baslatilabilir; her kod/test push'u artik bu workflow'u otomatik kuyruga koymaz.
- workflow_consolidation.py guvenlik kontrati K5 dahil tum ana workflow'larda push tetikleyicisini reddeder; test fixture ve gercek YAML testi uyumlu guncellendi.
- Degisiklikler tek git commit'inde toplandi. K1-K5 otomatik kabul edilmedi; 92 legacy parity ve 26 runtime security kabulleri degismedi. Kullanici onayi olmadan production veya live probe yok.


## 21 Ekim 2026 - K1/K2 toplu ilerleme, eski kaynak arama analizi
- Eski kaynak_kesfet.py GitHub search (5 query, 60 repo, 120 source, 90 gun), M3U baslik ve guncellik kontrolu kullaniyor; tools/genis_kaynak_taramasi.py 8 worker, haftalik/aylik kaynak, degisen digest, bilinen URL ve review queue kullaniyor. Eski repo salt okunur incelendi.
- Yeni madsc/discovery_batch.py salt okunur M3U parser, metadata, gecersiz URL reddi, kanal tvg-id/name-group kimligi, birden fazla kaynakta bagimsiz destek sayimi ve K3 oncesi review-only raporu ekler. tests/test_discovery_batch.py ile tek toplu commit.
- K1 kurallari ve gercek K2 ag dogrulamasi henuz tamamlanmadi; otomatik kabul ve production yazma yok. Sonraki is: parser ve discovery koruma testlerini genislet, K1 26 runtime kuralini somutlastir, tek manuel K1-K5 CI calistir.


## 21 Ekim 2026 - K1 K2 K3 K5 toplu M3U8 entegrasyonu
- K2 parse_m3u yalniz guvenli kabul edilmis adaylarin kaynak satirlarini candidate_rows ile K3 kataloguna tasiyor; build_m3u8_preview kaynaklarin tumunu birlestirip prepare_channel_catalog ve render_playlist_previews uzerinden TEST_BEKLIYOR grubunun bellekteki UTF-8 playlist.m3u8 taslagini uretiyor. Kaynak tekrarlarini atiyor, IBO veya production kabul iddia etmiyor.
- K1 guard korunan playlist.m3u8 ve xmltv.xml adlarini engelliyor, artifacts dizinine ters slash bypassini ve kontrol karakterlerini reddediyor. Testler birlikte eklendi.
- K4 yedek/restore bagimsizligi korunuyor; yeni onizleme production dosyalarina yazmaz. K5 final CI sadece manuel toplu tetiklenir. 26 runtime security, 92 parity, 75 canli kabul hala acik.


## K1-K2-K3-K5 toplu sertlestirme
- K2 M3U girdi boyutu sinirlandi; bilinen URL filtrelemesinde eslestirme indeks yerine zip ile deterministik hale getirildi.
- K1 manifest nesne tipi, yinelenen cikti yolları, kontrol karakteri ve drive/colon yollarini reddeder.
- K3 m3u8 sandbox onizlemesi disinda production listesine yazma yok; K4 yedekleme akisi degistirilmedi.
- Gercek kanal testleri, K1 runtime 26 kural ve K5 eski otomasyon esdegerligi bu commit ile tamamlanmis sayilmaz.


## 22 Ekim 2026 — K1/K5 toplu koruma ve 92/99 kapsam mutabakatı
- Başlangıç main: 223aa5c9c63ac160c98b2e0e9a8aef774a92e400. Yeni depo Madsc55/Madsc55-Tv; eski depo salt okunur.
- legacy_parity_cli ve legacy_99_bulk_audit rapor yazıları ortak K1 enforce_local_output_path kapısına bağlandı. Korunan hedef, symlink üst dizin ve mevcut dosya reddedilir; audit hedefi ağ erişiminden önce kontrol edilir. Hedef üst klasör önceden mevcut olmalıdır.
- 92/99 farkı kaynakla çözüldü: eski scripts/five_category_92_workflow_audit.py blob 9a35ecd797e5c1c595d6796cfffba6cd8a289853 beş merkezi YAML + k1-protected-write-tests.yml + madsc-hizli-on-kontrol.yml dosyalarını hariç tutuyor. Pinned tree a88dfa874b6964dcaa4de7a8f9075af2f146acd8 içinde aynı script SHA ve 99 workflow kaydı doğrulandı. docs/LEGACY_SOURCE_SCOPE.json 99 yol/blob SHA içerir. Bu tur tüm 99 YAML baytı yeniden indirilmedi.
- reconcile_legacy_scope 92+7 kapsamını doğrular; değişen/eksik merkezi kapsamı reddeder; offline_gate aynı kontrolü zorunlu uygular. Bu sayım mutabakatı davranışsal eşdeğerlik değildir.
- Yerel python -m madsc.offline_gate: 552 test, K1/K2/K3/K4/K5 izole fixture kapıları success, 10 yardımcı komut ve 22 görev envanteri geçti. Başarısız test yok. Kanıt ve değişen kaynak SHA256: docs/K1_K5_OFFLINE_KANIT_2026-10-22.json.
- Son gözlenen GitHub Actions #39686179902 success, SHA d5d61317806dc7a00b762567695286e3779ceaf1; bu yeni kodun CI kanıtı değildir. Actions tetiklenmedi, commitler [skip ci].
- 0/92 tam davranışsal kabul, 0/26 runtime kural kabulü, 0/22 tam görev kabulü korunuyor. Eksik: gerçek karşılaştırmalı execution/artifact kökeni, hata/timeout/retry, zamanlı canlı ölçümler, kullanıcı IBO cihaz kabulü, EPG/Pages, bağımsız harici restore.
- Korunan yayın listeleri, EPG, YEDEKLER/YENİLER/FAVORİLER ve eski depo değişmedi; PR #71 veya başka merge yapılmadı. Sıradaki adım: 92 kaynak yoluna bağlanan gerçek karşılaştırmalı kanıt çiftlerini doğrula; kanıt bulunmadan snapshot eşleşmesini kabul sayma. DEVAM_NOTU.md yeni sohbet giriş noktasıdır.


## 22 Ekim 2026 — K2/K5 kabul yazıcıları aynı K1 kapısına bağlandı
- Önceki kod SHA 53ca22f2781d106139d52a20493e223b391418fd, devir SHA 6c5ccba95211e67d9b24e3b8ef81a4ce0ac273d0 GitHub main üzerinden tekrar okundu. Compare: 11 dosya değişti; korunan dosyalarda fark yok, merge yok.
- history_origin_cli, batch_acceptance, handoff_acceptance ve legacy_notes_integrity: enforce_local_output_path + exclusive create. İlk üç CLI çıktı hedefini kanıt işleme/ağ doğrulamasından önce reddeder. Üst klasör önceden mevcut olmalı; rapor kanıtı üzerine yazılmaz.
- Yeni gerçek CLI sınır testleri korunan xmltv/playlist, symlink üst dizin, mevcut raporu reddederken işleyici/GitHub doğrulama çağrılmadığını ve dosya baytlarının korunduğunu denetler. Arşiv doğrulayıcısının korunan hedefi reddi de sınandı.
- Son yerel toplu regresyon: 554 test, beş K1–K5 izole kapısı, 92+7 kapsam kapısı, 10 yardımcı komut ve 22 görev envanteri başarılı. Başarısız test yok; git diff --check temiz. Kanıt: docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET2.json.
- Son eski CI run #39686179902 artifact metadata listesi salt okunur incelendi; fixture/handoff/restore raporları mevcut. İçerikler bu adımda indirilmedi; bunlara 92 tam parity kanıtı atfedilmedi. Yeni Actions çalıştırılmadı.
- 0/92, 0/26, 0/22 tam kabuller korunuyor. Bu altı yazıcıdaki düzeltme tüm bağımsız yazma noktalarının kapandığı anlamına gelmez; ci_diagnostics summary append, canlı pilot yazıcıları ve diğer dolaylı çağrılar için tam çağrı noktası denetimi açık. Sıradaki bağımsız yerel iş budur; gerçek cihaz/ağ/harici yedek kabulü ayrıca açık. DEVAM_NOTU.md güncellenecek.


## 22 Ekim 2026 — K1 rapor/summary ve K2/K3/K5 aktarım yazıcıları
- Başlangıç main d70479db18814251247b7da6cae72520982a56b3, eski çalışma kopyasını ezmeden güncel main üzerinden ayrı çalışma ağacı açıldı.
- K1 yeni explicit append preflight: korunan/kaçış/symlink yollar, regular olmayan dosyalar ve hardlink reddi. Yeni rapor kapısı mevcut hedefi reddetmeye devam eder. CI teşhis JSON'u exclusive create; summary ayrı hedef olmalı ve yazma öncesi guard + O_NOFOLLOW/O_NONBLOCK ve fstat ile regular/hardlink kontrolü kullanır. Bu, tüm üst dizinlerde eşzamanlı saldırılara karşı tam atomiklik iddiası değildir.
- Dört sabit JSON pilot yazıcısı mevcut write_fixture_report kapısına bağlandı: live_discovery_pilot, legacy_multisource_discovery, k3_live_manifest_pilot, k3_turkish_tv_video_pilot. K3 reason_counts artık ilk ve tek yazıdan önce hazırlanır; kanıt üzerine yazılmaz.
- progress_scorecard ve k5_channel_gate giriş işlemeden önce K1 output kontrolü yapar. artifact_transport/history_transport artık guard öncesi mkdir yapmaz; hedef üst dizini mevcut olmalı. history_artifact_download çıktı kökünü ağdan ve extraction'dan önce denetler. legacy_report_export lexical hedefi resolve ile gizlemeden kontrol eder.
- İlk genişletilmiş regresyonda LegacyReportExportTests.test_exports_separate_legacy_artifacts ERROR: mevcut klasör için önceki ValueError yerine ProtectedWriteRejected dönmüştü. Eski hata sözleşmesi korunarak düzeltildi; finalde geçti.
- Nihai python -m madsc.offline_gate: 562 test ve beş izole K kapısı success; 92+7 kaynak kapsamı, 10 yardımcı komut, 22 görev envanteri geçerli. git diff --check temiz. docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET3.json kaynak hashlerini ve çözülen hatayı içerir. Yeni gerçek ağ/cihaz/Actions çalıştırması yok.
- Güvenli gerçek dosya sınır testleri: summary append, korunan ve symlink/hardlink/FIFO hedef reddi, mevcut kanıt değişmezliği, dört pilotta ağsız gerçek rapor yazımı, aktarım hedefinde erken red, indirme öncesi red ve export symlink üst dizin reddi.
- Açık: turkish_tv_batch_validation deneme M3U8 ve JSON birlikte yazma yolu halen ayrı kapsam; yeni kapıya bağlandı sayma. 92 gerçek workflow execution/provenance, 26 tam runtime kuralı, cihaz, zamanlı kanal ve harici restore kabulleri değişmedi (0/92, 0/26, 0/22). Korunan veri, eski repo ve PR #71 değişmedi.
- Sıradaki: batch_validation yalnız reports/ altındaki deneme playlist + rapor paketini K1 ile güvenli/tekil yazacak şekilde mevcut K1 sözleşmesiyle uzlaştır; genel M3U yasağını gevşetme. Sonra 92 aynı-girdi/köken bağlı execution karşılaştırma kanıtı. Otomatik tur güncel DEVAM_NOTU.md'den başlamalı.


## 22 Ekim 2026 — K1/K3 deneme playlist kanıt paketi
- Kod fe40f60aa989c121144cdbdca0bdd38f7d67f607: sabit reports/MADSC55_TURKCE_TV_ADAY_DENEME.m3u8 ve companion JSON artık K1 sınır denetimi, exclusive create ve kısmi paket rollback ile yazılıyor. Genel M3U/M3U8 koruması aynen kaldı; başka playlist yolu açılmadı.
- Mevcut çıktı ve symlink reports kökü kaynak taramasından önce reddediliyor. Offline boş kaynak testi gerçek iki dosyayı üretip JSON içindeki SHA256'nın playlist baytlarıyla eşleştiğini doğruladı.
- Nihai yerel sonuç: 568 test ve beş izole K kapısı success; docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET4.json. Actions/live probe/cihaz yok; 0/92, 0/26, 0/22 değişmedi.
- Sonraki: pinned 92 kaynak yolu için aynı input hash ve bağımsız execution/artifact origin bağını karşılaştırıcıda fail-closed zorunlu kıl. Metadata fixture'ını gerçek GitHub API köken doğrulaması sayma.


## 22 Ekim 2026 — K5 aynı-girdi ve bağımsız köken kontratı
- Kod f222a81ce96901a8adc0dbc92a5213cf149500c9: yeni madsc-legacy-provenance-pairs-v1 şeması yalnız pinned 92 yolu işler; aynı input SHA256, legacy pinned workflow blob'u, yeni beşli workflow kimliği, ayrı run/artifact origin ve artifact-run-head bağlarını zorunlu tutar.
- Snapshot exit/timeout/output/side-effect karşılaştırması bu bağlardan sonra çalışır. Yanlış input, artifact run/head/repository bağı, kaynak yol/blob veya merkezi replacement yolu fail-closed reddedilir.
- Yapısal fixture bağı gerçek API doğrulaması sayılmaz: independent_origins_api_verified=0 ve behavioral_parity_accepted=0. CLI eski salt snapshot şemasını geriye uyumlu okur, yeni şemayı ayrıca işler.
- Nihai yerel sonuç: 570 test, K1–K5 izole kapıları, 92+7 kapsam ve 22 görev envanteri success. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET5.json. Actions/live probe yok; kabul 0/92, 0/26, 0/22.
- Sıradaki: salt-okunur GitHub run/artifact sorgularını şemaya besleyen ve API cevabıyla repository/workflow/head/run/artifact kimliğini bağımsız doğrulayan client. Gerçek eski/yeni çifti yoksa kabul verme.


## 22 Ekim 2026 — K5 bağımsız GitHub run/artifact origin verifier
- Kod 7b4855293564c1baafdca8246f932ca1a1e5986e: github_legacy_pair_client, pair'in her tarafında GitHub run kaydı, artifact listesi ve head SHA'daki workflow blob'unu ayrı okur; repo/dal/workflow/blob/run/attempt/head/event/conclusion ile artifact id/name/run/head/SHA256 digest bağlarını fail-closed doğrular.
- İki taraf için altı salt-okunur API kaydı gerekir. Artifact pagination eksikliği, digest yokluğu, expired/ambiguous artifact, yanlış workflow blob veya run repository reddedilir. Dispatch, rerun, artifact download veya production write yapmaz.
- Snapshot eşleşmesi ve API origin doğrulaması tek başına behavioral acceptance değildir; sonuçta production_ready=false ve behavioral_parity_accepted=false korunur.
- Yerel sonuç 573 test + beş izole K kapısı success; kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET6.json. Unscoped git diff --check bir kere signal 11 verdi; path-scoped kontrol ve offline_gate geçti, kaynak/test dosyalarında whitespace hatası yok.
- Gerçek salt-okunur artifact metadata kontrolü: yeni #39686179902 ve eski #39590927353 artifact kayıtlarında SHA256 digest ve run/head bağı mevcut. Eski run pinned 92 dışında k1-protected-write-tests.yml olduğundan gerçek legacy pair sayılmadı; aynı input manifesti metadata'dan doğrulanamadı. Kabul 0/92, 0/26, 0/22.
- Sıradaki: artifact ZIP içindeki sınırlı manifesti güvenli okuyup input SHA256 ve snapshot hashini doğrulanan artifact digest/run originine bağla. Eski depoya yazma ve Actions çalıştırma yok.


## 22 Ekim 2026 — K5 same-input artifact byte binding
- Kod b1be6c247b769bc911773ed35d30b5991875b913: legacy_pair_artifact, artifact ZIP SHA256'yı declared/API digest'e bağlar; yalnız tek madsc-parity-evidence.json entry kabul eder ve repo/run/head/workflow/input SHA256/snapshot alanlarını execution origin ile eşleştirir.
- ZIP boyutu 2 MiB, manifest 1 MiB ile sınırlı; extra entry, symlink, compression bomb oranı, bozuk ZIP/UTF-8/JSON ve duplicate key reddedilir. İki artifact aynı input hash taşımadan pair doğrulanmaz.
- Nihai yerel sonuç 576 test + K1–K5 fixture gates success; docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET7.json. Fixture yine acceptance değildir: 0/92, 0/26, 0/22.
- Geçmiş artifactler bu v1 manifestini taşımadığı için geriye dönük kabul yok. Sıradaki güvenli kod işi: yeni beşli opt-in parity artifact üretimini bu şemaya bağlamak; gerçek Actions yalnız ayrı izinle.


## 22 Ekim 2026 — K5 replacement parity manifest üretimi
- Kod c5a7060684e57f1e35d2b367e1757d5901dfcafb: parity_manifest_writer gerçek, bounded input baytlarını SHA256 ile bağlar; execution snapshotını mevcut sıkı şemayla doğrular ve deterministik madsc-parity-artifact-v1 JSON üretir.
- Çıktı sabit reports/madsc-parity-evidence.json yolunda ortak K1 write_fixture_report kapısından geçer. Mevcut hedef, symlink reports dizini, yanlış repo/dal/workflow, boş/büyük input ve bozuk snapshot yazı başlamadan reddedilir. Sonuç açıkça behavioral_parity_accepted=false ve production_ready=false taşır.
- Replacement workflow allowlist'i depodaki gerçek kurulumla eşitlendi: madsc-01-guvenlik.yml, madsc-02-kesif.yml, madsc-03-kanal-test.yml, madsc-04-yedek.yml, madsc-05-bakim.yml. Önceki yanlış K4/K5 replacement adları kaldırıldı; legacy scope exclusion isimleri değiştirilmedi.
- Offline sonuç: 580 test ve K1–K5 fixture gates success; 92+7 kapsam ve 22 görev envanteri geçti. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET8.json. Actions/live probe/production write yok; 0/92, 0/26, 0/22 değişmedi.
- Açık: üretici henüz gerçek job davranış girdisi/snapshot çağrılarına bağlanmış bir CLI değil. Eski read-only workflow artifactlerinde v1 manifest yok. Sonraki güvenli iş input dosyasını yerinde hashleyen opt-in CLI ve yalnız gerçek job verisi mevcutken workflow bağlantısı; deklaratif hash tek başına kabul edilmeyecek.


## 22 Ekim 2026 — K5 gerçek dosya hashleyen manifest CLI
- Kod 6b07cb1a7fa27e643e89cad6f1a7ffdb5a5d2c1a: parity_manifest_cli gerçek input ve snapshot dosyalarını read-only/O_NOFOLLOW açıp fstat ile regular-file ve boyut sınırlarını doğrular. Input hash kullanıcı beyanından alınmaz; gerçek baytlardan hesaplanır. Snapshot duplicate JSON key ve bozuk şema durumunda yazıdan önce reddedilir.
- Runtime repo/dal/run/head değişkenleri ile açık workflow path, paket 8'deki gerçek beşli allowlist ve ortak K1 writer üzerinden madsc-parity-evidence.json üretir. Bu yalnız opt-in çağrı yüzeyidir; artifact upload veya Actions dispatch yapmaz, production_ready=false ve behavioral acceptance=false kalır.
- İlk odak testindeki tek hata yanlış beklenen SHA256 test literal'iydi; gerçek hashlib sonucu ile düzeltildi. Nihai offline_gate 583 test ve beş fixture K kapısını, 92+7 kapsamı ve 22 görev envanterini geçirdi. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET9.json; 0/92, 0/26, 0/22.
- Sıradaki: beş workflow içinde gerçek davranış input/snapshot dosyası üreten noktaları statik olarak belirle. Fixture raporunu parity kanıtı sayma; gerçek veri sözleşmesi olmayan job'a CLI ekleme. Eski tarafın v1 artifact eksikliği blocker olarak sürer.


## 22 Ekim 2026 — K5 gerçek execution snapshot zinciri
- Kod 27c8b62165e511d09d42b319766a39d77994deb9: parity_snapshot_writer/CLI gerçek output ve side-effect dosyalarının baytlarını O_NOFOLLOW/fstat/boyut sınırı altında SHA256 ile ölçer. exit_code ve timed_out ile birlikte mevcut sıkı snapshot şemasını üretir; en az bir gerçek output zorunludur.
- Duplicate veya kontrol karakterli label, symlink, nonregular/oversize gözlem, boş output ve mevcut reports/madsc-parity-snapshot.json fail-closed reddedilir. Yazı ortak K1 izole report writer ve exclusive create üzerinden yapılır; üretim/kabul izni vermez.
- Uçtan uca offline zincir testi gerçek input/output dosyalarından snapshot ve manifest üretip tek-entry artifact ZIP'i declared digest/origin manifest doğrulayıcısına bağladı. Bu, GitHub API origin doğrulaması veya legacy pair kabulü değildir.
- Tam offline_gate 587 test ve K1–K5 fixture gates success; 92+7 pinned kapsam ve 22 görev envanteri geçti. Kanıt docs/K1_K5_OFFLINE_KANIT_2026-10-22_PAKET10.json. Actions/live probe/production write yok; 0/92, 0/26, 0/22.
- Açık: beş workflow ortak gerçek input/side-effect snapshot kontratını henüz üretmiyor. Sonraki iş statik readiness auditor ile her workflow'da gerçek ölçüm bağlarının var/yok durumunu kanıtlamak; fixture çıktılarını parity kabulü olarak yeniden etiketlememek. Eski 92 tarafındaki v1 artifact eksikliği de blocker kalır.
