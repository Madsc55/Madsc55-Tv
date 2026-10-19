# MADSC TV — İlk davranışsal eşdeğerlik kanıt paketi (19 Ekim 2026)

## Kapsam ve durum
Kaynak repo: Madsc55/madsc-tv, ref madsc/bes-sistem-toplu-birlestirme (salt okunur).
Yeni repo: Madsc55/Madsc55-Tv, main. Bu doküman **test planı ve fixture sözleşmesi**dir; gerçek koşu kanıtı veya onay değildir. Doğrulanmış eşdeğerlik 0/92.

## İlk karşılaştırma paketi: aday öncelik, tekrar, geçmiş
| Kimlik | Eski davranış / giriş | Beklenen karşılaştırma ve kanıt |
|---|---|---|
| P01 | aday_oncelik_raporu.py: tekrar doğrulanmış + yeni aday | Sıra 1; yeni K3 skor/çıktı ile karşılaştır |
| P02 | tekrar doğrulanmış + eski aday | Sıra 2 |
| P03 | video+ses + yeni aday, tekrar onayı yok | Sıra 3 |
| P04 | video+ses + eski aday, tekrar onayı yok | Sıra 4 |
| P05 | kalan aday | Sıra 5 |
| P06 | aynı sıra iki aday, farklı ad ve büyük/küçük harf | casefold ile deterministik tie-break |
| R01 | geçmiş başarısız aday | 2 saatlik retest sınırı öncesi/sonrası |
| R02 | geçmiş passed ve <2 success | 6 saatlik retest sınırı |
| R03 | passed ve >=2 success | 12 saatlik retest sınırı |
| R04 | passed ve >=3 success | 24 saatlik retest sınırı |
| R05 | aynı URL, iki HLS segment örneklemesi | değişen segment kabul, sabit segment reddi; sağlıklı sabit segment yanlış-negatif olarak ayrı kaydet |
| H01 | eski+yeninin last_test eşit ama gözlem farklı | history merge reddetmeli |
| H02 | yeni gözlemde runs azalmış | history merge reddetmeli |
| H03 | başarılı artifact başka dal/ata olmayan SHA | restore reddetmeli |
| H04 | önce başarı sonra daha yeni teknik başarısızlık | yeni ölçüm kazanmalı; otomatik onay verilmemeli |
| H05 | ikinci history JSON replace sırasında hata | yarım güncelleme riski ölçülmeli; atomik garanti varsayılmamalı |

## Her workflow için onay kanıtı
1. Eski YAML kaynak yolu ve kaynak commit SHA; çağrılan script/bağımlılık hashleri.
2. Yeni K1–K5 karşılık kodu ve commit SHA; tam fonksiyon haritası.
3. Tetikleme (push/path, cron, dispatch), izinler, hata/timeout, tekrar sırası ve limitleri.
4. Aynı sentetik girdiyle eski ve yeni çalışma; çıkış kodu, dosya listesi, şema, içerik farkı, SHA256.
5. Korunan üretim dosyalarında değişiklik olmadığının snapshot/hash kanıtı; gizli bilgi/URL maskeleme.
6. Değişen davranış varsa gerekçesi, güvenlik etkisi ve kullanıcı onayı.
7. Kanıt artifact URL, run ID, SHA ve fixture sürümü; reviewer kararı.
Sadece hepsi tamamlandığında behavioral_parity_verified=true olabilir. Script isim eşleşmesi, YAML lint, yeşil unittest veya rapor üretimi tek başına onay değildir.

## Mevcut uygulama engeli
Yeni Madsc55/Madsc55-Tv main dalında `tests/test_k1_runtime_workflow_guard.py`, `scripts/acceptance_26_92.py` ve `.github/workflows/k1-protected-write-tests.yml` yolları bulunamadı (GitHub 404). Bunlar eski kaynak dalında mevcut. Dolayısıyla yeni depoda varmış gibi doğrudan test düzeltmesi yapmak doğru değil. Önce kodun hangi depoda ve hangi committe yürütüldüğü, hangi dalın yürütülebilir hedef olduğu kararlaştırılmalı. Eski repo kullanıcı izni olmadan değiştirilmeyecek.

## Geçiş güvenliği
26/26 runtime güvenlik kuralı, 92/92 eşdeğerlik, offsite restore, IBO cihaz onayı ve açık kullanıcı kararı olmadan cutover yok. Üretim M3U, EPG, logo, favori, arşiv ve backup dosyalarına yazma yok.


## Kaynak betik düzeyinde somut kabul farkları — 19 Ekim ek denetimi

Bu bölüm eski depoda salt-okunur açılan üç YAML ve bunların çağırdığı üç gerçek Python betiğine dayanır. Önceki YAML envanterindeki aynı dosyalar yeniden "yeni incelenen workflow" sayılmamıştır. Hiçbir satır davranışsal parity onayı değildir.

| Eski iş | Kaynaktan doğrulanan gerçek davranış | Yeni K1–K5 için henüz kanıtlanmayan koşul |
|---|---|---|
| `390-aday-tekrar-test.yml` | `yedekler/tekrar_test_390.py` sabit tarihli kaynak M3U okur; en çok 12 worker (varsayılan 10), ffprobe 22 sn timeout, ffmpeg ile 20 sn video+ses çözümleme (45 sn timeout), sonuç CSV ve teknik doğrulanan M3U üretir. Workflow 90 dk sınır ve `if:always()` artifact kullanır. | K3'te yalnız ffprobe JSON ayrıştırılması **20 sn ffmpeg decode**, 10 paralel iş, çıktı M3U/CSV şeması, timeout, başarısız adayların raporu ve `if:always()` davranışı ile eşdeğer değildir. Üretim listesine yazma yok; `yedekler/` altına dosya yazımı var. |
| `aday-logo-epg-test.yml` | `candidate_epg_logo_join.py` pilot XMLTV kanal kimliği/program sayısı, logo SHA eşleşmesi, kimlik onaysızlığı ve cihaz doğrulanmamış durumunu ayrı raporlar; `CALISANLAR.m3u` hashini önce/sonra denetler. Pilot 5 kanal bekler. | Yeni K3'ün logo/EPG kimlik ve program ayrımı, pilot kapsamı ve ana liste hash koruması aynı girdilerle karşılaştırılmadı. Pilot 5 kanal tam EPG değildir. |
| `akilli-aday-puanlama.yml` | `SCAN_BATCH=-1` keşif, gerçek öncelikli ffprobe, `akilli_aday_puanla.py` CSV birleştirme; video 20, ses 15, çözünürlük 3/7/10, HTTPS logo 5 puan; URL'ye göre en yüksek skor seçimi ve CSV/JSON artifact. | Yeni K2/K3/K5 zinciri ile skor, deduplikasyon, çıktı kolonları ve `ANA_LISTEYE_EKLENEBILIR=HAYIR` birebir karşılaştırılmadı. Ağ ölçümü ve otomatik ekleme onayı yok. |

**Bir sonraki toplu kod kabulü:** Bu üç davranışın sentetik girdilerini, eski betiklerin salt-okunur izole kopyalarını ve yeni modülleri karşılaştıran negatif/pozitif regresyon paketi oluştur; üretim dosyalarına veya gerçek cihaz kararına dokunma. Bu dokümantasyon değişikliği tek başına yeni Actions çalıştırılmasını gerektirmez; sonraki kod paketi için tek toplu CI koşusu kullanılacak.
