# 🧪 Kamile Sor Test Otomasyonu

Playwright ve Python kullanarak geliştirilmiş YAML-tabanlı test otomasyon framework'ü.

**Sürüm:** 5.0 (Playwright + YAML Method Executor)  
**Durum:** ✅ Aktif

---

## 🎯 Ana Özellikler

- ✅ **YAML-Driven Tests** - Testleri YAML'da tanımla, kod yazmadan test et
- ✅ **Page Object Model** - Sürdürülebilir ve ölçeklenebilir yapı
- ✅ **Method Execution Engine** - Page metodlarını YAML'dan çağır
- ✅ **Playwright** - Modern, hızlı ve güvenilir browser automation
- ✅ **Dinamik Parametreler** - `{{config.BASE_URL}}`, `{{config.LOGIN_USER}}` vb.
- ✅ **Modüler Yapı** - Her test senaryosu ayrı YAML dosyası
- ✅ **Cross-browser** - Chromium, Firefox, WebKit desteği

---

## 📁 Proje Yapısı

```
automation_test_kamilesor/
│
├── scenarios/                            # 📝 Test Senaryoları (YAML)
│   ├── TC_001_registration_scenarios.yaml
│   ├── TC_002_login.yaml
│   ├── TC_003_chat_with_doctor.yaml
│   └── TC_004_chat_with_it_specialist.yaml
│
├── pages/                                # 🎭 Page Object Model
│   ├── __init__.py
│   ├── base_page.py                     # Temel page class (tüm ortak metodlar)
│   ├── login_page.py                    # Login sayfası + flow metodları
│   ├── chat_page.py                     # Chat sayfası + mesaj metodları
│   └── registration_page.py             # Kayıt sayfası
│
├── utils/                                # 🔧 Yardımcı Araçlar
│   ├── __init__.py
│   ├── driver_helper.py                 # Playwright browser yönetimi
│   ├── yaml_helper.py                   # YAML parser & loader
│   ├── yaml_method_executor.py          # ⭐ Method execution engine
│   └── test_data_helper.py              # Test verisi oluşturma
│
├── tests/                                # 🧪 Test Runner (pytest)
│   ├── __init__.py
│   ├── conftest.py                      # Pytest fixtures
│   └── test_runner.py                   # YAML test runner
│
├── config.py                            # ⚙️ Konfigürasyon
├── requirements.txt                     # 📦 Bağımlılıklar
├── pytest.ini                           # Pytest ayarları
├── run_specific_yaml.py                 # ⭐ YAML test runner script
└── README.md                            # Bu dosya
```

---

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler

- Python 3.9 veya üzeri
- pip (Python package manager)

### 2. Kurulum

```bash
# Bağımlılıkları yükle
pip3 install -r requirements.txt

# Playwright tarayıcılarını yükle
python3 -m playwright install
```

### 3. Konfigürasyon

`config.py` dosyasında ayarları yapılandırın:

```python
BASE_URL = "https://kamilesor.com"
BROWSER = "webkit"              # chromium, firefox, webkit
HEADLESS = False                # True: Headless mode
LOGIN_USER = "your@email.com"
LOGIN_PASSWORD = "yourpassword"
```

### 4. Test Çalıştırma

```bash
# Belirli bir YAML senaryosunu çalıştır
python3 run_specific_yaml.py scenarios/TC_002_login.yaml

# Chat senaryosunu çalıştır
python3 run_specific_yaml.py scenarios/TC_003_chat_with_doctor.yaml

# IT specialist senaryosunu çalıştır
python3 run_specific_yaml.py scenarios/TC_004_chat_with_it_specialist.yaml
```

---

## 📝 YAML Senaryo Yapısı

### Temel Format

```yaml
test_scenarios:
  category_name:
    - name: "scenario_name"
      description: "Senaryo açıklaması"
      enabled: true
      page: "PageClassName"              # LoginPage, ChatPage, vb.
      method: "method_name"               # Çalıştırılacak metod
      params:                             # Metod parametreleri
        email: "{{config.LOGIN_USER}}"
        password: "{{config.LOGIN_PASSWORD}}"
      wait_time: 5                        # Senaryo sonrası bekleme (saniye)
```

### Örnek: Login Senaryosu

```yaml
test_scenarios:
  login:
    - name: "successful_login"
      description: "Kullanıcı başarılı giriş yapar"
      enabled: true
      page: "LoginPage"
      method: "execute_successful_login_flow"
      params:
        base_url: "{{config.BASE_URL}}"
        email: "{{config.LOGIN_USER}}"
        password: "{{config.LOGIN_PASSWORD}}"
      wait_time: 5
```

### Örnek: Chat Senaryosu

```yaml
test_scenarios:
  chat:
    - name: "chat_with_doctor"
      description: "Doktorla mesajlaşma testi"
      enabled: true
      page: "ChatPage"
      method: "send_message_to_doctor1"
      wait_time: 20
```

---

## 🎭 Page Object Model

### BasePage

Tüm page sınıflarının miras aldığı temel sınıf. Ortak metodları içerir:

- `click_element(selector)` - Element'e tıkla
- `input_text(selector, text)` - Text gir
- `is_element_visible(selector)` - Element görünür mü?
- `wait_for_selector(selector)` - Element bekle
- `navigate(url)` - URL'ye git
- `take_screenshot(filename)` - Screenshot al

### LoginPage

Giriş sayfası işlemleri:

```python
def execute_successful_login_flow(self, email, password, base_url):
    """Başarılı giriş akışını gerçekleştir"""
    self.page.goto(base_url)
    self.click_login_link()
    self.fill_login_form(email, password)
    self.submit_login()
    return self.is_login_successful()
```

### ChatPage

Chat sayfası işlemleri:

