# MADSC TV - 45/45 ESKI MARKDOWN/TXT NOT KARSILASTIRMA SONUCU
Tarih: 19 Ekim 2026
Kaynak: Madsc55/madsc-tv, madsc/bes-sistem-toplu-birlestirme, ca374df3b9585c0d76a078db9536150ebbc260f7 (salt okunur).

## Kapsam
Recursive tree truncated=false: 822 blob. Markdown/TXT: 38 md + 7 txt = 45 belge. Onceki iki turda 25 merkezi belge okundu; bu tur 20 ek belge ile birlikte atlanmis 4 dokuman da okundu: .github/commands/aday-yedekleme.txt, .github/commands/genel-guncelleme.txt, CALISMAYANLAR.txt, yedekler/ADAY_KANALLAR_2026-10-09.txt. Dolayisiyla eski dalin 45/45 md/txt belgesi okunup konu ve karar bazinda karsilastirildi. Bu bir satir satir 822 blob icerik veya davranissal sertifikasyon DEGILDIR.

## Bu tur okunan 20 belge
- epg_deneme/README.md: TRT 5 kanal pilotu; cihaz gorunurlugu NOT_VERIFIED, tvg-id kimlikleri korunur.
- kontrol_notlari/2026-10-12_ekol_basa_sarma.md: Ekol TV/Sports basa sarma; kisa teknik test sureklilik kaniti degil.
- kontrol_notlari/DEVAM_GECMISI_2026-10-12_1947.md: tarihsel uc deneme ve 6 saat bekleme; eski snapshot yeni canli test degil.
- kontrol_notlari/YENI_KANAL_ARAMA_TALEPLERI.md: Eurostar alternatif arama acik, kullanici onayi olmadan ekleme yok.
- liste_kontrol/README.md: tarihsel kategori kayit ve farkli URL sayilari karistirilmaz.
- logo_deneme/HAZIRLIK_NOTLARI.md: 3/3 test ve 24h puanlama, kimlik/IBO/logo/EPG ayri.
- logo_deneme/README.md: SVG XML dogrulamasi cihazda goruntu degil, hata kalici bozukluk degil.
- madsc_kesif/NOT_EKSIK_TURK_KANALLARI.md: resmi/yasal Turk kanallari kesfi, uydu frekansi HLS degil, izin olmadan ekleme yok.
- madsc_kesif/ibo_kullanici_secimi_2026-10-13_3-5281.md: kullanici numara secimi snapshot'a bagli; eski numaralar yeni siraya uygulanmaz.
- raporlar/GELISTIRME_11_DURUM_2026-10-12.md: 11 gelistirme, tamamlanan testler tekrar edilmez, birlesik rapor eksigi.
- raporlar/IBO_TCL55C655_UYUMLULUK_DENETIMI.md: TCL 55C655 ve IBO Pro 2128.0, uygulama uyumlulugu gercek cihaz kaniti ister.
- raporlar/LOGO_DURUM_2026-10-12.md: 1029 liste kaydi/191 logo adresi tarihsel; dogru kanal/IBO gosterimi kanitlanmadi.
- raporlar/SON_DURUM_2026-10-12_1130.md: tarihsel ADA/Kanal D/SAT7 ve kullanici duzeltmeleri; son kararlar oncelikli.
- reports/ibo-user-decisions-2026-10-13-session2.md: 6115 numarali snapshot kararlari, 1-2 ve incelenmeyen 5967+ korunur.
- vod/IBO-AYRI-KURULUM.md: M3U Filmler sekmesini garanti etmez; Xtream API gercek sunucu olmadan var sayilmaz.
- vod/README.md: film/dizi TV listesinden ayri, lisansli icerik, cihaz testi bekliyor.
- yedekler/GECMIS_KANAL_KARARLARI_KORUMA_2026-10-09.md: IBO kararlari teknik testten ayri ve ustune yazilmaz.
- yedekler/IBO_YEDEK_EKSIK_KANALLAR_2026-10-09.txt: tarihsel baglantisi bulunmayan kanal adlari.
- yedekler/YENILER_KAYNAK_HATALARI_2026-10-09.txt: DNS hatasi tarihsel, bugunku ag kaniti degil.
- yedekler/YENILER_KAYNAK_HATALARI_2026-10-09_GRUP1.txt: ayni tarihsel DNS hatalari, iki farkli hata olayi sayilmaz.

## Onceki turlarda atlanmis 4 belge
- .github/commands/aday-yedekleme.txt: izole aday yedegi, CALISANLAR'a dokunma.
- .github/commands/genel-guncelleme.txt: salt okunur arama, normalize URL ve isimle duplicate onleme.
- CALISMAYANLAR.txt: kanal adlari kullanici karar kanitindan ayri; otomatik silme listesi degil.
- yedekler/ADAY_KANALLAR_2026-10-09.txt: M3U benzeri tarihsel test aday listesi; canli test veya ekleme izni degil.

## K1-K5 kapanis kontrol listesi
K1: AGENTS 26 kural; git write gate, negatif runtime testler, korunan hash, devre kesici, Turkce Actions isimleri.
K2: 156/155 kaynak tarihsel fark, yasal kaynak kesfi, duplicate URL/ad, 75 aday bekletme, tekrar deneme zamani.
K3: ffprobe/HLS surekliligi (Ekol basa sarma dahil), 3/3, 24h, logo kimligi, XMLTV tvg-id, EPG Pages, IBO cihaz kullanici onayi, kanal snapshot numaralari.
K4: 11599/42/11557 tarihsel arsiv ayrimi, izole restore, 30 gun saklama, GitHub disi kopya, secrets/cihaz yedegi; onaysiz otomatik geri yukleme yok.
K5: 99 workflow her biri icin tetik, permission, script, girdi/cikti, artifact, write side effect, K1-K5 sahip, tek dispatch ve fail-closed toplu rapor; eski workflow'lari kapatma yok.
Ek kapsam: VOD ayriligi ve Xtream ihtiyaci, EPG pilot vs production, Turkce gorunen workflow/job/step adlari.

## Sonuc
45/45 eski md/txt belge okundu ve bu raporlarla konu bazinda karsilastirildi. Onceki raporlar:
- docs/KAYNAK_NOT_KARSILASTIRMA_2026-10-19.md
- docs/KAYNAK_NOT_KARSILASTIRMA_TUR2_2026-10-19.md

HENUZ BITMEYEN: 777 md/txt disi blobun ayrintili icerik incelemesi, tarihsel 810 snapshot ile guncel 822 blobun SHA/yol delta eslemesi, 99 workflow davranissal esdegerlik, 26 runtime kural, gercek IBO ve offsite restore. Korunan eski repo ve production degistirilmedi.
