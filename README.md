# AutoCAD MCP Server

AutoCAD MCP Server, AutoCAD ile MCP (Model Context Protocol) üzerinden etkileşim kurmanızı sağlayan bir Windows odaklı sunucudur. DWG dosyalarıyla canlı AutoCAD oturumu (COM Interop) veya arka planda `accoreconsole.exe` ile çalışabilir.

Python kullanılmasının nedeni, Windows COM otomasyonunun `pywin32` ile daha olgun ve kararlı olması, aynı runtime'ın `accoreconsole.exe` süreçlerini, zaman aşımlarını, geçici çalışma alanlarını ve yol kısıtlamalarını daha az entegrasyon yüküyle yönetebilmesidir.

## Özellikler

Sunucu dört MCP aracı sunar:

- **`read_dwg_metadata`** — Katmanlar, blok referansları, metin/mtext içeriği ve çizim özetini JSON olarak döndürür.
- **`execute_autolisp`** — Politika denetiminden geçmiş AutoLISP kodunu canlı oturumda veya arka plan konsolunda çalıştırır.
- **`query_geometry`** — Varlık koordinatlarını, sınırlayıcı kutuları, uzunlukları ve alanları döndürür.
- **`manage_layers_and_blocks`** — Katman oluşturur/değiştirir ve doğrulanmış parametrelerle blok ekler.

## Güvenlik Modeli

Bu sunucu kasıtlı olarak kısıtlayıcıdır:

- Yalnızca yapılandırılmış izinli kök dizinler altındaki DWG dosyaları açılabilir.
- Tüm gelen yollar, yol traversali ve sandbox kaçış girişimlerine karşı normalize edilir ve doğrulanır.
- Core Console işleri, süreç çakışmalarını önlemek için tek bir kuyruk üzerinden çalışır.
- AutoLISP yürütmesi, yerleşik politika denetimlerinden geçmezse engellenir.

## Gereksinimler

- Windows 10 veya 11
- Python 3.11+
- AutoCAD kurulu olmalı (`acad.exe` ve `accoreconsole.exe`)
- Git

## Hızlı Kurulum

```bash
# 1. Projeyi klonla
git clone https://github.com/AhmetSoyluu/autocadmcp.git
cd autocadmcp

# 2. Sanal ortam oluştur
python -m venv .venv
.venv\Scripts\activate

# 3. Bağımlılıkları kur
pip install -e .[dev]

# 4. Ortam değişkenlerini ayarla
copy .env.example .env
# .env dosyasını düzenleyerek AutoCAD yollarını kendi sistemine göre ayarla

# 5. Sunucuyu çalıştır
python -m autocad_mcp_server.main
```

## Claude Desktop ile Kullanım

### Yöntem 1: Proje `.mcp.json` (Önerilen)

Proje kökünde `.mcp.json` oluşturun (şablon için `docs/mcp.example.json` dosyasına bakın):

```json
{
  "mcpServers": {
    "autocad-mcp-server": {
      "type": "stdio",
      "command": "C:\\path\\to\\your\\.venv\\Scripts\\python.exe",
      "args": ["-m", "autocad_mcp_server.main"],
      "env": {
        "PYTHONPATH": "C:\\path\\to\\your\\project\\src",
        "AUTOCAD_MCP_ALLOWED_DWG_ROOTS": "C:\\CAD\\Projects",
        "AUTOCAD_MCP_ACAD_PATH": "C:\\Program Files\\Autodesk\\AutoCAD 2025\\acad.exe",
        "AUTOCAD_MCP_ACCORECONSOLE_PATH": "C:\\Program Files\\Autodesk\\AutoCAD 2025\\accoreconsole.exe"
      }
    }
  }
}
```

### Yöntem 2: Claude Desktop Global Ayarları

`%APPDATA%\Claude\claude_desktop_config.json` dosyasını düzenleyin:

```json
{
  "mcpServers": {
    "autocad-mcp-server": {
      "command": "C:\\path\\to\\your\\.venv\\Scripts\\python.exe",
      "args": ["-m", "autocad_mcp_server.main"]
    }
  }
}
```

Detaylı şablon: `docs/claude_desktop_config.example.json`

## Testler

```bash
# Tüm testler
pytest

# Sadece birim testleri
pytest tests/unit/

# Entegrasyon testleri (AutoCAD gerekli)
pytest -m integration
```

## Daha Fazla Bilgi

Detaylı kurulum ve çalıştırma rehberi için: [PROJE_CALISTIRMA_REHBERI.md](PROJE_CALISTIRMA_REHBERI.md)

## Mimari

Sunucu, tool katmanını ince tutar. MCP araçları yapılandırılmış istekleri doğrular, ardından `DWGService`'e devreder. `DWGService`, COM veya Core Console kullanımına karar verir. Yol doğrulama `security/path_sandbox.py`'de, AutoLISP denetimi `security/lisp_policy.py`'de merkezileştirilmiştir. Core Console yürütmesi `services/execution_queue.py` ve `services/core_console_manager.py` üzerinden serileştirilir. Canlı AutoCAD erişimi `services/interop_manager.py` ve `adapters/com_adapter.py`'de izole edilmiştir.
