# 🧪 Kamile Sor Test Otomasyonu (Playwright)

Playwright, Python ve **YAML-Driven Testing** kullanarak geliştirilmiş kapsamlı test otomasyon framework'ü.

**Sürüm:** 4.0 (Playwright)  
**Durum:** ✅ Aktif

---

## 🎯 Ana Özellikler

- ✅ **YAML-Driven Tests** - Testleri YAML'da tanımla, kod yazma!
- ✅ **Page Object Model** - Sürdürülebilir ve ölçeklenebilir yapı
- ✅ **Otomatik Action Execution** - navigate, fill_form, submit vb.
- ✅ **Dinamik Parametreler** - `{{timestamp}}`, `{{date}}`, `{{random}}`
- ✅ **Assertion Engine** - url_changed, error_message, page_title vb.
- ✅ **HTML Raporları** - pytest-html ile detaylı raporlar
- ✅ **Screenshot Yönetimi** - Hata durumlarında otomatik görüntü
- ✅ **Parametreli Testler** - Aynı senararyoyu farklı datalarla çalıştır

---

## 📁 Proje Yapısı

```
automation_test_kamilesor/
│
├── 📄 test_scenarios.yaml                 ⭐ TEST SENARYOLARı (YAML)
├── 📄 YAML_DRIVEN_TESTING.md              ⭐ YAML TESTING REHBERI
├── 📄 REFACTORING_GUIDE.md                ⭐ REFACTORING DETAILS
│
├── pages/                                 # Page Object Model
│   ├── base_page.py                      # Temel class
│   ├── registration_page.py              # Kayıt sayfası + flow metodları
│   ├── login_page.py                     # Login sayfası + flow metodları
│   └── chat_page.py                      # Chat sayfası
│
├── tests/                                 # Test dosyaları
│   ├── test_1_registration.py            # Registration testleri (YAML + Manual)
│   ├── test_2_login.py                   # Login testleri (YAML + Manual)
│   ├── test_3_doctor_chat.py             # Chat testleri
│   ├── test_yaml_runner.py               # ⭐ GENERIC YAML RUNNER
│   └── screenshots/
│
├── utils/                                 # Yardımcı araçlar
│   ├── driver_helper.py                  # WebDriver yönetimi
│   ├── test_data_helper.py               # Test verisi oluşturma
│   ├── yaml_helper.py                    # YAML parser & loader
│   └── yaml_action_executor.py           # ⭐ ACTION/ASSERTION ENGINE
│
├── config.py                             # Yapılandırma
├── requirements.txt                      # Bağımlılıklar (PyYAML ✅)
├── pytest.ini                            # Pytest config
├── run_tests.bat                         # Test runner script
├── demo_yaml_runner.py                   # Demo script
└── test-reports/                         # HTML raporları
```

---

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
# Bağımlılıkları yükle
py -m pip install -r requirements.txt

# Mevcut testleri listele
py -m pytest tests/test_yaml_runner.py --collect-only
```

### 2. YAML Senaryosu ile Test Çalıştır

```bash
# Tüm YAML senaryolarını çalıştır
py -m pytest tests/test_yaml_runner.py -v -s

# Sadece registration senaryolarını
py -m pytest tests/test_yaml_runner.py::TestYamlScenarios::test_all_registration_scenarios -v -s

# Sadece login senaryolarını
py -m pytest tests/test_yaml_runner.py::TestYamlScenarios::test_all_login_scenarios -v -s

# Batch file ile (Windows)
run_tests.bat
```

### 3. YAML'da Yeni Senaryo Ekle

Dosya: `test_scenarios.yaml`

```yaml
test_scenarios:
  login:
    - name: "my_scenario"
      description: "Benim test senaryom"
      enabled: true
      base_url: "https://kamilesor.com"
      steps:
        - action: "navigate"
          url: "/"
        - action: "click_login_link"
        - action: "fill_login_form"
          email: "user@test.com"
          password: "Pass123"
        - action: "submit_login"
      assertions:
        - type: "url_changed"
          expected_url_contains: "/dashboard"
      wait_time: 5
