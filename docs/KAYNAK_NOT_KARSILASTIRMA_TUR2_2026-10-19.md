# KAYNAK NOT KARSILASTIRMASI - IKINCI TUR (19 EKIM 2026)

Kaynak: Eski salt okunur dal ca374df3b9585c0d76a078db9536150ebbc260f7. Recursive Git tree: 822 blob; 45 Markdown/TXT dokuman (38 md, 7 txt), 198 py, 99 yml, 51 json, 330 png, 40 svg, 27 m3u, 26 csv, 3 xml, 2 jpg, 1 webp. Ilk tur 14 temel belge; bu tur 11 ek gecis/eksik/kabul belgesi GitHub'dan okunup karsilastirildi. Toplam 25 benzersiz merkezi belge okundu. Tum 45 dokuman veya 822 dosya satir satir incelendi iddiasi YOK.

## Ikinci tur incelenen 11 belge ve somut kapanis maddesi
1. BES_SISTEM_GECIS_KONTROL.md: eskiyi kapatmadan once trigger, permission, artifact, yan etki, geri donus esdegerligi; kanal yazma izni yok.
2. BES_SISTEM_TOPLU_IS_DEFTERI.md: kategori basina tek dispatch ve ayri artifact; merkezi K1→K5 toplu kabul; eksikler kapanmadi.
3. MADSC_2026-10-13_KALAN_ISLER_DEVAM_KAYDI.md: 156 kaynak/155 hedef tarihsel fark; 740 yabanci arsiv, IBO kararlari, farkli kanal numara uzaylari.
4. MERKEZI_ARSIV_HARITASI.md: 11599 tarihsel yedekten 42 tutuldu/11557 arsive ayrildi; ana listede 2 yedek, 40 otomatik geri alinmaz.
5. SEKIZ_GOREV_TOPLU_DENETIM.md: dis yedek/30 gun saklama/secrets ve cihaz verisi eksik; eski 8 gorevin kapsami unutulmamali.
6. TOPLU_DURUM_RAPORU.md: 75 aday tekrar/kimlik, EPG Pages, offsite restore, otomatik yuk, tarihsel schedule degisiklikleri acik.
7. docs/BESLI_SISTEM_GECIS_RUNBOOK.md: tek merkezi dispatch, fail olan kategoriye ragmen diger salt okunur denetimler, genel kabul fail.
8. docs/MADSC-92-ESDEGERLIK-KARAR-MATRISI.md: 92 eski statik denetim 5/5 Actions basarisi davranissal parity degil.
9. docs/MADSC-92-WORKFLOW-ESDEGERLIK-KONTROL-2026-10-14.md: 92 workflow icin girdi/cikti/hata/hash/rollback kaniti gerekli.
10. docs/MADSC-IKI-TOPLU-KABUL-PLANI.md: iki toplu kabul, K5 needs bagimliligi, eksik davranis BLOCKED.
11. docs/MADSC-TAM-DURUM-VE-YOL-HARITASI-2026-10-14.md: 5/5 kurulum parity degil; yuzde iddiasi kanitsiz yapilmaz.

## Birinci tur ile karsilastirmada kritik kararlar
- 92 sayisi eski main/tarihsel; guncel dal 99 workflow. Yeni 99/99 YAML tetik envanteri sadece statik.
- 810 sayisi tarihsel snapshot; guncel 822 blob. 12 fark oldugu yalniz sayisal farktir, tekil delta kanitlanmadi.
- Eski 810 dosya notu.md icinde D2/D3 farki korunacak; metin kaydi canli test yerine gecmez.
- AGENTS Kural 26 Actions gorunen isimleri Turkce; 26/26 runtime test bekliyor.
- Yeni mimaride K3 EPG/logo/IBO, K4 backup; eski planlardan farkli kategori dagilimi dokumante edilmeli.
- EPG ertelenmis tarihsel karar ile yeni proje gereksinimi ayrilmali; otomatik uretim/Pages ve cihaz kaniti olmadan acilmaz.
- 75 aday, 156/155 kaynak, 740 yabanci arsiv, 11599 yedek tarihsel sayilardir; yeni veri olarak kopyalanmaz.
- Eski YEDEKLER'e aday ekleme iptali halen korunur.
- K1 26 runtime; K2-K3-K5 aday/tekrar/EPG/logo; K4 offsite restore; K5 tek rapor ve duplicate dispatch kontrolu.
- Tum eski workflow'lar ve playlistler izinsiz degistirilmeyecek, cron/production kapali.

## Kalan belge ve dosya kapsamı
45 md/txt belgenin 25'i merkezi kaynak olarak bu iki turda okundu; kalan 20 dokuman (komutlar, kanal kararlari, logo/EPG/IBO, VOD ve yedekler) tek tek okunup bu matrise baglanmali. 822 blobun 777'si md/txt disinda; kod, YAML, veri ve gorsel farkli denetim metodlari gerektirir. Bu ikinci tur, tum 822 dosyanin icerik sertifikasi DEGILDIR.

Ilk tur raporu: docs/KAYNAK_NOT_KARSILASTIRMA_2026-10-19.md.
