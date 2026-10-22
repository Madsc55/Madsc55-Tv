# 99 eski workflow — sabit kaynak kimlikleri ve K1–K5 inceleme sırası

Kaynak: `Madsc55/madsc-tv`, dal: `madsc/bes-sistem-toplu-birlestirme`; GitHub Contents API üzerinden doğrulanan **99** YAML dosyasının adları ve Git blob SHA kimlikleri.

**Önemli:** K1–K5 sütunu yalnızca dosya adından türetilmiş inceleme önceliğidir; görev çözümlemesi, entegrasyon veya davranışsal eşdeğerlik değildir. Eski sistemin 7 merkezi/test workflow'u 92 davranışsal iş kapsamından ayrıdır. Bu kayıt hiçbir workflow'u kapatmaz, Actions çalıştırmaz veya korunan IPTV verilerine dokunmaz.

| # | Eski YAML | Kaynak Git blob SHA | Kapsam | İnceleme adayı |
|---:|---|---|---|---|
| 1 | `390-aday-tekrar-test.yml` | `b12f53a17434fe719a65edfdc968f675e1f16b95` | LEGACY | K3, K2 |
| 2 | `aday-bekletme.yml` | `68564680a2c32b11d1c5ed78825f01c85d0378e8` | LEGACY | K2 |
| 3 | `aday-logo-epg-test.yml` | `21214309014625c4a63f00ee16c9017efac6b0a7` | LEGACY | K3, K2 |
| 4 | `aday-oncelik-kontrol.yml` | `1c2aa765b59ebad5ddbe3f0a06fcc9ead088e52b` | LEGACY | K2, K5 |
| 5 | `aday-yedekleme.yml` | `6ee9e08cc161b1fc975a8108fa102867de2d9690` | LEGACY | K4, K2 |
| 6 | `akilli-aday-puanlama.yml` | `8efd3656127031ebd3d73ca32d13ae55f9e22cb8` | LEGACY | K2 |
| 7 | `altinci-aday-tekrar-test.yml` | `268e05a82df328090ccf61c6335197350df8b99b` | LEGACY | K3, K2 |
| 8 | `automatic-png-logos.yml` | `3d321b81f023647d1cd29c99f015d296a34df525` | LEGACY | K3 |
| 9 | `besinci-zaman-asimi-test.yml` | `d36327a5b8846deab730e02043b3abc6a689ca63` | LEGACY | Belirsiz |
| 10 | `birlesik-aday-raporu.yml` | `26c0cb7bfc5af366d462eeb72461fb4ca2f9ff23` | LEGACY | K2, K5 |
| 11 | `birlesik-durum-raporu.yml` | `cfd859aa1c5d474749edd09d99506b006ab0f82b` | LEGACY | K5 |
| 12 | `dokuzuncu-akilli-tekrar-test.yml` | `ad54773ea6d7bb46d0c5deb51454fe8189f87c32` | LEGACY | K3 |
| 13 | `epg-gunluk.yml` | `d43d5c469b54b8ef89794e8fcc2c2cee9b0d84b9` | LEGACY | K3 |
| 14 | `epg-pages.yml` | `00e956c71c389d015209293b5de5b325cd4cb116` | LEGACY | K3 |
| 15 | `felaket-kurtarma-tatbikati.yml` | `53081c63ade88138049d8da1fef43ecfab588b5f` | LEGACY | K4 |
| 16 | `genel-aday-medya-test.yml` | `8d313fa5936799f86fd026831a3a149cbb0c250b` | LEGACY | K3, K2 |
| 17 | `genis-kanal-tarama.yml` | `ffea4c826bf1ea9f2b586ddbd279d169f930b9b1` | LEGACY | K2 |
| 18 | `ibo-bagimsiz-test-listesi.yml` | `be63acf659a9b50c68a8b01ff5434a3151877a8f` | LEGACY | K3 |
| 19 | `ibo-epg-kimlik-denetimi.yml` | `67ffc18c6cd79a5ea0960de72aeeecbc98fab7d7` | LEGACY | K1, K3 |
| 20 | `ibo-yedek-kalite.yml` | `da48c5195c35094a2a519feafd6b51f20f526edc` | LEGACY | K4, K3 |
| 21 | `iptv-test.yml` | `5cd014cb94e68be22f5f68b07618920c82fee740` | LEGACY | K3 |
| 22 | `k1-protected-write-tests.yml` | `83207d4ac4fa7abd9edd65de800f27fff7be2645` | EXCLUDED | K1 |
| 23 | `kanal-kararlilik.yml` | `c968204d3d9d54cf218d92954189c9e6945a509f` | LEGACY | K3 |
| 24 | `kaynak-puanlama-kontrol.yml` | `0ffc33a27ff7d6bb459fbfa608db1095218379f0` | LEGACY | K2, K5 |
| 25 | `madsc-01-guvenlik.yml` | `ae91b6c47745fe46659105f96cd28e6aca9d44d9` | EXCLUDED | K1 |
| 26 | `madsc-02-kesif.yml` | `f9970a874258c1cbd1c59f73fa427136ff2d53d4` | EXCLUDED | K2 |
| 27 | `madsc-03-kanal-test.yml` | `228d53500e99bc9953ab6d535b7809523a1854f0` | EXCLUDED | K3 |
| 28 | `madsc-04-arsiv-yedek.yml` | `7b4d62f33c6438236f418f8e60f779a22d05a9d3` | EXCLUDED | K4 |
| 29 | `madsc-05-genel-bakim.yml` | `4a7c9f0df18c9092ff8da886a1e33e55b5c5cbe4` | EXCLUDED | K5 |
| 30 | `madsc-11599-yedek-geri-yukle.yml` | `fb04cdcc5abede182df764804e8a5055956dcece` | LEGACY | K4 |
| 31 | `madsc-ana-liste-saglik.yml` | `6ba3cc60b74f26d3e7dcfecdf84d0cd2ce85baf7` | LEGACY | K5 |
| 32 | `madsc-arsiv-yedek-aktarim.yml` | `d2062b168db134177cb1683d86eaafa2c2937d54` | LEGACY | K4 |
| 33 | `madsc-aylik-merkezi-denetim.yml` | `8cca9b93855c1e2184863b8e59b07817e546366f` | LEGACY | K1 |
| 34 | `madsc-birlesik-kesif.yml` | `da472ae0e45aa0d3c03a7dc8f9833bf43f733902` | LEGACY | K2 |
| 35 | `madsc-cuma-ana-liste-denetimi.yml` | `b14aca32502179ae27e2399b0278502c512c2984` | LEGACY | K1 |
| 36 | `madsc-documentation-check.yml` | `0678a8a201eb194503f9097265fe37e68b1e4d3d` | LEGACY | K5 |
| 37 | `madsc-genis-kaynak-kontrol.yml` | `396d33dd8d5f3440dc81ae76abb91fc0d43f6a94` | LEGACY | K2, K5 |
| 38 | `madsc-hizli-on-kontrol.yml` | `92ba7ce2731d544b7361fb8877c531d4c4911840` | EXCLUDED | K5 |
| 39 | `madsc-ibo-3-5281.yml` | `4b0745614a11625f020baa39b832983ce5fc42ca` | LEGACY | K3 |
| 40 | `madsc-ibo-354-classify.yml` | `165bb7fc69775be790beab972dc68e92cf40c2c3` | LEGACY | K3 |
| 41 | `madsc-ibo-364-355-364.yml` | `7dff039f081b93c0efab2ced1ab8e873f021e496` | LEGACY | K3 |
| 42 | `madsc-ibo-398-16-49.yml` | `7b3dd19eb1fc1651e4f921e5b4f1c79fa0c91dc1` | LEGACY | K3 |
| 43 | `madsc-ibo-530-archive.yml` | `85bb9898838d253c99bc10f7d98468d71a522a37` | LEGACY | K3 |
| 44 | `madsc-ibo-6115-second.yml` | `4591be38fed55b81e6bf8d3a22319c262f11c01b` | LEGACY | K3 |
| 45 | `madsc-ibo-ilk-239.yml` | `7cfc6061bb1714c08cd52ff130a54c36bcee15c7` | LEGACY | K3 |
| 46 | `madsc-ibo-kararlar-grup1.yml` | `d79a157a13c667d6dd60a0c4837cca2c1da4f220` | LEGACY | K3 |
| 47 | `madsc-ibo-second-voice.yml` | `ad14d3daf071f8503651581ba93f6b6008fa0aee` | LEGACY | K3 |
| 48 | `madsc-otomatik-devam.yml` | `4cf99f3ce1801588c24082c2122b1d781192e7dd` | LEGACY | K5 |
| 49 | `madsc-rule24-test.yml` | `8092ea97979380e7af71aaa9383dc28f41c86ab8` | LEGACY | K1 |
| 50 | `madsc-sistem-saglik-denetimi.yml` | `c3c18155d13c2ca5e1a76304729fbcc6739849a5` | LEGACY | K1, K5 |
| 51 | `madsc-son-kontrol-kurtarma-teshis.yml` | `471540a306c4146fa12123510a4c70dcfe1356eb` | LEGACY | K4, K5 |
| 52 | `madsc-son-kontrol.yml` | `08871f1b397184459a093606c2519e1c19e5167a` | LEGACY | K5 |
| 53 | `madsc-toplu-butunluk.yml` | `d7456c7a5526350b0d52e39b6708cf288d209dbf` | LEGACY | K5 |
| 54 | `madsc-tum-sistem-yedek.yml` | `f56db59dc9a8a12f21296a80ea53b602340454ef` | LEGACY | K4, K5 |
| 55 | `madsc-turk-kanal-geri-sec.yml` | `ee4538c2b9e11f5589d8babacd9f3ff39457cc9b` | LEGACY | Belirsiz |
| 56 | `madsc-uc-asama.yml` | `93c3a87372b1dfbe80ba9e59dabc2180511112ae` | LEGACY | Belirsiz |
| 57 | `madsc-yedek-turk-ayir.yml` | `67b12b441fab5fa57eded1a7684ebf24e7d819c2` | LEGACY | K4 |
| 58 | `madsc-yedekler-aktarim-test.yml` | `e4de46aa7edbd84b8dc3bdda0e3d75a39421118b` | LEGACY | K4 |
| 59 | `madsc-yedekler-sayi-duzelt.yml` | `feb92ccf12c62b3818cac164f0effe319083872f` | LEGACY | K4 |
| 60 | `oncelikli-kanal-dogrulama.yml` | `ae7c910e5f7d840a6bceb0ab99cad3c9d414d63f` | LEGACY | Belirsiz |
| 61 | `onikinci-hata-siniflandirma-test.yml` | `41bf9c8b94b7f1e4ad045b1708cf52bb6edbe8da` | LEGACY | Belirsiz |
| 62 | `publish-iptv-png-logos.yml` | `7b8fa621b2cfaf151e26855d92a6ccbc326d6ed3` | LEGACY | K3 |
| 63 | `sekizinci-tekrar-raporu-test.yml` | `64665da9b8f4602e0b9310e012c835729a73afa7` | LEGACY | K1, K5 |
| 64 | `sozcu-akit-ozel-test.yml` | `b74d2db6f7acced67f514cae037be44b9722059d` | LEGACY | Belirsiz |
| 65 | `test-13-kaynak-degisiklik.yml` | `44c95db225dca48f6a50a72f72f6e4ce2f7d5457` | LEGACY | K2 |
| 66 | `test-14-istikrar.yml` | `4915ba2ac06a188a9ae4dddcfc46fda78f37515b` | LEGACY | Belirsiz |
| 67 | `test-15-logo-epg.yml` | `de27646659c70b0206f998ac2b69a3aa948682d2` | LEGACY | K3 |
| 68 | `test-16-workflow-safety.yml` | `902925df650f77f80e618a80da101cdeb68da23e` | LEGACY | K1 |
| 69 | `test-17-candidate-summary.yml` | `70d1ae2d665ebc398d1c41d7134ea7c89a3186f1` | LEGACY | Belirsiz |
| 70 | `test-18-change-simulation.yml` | `e39f6603c188d72f7ebb87f8b1cfbb858962d553` | LEGACY | Belirsiz |
| 71 | `test-19-integration.yml` | `bd8c5c1401661fc1dff468274d9e4f6ebe963279` | LEGACY | K5 |
| 72 | `test-20-full-integration.yml` | `41d5fd3ff8024f960a4c4f5e15810ea48d1fb3b8` | LEGACY | K5 |
| 73 | `test-21-functional-e2e.yml` | `f13904e84f0116b53120b792a89e1a4377f6dbc3` | LEGACY | Belirsiz |
| 74 | `test-22-real-playlist.yml` | `f1fe0cc001eac113f56acffaece5850d3eba515d` | LEGACY | Belirsiz |
| 75 | `test-23-live-stream.yml` | `412b3f263bab8d8f7c96f2776e56aa939a6b73b2` | LEGACY | K3 |
| 76 | `test-24-system-audit.yml` | `4cdb0dce456bd49cbb082c9506f7019f62776dc7` | LEGACY | K1, K5 |
| 77 | `test-25-full-project-readonly.yml` | `c00a6295182f7b31b7a0bc95af7056c0f20cae47` | LEGACY | Belirsiz |
| 78 | `test-26-automation-safety.yml` | `ada482112b58e47bd56b8c742ad08633e1f3b840` | LEGACY | K1 |
| 79 | `test-27-pipeline-contract.yml` | `41a24282bd6785cba1025d32040ccb1c994bf38a` | LEGACY | Belirsiz |
| 80 | `test-28-approval-gate.yml` | `d9253678d662c7bb2caefe12286ce15d5e6f702f` | LEGACY | K1 |
| 81 | `test-29-write-path-audit.yml` | `93b083583024215f0340b2d70974732ab9478c4d` | LEGACY | K1 |
| 82 | `test-30-write-risk-report.yml` | `97879b5d4f95546b521ecb5b034571fe230374dd` | LEGACY | K1 |
| 83 | `test-31-protected-write-gate.yml` | `eca623c47a4cb81e88e14d59f58862c8e110e6d1` | LEGACY | K1 |
| 84 | `test-32-unapproved-write-regression.yml` | `ca2bd0ed80045bc3ce0c027397172e16e28bdb5e` | LEGACY | K1 |
| 85 | `test-33-all-write-paths.yml` | `76d1d09da818fe8b8fe531167e8dd30b9a8717a2` | LEGACY | K1 |
| 86 | `test-34-protected-write-regression.yml` | `453f8ca6c0bcde59ef8fd4afc22fcc72baafc002` | LEGACY | K1 |
| 87 | `test-35-remaining-write-gate.yml` | `8bec3b96e6b084f6f2b44f9bd5af3af7bfd103c4` | LEGACY | K1 |
| 88 | `test-36-system-integration-audit.yml` | `f83899a4733d6bf979cd7ee74835ace179f6708e` | LEGACY | K1, K5 |
| 89 | `test-37-indirect-write-audit.yml` | `36b1c85749f7358efeb45962ffae0cae88525d56` | LEGACY | K1 |
| 90 | `test-38-audit-selftest.yml` | `bbe368fffdf354d9f61d654f009dcd749da8183f` | LEGACY | K1 |
| 91 | `test-39-protected-playlist.yml` | `2d495c94091c7c2194686c41181ac981f5a5d8aa` | LEGACY | K1 |
| 92 | `test-kanal-adaylari.yml` | `324040ec251f5bc9a0dc5c652312500d6cf37d67` | LEGACY | K2 |
| 93 | `toplu-sistem-kontrol.yml` | `34cf72108fb7aea4a1abde31027cfd3a859db43d` | LEGACY | K5 |
| 94 | `vod-guncelle.yml` | `78c3b8aa8e27b9f25e439337e2e94be9468b6f3b` | LEGACY | K3 |
| 95 | `yedek-geri-yukleme-tatbikat.yml` | `08a38be283550147e0e267f72fcc1291bfc9f88c` | LEGACY | K4 |
| 96 | `yedekler-yeniler-medya-kontrol.yml` | `43fd2b8bc0f6f4173bb3dde16744d10376d1027b` | LEGACY | K4, K3, K2, K5 |
| 97 | `yeni-aday-on-test.yml` | `a0d0625a65233e35f37dbcda25e6a3fd71915f75` | LEGACY | K2 |
| 98 | `yeni-kanal-arama-2026.yml` | `89f74c54f72f48583ff5abf1d148e3cc5b57f8f6` | LEGACY | K2 |
| 99 | `yeniler-guvenli-arama.yml` | `fabb2cf59223a983ed22046d19617a210efc16f2` | LEGACY | K2 |

## Gerçek entegrasyon için kabul kapısı

Her bir 92 workflow için gerçek eski çalıştırma, yeni K1–K5 çalıştırma, aynı girdi, çıktı ve yan etki karşılaştırması, hata/zaman aşımı karşılaştırması ve bağımsız onay gereklidir. Kaynak envanteri tek başına bunları sağlamaz.

Doğrulanmış davranışsal eşdeğerlik: **0/92**.
