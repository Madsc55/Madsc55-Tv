# KAYNAK NOTLAR VE BESLI SISTEM KARSILASTIRMA - 19 EKIM 2026

## Denetim kapsamı ve kanıt düzeyi
Eski salt-okunur depo: Madsc55/madsc-tv, madsc/bes-sistem-toplu-birlestirme, commit ca374df3b9585c0d76a078db9536150ebbc260f7.
Git tree recursive=true ve truncated=false: 822 blob, 99 .github/workflows dosyası. Yeni main: 49 blob (inceleme anı).
Asagidaki 10 eski merkezi belge ve 4 yeni merkezi belge GitHub'dan okunarak baslik, kapsam, karar ve tutarlilik acisindan karsilastirildi. 810 eski dosyanin her birinin satir satir yeniden okunmasi veya tum davranislarin kanitlanmasi DEGILDIR.

## Okunan eski belgeler
- 810 dosya notu.md (3393 satir): baslangicta 361/810 ilk tur ve 449 kalan; ilerleyen kayitlarda D2 437 dosya icin gorev/kanit satirlari olusturma ihtiyaci. D2 kayitlari D3 veya davranissal kabul degildir.
- AGENTS.md: 26 kural, IBO kullanici kararlari, Türkce workflow/job/step isimleri, sohbet devri ve koruma.
- BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md: 92 tarihsel tetik; 99 guncel sayimin yerine gecmez.
- DEVAM_NOTU.md: 3925 satirlik tarihce, son devir, gecmis K1-K5 kabul sinirlari; onceki dal talimatlari yeni depo kararinin yerini almaz.
- DEVIR_NOTU_2026-10-15.md: yedeklere aday ekleme karari IPTAL; kullanici yeniden istemeden eklenmez.
- GUVENLIK_KURALLARI.md: koruma ilkeleri, ortak devre kesici eksigi.
- IPTV_PROJE_HAFIZASI.md: kanal ve IBO kimlik kararlari, playlist korunmasi.
- ONCELIK_1_BES_MERKEZI_OTOMASYON_PLANI.md: tekrar tetiklemeyi azalt, ayda yaklasik 3-5 kapsamli kontrol hedefi.
- OZELLIK_ENVANTERI.md: eski uygulama kanitlari; EPG Pages, VOD, aday, 24h tekrar ve medya kontrolu.
- YENIDEN_KURULUM_KORUMA_PLANI.md: eski veri ve davranis korunur, yeni sistem izole; eskiyi erken kapatma yok.

## Okunan yeni belgeler
- PROJE_HAFIZASI.md
- docs/KURULUM_PLANI.md
- madsc/LEGACY_WORKFLOW_ON_ENVANTER.md (99/99 YAML ilk tur; davranissal degil)
- README.md

## Uyumsuzluklar ve kapanis kapilari
1. 810 / 822: eski not 810 bloblu tarihsel tree icin; guncel 822. Eski 810 dosyanin bire bir eslestirme manifesti ve yeni 12 dosyanin delta denetimi tamamlanmadi. 810/810 yeniden icerik dogrulamasi iddia edilmez.
2. 92 / 99: eski main tetik sayimi ile yeni dalda 99 workflow farki kaynak bazinda aciklanmali. 99 YAML envanteri davranissal esdegerlik degildir.
3. Eski YENIDEN_KURULUM_KORUMA_PLANI bes kategori olarak 3 kanal/veri, 4 EPG/logo tarif eder; yeni plan 3 kanal testi, 4 yedek. Her eski islev icin sahip K1-K5 ve devir baglantisi acikca eslenmeden parity denemez.
4. AGENTS Kural 26 Türkce Actions workflow/job/step gorunen adlari; yeni .github/workflows dosyalarinda ayrica kontrol edilmesi gerekir.
5. EPG Pages yayini, VOD, aday bekletme, tekrar test, logo/EPG eslestirme, IBO cihaz kimligi, korunan listeler ve bagimsiz restore icin davranissal kabul ayridir.
6. K1 26 kural icin runtime negatif test, gercek git diff write gate, ortak devre kesici; K3 canli yayin/IBO; K4 harici restore henuz kanitlanmadi.
7. Eski DEVAM_NOTU.md eski dalda calisma der; daha yeni kullanici karari yeni Madsc55/Madsc55-Tv main'e yazma ve eski dala KESINLIKLE dokunmama. Yeni karar gecerlidir.
8. Eski kullanici karari YEDEKLER'e yeni kanal eklemeyi iptal etti; yeni sistemde otomatik ekleme yetkisi yoktur.

## Izlenecek sirali isler
- 822 blobu dosya yolu + SHA ile tarihsel 810 manifestine esle; 12 fark varsayimini kanitsiz kesinlestirme.
- 99 workflow'un her birini gorev, trigger, permissions, script, input, output, write target, risk, K1-K5 owner, parity-test ve evidence ile esle.
- 26 guvenlik kuralinin her birini negatif test + runtime kanitla.
- K2-K3-K5 aday/IBO/EPG/logo/rapor, K4 geri yukleme ve K1 write gate zincirlerini tek toplu kabulde dogrula.
- Basarili izole Actions, gercek yayin/IBO ve harici restore kanitlarini birbirinden ayir; kullanici onayi olmadan cron/production/legacy disable YOK.

Bu belge eksiklerin kaybolmamasini saglayan karsilastirma kontrol listesidir; bitmis denetim sertifikasi degildir.
