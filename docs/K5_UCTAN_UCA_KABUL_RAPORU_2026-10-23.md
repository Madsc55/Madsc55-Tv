# MADSC55-TV — K5 Uçtan Uca Kabul ve Kapanış Raporu

**Tarih:** 23 Ekim 2026  
**Hedef:** `Madsc55/Madsc55-Tv`, `main`  
**Karar:** **KABUL EDİLMEDİ — ÜRETİM GEÇİŞİ ENGELLİ**  
**Kapsam:** K1 güvenlik, K2 keşif, K3 kanal/EPG, K4 yedek/geri yükleme, K5 bakım ve 92 eski workflow'un davranışsal karşılaştırması.

## 1. Kaynak ve kapsam zinciri

- Sabit eski depo: `Madsc55/madsc-tv`, commit `ca374df3b9585c0d76a078db9536150ebbc260f7`, tree `a88dfa874b6964dcaa4de7a8f9075af2f146acd8`.
- Kaynak envanteri: `docs/LEGACY_SOURCE_SCOPE.json`, 99 YAML. Kapsamdan çıkarılan 7 doğrulanmış istisna; davranış kapsamı **92**.
- Karşılaştırma matrisi: `docs/K5_92_WORKFLOW_KAPSAM_KARSILASTIRMA_2026-10-23.md` — 92/92 satır, kaynak blob kimlikleriyle listeli. Katalogda aday aşama alanları boş; bu nedenle 92/92 satır için ayrıntılı davranış eşlemesi ve bağımsız yürütme kanıtı **eksik**.
- Önceki ayrıntılı statik kaynak incelemesi: **45/92** (batch 01–15); **47/92** henüz ayrıntılı incelenmedi. Kapsam envanteri, ayrıntılı statik inceleme veya eşdeğerlik kabulü yerine geçmez.

## 2. Beşli sistem karşılaştırma sonucu

| Aşama | Yerel/izole tasarımın kanıt sınırı | Gerçek kabul için eksik |
|---|---|---|
| K1 — güvenlik | Korunan yazma yolları için offline fixture ve yazma kapısı kontrolleri mevcut | Tüm gerçek yazma yolları, **26/26** çalışma zamanı kuralı ve üretim değişmezliği |
| K2 — keşif | İzole aday ayrıştırma, kaynak geçmişi ve K3 devri fixture kontrolleri mevcut | Gerçek kaynak kökeni, lisans, gerçek keşif ve bağımsız artifact zinciri |
| K3 — kanal testi | Fixture FFprobe/EPG/logo ve IBO koruma mantığı mevcut | Canlı kanallar, gerçek XMLTV/Pages zinciri; **IBO Player Pro cihaz kabulü en son** |
| K4 — yedek | İzole üç ağaç geri yükleme ve bozulma reddi fixture kontrolleri mevcut | Harici yedek hedefi ve bağımsız gerçek geri yükleme SHA kanıtları |
| K5 — bakım | İzole beşli denetim, salt-okunur 354/364/398 arşiv önizlemesi, regresyon testleri mevcut | **92/92** aynı girdili davranış çifti, hata/timeout/retry/yan etki/artifact karşılaştırması, güncel CI ve incelemeci onayı |

## 3. Eski-yeni yürütme eşdeğerliği

| Kanıt alanı | Mevcut doğrulanabilir durum | Karar |
|---|---:|---|
| Sabit katalog satırı | 92/92 | Kapsam tam |
| Ayrıntılı statik inceleme | 45/92 | Eksik 47 |
| Kaynak katalog aşama eşleştirmesi | 0/92 | Eksik 92 |
| Aynı girdili bağımsız eski-yeni koşu çifti | 0/92 | Eksik 92 |
| Çıktı/yan etki/başarısızlık/timeout/retry/artifact SHA karşılaştırması | 0/92 kabul | Bloke |
| Bağımsız davranışsal onay | 0/92 | Bloke |
| Gerçek çalışma zamanı güvenlik kuralı kabulü | 0/26 | Bloke |
| Ana görevlerin gerçek kapanış kabulü | 0/22 (son kayıtlı defter) | Bloke |

**Uyarı:** 45/92 önceki kaynak incelemesi yalnızca statik analize dayanır. Eski workflow'ların üretimde gerçekten aynı sonuçları verdiğini kanıtlamaz. Beşli sistemdeki izole fixture testleri de canlı üretim kanıtı değildir.

## 4. K5 kabul kapıları

