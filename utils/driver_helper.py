"""
Driver Helper - Playwright synchronous browser management
"""
from playwright.sync_api import sync_playwright
import config


# Global playwright context
_playwright = None
_browser = None
_context = None
_page = None


def get_browser():
    """
    Playwright browser başlat (Sync API)
    
    Returns:
        Browser: Configured Playwright Browser instance
    """
    global _playwright, _browser
    
    try:
        _playwright = sync_playwright().start()
        
        browser_type = config.BROWSER.lower()
        
        if browser_type == "chromium":
            _browser = _playwright.chromium.launch(headless=config.HEADLESS)
        elif browser_type == "firefox":
            _browser = _playwright.firefox.launch(headless=config.HEADLESS)
        elif browser_type == "webkit":
            _browser = _playwright.webkit.launch(headless=config.HEADLESS)
        else:
            _browser = _playwright.chromium.launch(headless=config.HEADLESS)
        
        print(f"✓ Browser başlatıldı: {browser_type}")
        return _browser
    except Exception as e:
        print(f"❌ Browser başlatma hatası: {e}")
        raise


def get_page(browser):
    """
    Browser context ve page oluştur (Sync API)
    
    Args:
        browser: Playwright Browser instance
        
    Returns:
        Page: Configured Playwright Page instance
    """
    global _context, _page
    
    try:
        _context = browser.new_context(
            viewport={"width": config.VIEWPORT_WIDTH, "height": config.VIEWPORT_HEIGHT}
        )
        _page = _context.new_page()
        _page.set_default_timeout(config.EXPLICIT_WAIT)
        _page.set_default_navigation_timeout(config.NAVIGATION_TIMEOUT)
        
        print(f"✓ Page oluşturuldu: {config.VIEWPORT_WIDTH}x{config.VIEWPORT_HEIGHT}")
        return _page
    except Exception as e:
        print(f"❌ Page oluşturma hatası: {e}")
        raise


def close_browser(browser):
    """
    Browser'ı kapat (Sync API)
    
    Args:
        browser: Playwright Browser instance
    """
    global _playwright, _browser, _context, _page
    
    try:
        if _page:
            _page.close()
            _page = None
        if _context:
            _context.close()
            _context = None
        if browser:
            browser.close()
            _browser = None
        if _playwright:
            _playwright.stop()
            _playwright = None
        
        print("✓ Browser kapatıldı")
    except Exception as e:
        print(f"⚠ Browser kapatma hatası: {e}")
