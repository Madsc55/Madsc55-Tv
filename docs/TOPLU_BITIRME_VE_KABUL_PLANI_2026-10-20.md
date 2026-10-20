# Madsc55-Tv — Toplu bitirme ve gerçek kabul planı (20 Ekim 2026)

## Tek çalışma kuralı
Tek tek commit/test döngüleri yerine, ilgili kod, test, kanıt ve dokümantasyonu **toplu iş paketleri** halinde tamamla; CI'ı her paketin sonunda çalıştır. Bir yeşil CI koşusunu üretim kabulü olarak gösterme. Gerçek kaynak/cihaz/erişim yoksa kanıt uydurma ve ilgili kapıyı açık tut. Eski `Madsc55/madsc-tv` salt okunur; yeni `Madsc55/Madsc55-Tv` hedef depodur.

## Toplu iş paketleri
| Paket | Kapsam | Bitirme ölçütü |
|---|---|---|
| A — Envanter ve geçmiş | 99 YAML'ın kaynak betik/bağımlılık/tetikleyici/izin/artifact davranışları, 92 otomasyon matrisi, 810 dosya analizi, eski/yeni notların beraber okunması, eski notların tek doğrulanmış dosyada birleştirilmesi | Her eski görevin kaynak SHA'sı, yeni K1–K5 karşılığı, farkı ve kararı kayıtlı; notlar byte/hash kontrollü |
| B — K1 | 26 güvenlik kuralı, korunan listeler, salt okunur kapılar, GitHub izinleri, başarısızlık senaryoları | 26/26 gerçek çalışma zamanı kabul kanıtı |
| C — K2 | Aday keşfi, skor, öncelik, tekrar, gerçek geçmişin kökeni, SHA256 ve bağımsız GitHub artifact üretimi | Fixture ve gerçek kaynak ayrımı; gerçek köken/koşu/manifest doğrulaması; K2→K3/K5 kanıtı |
| D — K3 | ffprobe/ffmpeg, medya süresi/timeout, EPG XMLTV, logo, tvg-id, IBO cihaz doğrulaması | Eski/yeni aynı girdi çıktısı + gerçek ağ ve cihaz kanıtları; korunan listelere yazma yok |
| E — K4 | Yedek, arşiv, hash, offsite ve bağımsız geri yükleme | Gerçek geri yükleme ve değişmezlik kanıtı |
| F — K5 | Bakım, retry, raporlama, artefact aktarımı, çalışma sürekliliği | K1–K5 bütünleşik gerçek kanıt zinciri |
| G — Toplu kabul | 92 otomasyon için karşılaştırmalı koşular, tetikleme/izin/timeout/artifact, regresyon, 26 güvenlik, kullanıcı onayı | 92/92 + 26/26 + gerçek kaynak/IBO/restore; aksi halde üretime geçiş YASAK |

## Güncel doğrulanabilir sınırlar
- İzole beşli CI #268, #269, #270: SUCCESS. Bu gerçek kaynak veya canlı kabul değildir.
- 92 otomasyonun tam davranışsal eşdeğerlik kabulü: **0/92**.
- 26 güvenlik kuralının gerçek çalışma zamanı kabulü: **0/26**.
- K2 gerçek geçmiş üreticisi ve doğrulayıcısı kodu var; bağımsız doğrulanmış gerçek artifact/manifest henüz yok.
- Eski not arşivi kopyaları mevcut; `ESKI_SISTEM_NOTLARI.md` tek metin birleşimi tamamlanmış değil.
- Gerçek EPG/IBO cihaz, ağ ve bağımsız restore kabulü yok.

## İlerleme disiplini
1. Önce eski ve yeni kaynak notlarından ilgili kuralları ve envanteri oku.
2. Bir iş paketinin tüm modüllerini, negatif/pozitif testlerini ve kanıt şemasını **tek toplu çalışma** olarak hazırla.
3. Paket sonunda tek toplu CI/kanıt değerlendirmesi yap; iptal edilen koşuları başarı sayma.
4. Kanıt olmadan `behavioral_parity_verified`, `production_ready` veya güvenlik kabulü artırma.
5. Korunan M3U/M3U8, EPG, logo, favori ve yedeklere izinsiz yazma yapma; otomatik kanal ekleme/silme yok.
