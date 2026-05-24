# AutoCAD MCP Projesi Çalıştırma Rehberi

Bu doküman, `autocadmcp` projesini yerel ortamda kurup çalıştırmak için gerekli adımları içerir.

## 1) Ön Gereksinimler

- Python 3.10+ (önerilir 3.11+)
- Windows 10 veya 11 (AutoCAD otomasyonu için)
- AutoCAD kurulu olmalı (`acad.exe` ve `accoreconsole.exe`)
- `pip` (Python paket yöneticisi)

## 2) Projeyi Klonlama

```bash
git clone https://github.com/AhmetSoyluu/autocadmcp.git
cd autocadmcp
```

## 3) Sanal Ortam Oluşturma ve Aktifleştirme

```bash
python -m venv .venv
.venv\Scripts\activate
```

## 4) Bağımlılıkları Kurma

```bash
pip install -e .[dev]
```

## 5) Ortam Değişkenlerini Ayarlama

```bash
copy .env.example .env
```

Ardından `.env` dosyasını açarak AutoCAD yollarını kendi sisteminize göre düzenleyin:

| Değişken | Açıklama | Örnek |
|---|---|---|
| `AUTOCAD_MCP_ACAD_PATH` | AutoCAD yürütülebilir dosya yolu | `C:\Program Files\Autodesk\AutoCAD 2025\acad.exe` |
| `AUTOCAD_MCP_ACCORECONSOLE_PATH` | Core Console yolu | `C:\Program Files\Autodesk\AutoCAD 2025\accoreconsole.exe` |
| `AUTOCAD_MCP_ALLOWED_DWG_ROOTS` | İzin verilen DWG klasörleri (; ile ayrılır) | `C:\CAD\Projects` |
| `AUTOCAD_MCP_PROFILE_ROOT` | Profil verileri ana dizini | `C:\ProgramData\autocadmcp` |

## 6) MCP Sunucusunu Çalıştırma

```bash
python -m autocad_mcp_server.main
```

Veya yüklenen giriş noktası ile:

```bash
autocad-mcp-server
```

## 7) Claude Desktop ile Entegrasyon

### Seçenek A: `.mcp.json` (Önerilen)

Proje kök dizininde `.mcp.json` dosyası oluşturun:

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

> **Not:** `.mcp.json` kişisel bilgisayar yol bilgileri içerdiği için `.gitignore`'a eklenmiştir. Örnek şablon için `docs/mcp.example.json` dosyasına bakın.

### Seçenek B: Claude Desktop Global Ayarları

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

Detaylı şablon için: `docs/claude_desktop_config.example.json`

## 8) Testleri Çalıştırma

Tüm testler:

```bash
pytest
```

Sadece birim testleri:

```bash
pytest tests/unit/
```

Sadece entegrasyon testleri (AutoCAD kurulu olmalı):

```bash
pytest -m integration
```

Tek bir test dosyası:

```bash
pytest tests/unit/test_path_sandbox.py
```

## 9) Kod Kalite Kontrolleri

Lint:

```bash
ruff check .
```

Tip kontrolü:

```bash
mypy src
```

Test coverage:

```bash
pytest --cov=autocad_mcp_server --cov-report=term-missing
```

## 10) Kısa Mimari Notu

| Katman | Dizin / Dosya | Açıklama |
|---|---|---|
| Giriş noktası | `src/autocad_mcp_server/main.py` | MCP sunucu başlatma |
| Tool katmanı | `src/autocad_mcp_server/tools/` | MCP tool tanımları |
| İş mantığı | `src/autocad_mcp_server/services/dwg_service.py` | DWG işlemleri |
| COM (Canlı AutoCAD) | `src/autocad_mcp_server/services/interop_manager.py` | COM yönetimi |
| Core Console (Arka plan) | `src/autocad_mcp_server/services/core_console_manager.py` | Console yönetimi |
| Güvenlik - Yol | `src/autocad_mcp_server/security/path_sandbox.py` | Yol doğrulama |
| Güvenlik - LISP | `src/autocad_mcp_server/security/lisp_policy.py` | LISP politika denetimi |

## 11) Sık Karşılaşılan Sorunlar

| Sorun | Çözüm |
|---|---|
| Sanal ortam aktif değil | `.venv\Scripts\activate` çalıştırın |
| `pip install -e .[dev]` hatası | Python ve pip sürümünü kontrol edin |
| AutoCAD/COM bağlantı hatası | Sunucu loglarını inceleyin, AutoCAD'in kurulu olduğundan emin olun |
| `accoreconsole.exe` bulunamadı | `.env` dosyasındaki yolları kontrol edin |
| MCP bağlantı hatası | `.mcp.json` veya Claude config dosyasındaki yolları kontrol edin |
