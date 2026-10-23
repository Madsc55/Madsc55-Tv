# K2 → Yeni Sohbet Devir Notu — 23 Ekim 2026

## Görev
MADSC55-TV K1–K5 beşli sistemini, özellikle K2 aday keşfi ve kaynak kanıtı tarafını, mevcut kod ve CI durumunu doğrulayarak tamamlamaya devam et. Yalnızca rapor vermek yerine kanıtlanmış kusurları küçük kod+regresyon testi commitleriyle düzelt; tamamlanmamış kabulü tamamlanmış sayma.

## Depo
- Aktif: https://github.com/Madsc55/Madsc55-Tv ; dal: main.
- Bu not hazırlanırken gözlenen HEAD: e9132499887106ed1382a1285e987eedf6f10914. Yeni sohbette yeniden kontrol et; eşzamanlı K1/K3/K4/K5 değişiklikleri var.
- Eski Madsc55/madsc-tv ve madsc/bes-sistem-toplu-birlestirme dalı referans/okuma amaçlı; PR #71'i merge etme.

## K2'de son gerçek değişiklikler
1. commit 87eab0abebfc77c883d5857769da246616abee24: madsc/discovery_batch.py parse_m3u içinde hatalı #EXTINF metadata satırlarını da max_entries sınırına dahil etti. Önceden yalnızca URL'ye dönüşmüş adaylar sayılıyordu.
2. commit 5cbe9f3baaf8427cd1cb391f96a0a91ea327f106: tests/test_discovery_batch.py içine hatalı #EXTINF sınır aşımı ve tek geçerli giriş regresyon testleri eklendi.
3. Bu iki değişikliğin sonraki main içeriğinde korunduğu kontrol edildi. Testlerin başarılı CI koşusunda yer alıp almadığını güncel SHA üzerinden yeniden doğrula.

## Son CI gözlemleri
- 40002212175 başarılı (SHA 9b950286d905ca2393a7ffa30ca01c0852f94ef0).
- 40002229536 iptal; 40002248915 iptal.
- Önceki başarılı: 40000180766 (e4a4482c...), 39993823508 (871bbdc2...).
- CI yalnızca tam aynı SHA için kabul edilir. Güncel main'i ve Actions'ı yeniden oku. [skip ci] commitleri ayrıca doğrulama gerektirebilir.

## K2 modülleri
- madsc/discovery_batch.py: M3U ayrıştırma, kaynak kanıtı, URL adayları ve read-only preview.
- madsc/candidate_coordination.py: K2/K3 aday, probe, retry, EPG/logo ve IBO sonuç koordinasyonu; production_ready=false.
- madsc/k2_artifact_integrity.py: salt okunur, hash ve dosya bütünlüğü kontrolü.
- tests/test_discovery_batch.py ve ilgili testler.
- K2 kaynak bağımsızlığı gerçek dış kaynaktan doğrulanmış değildir. Aynı/mirror envanterlerinin oyları birleştirilir; farklı envanter gerçek bağımsızlığı tek başına kanıtlamaz.

## Açık kabul kapıları
- Gerçek yayınlardan bağımsız kaynak kökeni kanıtı.
- K2→K3 gerçek kanal testleri: üç gerçek teknik örnek, örnekler arası en az altı saat; ffprobe/ffmpeg kanıtı.
- IBO Player Pro cihaz kabulü kullanıcı tarafından yapılacak; CI veya simülasyon bunu karşılamaz.
- 92 eski workflow için gerçek davranışsal eşdeğerlik kanıtı eksik; 0/92 doğrulanmış olarak raporlanmıştı, güncel kanıtı tekrar kontrol et.
- Diğer K'lar için ayrı kabul kapıları: K1 runtime, K4 gerçek restore, K5 aktarım/bütünlük; güncel dosya ve raporlarla doğrula.

