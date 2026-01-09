# 🧪 Kamile Sor Test Automation

YAML-driven test automation framework built with Playwright and Python.

**Version:** 5.0 (Playwright + YAML Method Executor)  
**Status:** ✅ Active

---

## 🎯 Key Features

- ✅ **YAML-Driven Tests** - Define tests in YAML, no coding required
- ✅ **Page Object Model** - Maintainable and scalable architecture
- ✅ **Method Execution Engine** - Call page methods directly from YAML
- ✅ **Playwright** - Modern, fast, and reliable browser automation
- ✅ **Dynamic Parameters** - `{{config.BASE_URL}}`, `{{config.LOGIN_USER}}`, etc.
- ✅ **Modular Structure** - Each test scenario in separate YAML file
- ✅ **Cross-browser** - Chromium, Firefox, WebKit support

---

## 📁 Project Structure

```
automation_test_kamilesor/
│
├── scenarios/                            # 📝 Test Scenarios (YAML)
│   ├── TC_001_registration_scenarios.yaml
│   ├── TC_002_login.yaml
│   ├── TC_003_chat_with_doctor.yaml
│   └── TC_004_chat_with_it_specialist.yaml
│
├── pages/                                # 🎭 Page Object Model
│   ├── __init__.py
│   ├── base_page.py                     # Base page class (common methods)
│   ├── login_page.py                    # Login page + flow methods
│   ├── chat_page.py                     # Chat page + messaging methods
│   └── registration_page.py             # Registration page
│
├── utils/                                # 🔧 Utilities
│   ├── __init__.py
│   ├── driver_helper.py                 # Playwright browser management
│   ├── yaml_helper.py                   # YAML parser & loader
│   ├── yaml_method_executor.py          # ⭐ Method execution engine
│   └── test_data_helper.py              # Test data generation
│
├── tests/                                # 🧪 Test Runner (pytest)
│   ├── __init__.py
│   ├── conftest.py                      # Pytest fixtures
│   └── test_runner.py                   # YAML test runner
│
├── config.py                            # ⚙️ Configuration
├── requirements.txt                     # 📦 Dependencies
├── pytest.ini                           # Pytest settings
├── run_specific_yaml.py                 # ⭐ YAML test runner script
└── README.md                            # This file
```

---

## 🚀 Quick Start

### 1. Requirements

- Python 3.9 or higher
- pip (Python package manager)

### 2. Installation

```bash
# Install dependencies
pip3 install -r requirements.txt

# Install Playwright browsers
python3 -m playwright install
```

### 3. Configuration

Configure settings in `config.py`:

```python
BASE_URL = "https://kamilesor.com"
BROWSER = "webkit"              # chromium, firefox, webkit
HEADLESS = False                # True: Headless mode
LOGIN_USER = "your@email.com"
LOGIN_PASSWORD = "yourpassword"
```

### 4. Run Tests

```bash
# Run a specific YAML scenario
python3 run_specific_yaml.py scenarios/TC_002_login.yaml

# Run chat scenario
python3 run_specific_yaml.py scenarios/TC_003_chat_with_doctor.yaml

# Run IT specialist scenario
python3 run_specific_yaml.py scenarios/TC_004_chat_with_it_specialist.yaml
```

---

## 📝 YAML Scenario Structure

### Basic Format

```yaml
test_scenarios:
  category_name:
    - name: "scenario_name"
      description: "Scenario description"
      enabled: true
      page: "PageClassName"              # LoginPage, ChatPage, etc.
      method: "method_name"               # Method to execute
      params:                             # Method parameters
        email: "{{config.LOGIN_USER}}"
        password: "{{config.LOGIN_PASSWORD}}"
      wait_time: 5                        # Wait time after scenario (seconds)
```

### Example: Login Scenario

```yaml
test_scenarios:
  login:
    - name: "successful_login"
      description: "User successfully logs in"
      enabled: true
      page: "LoginPage"
      method: "execute_successful_login_flow"
      params:
        base_url: "{{config.BASE_URL}}"
        email: "{{config.LOGIN_USER}}"
        password: "{{config.LOGIN_PASSWORD}}"
      wait_time: 5
```

### Example: Chat Scenario

```yaml
test_scenarios:
  chat:
    - name: "chat_with_doctor"
      description: "Chat with doctor test"
      enabled: true
      page: "ChatPage"
      method: "send_message_to_doctor1"
      wait_time: 20
```

---

## 🎭 Page Object Model

### BasePage

Base class inherited by all page classes. Contains common methods:

- `click_element(selector)` - Click element
- `input_text(selector, text)` - Input text
- `is_element_visible(selector)` - Check if element is visible
- `wait_for_selector(selector)` - Wait for element
- `navigate(url)` - Navigate to URL
- `take_screenshot(filename)` - Take screenshot

### LoginPage

Login page operations:

```python
def execute_successful_login_flow(self, email, password, base_url):
    """Execute successful login flow"""
    self.page.goto(base_url)
    self.click_login_link()
    self.fill_login_form(email, password)
    self.submit_login()
    return self.is_login_successful()
```

