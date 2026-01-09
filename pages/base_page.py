"""
Base Page - All pages base class (Playwright compatible)
"""
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
import config
import time


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, page: Page):
        """
        Initialize BasePage
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.page.set_default_timeout(config.EXPLICIT_WAIT)
        self.page.set_default_navigation_timeout(config.NAVIGATION_TIMEOUT)
    
    def find_element(self, selector: str):
        """
        Find element
        
        Args:
            selector: CSS selector or XPath
            
        Returns:
            Locator: Playwright Locator
        """
        try:
            locator = self.page.locator(selector)
            locator.wait_for(timeout=config.EXPLICIT_WAIT)
            return locator
        except PlaywrightTimeoutError:
            print(f"❌ Element not found: {selector}")
            raise
    
    def click_element(self, selector: str):
        """
        Click element
        
        Args:
            selector: CSS selector or XPath
        """
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=config.EXPLICIT_WAIT)
            locator.click()
            print(f"✓ Element clicked: {selector}")
        except PlaywrightTimeoutError:
            print(f"❌ Element could not be clicked: {selector}")
            raise
    
    def input_text(self, selector: str, text: str):
        """
        Input text into input field
        
        Args:
            selector: CSS selector or XPath
            text: Text to input
        """
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=config.EXPLICIT_WAIT)
            locator.clear()
            locator.fill(text)
            print(f"✓ Text inputted: {selector}")
        except PlaywrightTimeoutError:
            print(f"❌ Input field not found: {selector}")
            raise
    
    def get_text(self, selector: str) -> str:
        """
        Get text of element
        
        Args:
            selector: CSS selector or XPath
            
        Returns:
            str: Text of the element
        """
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=config.EXPLICIT_WAIT)
            text = locator.text_content()
            return text or ""
        except PlaywrightTimeoutError:
            print(f"❌ Could not get text of element: {selector}")
            raise
    
    def is_element_visible(self, selector: str) -> bool:
        """
        Check if element is visible
        
        Args:
            selector: CSS selector or XPath
            
        Returns:
            bool: Is the element visible
        """
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible", timeout=config.EXPLICIT_WAIT)
            return locator.is_visible()
        except PlaywrightTimeoutError:
            return False
    
    def wait_for_selector(self, selector: str, timeout: int = None):
        """
        Wait for selector to be visible
        
        Args:
            selector: CSS selector or XPath
            timeout: Wait time (ms)
        """
        wait_timeout = timeout or config.EXPLICIT_WAIT
        try:
            self.page.wait_for_selector(selector, timeout=wait_timeout)
            print(f"✓ Element waited for: {selector}")
        except PlaywrightTimeoutError:
            print(f"❌ Element timeout: {selector}")
            raise
    
    def wait_for_url(self, url: str, timeout: int = None):
        """
        Wait for URL change
        
        Args:
            url: Expected URL (regex or string)
            timeout: Wait time (ms)
        """
        wait_timeout = timeout or config.NAVIGATION_TIMEOUT
        try:
            self.page.wait_for_url(url, timeout=wait_timeout)
            print(f"✓ URL change waited for: {url}")
        except PlaywrightTimeoutError:
            print(f"❌ URL change timeout: {url}")
            raise
    
    def get_current_url(self) -> str:
        """
        Get current URL
        
        Returns:
            str: Current URL
        """
        return self.page.url
    
    def navigate(self, url: str):
        """
        Navigate to page
        
        Args:
            url: URL to navigate to
        """
        self.page.goto(url)
        print(f"✓ Navigated to: {url}")
    
    def take_screenshot(self, filename: str):
        """
        Take screenshot
        
        Args:
            filename: File name
        """
        self.page.screenshot(path=filename)
        print(f"✓ Screenshot taken: {filename}")
    
    def wait(self, seconds: float):
        """
        Wait for specified time
        
        Args:
            seconds: Seconds
        """
        time.sleep(seconds)
        print(f"⏳ {seconds} seconds waited")