# K3 — Yeni sohbet devir notu (23 Ekim 2026)

## Hedef ve değişmez sıra
MADSC55-TV beşli sisteminin K3 kolu: (1) gerçek canlı kanal ölçümü, (2) 75 adayın tekrarlı HLS erişim kanıtı, (3) video+ses ffprobe kanıtı, (4) XMLTV/EPG kimlik eşleşmesi ve GitHub Pages erişim kanıtı, (5) **IBO Player Pro gerçek cihaz testi EN SON**. Diğer K1/K2/K4/K5 sohbetleri aynı main dalına eşzamanlı yazıyor.

## Depolar ve korunacaklar
- Ana depo: https://github.com/Madsc55/Madsc55-Tv ; dal main.
- Tarihsel EPG/Pages deposu: https://github.com/Madsc55/madsc-tv ; salt okunur incele; EPG kaynağı epg/madsc-epg.xml ve yayın hedefi madsc-epg.xml olarak raporlandı, **canlı erişim doğrulanmadı**.
- Üretim CALISANLAR.m3u ve diğer playlist, EPG, logo, favori, arşiv, yedekleri değiştirme. PR #71'i birleştirme. Her GitHub dosya güncellemesinden hemen önce güncel blob SHA çek. Çakışmada yeniden oku, körlemesine yazma.
- K1/K2/K4/K5'in durumunu K3 sonucundan çıkarsama.

## Gerçekte main dalına gönderilen K3 geliştirmeleri
1. `madsc/epg.py` M3U başlık sırası güvenliği ve `tests/test_epg.py` testi (65ba9da4, 09d297a6).
2. `madsc/trial_epg_matching.py` XMLTV NUL reddi ve testi (e59a1ee2, cd963633).
3. `madsc/k3_turkish_tv_video_pilot.py`: HTTPS same-origin HLS, fragment/boşluk/port/kimlik bilgisi kontrolü, ham variant ve segment URI'larını URL normalleştirmesinden önce denetleme, bozuk UTF-8, NUL ve Unicode satır ayıracı reddi. Testler `tests/test_k3_hls_origin_regression.py` (977c4a02, c7282170, daade279, df85f36d, d6f61578, 3b0fe2b7, 9199e54f, eaec986d, 3b1a2417, adb6cf63, 5f15af35, 269a9305).
4. `madsc/k3_live_manifest_pilot.py`: varsayılan 12, izin verilen üst sınır 75, CLI `--limit 75`, ölçüm UTC zamanı, istenen aday ve eksik aday sayısı raporlanıyor. `.github/workflows/madsc-k3-live-manifest-pilot.yml` manuel 12/75 seçimi, 25 dakika sınırı. `tests/test_k3_manifest_limit.py` limit ve rapor testleri (04183e25, 985cbe4d, 8d857c24, 3f082805, 64837696).
5. `madsc/k3_acceptance_evidence.py`: 3 farklı JSON ölçümünü, 75 benzersiz SHA256 kimliğini, 6 saat aralığını, 75 manifest sonucunu ve çelişkili başarı kayıtlarını denetler; **full_k3_acceptance=False** bırakılır. `tests/test_k3_acceptance_evidence.py` geçerli/eksik/çelişkili veri testleri (8567c185, f01176e3, 47ef7b9e, 147dd570).
6. Video/ses pilotu workflow `.github/workflows/madsc-k3-turkish-tv-video.yml` mevcut; `ffprobe` ile en fazla 12 aday kontrol edebilir. Video/ses testi **gerçekten çalıştırılmış veya başarıyla kanıtlanmış değil**.

## Açık ve kritik eksikler
- 75 adaylık canlı pilotun gerçekten GitHub Actions'ta başlatılması, JSON artifact indirilmesi, kaç manifest erişildiğinin ölçülmesi.
- 3 ayrı 75 adaylık raporun ilk/son arasında >=6 saat olacak şekilde alınması ve `python -m madsc.k3_acceptance_evidence rapor1.json rapor2.json rapor3.json` ile doğrulanması. **Mevcut kod sadece manifest doğrular; yayın video+ses kabulü değildir.** Aynı 75 URL hash'i her raporda bulunmalı.
- Gerçek `ffprobe` video ve ses kanıtları; mevcut video pilotu en fazla 12 aday.
- Gerçek XMLTV tvg-id/kanal/programme kapsamı, logo kimlikleri, eski EPG kaynağı -> Pages dağıtım zinciri ve yayımlanmış URL'nin HTTP/XMLTV doğrulaması.
- Son commit'in gerçek CI sonuçları ve başarısız/durdurulmuş Actions işlerindeki hataların incelenmesi. `get_commit_combined_status` boş dönmüştü; **boş = başarılı değil**. GitHub bağlayıcısında workflow_dispatch aracı bulunmadı; manuel çalıştırmayı yapılmış gibi yazma.
- **En son** IBO Player Pro gerçek cihaz kabulü (kullanıcının cihazında); kanıt olmadan onay verme.

## Son doğrulama
23 Ekim'de GitHub commit aramasıyla main'de diğer kolların eşzamanlı commit'leri görüldü; örnek son görülen SHA `8884b1c6fa1a66c0996a1cd6ecc4254eec044869` (sadece anlık görüntü, gelecekte yeniden oku). Son K3 commit `147dd57054f03adb1c8579171c755cfda0921a4e` (çelişkili manifest başarı testleri). Test kodları GitHub'a gönderildi, **bu oturumda CI veya canlı pilot başarısı doğrulanmadı**.

## Yeni sohbet için öncelik sırası
1. Main'in güncel commit'ini ve CI/Actions sonuçlarını kontrol et; test hatası varsa gerçekten düzelt.
2. K3 kabul denetimi ve testlerini çalıştır; test verilerinin doğru olduğundan emin ol.
3. 75 canlı adayın zaman aralıklı ölçümlerini başlat/kanıtla; başlatamıyorsan bunu açıkça bildir.
4. Video/ses kanıtını topla; 12 pilotun 75'i kanıtlamadığını unutma.
5. EPG XMLTV eşleşmesi, Pages gerçek URL ve logo denetimi.
6. IBO Player Pro cihaz testini son aşamaya bırak.
7. Kanıtsız yüzdelik veya tamamlandı iddiasında bulunma.

## Yeni sohbete yapıştırılacak komut
"Madsc55/Madsc55-Tv main dalındaki docs/K3_YENI_SOHBET_DEVIR_2026-10-23.md dosyasını oku. K3'e kaldığımız yerden devam et. Önce güncel CI ve testleri kontrol et; sonra 75 kanal canlı kanıtları, 6 saatlik 3 ölçüm, ffprobe video/ses, XMLTV/EPG ve Pages zincirini gerçekten doğrula. Eksik/hatalı kodu güvenli şekilde düzelt, commit et, kanıtla. IBO Player Pro cihaz testini en sona bırak. Üretim dosyalarına dokunma, K1/K2/K4/K5 eşzamanlı çalışıyor."
