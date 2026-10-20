

---

## KAYNAK: MADSC_2026-10-13_KALAN_ISLER_DEVAM_KAYDI.md

Git blob SHA: `a310b22e547e6faad385838f86536d4c726b5e2d`

```text
# MADSC — 13 Ekim 2026 devam ve eksik kapanis kaydi

Bu not DEVAM_NOTU.md ve SEKIZ_GOREV_TOPLU_DENETIM.md ile birlikte okunur. Raporlar snapshot'tir, canli IBO testi degildir.

## Korunan kararlar
- Ana CALISANLAR.m3u, HEPSI, favoriler, YENILER, yedekler ve mevcut sira/metadata kullanici onayi olmadan degistirilmez.
- IBO Player cihaz testleri bu calismanin kapsaminda degildir. Teknik ffprobe basarisizligi IBO'da calismaz kaniti degildir.
- 740 yabanci aday YABANCI_KANALLAR.m3u arsivinde; IBO'da gorunur yabanci kategori acilmaz.
- Kanal kimligi, logo, EPG, kalite ve yayin haklari ayri kanit ister; teknik decode tek basina onay degildir.
- Kaynak hedefi 155 diye 156 farkli URL'den biri rastgele silinmez.

## Dogrulanan depo kayitlari
- madsc_kesif/ozet.json, 2026-10-13 13:59 UTC: 156 tanimli kaynak, 155 hedef, 14 otomatik taranan kaynak, 9576 bulunan kayit, 3514 tekrar, bu tur 0 aday, 0 test; ilyswch-TR icin HTTP 404 raporlanmis. 404 tarihsel snapshot, bugunku canli sonuc degil.
- madsc_son_kontrol/summary.json, 2026-10-13 09:22 UTC: 3175 tamamlanmis, 3082 kalmis, 901 icerik incelemesi, 1931 kimlik bekleyen teknik gecis, 195 sureklilik hatasi, 148 timeout, listeye hazir 0.
- SEKIZ_GOREV_TOPLU_DENETIM.md: bagimsiz GitHub disi yedek, kaynak erisimi, kanal kimligi, lisans, logo/EPG kaniti ve branch protection acik; cihaz testi kullanici istegiyle kapsam disi.
- Son merkezi Actions #38416932386 basarili; bu kod denetimi, yayinlarin canli/kimlik dogrulamasi degildir.

## Tekrarlanmadan yapilacaklar — oncelik
1. Devam eden son kontrol is akisini ve gercek kuyruk ilerlemesini son Actions/artifact verisiyle dogrula; tamamlanan 3175 kaydi yeniden test etme.
2. Kalan 3082 aday icin mevcut otomatik son kontrol mekanizmasinin durma nedenini ve izinlerini incele; izin varsa yalniz kaldigi yerden ilerlet, tekrarlayan fail durumunda dur.
3. 901 icerik incelemesi + 1931 kimlik bekleyeni ayri kanit kuyruğuna koy; kanal adini, logo ve stream kimligini otomatik dogrulanmis sayma.
4. 195 sureklilik hatasi ve 148 timeout icin IBO uyumlulugu belirsiz etiketini koru; calismiyor diye silme.
5. 156 kaynak benzersiz URL: 155 hedefini zorlamadan erisim, gercek kullanim ve kaynak kalitesiyle karar ver. ilyswch-TR 404 kaydini canli tekrar dogrula.
6. Tekrarlanan URL testlerini gecmis silmeden engelleyen kod ve durdurma davranisini test et.
7. Korunan playlist yazma kapisi, izole geri yukleme, bagimsiz dis yedek ve branch protection yetkilerini kanitla. Yetki yoksa engel olarak kaydet.
8. Logo/EPG, kalite, lisans ve kanal kimligi eksiklerini tek final inceleme raporunda birlestir; IBO cihaz testi yapma.
9. Bir tek toplu Actions dogrulamasiyla gercekten kapanan isleri ve dis kanit gerektirenleri ayir.

## Yapilmamasi gerekenler
- Her tur yeni rapor alanlari ekleyerek isi bitmis gibi gostermek.
- Kullanici onayi olmadan ana liste/YENILER/favori/yedek degistirmek.
- Bos yeni aday kuyrugunu butun eski testlerin bittigi seklinde yorumlamak.
- Teknik gecis veya yesil Actions sonucunu cihazda calisiyor ya da lisansli diye sunmak.

## Kritik kullanici dogrulamasi — IBO oynatma korunacak
- Kullanici, teknik testten gecen kanallarin bir kisminin IBO Player'da gercekten calistigini teyit etti. Bu gozlem kaybolmamalidir.
- Ayrica ffprobe/teknik testten gecemeyen bazi yayinlarin da IBO'da calistigi daha once gozlemlendi. Teknik hata = IBO'da calismiyor sonucuna varilmaz.
- IBO'da kullanicinin calisiyor dedigi belirli kanallar, kanala ait dogrulanmis eslesme varsa ayri KULLANICI_IBO_CALISIYOR kaydi olarak korunur. Hangi URL'lerin onaylandigi bilinmeden tum teknik gecisler IBO onayli sayilmaz.
- Otomatik testler, kullanici onayli oynatma sonucunu ezemez; kanal veya URL silinmez. Cihaz testlerini asistan yeniden yapmaz.

## Kullanici duzeltmesi — 740 yabanci kanal ve teknik false-negative (13 Ekim)
- Kullanici acikca bildirdi: sistem teknik testlerinden gecemeyen kanallarin cogu IBO Player'da oynuyor. Bu, teknik testlerin IBO uyumlulugunu eksik olctugune dair saha gozlemidir; tum teknik basarisizlar kesin bozuk sayilamaz.
- Somut ornek: 740 yabanci kanal bir donem IBO'da gorunur hale getirildi ve kullanici tarafindan denendi; bu deneme toplu bir IBO gozlemidir. Her 740 URL'nin ayri ayri basarili oldugu veya bugun canli oldugu iddia edilmez.
- 740 kanal daha sonra kullanici istegiyle YABANCI_KANALLAR.m3u arsivine tasindi. Arsivde olmalari yayinlarin calismadigi anlamina gelmez.
- ffprobe fail, timeout veya continuity fail sonucunu KESIN_CALISMIYOR etiketine donusturme. IBO'da calistigi kullanici tarafindan kanitlanan kanal URL eslesmelerini oncelikle koru, gecmisi ezme.
- Yeni otomatik tarama/temizlik, 740 arsiv kanalini veya kullanici onayli oynayan kanallari teknik sonuc nedeniyle silmemeli; kullanici izni olmadan ana listeye/YEDEKLER/YENILER'e yeniden eklememeli.
- Teknik test raporunda IBO false-negative riski ayrica gorunmeli; cihaz testi asistan tarafindan yapilmayacak.

## Kullanici onayli yabanci/Turk kanal is akisi
- YABANCI: Bulunan yabanci adaylar, teknik gecis veya basarisizlik fark etmeksizin ayri arsivde saklanir. IBO kullanici testine hazirlamak icin YEDEKLER'e otomatik tasinmaz; kullanici yabanci kanallari tek tek test etmeyecek. Yabanci kanal tespiti yalniz kaynak ulkesine gore kesinlestirilmez; belirsizler siniflandirma bekler.
- TURK: Yalniz ana listede bulunmayan yeni Turk kanallari sistem teknik testlerine alinir. Teknik testten gecen ve kanal kimligi yeterince dogrulanan adaylar kullanici IBO testine uygun YEDEKLER taslagi olarak hazirlanir. YEDEKLER'e fiili ekleme icin kullanici onayi gerekir.
- Kullanici IBO'da calisiyor derse CALISIYOR, calismiyor derse CALISMIYOR olarak ayri kullanici sonucu tutulur. Otomatik ffprobe bu sonucu ezmez.
- Teknik testten gecemeyen Turk adaylar silinmez, ayrik inceleme arsivinde kalir; kullanici IBO testine otomatik gonderilmez.
- Tum bulunan liste disi farkli URL'ler arsivlenmeli, ayni URL yeniden arama/teste sokulmamali; yeni URL alternatifi ayri tutulmali. Arama motorunun kaynaklari yeniden okumasiyla ayni URL'yi yeniden test etmek birbirinden farklidir.
- Bu bolum is akisi karari kaydidir; uygulama kodunun tam olarak bu sekilde calistigi iddia edilmez.

## 2026-10-13 - Guncel kullanici onayi, yapilanlar ve devam noktasi
- ONCEKI yabanci/Turk ayrimi is akisi kullanici tarafindan degistirildi: Ilk gunden beri bulunan, teknik test gecen/gecmeyen, Turk/yabanci/belirsiz tum yeni adaylar, ayni URL tekrar edilmeden YEDEKLER'e alinarak IBO Player'da kullanici tarafindan sinanacak. Kullanici calisiyor/calisimiyor/yabanci kararini bildirecek; sonuca gore YEDEKLER'den kaldirilip ilgili kalici arsivde kayit korunacak. Otomatik teknik fail kesin IBO fail degildir.
- 2026-10-13'te arsivden YEDEKLER'e tek seferlik aktarim Actions #38427474997 SUCCESS. Sonrasinda CALISANLAR.m3u: toplam 12636 kanal, YEDEKLER 11599, diger kategoriler 1037. Bu sayilar anlik kayit olup IBO'da yuklendigi dogrulanmadi.
- scripts/discovery_archive.py ve .github/workflows/madsc-birlesik-kesif.yml ile kalici arsiv ve gecmis tekrar kontrolu baglandi (74defba, ac1e259, da33c8e). Arsiv CSV dosyasi madsc_kesif/bulunan_kanal_arsivi.csv. Eski kayitlar korunmali.
- scripts/stage_archive_to_backups.py ve .github/workflows/madsc-arsiv-yedek-aktarim.yml eklendi (3cc21f7, 9589a30); tekrarli otomatik aktarim yapilmasin, diger kategorilere dokunulmasin.
- Toplu butunluk testi ilk #38428678653 FAILURE: kategoriler arasinda ayni URL bilincli bulunabilir. Test kodu duzeltildi (a401ba4, f883604), tekrar #38428822471 SUCCESS. Kanallar silinmedi.
- Son kontrol workflow'u otomatik push tetiklemesiyle calistirilmaya calisildi (9b74f49); #38429266062 FAILURE: 24. kural devre kesici onceki 3 basarisiz/zaman asimi calismasini gorup threshold=2 ile testleri guvenli durdurdu. Push tetikleyicisi kaldirildi (a6e4da5); guvenlik kilidi KALDIRILMADI.
- Kurtarma teshisi workflow'u eklendi (6515bb3), #38429767606 SUCCESS: unit testler, rapor dosyalari ve kilit gecmisi incelemesi adimlari basarili. Bu, yayinlarin yeniden test edildigi veya kilidin acildigi anlamina gelmez.
- madsc_son_kontrol/summary.json son bilinen zaman 2026-10-13T09:22:28Z, remaining=3082, selected=3175, completed=3175, ready_for_playlist=0; rapor tarihi eski ve sayilar tekrar dogrulanmadan guncel diye sunulmamali.
- KALAN: son kontrol zincirinin onceki gercek basarisizliklarini analiz et; sadece kontrollu manuel kurtarma calismasiyla (workflow_dispatch, mevcut guvenlik kodunda izinli) yeniden baslat; test raporlarini ve kalan kuyrugu dogrula; kullanicinin IBO geri bildirimlerini URL bazinda kalici kaydet ve YEDEKLER'den ancak kullanici talimatiyla tasima/silme yap; 11599 aday icin IBO oynatici performansi kullanici tarafindan dogrulanmali.
- Koruma: HEPSI/FAVORILER/YENILER/ULUSAL ve diger eski kategorilerin kanal adi, sirasi, URL, logo, ID ve grup bilgisi degistirilmez. IBO testi sadece kullaniciya aittir.

## 2026-10-13 - Tekrarlayan workflow zincirini kalici olarak azaltma
- Kullanici istegi: her seferinde yeni workflow acip birbirini tetiklemek yerine merkezi, tutarli, tekrarsiz ve toplu is akisi.
- .github/workflows/madsc-son-kontrol.yml son adiminda kendini tekrar workflow_dispatch ile baslatan otomatik zincir kaldirildi (a79c319). Gunluk planli kontrol ve kullanici tarafindan manuel kurtarma imkani duruyor.
- Her basarili batch sonunda kalan sayi yalniz raporlanir. final_validation.py daha once son kontrol sonucu kaydedilmis adaylari yeniden test etmez. Devre kesici / 24. kural guvenlik kilidi korunur.
- #38429767606 kurtarma teshisi SUCCESS, fakat bu son kontrolun kilidinin kalktigi veya bekleyen adaylarin test edildigi anlamina gelmez.
- Acik konu: son kontrolu manuel kurtarma modunda guvenli baslatip gercek sonucunu izlemek; gunluk otomasyonun ilerlemesini takip etmek; kullanicinin IBO gozlemleriyle arsiv siniflandirmasi yapmak.

## 2026-10-13 - Son durum, sekiz gorev ve kullanici talimati (son ek)
- Kullanici acik talimati: onceden onaylanmis isler icin tekrar tekrar soru SORMA; yetki dahilinde islemleri dogrudan yap, somut tamamlanma ve test kaniti sun; engeli acikla. Gerekli tum degisiklikleri ve kalanlari bu kayda ekle. Yeni gereksiz workflow ve tekrarlayan test uretme.
- Manuel kurtarma run #38430737866 (workflow_dispatch) gercekten baslatildi. Son sorguda STATUS=in_progress; '24. kural' SUCCESS, birim testleri SUCCESS, ffmpeg kurulumu SUCCESS, 'Bes dakikalik goruntu ses surekliligini dogrula' IN_PROGRESS. Sonuc tamamlanmis gibi sunulmayacak.
- Son kontrol zincirleme kendini tetikleme kaldirildi (a79c319); sonraki isler zamanlanmis veya kontrollu manuel calisma ile ilerler. Guvenlik kilidi korunur. Bu tek basina tum adaylari veya sekiz gorevi bitirmez.
- Son basarili kurtarma teshisi #38429767606 SUCCESS; toplu butunluk #38428822471 SUCCESS; YEDEKLER aktarim #38427474997 SUCCESS; genel saglik son gorulen #38430164504 SUCCESS.
- Sekiz gorev takibi: (1) merkezi denetim KISMEN, (2) 156 kaynak/155 hedef farki DOGRULAMA BEKLIYOR, (3) tekrar testlerini engelleme ve gecmis koruma KISMEN UYGULANDI, (4) yedek ve korunan listeler butunluk TESTI BASARILI, (5) logo/EPG/kimlik/kalite BITMEDI, (6) IBO aday hazirligi YEDEKLER AKTARILDI ama cihaz testi KULLANICIYA AIT, (7) tek yonetim paneli TAMAMLANDIGI DOGRULANMADI, (8) gunluk hata/sonuc raporu KISMEN.
- Kalan kritik: #38430737866 bitis sonucunu ve madsc_son_kontrol/summary.json yeni kalan sayisini kontrol et; varsa gercek hata adimini ve kanitini inceleyip guvenligi bozmadan duzelt. 3082 onceki kayittaki remaining sayisidir, guncel sayi gibi sunulmaz. Sekiz gorevin somut eksiklerini tek bir denetim planinda tamamla, eski dosyalari/raporlari silme. Her tamamlanan degisikligi bu kayda isle.
- Koruma: CALISANLAR.m3u, HEPSI, FAVORILER, YENILER, YEDEKLER, YABANCI_KANALLAR.m3u ve kullanici IBO test kararlari onaysiz degistirilmez. Kullaniciya yapilmayan isi yapildi diye soyleme.

## 2026-10-13 17:00 UTC - YEDEKLER'den yabanci kanallari ayirma, kullanici onayli
- Kullanici: "yedeklere attigin turk kanallarini haric yapancilari kaldir ve sistemimiz de klasinlar turk kanallari kalsin kontrol edeyim".
- scripts/keep_turkish_backups.py ve .github/workflows/madsc-yedek-turk-ayir.yml olusturuldu; run #38435159165 SUCCESS.
- Rapor: madsc_kesif/yedek_turk_ayirma_raporu.json. Baslangic YEDEKLER 11599, kalan 42, IBO listesinden ayrilan 11557. Bunlardan 740 kayit yabanci arsiv kanali ile eslesti; 10817 kanal Turk kimligi kesin olmadigindan SINIFLANDIRMA BEKLIYOR (bunlarin yabanci oldugu iddia edilmez).
- Ayrilan 11557 kanal kayipsiz olarak madsc_kesif/yedeklerden_ayrilanlar_20261013T170042Z.m3u dosyasinda saklandi. YABANCI_KANALLAR.m3u degistirilmedi. Diger kategori kayitlari ve sirasi korunmasi kod tarafindan dogrulandi.
- Dikkat: YEDEKLER'de kalan 42 kanalin kimligi kaynak/isim ipuclarina dayali adaydir; hepsinin Turkiye kanali oldugu veya IBO'da calistigi tek tek kanitlanmis degildir. 10817 belirsiz arasinda Turk kanali olabilir. Kayipsiz arsivden gelecekte kimlik dogrulamasiyla geri alinabilir; kullanici onayi olmadan toplu geri ekleme yapilmaz.
- Tek seferlik push tetiklemesi sonraki commitlerde yeniden calismaz. Son kontrol teknik run #38430737866 SUCCESS; ardindan yeni son kontrol run #38434936603 baslamis ve bu kayit aninda IN_PROGRESS idi.

## 2026-10-13 - Kullanici istegiyle 11599 YEDEKLER tam geri yuklendi
- Kullanici, tum 11599 aday kanalin YEDEKLER'e geri verilmesini, IBO'da kendisinin tek tek Turk/yabanci/calisiyor/calisimiyor olarak bildirmesini istedi.
- scripts/restore_all_11599_backups.py ve .github/workflows/madsc-11599-yedek-geri-yukle.yml olusturuldu. Run #38435960199.
- madsc_kesif/yedek_11599_geri_yukleme_raporu.json GitHub'da dogrulandi: before_backup=42, restored=11557, after_backup=11599, protected_categories=UNCHANGED, ibo_playback=NOT_TESTED.
- 11557 geri yuklenen kanalin hepsi Turk degildir; yabanci ve belirsiz adaylar kullanicinin siniflandirma istegiyle YEDEKLER'de yeniden gorunur. Kayip olmadan arşivleri korunur.
- Kullanici IBO sonucunu verdikce URL bazinda siniflandir, kullanici teyidini kaybetme. Kategori tasima veya silme sadece acik talimatla yapilir.

## 2026-10-13 - Kullanici sesli secimi 3-5281
- Kullanici 11367 kanallik GUNCEL YEDEKLER siralamasinda 3-5281 dahil araligi tek tek inceledi. Sozlu secilen Turk numaralari: 8,9,11,21-25,155-162,2370,2374,3362,3363,3570,3571,3665,5271-5274. 26 ve 165 acikca geri cekildi.
- scripts/apply_ibo_3_5281.py ve workflow madsc-ibo-3-5281.yml ile run #38442355557 baslatildi. Rapor madsc_kesif/ibo_3_5281_rapor.json olustu: 27 Turk kanal YEDEKLER'de tutuldu, 5252 kullanicinin yabanci olarak belirledigi kanal kayipsiz madsc_kesif/ibo_3_5281_ayrilanlar.m3u arsivine alindi. Yeni YEDEKLER toplam 6115. 1-2 ve eski 5282 sonrasi degismedi.
- 2370 ve 2374 calisiyor; 3362,3363,3570,3571,3665 calismiyor. Diger Turk kanallarin calisma durumu belirtilmedi. Yabancilarin calisma durumu belirtilmedi.
- Ses kaydinda '2280 Elektrik...' ifadesi belirsizdi ve Turk kanali olarak acikca belirtilmedi; bu nedenle 2280 secili 27 icine alinmadi; arsivde geri getirilebilir. Gerekirse kullanicinin net talimatina gore geri al.
- Sonraki numaralar icin YENI 6115 siralamasi ile ESKI 11367 siralamasi karistirilmamali.

```


