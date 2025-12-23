"""
Registration Page - Kayıt sayfası (Playwright)
"""
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.test_data_helper import generate_test_user_data
import time


class RegistrationPage(BasePage):
    """Kayıt sayfası için Page Object"""
    
    # Locators - Playwright selectors (CSS or XPath)
    LOGIN_LINK = "a[href='/login']"
    SIGNUP_LINK = "a[href='/signup']"
    FIRST_NAME_INPUT = "input[name='first_name']"
    LAST_NAME_INPUT = "input[name='last_name']"
    EMAIL_INPUT = "input[name='email']"
    PASSWORD_INPUT = "input[name='password']"
    SUBMIT_BUTTON = "button[type='submit']"
    SIGNUP_URL = "https://kamilesor.com/signup"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def click_login_link(self):
        """Giriş yap linkine tıkla"""
        self.click_element(self.LOGIN_LINK)
    
    def click_signup_link(self):
        """Kayıt ol linkine tıkla"""
        self.click_element(self.SIGNUP_LINK)
    
    def fill_registration_form(self, first_name, last_name, email, password):
        """Kayıt formunu doldur"""
        self.input_text(self.FIRST_NAME_INPUT, first_name)
        self.input_text(self.LAST_NAME_INPUT, last_name)
        self.input_text(self.EMAIL_INPUT, email)
        self.input_text(self.PASSWORD_INPUT, password)
    
    def submit_registration(self):
        """Kayıt formunu gönder"""
        self.click_element(self.SUBMIT_BUTTON)
    
    def is_registration_successful(self):
        """Kayıt başarılı mı kontrol et (URL değişti mi?)"""
        return self.get_current_url() != self.SIGNUP_URL
    
    # ========================================
    # TEST FLOW METODLARI
    # ========================================
    
    def execute_successful_registration_flow(self, base_url="https://kamilesor.com"):
        """
        Başarılı kayıt akışını gerçekleştir
        
        Steps:
        1. Ana sayfaya git
        2. Giriş linkine tıkla
        3. Kayıt linkine tıkla
        4. Formu doldur
        5. Formu gönder
        
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
            
            # Kayıt ol linkine tıkla
            self.click_signup_link()
            print("✓ Kayıt sayfasına gidildi")
            time.sleep(2)
            
            # Test verilerini oluştur
            test_data = generate_test_user_data()
            
            # Kayıt formunu doldur
            self.fill_registration_form(
                test_data["first_name"],
                test_data["last_name"],
                test_data["email"],
                test_data["password"]
            )
            print(f"✓ Form dolduruldu (Email: {test_data['email']})")
            time.sleep(1)
            
            # Formu gönder
            self.submit_registration()
            print("✓ Form gönderildi")
            time.sleep(5)
            
            # Başarılı kayıt doğrulaması
            if not self.is_registration_successful():
                return {
                    "success": False,
                    "message": "Kayıt sonrası sayfa değişmedi",
                    "current_url": self.get_current_url()
                }
            
            current_url = self.get_current_url()
            print(f"✓ Kayıt başarılı! Yönlendirilen URL: {current_url}")
            
            return {
                "success": True,
                "message": "Başarılı kayıt yapıldı",
                "current_url": current_url,
                "user_email": test_data["email"]
            }
            
        except Exception as e:
            error_msg = f"❌ Test hatası: {str(e)}"
            print(error_msg)
            return {
                "success": False,
                "message": error_msg,
                "exception": str(e)
            }
    
    def execute_registration_flow_with_data(self, first_name, last_name, email, password, 
                                           base_url="https://kamilesor.com"):
        """
        Verilen verilerle kayıt akışını gerçekleştir
        
        Args:
            first_name: Adı
            last_name: Soyadı
            email: E-mail adresi
            password: Şifre
            base_url: Base URL
            
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
            
            # Kayıt ol linkine tıkla
            self.click_signup_link()
            print("✓ Kayıt sayfasına gidildi")
            time.sleep(2)
            
            # Kayıt formunu doldur
            self.fill_registration_form(first_name, last_name, email, password)
            print(f"✓ Form dolduruldu (Email: {email})")
            time.sleep(1)
            
            # Formu gönder
            self.submit_registration()
            print("✓ Form gönderildi")
            time.sleep(5)
            
            current_url = self.get_current_url()
            
            return {
                "success": True,
                "message": "Kayıt işlemi tamamlandı",
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
