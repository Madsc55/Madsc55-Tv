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