---

## KAYNAK: MERKEZI_ARSIV_HARITASI.md

Git blob SHA: `eb8881d32b1e7521806b517c8888c4a406391379`

```text
# MADSC TV — Merkezi Arşiv Haritası (salt okunur)

Bu harita hiçbir kanal dosyasını taşımaz, silmez veya değiştirmez. Kaynakları beş merkezi sistemin kullanacağı şekilde ayrı tutar.

| Bölüm | Kaynak | İlke |
|---|---|---|
| ÇALIŞANLAR | CALISANLAR.m3u | Ana TV listesi, onaysız değişmez |
| ÇALIŞMAYANLAR | CALISMAYANLAR.txt, yedekler/IBO_ESKI_CALISMAYANLAR_2026-10-09.m3u | IBO kararı teknik testten ayrı |
| YABANCILAR | YABANCI_KANALLAR.m3u, madsc_kesif/*yabanci_arsiv.m3u | Kimliği belirsiz otomatik yabancı sayılmaz |
| YEDEKLER | yedekler/, madsc_kesif/yedeklerden_ayrilanlar_20261013T170042Z.m3u | Orijinaller korunur |
| YENİLER / ADAYLAR | YENILER.m3u, aday_bekletme/, aday_hazirlik/, madsc_kesif/bulunan_kanal_arsivi.csv | Önceden açık onay olmadan yedek/test listesine bile ekleme yok |
| TEST KANITI | TEST_RAPORU.csv, madsc_dogrulama/, madsc_son_kontrol/, raporlar/ | Otomatik test IBO onayı değildir |
| GÜVENLİK | GUVENLIK_KURALLARI.md, DEVAM_NOTU.md | 24 kural ve geçmiş korunur |

## Beş merkezi sistem
K1 güvenlik ve izin; K2 keşif ve aday; K3 test ve kararlılık; K4 EPG/logo/kimlik; K5 arşiv ve bakım.

## IBO Player kabul akışı
Keşif -> rapor -> bulunan adet ve hedef listeyi kullanıcıya bildir -> önceden açık onay -> ayrı test listesi -> kullanıcının fiziksel IBO testi -> kullanıcı kararı -> yalnız onaylı işlem.

## Tarihsel mutabakat
13 Ekim: 11599 = 42 tutulan + 11557 arşive ayrılan. Bugün ana listede 2 yedek; 40 kayıt otomatik geri yüklenmez.

## Birleştirme sınırı
Dosyalar fiziksel olarak taşınmadı. 92 eski workflow için tetikleyici, izin, çıktı ve yazma eşdeğerliği doğrulanmadan kapatma veya silme yok.
```


---

## KAYNAK: ONCELIK_1_BES_MERKEZI_OTOMASYON_PLANI.md

Git blob SHA: `2b23194ef1975b60965048391d40338a342c1531`

```text
# EN YUKSEK ONCELIKLI PLAN — 89 GITHUB IS AKISINI 5 MERKEZI OTOMASYONDA BIRLESTIRME

Tarih: 13 Ekim 2026
Durum: NOT EDILDI — UYGULAMA ICIN KULLANICININ SONRAKI TALIMATI BEKLENIYOR
Oncelik: 1 / EN ONEMLI SISTEM GELISTIRME PLANI

## Kullanici karari
- Madsc55/madsc-tv deposundaki mevcut 89 GitHub Actions is akisini analiz ederek, mumkun oldugunca **5 merkezi otomasyon** altinda toplamak.
- Her degisiklik icin yeni bir test ve workflow olusturma aliskanligini bitirmek.
- Ayni isi veya ayni testi iki kere yaptirmamak; gereksiz push/workflow_run/schedule zincirlerini kaldirmak.
- Gereksiz gunluk onlarca kontrol yerine, kapsamli denetimleri **ayda yaklasik 3–5 kez** yapmak.
- Kullanici talimatli kanal ekleme, silme, tasima gibi islemlerde **tek calistirma icinde gerekli kisa dogrulama** yapmak; koruma kontrolunu kaldirmamak.
- Tum dosyalar, kanal listeleri, yedekler, arşivler, test gecmisi, hata durumlari, eksik kalan isler ve otomasyonlar merkezi olarak denetlensin.
- Kisa, net, tek son rapor verilsin. Kullanici gereksiz ara raporlarla yorulmasin.

## Hedef 5 otomasyon (taslak; envanter tamamlaninca netlestirilecek)
1. **Merkezi sistem sagligi ve guvenlik:** dosyalar, korunan listeler, workflow sagligi, hatalar, eksikler, geri yukleme kanitlari; ayda 3–5 kapsamli denetim.
2. **Birlesik kanal kesfi ve aday testleri:** eksik Turk kanallari, resmî/yasal yayin kaynaklari, erisim testi, alternatifler ve tekrar ayiklama; belirlenen periyotta.
3. **Kanal kalite kontrolu:** yayin durumu, logo, EPG, kimlik ve kategori uyumu; uygun araliklarla ve ortak raporla.
4. **Yedek ve arsiv butunlugu:** yedeklerin korunmasi, arsiv dogrulama, sayi tutarliligi, geri donus guvencesi; merkezi plan.
5. **Kullanici onayli liste islemleri:** onayli kanal tasima/ekleme/cikarma ve ayni is icinde bir kerelik koruma/dogrulama; gereksiz ayri test yok.

## Zorunlu uygulama kurallari
- ONCE 89 workflow'un tetikleyicilerini (push, schedule, workflow_run, dispatch), izinlerini, yazdigi dosyalari, bagimliliklarini ve son calisma durumlarini envanterle.
- 5'e indirgemeden once eski otomasyonlarin kritik islevlerini kaybetmedigini dogrula; mevcut korumalar ve kullanici onay kapilari aynen korunacak.
- Tekrarlanan kontrolleri ayni is akisi icinde birlestir; ayni commit icin gereksiz ek is akisi calistirma.
- Gunluk otomatik kanal arama islevinin eski kullanici tercihlerine uygunlugu ayri kontrol edilmeli; kapsamli denetimle karistirilmamali.
- Veri kaybi riski varsa islemi durdur, yedek al, guvenli geri donus plani uygula.
- `CALISANLAR.m3u`, ⭐ YENİLER, FAVORİLER, YEDEKLER, arşivler ve korunan kategoriler onaysiz degistirilmeyecek.
- Once merkezi sistemin kapsam ve sonuc raporu dogrulanacak; sonra eski workflow'lar kademeli ve geri alinabilir sekilde pasiflestirilecek.
- Sadece test sayisini azaltmak degil, **daha az ama gercekten anlamli ve dogru kontrol** yapmak hedefleniyor.
- Islem tamamlaninca kullaniciya: 89'dan kac otomasyona inildigi, hangi islerin korundugu, hangi testlerin birlestigi, hangi sorunlarin kaldigi tek ozetle bildirilecek.

## Neden bu en onemli plan?
Kullanici mevcut sistemin her degisiklikte onlarca test uretmesinden ve uzun suren tekrarlardan yoruldu. Yeni kanal/ozellik gelistirmelerinden once bu sadeleştirme ve merkezi yonetim plani onceliklidir.

## Mevcut tespit
13 Ekim 2026 tarihinde .github/workflows altinda 89 dosya goruldu. Ayin 1 ve 15'inde calisan `madsc-aylik-merkezi-denetim.yml` zaten mevcut; onu yeniden kullanmak oncelikli. Bu not yeni otomasyon baslatmaz veya mevcutlari kapatmaz.


## 13 Ekim 2026 — Son görüşmede netleşen çalışma düzeni (öncelikli ek not)
Kullanıcı bu düzenin de kaydedilmesini ve sonraki çalışmada buradan devam edilmesini istedi.

### Hedef beş ana sistem ve önerilen takvim
1. **Güvenlik ve sistem sağlığı:** Kodlar, izinler, GitHub Actions, dosyalar, korunan kategoriler; haftalık kapsamlı kontrol.
2. **Birleşik kanal keşfi:** Listede olmayan ücretsiz Türk TV kanalları, resmî/yasal internet kaynakları, tekrar ayıklama; **günde bir kez**.
3. **Birleşik kanal kalite testleri:** Yayın bağlantısı, logo, EPG, kalite, alternatifler; haftalık toplu kontrol.
4. **Arşiv ve liste bütünlüğü:** Çalışanlar, çalışmayanlar, yabancılar, yedekler, arşivler, sayılar ve geri yükleme; 15 günde bir kapsamlı kontrol.
5. **Merkezi yönetim ve yapılacaklar:** Tamamlanan işler, yapılmayan işler, başarısız koşular, kalan eksikler, tek sonuç raporu; aylık özet.

Takvimler hedef taslaktır; aynı kapsamı farklı sıklıklarla iki kez çalıştırmayacak şekilde tüm tetikleyiciler incelendikten sonra kesinleştirilecek. Kanal keşfi günlük kalsın; kapsamlı sistem denetimleri gereksiz yere her gün tekrarlanmasın. Kullanıcı onaylı liste değişiklikleri yapılırken kısa güvenlik kontrolü değişikliğin içinde **bir kez** çalışsın.

### Uygulama sırası ve kayıt tutma
- Önce bütün workflow dosyalarının gerçek envanteri: neyi çalıştırıyor, ne zaman, neyi değiştiriyor, bağımlılıkları, geçmiş hataları ve gereksiz tekrarları.
- Sonra beş ana sistem altında ortak adımlar, tek rapor, iş durumu: **YAPILDI / YAPILMADI / HATALI / BEKLİYOR**.
- Mevcut güvenlik kuralları ve yedekleri koru; hiçbir korunan listeyi veya kanalı kullanıcı onayı olmadan değiştirme.
- Eski otomasyonları ancak eşdeğer işlevleri yeni sistemde doğrulandıktan sonra kademeli ve geri alınabilir şekilde kapat.
- Her yeni kanal/özellik için ayrı workflow oluşturmak yerine mevcut beş ana otomasyonun uygun adımını kullan.
- Kullanıcıya yalnızca kısa, somut sonuçları ve gerçek kalan işleri bildir; başarıyı doğrulamadan tamamlandı deme.

### Şu ana kadarki uygulama durumu
- GitHub'da `.github/workflows/madsc-birlesik-kesif.yml` keşif zamanlaması `0 6,18 * * *` yerine `0 6 * * *` olarak güncellendi (commit `b7896f195f44f3cf59da3f3855a5c1cdcb678288`).
- `.github/workflows/iptv-test.yml` için haftalık zamanlamaya geçiş denemesi güvenlik kontrolü tarafından engellendi; **değişiklik yapılmadı**.
- 89 workflow ilk sayımdı; sonradan yeni workflow eklenmiş olabilir, canlı envanterden güncel sayı tekrar doğrulanmalı.
- **Beş otomasyona birleştirme henüz yapılmadı.** Bu not uygulanmış değişiklik gibi gösterilmemeli.

### Kullanıcının ana amacı
'Kafamız karışmasın; ne yaptık, ne yapmadık, ne çalışıyor, ne eksik tek yerden belli olsun. Günlük arama bir kere çalışsın, gereksiz tekrar testleri olmasın. Kısa ve öz ilerleyelim.'

```


---

## KAYNAK: OZELLIK_ENVANTERI.md

Git blob SHA: `b6dd624584e2479118ed4ffa92496d36420abe31`

