# Yeni M3U8 kategori uyumluluk sözleşmesi

Kullanıcı kararı (20 Ekim 2026): `MADSC55_TV_YENI_TEST.m3u8` eski IPTV ana listesindeki kategori adlarını, emojilerini ve sırasını birebir koruyacak. Eski listeler değiştirilmeyecek.

Beklenen kategori sırası (eski sistem sohbet notlarından; kaynak M3U8 dosyasıyla nihai bayt düzeyi doğrulama henüz yapılmadı):

1. 🇹🇷 ULUSAL
2. 📺 HABER
3. ⚽ SPOR
4. 🌍 BELGESEL
5. 🧸 ÇOCUK
6. 🎧 MÜZİK
7. 📍 YEREL
8. 🕌 DİNİ
9. ⭐ FAVORİLER
10. 🔄 ALTERNATİF
11. ⭐ YENİLER
12. 📦 YEDEKLER

## Güvenlik ve geçiş şartları
- Yeni M3U8 dosyası ayrı kalacak; `CALISANLAR`, `YENILER`, `YEDEKLER`, `HEPSI`, `FAVORILER`, eski repo, XMLTV, EPG, logo ve yedeklere yazma yapılmayacak.
- M3U8 formatında boş kategori başlığı standart değildir: `group-title` ancak gerçek bir kanalın `#EXTINF` satırında bulunur. Bu yüzden 0 kanallı yeni listede henüz kategori satırları yoktur. Kanal eklenince uygun `group-title` kullanılacak.
- Sırf K2 adayı olduğu için kanalı yayın listesine ekleme; önce K3 gerçek erişim, görüntü ve ses doğrulaması, ardından kullanıcı onay sınırları.
- Eski ana M3U8'nin güncel gerçek kategori değerleri ve sırası okunup karşılaştırılmadan birebir uyumluluk **doğrulandı** denmeyecek.
