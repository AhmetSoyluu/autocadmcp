# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development commands

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

Run the MCP server over stdio:

```bash
python -m autocad_mcp_server.main
```

Run all tests:

```bash
pytest
```

Run one unit test file:

```bash
pytest tests/unit/test_path_sandbox.py
```

Run one test by name:

```bash
pytest tests/unit/test_lisp_policy.py -k test_rejects_shell_primitives
```

Run integration tests only:

```bash
pytest -m integration
```

Run lint and type checks:

```bash
ruff check .
mypy src
```

Run coverage:

```bash
pytest --cov=autocad_mcp_server --cov-report=term-missing
```

## Architecture overview

This repository is a Python MCP server for AutoCAD automation on Windows. The design intentionally separates MCP-facing tools from AutoCAD process control.

`src/autocad_mcp_server/main.py` is the entrypoint. It loads settings, configures logging, builds the runtime services, and registers the MCP tools.

The tool modules under `src/autocad_mcp_server/tools/` should stay thin. They validate requests, call `DWGService`, and shape responses. Business decisions about execution mode belong in `src/autocad_mcp_server/services/dwg_service.py`, not in tool files.

There are two AutoCAD execution paths. Live desktop automation goes through COM in `src/autocad_mcp_server/services/interop_manager.py` and `src/autocad_mcp_server/adapters/com_adapter.py`. Background/offline processing goes through `accoreconsole.exe` in `src/autocad_mcp_server/services/core_console_manager.py` and `src/autocad_mcp_server/adapters/core_console_adapter.py`.

Core Console jobs must remain serialized through `src/autocad_mcp_server/services/execution_queue.py`. Do not bypass that queue from a tool or service.

The security boundary is centralized. Every incoming DWG path must go through `src/autocad_mcp_server/security/path_sandbox.py` before any file access, copy, open, or script generation. Every AutoLISP execution request must go through `src/autocad_mcp_server/security/lisp_policy.py` before it reaches COM or Core Console.

Structured request and response contracts live in `src/autocad_mcp_server/models/requests.py` and `src/autocad_mcp_server/models/responses.py`. Keep tool I/O changes aligned with these models and update tests when schemas change.

## Repository-specific constraints

Never open or modify a DWG path that has not been canonicalized and verified against `allowed_dwg_roots`.

Never execute raw AutoLISP directly from a tool. Route it through `LispPolicy` and `LispRunner` so blocked primitives, payload size limits, and execution depth limits stay enforced.

Never spawn `accoreconsole.exe` directly from a tool or adapter without going through the queue and timeout wrapper.

Graceful degradation matters here. COM failures, hung AutoCAD sessions, and Core Console timeouts should become structured errors instead of crashing the MCP process.

---

## Elektrik Tesisat Çizim Standartları (Kalıcı Referans)

Bu bölüm, Türkiye elektrik tesisat projelerinde uygulanan standart çizim kurallarını içerir. **Yeni bir elektrik projesi çizerken bu kurallara uyulmalıdır.**


### 1. Katman (Layer) Yapısı

Elektrik tesisat çizimlerinde her disiplin ve eleman türü ayrı katmandadır. Renk kodları standardize edilmiştir.

#### 1.1 Aydınlatma Katmanları
| Katman Adı | Renk | Kullanım |
|---|---|---|
| `aydınlatma` | 3 (yeşil) | Aydınlatma armatür sembolleri ve hatları |
| `AYDINLATMA` | 3 (yeşil) | Aydınlatma kolon hatları ve besleme kabloları |
| `MYAYDINLATMA` | 3 (yeşil) | Mekanik tesisat aydınlatma (ortak kullanım) |
| `SPOT IŞIĞI` | 242 | Spot aydınlatma alanları |
| `SPOT TARAMA` | 254 | Spot aydınlatma tarama deseni |

