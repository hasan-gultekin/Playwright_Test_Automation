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