1. **Kapsam:** 92 satırın her biri kaynak SHA ile izlenebilir — **SAĞLANDI**.
2. **Statik davranış ve gerçek eşleştirme:** 47 kaynak ve 92 aşama/komut eşleştirmesi eksik — **SAĞLANMADI**.
3. **Bağımsız yürütme:** Eski/yeni workflow için aynı girdi SHA, ayrı run ID, commit, artifact kimliği ve hash — **SAĞLANMADI**.
4. **Davranış eşdeğerliği:** Çıktı, yan etki, hata, timeout, retry ve artifact sonuçları — **SAĞLANMADI**.
5. **K1–K4 gerçek kabulü:** Güvenlik, lisans/köken, canlı yayın/EPG/Pages ve bağımsız harici geri yükleme — **SAĞLANMADI**.
6. **Güncel main CI:** Bu rapor yazılırken tam offline test paketi ve ilgili commit için başarılı CI kanıtı doğrulanmadı — **SAĞLANMADI**.
7. **Cihaz:** IBO Player Pro nihai kullanıcı testi diğer kapılardan sonra — **SAĞLANMADI**.

## 5. Güvenli kapanış kararı ve uygulama sırası

**K5-19:** 92/92 envanter karşılaştırması kayıt altına alındı; davranışsal kabul **in_progress** kalmalı.  
**K5-20:** Gerçek K1–K5 uçtan uca kanıt zinciri **pending**.  
**K5-21:** Timeout, retry, hata ve artifact eşdeğerliği **pending**.  
**K5-22:** Türkçe rapor **hazırlandı**, ancak üretim kabulü **pending**; rapor üretim onayı yerine geçmez.

Öncelik sırası: (i) eksik 47 eski workflow'un doğrudan script'leriyle salt-okunur ayrıntılı incelemesi; (ii) 92 davranış için K1–K5 tüketici/komut/girdi/çıktı haritası; (iii) güvenli izole, aynı-girdili eski/yeni koşular ve SHA kanıtları; (iv) timeout/retry/yan etki karşılaştırması ve bağımsız gözden geçirme; (v) K1–K4 gerçek kabulü ve güncel main CI; (vi) en son IBO Player Pro cihaz testi; (vii) açık onayla üretim geçişi.

**Değişmezlik:** Bu karşılaştırma ve rapor yalnızca dokümantasyondur. `CALISANLAR.m3u`, `FAVORILER`, `YENILER`, `YEDEKLER`, `HEPSI`, EPG/XMLTV, logolar, harici yedekler ve cihazlara yazma yapılmadı. Eski workflow'lar devre dışı bırakılmadı, üretim değişikliği ve canlı test başlatılmadı.

## 6. Sabit kaynakta doğrudan doğrulanan örnekler (ek kontrol)

`docs/K5_LEGACY_KAYNAK_DOGRULAMASI_2026-10-23.md` dosyasında `390-aday-tekrar-test.yml`, `aday-bekletme.yml` ve `aday-logo-epg-test.yml` eski sabit commit'ten **doğrudan okunarak** tetik, komut, timeout, artifact ve beşli sistem karşılıkları karşılaştırıldı. Bu örnekler, sırasıyla K3/K5, K2/K3/K5 ve K1/K3/K5 arasında çok-aşamalı davranışların bulunduğunu gösterir. Kaynak incelemesi, çağrılan script'lerin bağımsız yürütme sonuçlarını ve artifact SHA eşitliğini doğrulamadığından **davranışsal kabul 0/92** kalır. Önceki 45/92 ayrıntılı inceleme sayısı bu üç örneğin daha önce sayılmış olabilmesi nedeniyle artırılmadı.

## 7. Altı ek workflow'un doğrudan YAML sözleşmesi

`docs/K5_LEGACY_ALTI_WORKFLOW_KARSILASTIRMA_2026-10-23.md` ile aday önceliklendirme, teknik aday yedek taslağı, akıllı puanlama, altıncı tekrar testi, otomatik PNG logo hazırlığı ve beşinci zaman aşımı testinin eski sabit commit'teki workflow YAML'ları doğrudan okundu. 65 saniye teknik timeout, `RETEST_LIMIT=5`, gerçek ffprobe ve logo playlist değişmezliği gibi **eşdeğerlik için zorunlu** sınırlar kaydedildi. Eski-yeni ayrı koşu ve artifact kanıtları olmadığından üretim kabul kararı değişmedi; önceki 45/92 statik inceleme sayısı mükerrerlik denetlenmeden artırılmadı.

