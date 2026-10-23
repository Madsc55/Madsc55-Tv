# K5 — 92/92 eski workflow kapsam–beşli sistem karşılaştırma matrisi

Tarih: 2026-10-23. Kaynak: `Madsc55/madsc-tv` sabit commit `ca374df3b9585c0d76a078db9536150ebbc260f7`; katalog ağacı `a88dfa874b6964dcaa4de7a8f9075af2f146acd8`. Hedef: `Madsc55/Madsc55-Tv`, `main`. Bu belge **kapsam ve aday eşleştirme karşılaştırmasıdır**, gerçek davranışsal eşdeğerlik kanıtı değildir. Eski workflow'lar çalıştırılmadı, kaynak içerikleri bu toplu aşamada tek tek incelenmedi; katalogda sabitlenmiş blob kimlikleri kullanıldı. `candidate_k_stages` yalnızca katalogdaki ön sınıflandırmadır. Eski-yeni bağımsız yürütme çiftleri, aynı girdiye ait SHA256, yan etkiler, timeout/retry ve artifact kökeni olmadan hiçbir satır kabul edilmez.

## Yeni beşli sistemin güncel kaynak bağları

| Aşama | Güncel workflow | Git blob SHA |
|---|---|---|
| K1 | `.github/workflows/madsc-01-guvenlik.yml` | `07506ec506d1c329bfab23e3488d1ffd0fc7991a` |
| K2 | `.github/workflows/madsc-02-kesif.yml` | `e1954cdca2b7a7b77e016d797260ecffe861a170` |
| K3 | `.github/workflows/madsc-03-kanal-test.yml` | `d99c8dfccb4d9ca64af963fbbfac90da936731ea` |
| K4 | `.github/workflows/madsc-04-yedek.yml` | `31d6ff6fd98fbb87dcfeef6aa2709a517b268c7e` |
| K5 | `.github/workflows/madsc-05-bakim.yml` | `60dd4242aa0e2a8e1bcb63cf34224bc4951272f8` |

## 92 workflow karşılaştırması

Her satırın sonucu **BEKLEMEDE**; aday aşama eşleşmesi uygulama eşdeğerliği değildir. `—` = katalogda aşama adayı belirtilmemiş, manuel inceleme gerekli.