#### 1.2 Priz ve Kuvvet Katmanları
| Katman Adı | Renk | Kullanım |
|---|---|---|
| `priz` | 12 (kırmızı-mor) | Priz sembolleri ve konumları |
| `priz linyesi` | 170 | Priz grupları, linyeler ve sembol açıklamaları |
| `BLK-PRİZ` | 1 (kırmızı) | Priz blok sembolleri |
| `BLK-PRİZ GRUP` | 1 (kırmızı) | Priz grup şeması |
| `PRİZ BESLEME` | 4 (mavi) | Priz besleme hatları |
| `ELK_PRİZ` | 3 (yeşil) | Ek priz katmanı |
| `KUVVET` | 1 (kırmızı) | Kuvvet tesisatı |
| `MY_KUVVET` | 3 (yeşil) | Mekanik kuvvet bağlantıları |
| `MYKUVVET` | 1 (kırmızı) | Alternatif kuvvet katmanı |
| `YEDEK PRİZ` | 3 | Yedek priz hatları |

#### 1.3 Zayıf Akım Katmanları
| Katman Adı | Renk | Kullanım |
|---|---|---|
| `telefon` | 6 (magenta) | Telefon tesisatı |
| `tv` | 4 (mavi) | TV tesisatı |
| `BLK-DATA` | 2 (sarı) | Data prizi blokları |
| `BLK-TELEFON` | 8 (gri) | Telefon blok sembolleri |
| `BLK-TV` | 8 (gri) | TV blok sembolleri |
| `C_DATA` | 6 | Data kablo hatları |
| `C_TEL` | 4 | Telefon kablo hatları |
| `C_TV` | 3 | TV kablo hatları |
| `FO KABLO` | 1 (kırmızı) | Fiber optik kablo |
| `ELK-CCTV` | 30 | CCTV kablo hatları |
| `CY_CCTV` | 4 | CCTV çevre güvenlik |
| `BLK-CCTV` | 50 | CCTV blok sembolleri |
| `ELK-SES` | 3 | Seslendirme tesisatı |
| `CY_SES` | 3 | Ses sistemi |
| `BLK-HDMI` | 8 | HDMI bağlantı blokları |
| `RG-11` | 4 | RG-11 koaksiyel kablo |

#### 1.4 Yangın Algılama Katmanları
| Katman Adı | Renk | Kullanım |
|---|---|---|
| `2A-YANGIN ALGILAMA HATTI` | 1 (kırmızı) | Yangın algılama hattı |
| `2A-YANGIN ALARM HATTI` | 5 (mavi) | Yangın alarm hattı |
| `BLK-YANGIN` | 3 | Yangın algılama blokları |
| `BLK-YANGIN YAZI` | 9 | Yangın algılama yazıları |

#### 1.5 Topraklama Katmanları
| Katman Adı | Renk | Kullanım |
|---|---|---|
| `TOPRAKLAMA` | 44 (turuncu) | Topraklama hatları |
| `B_TOPRAKLAMA` | 1 (kırmızı) | Bina topraklama sistemi |
| `TOPRAKLAMA-YAZI` | 7 (beyaz) | Topraklama yazıları |
| `TOPRAKLAMA-DETAY` | 7 | Topraklama detay çizimleri |
| `PARATONER` | 1 (kırmızı) | Paratoner sistemi |

#### 1.6 Genel Elektrik Katmanları
| Katman Adı | Renk | Kullanım |
|---|---|---|
| `Elektrik Yazı` / `Elk - Yazı` | 7 (beyaz) | Elektrik yazıları, etiketler |
| `Elk - Tesisat` | 10 | Tesisat genel |
| `ELK-YAZI` | 2 (sarı) | Elektrik etiket yazıları |
| `YAZI` | 30 / 251 | Genel yazı katmanı |
| `SEMBOL` | 7 (beyaz) | Sembol listesi ve açıklama |
| `SEMBOLLER` | 7 | Genel semboller |
| `HAT` | 3 (yeşil) / 6 | Hat çizimleri |
| `HAT_ENH` | 56 | Enerji nakil hattı |
| `KOLON` | 51 / 1 | Kolon hattı |
| `KOLON HATTI 0.60 mm` | 91 | Kolon hat kalınlığı |
| `B_PANO` | 2 (sarı) | Pano sembolleri |
| `B_UPS BESLEME` | 6 | UPS besleme hatları |
| `B_UPS` | 3 | UPS tesisatı |
| `UPS` | 6 | UPS genel |
| `B_ACİL YÖNL.` | 3 | Acil aydınlatma yönlendirme |
| `KANAL_TIPLER` | 5 | Kablo kanalı tipleri |