## 8. On ek sabit workflow'un kaynak doğrulaması ve EPG yayın riski

`docs/K5_LEGACY_ON_WORKFLOW_KARSILASTIRMA_2026-10-23.md` dosyasında 10 eski YAML doğrudan sabit commit'ten okunarak karşılaştırıldı. `epg-gunluk.yml` içindeki **contents: write + korunan kapı + git push** ve `epg-pages.yml` içindeki **Pages deploy + yayın SHA256 doğrulaması** üretim yan etkisi olan kritik zincirdir; bu çalışma sırasında çalıştırılmadı. Kaynak-temelli inceleme ve belge güncellemesi, gerçek yayın eşdeğerliği, başarılı CI veya bağımsız eski/yeni artifact kanıtı anlamına gelmez. **Kabul 0/92; üretim geçişi bloke.** Önceki statik 45/92 sayısı mükerrerlik kontrolü olmadan artırılmadı.

## 9. On ek sabit workflow ve kritik main yazma yolu

`docs/K5_LEGACY_EK_ON_WORKFLOW_2026-10-23.md` ile 10 ek eski workflow YAML'ı sabit commit'ten doğrudan incelendi. `madsc-birlesik-kesif.yml` `contents: write`, `actions: write`, korunan kapı ve 10 denemelik `main` push döngüsü içerir. `iptv-test.yml` korunan `CALISANLAR.m3u` dosyasını artifact olarak taşır; salt-okunur GitHub izni yerel dosya değişmezliğini tek başına kanıtlamaz. İlgili script yan etkileri ve yeni sistemdeki gerçek koruma kapısı bağımsız olarak doğrulanmadan üretim kabulü verilmez. Statik inceleme sayısı mükerrerlik kontrolü yapılmadan artırılmadı; **davranışsal kabul 0/92**.

## 10. Eski workflow'larda korunan yazma ve güvenli no-op ayrımı

`docs/K5_LEGACY_YAZMA_NOOP_ON_WORKFLOW_2026-10-23.md` dosyasında 10 sabit eski workflow doğrudan YAML içeriği üzerinden karşılaştırıldı. IBO 530/6115/ilk 239/grup1/ikinci sesli işlerinde `CALISANLAR.m3u` üzerinde commit/push sözleşmeleri bulundu. Buna karşılık IBO 3–5281 ve otomatik devam işleri yalnızca güvenli no-op/echo davranışında. 399–530 arşiv konumları ve 239/6115 karar senaryoları için 354/364/398 önizlemesinden **ayrı** kanıt gerekir. Bu yazma yolları çalıştırılmadı. Önceki statik 45/92 sayısı mükerrerlik kontrolü olmadan artırılmadı; **davranışsal kabul 0/92** ve üretim geçişi bloke.

## 11. On ek workflow: yeniden tetikleme, son kontrol ve yedek yazma zinciri

`docs/K5_LEGACY_ZINCIR_ON_WORKFLOW_2026-10-23.md` dosyasında 10 eski YAML doğrudan sabit commit'ten incelendi. `madsc-uc-asama.yml` kendini yeniden dispatch edebilir, `madsc-son-kontrol.yml` 10 rapor push retry içerir; YEDEKLER/Türk kanal işlemleri `CALISANLAR.m3u` dosyasını commit/push zincirine dahil eder. Bu davranışların K1 yazma kapısı, K2 kaynak kimliği, K3 canlı teknik test, K4 bağımsız restore ve K5 retry/artifact kanıtı birlikte sağlanmadan kabul edilmesi yasaktır. Eski workflow'lar çalıştırılmadı. **Davranışsal kabul 0/92; üretim geçişi bloke.** Mükerrerlik incelemesi yapılmadan statik 45/92 sayısı yükseltilmedi.

## 12. TOPLU 92/92 sabit kaynak doğrulaması ve otomatik koruma (2026-10-23)

Bu bölüm önceki parça parça kaynak incelemelerinden farklıdır: `docs/K5_KAYNAK_DOGRULAMA_01_18.json`, `19_36.json`, `37_54.json`, `55_72.json`, `73_90.json`, `91_92.json` dosyalarında **92 eski workflow YAML'ı** doğrudan `ca374df3b9585c0d76a078db9536150ebbc260f7` commit'inden okunup Git blob SHA ile eşleştirildi. Kaynak envanteriyle makine üzerinden yeniden karşılaştırmada **92/92 doğru, 0 eksik, 0 yinelenen, 0 SHA uyuşmazlığı** bulundu. YAML sinyalleri: `contents: write` 20, `git push` 21, `CALISANLAR.m3u` 34, aşağı akış dispatch 2. Bunlar statik metin eşleşmesidir; çalıştırma/yan etki kanıtı değildir.

