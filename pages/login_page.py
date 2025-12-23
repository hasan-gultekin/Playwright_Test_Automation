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
    LOGIN_URL = "https://kamilesor.com/login"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def click_login_link(self):
        """Giriş yap linkine tıkla"""
        self.click_element(self.LOGIN_LINK)

    
    def fill_login_form(self, email, password):
        """Giriş formunu doldur"""
        self.input_text(self.EMAIL_INPUT, email)
        self.input_text(self.PASSWORD_INPUT, password)
    
    def submit_login(self):
        """Giriş formunu gönder"""
        self.click_element(self.SUBMIT_BUTTON)
    
    def is_login_successful(self):
        """Giriş başarılı mı kontrol et (URL değişti mi?)"""
        return self.get_current_url() != self.LOGIN_URL
    
    # ========================================
    # TEST FLOW METODLARI
    # ========================================
    
    def execute_successful_login_flow(self, email, password, base_url="https://kamilesor.com"):
        """
        Başarılı giriş akışını gerçekleştir
        
        Args:
            email: E-mail adresi
            password: Şifre
            base_url: Base URL
            
        Steps:
        1. Ana sayfaya git
        2. Giriş linkine tıkla
        3. Formu doldur
        4. Formu gönder
        
        Returns:
            dict: Test sonuçları ve hata bilgisi
        """
        try:
            # Ana sayfaya git
            self.page.goto(base_url)
            print(f"\n✓ Ana sayfaya gidildi: {base_url}")
            time.sleep(2)
            
            # Giriş yap linkine tıkla
            self.click_login_link()
            print("✓ Giriş sayfasına gidildi")
            time.sleep(2)
            
            # Giriş formunu doldur
            self.fill_login_form(email, password)
            print(f"✓ Form dolduruldu (Email: {email})")
            time.sleep(1)
            
            # Formu gönder
            self.submit_login()
            print("✓ Form gönderildi")
            time.sleep(5)
            
            # Başarılı giriş doğrulaması
            if not self.is_login_successful():
                return {
                    "success": False,
                    "message": "Giriş sonrası sayfa değişmedi",
                    "current_url": self.get_current_url()
                }
            
            current_url = self.get_current_url()
            print(f"✓ Giriş başarılı! Yönlendirilen URL: {current_url}")
            
            return {
                "success": True,
                "message": "Başarılı giriş yapıldı",
                "current_url": current_url,
                "user_email": email
            }
            
        except Exception as e:
            error_msg = f"❌ Test hatası: {str(e)}"
            print(error_msg)
            return {
                "success": False,
                "message": error_msg,
                "exception": str(e)
            }
    
    def execute_login_flow(self, email, password, base_url="https://kamilesor.com", wait_time=5):
        """
        Genel amaçlı giriş akışını gerçekleştir (YAML verilerinden çağrılır)
        
        Args:
            email: E-mail adresi
            password: Şifre
            base_url: Base URL
            wait_time: Bekleme süresi
            
        Returns:
            dict: Test sonuçları ve hata bilgisi
        """
        try:
            # Ana sayfaya git
            self.page.goto(base_url)
            print(f"\n✓ Ana sayfaya gidildi: {base_url}")
            time.sleep(2)
            
            # Giriş yap linkine tıkla
            self.click_login_link()
            print("✓ Giriş sayfasına gidildi")
            time.sleep(2)
            
            # Giriş formunu doldur
            self.fill_login_form(email, password)
            print(f"✓ Form dolduruldu (Email: {email})")
            time.sleep(1)
            
            # Formu gönder
            self.submit_login()
            print("✓ Form gönderildi")
            time.sleep(wait_time)
            
            current_url = self.get_current_url()
            
            return {
                "success": True,
                "message": "Giriş işlemi tamamlandı",
                "current_url": current_url,
                "user_email": email
            }
            
        except Exception as e:
            error_msg = f"❌ Test hatası: {str(e)}"
            print(error_msg)
            return {
                "success": False,
                "message": error_msg,
                "exception": str(e),
                "current_url": self.get_current_url()
            }
