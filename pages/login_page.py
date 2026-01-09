"""
Login Page - Login page (Playwright)
"""
from playwright.sync_api import Page
from pages.base_page import BasePage
import time


class LoginPage(BasePage):
    """Giriş sayfası için Page Object"""
    
    # Locators - Playwright selectors (CSS or XPath)
    LOGIN_LINK = "a[href='/login']"
    EMAIL_INPUT = "input[name='email']"
    PASSWORD_INPUT = "input[name='password']"
    SUBMIT_BUTTON = "button[type='submit']"
    BASE_URL = "https://www.kamilesor.com"
    LOGIN_VERIFICATION_ELEMENT = "text=Hesabım"  # Element visible after login
    
    def __init__(self, page: Page):
        super().__init__(page)

    def navigate_to_login_page(self):
        """Navigate to the login page"""
        self.page.goto(f"{self.BASE_URL}")
        print(f"✓ Navigated to login page: {self.BASE_URL}")
        return True
    
    def click_login_link(self):
        """Click the login link"""
        self.click_element(self.LOGIN_LINK)
        return True

    
    def fill_login_form(self, email, password):
        """Fill in the login form"""
        self.input_text(self.EMAIL_INPUT, email)
        self.input_text(self.PASSWORD_INPUT, password)
        return True
    
    def submit_login(self):
        """Submit the login form"""
        self.click_element(self.SUBMIT_BUTTON)
        return True
    
    def is_login_successful(self):
        """Check if login was successful"""
        result = self.is_element_visible(self.LOGIN_VERIFICATION_ELEMENT)
        return result
    
    def execute_successful_login_flow(self, email, password, base_url="https://kamilesor.com"):
        """
        Verifies successful login flow.
        
        Steps:
        1. Go to the homepage
        2. Click the login link
        3. Fill in the login form
        4. Submit the login form
        5. Verify that login was successful
        """
        self.page.goto(f"{base_url}")
        print(f"✓ Navigated to homepage: {base_url}")
        
        self.click_login_link()
        print("✓ Clicked login link")
        
        self.fill_login_form(email, password)
        print(f"✓ Filled login form: {email} / {'*' * len(password)}")
        
        self.submit_login()
        print("✓ Submitted login form")
        
        time.sleep(2)  # Short wait for page to load
        
        if self.is_login_successful():
            print("✓ Login successful!")
            return True
        else:
            print("❌ Login failed!")
            return False
    