| # | Sabit eski workflow | Eski blob SHA | K1–K5 aday eşleştirme | Davranışsal kabul |
|---:|---|---|---|---|
| 1 | `.github/workflows/390-aday-tekrar-test.yml` | `b12f53a17434fe719a65edfdc968f675e1f16b95` | — | BEKLEMEDE |
| 2 | `.github/workflows/aday-bekletme.yml` | `68564680a2c32b11d1c5ed78825f01c85d0378e8` | — | BEKLEMEDE |
| 3 | `.github/workflows/aday-logo-epg-test.yml` | `21214309014625c4a63f00ee16c9017efac6b0a7` | — | BEKLEMEDE |
| 4 | `.github/workflows/aday-oncelik-kontrol.yml` | `1c2aa765b59ebad5ddbe3f0a06fcc9ead088e52b` | — | BEKLEMEDE |
| 5 | `.github/workflows/aday-yedekleme.yml` | `6ee9e08cc161b1fc975a8108fa102867de2d9690` | — | BEKLEMEDE |
| 6 | `.github/workflows/akilli-aday-puanlama.yml` | `8efd3656127031ebd3d73ca32d13ae55f9e22cb8` | — | BEKLEMEDE |
| 7 | `.github/workflows/altinci-aday-tekrar-test.yml` | `268e05a82df328090ccf61c6335197350df8b99b` | — | BEKLEMEDE |
| 8 | `.github/workflows/automatic-png-logos.yml` | `3d321b81f023647d1cd29c99f015d296a34df525` | — | BEKLEMEDE |
| 9 | `.github/workflows/besinci-zaman-asimi-test.yml` | `d36327a5b8846deab730e02043b3abc6a689ca63` | — | BEKLEMEDE |
| 10 | `.github/workflows/birlesik-aday-raporu.yml` | `26c0cb7bfc5af366d462eeb72461fb4ca2f9ff23` | — | BEKLEMEDE |
| 11 | `.github/workflows/birlesik-durum-raporu.yml` | `cfd859aa1c5d474749edd09d99506b006ab0f82b` | — | BEKLEMEDE |
| 12 | `.github/workflows/dokuzuncu-akilli-tekrar-test.yml` | `ad54773ea6d7bb46d0c5deb51454fe8189f87c32` | — | BEKLEMEDE |
| 13 | `.github/workflows/epg-gunluk.yml` | `d43d5c469b54b8ef89794e8fcc2c2cee9b0d84b9` | — | BEKLEMEDE |
| 14 | `.github/workflows/epg-pages.yml` | `00e956c71c389d015209293b5de5b325cd4cb116` | — | BEKLEMEDE |
| 15 | `.github/workflows/felaket-kurtarma-tatbikati.yml` | `53081c63ade88138049d8da1fef43ecfab588b5f` | — | BEKLEMEDE |
| 16 | `.github/workflows/genel-aday-medya-test.yml` | `8d313fa5936799f86fd026831a3a149cbb0c250b` | — | BEKLEMEDE |
| 17 | `.github/workflows/genis-kanal-tarama.yml` | `ffea4c826bf1ea9f2b586ddbd279d169f930b9b1` | — | BEKLEMEDE |
| 18 | `.github/workflows/ibo-bagimsiz-test-listesi.yml` | `be63acf659a9b50c68a8b01ff5434a3151877a8f` | — | BEKLEMEDE |
| 19 | `.github/workflows/ibo-epg-kimlik-denetimi.yml` | `67ffc18c6cd79a5ea0960de72aeeecbc98fab7d7` | — | BEKLEMEDE |
| 20 | `.github/workflows/ibo-yedek-kalite.yml` | `da48c5195c35094a2a519feafd6b51f20f526edc` | — | BEKLEMEDE |
| 21 | `.github/workflows/iptv-test.yml` | `5cd014cb94e68be22f5f68b07618920c82fee740` | — | BEKLEMEDE |
| 22 | `.github/workflows/kanal-kararlilik.yml` | `c968204d3d9d54cf218d92954189c9e6945a509f` | — | BEKLEMEDE |
| 23 | `.github/workflows/kaynak-puanlama-kontrol.yml` | `0ffc33a27ff7d6bb459fbfa608db1095218379f0` | — | BEKLEMEDE |
| 24 | `.github/workflows/madsc-11599-yedek-geri-yukle.yml` | `fb04cdcc5abede182df764804e8a5055956dcece` | — | BEKLEMEDE |
| 25 | `.github/workflows/madsc-ana-liste-saglik.yml` | `6ba3cc60b74f26d3e7dcfecdf84d0cd2ce85baf7` | — | BEKLEMEDE |
| 26 | `.github/workflows/madsc-arsiv-yedek-aktarim.yml` | `d2062b168db134177cb1683d86eaafa2c2937d54` | — | BEKLEMEDE |
| 27 | `.github/workflows/madsc-aylik-merkezi-denetim.yml` | `8cca9b93855c1e2184863b8e59b07817e546366f` | — | BEKLEMEDE |
| 28 | `.github/workflows/madsc-birlesik-kesif.yml` | `da472ae0e45aa0d3c03a7dc8f9833bf43f733902` | — | BEKLEMEDE |
| 29 | `.github/workflows/madsc-cuma-ana-liste-denetimi.yml` | `b14aca32502179ae27e2399b0278502c512c2984` | — | BEKLEMEDE |
| 30 | `.github/workflows/madsc-documentation-check.yml` | `0678a8a201eb194503f9097265fe37e68b1e4d3d` | — | BEKLEMEDE |
| 31 | `.github/workflows/madsc-genis-kaynak-kontrol.yml` | `396d33dd8d5f3440dc81ae76abb91fc0d43f6a94` | — | BEKLEMEDE |
| 32 | `.github/workflows/madsc-ibo-3-5281.yml` | `4b0745614a11625f020baa39b832983ce5fc42ca` | — | BEKLEMEDE |
| 33 | `.github/workflows/madsc-ibo-354-classify.yml` | `165bb7fc69775be790beab972dc68e92cf40c2c3` | — | BEKLEMEDE |
| 34 | `.github/workflows/madsc-ibo-364-355-364.yml` | `7dff039f081b93c0efab2ced1ab8e873f021e496` | — | BEKLEMEDE |
| 35 | `.github/workflows/madsc-ibo-398-16-49.yml` | `7b3dd19eb1fc1651e4f921e5b4f1c79fa0c91dc1` | — | BEKLEMEDE |
| 36 | `.github/workflows/madsc-ibo-530-archive.yml` | `85bb9898838d253c99bc10f7d98468d71a522a37` | — | BEKLEMEDE |
| 37 | `.github/workflows/madsc-ibo-6115-second.yml` | `4591be38fed55b81e6bf8d3a22319c262f11c01b` | — | BEKLEMEDE |
| 38 | `.github/workflows/madsc-ibo-ilk-239.yml` | `7cfc6061bb1714c08cd52ff130a54c36bcee15c7` | — | BEKLEMEDE |
| 39 | `.github/workflows/madsc-ibo-kararlar-grup1.yml` | `d79a157a13c667d6dd60a0c4837cca2c1da4f220` | — | BEKLEMEDE |
| 40 | `.github/workflows/madsc-ibo-second-voice.yml` | `ad14d3daf071f8503651581ba93f6b6008fa0aee` | — | BEKLEMEDE |
| 41 | `.github/workflows/madsc-otomatik-devam.yml` | `4cf99f3ce1801588c24082c2122b1d781192e7dd` | — | BEKLEMEDE |
| 42 | `.github/workflows/madsc-rule24-test.yml` | `8092ea97979380e7af71aaa9383dc28f41c86ab8` | — | BEKLEMEDE |
| 43 | `.github/workflows/madsc-sistem-saglik-denetimi.yml` | `c3c18155d13c2ca5e1a76304729fbcc6739849a5` | — | BEKLEMEDE |
| 44 | `.github/workflows/madsc-son-kontrol-kurtarma-teshis.yml` | `471540a306c4146fa12123510a4c70dcfe1356eb` | — | BEKLEMEDE |
| 45 | `.github/workflows/madsc-son-kontrol.yml` | `08871f1b397184459a093606c2519e1c19e5167a` | — | BEKLEMEDE |
| 46 | `.github/workflows/madsc-toplu-butunluk.yml` | `d7456c7a5526350b0d52e39b6708cf288d209dbf` | — | BEKLEMEDE |
| 47 | `.github/workflows/madsc-tum-sistem-yedek.yml` | `f56db59dc9a8a12f21296a80ea53b602340454ef` | — | BEKLEMEDE |
| 48 | `.github/workflows/madsc-turk-kanal-geri-sec.yml` | `ee4538c2b9e11f5589d8babacd9f3ff39457cc9b` | — | BEKLEMEDE |
| 49 | `.github/workflows/madsc-uc-asama.yml` | `93c3a87372b1dfbe80ba9e59dabc2180511112ae` | — | BEKLEMEDE |
| 50 | `.github/workflows/madsc-yedek-turk-ayir.yml` | `67b12b441fab5fa57eded1a7684ebf24e7d819c2` | — | BEKLEMEDE |
| 51 | `.github/workflows/madsc-yedekler-aktarim-test.yml` | `e4de46aa7edbd84b8dc3bdda0e3d75a39421118b` | — | BEKLEMEDE |
| 52 | `.github/workflows/madsc-yedekler-sayi-duzelt.yml` | `feb92ccf12c62b3818cac164f0effe319083872f` | — | BEKLEMEDE |
| 53 | `.github/workflows/oncelikli-kanal-dogrulama.yml` | `ae7c910e5f7d840a6bceb0ab99cad3c9d414d63f` | — | BEKLEMEDE |
| 54 | `.github/workflows/onikinci-hata-siniflandirma-test.yml` | `41bf9c8b94b7f1e4ad045b1708cf52bb6edbe8da` | — | BEKLEMEDE |
| 55 | `.github/workflows/publish-iptv-png-logos.yml` | `7b8fa621b2cfaf151e26855d92a6ccbc326d6ed3` | — | BEKLEMEDE |
| 56 | `.github/workflows/sekizinci-tekrar-raporu-test.yml` | `64665da9b8f4602e0b9310e012c835729a73afa7` | — | BEKLEMEDE |
| 57 | `.github/workflows/sozcu-akit-ozel-test.yml` | `b74d2db6f7acced67f514cae037be44b9722059d` | — | BEKLEMEDE |
| 58 | `.github/workflows/test-13-kaynak-degisiklik.yml` | `44c95db225dca48f6a50a72f72f6e4ce2f7d5457` | — | BEKLEMEDE |
| 59 | `.github/workflows/test-14-istikrar.yml` | `4915ba2ac06a188a9ae4dddcfc46fda78f37515b` | — | BEKLEMEDE |
| 60 | `.github/workflows/test-15-logo-epg.yml` | `de27646659c70b0206f998ac2b69a3aa948682d2` | — | BEKLEMEDE |
| 61 | `.github/workflows/test-16-workflow-safety.yml` | `902925df650f77f80e618a80da101cdeb68da23e` | — | BEKLEMEDE |
| 62 | `.github/workflows/test-17-candidate-summary.yml` | `70d1ae2d665ebc398d1c41d7134ea7c89a3186f1` | — | BEKLEMEDE |
| 63 | `.github/workflows/test-18-change-simulation.yml` | `e39f6603c188d72f7ebb87f8b1cfbb858962d553` | — | BEKLEMEDE |
| 64 | `.github/workflows/test-19-integration.yml` | `bd8c5c1401661fc1dff468274d9e4f6ebe963279` | — | BEKLEMEDE |
| 65 | `.github/workflows/test-20-full-integration.yml` | `41d5fd3ff8024f960a4c4f5e15810ea48d1fb3b8` | — | BEKLEMEDE |
| 66 | `.github/workflows/test-21-functional-e2e.yml` | `f13904e84f0116b53120b792a89e1a4377f6dbc3` | — | BEKLEMEDE |
| 67 | `.github/workflows/test-22-real-playlist.yml` | `f1fe0cc001eac113f56acffaece5850d3eba515d` | — | BEKLEMEDE |
| 68 | `.github/workflows/test-23-live-stream.yml` | `412b3f263bab8d8f7c96f2776e56aa939a6b73b2` | — | BEKLEMEDE |
| 69 | `.github/workflows/test-24-system-audit.yml` | `4cdb0dce456bd49cbb082c9506f7019f62776dc7` | — | BEKLEMEDE |
| 70 | `.github/workflows/test-25-full-project-readonly.yml` | `c00a6295182f7b31b7a0bc95af7056c0f20cae47` | — | BEKLEMEDE |
| 71 | `.github/workflows/test-26-automation-safety.yml` | `ada482112b58e47bd56b8c742ad08633e1f3b840` | — | BEKLEMEDE |
| 72 | `.github/workflows/test-27-pipeline-contract.yml` | `41a24282bd6785cba1025d32040ccb1c994bf38a` | — | BEKLEMEDE |
| 73 | `.github/workflows/test-28-approval-gate.yml` | `d9253678d662c7bb2caefe12286ce15d5e6f702f` | — | BEKLEMEDE |
| 74 | `.github/workflows/test-29-write-path-audit.yml` | `93b083583024215f0340b2d70974732ab9478c4d` | — | BEKLEMEDE |
| 75 | `.github/workflows/test-30-write-risk-report.yml` | `97879b5d4f95546b521ecb5b034571fe230374dd` | — | BEKLEMEDE |
| 76 | `.github/workflows/test-31-protected-write-gate.yml` | `eca623c47a4cb81e88e14d59f58862c8e110e6d1` | — | BEKLEMEDE |
| 77 | `.github/workflows/test-32-unapproved-write-regression.yml` | `ca2bd0ed80045bc3ce0c027397172e16e28bdb5e` | — | BEKLEMEDE |
| 78 | `.github/workflows/test-33-all-write-paths.yml` | `76d1d09da818fe8b8fe531167e8dd30b9a8717a2` | — | BEKLEMEDE |
| 79 | `.github/workflows/test-34-protected-write-regression.yml` | `453f8ca6c0bcde59ef8fd4afc22fcc72baafc002` | — | BEKLEMEDE |
| 80 | `.github/workflows/test-35-remaining-write-gate.yml` | `8bec3b96e6b084f6f2b44f9bd5af3af7bfd103c4` | — | BEKLEMEDE |
| 81 | `.github/workflows/test-36-system-integration-audit.yml` | `f83899a4733d6bf979cd7ee74835ace179f6708e` | — | BEKLEMEDE |
| 82 | `.github/workflows/test-37-indirect-write-audit.yml` | `36b1c85749f7358efeb45962ffae0cae88525d56` | — | BEKLEMEDE |
| 83 | `.github/workflows/test-38-audit-selftest.yml` | `bbe368fffdf354d9f61d654f009dcd749da8183f` | — | BEKLEMEDE |
| 84 | `.github/workflows/test-39-protected-playlist.yml` | `2d495c94091c7c2194686c41181ac981f5a5d8aa` | — | BEKLEMEDE |
| 85 | `.github/workflows/test-kanal-adaylari.yml` | `324040ec251f5bc9a0dc5c652312500d6cf37d67` | — | BEKLEMEDE |
| 86 | `.github/workflows/toplu-sistem-kontrol.yml` | `34cf72108fb7aea4a1abde31027cfd3a859db43d` | — | BEKLEMEDE |
| 87 | `.github/workflows/vod-guncelle.yml` | `78c3b8aa8e27b9f25e439337e2e94be9468b6f3b` | — | BEKLEMEDE |
| 88 | `.github/workflows/yedek-geri-yukleme-tatbikat.yml` | `08a38be283550147e0e267f72fcc1291bfc9f88c` | — | BEKLEMEDE |
| 89 | `.github/workflows/yedekler-yeniler-medya-kontrol.yml` | `43fd2b8bc0f6f4173bb3dde16744d10376d1027b` | — | BEKLEMEDE |
| 90 | `.github/workflows/yeni-aday-on-test.yml` | `a0d0625a65233e35f37dbcda25e6a3fd71915f75` | — | BEKLEMEDE |
| 91 | `.github/workflows/yeni-kanal-arama-2026.yml` | `89f74c54f72f48583ff5abf1d148e3cc5b57f8f6` | — | BEKLEMEDE |
| 92 | `.github/workflows/yeniler-guvenli-arama.yml` | `fabb2cf59223a983ed22046d19617a210efc16f2` | — | BEKLEMEDE |

