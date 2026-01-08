# 🚀 Playwright Kurulum ve Başlangıç Rehberi

Bu rehber projeyi Playwright ile çalıştırmaya hazırlamak için adım adım talimatlar içerir.

## ✅ Yapılan Değişiklikler

Proje **Selenium'dan Playwright'a** başarıyla geçirilmiştir:

### 1. Paket Gereksinimleri Güncellendi
- ✅ `playwright>=1.40.0` eklendi
- ✅ `pytest-playwright` eklendi
- ✅ `python-dotenv` eklendi
- ✅ Tüm paketler en son versiyon

### 2. Dosyalar Güncellendi
- ✅ `driver_helper.py` - Playwright API ile güncellendi
- ✅ `base_page.py` - Playwright locators ve metodları
- ✅ `run_specific_yaml.py` - Selenium referansları kaldırıldı
- ✅ `run_tests.bat` - Playwright güncellemeleri
- ✅ `config.py` - Playwright-specific ayarlar eklendi

### 3. Documentation Eklendi
- ✅ `PLAYWRIGHT_SETUP.md` - Kapsamlı setup rehberi
- ✅ `README.md` - Başlık "Playwright" olarak güncellendi

---

## 🔧 Kurulum Adımları

### Adım 1: Python Paketlerini Yükle

```bash
cd c:\seleniumPython\automation_test_kamilesor

# Tüm gereksinimleri yükle
pip install -r requirements.txt
```

### Adım 2: Playwright Browser'larını Yükle

```bash
# Tüm browser'ları indir
playwright install

# VEYA sadece Chromium (önerilen)
playwright install chromium
```

### Adım 3: Konfigürasyon Doğrula

`config.py` dosyasında aşağıdaki ayarları kontrol et:

```python
BASE_URL = "https://kamilesor.com"
BROWSER = "chromium"              # chromium, firefox, webkit
HEADLESS = False                  # Hata debug için False yapabilirsin
SLOW_MO = 0                       # Debug için millisecond artır
```

---

## ▶️ Testleri Çalıştırma

### 1️⃣ Windows Batch Script ile (Kolay)

```batch
cd c:\seleniumPython\automation_test_kamilesor
run_tests.bat
```

### 2️⃣ Komut Satırı ile (Kontrollü)

```bash
# Tüm testleri çalıştır
python -m pytest tests/ -v -s

# Belirli test dosyasını çalıştır
python -m pytest tests/test_chat_with_doctor.py -v -s

# YAML senaryo çalıştır
python run_specific_yaml.py scenarios/TC_002_login.yaml
```

### 3️⃣ Debug Modu ile (Hata giderme)

```bash
# Tarayıcıyı görünür yap
# config.py'de HEADLESS = False yap

# Daha yavaş çalıştır (1 saniye delay)
# config.py'de SLOW_MO = 1000 yap

# Sonra çalıştır
python -m pytest tests/ -v -s
```

---

## 📁 Proje Dosya Hiyerarşisi

```
✅ automation_test_kamilesor/
   ├── ✅ config.py                   (Playwright ayarları)
   ├── ✅ requirements.txt            (Güncel paketler)
   ├── ✅ pytest.ini                  (Test config)
   ├── ✅ run_tests.bat               (Batch runner)
   ├── ✅ run_specific_yaml.py        (Playwright uyumlu)
   │
   ├── 📁 pages/
   │   ├── ✅ base_page.py            (Playwright metodları)
   │   ├── ✅ login_page.py           (Playwright uyumlu)
   │   ├── ✅ registration_page.py    (Playwright uyumlu)
   │   └── ✅ chat_page.py            (Playwright uyumlu)
   │
   ├── 📁 utils/
   │   ├── ✅ driver_helper.py        (Playwright API)
   │   ├── ✅ yaml_helper.py          (Uyumlu)
   │   ├── ✅ yaml_method_executor.py (Uyumlu)
   │   └── ✅ test_data_helper.py     (Uyumlu)
   │
   ├── 📁 tests/
   │   ├── ✅ conftest.py             (Playwright fixtures)
   │   ├── ✅ test_runner.py          (Playwright uyumlu)
   │   └── ✅ test_chat_with_doctor.py
   │
   └── 📁 scenarios/
       ├── TC_001_registration.yaml
       ├── TC_002_login.yaml
       ├── TC_003_chat_with_doctor.yaml
       └── TC_004_chat_with_it.yaml
```

---

## 🎯 Test Başarısını Doğrulama

Testler başarılı çalışıyor mu kontrol et:

```bash
# Çalıştır
python -m pytest tests/ -v -s

# Aşağıdakini ara çıktıda:
# ✓ Browser başlatıldı: chromium
# ✓ Page oluşturuldu: 1920x1080
# ✅ BAŞARILI (tüm testler)
# ✓ Browser kapatıldı
```

---

## ⚙️ Playwright vs Selenium - Farklar

| Özellik | Selenium | **Playwright** |
|---------|----------|---|
| API | Daha eski | Modern ve sade |
| Hız | Daha yavaş | ⚡ Çok hızlı |
| Stabilite | Bazen timeouts | Daha sağlam |
| Multi-browser | Sınırlı | Chromium, Firefox, WebKit |
| Auto-wait | Manuel wait gerekli | Otomatik wait |
| Headless | Seçeneğe göre | Varsayılan |

---

## 🆘 Sorun Giderme

### Problem: "ModuleNotFoundError: No module named 'playwright'"

**Çözüm:**
```bash
pip install playwright
```

### Problem: "Browser not found"

**Çözüm:**
```bash
playwright install chromium
```

### Problem: "Timeout waiting for selector"

**Çözüm:**
- `config.py`'de `EXPLICIT_WAIT` artır: `EXPLICIT_WAIT = 30000`
- `HEADLESS = False` yaparak tarayıcıyı görün

### Problem: "Element is not clickable"

**Çözüm:**
```python
# config.py'de SLOW_MO ekle
SLOW_MO = 1000  # 1 saniye

# Veya base_page.py'de bekle
self.wait(2)
```

---

## 📚 Faydalı Kaynaklar

- 📖 [Playwright Python Docs](https://playwright.dev/python/)
- 🎥 [Playwright Video Tutorials](https://www.youtube.com/results?search_query=playwright+python)
- 💬 [Playwright GitHub Issues](https://github.com/microsoft/playwright-python/issues)

---

## ✨ Sonraki Adımlar (Opsiyonel)

1. **Video Kayıt Ekle** (`config.py`'de `RECORD_VIDEO = True`)
2. **Trace Kayıt Ekle** (`config.py`'de `RECORD_TRACE = True`)
3. **Parallel Test Çalıştırma** (`pytest-xdist` paketi)
4. **API Mocking** (`pytest-mock`)

---

## 🎉 Tebrikler!

Projeniz artık **Playwright ile tam uyumlu**! 

Test etmeye başla:

```bash
python run_tests.bat
```

**İyi test yazmaları dilerim! 🚀**