#### 1.7 OG (Orta Gerilim) ve Abonelik Katmanları
| Katman Adı | Renk | Kullanım |
|---|---|---|
| `Mev. AG Hat` | 1 (kırmızı) | Mevcut AG hatları |
| `ROL_CEPHE` | 1 (kırmızı) | Röle cephe detayı |
| `SUPPLEMENTARY` | 7 (beyaz) | Tek hat şeması ek bilgileri |
| `SYMBOL` | 4 (mavi) | OG sembolleri |
| `AUTOCONNECTING` | 2 | Oto bağlantı hatları |
| `AFB ANTED` | 7 | Antet çerçevesi |
| `0 0 ANTED CERCEVE` | 144 | Antet çerçeve alt katman |
| `0  0 OG HUCRE` | 4 | OG hücre detayı |
| `00-ELKYAZ` | 141 | Kablo kanalı detay yazıları |
| `ENERJI_ANL` | 7 | Enerji analizörü |

#### 1.8 Mimari Altlık Katmanları (Referans)
| Katman Adı | Renk | Kullanım |
|---|---|---|
| `DUVAR` | 52 / 255 | Mimari duvar |
| `A.O. DUVAR` | 7 | Mimari duvar altlık |
| `KOLON` | 51 | Yapısal kolon |
| `KAPI` | 5 / 142 | Kapı |
| `TARAMA` | 252 / 254 | Mimari tarama |
| `Defpoints` | 7 | AutoCAD nokta referans (yazdırılmaz) |

### 2. Blok Tanımları (Block Definitions)

#### 2.1 Aydınlatma Blokları
| Blok Adı | Açıklama |
|---|---|
| `60x60 ARMATÜR` | 60x60 cm gömme LED panel armatür |
| `60x60 S.Ü. Led Panel Armatür` | 60x60 sıva üstü LED panel |
| `12W LED SPOT` | 12W LED spot aydınlatma |
| `12W SIVA ÜSTü LED DAİRESEL ARMATÜR (IP40)` | 12W dairesel LED |
| `SENSÖRLÜ TAVAN ARMATÜR` | Hareket sensörlü tavan armatürü |
| `YATAY BANT ARMATÜR` | Yatay bant tip LED armatür |
| `6x9W SARKIT AVİZE` | Sarkıt avize (6x9W) |
| `aplik` | Duvar aplikası |
| `buat aydınlatma` | Aydınlatma buatı |
| `anahtar` | Aydınlatma anahtarı |
| `komütatör` | Komütatör anahtar |
| `LED SÜRÜCÜ` | LED sürücü |
| `LED1603` / `LED2011` / `LED1502` / `LED1102` / `LED1601` / `LED1801S` | LED armatür tipleri (model kodlarıyla) |
| `KÜT3050` | Kütük armatür 30x50 |

#### 2.2 Priz Blokları
| Blok Adı | Açıklama |
|---|---|
| `priz` | Standart şebeke prizi |
| `etanj priz` | Etanj (su geçirmez) priz |
| `buat priz` | Priz buatı |
| `2 Lİ ŞEBEKE PRİZ` | İkili şebeke prizi |
| `2'Lİ UPS` | İkili UPS prizi |
| `ETP` | Etanj topraklı priz |
| `ETRPK` | Etanj renkli priz kutusu |
| `PK2` | Priz kutusu tip 2 |
| `DKPK` | Data + şebeke priz kutusu |

