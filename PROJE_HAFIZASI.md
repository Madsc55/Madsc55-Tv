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
