# MADSC55-TV — Playlist ve EPG standardı

Karar: ana kanal listesi **playlist.m3u8** (UTF-8 kodlama), program rehberi **xmltv.xml** (XMLTV).

- M3U8 dosyası #EXTM3U başlığı ve #EXTINF satırlarıyla IPTV kanal listesidir; yayın URL'leri .m3u8 HLS adresleri olabilir.
- Her kanalın tvg-id değeri, XMLTV dosyasındaki <channel id="..."> değeriyle **birebir** eşleşmelidir.
- tvg-name, tvg-logo ve group-title varsa korunur; kanal adı, URL, sıralama ve kategoriler onaysız değiştirilmez.
- XMLTV programlarının channel niteliği aynı kanal id'sine işaret eder.
- Dosya uzantısı tek başına EPG uyumluluğu sağlamaz; IBO Player Pro üzerinde cihaz testi gereklidir.
- Var olan üretim playlist dosyası bu kararla otomatik yeniden adlandırılmaz, üzerine yazılmaz veya yayımlanmaz.
- Yeni kurulumdaki doğrulayıcı, örnek dosyalarla izole çalışır. EPG/IBO uyumluluğu kanıtlanana kadar üretim geçişi kapalıdır.