```

### 4. Test Çalıştır

```bash
# Yeni senaryo otomatik olarak bulunur ve çalışır
py -m pytest tests/test_yaml_runner.py -v -s
```

---

## 📊 İki Çalıştırma Yöntemi

### Yöntem 1: YAML-Driven (⭐ YENİ - Önerilen)

**Dosyalar:**
- `test_scenarios.yaml` - Senaryolar
- `utils/yaml_action_executor.py` - Engine
- `tests/test_yaml_runner.py` - Test runner

**Avantaj:**
- ✅ Kod yazmanız gerekmez
- ✅ YAML değişimi = Otomatik test güncelleme
- ✅ Tekrarlı kod yok
- ✅ Non-technical kullanıma uygun

**Çalıştırma:**
```bash
py -m pytest tests/test_yaml_runner.py -v -s
```

---

### Yöntem 2: Manual (Eski)

**Dosyalar:**
- `tests/test_1_registration.py`
- `tests/test_2_login.py`
- `tests/test_3_doctor_chat.py`

**Avantaj:**
- ✅ Kompleks logik yazabilirsiniz
- ✅ Detaylı kontrol

**Çalıştırma:**
```bash
py -m pytest tests/test_1_registration.py -v -s
py -m pytest tests/test_2_login.py -v -s
```

---

## 🔧 Mevcut Actions ve Assertions

### Actions (Komutlar)
```
✅ navigate(url)                 # URL'ye git
✅ click_login_link()            # Login linkine tıkla
✅ click_signup_link()           # Signup linkine tıkla
✅ fill_login_form(email, password)     # Login formu doldur
✅ fill_registration_form(first_name, last_name, email, password)  # Reg formu doldur
✅ submit_login()                # Login gönder
✅ submit_registration()         # Registration gönder
```

### Assertions (Doğrulamalar)
```
✅ url_changed(expected_url_contains)   # URL değişti mi?
✅ error_message(expected_text)         # Hata mesajı var mı?
✅ page_title(expected)                 # Sayfa başlığı doğru mu?
✅ user_logged_in()                     # Kullanıcı giriş yaptı mı?
✅ validation_error(expected_text)      # Validasyon hatası var mı?
```

---

## 📚 Dokümantasyon

| Dosya | Açıklama |
|-------|----------|
| [YAML_DRIVEN_TESTING.md](YAML_DRIVEN_TESTING.md) | ⭐ YAML testing rehberi |
| [REFACTORING_GUIDE.md](REFACTORING_GUIDE.md) | Refactoring detayları |
| [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) | Özet |

---

## 💡 Örnek Senaryolar

### Örnek 1: Başarılı Giriş

```yaml
- name: "successful_login"
  steps:
    - action: "navigate"
      url: "/"
    - action: "click_login_link"
    - action: "fill_login_form"
      email: "test@test.com"
      password: "Test123"
    - action: "submit_login"
  assertions:
    - type: "url_changed"
      expected_url_contains: "/dashboard"
```

### Örnek 2: Dinamik Email ile Kayıt

```yaml
- name: "unique_registration"
  steps:
    - action: "navigate"
      url: "/"
    - action: "click_signup_link"
    - action: "fill_registration_form"
      email: "user_{{timestamp}}@test.com"  # 🔄 Dinamik!
      first_name: "John"
      last_name: "Doe"
      password: "Pass@1234"
    - action: "submit_registration"
```

---

## 🎯 Dinamik Parametreler

YAML'da şu parametreleri kullanabilirsiniz:

| Parametre | Örnek | Açıklama |
|-----------|-------|----------|
| `{{timestamp}}` | `user_20231225123045@test.com` | Geçerli timestamp |
| `{{date}}` | `user_20231225@test.com` | Geçerli tarih |
| `{{random}}` | `user_45678@test.com` | Rastgele sayı |

---

## 📋 Test Çalıştırma Seçenekleri

```bash
# Tüm YAML testleri
py -m pytest tests/test_yaml_runner.py -v -s

