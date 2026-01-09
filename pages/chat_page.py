"""
Chat Page - Playwright uyumlu
"""
from playwright.sync_api import Page
from typing import Optional
from pages.base_page import BasePage
import time


class ChatPage(BasePage):
    """Page Object for Chat Page"""

    # Mesaj içerikleri
    MESSAGE_TO_DOCTOR1 = "My head hurts and I have severe pain in my eyes. What should I do?"
    MESSAGE_TO_DOCTOR2 = "Thank you."
    MESSAGE_TO_IT1 = "How can I reverse a list in Python?"
    MESSAGE_TO_IT2 = "Thanks for your help!"
    MESSAGE_TO_TEACHER1 = "Can you explain the concept of integrals in mathematics?"
    MESSAGE_TO_TEACHER2 = "Thank you very much, you were very helpful!"
    
    # Locators - Playwright selectors
    DOCTOR_BUTTON = "button[data-code-name='Doktor']"
    IT_BUTTON = "button[data-code-name='Yazılım Uzmanı']"
    TEACHER_BUTTON = "button[data-code-name='Ogretmen'], button:has-text('Ogretmen')"
    MESSAGE_INPUT = "textarea[placeholder='Mesajınızı buraya yazın...'], textarea[name='message']"
    SEND_BUTTON = "button#send-btn, button:has-text('Gönder')"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def click_doctor_button(self):
        """Click Doctor button"""
        self.click_element(self.DOCTOR_BUTTON)

    def click_it_button(self):
        """Click IT Specialist button"""
        self.click_element(self.IT_BUTTON)    

    def click_teacher_button(self):
        """Click Teacher button"""
        self.click_element(self.TEACHER_BUTTON)      
    
    def enter_message(self, message: str):
        """Enter text in message input"""
        self.input_text(self.MESSAGE_INPUT, message)
    
    def click_send_button(self):
        """Click Send button"""
        self.click_element(self.SEND_BUTTON)
    
    def send_message_to_doctor1(self, message: str = None):
        """Send first message to Doctor"""
        self.click_doctor_button()
        msg = message if message else self.MESSAGE_TO_DOCTOR1
        self.enter_message(msg)
        self.click_send_button()
        return True
    
    def send_message_to_doctor2(self, message: str = None):
        """Send second message to Doctor"""
        msg = message if message else self.MESSAGE_TO_DOCTOR2
        self.enter_message(msg)
        self.click_send_button()
        return True
    
    def send_message_to_it_specialist1(self, message: str = None):
        """Send first message to IT Specialist"""
        self.click_it_button()
        msg = message if message else self.MESSAGE_TO_IT1
        self.enter_message(msg)
        self.click_send_button()
        return True
    
    def send_message_to_it_specialist2(self, message: str = None):
        """Send second message to IT Specialist"""
        msg = message if message else self.MESSAGE_TO_IT2
        self.enter_message(msg)
        self.click_send_button()
        return True
    
    def send_message_to_teacher(self, message: str):
        """Send message to Teacher"""
        self.click_teacher_button()
        self.enter_message(message)
        self.click_send_button()
        return True

