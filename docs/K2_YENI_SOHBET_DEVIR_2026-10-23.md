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