# Sadece registration
py -m pytest tests/test_yaml_runner.py::TestYamlScenarios::test_all_registration_scenarios -v -s

# Sadece login
py -m pytest tests/test_yaml_runner.py::TestYamlScenarios::test_all_login_scenarios -v -s

# Parametreli testler (her senaryo ayrı test)
py -m pytest tests/test_yaml_runner.py::TestYamlScenarios::test_login_scenarios_parametrized -v -s

# Kategori bazlı
py -m pytest tests/test_yaml_runner.py::TestYamlScenariosByCategory -v -s

# HTML rapor ile
py -m pytest tests/test_yaml_runner.py -v -s --html=test-reports/report.html --self-contained-html

# Tüm testler (manual + YAML)
py -m pytest tests/ -v -s
```

---

## 🔍 Test Raporu

Testler bittiğinde `test-reports/test-report.html` dosyasında HTML rapor oluşturulur.

```bash
# Raporu aç
start test-reports/test-report.html
```

---

## 🐛 Troubleshooting

### pytest bulunamıyor
```bash
py -m pip install -r requirements.txt
py -m pytest tests/ -v -s
```

### YAML dosyası bulunamıyor
`test_scenarios.yaml` dosyasının proje kök dizininde olduğundan emin olun.

### Action/Assertion hatası
`utils/yaml_action_executor.py` dosyasında action adını kontrol edin.

---

## 🎓 Test Akışı

```
1. test_scenarios.yaml dosyasını oku
                ↓
2. YAML ActionExecutor başlat
                ↓
3. Her adım için action handler'ı çalıştır
   - navigate → driver.get()
   - fill_form → page.fill_form()
   - submit → page.submit()
                ↓
4. Assertions execute et
   - url_changed → driver.current_url kontrol et
   - error_message → page_source kontrol et
                ↓
5. Sonuç döndür (success/failure)
                ↓
6. Rapor oluştur
```

---

## 📞 Hızlı Referans

```bash
# YAML helper test et
python utils/yaml_helper.py

# Demo çalıştır
python demo_yaml_runner.py

# Tüm testleri çalıştır
run_tests.bat

# Belirli test
py -m pytest tests/test_yaml_runner.py::TestYamlScenariosByCategory::test_successful_login -v -s
```

---

## ✨ Geliştirilecek Alanlar

- [ ] Database testleri ekle
- [ ] Performance testleri ekle
- [ ] Parallel execution
- [ ] Jenkins integration
- [ ] Slack notifications
- [ ] Video recording

---

## 📦 Bağımlılıklar

```
selenium==4.15.2
pytest==7.4.3
webdriver-manager==4.0.1
pytest-html==4.1.1
pytest-metadata==3.1.1
PyYAML==6.0.1
```

---

## 👤 Katkıda Bulunma

Yeni feature'lar veya bug fix'leri için pull request gönderin.

---

**Sürüm:** 3.0  
**Son Güncelleme:** Aralık 2025  
**Status:** ✅ Aktif & Maintaining

- Python 3.8 veya üzeri
- Google Chrome tarayıcı
- ChromeDriver (otomatik olarak indirilir)

## 🔧 Kurulum

### 1. Projeyi Klonlayın

```bash
git clone https://github.com/hasan-gultekin/automation_test_kamilesor.git
cd automation_test_kamilesor
```

### 2. Sanal Ortam Oluşturun (Önerilen)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# veya
source venv/bin/activate  # Linux/Mac
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Yapılandırma Dosyasını Ayarlayın

`config.example.py` dosyasını `config.py` olarak kopyalayın ve gerekli ayarları yapın:

```bash
copy config.example.py config.py  # Windows
# veya
cp config.example.py config.py    # Linux/Mac
```

## 🎯 Testleri Çalıştırma

### Windows'ta Otomatik Çalıştırma

**Tüm testleri çalıştır:**
```bash
run_tests.bat
```

<<<<<<< HEAD
**Belirli bir testi çalıştır:**
```bash
run_specific_test.bat
```
=======
**Tüm testleri çalıştır ve rapor oluştur:**
```bash
run_tests.bat
```

### 3. Yapılandırma
>>>>>>> e51fda69afa28ad076710e16fae88977d27bb905

### Manuel Çalıştırma

**Tüm testleri çalıştır:**
```bash
pytest tests/ -v -s --html=test-reports/test-report.html --self-contained-html
```

**Sadece kayıt testlerini çalıştır:**
```bash
pytest tests/test_1_registration.py -v -s
```

**Sadece login testlerini çalıştır:**
```bash
pytest tests/test_2_login.py -v -s
```

**Sadece chat testlerini çalıştır:**
```bash
pytest tests/test_3_doctor_chat.py -v -s
```

## 📊 Test Raporları

Test çalıştırıldıktan sonra HTML raporu `test-reports/test-report.html` dosyasında oluşturulur. Bu rapor şunları içerir:

- Test sonuçları (Pass/Fail)
- Test süresi
- Hata mesajları
- Screenshot'lar (başarısız testler için)

## 🏗️ Page Object Model (POM)

Proje, Page Object Model tasarım desenini kullanır:

- **base_page.py**: Tüm sayfa sınıflarının miras aldığı temel sınıf
- **registration_page.py**: Kayıt sayfası işlemleri
- **login_page.py**: Giriş sayfası işlemleri
- **chat_page.py**: Chat sayfası işlemleri

### Örnek Kullanım

```python
from pages.login_page import LoginPage