#### 2.3 Kombine Priz Blokları (Birleşik Kutular)
| Blok Adı | İçerik |
|---|---|
| `1U1D` | 1 UPS + 1 Data |
| `1U1D1TV` | 1 UPS + 1 Data + 1 TV |
| `1U1HDMI` | 1 UPS + 1 HDMI |
| `2U1S1D1T` | 2 UPS + 1 Şebeke + 1 Data + 1 Telefon |
| `2U1S1D1T1HDMI` | 2 UPS + 1 Şebeke + 1 Data + 1 Telefon + 1 HDMI |
| `2S2U1D` | 2 Şebeke + 2 UPS + 1 Data |
| `1S1TV` | 1 Şebeke + 1 TV |
| `1S2U2T2D` | 1 Şebeke + 2 UPS + 2 Telefon + 2 Data |
| `1S1T` | 1 Şebeke + 1 Telefon |
| `1S2U1D` | 1 Şebeke + 2 UPS + 1 Data |

#### 2.4 Zayıf Akım Blokları
| Blok Adı | Açıklama |
|---|---|
| `telefon` | Telefon prizi |
| `tv` | TV prizi |
| `DATA` | Data (RJ45) prizi |
| `HDMI` | HDMI çıkış prizi |
| `MDF` | Ana dağıtım çerçevesi |
| `TEL. SANT.` | Telefon santralı |
| `R. KABİNET` | Rack kabinet |
| `KABİNET` | FO kabinet |
| `ANTEN` | Anten |
| `AMPL` | Amplifikatör |

#### 2.5 Güvenlik ve CCTV Blokları
| Blok Adı | Açıklama |
|---|---|
| `B_KAMERA` / `KAM2` | Güvenlik kamerası |
| `CCTV MERKEZİ` | CCTV merkezi |
| `LCD` | LCD monitör |
| `viwer` | Video izleme ünitesi |
| `PRO` | Projektör/hoparlör |

#### 2.6 Yangın Algılama Blokları
| Blok Adı | Açıklama |
|---|---|
| `KD` | Konvansiyonel duman dedektörü |
| `YB` | Yangın butonu (ihbar butonu) |
| `YAS` | Yangın alarm sireni |
| `FLK` | Flaşör (görsel uyarıcı) |
| `RÖLE MODÜLÜ` | Röle modülü |
| `İZLEME MODÜLÜ` | İzleme/adreslenebilir modül |
| `DMDK` | Duman dedektörü (alternatif) |
| `YANGIN POMPA` | Yangın pompası |

#### 2.7 Acil Aydınlatma Blokları
| Blok Adı | Açıklama |
|---|---|
| `ACİL1` ~ `ACİL6` | Farklı tipte acil aydınlatma armatürleri |
| `SOL ACIK` / `SOL CIK` | Acil yönlendirme (sol yön) |

#### 2.8 Pano ve Dağıtım Blokları
| Blok Adı | Açıklama |
|---|---|
| `TALİ PANO` | Tali dağıtım panosu |
| `TALİ DAĞITIM TABLOSU` | Tali dağıtım tablosu (tek hat) |
| `KUVVET TABLOSU` | Kuvvet tablosu |
| `KAT UPS TABLOSU` | Kat UPS tablosu |
| `PANO DETAYI` | Pano detay çizimi |
| `TEK HAT ŞEMASI` | Tek hat şeması bloğu |
| `ENERJİ ANALİZÖRÜ` | Enerji analizörü |
| `PANO NO` | Pano numarası etiketi |
| `LİNYE NO` | Linye numarası etiketi |

#### 2.9 Topraklama ve Direk Blokları
| Blok Adı | Açıklama |
|---|---|
| `topraklama` | Topraklama sembolü |
| `POT. DEN. BARASI` | Potansiyel dengeleme barası |
| `TEMEL TOPR DETAYI` | Temel topraklama detayı |
| `SH_TOPR-D-ÇELİKDONATILI` | Çelik donatılı topraklama |
| `TOPP` | Topraklama prizi |
| `Mevcut Direk` / `Mevcut Demir Direk` | Mevcut direk sembolleri |
| `Mevcut Bina Tipi TR KÜK` | Mevcut bina tipi trafo köşkü |
| `DİREK CİNSİ` / `DİREK CİNSİ 1` | Direk tipi sembolleri |
| `MEV_DIREK` | Mevcut direk (alternatif) |
| `TRAFO` | Trafo sembolü |

