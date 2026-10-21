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


## 19 Ekim 2026 — kaynak puanlama ve onay regresyonu

`tests/test_legacy_source_score_vectors.py` eski `akilli_aday_puanla.py` kaynak incelemesinden çıkarılmış 10 puan/status vektörü ile ayrıca 4 puan × 3 teknik durum × 2 kararlılık = 24 otomatik listeye yazmama kombinasyonunu kapsar. Yanlış veri türlerinin reddi de test edilir. İlk 10 vektörün CI koşusu #39330966958 **SUCCESS**. Onay matrisi genişletmesi commit `29b945a` ile eklendi; bunun CI sonucu ayrıca doğrulanmalıdır. Bu karşılaştırma eski betiği fiilen çalıştıran diferansiyel test değildir ve `akilli-aday-puanlama.yml` için 92'lik tam davranışsal kabul sayısını artırmaz. Gerçek ffprobe, CSV şeması, URL bazında en yüksek skor seçimi ve artifact davranışı hâlâ açık.


## 20 Ekim 2026 — akıllı aday puanlama CSV birleştirme sözleşmesi

`madsc/legacy_candidate_merge.py` eski salt-okunur `scripts/akilli_aday_puanla.py` kaynak davranışından çıkarıldı: yalnız üç rapor adından teknik kanıt önceliği, `VIDEO_SES_VAR` kanıtının önceliği, `TEKNIK_MEDYA/COZUNURLUK/SES_IZI` alanlarının URL üzerinden birleştirilmesi, HTTP(S) filtreleme, aynı URL için yüksek puanın korunması, eşit puanda ilk aday, puan/kanal sıralaması ve 13 CSV alanı. `tests/test_legacy_candidate_merge.py` olumlu/olumsuz örnekleri kapsar. Bu testler eski betikle fiili karşılaştırmalı çalıştırma, gerçek ağ/ffprobe veya tam workflow davranışsal kabul değildir; 0/92 korunur. İlk puanlama vektörleri Actions #39331287407 SUCCESS. Bu yeni kodun CI sonucu ayrıca doğrulanmalıdır.

## 20 Ekim 2026 — Gercek eski betik ile diferansiyel CI kanitlari
- Akilli aday puanlama: `tests/test_candidate_differential.py`, pinned `tests/fixtures/legacy_akilli_aday_puanla.py`; ek tekrar/teknik kanit onceligi senaryolari; commit `eaed201d`, Actions #39337813130 SUCCESS.
- EPG/logo: `tests/test_legacy_epg_logo_differential.py`, pinned `tests/fixtures/legacy_candidate_epg_logo_join.py`; bos, pilot programli/programsiz ve logo SHA senaryolari; commit `923aea0b`, Actions #39338017857 SUCCESS.
- 390 tekrar testi: `tests/test_legacy_390_differential.py`, pinned `tests/fixtures/legacy_tekrar_test_390.py`; agsiz ffprobe/ffmpeg taklitleriyle eski/yeni CSV ve M3U karsilastirmasi; commit `bbde1b94`, Actions #39338267421 SUCCESS.
**Kapsam siniri:** Yalnizca secili sentetik girdi/rapor davranislari dogrudan karsilastirildi. Workflow cron/trigger/izinler, gercek ag, cihaz, hata-artifact, tam davranissal kabul kanitlanmadi. 92/92 kabul 0/92; 26/26 runtime guvenlik 0/26. Siradaki grup: eski K2 aday oncelik, tekrar siniri ve gecmis birlestirme (P01-P06, R01-R05, H01-H05), sonra K3 workflow artifact/timeout davranislari. 


## 20 Ekim 2026 — Toplu eski/yeni CLI karşılaştırma ve bilinen güvenlik farkı

| Betik düzeyi | Çalıştırmalı fixture testi | CI kanıtı | Sınır |
|---|---|---|---|
| `akilli_aday_puanla.py` | `tests/test_legacy_scoring_differential_batch.py`: 8 puan vektörü, URL dedup, CSV sıra, JSON özet, otomatik liste onayı yok | #39425233309 SUCCESS | Sabitlenmiş fixture, eski Git SHA'sı bağımsız doğrulanmadı |
| `akilli_tekrar_test_takvimi.py` | `tests/test_legacy_retest_differential_batch.py`: 2/6/12/24 saat, bozuk tarih, geçersiz kayıt, CSV eşleme | #39437371154 SUCCESS | Sabitlenmiş fixture, gerçek cron/cache zinciri yok |
| `aday_oncelik_raporu.py` | `tests/test_legacy_priority_differential_batch.py`: beş seviye, tie-break ve CSV | #39437666057 SUCCESS | Sabitlenmiş fixture, workflow tetik/izin/artefakt karşılaştırması yok |

**Eski betikteki güvenlik farkı (kasıtlı eşdeğer olmama):** `aday_oncelik_raporu.py` çıktısında `{ "ONCELIK": tier + 1, "INCELEME_NOTU": ..., **row }` sırası nedeniyle giriş CSV'sinde bulunan `ONCELIK`/`INCELEME_NOTU` alanları hesaplanan değerleri geçersiz kılabiliyor. Yeni `priority_rows` bu alanları girişten sonra yeniden hesaplayarak sahte öncelik veya otomatik onay notunu reddediyor. Negatif test: `test_legacy_input_fields_can_override_computed_priority`, commit `d3f7764423607d600fbdc34e923d0650dec6935a`. Bu **bilinçli güvenlik düzeltmesi**dir; tam davranış eşdeğerliği iddia edilmez. Son commitin CI sonucu ayrıca kontrol edilmelidir.

Bu üç betik karşılaştırması **üç workflow kabulü değildir**. Gerçek 92 workflow için kaynak commit/bağımlılık hashleri, tetik/izin, hata/timeout, artefaktlar, yan etkiler ve kullanıcı onayı gereklidir. Kabul 0/92, K1 runtime kabulü 0/26. Korunan üretim dosyalarına yazma yok.