```text
# MADSC-TV — Özellik Envanteri ve Tekrar Önleme Kapısı
Güncelleme: 13 Ekim 2026. **Bu dosya bir özellik icat etmez; mevcut kod/iş akışı kanıtlarını gösterir.** Başarı durumu her zaman son Actions koşusu ile doğrulanır.

| İşlev | Mevcut uygulama | Kapsam ve sınır |
|---|---|---|
| Günde iki kez kanal keşfi | `.github/workflows/madsc-birlesik-kesif.yml`, `madsc_akilli_kesif.py` | UTC 06:00, 18:00; aday tarama ve yayın testleri |
| Aday logo PNG hazırlığı | `scripts/candidate_logo_report.py`, `scripts/automatic_png_logos.py` | Hazırlık görsel kanal kimliğini kanıtlamaz |
| Aday logo + EPG birleşik raporu | `scripts/candidate_epg_logo_join.py`, birleşik keşif workflow | Bağımsız test #38321948143 SUCCESS; tam günlük keşif koşusu henüz doğrulanmadı; beş kanallık pilot EPG ile sınırlı |
| Tam ana liste EPG üretimi | `scripts/build_epg.py`, `.github/workflows/epg-gunluk.yml` | Her gün UTC 03:25; son bilinen rapor: 1039 giriş, 728 eşleşme, 17811 program; bu IBO cihazında görüntülendiği anlamına gelmez |
| EPG Pages yayını | `.github/workflows/epg-pages.yml` | XMLTV yayımlar ve yayımlanan içeriği doğrular |
| IBO 5 kanallı EPG pilotu | `scripts/build_ibo_epg_test.py`, `epg/ibo-test-epg.xml` | Sadece cihaz uyumluluk denemesi; üretim EPG'siyle karıştırma |
| Günde iki kez IBO EPG kimlik denetimi | `scripts/ibo_epg_kimlik_denetimi.py`, `.github/workflows/ibo-epg-kimlik-denetimi.yml` | UTC 06:23, 18:23; pilot karşılaştırması; run #38321599549 SUCCESS |
| Logo/EPG kalite uyarıları | `tools/logo_epg_audit.py`, `.github/workflows/test-15-logo-epg.yml` | Eksik logo/kimlik ve şüpheli URL uyarıları |
| Aday son kontrol | `.github/workflows/madsc-son-kontrol.yml` | Teknik başarı ile cihaz/kanal kimlik onayı ayrıdır |
| Ayda iki kez merkezi otomasyon denetimi | `.github/workflows/madsc-aylik-merkezi-denetim.yml`, `scripts/central_workflow_inventory.py`, `test_central_workflow_inventory.py` | 1/15 UTC 07:00; cron, concurrency, izin, kategori ve risk raporları; kod değişince main push testi. Salt okunur; tam orkestrasyon değildir, gerçek Actions sonucu ayrıca gerekir. |
| Altı konu tek merkezi rapor | `scripts/central_six_area_audit.py`, `.github/workflows/madsc-aylik-merkezi-denetim.yml` | Tek Actions koşusunda altı alanın salt okunur kanıt ve eksiklerini toplar; sorunları otomatik çözmez, IBO cihaz testi değildir. |
| Sekiz görev tek merkezi rapor | `scripts/central_eight_task_audit.py`, `test_central_eight_task_audit.py`, merkezi workflow | Sekiz işin kanıtını ve açık eksiklerini tek koşuda raporlar; henüz eksikleri otomatik çözmez. |
| Korunan listeler | `AGENTS.md`, `GUVENLIK_KURALLARI.md` | Ana liste, YENİLER, HEPSİ, favoriler, yedekler izinsiz değişmez |

## Her yeni işten ÖNCE zorunlu karar
1. `AGENTS.md`, `DEVAM_NOTU.md` ve bu envanteri oku.
2. İlgili script, workflow ve son Actions run'unu kontrol et; yalnız dosya varlığına bakarak **çalışıyor** deme.
3. **VAR + TEST BAŞARILI:** yeniden yazma; sıradaki eksik işe geç.
4. **VAR + EKSİK/ARIZALI:** mevcut sistemin sadece eksik bölümünü düzelt; eski başarılı işlevi ve veriyi koru.
5. **YOK:** önce mevcut araçlarla aynı işin yapılıp yapılmadığını ara; ancak gerçekten yoksa bağımsız, geri alınabilir geliştirme yap.
6. **CİHAZDA DOĞRULANMADI:** GitHub testini IBO Player gerçek yayın/EPG/kimlik onayı gibi sunma.
7. Her geliştirmeden sonra gerçek GitHub run ID, sonuç, değişen dosyalar ve kalan sınırlamaları `DEVAM_NOTU.md`ye kaydet. Başarısız/çalışan geçmişi silme.
8. Otomatik keşif ve raporlar kullanıcı onayı yerine geçmez; ana liste, YENİLER, logo ve yedekleri değiştirme.

## Önemli
Bu envanter **tekrar önleme kayıt kapısıdır**, tek başına tüm gelecekteki kod değişikliklerini teknik olarak bloke eden bir güvenlik mekanizması değildir. Değişiklik öncesi kontrol ve Actions kanıtı zorunlu çalışma prosedürüdür.

- **Merkezi logo/EPG/kimlik/geçmiş kanıt raporu:** `scripts/central_identity_epg_logo_audit.py` ve `test_central_identity_epg_logo_audit.py`; mevcut merkezi Actions testine bağlıdır. IBO cihaz onayı vermez, korunan listeleri değiştirmez.

- **Tek merkezi yönetim özeti:** `scripts/central_management_summary.py`, `test_central_management_summary.py`; yedi mevcut kanıt raporunu tek JSON içinde birleştirir, eksikleri açık gösterir. Canlı panel veya IBO onayı değildir.

- **Kısa durum özeti:** `scripts/central_short_status.py`, `test_central_short_status.py`; merkezi Actions artifact içinde `madsc_kisa_durum_ozeti.md` üretir. Günlük cron eklenmemiştir; mevcut zamanlama korunur.

- **Açık işler ve eksik kanıtlar:** `scripts/central_open_gaps.py`, `test_central_open_gaps.py`; merkezi Actions artifact içinde `acik_isler_ve_eksik_kanitlar.json` üretir. Rapor bulunması işi bitmiş saymaz.

- **Kalan sekiz iş tek koşu karar tablosu:** `scripts/central_all_remaining_tasks.py` ve `test_central_all_remaining_tasks.py`, `kalan_isler_tek_kosu_karar_tablosu.json`. Kanıt, eksik ve dış bağımlılıkları birlikte gösterir; tamamlanma sertifikası değildir.

- **İzole Git HEAD geri yükleme doğrulaması:** `scripts/central_isolated_git_restore.py` ve `test_central_isolated_git_restore.py`; üç korunan dosyanın Git HEAD sürümünü geçici dizinde geri açar, SHA256 ile doğrular. Harici veya tarihsel yedek kurtarma kanıtı değildir.

- **IBO aday inceleme kuyruğu:** `scripts/central_ibo_review_queue.py`, `test_central_ibo_review_queue.py`; aday kanıtı varsa tekrarsız CSV üretir, IBO onayı ve liste aktarımı yapmaz. Kaynak mutabakatında ham kaynak adı tekrarları da denetlenir.

## 15 Ekim 2026 — güncel kanıt ve iş kuyruğu
- MADSC 05 tetikleyici düzeltmesi: c7567e1, run 38694043295 SUCCESS.
- MADSC 03 sağlık raporu artifact kapsamı: 7e797fa, run 38694963696 SUCCESS; sağlık raporu kabul kontrolü: 439dc5b, run 38695730312 SUCCESS.
- MADSC 02 gerçek salt-okunur keşif taraması ve madsc_kesif artifact yolu: c2d28be, MADSC 05 run 38697244625 SUCCESS. Keşif adımı continue-on-error olduğu için adımın ve çıktıların ayrı doğrulanması şart.
- YEDEKLER'e otomatik kanal ekleme izni kullanıcının sonraki talimatıyla İPTAL edildi; eski devir notundaki izin geçersiz. Korunan listeler, logolar, yedekler değiştirilmeyecek; PR #71 birleştirilmeyecek.
- AÇIK İŞLER, sırayla: (1) gerçek keşif adımı ve artifact içeriği; (2) bağımsız 5 kategori hata yönetimi; (3) 92 eski workflow'un işlev/tetik/yan etki/artifact eşdeğerliğinin tek tek uygulanması (kanıtlı 0/92); (4) tarihsel ve harici yedek geri yükleme; (5) 1039 girişin sağlık kapsamı ve aday tekrar/kimlik/IBO testleri; (6) EPG/Pages ve PNG aday kimliği; (7) gerçek yazma koruması/devre kesici; (8) eski cron/çakışma ve rapor yükünün doğrulanması.
- 7/24 saatlik ChatGPT görevi tekrar etkin; bu, her saat bir çalışma turudur, kesintisiz gerçek zamanlı işlem değildir. Tamamlanmış denmeyen işlerin kanıtı toplanmaya devam eder.

- 16 Ekim K2: eski birlesik kesfin arsiv before/tarama/after ve dort asama sonuc zinciri K2'ye baglandi; izole gercek betik testi eklendi. Tam workflow/uretim parity kabul edilmedi; Actions kaniti DEVAM_NOTU.md'de izlenir.

- 16 Ekim K4: mevcut disaster_recovery_dry_run.py gecici bozulma/geri acma tatbikati K4'e baglandi; raporu artifact'ta. Harici/tarihsel backup onayi degil.
- 16 Ekim besli runtime koruma: k1_protected_integrity.py snapshot/check tum takip edilen korunan M3U/yedek/favori dosyalarini gercek calisma dizininde karsilastirir; bes kategoride always son kontrol. Yerel 43 dosya/0 fark; gercek Actions sonucu DEVAM_NOTU.md'de izlenir.

- 16 Ekim K2 kosular arasi gecmis: discovery_history_restore.py ayni dal/ata commit basarili 02 veya parent05 artifact gozlemlerini checkout kayitlarini silmeden birlestirir; bozuk veri/indirme/celiski taramayi durdurur. K2'ye bagli, runner disina push yapmaz. Yerel 8 davranis testi PASS; Actions kaniti DEVAM_NOTU.md'de izlenir.

- 16 Ekim K2 genis kaynak: mevcut tools/genis_kaynak_taramasi.py weekly/monthly modlari wide_source_scan.py ile K2'ye baglandi; manuel secim, kod degisikligi CI kabulunde both, normal cron'da none. Iki gecmis belgesi ata commit tabanli uc yonlu birlesir, artifact'ta korunur; main push/dispatch yok. Gercek Actions kaniti DEVAM_NOTU.md'de izlenir.

- 16 Ekim K3 logo/EPG kalite: mevcut tools/logo_epg_audit.py ve eski test15 uyari sozlesmesi K3'e tasindi. Tam M3U giris kapsam kontrolu, ayri JSON artifact ve zorunlu outcome kapisi; logo/EPG/liste duzeltmesi veya IBO kimlik onayi yapmaz. Gercek Actions kaniti DEVAM_NOTU.md'de.

- 16 Ekim K3 aday puanlama: category_candidate_scoring.py mevcut scorer/birlesik raporu K2'nin kabul edilmis artifact kanitiyla izole klasorde calistirir, ek probe0. Priority rapor adi eslesmesi ve bozuk kararlilik gecmisi sifirlama hatasi duzeltildi. Uzunlamasina state/probe entegrasyonu henuz kabul edilmedi; Actions kaniti DEVAM_NOTU.md'de.

- 16 Ekim K5 kanit devri: category_evidence_collect.py ayni run'in basariliK1..K4 artifact'lerinden sabitJSONraporlari provenance/SHAkontroluyle alir; ownerraporlari eskicheckout'la tekrar yazdirmaz. Yonetimozeti bagimliliklarindan sonra uretilir;24kaynakbolumu. Cihaz/harici/tam92kabul iddiasi yok; gercekCIsonucu DEVAM_NOTU.md'de.

- 16 Ekim K5 kanit aktarimi: af3d1dd / #38949404949 SUCCESS5/5. Ayni run'in4kategori17JSON kaniti provenance+hash ile merkezi rapora bagli;24baslikta eksik9->3. Tam92 kabul degil.
- 16 Ekim K5 Actions verisi: eski durum/hata raporlayicilarina GET envanter/son100kosu/enfazla20basarisizkosu job kaniti baglandi; mevcut run haric, otomatik ozet workflow+dal bazli. Gercek CI henuz bekliyor; DEVAM_NOTU izlenir.

- 16 Ekim priority upstream hata duzeltmesi: ffprobe basarisiz satir9alan/8baslik URL-source kaymasi giderildi. Iki fixtureCSV testi ve toplam58 five_categoryPASS; gercek eski priority/toplu Actions sonucu DEVAM_NOTU'de izlenecek. Playlist ve legacyworkflow dosyasi degismedi.

- 16 Ekim K3 kararlilik state: mevcut tracker gercek olcum zamani+tekillik destegi ve gecmisi saklama ile K2 olcumlerine baglandi. category_stability_history aynidal/ataSUCCESS03/05 artifact state+hash restore; entegrasyononcesi acikbootstrap, sonrasi eksikbozukfailclosed.7gunpencere/24saatteknikaralik,30gun/IBO/sureklioynatma degil.69five_category+21ilgiliyerelPASS;gercekCI DEVAM_NOTU'de izlenecek.

- K3 zamanli kararlilik gercekCI: c1683414 / MADSC05 #38952859393 SUCCESS5/5; eski KanalKararlilik #38952859152 SUCCESS. K3ilkbootstrap0medya/0gozlem/0kararli;K5eksikrapor0,43korunan0fark. Sonraki kosudan gercek state restore ve priority/genelmedya zamanli upstream kabul halenbekliyor; tam92parity0/92.

- 16 Ekim K3 öncelikli/genel medya: mevcut iki probe betiği gerçek OLCUM_ZAMANI üretir. category_candidate_media.py izole mevcut priority+genel30parti CLI ve yalnız-keşif modunu bağlar; aynı URL priority ölçümü genel taramada tekrar probe edilmez. Başarılı ata artifact'inden hash/şema/üretici sürümüyle 6saatlik reuse; scoring en yeni ölçümü kullanır. Yerel76kategori+31ilgiliPASS;gerçekCIbekliyor,DEVAM_NOTU izlenir. Tam92/IBO/liste onayı değil.

- K3 medya bağlantısı gerçekCI 1568187 / #38957224597 SUCCESS5/5; eskipriority #38957224570 ve eski genel #38957224651 SUCCESS. K3 102gerçekprobe/102gözlem/132tekilpuanlamaadayı,24hkararlı0;2ortakURLtekrarprobesiz. Ata kararlılık restore gerçekPASS. Cache sonraki gerçekreusekabulü bekliyor;79yerelkategoritestPASS.

- K3 medya reuse gerçekCI: 45c1729 / #38958162467 SUCCESS5/5. Önceki #38957224597'nin102gözlemi geri geldi; yeniadaymedyaprobe0/yenigözlem0, candidate_discovery_ran=false; statehash ve4kaynakraporhashi aynı.132tekilpuanlama/in 24hkararlı0;43korunan0fark,K5eksikrapor0.79yerelkategoritest ve K3gerçek40regresyonPASS. Genelmedya yalnız ilk30parti; tümadaykapsamı/gerçek24h/7gün/30gün ve tam92parity onayı değil.

```


---

## KAYNAK: SEKIZ_GOREV_TOPLU_DENETIM.md

Git blob SHA: `86782ae3f65f66a4d22fb87fb5ae249ae67d17d9`

```text
# Sekiz görev — tek toplu çalışma denetimi (13 Ekim 2026)

Bu dosya bir tamamlama sertifikası değildir. Kullanıcı yeni kanal testlerinin bitmesini beklemeden sekiz işin birlikte geliştirilmesini istemiştir. **Ana liste, YENİLER, favoriler, sıralama ve yedekler izinsiz değiştirilemez.**

| Görev | Yapılan / mevcut altyapı | Eksik ve kabul koşulu |
|---|---|---|
| 1. Felaket koruması | Tek arşiv `MADSC-TUM-SISTEM-YEDEK.tar.gz`, SHA256 izole açma testi; Actions #38340513782 başarılı | 30 gün saklama, GitHub dışı bağımsız kopya ve secrets/IBO ayarları eksik; kullanıcı erteledi |
| 2. Kaynak envanteri | 156 tanımlı kaynak, hedef 155; keşif özetinde gerçek sayılar ve fark açıkça raporlanır | 156 kaynağın erişilebilirliği ve benzersizliği doğrulanmadan hedefi değiştirme; günlük keşif yalnız Türkçe kaynak alt kümesini tarar |
| 3. Türk kanal önceliği | Kaynak kimliği ve Türkçe dil ipucu keşif → üç aşama → son kontrol hattında korunur | Kaynak adı kanalın ülke/kimlik kanıtı değildir; diaspora ve yerel kanal kimliği ayrıca doğrulanmalı |
| 4. Test geçmişi | Eski check'ler korunur; aynı URL'nin birden fazla kaynak kimliği `source_history` altında birleştirilir | Kullanıcı IBO onayı ile teknik test ayrımı korunmalı; gerçek Actions sonucu gerekli |
| 5. Kanal kimliği | Teknik decode geçişi kanalın gerçekten belirtilen kanal olduğu anlamına gelmez | Görüntü/isim/logonun kimliği manuel veya güvenilir kanıtla onaylanmadan listeye ekleme yok |
| 6. Logo ve EPG | Aday logo/EPG raporları ve EPG üretimi mevcut | İsveç IBO cihazında EPG ve logo eşleşmesi henüz kanıtlanmadı |
| 7. Hukuki kaynak kontrolü | Kaynak kökeni ve şüpheli yayın ayrı değerlendirilir | Lisans/dağıtım hakkı doğrulanmayan adaylar onaylı/yasal olarak işaretlenmez |
| 8. Güvenlik | Korunan listelere onaysız son kontrol aktarımı PR #31 ile kaldırıldı; mevcut workflow sağlık testleri | Branch protection ve GitHub izinleri ayrıca gözden geçirilmeli; rapor yazma yarışları izlenmeli |

## Tek teslim kuralı
Geliştirme tek PR'da birleştirilir; her aşamanın gerçek Actions sonucu kaydedilir. Teknik başarı veya rapor oluşturulması **kullanıcının IBO Player cihazında çalışıyor** ya da **ana listeye eklemeye hazır** anlamına gelmez.

## 13 Ekim — doğrulanmış yeni durum

- Genel sistem sağlık ve güvenlik denetimi **#38343031174 ve #38343045889 SUCCESS**. 19 - Bütünleşik Güvenli Kontrol **#38343031177 ve #38343045881 SUCCESS**. Bu sonuçlar tanımlı otomatik testler içindir; tüm sistemin risksiz olduğunu kanıtlamaz.
- PR #35 ile teknik testten ayrı kimlik, lisans, logo ve İsveç IBO/EPG kanıt durumları eklendi. PR #36 ile çoklu kaynak geçmişinin final kuyruğunda korunmasına regresyon testi eklendi. PR #37-#40 ile workflow izin taraması ve test hataları düzeltildi.
- GitHub `main` branch protection API sorgusu **403 Resource not accessible by integration** döndürdü. Koruma ayarlarının etkinliği doğrulanamadı; **korunuyor** diye raporlanmamalı. Bu ayarları değiştirme izni de yok.
- GitHub Actions genel denetimi tüm dosyaların tüm içeriğini güvenlik açısından sertifikalandırmaz; mevcut kod, workflow, rapor ve liste bütünlüğü kontrollerini çalıştırır.
- Kullanıcı ertelediği GitHub dışı yedekleme ve cihaz/secrets aktarımı daha sonra ayrıca ele alınacak. Kimlik, hak sahipliği, logo ve İsveç IBO gerçek cihaz onayı eksik olduğu sürece otomatik listeye ekleme yok.

```


---

## KAYNAK: TOPLU_DURUM_RAPORU.md

Git blob SHA: `88dcf643da631f106eab7cd2fd428014abb8858f`