#### 2.10 Mekanik (HVAC) İlişkili Elektrik Blokları
| Blok Adı | Açıklama |
|---|---|
| `ADİ` / `EADİ` | Anemostatlı difüzör |
| `VAV` / `EVAV` | Değişken hava debisi |
| `KOM` / `EKOM` | Kombi/fan coil |
| `IT` / `UT` | İç/Dış ünite |
| `VS` | Vana seti |
| `HAVALANDIRMA` | Havalandırma motoru |
| `KOLLEKTÖR` | Kollektör |
| `FOTOSELLI KAPI` | Fotoselli kapı (elektrik bağlantısı) |

### 3. Kablo Tipleri ve Kesitleri (Standart)

Projelerde kullanılan kablo notasyonu:

| Notasyon | Açıklama |
|---|---|
| `4x4 N2XH KABLO` | 4 damarlı 4mm² halogensiz (aydınlatma kolon) |
| `3x25+16 mm² NAYY` | 3 faz 25mm² + nötr 16mm² alüminyum yeraltı |
| `3x120+70 mm² NAYY` | Ana kolon besleme (büyük güçler) |
| `4x16 mm² NAYY` | 4 damarlı 16mm² alüminyum |
| `(3x50+25mm²) NYY` | 3 faz bakır yeraltı |
| `3x(1x35/16) XLPE` | OG kablo (XLPE izoleli) |
| `3x(1x150/25 mm² Cu XLPE)` | OG ana kablo |
| `3x(1/0 Pigeon) 34,5 kV` | OG havai hat (Pigeon iletken) |
| `3xSwallow 34,5 kV` | OG havai hat (Swallow iletken) |
| `1X16 ÖRGÜLÜ CU İLETKEN` | Topraklama iletkeni |
| `1x50mm² NYY` | Topraklama bakır iletkeni |
| `ÇE110 PE Boru` | PE muhafaza borusu |

### 4. Tek Hat Şeması Bileşenleri

Tek hat şemasında kullanılan standart elemanlar ve sembol listesi:

| Eleman | Açıklama |
|---|---|
| `A.O.S. 3xNNA (10kA)` | Anahtarlı otomatik sigorta (kesme kapasitesi) |
| `K.A.R. 4xNNA NNmA` | Kaçak akım rölesi (4 kutup, hassasiyet) |
| `T.M.Ş.` | Termik manyetik şalter |
| `NH BUŞON` | NH sigorta buşon |
| `KONTAKTÖR` | Kontaktör |
| `SİNYAL LAMBASI` | Sinyal lambası |
| `VOLTMETRE KOMÜTATÖRÜ` | Voltmetre komütatörü |
| `AKIM TRAFOSU` | Akım trafosu (ör: 150/5A, 200/5A) |
| `X/5 A ELEKTRONİK SAYAÇ` | Elektronik enerji sayacı |
| `KONDANSATÖR` | Kompanzasyon kondansatörü (kVAr) |
| `ENERJİ ANALİZÖRÜ` | Enerji analizörü |
| `PARAFUDR` | Parafudr (aşırı gerilim koruma) |
| `HARİCİ TİP SİGORTALI SEKSİYONER` | OG seçme anahtarı |
| `HARİCİ VE DAHİLİ ÜTP TRAFO` | ÜTP (üç trafolu posta) |

### 5. Topraklama Standartları

