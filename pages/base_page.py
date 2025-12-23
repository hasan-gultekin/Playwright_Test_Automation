"""
Base Page - Tüm sayfa objelerinin miras alacağı temel sınıf (Playwright uyumlu)
"""
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
import config
import time


class BasePage:
    """Tüm sayfa objelerinin miras alacağı temel sınıf"""
    
    def __init__(self, page: Page):
        """
        BasePage'i başlat
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.page.set_default_timeout(config.EXPLICIT_WAIT)
        self.page.set_default_navigation_timeout(config.NAVIGATION_TIMEOUT)
    
    def find_element(self, selector: str):
        """
        Element bul
        
        Args:
            selector: CSS selector veya XPath
            
        Returns:
            Locator: Playwright Locator
        """
        try:
            locator = self.page.locator(selector)
            locator.wait_for(timeout=config.EXPLICIT_WAIT)
            return locator
        except PlaywrightTimeoutError:
            print(f"❌ Element bulunamadı: {selector}")
            raise
    
    def click_element(self, selector: str):
        """
        Element'e tıkla
        
        Args:
            selector: CSS selector veya XPath
        """
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=config.EXPLICIT_WAIT)
            locator.click()
            print(f"✓ Element'e tıklandı: {selector}")
        except PlaywrightTimeoutError:
            print(f"❌ Element tıklanamadı: {selector}")
            raise
    
    def input_text(self, selector: str, text: str):
        """
        Input alanına text gir
        
        Args:
            selector: CSS selector veya XPath
            text: Girilecek metin
        """
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=config.EXPLICIT_WAIT)
            locator.clear()
            locator.fill(text)
            print(f"✓ Text girildi: {selector}")
        except PlaywrightTimeoutError:
            print(f"❌ Input alanı bulunamadı: {selector}")
            raise
    
    def get_text(self, selector: str) -> str:
        """
        Element'in text'ini al
        
        Args:
            selector: CSS selector veya XPath
            
        Returns:
            str: Element'in metni
        """
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=config.EXPLICIT_WAIT)
            text = locator.text_content()
            return text or ""
        except PlaywrightTimeoutError:
            print(f"❌ Element'in metni alınamadı: {selector}")
            raise
    
    def is_element_visible(self, selector: str) -> bool:
        """
        Element görünür mü kontrol et
        
        Args:
            selector: CSS selector veya XPath
            
        Returns:
            bool: Element görünür mü
        """
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=config.EXPLICIT_WAIT)
            return locator.is_visible()
        except PlaywrightTimeoutError:
            return False
    
    def wait_for_selector(self, selector: str, timeout: int = None):
        """
        Selector'un görünür olmasını bekle
        
        Args:
            selector: CSS selector veya XPath
            timeout: Bekleme süresi (ms)
        """
        wait_timeout = timeout or config.EXPLICIT_WAIT
        try:
            self.page.wait_for_selector(selector, timeout=wait_timeout)
            print(f"✓ Element beklendi: {selector}")
        except PlaywrightTimeoutError:
            print(f"❌ Element zaman aşımı: {selector}")
            raise
    
    def wait_for_url(self, url: str, timeout: int = None):
        """
        URL değişimini bekle
        
        Args:
            url: Beklenen URL (regex veya string)
            timeout: Bekleme süresi (ms)
        """
        wait_timeout = timeout or config.NAVIGATION_TIMEOUT
        try:
            self.page.wait_for_url(url, timeout=wait_timeout)
            print(f"✓ URL değişimi beklendi: {url}")
        except PlaywrightTimeoutError:
            print(f"❌ URL değişimi zaman aşımı: {url}")
            raise
    
    def get_current_url(self) -> str:
        """
        Mevcut URL'i al
        
        Returns:
            str: Mevcut URL
        """
        return self.page.url
    
    def navigate(self, url: str):
        """
        Sayfa'ya git
        
        Args:
            url: Gidilecek URL
        """
        self.page.goto(url)
        print(f"✓ {url} adresine gidildi")
    
    def take_screenshot(self, filename: str):
        """
        Ekran görüntüsü al
        
        Args:
            filename: Dosya adı
        """
        self.page.screenshot(path=filename)
        print(f"✓ Ekran görüntüsü alındı: {filename}")
    
    def wait(self, seconds: float):
        """
        Belirtilen süre bekle
        
        Args:
            seconds: Saniye
        """
        time.sleep(seconds)
        print(f"⏳ {seconds} saniye beklendi")
