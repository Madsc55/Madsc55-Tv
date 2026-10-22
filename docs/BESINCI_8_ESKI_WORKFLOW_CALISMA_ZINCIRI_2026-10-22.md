# Beşinci kaynak çözümlemesi: sekiz eski workflow (48/99)

Sabit kaynak: `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`. Sekiz YAML'ın tam metni okundu. Yalnızca YAML düzeyi statik incelemedir; betiklerin tüm yan etkileri ve gerçek eşdeğerlik henüz doğrulanmadı.

| Workflow | K adayı | Tetikleme | Gözlenen çalışma zinciri ve kanıt | Kabul boşluğu |
|---|---|---|---|---|
| `aday-yedekleme.yml` | K3/K4 | Manuel + `.github/commands/aday-yedekleme.txt` değişiminde main push | `GH_TOKEN` ile `yedekler/teknik_adaylari_aktar.py`; her durumda `ONAY-BEKLEYEN-TEKNIK-ADAYLAR` artifact; 30 dk | Scriptin API okuması ve M3U çıktısı, ana listeye yazmama kanıtı |
| `akilli-aday-puanlama.yml` | K2/K3 | Manuel + betik/YAML push | ffmpeg; sınırsız tarama (`SCAN_BATCH=-1`); gerçek ffprobe; puanlama; 4 dosyalı `AKILLI-ADAY-PUANLAMA` artifact, 30 gün; 55 dk | Gerçek teknik kanıt, kaynak/puan eşlemesi ve dört artifact |
| `altinci-aday-tekrar-test.yml` | K3 | Manuel + üç dosya push | Mock HLS/video testleri; ffmpeg; `RETEST_LIMIT=5` gerçek tekrar testi; `altinci-gelistirme-tekrar-test-raporu` artifact; 20 dk | Başarılı test sayısı 2 olduğunda ret; HLS hata halinde `TEKRAR_TEST_BEKLIYOR` semantiği; gerçek yayın ölçümü |
| `automatic-png-logos.yml` | K1/K3 | Sadece manuel | Pillow/cairosvg; logo audit/PNG; ffmpeg görsel kanıtı; iki artifact; korunan `CALISANLAR.m3u` değişimini restore et, staged fark varsa hata; 15 dk | Ana liste hash ve staged koruma; logo dosyaları ve kareler; gerçek görsel inceleme |
| `besinci-zaman-asimi-test.yml` | K3 | Manuel + YAML/medya betiği push | `subprocess.TimeoutExpired(timeout=65)` mock; `BELIRSIZ/BELIRSIZ`, `TEKRAR_TEST_BEKLIYOR` beklenir; bozuk kabul edilmez | Timeout sınıflaması ve 65 saniye argümanı için test eşdeğerliği |
| `birlesik-aday-raporu.yml` | K2/K3 | Manuel + iki dosya push | Önce `KARARLILIK_GECMISI.json` cache restore; ffmpeg; sınırsız tarama; öncelikli+genel ffprobe; puanlama; kararlılık; birleşik onay raporu; dört dosyalı artifact; 60 dk | Cache kökeni, uzunlamasına ölçüm, onay semantiği ve hata durumunda artifact politikası |
| `birlesik-durum-raporu.yml` | K2/K5 | Manuel + üç dosya main push | Python 3.11; salt okunur durum, eksik Türk kanalı, 155 kaynak envanteri, haftalık bakım; dört JSON artifact; 5 dk | Gerçek 155 kaynak kapsaması; bakım raporu; yayın testi başlatmama |
| `dokuzuncu-akilli-tekrar-test.yml` | K3 | Manuel + takvim/test/YAML push | `python3 -m unittest -v test_akilli_tekrar_test_takvimi.py` | Zamanlama testlerinin kod içeriği ve regresyon sonucu |

## Kritik kararlar

- `automatic-png-logos` üretim ana listesini korumaya çalışır ama **çalışma dizinindeki** değişikliği geri alır; başka yazma noktaları ayrıca denetlenmelidir.
- `birlesik-aday-raporu` ile `akilli-aday-puanlama` sadece rapor üretmez; gerçek ffprobe ve sınırsız tarama çalıştırır. K2/K3'te açık ağ izni gerektirir.
- `aday-yedekleme` adında yedek geçse de kanıtlanan davranış teknik aday M3U taslağını artifact olarak saklamaktır; harici geri yüklenebilir yedek kanıtı değildir.
- `besinci-zaman-asimi-test` gerçek 65 saniyelik ağ timeout testi değil, mock birim testidir.

**Toplam ayrıntılı YAML çözümlemesi: 48/99 (%48,5). Kalan: 51.** Davranışsal kabul **0/92**, güvenlik üretim kabulü **0/26**. Üretim yazımı veya Actions çalıştırması yapılmadı.