`madsc/k5_source_audit.py` altı parçayı 99 satırlık donmuş katalogla fail-closed denetler; `tests/test_k5_source_audit.py` tam kapsam, eksik parça ve SHA bozulması regresyonlarını içerir. **Bu turda GitHub Actions test sonucu doğrulanmadı; yeni testlerin CI başarısı henüz kanıtlanmadı.** K5'in önceki **45/92 ayrıntılı davranış incelemesi** sayısı ile **92/92 YAML kimlik/sinyal taraması** birbirine karıştırılmamalıdır. Python script'lerinin tüm semantiği, aynı-girdi eski/yeni run ID ve artifact SHA karşılaştırması eksiktir. **Davranışsal kabul 0/92, üretim kabulü RED.**

## 13. K5 gerçek CI kapısı ve şema sıkılaştırması

`main` dalındaki `.github/workflows/madsc-05-bakim.yml` K5 job'una `python -m madsc.k5_source_audit --output reports/k5-source-audit.json` komutu eklendi. Başarısız kaynak SHA kapsam denetimi job'u başarısız kılar; rapor `madsc-k5-frozen-source-audit` artifact'ı olarak `always()` koşulunda saklanır. Denetleyici artık geçersiz yol, eksik/ekstra sinyal anahtarı, bool olmayan sinyal, mükerrer/uygunsuz K1–K5 aşama işaretlerini de fail-closed reddeder. `tests/test_k5_source_audit.py` içinde dördüncü bozuk aşama regresyonu eklendi. **CI'nin yeni commit'te geçtiği henüz doğrulanmadı**. 92/92 kaynak kimliği doğrulaması davranışsal eşdeğerlik veya üretim onayı değildir. **Kabul: RED, 0/92 davranışsal kanıt.**

## 14. K5 bağımsız salt-okunur CI otomasyonu

`.github/workflows/k5-frozen-source-ci.yml` yeni `push` (`main`, ilgili dosyalar), `pull_request` ve manuel tetiklemeler için ayrı bir 10 dakikalık salt-okunur doğrulama zinciridir. `persist-credentials: false`, `permissions: contents: read`, kaynak SHA denetimi, `tests.test_k5_source_audit` regresyonları ve başarısızlıkta da artifact saklama içerir. Üretim playlist, EPG, Pages veya gerçek cihaz workflow'u dispatch edilmez. **GitHub Actions sonuçları bu güncelleme sırasında doğrulanmış değildir; eklenen workflow'un geçtiği iddia edilmez.** 92/92 kaynak kimliği kontrolü tamam, davranışsal eşdeğerlik ve bağımsız uçtan uca üretim kabulü eksiktir.

## 15. CI kanıt görünürlüğü ve risk sayacı (2026-10-23)

`madsc/k5_source_audit.py` kaynak SHA kapsamına ek olarak YAML sinyal sayılarını ve **0 bağımsız eski/yeni koşu çifti, 92 eksik davranışsal kanıt** durumunu JSON rapora yazar. Beklenen statik işaret sayıları: `contents: write` 20, `git push` 21, `CALISANLAR.m3u` 34 ve aşağı akış dispatch 2. `tests/test_k5_source_audit.py` risk sayacı ve kanıt yokluğu regresyonlarını da içerir. Bu sayılar çalıştırma sırasında oluşan gerçek yan etkileri ispatlamaz. GitHub Actions'ın güncel sonucu bu turda bağımsız doğrulanamadı; mevcut commit için CI başarısı iddia edilmez. **Üretim kabulü halen RED.**

## 16. K5 bağımsız CI komutu ve bozuk envanter düzeltmesi

K5 bağımsız CI testi `python -m unittest discover -s tests -p 'test_k5_source_audit.py' -v` olarak değiştirildi; `tests` klasörünün Python paketi olması gerekmiyor. `madsc/k5_source_audit.py` kaynak envanterindeki eksik/yanlış Git blob SHA alanlarını kontrollü `invalid_inventory_row` hatasıyla reddediyor; regresyon testi eklendi. Bu düzeltmelerin GitHub Actions üzerinde başarılı olduğu henüz kanıtlanmadı. **92/92 kaynak kimliği denetimi ile 0/92 bağımsız davranışsal kabul ayrımı geçerlidir.**
