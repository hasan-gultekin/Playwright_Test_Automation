"""
Basit Playwright Test - Kurulumu doğrula
"""

import pytest
import sys
import os

# Proje kök dizinini Python path'e ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_helper import get_browser, get_page, close_browser
import config


class TestBasicPlaywright:
    """Playwright kurulumunu doğrulayan basit testler"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Browser setup"""
        self.browser = get_browser()
        self.page = get_page(self.browser)
        yield
        close_browser(self.browser)
    
    def test_browser_launched(self):
        """Browser başarıyla başlatıldı mı?"""
        assert self.page is not None, "Page oluşturulamadı"
        print("✅ Browser başarıyla başlatıldı")
    
    def test_navigate_to_base_url(self):
        """Base URL'ye navigate edilebiliyor mu?"""
        self.page.goto(config.BASE_URL)
        current_url = self.page.url
        assert config.BASE_URL in current_url, f"URL değişmedi: {current_url}"
        print(f"✅ {config.BASE_URL}'ye başarıyla gidildi")
    
    def test_page_title(self):
        """Sayfa title'ı alınabiliyor mu?"""
        self.page.goto(config.BASE_URL)
        title = self.page.title()
        assert title, "Sayfa title'ı boş"
        print(f"✅ Sayfa title'ı: {title}")
    
    def test_browser_config(self):
        """Browser konfigürasyonu doğru mu?"""
        assert config.BROWSER in ["chromium", "firefox", "webkit"], "Geçersiz browser"
        print(f"✅ Browser: {config.BROWSER}")
        print(f"✅ Headless: {config.HEADLESS}")
        print(f"✅ Viewport: {config.VIEWPORT_WIDTH}x{config.VIEWPORT_HEIGHT}")
