# 🎭 Playwright Setup Guide

Bu dokümanda proje için Playwright kurulumu ve kullanımı açıklanmıştır.

## 📋 İçindekiler
- [Playwright Nedir?](#playwright-nedir)
- [Kurulum](#kurulum)
- [Proje Yapısı](#proje-yapısı)
- [Testleri Çalıştırma](#testleri-çalıştırma)
- [Kullanılan Playwright Özellikleri](#kullanılan-playwright-özellikleri)

---

## 🎭 Playwright Nedir?

Playwright, Microsoft tarafından geliştirilen modern web otomasyon framework'ü. 
Selenium'a kıyasla hızlı, güvenilir ve kolay kullanımlıdır.

**Avantajlar:**
- ✅ Daha hızlı test çalışması
- ✅ Daha sağlam element bulma
- ✅ Birden fazla browser tarafından destek (Chromium, Firefox, WebKit)
- ✅ Otomatik waiters
- ✅ Headless mode varsayılan

---

## 🔧 Kurulum

### 1. Python Gereksinimleri

Python 3.8+ gereklidir.

### 2. Paket Yükleme

```bash
# Tüm gereksinimleri yükle
pip install -r requirements.txt

# veya manuel olarak
pip install playwright>=1.40.0
pip install pytest>=7.0.0
pip install pytest-html>=4.0.0
pip install PyYAML>=6.0
```

### 3. Playwright Browser'larını Yükle

```bash
# Tüm browser'ları yükle
playwright install

# veya sadece belirli browser'ları yükle
playwright install chromium
playwright install firefox
playwright install webkit
```

---

## 📁 Proje Yapısı

```
automation_test_kamilesor/
│
├── 📄 config.py                    # Konfigürasyon (BASE_URL, timeouts, vb.)
├── 📄 requirements.txt             # Python paketleri
├── 📄 pytest.ini                   # Pytest ayarları
├── 📄 run_tests.bat                # Test çalıştırma script'i
├── 📄 run_specific_yaml.py         # YAML test çalıştırıcısı
│
├── 📁 pages/                       # Page Object Model
│   ├── base_page.py               # Tüm page'ların inherit ettiği base sınıf
│   ├── login_page.py              # Login page işlemleri
│   ├── registration_page.py       # Kayıt işlemleri
│   └── chat_page.py               # Chat işlemleri
│
├── 📁 utils/                       # Yardımcı araçlar
│   ├── driver_helper.py           # Playwright driver yönetimi
│   ├── yaml_helper.py             # YAML dosya yönetimi
│   ├── yaml_method_executor.py    # YAML senaryo çalıştırıcısı
│   └── test_data_helper.py        # Test verisi oluşturma
│
├── 📁 tests/                       # Test dosyaları
│   ├── conftest.py                # Pytest fixtures
│   ├── test_runner.py             # Generic test runner
│   └── test_chat_with_doctor.py   # Spesifik testler
│
└── 📁 scenarios/                   # YAML test senaryoları
    ├── TC_001_registration.yaml
    ├── TC_002_login.yaml
    ├── TC_003_chat_with_doctor.yaml
    └── TC_004_chat_with_it.yaml
```

---

## ▶️ Testleri Çalıştırma

### 1. Tüm Testleri Çalıştır

```bash
# Windows
run_tests.bat

# Linux/Mac
python -m pytest tests/ -v -s
```

### 2. Belirli Bir YAML Dosyasını Çalıştır

```bash
python run_specific_yaml.py scenarios/TC_002_login.yaml
```

### 3. Belirli Bir Test Dosyasını Çalıştır

```bash
python -m pytest tests/test_chat_with_doctor.py -v -s
```

### 4. Headless Modu Devre Dışı Bırak (Tarayıcı Görünür)

```bash
# config.py'de değiştir:
HEADLESS = False
```

### 5. Slow Mo Ekle (Debug için)

```bash
# config.py'de değiştir (millisecond):
SLOW_MO = 500  # 500ms delay
```

---

## 🎯 Kullanılan Playwright Özellikleri

### 1. Browser Yönetimi (`utils/driver_helper.py`)

```python
# Browser başlat
browser = get_browser()

# Page oluştur
page = get_page(browser)

# Browser kapat
close_browser(browser)
```

### 2. Element Bulma ve İşlem (`pages/base_page.py`)

```python
# Element bul
locator = self.find_element("input[name='email']")

# Element'e tıkla
self.click_element("button[type='submit']")

# Text gir
self.input_text("input[name='password']", "password123")

# Text al
text = self.get_text("h1")

# Element görünür mü?
is_visible = self.is_element_visible("div.success")
```

### 3. Waiters (Otomatik Bekleme)

```python
# Element görünür olana kadar bekle (Playwright otomatik yapar)
locator.wait_for(state="visible", timeout=15000)

# URL değişimini bekle
page.wait_for_url("/dashboard")

# Selector'u bekle
page.wait_for_selector("div.notification")
```

### 4. Navigation

```python
# Sayfaya git
page.goto("https://kamilesor.com")

# Mevcut URL al
url = page.url

# Geri git
page.go_back()

# İleri git
page.go_forward()
```

### 5. Screenshot

```python
# Ekran görüntüsü al
page.screenshot(path="screenshot.png")
```

### 6. Keyboard Olayları

```python
# Enter tuşuna bas
page.press("input[name='search']", "Enter")

# Tab tuşuna bas
page.press("input", "Tab")
```

---

## ⚙️ Konfigürasyon (`config.py`)

```python
BASE_URL = "https://kamilesor.com"     # Test edilecek site
BROWSER = "chromium"                   # chromium, firefox, webkit
HEADLESS = False                       # True = görünmez mod
VIEWPORT_WIDTH = 1920                  # Browser genişliği
VIEWPORT_HEIGHT = 1080                 # Browser yüksekliği

# Timeouts (millisecond)
EXPLICIT_WAIT = 15000                  # Element bekleme süresi
NAVIGATION_TIMEOUT = 30000             # Sayfa yükleme süresi
```

---

## 📝 YAML Senaryo Yazma Örneği

```yaml
# scenarios/TC_002_login.yaml
scenarios:
  - name: "Successful Login Flow"
    description: "Valid credentials ile giriş yap"
    page: "LoginPage"
    method: "execute_successful_login_flow"
    params:
      email: "test@example.com"
      password: "password123"
      base_url: "https://kamilesor.com"
```

---

## 🐛 Debugging İpuçları

### 1. Verbose Output

```bash
python -m pytest tests/ -v -s
```

### 2. Headless Modu Kapat

```python
# config.py
HEADLESS = False
```

### 3. Daha Yavaş Çalıştır (Debug)

```python
# config.py
SLOW_MO = 1000  # 1 saniye delay
```

### 4. Ekran Görüntüsü Al

```python
self.take_screenshot("debug.png")
```

### 5. Log Yazma

```python
print("✓ Element bulundu")
print("✅ Test başarılı")
print("❌ Test başarısız")
```

---

## 🤝 Faydalı Linkler

- [Playwright Python Docs](https://playwright.dev/python/)
- [Playwright API](https://playwright.dev/python/docs/api/class-browser)
- [Selectors Guide](https://playwright.dev/python/docs/selectors)

---

## ✅ Kontrol Listesi

- [ ] Python 3.8+ yüklü mü?
- [ ] `requirements.txt` kuruldu mu?
- [ ] Playwright browser'ları yüklendi mi? (`playwright install`)
- [ ] `config.py` düzenlendi mi?
- [ ] `run_tests.bat` çalışıyor mu?
- [ ] Test raporları oluşuyor mu?

---

**Başarılar! 🎉**
