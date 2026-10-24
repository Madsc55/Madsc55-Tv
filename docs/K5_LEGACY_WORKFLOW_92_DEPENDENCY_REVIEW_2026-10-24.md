# K5 — Eski workflow #92 tam bağımlılık incelemesi (2026-10-24)

**Sabit kaynak:** `Madsc55/madsc-tv@ca374df3b9585c0d76a078db9536150ebbc260f7`

**Workflow:** `.github/workflows/yeniler-guvenli-arama.yml`

Bu not, ilk YAML incelemesine ek olarak doğrudan iki Python giriş dosyasının kaynak başlıklarını ve workflow'un tüm YAML içeriğini kontrol eder. Tam davranışsal eşdeğerlik veya yürütme kabulü değildir.

## Yürütme sözleşmesi

- Tetikleyiciler: elle `workflow_dispatch`; `main` dalında `.github/commands/genel-guncelleme.txt` değişiminde push.
- Yetki: `contents: read`; iki job'da `actions/checkout@v4` ve `persist-credentials: false`.
- `kaynak-kesfi`: 20 dakika üst sınır, `GITHUB_TOKEN` ile `python3 kaynak_kesfet.py`; `YENI_KAYNAK_ONERILERI.csv` ve `KAYNAK_KESIF_HATALARI.txt` artifact'leri.
- `yeni-kanal-tara`: keşif job'una bağlı; `SCAN_BATCH` matrisi 34–99 (66 batch); her job 35 dakika; ffmpeg kurulumu, önceki artifact indirme, `python3 yeni_kanal_tara.py` ve batch başına `YENILER-KANAL-ADAYLARI-GRUP-<batch>` artifact'i.
- `if-no-files-found: error`, artifact saklama süresi 30 gün.

## Kaynak dosyalarında gözlenen bağımlılıklar

- `kaynak_kesfet.py`: `urllib.request` ve GitHub API ile depo/playlist kaynağı keşfi; zaman aşımı 12 saniye; `MAX_REPOS=60`, `MAX_SOURCES=120`, `MAX_AGE_DAYS=90`; `yeni_kanal_tara.py` dosyasını okur. Ağ erişimi ve güncel zaman sonuçları etkiler.
- `yeni_kanal_tara.py`: `channel_name_normalization.normalize_channel_name` ve `discovery_m3u_parser.parse_discovery_m3u` modüllerini içe aktarır; kaynak M3U URL listesi ve `YENI_KAYNAK_ONERILERI.csv` girdisi kullanır; subprocess, urllib ve zaman ölçümleri mevcuttur. Çalışma ağ/medya koşullarına bağımlıdır.

## Kabul engelleri

1. İki Python giriş dosyasının tamamı bu incelemede okundu; dolaylı modüller (`channel_name_normalization`, `discovery_m3u_parser`) ve yeni sistem karşılığı için ayrı tam çağrı grafiği hâlâ gerekli.
2. 66 batch'in her biri için ağ çağrıları, ffprobe alt süreçleri, zaman aşımı ve çıktı/artifact deterministik fixture'larla izole edilmeli.
3. Değişken dış GitHub API ve canlı medya yanıtları sabitlenmeden eski/yeni SHA256 kanıtları karşılaştırılamaz.
4. Keşfedilen M3U adresi tek başına yayın hakkı veya kullanım izni kanıtı değildir; kaynak doğrulaması ayrı yapılmalı.
5. İki bağımsız yürütmenin gerçek logları, hash'leri, side-effect manifestleri ve korunan dosya değişmezliği doğrulanmadı.

**Kabul sonucu: BLOCKED; bağımsız davranışsal kabul sayısı değişmedi (0/92).** Üretim taraması veya liste yazımı yapılmadı.

## Tam Python giriş dosyası incelemesi — ek bulgular

- `kaynak_kesfet.py`: GitHub repository search, tree ve commits API çağrıları yapar; indirilen M3U içeriğini `#EXTM3U` ve `#EXTINF` üzerinden sayar. Güncellik kontrolü başarısız kaynakları eler; `YENI_KAYNAK_ONERILERI.csv` ve `KAYNAK_KESIF_HATALARI.txt` yazar. Önerileri otomatik ana listeye eklemez.
- `yeni_kanal_tara.py`: `CALISANLAR.m3u` dosyasını **okur**; 30 kayıt/batch kotası uygular; `BATCH*30 <= index < (BATCH+1)*30` aralığındaki `.m3u8` URL'lerine `hls_probe` uygular. En az iki segment indirildiyse `ffprobe` çalıştırır (22 saniye subprocess timeout). Kanal kimliği doğrulanmaz.
- Yazılan dosyalar: `aday_bekletme/HAM_ADAY_KAYNAKLARI.csv`, `YENILER_TARAMA_RAPORU.csv`, `YENILER_KAYNAK_HATALARI.txt`; ilk job'un keşif CSV ve hata dosyaları. **Ana listeye doğrudan yazma gözlenmedi.**
- **Kapsam riski:** 66 batch × 30 = 1.980 indeks (1.021–3.000); sıralanmış aday sayısı bunun üzerinde ise bu workflow tek başına hepsini test etmez. Her batch tüm kaynakları yeniden indirip tüm adaylar için rapor oluşturduğundan yüksek ağ yükü ve yinelenen veri oluşabilir.
- **Güvenlik riski:** keşif kaynakları ve HLS segment adresleri dışarıdan gelir; kaynak izinleri, SSRF/özel ağ adresleri ve URL yönlendirmeleri için bu iki giriş dosyasında açık bir güvenli hedef doğrulama katmanı gözlenmedi. Bu durum üretim güvenliği açısından ayrı kapı gerektirir.
- **Karşılaştırma riski:** stdout'da ağ sonuçları ve kaynak sayıları bulunduğundan deterministik fixture olmadan byte eşitliği beklenemez.

**Yürütme yapılmadı; davranışsal kabul 0/92 olarak kalır.**
