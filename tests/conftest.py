"""
Pytest configuration and shared fixtures (Playwright uyumlu)
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
    """Browser fixture - Test boyunca açık kalır"""
    browser_instance = get_browser()
    yield browser_instance
    # Test bittikten sonra browser'ı kapat
    close_browser(browser_instance)


@pytest.fixture(scope="function")
def page(browser):
    """Page fixture - Her test için yeni bir page"""
    page_instance = get_page(browser)
    yield page_instance


@pytest.fixture(scope="function")
def logged_in_page(page):
    """
    Precondition: Kullanıcı giriş yapmış page döndürür
    Login işlemini gerçekleştirir ve page'ı açık tutar
    """
    login_page = LoginPage(page)
    
    print("\n" + "="*60)
    print("PRECONDITION: Login işlemi başlatılıyor...")
    print("="*60)
    
    # Ana sayfaya git
    page.goto(config.BASE_URL)
    print(f"✓ Ana sayfaya gidildi: {config.BASE_URL}")
    time.sleep(2)
    
    # Giriş yap linkine tıkla
    login_page.click_login_link()
    print("✓ Giriş sayfasına gidildi")
    time.sleep(2)
    
    # Giriş formunu doldur
    login_page.fill_login_form(
        config.LOGIN_USER,
        config.LOGIN_PASSWORD
    )
    print(f"✓ Form dolduruldu (Email: {config.LOGIN_USER})")
    time.sleep(1)
    
    # Formu gönder
    login_page.submit_login()
    print("✓ Form gönderildi")
    time.sleep(5)
    
    # Başarılı giriş doğrulaması
    assert login_page.is_login_successful(), "Giriş başarısız!"
    
    current_url = login_page.get_current_url()
    print(f"✓ Giriş başarılı! URL: {current_url}")
    print("="*60)
    print("PRECONDITION TAMAMLANDI - Test senaryosu başlıyor...")
    print("="*60 + "\n")
    
    yield page
    # Page'ı kapatma, browser fixture'ı yapacak