def test_login(driver):
    login_page = LoginPage(driver)
    login_page.login("user@example.com", "password123")
    assert login_page.is_login_successful()
```

## 🛠️ Yapılandırma

`config.py` dosyasında aşağıdaki ayarları değiştirebilirsiniz:

```python
BASE_URL = "https://kamilesor.com"
BROWSER = "chrome"              # chrome, firefox, edge
IMPLICIT_WAIT = 10              # Saniye
EXPLICIT_WAIT = 20              # Saniye
HEADLESS = False                # True: Tarayıcı görünmeden çalışır
SCREENSHOT_ON_FAILURE = True    # Hata durumunda screenshot al
```

## 🔍 Test Verileri

Test verileri dinamik olarak `utils/test_data_helper.py` kullanılarak oluşturulur:

- Benzersiz email adresleri
- Rastgele kullanıcı adları
- Güvenli şifreler
- Telefon numaraları

## 📝 Test Senaryoları

### 1. Kayıt Testleri (`test_1_registration.py`)
- Yeni kullanıcı kaydı
- Form validasyonu
- Başarılı kayıt doğrulama

### 2. Login Testleri (`test_2_login.py`)
- Geçerli kimlik bilgileriyle giriş
- Geçersiz kimlik bilgileriyle giriş
- Şifre hatırlatma

### 3. Chat Testleri (`test_3_doctor_chat.py`)
- Doktor ile chat başlatma
- Mesaj gönderme
- Chat geçmişi kontrolü

## 🐛 Sorun Giderme

### ChromeDriver Hatası
```
webdriver-manager otomatik olarak driver'ı indirir.
İnternet bağlantınızı kontrol edin.
```

### Element Bulunamadı
```
- Locator'ları kontrol edin
- Bekleme sürelerini artırın (config.py)
- Sayfanın tamamen yüklendiğinden emin olun
```

### Import Hataları
```bash
# Python path'ini kontrol edin
set PYTHONPATH=%PYTHONPATH%;%CD%  # Windows
export PYTHONPATH=$PYTHONPATH:$(pwd)  # Linux/Mac
```

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje test ve eğitim amaçlı geliştirilmiştir.

## 📧 İletişim

Hasan Gültekin - [@hasan-gultekin](https://github.com/hasan-gultekin)

Proje Linki: [https://github.com/hasan-gultekin/automation_test_kamilesor](https://github.com/hasan-gultekin/automation_test_kamilesor)