### ChatPage

Chat page operations:

```python
def send_message_to_doctor1(self, message: str = None):
    """Send first message to doctor"""
    self.click_doctor_button()
    msg = message if message else self.MESSAGE_TO_DOCTOR1
    self.enter_message(msg)
    self.click_send_button()
    return True
```

---

## 🔧 YAML Method Executor

`yaml_method_executor.py` - Dynamically executes methods defined in YAML.

### How It Works

1. Get scenario info from YAML (page, method, params)
2. Dynamically import page class
3. Create page instance
4. Execute method with parameters
5. Evaluate result (success/failure)

### Dynamic Parameters

```yaml
params:
  base_url: "{{config.BASE_URL}}"          # Get value from config.py
  email: "{{config.LOGIN_USER}}"
  password: "{{config.LOGIN_PASSWORD}}"
  message: "{{ChatPage.MESSAGE_TO_DOCTOR1}}" # Get from page constant
```

---

## 📊 Test Results

After test completion, detailed summary is displayed:

```
================================================================================
📊 TEST SUMMARY
================================================================================
✅ Passed: 2
❌ Failed: 0
📋 Total: 2

--------------------------------------------------------------------------------
Detailed Results:
--------------------------------------------------------------------------------

✅ execution_login
   Status: PASSED
   Message: Scenario successful: execution_login

✅ chat_with_doctor1
   Status: PASSED
   Message: Scenario successful: chat_with_doctor1
```

---

## 🛠️ Adding New Scenarios

### 1. Create Page Method

```python
# pages/chat_page.py
def send_message_to_teacher(self, message: str = None):
    """Send message to teacher"""
    self.click_teacher_button()
    msg = message if message else self.MESSAGE_TO_TECHER1
    self.enter_message(msg)
    self.click_send_button()
    return True  # Return success status
```

### 2. Add YAML Scenario

```yaml
# scenarios/TC_005_chat_with_teacher.yaml
test_scenarios:
  chat:
    - name: "execution_login"
      description: "User login"
      enabled: true
      page: "LoginPage"
      method: "execute_successful_login_flow"
      params:
        base_url: "{{config.BASE_URL}}"
        email: "{{config.LOGIN_USER}}"
        password: "{{config.LOGIN_PASSWORD}}"
      wait_time: 5

    - name: "chat_with_teacher"
      description: "Chat with teacher"
      enabled: true
      page: "ChatPage"
      method: "send_message_to_teacher"
      wait_time: 20
```

### 3. Run Test

```bash
python3 run_specific_yaml.py scenarios/TC_005_chat_with_teacher.yaml
```

---

## 🎯 Current Test Scenarios

| Test File | Description | Scenarios |
|-----------|-------------|-----------|
| `TC_001_registration_scenarios.yaml` | Registration tests | User registration |
| `TC_002_login.yaml` | Login tests | Successful login |
| `TC_003_chat_with_doctor.yaml` | Doctor chat tests | 2 message scenarios |
| `TC_004_chat_with_it_specialist.yaml` | IT specialist chat tests | 2 message scenarios |

---

## 🐛 Troubleshooting

### Playwright Browsers Not Installed

```bash
python3 -m playwright install
```

### Element Not Found

- Check locators in pages/*.py
- Increase timeout values in `config.py`
- Disable headless mode (`HEADLESS = False`)

### YAML Parse Error

- Check YAML indentation (use 2 spaces)
- Ensure category name is correct (`chat:`, `login:`, etc.)

### Method Not Found Error

- Ensure page class name is correct (e.g., `LoginPage`)
- Check that method is defined in the page class
- Ensure method returns `True`

---

## 📚 Technologies Used

- **Python 3.9+** - Programming language
- **Playwright** - Browser automation
- **PyYAML** - YAML parser
- **pytest** - Test framework (optional)

---

## 🔍 Playwright vs Selenium

| Feature | Playwright | Selenium |
|---------|-----------|----------|
| Speed | ⚡ Very Fast | 🐢 Medium |
| Modern API | ✅ Yes | ❌ No |
| Auto-wait | ✅ Yes | ❌ Manual |
| Cross-browser | ✅ 3 Engines | ✅ Multiple |
| Headless | ✅ Native | ⚠️ Limited |
| Screenshot | ✅ Advanced | ⚠️ Basic |

---

## 📞 Quick Reference

```bash
# Install all dependencies
pip3 install -r requirements.txt

# Install Playwright browsers
python3 -m playwright install

# Run specific scenario
python3 run_specific_yaml.py scenarios/TC_002_login.yaml

# Run all tests (with pytest)
pytest tests/test_runner.py -v -s

# Edit config file
nano config.py
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Create Pull Request

---

## 📄 License

This project is developed for testing and educational purposes.

---

**Version:** 5.0  
**Last Updated:** January 2026  
**Status:** ✅ Active & Maintaining

**Developer:** Hasan Gültekin  
**Project:** Kamile Sor Test Automation Framework
