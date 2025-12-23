"""
Chat Page - Playwright uyumlu
"""
from playwright.sync_api import Page
from typing import Optional
from pages.base_page import BasePage
import time


class ChatPage(BasePage):
    """Chat/Mesaj sayfası için Page Object"""

    # Mesaj içerikleri
    MESSAGE_TO_DOCTOR1 = "Başımın ön tarafında ve gözlerimde şiddetli bir ağrı var. Ne yapmalıyım?"
    MESSAGE_TO_DOCTOR2 = "Teşekkürler."
    MESSAGE_TO_IT1 = "Python'da bir listeyi nasıl tersine çevirebilirim?"
    MESSAGE_TO_IT2 = "Yardımın için teşekkürler!"
    MESSAGE_TO_TECHER1 = "Matematikte integral kavramını açıklayabilir misiniz?"
    MESSAGE_TO_TECHER2 = "Çok teşekkürler, çok yardımcı oldunuz!"
    
    # Locators - Playwright selectors
    DOCTOR_BUTTON = "button[data-code-name='Doktor']"
    IT_BUTTON = "button[data-code-name='Yazılım Uzmanı']"
    TEACHER_BUTTON = "button[data-code-name='Ogretmen'], button:has-text('Ogretmen')"
    MESSAGE_INPUT = "textarea[placeholder='Mesajınızı buraya yazın...'], textarea[name='message']"
    SEND_BUTTON = "button#send-btn, button:has-text('Gönder')"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def click_doctor_button(self):
        """Doktor butonuna tıkla"""
        self.click_element(self.DOCTOR_BUTTON)

    def click_it_button(self):
        """IT Uzmanına tıkla"""
        self.click_element(self.IT_BUTTON)    

    def click_teacher_button(self):
        """Öğretmene tıkla"""
        self.click_element(self.TEACHER_BUTTON)      
    
    def enter_message(self, message: str):
        """Mesaj alanına yazı yaz"""
        self.input_text(self.MESSAGE_INPUT, message)
    
    def click_send_button(self):
        """Gönder butonuna tıkla"""
        self.click_element(self.SEND_BUTTON)
    
    def send_message_to_doctor(self, message: str):
        """Doktora mesaj gönder (tüm adımlar)"""
        self.click_doctor_button()
        self.enter_message(message)
        self.click_send_button()

    def send_message_to_it(self, message: str):
        """IT Uzmanına mesaj gönder (tüm adımlar)"""
        self.click_it_button()
        self.enter_message(message)
        self.click_send_button()

    def send_message_to_teacher(self, message: str):
        """Öğretmene mesaj gönder (tüm adımlar)"""
        self.click_teacher_button()
        self.enter_message(message)
        self.click_send_button()

    def execute_chat_with_doctor(self, base_url: str = "https://kamilesor.com", message: Optional[str] = None) -> dict:
        """
        YAML-compatible: Doktorla sohbet flow'u
        
        Args:
            base_url: Ana sayfa URL'si
            message: Gönderilecek mesaj
            
        Returns:
            dict: Sonuç
        """
        try:
            if message is None:
                message = self.MESSAGE_TO_DOCTOR1
            
            self.navigate(base_url)
            self.find_element(self.DOCTOR_BUTTON)
            self.send_message_to_doctor(message)
            
            return {
                "success": True,
                "message": "Doktor mesajı başarılı",
                "current_url": self.get_current_url()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Doktor mesajı hatası: {str(e)}"
            }

    def execute_chat_with_it(self, base_url: str = "https://kamilesor.com", message: Optional[str] = None) -> dict:
        """
        YAML-compatible: IT Uzmanıyla sohbet flow'u
        
        Args:
            base_url: Ana sayfa URL'si
            message: Gönderilecek mesaj
            
        Returns:
            dict: Sonuç
        """
        try:
            if message is None:
                message = self.MESSAGE_TO_IT1
            
            self.navigate(base_url)
            self.find_element(self.IT_BUTTON)
            self.send_message_to_it(message)
            
            return {
                "success": True,
                "message": "IT Uzmanı mesajı başarılı",
                "current_url": self.get_current_url()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"IT Uzmanı mesajı hatası: {str(e)}"
            }
        
    def execute_chat_with_teacher(self, base_url: str = "https://kamilesor.com", message: Optional[str] = None, 
                                 second_message: Optional[str] = None, wait_between: int = 0) -> dict:
        """
        YAML-compatible: Öğretmenle sohbet flow'u
        
        Args:
            base_url: Ana sayfa URL'si
            message: Gönderilecek ilk mesaj
            second_message: Gönderilecek ikinci mesaj (opsiyonel)
            wait_between: İlk ve ikinci mesaj arasında bekleme süresi (saniye)
            
        Returns:
            dict: Sonuç
        """
        try:
            if message is None:
                message = self.MESSAGE_TO_TECHER1
            
            print(f"📍 Base URL'ye gidiliyor: {base_url}")
            self.navigate(base_url)
            
            # Öğretmen butonunun yüklenmesini bekle
            print(f"⏳ Öğretmen butonu bekleniyor...")
            self.wait_for_selector(self.TEACHER_BUTTON)
            print(f"✅ Öğretmen butonu bulundu")
            
            # İlk mesajı gönder
            print(f"💬 İlk mesaj gönderiliyor: {message[:50]}...")
            self.send_message_to_teacher(message)
            print(f"✅ İlk mesaj gönderildi")
            
            # İkinci mesaj varsa gönder
            if second_message is not None:
                print(f"⏳ {wait_between} saniye bekleniyor...")
                if wait_between > 0:
                    time.sleep(wait_between)
                print(f"💬 İkinci mesaj gönderiliyor: {second_message[:50]}...")
                self.send_message_to_teacher(second_message)
                print(f"✅ İkinci mesaj gönderildi")
            
            return {
                "success": True,
                "message": "Öğretmen mesajları başarılı",
                "current_url": self.get_current_url()
            }
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"❌ Öğretmen hatası:\n{error_detail}")
            return {
                "success": False,
                "message": f"Öğretmen mesajı hatası: {str(e)}"
            }