## Mutabakat ve eksikler

- Sabit kaynak envanteri: **99** YAML. Kapsam dışı tutulan doğrulanmış 7 kaynak: `k1-protected-write-tests.yml`, `madsc-01-guvenlik.yml`, `madsc-02-kesif.yml`, `madsc-03-kanal-test.yml`, `madsc-04-arsiv-yedek.yml`, `madsc-05-genel-bakim.yml`, `madsc-hizli-on-kontrol.yml`.
- Kapsamdaki eski davranış workflow'u: **92/92** katalog satırı burada listelendi. Bu, **92/92 kaynak kodu incelendi** demek değildir. Önceki ayrıntılı statik inceleme: **45/92**; kalan **47/92** ayrı kaynak incelemesi bekliyor.
- Bağımsız aynı-girdi eski/yeni yürütme çifti: **0/92**; davranışsal kabul: **0/92**. Timeout/retry/side-effect/artifact kanıtı yok. Bu nedenle otomatik kapatma, eski workflow devre dışı bırakma veya üretim geçişi **yasak**.
- Sonraki adım: kalan 47 eski workflow'un içerik ve doğrudan çağırdığı script'lerin salt-okunur incelemesi, her workflow için gerçek kaynak/çıktı/yan-etki sözleşmesi, beşli karşılıkta aynı girdili izole yürütmeler, bağımsız artifact SHA ve incelemeci onayı.