## Kesin güvenlik kuralları
- CALISANLAR, YENILER, YEDEKLER, HEPSI, FAVORILER, EPG/XMLTV, logolar, yedekler, cihaz ayarları ve çalışan IPTV verilerini değiştirme/silme.
- Canlı IPTV URL probe, production yayınlama, cron açma, workflow manuel çalıştırma, eski otomasyonları kapatma ve PR #71 merge işlemlerini ayrı açık izin olmadan yapma.
- K2 kodu ve testleri için küçük, çakışma kontrollü commitler mümkün; her yazımdan önce dosya SHA'sını yeniden al.
- Başarılı CI ≠ canlı kabul. Yalnızca doğrulanmış sonuçları söyle.

## Yeni sohbette ilk işler
1. GitHub main HEAD, son Actions sonuçları ve varsa başarısız job loglarını kontrol et.
2. K2'nin son iki commitinin main'de ve testlerde olduğunu doğrula; gerekiyorsa mevcut HEAD'de CI.
3. K2/K3 kanıt sözleşmelerinde somut eksik ara; test ile yeniden üret, güvenli kod düzeltmesi yap, CI kontrol et.
4. Eski workflow 92/92 gerçek davranışsal eşdeğerlik için kaynak/kanıt envanterini incele; kanıtsız ilerleme yazma.
5. K1–K5 kabul kapılarını tek tabloda gerçek kanıtla raporla; IBO cihaz testini kullanıcıya bırak.

## 23 Ekim ek devir güncellemesi — son K2 ilerlemesi
- Kaynak/lisans denetim belgesi: docs/K2_KAYNAK_KOKEN_LISANS_DENETIM_2026-10-23.md. iptv-org README CC0 rozeti ile LICENSE The Unlicense metni farklıdır; depo lisansı üçüncü taraf yayın iznini doğrulamaz.
- K2 güvenlik kodu ve regresyon commitleri: f4b514f4 + 104250ee (başta boşluklu EXTINF); 27203b37 + eeb502d0 (kaynak kökeni/lisans fail-closed); 4bf37df7 + 97e1534f (UTF-8 bayt sınırı); 8a29d3e8 + 0f2004aa (önizleme UTF-8 bayt sınırı); c9b44e8f + ee08a04b (önizlemede köken/lisans/canlı doğrulama false); 79a51c62 + 0b7592b3 (reddedilmiş metadata dahil birleşik 20.000 sınırı); 1d1e685d + 8884b1c6 (kaynak başına metadata_entries raporu ve testi).
- Kod dosyaları: madsc/discovery_batch.py; tests/test_discovery_batch.py. Her iki dosyayı güncel main üzerinden tekrar oku. Son iki K2 commit 1d1e685d2ef8726ffa8a9731c5e3cd83c43dbec3 ve 8884b1c6fa1a66c0996a1cd6ecc4254eec044869.
- Güncel K2 kabulü: yayıncı sahipliği, açık yayın lisansı/yeniden dağıtım izni, gerçek operatör bağımsızlığı ve izinli kaynakla tekrarlanabilir keşif kanıtı YOK/BEKLİYOR. Farklı playlist envanteri bağımsız operatör kanıtı değildir.
- Test commitleri CI başarısı değildir. En yeni main SHA ve Actions/job/logları doğrulanmadan geçiş iddia etme. K2 production_ready=false, live_verified=false; K3 canlı ölçüm ve kullanıcı IBO cihaz testi ayrı kapıdır.
- DEVAM_NOTU.md dosyasının bu güncelleme öncesinde görülen sonunda parity 0/92, runtime 0/26, görev 0/22, production false yazılıydı. Bu sayılar güncellenmiş olabilir: yeniden oku, K2 tamamlanma yüzdesi olarak sunma.
- İlk iş: main HEAD, mevcut testleri, son Actions sonucunu ve kaynak kanıt envanterini doğrula. Kalan işlerde gerçek kanıt üret; sadece yeni yorum satırı ekleyerek tamamlandı iddia etme.
