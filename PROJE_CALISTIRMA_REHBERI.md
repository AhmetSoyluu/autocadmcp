# AutoCAD MCP Projesi Çalıştırma Rehberi

Bu doküman, `autocadmcp` projesini yerel ortamda kurup çalıştırmak için gerekli adımları içerir.

## 1) Ön Gereksinimler

- Python 3.10+ (önerilir)
- Windows ortamı (AutoCAD otomasyonu için)
- `pip`

## 2) Proje Dizinine Geçiş

```bash
cd C:/Users/asoyl/OneDrive/Masaüstü/projes/autocadmcp
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

## 5) MCP Sunucusunu Çalıştırma

```bash
python -m autocad_mcp_server.main
```

## 6) Testleri Çalıştırma

Tüm testler:

```bash
pytest
```

Sadece entegrasyon testleri:

```bash
pytest -m integration
```

Tek bir test dosyası:

```bash
pytest tests/unit/test_path_sandbox.py
```

Belirli bir test adı ile:

```bash
pytest tests/unit/test_lisp_policy.py -k test_rejects_shell_primitives
```

## 7) Kod Kalite Kontrolleri

Lint:

```bash
ruff check .
```

Tip kontrolü:

```bash
mypy src
```

Coverage:

```bash
pytest --cov=autocad_mcp_server --cov-report=term-missing
```

## 8) Kısa Mimari Notu

- Giriş noktası: `src/autocad_mcp_server/main.py`
- Tool katmanı: `src/autocad_mcp_server/tools/`
- İş mantığı: `src/autocad_mcp_server/services/dwg_service.py`
- COM tabanlı canlı AutoCAD yürütme:
  - `src/autocad_mcp_server/services/interop_manager.py`
  - `src/autocad_mcp_server/adapters/com_adapter.py`
- Core Console (arka plan) yürütme:
  - `src/autocad_mcp_server/services/core_console_manager.py`
  - `src/autocad_mcp_server/adapters/core_console_adapter.py`
- Güvenlik katmanı:
  - Yol denetimi: `src/autocad_mcp_server/security/path_sandbox.py`
  - AutoLISP politika denetimi: `src/autocad_mcp_server/security/lisp_policy.py`

## 9) Sık Karşılaşılan Sorunlar

- Sanal ortam aktif değilse komutlar başarısız olabilir. Önce `.venv\Scripts\activate` çalıştırın.
- `pip install -e .[dev]` hatası alırsanız Python ve pip sürümünü kontrol edin.
- AutoCAD/COM tarafı sorunlarında, sunucunun log çıktısını inceleyin.

---

İsterseniz bir sonraki adımda bu dosyayı `README.md` içinden linkleyebilirim.