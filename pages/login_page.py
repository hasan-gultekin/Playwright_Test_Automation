"""
Login Page - Giriş sayfası (Playwright)
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
    LOGIN_VERIFICATION_ELEMENT = "text=Hesabım"  # Giriş sonrası görünen bir element
    
    def __init__(self, page: Page):
        super().__init__(page)

    def navigate_to_login_page(self):
        """Giriş sayfasına git"""
        self.page.goto(f"{self.BASE_URL}")
        print(f"✓ Login sayfasına gidildi: {self.BASE_URL}")
        return True
    
    def click_login_link(self):
        """Giriş yap linkine tıkla"""
        self.click_element(self.LOGIN_LINK)
        return True

    
    def fill_login_form(self, email, password):
        """Giriş formunu doldur"""
        self.input_text(self.EMAIL_INPUT, email)
        self.input_text(self.PASSWORD_INPUT, password)
        return True
    
    def submit_login(self):
        """Giriş formunu gönder"""
        self.click_element(self.SUBMIT_BUTTON)
        return True
    
    def is_login_successful(self):
        """Giriş başarılı mı kontrol et """
        result = self.is_element_visible(self.LOGIN_VERIFICATION_ELEMENT)
        return result
    