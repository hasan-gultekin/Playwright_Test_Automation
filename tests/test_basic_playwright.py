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
    """Simple tests to verify Playwright setup"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Browser setup"""
        self.browser = get_browser()
        self.page = get_page(self.browser)
        yield
        close_browser(self.browser)
    
    def test_browser_launched(self):
        """Is the browser launched successfully?"""
        assert self.page is not None, "Page could not be created"
        print("✅ Browser launched successfully")
    
    def test_navigate_to_base_url(self):
        """Can navigate to the Base URL?"""
        self.page.goto(config.BASE_URL)
        current_url = self.page.url
        assert config.BASE_URL in current_url, f"URL did not change: {current_url}"
        print(f"✅ Successfully navigated to {config.BASE_URL}")
    
    def test_page_title(self):
        """Can the page title be retrieved?"""
        self.page.goto(config.BASE_URL)
        title = self.page.title()
        assert title, "Page title is empty"
        print(f"✅ Page title: {title}")
    
    def test_browser_config(self):
        """Is the browser configuration correct?"""
        assert config.BROWSER in ["chromium", "firefox", "webkit"], "Invalid browser"
        print(f"✅ Browser: {config.BROWSER}")
        print(f"✅ Headless: {config.HEADLESS}")
        print(f"✅ Viewport: {config.VIEWPORT_WIDTH}x{config.VIEWPORT_HEIGHT}")