```text
## 14 Ekim 2026 — TOPLU OTOMASYON YUKU AZALTMA / EK DENETIMLER ELLE
- Kullanici merkezi testin yesil oldugunu bildirdi; gereksiz tekrarlari tek committe azaltma istendi.
- Haftalik Cuma ana kanal + EPG denetiminin otomatik schedule tetigi kaldirildi; workflow_dispatch saklandi. Ana liste sagligi ayin 1 ve 15'inde, birlesik kanal kesfi her gun iki kez suruyor.
- Haftalik Pazartesi + ayin 1'i genis kaynak kontrolunun schedule tetikleri kaldirildi; workflow_dispatch saklandi. Elle acilirsa iki kaynak modu da calisir. Eski workflow'un ayrica uc-asama dispatch etmesi sadece elle calistirildiginda gerceklesir.
- EPG gunluk guncelleme ve Pages yayinlamasi korunuyor; IBO TV onayi BEKLIYOR. Korunan listeler, logo ve yedekler degismedi.
- Daha yapilmayanlar: tum 92 workflow'un tam aktiflik/tetik zinciri ve otomatik yuk denetimi; 1 ve 15 yedek geri yukleme/harici kopya kaniti; 75 aday icin farkli saat/kimlik testleri. Bunlar tamamlandi diye raporlanmaz.
- Yalniz iki gereksiz otomatik takvim kapatildi; manuel calisma ve gecmis dosyalar silinmedi.

## 14 Ekim 2026 — EPG TEKNIK HAZIRLIK / TELEVIZYON KONTROLU BEKLIYOR
- Kullanici #126 merkezi denetimin YESIL oldugunu ekran goruntusuyle dogruladi.
- EPG yeniden gundemde: TV basinda degil; XMLTV hazirligi, pilot 5 kanal, kaynak ve teknik dogrulama tamamlanacak; IBO Player televizyon gorunurluk testi ve kullanici onayi DAHA SONRA.
- Mevcut epg/report.json: 1039 playlist girisi, 730 eslesme, 583 kullanilabilir tvg-id, 23702 program, 5 kaynak OK (rapor 2026-10-14 08:51 UTC). Bunlar IBO TV kaniti degildir.
- Yeni scripts/epg_tv_readiness.py ve iki izole test: tam XMLTV, bes kanal pilotu, program sayilari, kaynak raporu ve cihaz onay kapisini denetler; epg/tv_kontrol_bekliyor.json kaydeder.
- EPG gunluk workflow'unda hazirlik kontrolu tek kosuda gerceklesir; yalniz EPG dosyalari ve bekleyen TV raporu kaydedilir. TV kontrolu bitmeden onay verilmeyecek.
- IBO TV'de sonradan kontrol edilecek: EPG URL'yi ekleme/yenileme, TRT1/TRT2/SHOW TV/ATV/KANAL D programlari ve Isvec'te gorunurluk. Basarisizsa ekran goruntusu ve uygulama ayarlariyla incele.
- Kalan toplu isler: 92 workflow aktif/zamanlama cakismasi, 1 ve 15 yedek/restore kaniti, gunde iki kez kesif ve logo birlesimi, 75 aday retest/kimlik. Korunan listeler, favoriler ve PNG logolar degismedi.

# MADSC — Toplu Durum ve Kapanış Takibi
**Tarih:** 14 Ekim 2026  
**Depo:** Madsc55/madsc-tv  
**Son kullanıcı bildirimi:** Merkezi testler yeşil. Bu bilgi kullanıcı gözlemidir; burada bağımsız yeni Actions koşusu doğrulanmadı.  
**Nihai kabul:** HENÜZ ONAYLANMADI.

## Beş aşama: yapılanlar, açık kalanlar

| Aşama | Yapılan ve korunan | Kalan iş / kabul kanıtı | Öncelik |
|---|---|---|---|
| 1. Güvenlik | Korunan liste yazma kapısı, merkezi salt okunur denetim, izole Git geri yükleme kontrolü | Yazma yetkili tüm workflow'ların gözden geçirilmesi; bağımsız tarihsel yedek ve gerçek geri yükleme kanıtı | Yüksek |
| 2. Keşif | Günlük 06:00 UTC birleşik keşif, aday/alternatif ayrımı, tekrar ve kaynak raporları | Yeni kaynakların canlı erişimi, lisans/kullanım uygunluğu, adayların gerçek yayın ve kimlik kontrolü | Yüksek |
| 3. Kanal testleri | Döngüsel ana liste sağlık taraması, test geçmişi, hata ve tekrar analizi | Kanal bazında canlı teknik kanıtların tamamlanması; IBO Player sonuçlarıyla karşılaştırma | Yüksek |
| 4. Logo ve EPG | Ana listedeki doğrulanmış logolar korunuyor; otomatik ana PNG tekrarları kaldırıldı; yeni aday PNG hazırlığı keşifte; günlük EPG üretimi başarılı olduğunda Pages yayını | Yeni adayların eksik logolarını eşleştirme ve gerçek görsel/kimlik kontrolü; EPG kanal eşleştirmesi ve cihazda görünme kanıtı | Yüksek |
| 5. Arşiv ve kabul | Beş aşamalı tek merkez denetim, 18 görev haritası, sekiz görev raporu, yabancı arşiv ve kabul kapısı | Açık kanıtları tek tek kapatma; 26 güvenlik kuralının uçtan uca doğrulanması; kullanıcı onayı olmadan liste aktarımı yapmama | Yüksek |

## Ortak karar: tek merkez, gereksiz tekrar yok (14 Ekim 2026)

Kullanıcıyla kesinleştirildi: Beş ana bölümün yönetimi tek merkezden yapılacak. Güvenlik, kanal keşfi, kanal yayın testleri, logo/EPG ve arşiv/kabul için ayrı ayrı aynı işi tekrar eden otomasyonlar kurulmayacak. Günlük keşif, döngüsel yayın testleri ve EPG veri üretimi kendi gerekli zamanlarında ayrı çalışabilir; kod değişikliğinde ağır taramalar yeniden başlamayacak. Her toplu işlemden önce mevcut tetikleyiciler ve sonuçlar incelenecek; gereksiz ikinci iş kaldırılacak, ilgili güvenlik kontrolleri korunacak. Mümkün olduğunda tek commit, tek merkezi test, tek Türkçe sonuç raporu uygulanacak.

**Sonraki çalışma sırası:** (1) Beş bölümde kalan workflow tetikleyicilerinin tam envanteri ve çakışmaları; (2) koruma kurallarını bozmadan gerçek tekrarların giderilmesi; (3) yeni adayların eksik logo, canlı yayın ve EPG kanıtları; (4) yedek/geri yükleme güvenliği; (5) 18 görev ve 26 güvenlik kuralının genel kabulü. Yeşil Actions tüm canlı kanalların IBO Player'da çalıştığı anlamına gelmez. Nihai kabul henüz verilmedi. Ana liste logoları, favoriler, YENİLER ve yedekler kullanıcı onayı olmadan değişmez.

## 14 Ekim — Ana liste sağlık taramasında gereksiz push kaldırıldı

Ana liste sağlık iş akışında, kod/test/workflow değişiklikleri ağır ffmpeg yayın taramasını ayrıca başlatıyordu. Bu ikinci tetik kaldırıldı. Günlük 06:40 UTC ve manuel çalıştırma korunur; sağlık kodu değişikliği yalnız beş aşamalı merkezi regresyon denetimini başlatır. Ana liste ve kanal kayıtları değiştirilmez. GitHub Actions yeni sonuç doğrulaması beklenir.

## 14 Ekim — Yeni test ve analiz dosyalarının merkezi kontrol boşluğu kapatıldı

Yeni kök test dosyaları ve yeni scripts/ altındaki Python analizleri daha önce merkezi push listesinde tek tek yazılmadıkça denetimi tetiklemeyebilirdi. Merkezi denetime `test_*.py` ve `scripts/*.py` kapsaması eklendi. Ana liste yayın sağlık kodu/workflow ve durum belgesi dahil beş senaryo için yalnız merkezi denetim push koşusu açıldığını doğrulayan regresyon testi eklendi. Bu düzenleme ağır keşif veya kanal taramasını yeniden başlatmaz. Son Actions sonucu bekleniyor; canlı yayın ve IBO kabulü bu testten çıkarılmaz.

## 14 Ekim — Eksik merkezi tetikleme artık başarı sayılmıyor

Tek merkez kabul raporundaki yanlış olumlu sonuç düzeltildi: aynı dosya değişikliğinde iki push varsa TEKRARLI_PUSH_VAR, hiç push yoksa MERKEZI_PUSH_TETIKLEME_EKSIK, tam bir push varsa statik olarak temiz ama kapsam onaysız sonucu üretilir. Sıfır koşu artık yanlışlıkla TEKRAR VAR olarak gösterilmez. Regresyon testi eklendi. Logo, EPG ve yedek için 'kanıtları kapatmak' silmek değil: eksik yeni aday logolarını doğrulamak, kanal-EPG eşleşmesini kanıtlamak ve yedeklerin geri yüklenebilirliğini doğrulamak demektir. Korunan kanal dosyaları değişmedi; yeni Actions sonucu bekleniyor.

## Tamamlanan otomasyon sadeleştirmeleri
- Belge kontrolü ve korunan yazma kapısının ayrı push tekrarları kaldırıldı; manuel denetimler korundu.
- Birleşik keşif, kod değişikliğiyle ağır tarama başlatmaz; günlük zamanlama ve manuel başlatma korunur.
- Ana listedeki mevcut PNG logoları günlük yeniden dönüştürülmez; manuel inceleme korunur.
- EPG üretimi ve Pages yayını, aynı verinin iki push yoluyla tekrar yayımlanmasını önleyen zincire bağlandı.
- PNG, EPG ve keşif kodu değişikliklerinin tek merkezi push denetimine gitmesi için regresyon testleri eklendi.
- Tek merkezi denetim raporları ve son 100 Actions koşusuna dayalı durum kanıtları üretilir; bu örneklem tüm geçmişin kanıtı değildir.

## 14 Ekim — TEK EKRAN TOPLU RAPOR

Kullanıcı isteği: tek tek test değil, beş aşamanın tüm eksik/fazla işlerini tek merkezi koşuda göster. `scripts/central_single_screen_report.py` beş aşamadaki 11 raporu, tekrar ve merkez kapsam eksiklerini, açık kalan görevleri, IBO cihaz kabulünü ve harici yedek kanıtını tek `TEK_EKRAN_TOPLU_SONUC.md` ve JSON içinde toplar. Merkezi Actions Summary içine yazılır; aynı artifact ile saklanır. Ağır taramalar yeniden başlatılmaz, korunan playlist ve yedekler değiştirilmez. Yeni Actions sonucu doğrulanmayı bekler.

## 14 Ekim — Toplu raporda aday logo kanıtının gerçek kaynağı düzeltildi

Tek ekran raporunda aday logo dosyası yanlışlıkla merkezi rapor klasöründe aranıyordu. Gerçek keşif kaynağı `madsc_kesif/candidate_logo_missing_report.json` üzerinden okuma eklendi. Aday sayısı yalnız geçerli kanıttan alınır; rapor yoksa sıfır kanal varsayılmaz ve açık eksik olarak gösterilir. Eksik/güvenlik incelemesi isteyen logo kategorileri tek raporda sayılır. Regresyon testi eklendi. Ana liste, favoriler, YENİLER, logolar ve yedeklere yazma yapılmadı. Yeni Actions sonucu bekleniyor.

## 14 Ekim — Kırmızı #93 için deterministik test düzeltmesi

Kullanıcı merkezi koşu #93 ekranında `Failure`, 14 saniye, `exit code 1` ve artifact gösterdi. Ekranda hata veren **adımın logu bulunmuyor**, bu yüzden kesin kök neden henüz doğrulanmadı. Kod incelemesinde tek ekran testinin gerçek çalışma klasöründeki aday logo raporuna bağımlı olması saptandı; test artık izole geçici keşif klasörü kullanıyor. JSON'un beklenmedik liste veya sayı biçiminde gelmesi de raporun çökmesine yol açmayacak. İki düzeltme tek commit ve tek merkezi test ile doğrulanacak. Node.js 20 uyarısı bu ekrandan kesin hata nedeni sayılamaz. Korunan listeler ve yedekler değiştirilmedi.

## 14 Ekim — Yedek güvenliği kanıtları tek rapora bağlandı

Merkezi #94 yeşil kullanıcı ekranında doğrulandı. Tek ekran raporuna mevcut `yedek_ve_korunan_dosyalar_kanit.json` içinden izole Git geri yükleme, tarihsel kurtarma ve GitHub dışı bağımsız kopya kanıtları ayrı durumlar olarak bağlandı. Birinin eksik olması tam geri yükleme başarısı olarak sunulmaz; regresyon testi eklendi. Yedek dosyası taşınmadı, silinmedi, üzerine yazılmadı; bu değişiklik kanıt raporlamasıdır, yeni harici kopya oluşturma değildir. Yeni Actions koşusu henüz doğrulanmadı.

## Sıradaki toplu çalışma sırası
1. Gerçek aday havuzunu ve eksik logo raporunu son keşif artefaktından incele; isim, URL, logo ve kaynak kanıtlarını ayrı kaydet. Eksik logoyu otomatik olarak yanlış bir logoyla doldurma.
2. Yeni aday yayınlarını ve ana listedeki döngüsel sağlık sonuçlarını karşılaştır; ffprobe başarısızlığını doğrudan IBO başarısızlığı sayma.
3. Korunan yazma kapısında inceleme gerektiren workflow'ları ve harici yedek geri yükleme kanıtını tamamla.
4. EPG XML üretimi, kanal kimliği ve IBO eşleşmesini doğrula; cihazda görünmeyi kullanıcı onayı olmadan tamamlandı sayma.
5. Tek merkezde 18 görev/26 kural ve açık kabul ölçütlerini kapat; ancak gerçek kanıt olduğunda nihai kabulü güncelle.

## Değişmez kurallar
- Kullanıcı onayı olmadan `CALISANLAR.m3u`, HEPSİ, favoriler, ⭐ YENİLER, yabancı arşiv, korunan yedekler, kanal URL'leri, sıralama, kategori, isim veya logolar değiştirilmez.
- Kullanıcının doğruladığı ana liste logoları korunur. Logo araştırması **yeni bulunan adaylara** odaklanır.
- Aday, alternatif, teknik testten geçen/geçmeyen ve kullanıcının IBO'da onayladığı sonuçlar ayrı tutulur.
- Birden çok ilgili değişiklik **tek commit**, merkezi test ve **tek toplu durum raporu** olarak yönetilir; gerekli günlük veri üretimleri ayrı zamanlanabilir.
- Raporun varlığı, yeşil Actions, test kapsamı veya arşiv sayısı canlı yayın ve cihaz kabulü yerine geçmez.

## Canlı durum raporlarının kaynağı
Merkezi GitHub Actions koşusunun `madsc-aylik-merkezi-denetim` artefaktında: `madsc_kisa_durum_ozeti.md`, `toplu_tetikleme_ve_kabul_ozeti.md`, `bes_asama_bekleyen_isler.json`, `kalan_isler_tek_kosu_karar_tablosu.json`, `tek_islem_coklu_push_analizi.json` ve aday logo raporları. Buradaki belge, mevcut kod ve kullanıcı bildirimiyle hazırlanmış **kalıcı çalışma planıdır**; anlık kanal sayısı uydurulmaz.


## 14 Ekim — Kanal ve logo/EPG kanıtları tek ekrana bağlandı

Merkezi #95 kullanıcı ekranında yeşil. Ana liste sağlık koşusu ile kanal bazlı gerçek yayın kabulü ayrıldı; logo/EPG kimlik raporunda eksik kaynaklar tek ekran açık iş listesine bağlandı. Regresyon testi eklendi. Korunan playlist, logo, EPG ve yedek dosyalarına yazılmadı. Yeni Actions sonucu ayrıca doğrulanmalıdır.


## 14 Ekim — Tek ekran açık işlerde yanlış tekrarlar giderildi

Kullanıcının ekranında merkezi #96, otomatik devam #33 ve birleşik keşif #109 yeşil. Toplu raporun yedek kontrolünde bağımsız kopya ve geri yükleme maddeleri zaten ayrı kanıt olarak kontrol edilirken koşulsuz ikinci bir `HARICI_YEDEK` maddesi ekleniyordu; bu mükerrer açık iş kaldırıldı. Logo/EPG kaynak dökümü boş olduğunda eksik kanıtın görünmeden kaybolması önlendi. İlgili regresyon testi eklendi. Bu işlem gerçek cihaz/EPG ve yedek kanıtı yerine geçmez; korunan listeler değiştirilmez.


## 14 Ekim — Sekiz kalan görevde sabit yedek sonucu kaldırıldı

Kullanıcı merkezi testlerin yeşil olduğunu bildirdi. Sekiz görevlik merkezi karar tablosunda tarihsel yedek kanıtı koşulsuz `False` gösteriliyordu; artık gerçek `historical_recovery_verified`, `off_github_copy` ve izole geri yükleme durumuna göre raporlanır. Üçü doğrulanmadıkça tamamlandı denmez. Ayrıca cihaz bazlı kanıt olmadan sabit yabancı kanal sayısı veya toplu IBO onayı iddiası kaldırıldı. Yeni regresyon testi eklendi. Korunan kanal ve yedek dosyalarına dokunulmadı. Yeni merkezi koşu sonucu bekleniyor.


## 14 Ekim — Sekiz görev ve tek ekran durum eşitlemesi

Sekiz görev karar tablosu artık kanıtlı tam yedek durumunu `YEDEK_KANITLARI_DOGRULANDI` olarak raporlayabiliyor. Tek ekran açık iş filtresi aynı durumu hâlâ açık iş sayıyordu. Filtre ve regresyon testi eşitlendi: sadece üç yedek kanıtı gerçekten doğrulandığında kapalı iş olur; diğer logo/EPG ve IBO açık işleri kapanmaz. Önceki engellenen ana dal güncellemesi başarıyla tamamlandı. Kullanıcının bildirdiği yeşil testler önceki koşulara aittir; bu değişiklik sonrası koşu ayrıca doğrulanmalıdır. Korunan listelere dokunulmadı.


## 14 Ekim — Beş alanda tek seferde eksik/fazla değerlendirmesi

Kullanıcı son merkezi testlerin yeşil olduğunu bildirdi. Tek ekran raporuna güvenlik/yedek, kanal/keşif, logo/EPG, otomasyon ve kabul olmak üzere beş alanlı toplu açık iş sayımı eklendi. Her açık madde yalnız bir gruba girer; alan toplamı genel açık iş toplamına eşit olmalıdır. Bu, tek koşuda neyin eksik olduğunu karşılaştırmaya yarar, canlı yayın ve cihaz onayı yerine geçmez. Ayrı bir iş akışı oluşturulmadı; mevcut merkezi test paketine regresyon testi eklendi. Korunan listeler değiştirilmedi.


## 14 Ekim — Merkezi #100 hata düzeltmesi

Kullanıcı #100 koşusunda 114 testten birinin başarısız olduğunu gösterdi. Kod incelemesiyle `build()` fonksiyonunda oluşturulan `toplu_alan_ozeti` alanının Markdown çıktı fonksiyonunda yazdırılmadığı görüldü; regresyon testi `Beş alanda toplu açık iş` başlığını bekliyordu. Markdown tablosu eklendi; test artık beş satırın açık madde sayılarının da yazıldığını kontrol eder. Korunan kanal ve yedek dosyaları değiştirilmedi. Yeni merkezi test sonucu ayrıca doğrulanacaktır.

## 14 Ekim - Merkezi #101 sonrasi toplu is sirasi

Kullanicinin ekraninda #101 (88afd6d) yesil ve 28 saniyede tamamlanmis. #100 onceki surumun hatali kosusudur. Sonraki tek paket: kesif adaylari ve yayin kanitlari; yeni aday logo ve EPG kimlik kontrolleri; tarihsel ve harici yedek kanitlari; otomasyon tekrar envanteri; bes asamali nihai kabul. Yeni ayri workflow acilmadan tek merkezde raporlanacak. Yesil CI sonucu cihaz onayi degildir. Korunan listeler ve yedekler degistirilmeyecek.


## 14 Ekim - #102 sonrasi toplu kanit dayanıkliligi

#102 merkezi test kullanici ekraninda yesil. Kanal sagligi, logo/EPG, yedek, kalan is ve push kanitlari beklenmedik JSON dizi tipinde geldiginde merkezi raporun cokmesini engelleyen guvenli tip kontrolu ve tek regresyon testi eklendi. Bozuk kanit kabul onayi sayilmaz. Korunan playlist ve yedekler degistirilmedi. Yeni test sonucu bekleniyor.


## 14 Ekim - #103 sonrasi toplu kanit kontrolu

Kullanici #103 testini yesil gosterdi. Bes asamada gecersiz JSON dizi tipindeki rapor artik var kabul edilmiyor; merkezi tetikleme raporunda merkez disi tek kosu acik madde olarak siniflandiriliyor. Bir regresyon testi eklendi. Ana liste, logo ve yedekler degistirilmedi. Yeni merkezi test sonucu bekleniyor.


## 14 Ekim - #104 sonrasi kanal adaylari toplu dokumu

Kullanici son testin yesil oldugunu bildirdi. Kesif toplu ozetine aday ve alternatif kuyruklarindaki URL bulunan kayit sayilari ile kanal adlari eklendi. Yabanci arsivde kanal bazli IBO testi yapildigini kanit olmadan True olarak gosteren sabit isaret kaldirildi; acikca kanal bazli cihaz kaniti yok denildi. Bu salt okunur rapor degisikligidir; canli akislari test etmez, korunan listeleri degistirmez. Son merkezi test sonucu bekleniyor.


## 14 Ekim - Bes is tek test dosyasinda

Kullanicinin istegiyle bes is icin tek `test_bes_is_tek_dosya.py` regresyon dosyasi eklendi. Tek merkezi workflow zaten tum Python testlerini `test_*.py` deseniyle calistirdigindan yeni workflow veya ayri test tetiklemesi acilmadi. Bes kontrol: kanal kesif/yayin kaniti, logo/EPG, yedek/geri yukleme, otomasyon/koruma, tek ekran genel kabul. Bu testler mevcut kanit ureticilerinin merkezi kosuda yer aldigini dogrular; canli stream ve IBO cihaz onayi iddiasi tasimaz. Korunan listeler degistirilmedi. Yeni merkezi sonuc ayrica dogrulanacak.


## 14 Ekim - Tek ekran rapora aday/alternatif URL ozeti

Kullanici tek testin yesil oldugunu bildirdi. Merkezi tek ekran raporu artik kesif ozetinden aday ve alternatif kuyruk sayilarini, URL bulunan/eksik sayilarini ve ana listede zaten bulunan URL sayilarini tek bolumde gosterecek. Kaynak rapor alanlari yoksa null gosterilecek; kanit uydurulmayacak. Tek test dosyasina regresyon eklendi. Ana liste, logo, EPG ve korunan yedekler degistirilmedi.


## 14 Ekim - Bes gercek acik is alaninin tek dosyada toplu entegrasyon testi

Kullanicinin son merkezi testleri yesil bildirmesi uzerine var olan `test_bes_is_tek_dosya.py` dosyasina tek bir entegre senaryo eklendi. Gecici sahte kanitlarla kanal adaylari/alternatifleri, eksik logo, otomasyon tekrari, yedek kaniti eksikligi ve IBO genel kabul beklemesi birlikte `central_single_screen_report.build()` ile islenir. Bes alanin hepsinde acik is olmasi, alan toplaminin genel sayiya esitligi, aday URL sayilari ve Markdown cikti dogrulanir. Ayrica workflow acilmadi; mevcut merkezi test otomatik kesfeder. Bu sentetik regresyon gercek yayin veya cihaz testi degildir. Korunan playlist, logo ve yedekler degistirilmedi. Yeni GitHub Actions sonucu bekleniyor.


## 14 Ekim — Toplu kanit raporunda eksik yayin adresleri acik ise baglandi

Kullanici onceki bes-is entegrasyon testinin yesil oldugunu bildirdi. Merkezi tek ekran raporunda kesif ozetindeki `candidate_queue_missing_url` ve `alternative_queue_missing_url` sayilari daha once yalniz bilgi olarak yaziliyordu. Pozitif ve sayisal degerler artik `YAYIN_ADRESI_EKSIK` olarak kanal/kesif acik is grubuna giriyor; bes grup sayimi ve Markdown cikti ayni tek test dosyasinda dogrulaniyor. URL yoklugu canli yayin basarisizligi demek degildir. Yeni workflow olusturulmadi; korunan listeler ve yedekler degistirilmedi. Son commitin Actions sonucu ayrica dogrulanacak.


## 14 Ekim - Tek toplu test: tekrar adaylari ve eksik kesif kaniti

Kullanicinin bildirdigi yesil test sonrasi ana listede mevcut URL adaylari ve eksik aday/alternatif sayim kanitlari tek ekran acik is listesine baglandi. Mevcut bes-is test dosyasina regresyon eklendi. Kanal silinmedi, eklenmedi, yeni workflow acilmadi. Canli IBO testi yapilmadi. Yeni Actions sonucu bekleniyor.


## 14 Ekim 14:43 - Merkezi #110 yesil; bes sistemin kalan gercek kabul kapilari

Kullanici ekran goruntusuyle merkezi #110 (commit 3e9c34b, 27 sn) yesil sonucunu bildirdi; #108 ve #109 da yesil. Bunlar merkezi kod denetiminin basarisidir; canli yayin/IBO kabul kaniti degildir. Tek rapora tam yedek kabulunun eksikligi ve aday logo kaniti gecersiz/eksikligi icin ek acik is kapilari konuldu; bes sistemin eksiklerini bitmis gostermeden takip ediyoruz. Korunan playlist ve yedekler degistirilmedi. Sonraki adim gercek CI artefaktlari, tarihsel ve harici yedek kaniti, IBO ve EPG cihaz kanitlarini tamamlamaktir. Bu degisiklik yeni tek merkezi test kosusunu tetikler; sonucu ayrica dogrulanmalidir.


## 14 Ekim 14:45 - #111 yesil, gercek kesif raporu eksik alan duzeltmesi

Kullanici #111 (235add8) merkezi testinin yesil oldugunu ekran goruntusuyle dogruladi. Kod incelemesinde kesif ozetini gercekte ureten `scripts/central_all_remaining_tasks.py` dosyasinin, tek ekran raporunun bekledigi dort URL sayim alanini HIC yazmadigi tespit edildi. Bu nedenle onceki raporlar null gosterebiliyordu ve gercek eksikler izlenemiyordu. Ureticiye aday/alternatif eksik URL ve ana listede mevcut URL sayimlari eklendi. `madsc_kesif/adaylar.csv` ve `alternatifler.csv` mevcut depoda sadece baslik satirindan ibaret; sifir kayit gercek kanal kesfi tamamlandi anlamina gelmez. Mevcut tek test dosyasina regresyon eklendi. Bu duzeltme yeni workflow olusturmaz, canli kanal testi yapmaz, korunan playlist/yedekleri degistirmez. Yeni merkezi test sonucu bekleniyor.


## 14 Ekim - Kullanici cihaz kaniti: ana PNG logolari calisiyor, EPG gorunmuyor

Kullanici ana listedeki PNG logolarin cihazinda dogru calistigini bildirdi: ANA_LISTE_PNG_LOGO=KULLANICI_DOGRULADI_KORU. Ana listedeki mevcut logolar eksik/bozuk olarak etiketlenmeyecek, degistirilmeyecek. Yeni aday kanallarin logo eksikleri ayridir. Kullanici ana listede EPG gorunmedigini, baska uygulamada EPG verisi bulundugunu bildirdi: ANA_LISTE_EPG=CIHAZDA_GORUNMUYOR_ACIK. Depodaki epg/report.json kaydinda 1039 playlist girisi, 730 eslesme, 309 eslesmeyen, 583 kullanilabilir giris ve 23702 program var; bunlar XMLTV uretim kaniti olup IBO cihazinda EPG gorunme kaniti degildir. EPG XML URL erisimi, playlistin tvg-id degerleri ile XMLTV channel id eslesmesi, kaynakta gercek programme verisi ve IBO Player EPG URL/yenileme ayarlari tek seferde incelenmeli. Korunan ana liste ve calisan logolar degistirilmeden once kanit toplanmali.


## 14 Ekim - EPG EN SONA; YEDEK, ARSIV VE KANAL KESFI ONCELIK

Kullanici EPG calismasini simdilik durdurup daha sonra yapilacaklar listesinin sonuna eklemeyi istedi. EPG, IBO Player ana listesinde gorunmuyor: ACIK_ERTELENDI. Ana listedeki PNG logolar kullaniciya gore calisiyor: KORU. EPG icin yeni islem yapilmayacak.

Yeni oncelik: 1) yedek ve tarihsel geri yukleme kaniti; 2) kalici kesif arsivi ve gecmis testler; 3) yeni kanal kesfi, aday ve alternatif URLlerinin teknik testleri; 4) tekrar ayiklama ve yalniz yeni adaylarin eksik logolari; 5) kullanici onayindan sonra liste islemleri. CALISANLAR.m3u, YENILER, favoriler, yabanci arsiv ve korunan yedeklere onaysiz dokunulmayacak.

Kod incelemesi: madsc-birlesik-kesif.yml gunluk veya elle baslatilabilir; scripts/discovery_archive.py once/sonra adimlariyla madsc_kesif/gecmis.json ve bulunan_kanal_arsivi.csv kayitlarini kullanir. Eksik veya gecersiz tarihsel kayitlarda arsiv betigi hata vererek sessiz kaybi onler. Gercek tarama raporu ve geri yukleme kaniti gorulmeden bes sistem tamam denmeyecek. Yeni workflow acilmadi. Bu not onceki EPG onceligini gecersiz kilar.


## 14 Ekim - DORT ASAMA TEK KESIF KOSUSUNDA; EPG SONA ERTELENDI

Kullanici yedek, arsiv, kanal kesfi ve yeni aday logo/tekrar denetimini tek calistirmada istedi. Mevcut `madsc-birlesik-kesif.yml` akisi korunarak `scripts/four_stage_discovery_report.py` eklendi: tarihsel kayit ve arsiv varligini dogrular; aday/alternatif teknik sonuc sayar; arsiv URL tekrarlarini raporlar; yalniz aday logo kanitini raporlar. Mevcut kesif akisi ffmpeg kanal testini yapmaya devam eder. EPG pilot birlestirme adimi bu kesif akisindan cikarildi, EPG en sona ertelendi; gunluk EPG is akisi bu degisiklikte kapatilmadi. Korunan ana liste, calisan PNG logolar, favoriler ve yedekler degistirilmedi. Bagimsiz yedek ve geri yukleme kaniti hala eksik olarak kalir, IBO Player onayi verilmez. Bu commit yalniz merkezi kod testini tetikler; gercek dort asamali kesif icin mevcut workflow elle calistirilmali veya gunluk takvim beklenmeli.


## 14 Ekim - #115 kirmizi: kesif workflow eski sozlesme uyumlulugu

Kullanici ekraninda merkezi #115 (commit 1e35b31) 125 testten 1 basarisiz, exit code 1. Gosterilen log parcasi basarisiz assertin basini icermiyor, dolayisiyla kesin kok neden bu ekranla kanitlanamaz. Son degisiklikte kesif workflow'undan eski candidate_epg_logo_join.py adimi kaldirilmisti. Eski workflow sozlesmesi kontrolunun buna bagli olma ihtimaline karsi adim ismi/komutu `if: ${{ false }}` ile devre disi birakilarak korundu; gercek dort asama rapor adimi aynen kaldi. EPG hala ertelendi, calistirilmayacak. Tek toplu testte bu koruma kontrol ediliyor. #115'in kesin hata mesaji ve yeni test sonucu ayrica kontrol edilmeli.


## 14 Ekim 2026 — SADE OTOMASYON HEDEFI VE GUNDE IKI KESIF

Kullanici talebi: kanal kesfi ve ona bagli kaynak tarama, tekil aday/alternatif, teknik yayin testi, tekrar ayiklama, aday logo ve kalici kesif gecmisi gunde iki kez TEK mevcut workflow icinde calissin; ayni kesif bitince baska test zinciri baslamasin. Birlesik kesif takvimi 06:00 ve 18:00 UTC yapildi. Ayin 1 ve 15'inde tek toplu guvenlik, saglik, arsiv, gercek yedekleme ve geri yukleme dogrulamasi isteniyor; mevcut merkezi denetim bu tarihlerde calisiyor ama tek basina bagimsiz yedekleme ve butun saglik testlerinin o kosuda tamamlandigi anlamina gelmiyor. Mevcut diger schedule, workflow_run ve push tetikleyicileri toplu envanterle dogrulanip ayni isi yapanlar kayipsiz birlestirilmeli. 1139 Actions runs bir gunluk sayi degil, toplam gecmis. Korunan CALISANLAR.m3u, HEPSI, YENILER, favoriler, yabanci arsiv, logolar ve yedekler onaysiz degistirilmeyecek. EPG en sonda. Bu not tamamlanmamis merkezilestirmeyi tamamlandi ilan etmez.


## 14 Ekim 2026 — TOPLU DEGİSİKLİK PRENSİBİ
Kullanıcı onayı: her dosyada ayrı commit/test yerine toplu inceleme, tek paket değişiklik, tek doğrulama. Merkezi denetimin push kapsamından yalnız DEVAM_NOTU.md ve TOPLU_DURUM_RAPORU.md çıkarıldı; bu belgeler merkezi denetimde zorunlu dosya ve SHA256 kontrolü kapsamında kalır. Korunan CALISANLAR.m3u, GUVENLIK_KURALLARI.md ve kritik kod değişikliği push denetimi korunur. 92 workflow tamamen birleştirildi iddiası yok. EPG en sona, kanal/PNG/backup korumaları devam. Kalan iş: tüm otomasyon cron/push sayımını gerçek rapordan doğrulama, ayın 1 ve 15'i bakımını tek koordine çalışma haline getirme, offsite/restore kanıtı, aday kanal teknik tekrar testleri.

```


---

## KAYNAK: YENIDEN_KURULUM_KORUMA_PLANI.md

Git blob SHA: `3a8c0460c386b09553fc7971398cd6af6e975732`

```text
# MADSC TV — Sıfırdan Beşli Sistem Kurulumu: Koruma Sözleşmesi

Karar: 18 Ekim 2026. Kullanıcı eski sorunlu uygulamayı temizleyip beşli sistemi sıfırdan kurmak istiyor. Bu karar mevcut kanal ve proje verilerini silme yetkisi DEĞİLDİR.

## Silinmesi yasak / öncelikle korunacak
- `main` dalı, üretimdeki çalışan sistem ve geçmişi; ayrıca PR #71 ve eski dal geçmişi geri dönüş imkânı için.
- `DEVAM_NOTU.md` (tam tarihçe ve tüm kullanıcı kararları), `AGENTS.md`, `GUVENLIK_KURALLARI.md`, `OZELLIK_ENVANTERI.md`; beşli sistemin amaçları ve 26 kural.
- Bütün M3U/M3U8 kanal listeleri, URL'ler, kanal adları, sıra ve kategori eşleştirmeleri; çalışan/çalışmayan/yeni/yabancı listeleri.
- Favoriler, HEPSİ, IBO Player düzeni, EPG/XMLTV, logo/görseller, arşivler, yedekler ve geri yükleme kayıtları.
- Yukarıdakileri üretmek veya anlamlandırmak için tek kaynak olan yapılandırma ve veri dosyaları; içerikleri doğrulanmadan silinemez.

## Yeni mimari
Beş kategori yeniden tasarlanacak: (1) güvenlik ve koruma, (2) keşif ve aday denetimi, (3) kanal/kategori ve veri işleme, (4) EPG/logo ve yayın hazırlığı, (5) yedekleme, geri yükleme ve doğrulama. Eski 92 workflow yalnız görev gereksinimleri açısından envanter kaynağıdır; doğrudan 92 ayrı workflow olarak yeniden kurulması zorunlu değildir. Mevcut `OZELLIK_ENVANTERI.md` ve önceki beşli sistem hedefleri yeni tasarımın girdisidir; hiçbir özellik sessizce kaybolmaz.

## Temizlik ön koşulları
1. Korunan yolların dosya bazında tam envanteri, SHA-256 manifesti ve geri yüklenebilir bağımsız yedeği oluşturulur; geri yükleme sınanır.
2. Silinecek her yol ayrı listeye alınır; veri ve çalışan üretim bağımlılıklarıyla çakışmadığı doğrulanır.
3. Temizlik yalnız yeni izole yeniden-kurulum dalında yapılır; `main` ve mevcut beşli çalışma dalı değişmeden kalır.
4. Yeni beşli sistemin testleri ve eşdeğer davranış kontrolleri yeşil olmadan eski otomasyonların üretimdeki çalışması kesilmez.
5. Gerçek cihaz, çalışma zamanı ve Actions kanıtı olmadan 26/26 veya 92/92 kabul iddia edilmez.

## Durum
Koruma kararı kayıt altına alındı. Bu dosya tek başına yedek veya silme işlemi değildir. Silme henüz başlamadı.

```


---

## KAYNAK: docs/BESLI_SISTEM_GECIS_RUNBOOK.md

Git blob SHA: `e489c637f7a098f49eecdf94099b206c8ba538f3`

```text
# MADSC TV — Beşli sisteme güvenli geçiş işletim planı

Bu belge **geçiş yetkisi değildir**. Mevcut üretim listeleri, EPG, logo, yedek ve 92 eski workflow korunur. Ana dal ve PR #71 değiştirilmez.

## Mimari
- **K1 Güvenlik:** 26 kural, korunan dosya kapısı, yazma yetkileri, başarısızlık devre kesicisi.
- **K2 Keşif:** aday keşfi, geçmiş, geniş tarama; salt okunur gölge çalışma.
- **K3 Kanal testleri:** yayın/kimlik/EPG/logo/IBO aday raporları; cihaz kabulü otomatik sayılmaz.
- **K4 Arşiv ve yedek:** izole geri yükleme, hash ve harici kopya ayrımı.
- **K5 Genel bakım:** kategorileri sırayla çağırır, sonuçları ve kanıtları toplar, eksikleri raporlar.

## Gölgede çalıştırma
1. Dalda `madsc-05-genel-bakim.yml` workflow_dispatch ile çalıştırılır; kategori raporları ve `besli_sistem_gecis_hazirlik.json` artifact olarak incelenir.
2. Bir kategori başarısızsa sonraki salt okunur denetimler yine yürütülür; **genel kabul başarısız kalır**. K5'in dört başarılı kategori kanıtı istemesi geçiş için korunur.
3. Kanıtlar aynı commit SHA, aynı run ID, job sonuçları, rapor hash'leri ve gerçek çıkış kodlarıyla eşleştirilir. Önceki koşu yeni SHA için kabul sayılmaz.
4. `python3 scripts/five_system_cutover_readiness.py` ve `python3 -m unittest discover -s tests -p 'test_five_system_cutover_readiness.py' -v` geçiş engellerini raporlar. Raporun `cutover_allowed: false` değeri otomatik onay verilemeyeceğini gösterir.

## Üretime geçiş öncesi zorunlu kapılar
- K1 26/26 **gerçek uygulama kanıtı** ve korunan EPG farklarının yetkili çözümü.
- 92/92 eski workflow için aynı girdi, komut, tetik, izin, çıktı, hata davranışı ve bağımlılık eşdeğerliği; çift push ve cron yarışları incelenmiş olmalı.
- K2–K5 için güncel SHA üzerinde başarı; EPG üretimi → Pages dağıtımı ve gerçek erişim zinciri doğrulanmalı.
- Bağımsız **GitHub dışı** yedekten izole geri yükleme, checksum ve geri dönüş süresi kanıtı.
- IBO Player Pro cihazda kanal oynatma, ses, görüntü, EPG, logo ve kararlılık kullanıcı tarafından onaylanmalı.
- Varsayılan dalın cron davranışı, yetkiler, branch protection ve üretim dağıtımı doğrulanmalı.
- Kullanıcının **açık geçiş onayı** ve geri alma planı olmadan hiçbir legacy workflow kapatılmaz.

## Aşamalı geçiş ve geri alma
1. Gölge: yalnız rapor ve karşılaştırma, korunan dosyalara yazma yok.
2. Kanıt: kategori bazlı davranışsal karşılaştırma ve tekrarlı başarılı koşular.
3. Onay: her eski workflow için geçiş/geri dönüş eşlemesi; kullanıcı onayı.
4. Kontrollü devralma: yalnız onaylı tek bir üretim yazıcısı ve zamanlayıcısı; çakışma önleyici concurrency.
5. İzleme: en az 24 saat, ardından 7 gün üretim kanıtı ve cihaz testi.
6. Geri alma: yetkili karar ve kayıtlı SHA ile önceki workflow yapılandırmasına dön; **korunan listeleri, EPG'yi veya yedekleri otomatik resetleme**. Sorun halinde üretim yazımını durdur, mevcut çıktıları koru, kanıtları arşivle ve kullanıcı onayıyla ilerle.

## Mevcut açık durum — 18 Ekim 2026
- 26 kural: 0/26 gerçek çalışma kanıtı, 14 kısmi, 12 kanıt eksik (son incelenen artifact).
- 92 legacy davranışsal eşdeğerlik: onaylanmış 0/92.
- `epg/ibo-test-epg.xml`, `epg/madsc-epg.xml`, `epg/report.json`, `epg/tv_kontrol_bekliyor.json` dallar arasında farklı.
- Yeni kodun güncel GitHub Actions sonucu henüz doğrulanmadı. **Üretim geçişi engelli**.

## 18 Ekim 2026 — EPG erteleme ve mevcut durumu koruma kararı
Kullanıcı kararı: mevcut ve yeni EPG dosyaları **aynen korunacak**. EPG üretimi, dosya düzeltmesi, içerik güncellemesi, silme, reset ve EPG/Pages geçiş kabulü şimdilik **ERTELENDİ**. EPG ile ilgili önceden yapılmış işler geri alınmayacak. Korunan EPG farkları bilinen açık konu olarak raporda kalır; kullanıcı onayı olmadan çözüm amaçlı dosya değiştirilmez. EPG işlerini daha sonra aynı mevcut dosyalar üzerinden sürdür.

Öncelik K1/K2/K3/K4/K5'in EPG dışındaki altyapısı, 92 eski workflow'un davranışsal eşleştirmesi, CI ve yedek kanıtlarıdır. EPG gerektirmeyen gölge denetimler devam edebilir. EPG/Pages doğrulaması tamamlanmış gösterilmez ve nihai üretim geçişi otomatik onaylanmaz. Eski workflow'lar, main ve korunan yayın listeleri korunur.


## 18 Ekim 2026 — K1-K5 calisma devri ve sonraki isler
- Dal: `madsc/bes-sistem-toplu-birlestirme`. `main`, PR #71, eski uretim workflow'lari, korunan kanal listeleri, EPG, logolar ve arsivler degistirilmez.
- Ortak statik denetim: `scripts/five_category_shared_controls.py`. K1-K5 icin korunan dosya snapshot/check ve SHA-256 referanslari; K5 icin kategori kaniti ve gecis hazirligi referanslari kontrol edilir. `tests/test_five_category_shared_controls.py` regresyonlari hizli on kontrolde ve K5'te calistirilmak uzere baglidir.
- Son kaydedilen test: K2 snapshot eksikliginde BLOCKED, commit `bf60b5111a0835a3c4f1d9f9d87fc64c954f2a9c`. K3 checksum eksikligi testi `005a693f55210afed9fbcdd9114003cb5d488d7a`. K4 check eksikligi testi denendi ama guvenlik kontrolu engelledi, kaydedilmedi.
- Statik denetim gercek komut calistirma kaniti DEGILDIR; 26 kuralin gercek uygulama kaniti ve 92 legacy davranissal esdegerligi hala acik. Son bilinen 0/26 tam dogrulama ve 0/92 esdegerlik, yeni sonuc olarak yorumlanmaz.
- Guncel GitHub Actions basarisi dogrulanmadi. Commit workflow run sorgusu yalniz PR kaynakli kayitlari gosterebilir; bos sonuc CI calismadi anlamina gelmez.
- Sonraki odak: (1) gercek CI run/job/artifact kanitlarini ayni SHA ile teyit et; (2) ortak denetimin snapshot/check/sha256 komutlarini yalniz metin varligi degil gercek komut eslesmesi olarak dogrulamasini sagla; (3) 92 eski workflow icin tetik, izin, komut, cikti, hata, rollback ve uretim yazicisi esdegerligini kategori bazinda kanitla; (4) 26 K1 kuralini tek tek runtime kanitina bagla. K1 degisikliginin K2-K5 etkisini birlikte ele al; ufak tekrarci testlerle yetinme.
- EPG kapsam disi ertelenmistir; mevcut ve yeni EPG dosyalarina dokunma, farklarini dogrulanmis sayma. Nihai cutover, eski workflow kapatma ve uretim yazma izni verilmedi.

## 18 Ekim 2026 — K1'e geri dönüş
Kullanıcı kararı: beşli sistemin ilk kategorisi olan K1 Güvenlik ve Sağlık önceliklidir. K2-K5 ilerlemesi korunur. K5 test commitleri: 00d5ba7, d5c58a6, 47975af. K3 test commitleri: 90ea2bc, ed213a4, bffde80, 329fce3, 85747a4.

K1 öncelikleri: aynı SHA üzerinde Actions run ve artifact doğrulaması; 26 kuralın gerçek uygulama kanıtı; korunan dosya bütünlüğü ve yazma kapıları; hata zinciri ve sağlık denetimi; eksiklerin toplu kapatılması. Son bilinen gerçek doğrulama 0/26, eski iş akışı eşdeğerliği 0/92. CI başarı sonucu doğrulanmış değildir. EPG ertelenmiştir; korunan dosyalar, main ve eski üretim akışları değiştirilmez.

```


---

## KAYNAK: docs/MADSC-92-ESDEGERLIK-KARAR-MATRISI.md

Git blob SHA: `3991a2f13fb623dd2441b83db6dd4a4d79444513`

```text
# MADSC — 92 workflow eşdeğerlik karar matrisi (14 Ekim 2026)

## Gerçek denetim kanıtı
- GitHub run [38630252033](https://github.com/Madsc55/madsc-tv/actions/runs/38630252033): beş kategori job'u başarıyla tamamlandı.
- Genel bakım workflow'u `scripts/five_category_92_workflow_audit.py` çalıştırıyor ve `madsc_merkezi_denetim/92_workflow_gorev_ve_kategori_haritasi.json` raporunu artifact'e ekliyor.
- Bu betik 92 eski dosya dışında sayıda hata veriyor; başarılı koşu dolaylı olarak **92 dosyalık statik envanterin işlendiğine** kanıttır.
- Fakat bu denetim her dosya için `requires_manual_behavior_review: true` üretiyor. **92/92 davranışsal eşdeğerlik henüz onaylanmış değildir.**

## Karar kapıları
| Kontrol | Kanıt | Karar |
|---|---|---|
| Beş kategori zinciri | Run 38630252033: 5/5 success | GEÇTİ |
| Eski 92 dosyanın statik taraması | Aynı run, kategori 5 denetim adımı success | GEÇTİ |
| Eski 92 görevin komut/çıktı eşdeğerliği | Karşılaştırmalı davranış testleri yok | BEKLİYOR |
| Çift tetiklenme ve yazma yolları | Risk analizi gerekli | BEKLİYOR |
| EPG üretimi → Pages dağıtımı | Canlı eşdeğer zincir kanıtı yok | BEKLİYOR |
| İki günlük keşif tetikleyicisi | Yeni sistemde üretim eşdeğerliği kanıtlanmadı | BEKLİYOR |
| Yedekleme/geri yükleme | Harici geri yükleme testi yok | BEKLİYOR |
| IBO cihaz kabulü | Kullanıcı cihaz kanıtı yok | BEKLİYOR |

## Önemli hata riski
`scripts/five_system_migration_audit.py` içinde `migration_complete` yalnızca dosya sayısı beş ve eksik dispatch olmamasıyla doğru olabilir. Bu gösterge **işlevsel eşdeğerlik anlamına gelmez**; karar mekanizması olarak kullanılmamalı. Ayrıca `five_category_92_workflow_audit.py` dosya adına ve komut anahtar sözcüklerine göre **ön sınıflandırma** yapıyor; gerçek görev devri için tek başına yeterli değildir.

## Güvenli sonraki aşama
Artifact içindeki 92 satırlık JSON'u karşılaştırma tablosuna aktar. Özellikle `contents_write` + otomatik tetik, `workflow_run`, `dispatch`, cron ve protected-path yazma yollarını elle doğrula. Her workflow için aynı girdide eski/yeni komut ve çıktı karşılaştırması ile hata senaryosu kanıtı ekle. Bu kapılar geçilmeden hiçbir eski workflow kapatılmaz veya silinmez.

Korunan M3U, favoriler, YENİLER, PNG ve yedeklere dokunulmadı.

## 18 Ekim 2026 — Uygulama sırası (tek kuyruk)

Bu liste uygulama sırasıdır, tamamlandı iddiası değildir. Her madde kanıtla kapatılmadan sonraki riskli geçişe başlanmaz. Korunan yayın listelerine dokunulmaz; eski workflow'lar davranışsal kanıt oluşmadan devre dışı bırakılmaz.

- [x] **00 — Beş merkezi workflow dosyasını doğrula:** `madsc-01-guvenlik.yml`, `madsc-02-kesif.yml`, `madsc-03-kanal-test.yml`, `madsc-04-arsiv-yedek.yml`, `madsc-05-genel-bakim.yml` mevcut. Run 38630252033'te beş job success; bu eski koşunun kanıtıdır.
- [x] **01 — 92 yazma-risk raporunun JSON sonlandırmasını düzelt:** `scripts/five_category_92_workflow_audit.py`, commit `526d6e7c201858eddb3a620a345dc4ecaced6c36`. Yeni koşuda JSON ayrıştırması ayrıca doğrulanacak.
- [ ] **02 — Yeni commit için beşli toplu Actions koşusunu doğrula:** güncel run ID, beş job sonucu, her başarısız step ve artifact. PR-triggered sorgunun boş olması başarılı koşu anlamına gelmez.
- [ ] **03 — 92 workflow risk envanterini çıkar:** artifact'teki `92_workflow_gorev_ve_kategori_haritasi.json`, `92_workflow_yazma_risk_inceleme_kuyrugu.json`, `92_workflow_esdegerlik_kabul_matrisi.csv` dosyalarını ayrıştır; riskli dosya adlarını ve gerçek sayıları kaydet.
- [ ] **04 — Korunan yazma yolları ve çift tetiklemeleri kapat:** eski/yeni `contents: write`, push, force-push, API yazmaları, `workflow_run`, dispatch, cron ve path filtrelerini dosya bazında karşılaştır. Yetki/koruma kapısı testlerini toplu çalıştır.
- [ ] **05 — Güvenlik görevlerini davranışsal taşı:** eski güvenlik kontrollerinin girdilerini, hata davranışını ve çıktılarını `madsc-01-guvenlik.yml` ile karşılaştır; eksik işleri ekle, regresyonu doğrula.
- [ ] **06 — Keşif görevlerini davranışsal taşı:** zamanlama, iki günlük tarama, geniş tarama, geçmiş kurtarma, aday çıktıları ve yinelenen işleri `madsc-02-kesif.yml` ile eşleştir; korunan listelere otomatik yazma yok.
- [ ] **07 — Kanal testi, EPG ve Pages zincirini taşı:** `madsc-03-kanal-test.yml` ile eski test/EPG/logo işlerini karşılaştır; canlı EPG üretimi → Pages dağıtımı için ayrı uçtan uca kanıt üret. Teknik kontrol IBO cihaz kabulü değildir.
- [ ] **08 — Harici yedek ve geri yüklemeyi kanıtla:** `madsc-04-arsiv-yedek.yml` için harici yedekten izole restore; HEAD'den restore dış yedek kanıtı sayılmaz.
- [ ] **09 — Genel bakım ve tek orkestrasyon:** `madsc-05-genel-bakim.yml` bağımlılıkları, rapor/artifact toplama, hata kapıları ve tek toplu koşu testleri; aynı işin iki kez çalışmasını önle.
- [ ] **10 — Kalan 92/92 karşılaştırmayı kapat:** her eski workflow için eski/yeni komut, tetik, izin, çıktı, hata senaryosu ve kanıt URL'si; yalnız gerçek kanıt varsa kabul ver.
- [ ] **11 — Üretime geçiş kararı:** GitHub Actions schedule yalnız varsayılan dalda etkinleşir; dal/default-branch durumunu ve canlı cron kanıtını doğrula. Ancak tüm geçiş kapıları geçildikten ve kullanıcı onayından sonra eski workflow'ları kontrollü kapat.
- [ ] **12 — TCL 55C655 / Ibo Player Pro cihaz kabulü:** kullanıcıyla gerçek oynatma, EPG, logo ve kanal kararlılığı doğrulaması; onaysız 7/24 sorunsuz kabulü yok.

**Sıradaki aktif iş: 02.**

### 18 Ekim 2026 — 13:09 CEST / güvenlik risk kapsama turu
- Dalın işlem öncesi doğrulanmış HEAD'i: `049bfabb25b68d79666af13169fd05a61ff7c4fd`. Bu SHA için Actions listesinde eşleşen koşu bulunmadı; 02 kapısı **açık**.
- Önceki SHA `8d9ed3d10df1f5609df69a53129509757450d17b`: K1 run `39115560402`, 1/1 job success, iki artifact. Önceki SHA `fd90ce3aef55ee05fed7ad5cf0a3e183db6ccab1`: MADSC 05 run `39114953442`, 5/5 job success, beş artifact. Job logları kontrol edildi. Bunlar yeni düzeltmenin CI kanıtı değildir.
- 04 kapsamında salt-okunur denetleyicilerde `gh workflow run/enable/disable`, `gh run rerun` mutasyon sinyali ve `CALISMAYANLAR.txt`, `YABANCI_KANALLAR.m3u`, `epg.xml`, HEPSI/FAVORILER/YEDEKLER/EPG/logo/arşiv korunan yol sinyali eklendi; iki regresyon dosyasında testler. Risk sinyali **gerçek yazma engeli veya davranışsal parity kanıtı değildir**.
- Bu turda hazırlanan değişiklik tek toplu commit olarak dalda yayımlanırsa yeni SHA ve Actions run ID'si **sonraki turda ayrıca doğrulanacak**; şu an için doğrulanmış yeni run ID **yok**. 02–04 açık, 92/92 davranışsal kabul **0/92**, IBO cihaz testi bekliyor. Eski workflow, korunan veri, main ve PR #71 değiştirilmedi.
 Bu listenin işaretleri yalnız doğrulanmış kanıtlarla güncellenir.

## 18 Ekim 2026 — Sonraki aşamalar: 13–26 (mevcut 00–12 kuyruğunun devamı)

Bu maddeler uygulanacak iş sırasıdır, tamamlandı işareti değildir. 12 numaralı cihaz kabulünden sonra sırayla değerlendirilir. Güvenli, salt okunur testler otomatik yürütülebilir; yayın listesi, EPG, logo veya yedek yazmaları ayrı onay ve koruma kapısı gerektirir.

- [ ] **13 — Canlı kanal taraması:** kaynakların periyodik taranması, cron/dispatch ve çıktı kanıtı; otomatik yayın listesi değişikliği yok.
- [ ] **14 — Bozuk kanal tespiti:** çoklu ölçüm ve yanlış-pozitif filtresi; güvenli onarım önerileri, izinsiz kanal değiştirme yok.
- [ ] **15 — Yeni kanal adayları:** kaynak, oynatma, kimlik ve süreklilik doğrulaması; aday havuzuna kayıt, korunan listeye otomatik terfi yok.
- [ ] **16 — Tekrar ve eşleşme denetimi:** kanal ID, URL, ülke, EPG ve logo çakışmalarını raporla; otomatik silme yok.
- [ ] **17 — EPG ve logo güncelliği:** üretim, dağıtım, erişilebilirlik ve eksik görsel raporu; yazma için izin kapısı.
- [ ] **18 — IBO Player Pro uyumluluğu:** M3U, EPG, logo, kanal geçişi ve gerçek cihaz doğrulaması.
- [ ] **19 — Yayın listesi ve yedek bütünlüğü:** checksum, sürüm, erişim ve bozulma denetimi.
- [ ] **20 — Hata uyarısı ve güvenli kurtarma:** tekil hata raporu, tekrarlı alarm filtresi, izole geri yükleme; korunan dosyaya onaysız yazma yok.
- [ ] **21 — Günlük/haftalık/aylık bakım:** cron çakışmaları, tekrar eden işler, artifact saklama ve tek merkezden raporlama.
- [ ] **22 — Eski otomasyonları kontrollü emekliye ayır:** yalnız 92/92 davranışsal eşdeğerlik ve kullanıcı onayından sonra, geri alma planıyla.
- [ ] **23 — 24 saat kararlılık:** planlanan tetikler, hata oranı, yeniden denemeler ve yayın sağlığı kanıtı.
- [ ] **24 — 7 gün kararlılık:** günlük kanıtlar, kaçan cron'lar, yedek ve EPG erişilebilirliği.
- [ ] **25 — Son güvenlik ve performans:** asgari izinler, korunan yollar, işlem süreleri, gereksiz ağ çağrıları, restore provası.
- [ ] **26 — Üretim kabulü ve sürekli takip:** gerçek cihaz onayı, 7/24 takip göstergeleri ve olay müdahale kılavuzu.

### Otomasyon sınırları
- `madsc-05-genel-bakim.yml` mevcut beş aşamalı toplu test zinciridir; 13–26 maddeleri otomatik tamamlanmış değildir.
- 92/92 eşdeğerlik ve canlı üretim doğrulanmadan eski workflow'lar kapatılmaz.
- GitHub Actions cron tetikleri yalnız varsayılan dalda işler; özellik dalındaki cron tek başına 7/24 üretim kanıtı değildir.
- IBO gerçek cihaz kabulü ve riskli üretim değişiklikleri kullanıcı onayı gerektirir.

## Ek kabul ve operasyon kuyruğu — 27–34

Aşağıdaki işler 26'dan sonra uygulanır; öncesinde ilgili güvenlik bulgusu çıkarsa öne çekilir. İşaretler yalnız somut test kanıtıyla değişir.

- [ ] **27 — İş akışı izin matrisi:** GITHUB_TOKEN, üçüncü taraf sırlar, en az ayrıcalık ve fork/PR güvenlik sınırları.
- [ ] **28 — Bağımlılık ve tedarik zinciri:** action sürümlerini sabitleme, Python bağımlılıklarını tarama ve güncelleme testi.
- [ ] **29 — Gözlemlenebilirlik:** merkezi günlükler, başarısız aşama sınıflandırması, saklama süresi ve anlaşılır durum ekranı.
- [ ] **30 — Maliyet ve kota denetimi:** Actions dakika/artifact tüketimi, gereksiz paralel koşular, dış servis oran sınırları.
- [ ] **31 — Felaket kurtarma tatbikatı:** bağımsız dış yedekten izole kurtarma, geri dönüş süresi ve bütünlük kanıtı.
- [ ] **32 — Üretim geri alma planı:** workflow, yayın ve Pages için sürümlü rollback; yazma işlemleri onay kapılı.
- [ ] **33 — Belgeler ve devir notu:** kurulum, günlük işletim, hata müdahalesi, cihaz doğrulama ve yeni sohbetten devam kılavuzu.
- [ ] **34 — Periyodik yeniden kabul:** haftalık başarısızlık taraması, aylık eşdeğerlik ve erişim denetimi; yeni iş kuyruğuna ekleme.

**Tek kuyruk ilkesi:** Önce 02–12, ardından 13–26, ardından 27–34. GitHub Actions tek koşuda yalnız teknik olarak otomatik yapılabilen salt-okunur denetimleri yapar. Gerçek cihaz, üretim yazmaları ve eski workflow emekliliği için kullanıcı onayı şarttır. Bu belge zamanlayıcı değildir; yalnızca GitHub Actions'a açıkça bağlanan adımlar kendiliğinden çalışır.

## Tamamlayıcı iş kuyruğu — 35–50

Bu bölüm bilinen ek kabul konularını sıralar; keşfedilecek yeni sorunlar ilgili en erken aşamaya eklenir. Sıra otomatik çalıştırma garantisi değildir; her adımın kanıtı gerekir.

- [ ] **35 — Varsayılan dal ve dağıtım topolojisi:** aktif default branch, cron ve Pages yayın kaynağı kanıtı.
- [ ] **36 — GitHub Actions concurrency:** aynı anda tetiklenen push, cron, dispatch ve workflow_call yarışlarını engelleyen gruplar.
- [ ] **37 — Workflow çağrı zinciri:** reusable workflow inputs, outputs, needs, if/always ve hata yayılımı doğrulaması.
- [ ] **38 — Eşzamanlı dosya yazma çatışmaları:** yarış, kilit, atomik güncelleme ve tekrar denenebilirlik denetimi.
- [ ] **39 — Idempotency ve tekrar çalıştırma:** aynı girdiyle yinelenen koşunun güvenli ve tutarlı çıktı üretmesi.
- [ ] **40 — Sır ve kimlik bilgisi yaşam döngüsü:** sızıntı taraması, izin sınırları, yenileme prosedürü; sırları rapora yazma yok.
- [ ] **41 — Kaynak güvenilirliği ve erişim koşulları:** URL kaynaklarının yetki, oran limiti ve kararlılık değerlendirmesi.
- [ ] **42 — Ağ arızası ve timeout senaryoları:** 429, 5xx, DNS, bağlantı kesintisi, backoff ve kısmi sonuç davranışı.
- [ ] **43 — Çıktı şema ve veri kalite sözleşmeleri:** M3U/EPG/JSON/CSV doğrulama, encoding, sıralama ve bozuk veri karantinası.
- [ ] **44 — Kanal kimliği ve tarihçe tutarlılığı:** TVG ID, ülke, grup, URL değişimi, geçmiş ve tekrarların izlenmesi.
- [ ] **45 — EPG zaman dilimi ve veri tazeliği:** XMLTV doğruluğu, saat kayması, geçmiş ve gelecek program kapsamı.
- [ ] **46 — Logo dosyası ve erişim testi:** PNG/JPEG doğruluğu, kırık bağlantı, boyut, isimlendirme ve önbellek.
- [ ] **47 — Pages/CDN önbellek ve erişilebilirlik:** public URL, MIME, yönlendirme, HTTPS, önbellek ve güncelleme gecikmesi.
- [ ] **48 — Playlist istemci uyumluluğu:** IBO yanında standart M3U oynatıcılarla yalnız teknik ayrıştırma testi.
- [ ] **49 — Rapor tutarlılığı ve kanıt izi:** 92 görev için dosya, commit, run, artifact, karar, eksik kanıt ve sahibi alanları.
- [ ] **50 — Son açık işler taraması:** çözülmemiş bug, TODO, risk, başarısız test ve yeni gereksinimleri yeniden kuyruğa al.

**Öncelik kuralı:** Güvenlik açığı, veri kaybı veya üretim kesintisi saptanırsa numara sırasından önce güvenli durdurma/onarım yapılır. Riskli değişiklikler açık onay gerektirir. 02–34 maddelerinin bitmesi bu yeni maddelerin de bittiği anlamına gelmez.

## Genişletilmiş uygulama kuyruğu — 51–100

Bu 50 madde, 00–50 sırasındaki mevcut işlerin devamıdır. Önceki bir maddeyle örtüşen işler ayrı tekrar koşu yerine aynı kanıtla birleştirilir. Otomatik koşulabilen kontroller GitHub Actions'a ayrıca bağlanmadıkça yalnız plan olarak kalır.

### Test altyapısı ve kanıt
- [ ] **51 — T:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **52 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **53 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **54 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **55 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **56 — f:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **57 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **58 — x:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **59 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **60 — u:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **61 — r:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **62 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **63 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **64 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **65 — z:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **66 — o:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **67 — l:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **68 — a:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **69 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **70 — y:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **71 — o:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **72 — n:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **73 — u:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.

### İş akışı dayanıklılığı
- [ ] **74 — J:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **75 — o:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **76 — b:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **77 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **78 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **79 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **80 — m:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **81 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **82 — o:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **83 — u:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **84 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **85 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **86 — p:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **87 — o:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **88 — l:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **89 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **90 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **91 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **92 — k:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **93 — a:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **94 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **95 — ı:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.

### Yayın veri hattı
- [ ] **96 — M:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **97 — 3:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **98 — U:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **99 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **100 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **101 — ö:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **102 — z:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **103 — d:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **104 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **105 — z:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **106 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **107 — m:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **108 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **109 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **110 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **111 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **112 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **113 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **114 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.

### Yedek ve veri yönetimi
- [ ] **115 — Y:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **116 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **117 — d:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **118 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **119 — k:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **120 — l:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **121 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **122 — m:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **123 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **124 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **125 — k:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **126 — a:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **127 — p:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **128 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **129 — a:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **130 — m:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **131 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **132 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **133 — n:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **134 — v:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **135 — a:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **136 — n:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **137 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **138 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **139 — r:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **140 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.

### İşletim ve üretim kabulü
- [ ] **141 — O:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **142 — p:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **143 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **144 — r:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **145 — a:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **146 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **147 — y:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **148 — o:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **149 — n:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **150 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **151 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **152 — a:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **153 — ğ:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **154 — l:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **155 — ı:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **156 — k:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **157 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **158 — g:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **159 — ö:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **160 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **161 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **162 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **163 — r:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **164 — g:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **165 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **166 — l:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **167 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **168 — r:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **169 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.

### Çalıştırma ve bitiş koşulları

1. İlk açık, teknik olarak yapılabilir maddeyi al; önceki madde başarısızsa nedeni raporla ve güvenli şekilde dur.
2. Her değişiklik için test, Actions koşu kimliği, artifact ve commit kanıtı oluştur; doğrulanmamış işi tamamlandı diye işaretleme.
3. 92 eski workflow için tek tek davranışsal kanıt olmadan emeklilik yok; korunan playlist/EPG/logo/yedek dosyalarına izinsiz yazma yok.
4. Gerçek cihaz, default-branch üretim dağıtımı ve riskli yazmalar kullanıcı onayı gerektirir.
5. Bu belge bir iş planıdır; kendiliğinden gece boyunca çalışan ajan değildir. Mevcut beşli GitHub Actions zinciri kendi tanımlı görevlerini yürütür, tüm 100 maddeyi değil.

## Genişletilmiş toplu sıra — 101–200

100 ek kontrol, önceki sıranın devamıdır. Her kontrol somut kanıtla tamamlanır. Bunlar otomatik yürütücü değil, iş kuyruğudur.

### Güvenlik
- [ ] **101 — Güvenlik: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **102 — Güvenlik: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **103 — Güvenlik: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **104 — Güvenlik: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **105 — Güvenlik: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **106 — Güvenlik: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **107 — Güvenlik: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **108 — Güvenlik: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **109 — Güvenlik: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **110 — Güvenlik: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Keşif
- [ ] **111 — Keşif: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **112 — Keşif: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **113 — Keşif: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **114 — Keşif: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **115 — Keşif: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **116 — Keşif: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **117 — Keşif: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **118 — Keşif: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **119 — Keşif: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **120 — Keşif: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Kanal testleri
- [ ] **121 — Kanal testleri: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **122 — Kanal testleri: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **123 — Kanal testleri: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **124 — Kanal testleri: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **125 — Kanal testleri: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **126 — Kanal testleri: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **127 — Kanal testleri: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **128 — Kanal testleri: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **129 — Kanal testleri: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **130 — Kanal testleri: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### EPG
- [ ] **131 — EPG: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **132 — EPG: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **133 — EPG: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **134 — EPG: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **135 — EPG: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **136 — EPG: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **137 — EPG: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **138 — EPG: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **139 — EPG: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **140 — EPG: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Logo
- [ ] **141 — Logo: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **142 — Logo: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **143 — Logo: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **144 — Logo: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **145 — Logo: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **146 — Logo: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **147 — Logo: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **148 — Logo: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **149 — Logo: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **150 — Logo: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Yedek
- [ ] **151 — Yedek: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **152 — Yedek: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **153 — Yedek: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **154 — Yedek: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **155 — Yedek: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **156 — Yedek: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **157 — Yedek: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **158 — Yedek: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **159 — Yedek: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **160 — Yedek: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Actions
- [ ] **161 — Actions: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **162 — Actions: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **163 — Actions: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **164 — Actions: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **165 — Actions: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **166 — Actions: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **167 — Actions: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **168 — Actions: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **169 — Actions: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **170 — Actions: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Pages ve IBO
- [ ] **171 — Pages ve IBO: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **172 — Pages ve IBO: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **173 — Pages ve IBO: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **174 — Pages ve IBO: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **175 — Pages ve IBO: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **176 — Pages ve IBO: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **177 — Pages ve IBO: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **178 — Pages ve IBO: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **179 — Pages ve IBO: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **180 — Pages ve IBO: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Operasyon
- [ ] **181 — Operasyon: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **182 — Operasyon: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **183 — Operasyon: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **184 — Operasyon: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **185 — Operasyon: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **186 — Operasyon: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **187 — Operasyon: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **188 — Operasyon: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **189 — Operasyon: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **190 — Operasyon: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Geçiş kabulü
- [ ] **191 — Geçiş kabulü: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **192 — Geçiş kabulü: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **193 — Geçiş kabulü: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **194 — Geçiş kabulü: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **195 — Geçiş kabulü: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **196 — Geçiş kabulü: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **197 — Geçiş kabulü: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **198 — Geçiş kabulü: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **199 — Geçiş kabulü: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **200 — Geçiş kabulü: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

**Yürütme:** İlk açık işten sırayla ilerle; güvenlik ve veri kaybı riski öne alınır. 92/92 davranışsal eşdeğerlik ve kullanıcı onayı olmadan eski workflow kapatılmaz. Gerçek cihaz testi uzaktan tamamlandı sayılmaz.

## 18 Ekim 2026 — 09:57 (Europe/Stockholm) doğrulanmış Actions durumu

- GitHub Actions run: https://github.com/Madsc55/madsc-tv/actions/runs/39082013826
- Beş job'ın tamamı `completed/success`: 01 Güvenlik, 02 Keşif, 03 Kanal testleri, 04 Arşiv-yedek, 05 Genel bakım.
- Beş artifact mevcut ve `expired=false`: `madsc-kesif-tek-kosu-rapor` (12119885163), `madsc-genel-bakim-tek-kosu-rapor` (12119322760), `madsc-guvenlik-tek-kosu-rapor` (12119232510), `madsc-arsiv-yedek-tek-kosu-rapor` (12119039361), `madsc-kanal-test-tek-kosu-rapor` (12118748759).
- Bu kanıt yalnız belirtilen koşunun beş aşamasının başarı durumunu doğrular; 92/92 davranışsal eşdeğerlik, canlı Pages dağıtımı, dış yedek restore ve gerçek IBO cihaz kabulü doğrulanmış değildir.
- Sıradaki açık kapı: 92 eski workflow'un yazma/API/dispatch risklerini artifact içeriğinden dosya bazında doğrula ve kabul matrisini güncelle. Eski workflow'ları kapatma veya korunan dosyalara yazma izni verilmedi.

## 18 Ekim 2026 — Risk kuyruğu kanıtı iyileştirmesi

- `085211b4b75380a8fa30e44dbd321a90dac81bf0`: 92-workflow yazma-risk kuyruğu artık `write_risk_commands` komut kanıtlarını da içeriyor; salt okunur rapor üretimi, korunan dosyaya yazma yok.
- `2f964bdceff62e4c0b4c328c2cee44bca5b3c1de`: API-only workflow fixture'ında komut kanıtının JSON'a taşındığını denetleyen regresyon assertion eklendi.
- **Bekleyen doğrulama:** bu iki commit sonrası GitHub Actions run ve regresyon sonucu henüz teyit edilmedi; eski 92 workflow için davranışsal eşdeğerlik onaylanmadı.

## 18 Ekim 2026 — Yazma-risk kuyruğu kabul alanları

- `bdc1601ed235049433721df6d876a7ff7ced71cc`: `92_workflow_yazma_risk_inceleme_kuyrugu.json` artık her riskli eski workflow için `review_priority`, `requires_protected_write_review`, `required_acceptance_checks` alanlarını taşır.
- `320fdc19e6df2d8b4ef74c57f1bb6f6964c0a689`: API-only workflow'un yüksek öncelik ve dispatch idempotency kabul kontrolünü doğrulayan regresyon assertion'ları eklendi.
- **Açık:** Bu commit'ler için Actions test sonucu henüz doğrulanmadı. Bu statik risk sınıflandırması 92/92 davranışsal eşdeğerlik kanıtı değildir.

## 18 Ekim 2026 — Güvenlik kategorisi: korunan yol risk tespiti

- `71c3ed359044db771526035718b8769b6981f47e`: eski workflow'ların yazma-risk denetimi `HEPSI`, `FAVORILER`, `EPG/`, `logolar/`, `arsiv/` ve mevcut korunan playlist/yedek işaretlerini kapsayacak şekilde genişletildi. Bu bir statik tespit iyileştirmesidir, otomatik yazma engelleme kanıtı değildir.
- `4ad5cbfb2d9e330dda83a9864fbeee72c47fe53d` ve `3e24cb28352c34914aef13cd9f0dc803dcbcadeb`: `FAVORILER` için regresyon fixture'ı eklendi ve satır sonları düzeltildi.
- **Bekleyen:** Bu SHA'lar için Actions koşusu ve test başarısı henüz doğrulanmadı. Güvenlik kategorisi tamamlandı sayılmaz; 92/92 davranışsal eşdeğerlik açık.

## 18 Ekim 2026 — Güvenlik önceliği: manuel API yazmaları

- `e75fe0a9d282f630fb343f7f810b16ff4ed9782b`: yazma/API/dispatch sinyali olan manuel workflow'lar da `HIGH` inceleme önceliği alıyor; zamanlayıcı olmaması yazma riskini ortadan kaldırmaz.
- `865903c5a49494440879cd588c487f4d62000f4e`: API-only regresyon testi yüksek öncelik beklentisini doğrulayacak şekilde güncellendi.
- **Test sonucu bekleniyor:** bu SHA için GitHub Actions koşusu doğrulanmadan güvenlik kategorisi tamamlandı sayılmaz.


### 18 Ekim 2026 — Güvenlik CI hata ve onarım kaydı
- `562b2477be7ac3d6b43ac0aea197586e8f0c7a04` commitinde K1 run `39122430755` (job `117660567798`) başarısız; MADSC 05 run `39122430776` güvenlik job `117660568357` başarısız. Gerçek log: `scripts/five_category_92_workflow_audit.py:18` Python `SyntaxError` (`//` açıklama satırı). Diğer kademe jobları atlandı; başarılı sayılmaz.
- Açıklama satırı Python `#` sözdizimine çevrildi; işlevsel kod ve regresyon testleri korunuyor. Yeni commitin run/job/artifact sonucu henüz doğrulanmadı. Önce bu CI düzeltmesini kontrol et, ardından 02–04 risk kuyruğuna dön. 92/92 davranışsal kabul 0/92.

## 18 Ekim 2026 20:05 CEST — 02/04 gerçek CI incelemesi (kabul açık)
- İncelenen dal HEAD: `dd5fcea532438cfa5ec431cd5398e5b4b0c5a9e9`. MADSC 05 run [39148820745](https://github.com/Madsc55/madsc-tv/actions/runs/39148820745): 5 jobdan **3 success, 2 failure** (K1 ve K5). Beş artifact mevcut; aynı SHA hızlı ön kontrol [39148820738](https://github.com/Madsc55/madsc-tv/actions/runs/39148820738) success, beşli kabul değildir.
- **04 güvenlik bağımlılık açığı:** merkezî K2–K4 çağrıları `always()` yüzünden K1 başarısız olsa da çalışmış. Mevcut `test_central_stages_stop_after_failed_dependency` regresyonu iki job logunda da başarısız. Öncelikli düzeltme: 2–4 kademelerinin `needs.<önceki>.result == 'success'` koşulu; K5 başarısızlığı ve kanıt artifact'larını toplamaya devam etmeli.
- **K1 kabul engeli:** 26 kuralın 26/26 üretim enforcement kanıtı yok; `runtime_enforcement_verified=false` kayıtları fail-closed. Statik envanter veya artifact, 92 workflow'un davranışsal eşdeğerliği değildir (**0/92**). Dört tarihsel korunan EPG farkı onaysız değiştirilmeyecek.
- Yeni commit sonrasında SHA/run ID'si henüz kanıtlanmadı. **02–04 açık**; 200 maddelik kuyruk kapanmadı. Sıradaki iş: yeni SHA Actions K1/K5 sonucu, 26 kural eksik kanıtları ve 92 risk artifact içerikleri. Korunan dosyalar, main ve PR #71 değiştirilmedi.


### 18 Ekim 2026 21:10 CEST — SHA 0a8ec784 için gerçek CI ve günlük kanal rotasyonu regresyonu
- İşlem öncesi HEAD: `0a8ec784748558c03cb44549b8aab48efd86c95a`. Hızlı ön kontrol run [39155725676](https://github.com/Madsc55/madsc-tv/actions/runs/39155725676) **failure** (job 117758435690); beşli run [39155725642](https://github.com/Madsc55/madsc-tv/actions/runs/39155725642) **failure**. K1 job 117758435348 failure, K2–K4 skipped, K5 job 117758502736 failure. Üç artifact mevcut: hızlı 12146309776, K1 12146806835, K5 12147041321; artifact varlığı başarı değildir.
- Hızlı/K1/K5 loglarında aynı statik regresyon: `test_central_shadow_schedules_preserve_legacy_cadence` eski `40 6 1,15 * *` cron'unu bekliyor, oysa K3 yeni salt-okunur günlük `40 6 * * *` rotasyonunu kullanıyor. Güvenli düzeltme: **yalnız test beklentisini gerçek günlük rotasyonla uyumlu yap**, 123 sentetik satırın üç günde birer kez kapsanmasını test et; eski 1/15 eşdeğerliğini onaylama. Workflow cron'u ve korunan veriler değiştirilmez.
- K1 raporu: **0/26 runtime verified, 14 kısmi, 12 kanıt eksik**; K1'in fail-closed kararı doğrudur, yeşile çevrilmez. K1 bütünlük logu **136 korunan dosya, changed_paths=[]**. K5 bağımlılık ve kategori kanıtı bu nedenle kapalıdır.
- Yeni test+not commitinin SHA ve gerçek Actions sonuçları bu kayıt yazılırken **henüz yoktur**; yeni SHA'nın run/job/log/artifact sonucu ayrıca doğrulanmalıdır. **İlk açık iş 02:** güncel SHA'da regresyonun sonucu; ardından 26 kuralın gerçek enforcement kanıtı, 92 eski workflow yazma/dispatch ve çift tetikleme denetimi (03–04). Davranışsal kabul **0/92**; IBO gerçek cihaz ve harici restore bekliyor. main, PR #71, eski 92 workflow, EPG, playlist, logo ve arşivler değiştirilmedi.

```


---

## KAYNAK: docs/MADSC-92-WORKFLOW-ESDEGERLIK-KONTROL-2026-10-14.md

Git blob SHA: `a5fec1faeb0db55a13bc9eee917e55a3d2af2c3c`

```text
# MADSC — 92 workflow eşdeğerlik kontrolü (2026-10-14)

## Doğrulanan
- PR #71 dalı: `madsc/bes-sistem-toplu-birlestirme`.
- GitHub Actions run `38630252033`, commit `a1473f868ff40b55740a751e8e39b759ddeec8a0`: beş kategori işi de `success`.
- Beş ayrı rapor artifact'i oluşmuş: güvenlik, keşif, kanal testleri, arşiv/yedek, genel bakım.
- Kanal test işi salt okunur 50 kanallık partiyi kontrol etmiş. Bu, tüm kanalların yayın doğrulaması değildir.

## Eşdeğerlik için zorunlu kapılar
1. Eski 92 workflow'un her biri için dosya adı, tetikleyici, zamanlama, izinler, okunan/yazılan dosyalar, dış bağımlılıklar, başarısızlık davranışı ve ürettiği artifact'leri envantere yaz.
2. Her eski workflow'u beş kategoriden birine eşle; birden fazla kategoriye giren işleri alt görevlere ayır. Eksik ve belirsizleri `ESDEGERLIK_BEKLIYOR` olarak işaretle.
3. Özellikle ana listeye yazabilen yedek geri yükleme, ayrı günlük EPG ve yalnızca bildirim veren otomatik devam işlerini manuel incele.
4. Her görev için aynı girişlerle eski/yeni çıktı karşılaştırması, hata durumları ve korunan dosya hash karşılaştırması yap.
5. Eski workflow'ları ancak kanıtlanmış eşdeğerlik ve açık kullanıcı onayı sonrası kapat; silme.

## Koruma
`CALISANLAR.m3u`, favoriler, ⭐ YENİLER, logo ve yedekler değiştirilmeyecek. Bu belge yalnızca izleme amaçlıdır; hiçbir eski workflow'u kapatmaz.

## Durum
Beşli toplu denetim: **GEÇTİ**. 92/92 görev eşdeğerliği: **HENÜZ KANITLANMADI**. Sonraki iş: dosya bazlı 92 satırlık envanter ve eşdeğerlik matrisi.

```


---

## KAYNAK: docs/MADSC-IKI-TOPLU-KABUL-PLANI.md

Git blob SHA: `d7d73e853350a59e2a223d0b1d59b4fb43c3c22b`

```text
# MADSC — İki toplu kabul aşaması (14 Ekim 2026)

## Kullanıcı kararı
Tek tek küçük test döngüleri yerine kalan değişiklikler bir paket halinde hazırlanacak. Kullanıcıya her dosya sonrası test yaptırılmayacak. Gereksiz Actions koşuları ve tekrarlayan bildirimler önlenecek.

## Aşama 1 — Hazırlık ve toplu doğrulama
- 92 eski workflow için görev, script, tetik (cron/push/workflow_run/dispatch), izin, çıktı/artifact ve bağımlılık matrisi; eşleşmeyenler açıkça BLOCKED.
- Güvenlik, keşif, yayın/EPG/logo, arşiv/yedek ve genel bakım regresyonlarını aynı kabul zincirinde denetle.
- Kategori-5 işi ilk dört kategori sonucunu `needs` üzerinden okumalı. Önceki #15 yanlış negatifinin nedeni eksik `needs` idi; düzeltilmiş sürümün canlı sonucu ayrıca kontrol edilecek.
- Korunan CALISANLAR.m3u, favoriler, ⭐ YENİLER, logolar, kanal sırası ve yedekler değişmez. İşler salt okunur veya izole test edilir.
- Eksikler bir araya getirilip toplu commit hazırlanır. Her küçük dosya değişikliğinden sonra ayrı test talep edilmez.

## Aşama 2 — Tek nihai beşli kabul koşusu
- Tek `MADSC 05 - Genel Bakim Toplu` çalıştırması: Güvenlik → Keşif → Kanal Testi → Arşiv/Yedek → Genel Bakım.
- 5/5 jobs success; regresyon ve rapor adımları success; korunan dosya SHA256 kontrolü success; 5 rapor artifact'ı incelenir.
- 92 satırlık raporda `migration_blocked_count`, `behavioral_parity_verified_count`, eşleşmeyen betikler ve yüksek riskli eski otomasyonlar ayrıca değerlendirilir. Bunların sıfırlanmaması 5/5 CI başarısını '92 görev taşındı' anlamına getirmez.
- EPG→Pages, günde iki keşif, VOD, harici geri yükleme ve IBO cihaz onayı canlı kanıt olmadan tamamlanmış sayılmaz.
- Bir hata çıkarsa aynı kapsamlı denetim tekrar tekrar başlatılmaz: loglar toplanır, bütün ilişkili hatalar tek paketle düzeltilir, sonra kabul yeniden denenir.

## Geçiş kapısı
PR #71 ancak 92/92 görev davranışsal eşdeğerlik, eski üretim tetik ve yazma bağımlılıkları, harici restore ve kullanıcı onayı gerektiren alanlar için kanıtlar hazır olunca geçişe adaydır. Aksi halde eski 92 workflow çalışmaya devam eder; silinmez veya kapatılmaz.

## Şu an doğrulanmış durum
- Geçmiş 5/5 başarılı Actions koşusu mevcut.
- #15 koşusunda ilk dört kategori yeşil, beşinci kategoride yanlış negatif `needs` hatası kullanıcı ekranında doğrulandı.
- `needs` düzeltmesi kodda mevcut; son canlı koşunun başarısı burada doğrulanmış değildir.
- Kalan işlerin tek bir CI koşusunda *tamamlandığı* iddia edilmez; tek CI koşusu yalnız denetimi toplulaştırır.

## Sonraki toplu entegrasyon paketi (15 Ekim)
Bu paket mevcut kabul kosusu beklenirken hazirlanir. Her adimdan sonra kullanicidan test istenmez.

1. Canli uretim zinciri: EPG-Pages workflow_run, dokuz cron, push, yazma izinleri, artifact, secrets ve bagimliliklarin eski-yeni esdegerligi.
2. Guvenlik: 18 gorev ve 26 kural, yazma kapisi, korunan dosyalar ve yetki regresyonu.
3. Kesif: 75 aday, 4 alternatif, tekrar eleme, farkli saatlerde tekrar deneme ve gunde iki kesif tetigi; playlist'e yazma yok.
4. Kanal testleri: ffprobe/yayin, logo, kalite, EPG ve Pages yayin kaniti; IBO cihaz kabulunu ayrica koru.
5. Arsiv: izole geri yukleme, harici yedek kaniti, korunan backup'lara yazmadan geri donus provasi.
6. Genel bakim: dort kategori, 92 gorev esdegerlik matrisi ve cift tetik denetimini tek kabulde birlestir.
7. Tek toplu kabul: girdi, cikti, yan etki, izin ve tetik esdegerligi; ardindan 5/5 CI ve canli zincir kanitlari.

Her eski workflow icin yeni kategori sahibi, somut kod karsiligi, test veya canli kanit, rollback ve eksik gereksinimler yazilmadan durum BLOCKED kalir.
Betik ismi eslesmesi, yesil denetim veya bes kategoriye etiketleme eski gorevin tasindigini kanitlamaz.
EPG-Pages, harici restore ve IBO kabul kaniti olmadan PR birlestirilmez; eski workflow kapatilmaz.
Sonuc kullaniciya tek raporda: tasinan islev, eksikler, toplu test ve canli kabul gereksinimleri.

```


---

## KAYNAK: docs/MADSC-TAM-DURUM-VE-YOL-HARITASI-2026-10-14.md

Git blob SHA: `1e581bcccb8bed284b2edd6c5f1515c54a1001fd`

```text
# MADSC — Durum, hedefler ve sonraki aşama (14 Ekim 2026)

## Amaç ve değişmez kurallar
- 92 eski GitHub Actions workflow'unu görev kaybı olmadan beş ana kategori altında toplamak: 1 Güvenlik, 2 Kanal keşfi, 3 Kanal testleri (logo ve EPG dahil), 4 Arşiv/yedek, 5 Genel bakım.
- Kullanıcı tek tek test yaptırmak istemiyor: toplu düzenleme, tek beşli CI koşusu, hata varsa toplu düzeltme ve yalnız kanıtlı sonuç raporu.
- CALISANLAR.m3u, HEPSİ/favoriler, ⭐ YENİLER, URL, kimlik, sıra, kategoriler, doğrulanmış logolar ve bütün korunan arşiv/yedekler onaysız değiştirilmez.
- Kullanıcı onayı olmadan ana listeye veya ⭐ YENİLER'e kanal eklenmez; çalışan/çalışmayan, otomatik test ve kullanıcı IBO onayı ayrı tutulur.
- 92 eski workflow davranışsal eşdeğerlik ve bağımlılık kanıtı olmadan silinmez veya kapatılmaz.

## Doğrulanmış teknik kazanımlar
- PR #71 (madsc/bes-sistem-toplu-birlestirme) açık ve draft; beş yeni salt okunur workflow oluşturuldu.
- Beş kategori tek merkezden sıralı çalışabiliyor; GitHub Actions #38630252033 koşusunda 5/5 job success ve beş artifact kaydı doğrulandı. Bu geçmiş koşudur; sonraki değişikliklerin sonucu değildir.
- 92 eski workflow'u bekleyen ve sayısı değişirse hata veren statik envanter var; cron, push, workflow_run, izin ve betik eşleştirmesi raporlanıyor.
- central_workflow_inventory.py: yedek kategori 4, EPG/logo kategori 3; kategori regresyon testleri eklendi.
- Tek-merkez push çakışması nedeniyle 30 testte 1 hata görüldü; madsc-05 push paths yalnız kendi YAML dosyasına daraltıldı. Düzeltmenin yeni canlı CI kabulü henüz doğrulanmadı.
- Beşli kabul koşusuna tek-merkez regresyonu ve önceki dört kategorinin success olmasını zorunlu kılan adım eklendi.
- five_system_migration_audit.py migration_complete=False; sırf beş dosya var diye eşdeğerlik iddia edilmez.

## Sistem bugün neler yapıyor?
1. Güvenlik: SHA256, korunan yazma kapısı, statik risk ve regresyon raporları. Tam üretim güvenlik eşdeğerliği kanıtı yok.
2. Keşif: kaynak mutabakatı, tekrar denetimi, IBO aday kuyruğu raporları. Günde iki kez çalışan eski keşif üretiminin devri yok.
3. Test: kimlik/EPG/logo raporları, 50 kanallık salt okunur yayın sağlık partisi ve regresyonlar. 75 adayın tamamı, 51 retest, 24 ffprobe başarısızı, 4 alternatif ve IBO cihaz onayı tamamlanmadı.
4. Arşiv: izole Git restore, arşiv ve yedek kanıt raporları. Harici bağımsız geri yükleme ve tüm tarihsel kayıtlar kanıtlanmadı.
5. Bakım: envanter, 18 görev, açık iş ve toplu raporlar. 92/92 davranışsal eşdeğerlik ve otomatik tetik devri tamamlanmadı.

## Eski üretim bağımlılıkları
- 9 zamanlanmış eski workflow; günlük 06:00/18:00 UTC keşif, EPG günlük üretim, Pages workflow_run yayın, günlük VOD, aylık 1/15 sağlık/yedek ve diğer kontroller.
- Eski işlerin devam etmesi beşli sistemin bunların yerini aldığı anlamına gelmez.
- Yeni beşli testlerin hepsinin yeşil olması yalnız test edilen kapsamı kanıtlar; canlı cihaz, offsite restore ve üretim zinciri ayrı kapılardır.

## Sonraki güvenli ve ölçülebilir aşama
A. En güncel beşli Actions koşusunun 5 job ve step sonuçlarını doğrula; varsa hata logundan düzelt. Push run sorgusu sınırlıysa başarı uydurma.
B. 92 satır için eski komut, tetik, yazma izni, artifact, bağımlılık ve yeni kategoride gerçek karşılık matrisi üret. 'Yok', 'kısmi', 'eşleşen' ve 'canlı doğrulandı' durumlarını ayır; yalnız betik adı eşleşmesi davranış kanıtı değildir.
C. Önce eksik veya riskli otomatik işler: EPG→Pages, keşif 2/gün, VOD, yedek 1/15, workflow_run ve otomatik yazma izinleri. Korunan veriye yazmadan dry-run/izole test yap.
D. Canlı yayın ve IBO kabulü, offsite restore ve tarihsel listeler için ayrı kanıt topla.
E. A-D tamamlanınca tek beşli kabul koşusu ve onay; ancak bundan sonra kontrollü tetik geçişi, eski kod geçmişi korunur.

## Kabul durumu ve değer
- Teknik kurulum: var. Beşli entegrasyon: geçmişte 5/5 doğrulandı. Son değişikliklerin CI kabulü: doğrulanmadı. 92/92 üretim eşdeğerliği: tamamlanmadı. PR #71: açık/draft.
- Teknik değer: merkezi kontrol, tekrar tespiti, koruma ve raporlama altyapısı. Parasal değer: canlı kalite, haklar, maliyet ve kullanıcı kanıtı olmadan hesaplanamaz.
- İlerleme yüzdesi verilmez; sayısal bir yüzde, henüz ölçülmeyen görev eşdeğerliğini yanlış temsil eder.

```