| Eleman | Ölçü/Detay |
|---|---|
| İşletme topraklama elektrodu | 2m, 65x65x7 galvaniz köşebent kazık |
| Koruma topraklama elektrodu | 2m, 65x65x7 galvaniz köşebent kazık |
| Topraklama şeridi | 30x3,5mm galvaniz şerit |
| Topraklama iletkeni | 1x16 mm² örgülü Cu / 1x50 mm² NYY |
| Kablo kanalı koruma | ÇE110 PE Boru + kum + ikaz bandı |

### 6. AG Kablo Kanalı Detayı (TİP1-A)

Kablo kanalı kesiti katmanları (üstten alta):
1. Sıkıştırılmış elenmiş toprak
2. İkaz şeridi
3. Dolgu malzemesi (elenmiş toprak)
4. Kum yatağı
5. Koruyucu malzeme (tuğla vb.)
6. Kab. Muhafaza Borusu (PE)
7. AG Kablo
8. Kum yatağı (alt)

Kanal ölçüleri: G(genişlik)+20, H(derinlik) belirtilir.

### 7. Antet (Başlık) Bloğu Standart Alanları

Her paftada bulunması gereken bilgiler:
- PROJENİN ADI
- İL / İLÇE / BELEDİYE
- ADRESİ
- YAPTIRAN (ADI SOYADI)
- PROJEYİ ÇİZEN (Teknik Personel / Mühendis)
- PROJE NO
- ÇİZİM TARİHİ
- ÖLÇEK (1/1000, 1/50, vb.)
- PAFTA NO / ADA NO / PARSEL NO
- TOPLAM KURULU GÜÇ (KVA)
- EKLENEN GÜÇ (KVA)
- ESKİ T.GÜÇ (KVA)
- ENERJİ MÜSADESİ SAYI VE TARİHİ
- GÖREV ID
- DYS ONAY NO
- VERGİ D. ve NO.
- PROJE MÜELLİFİ / SORUMLU İMZA VE KAŞE
- SMM NO / BT.NO
- ODA / Elektrik Dağıtım Şirketi (EDŞ) onay bilgileri

### 8. Çizim Kuralları Özeti

1. **Katman Ayrımı**: Her disiplin (aydınlatma, priz, telefon, tv, data, yangın, topraklama, UPS, acil) kendi katmanında çizilir.
2. **Renk Standardı**: Aydınlatma = yeşil(3), Priz = kırmızı(1-12), Telefon = magenta(6), TV = mavi(4), Yangın = kırmızı(1), Topraklama = turuncu(44).
3. **Blok Kullanımı**: Her armatür, priz, anahtar, dedektör vb. standart blok olarak INSERT edilir — ham çizgi ile çizilmez.
4. **Kombine Kutular**: Birden fazla priz/data/telefon/UPS aynı kutuda ise özel kombine blok kullanılır (ör: `2U1S1D1T`).
5. **Kablo Etiketleri**: Her hat üzerinde kablo tipi ve kesiti TEXT olarak yazılır (ör: "4x4 N2XH KABLO").
6. **Tek Hat Şeması**: Her projede mutlaka tek hat şeması bulunur; pano detayları, şalter değerleri, KAR hassasiyetleri belirtilir.
7. **Topraklama**: İşletme ve koruma topraklaması ayrı kazıkla yapılır; detay kesiti her projede gösterilir.
8. **Sembol Listesi**: Her paftada sembol listesi tablosu bulunmalıdır (İŞARET | ANLAMI formatında).
9. **Antet**: Her paftada standart antet bloğu ile proje, yaptıran, müellif bilgileri yer alır.
10. **OG Vaziyet Planı**: Abonelik projelerinde trafo, direk, hat güzergahı ve koordinatlar vaziyet planında gösterilir.
11. **Kablo Kanalı**: Yeraltı kabloları için kanal kesit detayı (TİP1-A) çizilir.
12. **Linye Numaralama**: Her aydınlatma ve priz grubu linye numarasıyla etiketlenir.
13. **Mekanik Koordinasyon**: Elektrik projesi, mekanik tesisat (HVAC) elemanlarının elektrik bağlantılarını da içerir (fan coil, VAV, havalandırma motoru vb.).
