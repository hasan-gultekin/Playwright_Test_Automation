"""
Pytest configuration and shared fixtures (Playwright compatible)
"""
import pytest
import sys
import os
import time

# Proje kök dizinini Python path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('tests', ''))

from pages.login_page import LoginPage
from utils.driver_helper import get_browser, get_page, close_browser
import config


@pytest.fixture(scope="function")
def browser():
    """Browser fixture - Stays open throughout the test"""
    browser_instance = get_browser()
    yield browser_instance
    # Close the browser after the test
    close_browser(browser_instance)


@pytest.fixture(scope="function")
def page(browser):
    """Page fixture - New page for each test"""
    page_instance = get_page(browser)
    yield page_instance


@pytest.fixture(scope="function")
def logged_in_page(page):
    """
    Precondition: Returns a page with the user logged in
    Performs the login process and keeps the page open
    """
    login_page = LoginPage(page)
    
    print("\n" + "="*60)
    print("PRECONDITION: Login process is starting...")
    print("="*60)
    
    # Go to the home page
    page.goto(config.BASE_URL)
    print(f"✓ Navigated to home page: {config.BASE_URL}")
    time.sleep(2)
    
    # Click the login link
    login_page.click_login_link()
    print("✓ Navigated to login page")
    time.sleep(2)
    
    # Fill the login form
    login_page.fill_login_form(
        config.LOGIN_USER,
        config.LOGIN_PASSWORD
    )
    print(f"✓ Form filled (Email: {config.LOGIN_USER})")
    time.sleep(1)
    
    # Submit the form
    login_page.submit_login()
    print("✓ Form submitted")
    time.sleep(5)
    
    # Successful login verification
    assert login_page.is_login_successful(), "Login failed!"
    
    current_url = login_page.get_current_url()
    print(f"✓ Login successful! URL: {current_url}")
    print("="*60)
    print("PRECONDITION COMPLETED - Test scenario is starting...")
    print("="*60 + "\n")
    
    yield page
    # Page closing will be handled by the browser fixture

