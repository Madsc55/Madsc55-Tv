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

1. Bu iki Python dosyasının **tam fonksiyon gövdeleri** ve dolaylı modüller için yan etki/çağrı grafiği tamamlanmalı.
2. 66 batch'in her biri için ağ çağrıları, ffprobe alt süreçleri, zaman aşımı ve çıktı/artifact deterministik fixture'larla izole edilmeli.
3. Değişken dış GitHub API ve canlı medya yanıtları sabitlenmeden eski/yeni SHA256 kanıtları karşılaştırılamaz.
4. Keşfedilen M3U adresi tek başına yayın hakkı veya kullanım izni kanıtı değildir; kaynak doğrulaması ayrı yapılmalı.
5. İki bağımsız yürütmenin gerçek logları, hash'leri, side-effect manifestleri ve korunan dosya değişmezliği doğrulanmadı.

**Kabul sonucu: BLOCKED; bağımsız davranışsal kabul sayısı değişmedi (0/92).** Üretim taraması veya liste yazımı yapılmadı.