```python
def send_message_to_doctor1(self, message: str = None):
    """Doktora ilk mesajı gönder"""
    self.click_doctor_button()
    msg = message if message else self.MESSAGE_TO_DOCTOR1
    self.enter_message(msg)
    self.click_send_button()
    return True
```

---

## 🔧 YAML Method Executor

`yaml_method_executor.py` - YAML'da tanımlı metodları dinamik olarak çalıştırır.

### Nasıl Çalışır?

1. YAML'dan senaryo bilgilerini al (page, method, params)
2. Page class'ını dinamik olarak import et
3. Page instance'ı oluştur
4. Metodu parametrelerle çalıştır
5. Sonucu değerlendir (success/failure)

### Dinamik Parametreler

```yaml
params:
  base_url: "{{config.BASE_URL}}"          # config.py'den değer al
  email: "{{config.LOGIN_USER}}"
  password: "{{config.LOGIN_PASSWORD}}"
  message: "{{ChatPage.MESSAGE_TO_DOCTOR1}}" # Page sabitinden al
```

---

## 📊 Test Sonuçları

Test tamamlandığında detaylı özet gösterilir:

```
================================================================================
📊 TEST ÖZETI
================================================================================
✅ Başarılı: 2
❌ Başarısız: 0
📋 Toplam: 2

--------------------------------------------------------------------------------
Detaylı Sonuçlar:
--------------------------------------------------------------------------------

✅ execution_login
   Status: PASSED
   Mesaj: Senaryo başarılı: execution_login

✅ chat_with_doctor1
   Status: PASSED
   Mesaj: Senaryo başarılı: chat_with_doctor1
```

---

## 🛠️ Yeni Senaryo Ekleme

### 1. Page Metodunu Oluştur

```python
# pages/chat_page.py
def send_message_to_teacher(self, message: str = None):
    """Öğretmene mesaj gönder"""
    self.click_teacher_button()
    msg = message if message else self.MESSAGE_TO_TECHER1
    self.enter_message(msg)
    self.click_send_button()
    return True  # Başarı durumunu döndür
```

### 2. YAML Senaryosu Ekle

```yaml
# scenarios/TC_005_chat_with_teacher.yaml
test_scenarios:
  chat:
    - name: "execution_login"
      description: "Kullanıcı girişi"
      enabled: true
      page: "LoginPage"
      method: "execute_successful_login_flow"
      params:
        base_url: "{{config.BASE_URL}}"
        email: "{{config.LOGIN_USER}}"
        password: "{{config.LOGIN_PASSWORD}}"
      wait_time: 5

    - name: "chat_with_teacher"
      description: "Öğretmenle mesajlaşma"
      enabled: true
      page: "ChatPage"
      method: "send_message_to_teacher"
      wait_time: 20
```

### 3. Testi Çalıştır

```bash
python3 run_specific_yaml.py scenarios/TC_005_chat_with_teacher.yaml
```

---

## 🎯 Mevcut Test Senaryoları

| Test Dosyası | Açıklama | Senaryolar |
|--------------|----------|------------|
| `TC_001_registration_scenarios.yaml` | Kayıt testleri | Kullanıcı kaydı |
| `TC_002_login.yaml` | Giriş testleri | Başarılı giriş |
| `TC_003_chat_with_doctor.yaml` | Doktor chat testleri | 2 mesaj senaryosu |
| `TC_004_chat_with_it_specialist.yaml` | IT uzmanı chat testleri | 2 mesaj senaryosu |

---

## 🐛 Sorun Giderme

### Playwright Tarayıcıları Yüklenmemiş

```bash
python3 -m playwright install
```

### Element Bulunamıyor

- Locator'ları kontrol edin (pages/*.py)
- `config.py` içinde timeout değerlerini artırın
- Headless mode'u kapatın (`HEADLESS = False`)

### YAML Parse Hatası

- YAML indentation'ı kontrol edin (2 boşluk kullanın)
- Kategori adının doğru olduğundan emin olun (`chat:`, `login:`, vb.)

### Metod Bulunamadı Hatası

- Page class adının doğru olduğundan emin olun (örn: `LoginPage`)
- Metod adının page class'ında tanımlı olduğunu kontrol edin
- Metodun `return True` döndürdüğünden emin olun

---

## 📚 Kullanılan Teknolojiler

- **Python 3.9+** - Programlama dili
- **Playwright** - Browser automation
- **PyYAML** - YAML parser
- **pytest** - Test framework (opsiyonel)

---

## 🔍 Playwright vs Selenium

| Özellik | Playwright | Selenium |
|---------|-----------|----------|
| Hız | ⚡ Çok Hızlı | 🐢 Orta |
| Modern API | ✅ Evet | ❌ Hayır |
| Auto-wait | ✅ Evet | ❌ Manuel |
| Cross-browser | ✅ 3 Engine | ✅ Birçok |
| Headless | ✅ Native | ⚠️ Sınırlı |
| Screenshot | ✅ Gelişmiş | ⚠️ Basit |

---

## 📞 Hızlı Referans

```bash
# Tüm bağımlılıkları yükle
pip3 install -r requirements.txt

# Playwright tarayıcıları yükle
python3 -m playwright install

# Belirli senaryoyu çalıştır
python3 run_specific_yaml.py scenarios/TC_002_login.yaml

# Tüm testleri çalıştır (pytest ile)
pytest tests/test_runner.py -v -s

# Config dosyasını düzenle
nano config.py
```

---

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

---

## 📄 Lisans

Bu proje test ve eğitim amaçlı geliştirilmiştir.

---

**Sürüm:** 5.0  
**Son Güncelleme:** Ocak 2026  
**Status:** ✅ Aktif & Maintaining

**Geliştirici:** Hasan Gültekin  
**Proje:** Kamile Sor Test Automation Framework
