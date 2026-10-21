# Madsc55-Tv — K1–K5 toplu kurulum durumu (21 Ekim 2026)

## Karar
Önce beşli sistemi ve eksik bağlantıları tamamla; bütün testleri bundan SONRA tek toplu yerel offline regresyonda çalıştır. Kullanıcı ayrıca izin vermedikçe GitHub Actions, canlı stream probe, eski depoya veya korunan üretim listelerine yazma YASAK. Kod/not commitleri [skip ci].

## GitHub main envanteri
- Ana beş workflow mevcut: madsc-01-guvenlik.yml (K1), madsc-02-kesif.yml (K2), madsc-03-kanal-test.yml (K3), madsc-04-yedek.yml (K4), madsc-05-bakim.yml (K5).
- Ancak .github/workflows altında toplam 15 YAML var; beş ana dosyanın DIŞINDA 10 yardımcı/pilot/legacy YAML bulunuyor. Bu nedenle 'yalnız beş workflow var' veya 'tam birleşti' demek yanlış. Kaldırma/taşıma kararı verilmeden önce tetikleyici, bağımlılık, izin, artifact ve davranış etkisi tek tek ana beşe taşınmalı; hiçbirini körlemesine silme.
- 22 ana görev: K1 4, K2 4, K3 6, K4 4, K5 4; toplam 0 completed, 5 in_progress, 17 pending.
- 92 eski davranış için gerçek kabul 0/92; 26 runtime güvenlik kuralı için kabul 0/26. 99 eski YAML kaynak incelemesi davranışsal kabul değildir.
- madsc/five_system_installation.py kurulum ve görev envanterini salt okunur üretir; TEST ÇALIŞTIRMAZ. Komut: python -m madsc.five_system_installation

## Kademelere göre kurulum/eksik iş
| Kademe | Mevcut kod/altyapı | Kurulum ve kabulde açık iş |
| --- | --- | --- |
| K1 Güvenlik | write_path_audit, core, korunan yollar | 26 gerçek runtime kuralı, tüm bağımsız yazma noktaları, 18 görev denetimindeki 10 açık görev, korunan dosya değişmezliği |
| K2 Keşif | discovery, source_import, history doğrulama, aday eşleme | Gerçek kaynak/lisans mutabakatı, günlük tetik davranışı, bağımsız artifact kökeni ve SHA, aday alternatif ayrımı |
| K3 Kanal/EPG/logo/IBO | channel_test, üç aşama/6 saat gate, EPG ve logo modülleri, kanal kataloğu | 75 adayın gerçek zaman aralıklı ölçümleri, ffprobe/ffmpeg, gerçek IBO cihaz kabulü, XMLTV/Pages ve görsel kimlik |
| K4 Arşiv/yedek | backup manifest, restore_drill, bağımsız sandbox karşılaştırma | Harici depolama kanıtı, hariciden gerçek izole restore, VOD/arşiv davranışı, ayın 1 ve 15'i tetik eşdeğerliği |
| K5 Bakım/rapor | maintenance, offline_five_gate, offline_gate, kanıt görev defteri | 92 davranışsal eşdeğerlik, hata/timeout/retry/artifact karşılaştırması, gerçek uçtan uca kanıt ve Türkçe kapanış |

## Toplu uygulama sırası
1. On ek workflow'un tüm görev/trigger/env/artifact/izin davranışlarını beş ana workflow ile karşılaştır; eksik entegrasyonları tek paket halinde kodla; hiçbir canlı çalıştırma yapma.
2. K1 güvenlik kapısını K2–K5 yazıcılarının hepsine bağla; K2→K3→K5 veri/kanıt devrini ve K4 bağımsız yedek kanıtını tamamla.
3. 22 görevin her birini gerçek kanıt gerekliliklerine bağla; offline mümkün olanları kur, gerçek cihaz/harici depolama gerektirenleri 'blocked external evidence' olarak dürüstçe bırak.
4. Kurulum kodu tamamlandıktan sonra, güncel main'in tüm dosyaları SHA doğrulanarak yerelde toplanır; python -m madsc.offline_gate ile tüm testler tek seferde çalıştırılır. GitHub Actions için ayrıca açık izin gerekir.

## Bu turda
Salt okunur kurulum envanteri modülü eklendi. Bu turda hiçbir test, GitHub Actions veya canlı kanal ölçümü çalıştırılmadı. Kurulum henüz tamamlanmadı; kullanıcıya aksini söyleme.
