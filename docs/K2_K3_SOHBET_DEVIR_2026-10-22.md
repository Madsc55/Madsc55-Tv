# MADSC55-TV — K2/K3 sohbet devri (22 Ekim 2026)

## Kapsam ve çakışma önleme
- Depo: Madsc55/Madsc55-Tv, dal: main. Bu sohbet K2 aday/kaynak/ölçüm bağlantısı ve K3 kanal sürekliliği/kanıt doğrulaması kapsamındadır. K1, K4, K5 diğer sohbetlere bırakılmıştır.
- Korunan üretim playlistleri, EPG/XMLTV, logolar, favoriler, arşivler ve yedekler değiştirilmez. Eski madsc-tv deposu salt okunur. Canlı akış testleri ve Actions tetikleme yapılmadı.
- Eşzamanlı sohbetler main'e yazıyor: her yazımdan önce güncel dosya blob SHA'sını al; 409 çakışmada zorla yazma, yeniden oku. Commit mesajlarında [skip ci] kullan.

## Bu sohbetin doğrulanmış GitHub kayıtları
- 35090e5606a603bbf176194e55e8393f3bd09b9c: K2 aday/K3 probe bağlantısı için yinelenen aday, yinelenen ölçüm, geçersiz SHA-256 testleri.
- ad42d13e2006e4519935000f2a0d6df0ffa5f010: madsc/channel_test.py evaluate_three_stage_continuity ardışık her iki gözlem arasında en az minimum_hours (varsayılan 6 saat) arar; yalnız ilk-son toplam süre artık yeterli değildir.
- ab0c9931882d60022d71d1e6c1b5f3b1ef89bb29: yakın zamanlı örneklerin uzun toplam pencerede yanlış ön kabul almasını engelleyen regresyon testi.
- bc06b806d343f6ab8539492f00d776428a5d9253: madsc/k3_three_stage_gate.py captured_at için katı UTC RFC3339 biçimi doğrulaması.
- 745adb23c4d2b9c6940f431d914462f5936a7201: UTC tarih biçimi reddi regresyon testi.
- f07dbbbe7fd2b49fbeb1cd9f5bd45b6fdd9f99cf: UTC RFC3339 regex içindeki hatalı çift kaçış düzeltildi; geçerli timestamp reddi hatası giderildi.
- Başka sohbetlerin sonradan eklediği K2/K3 kaynak snapshot hash korelasyonu ve K3 test fixture güncellemelerini yeniden yapma. Bu devir notu hazırlanırken main başı bfb606865a...; güncel HEAD'i yeniden kontrol et.

## Kanıt durumu ve açık işler
- GitHub'a commit atılması testlerin geçtiği anlamına gelmez. Bu sohbet güncel tüm test paketini veya yeni regresyon testlerini çalıştırıp doğrulamadı; doğrulanmış yeşil test sayısı iddia edilmez.
- K2 gerçek kaynak/geçmiş kanıtının aynı snapshot'a bağlanması, K3'te 3 bağımsız örnek, ardışık >=6 saat, gerçek ffprobe/ffmpeg kanıtı ve IBO Player Pro cihaz denemesi uçtan uca doğrulanmalı. Offline sahte/fixture kanıt üretim kabulü değildir.
- Önceki proje devirlerine göre 92 eski workflow için bağımsız gerçek davranışsal kabul, 26 K1 kuralı için runtime denetim ve 22 görev için tam kabul hâlâ açık; bunları bitmiş ilan etme. Güncel durum için ana devir notları ve en yeni commitleri tekrar oku.
- Sonraki güvenli iş: güncel main'de K2/K3 testlerini topluca çalıştır; hataları kaynağında düzelt; önceki sohbetlerin aynı dosyalardaki güncellemelerini koru. Üretim kaynaklarını değiştirme.
