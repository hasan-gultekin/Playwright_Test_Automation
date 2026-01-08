"""
Generic YAML Method Test Runner - YAML'da belirtilen page metodlarını çalıştırır (Playwright uyumlu)

Kullanım:
  py -m pytest tests/test_runner.py -v -s
"""

import pytest
import sys
import os

# Proje kök dizinini Python path'e ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_helper import get_browser, get_page, close_browser
from utils.yaml_helper import load_test_scenarios
from utils.yaml_method_executor import YamlMethodExecutor
import config


class TestYamlMethods:
    """
    YAML'da belirtilen page metodlarını çalıştıran generic test class
    
    YAML Yapısı:
      - name: "scenario_name"
        page: "LoginPage"
        method: "execute_successful_login_flow"
        params:
          email: "user@test.com"
          password: "Pass123"
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Test başlamadan önce browser'ı başlat"""
        self.browser = get_browser()
        self.page = get_page(self.browser)
        
        # YAML loader'ı başlat - scenarios/ klasöründeki tüm YAML'ları otomatik yükle
        self.scenario_loader = load_test_scenarios()
        
        # Eğer senaryolar boşsa, uyarı ver
        if not self.scenario_loader.scenarios:
            print("\n⚠️  YAML Senaryo Uyarısı:")
            print("   Senaryolar yüklenmedi veya boş. Lütfen scenarios/ klasöründe YAML dosyaları kontrol edin.")
            print("   Beklenen dosyalar: TC_001_registration.yaml, TC_002_login.yaml, vb.")
        
        # Method executor'ı başlat
        self.executor = YamlMethodExecutor(self.page, self.scenario_loader)
        
        yield
        # Test bittikten sonra browser'ı kapat
        close_browser(self.browser)
    
    def test_all_registration_scenarios(self):
        """
        YAML'daki tüm registration senaryolarını çalıştır
        """
        scenarios = self.scenario_loader.get_registration_scenarios()
        
        # None check
        if scenarios is None:
            scenarios = []
        
        assert len(scenarios) > 0, "YAML'da registration senaryosu bulunamadı"
        
        print(f"\n🎯 {len(scenarios)} registration senaryosu bulundu\n")
        
        # Her senaryo için test çalıştır
        results = []
        for scenario in scenarios:
            scenario_name = scenario['name']
            print(f"\n{'*'*70}")
            print(f"📋 Senaryo çalıştırılıyor: {scenario_name}")
            print(f"{'*'*70}")
            
            # YAML Method Executor'u kullan
            result = self.executor.execute_scenario(scenario_name)
            results.append(result)
            
            # Sonucu assert et
            assert result['success'], \
                f"Senaryo başarısız: {scenario_name}\nHata: {result['message']}"
        
        print(f"\n✅ Tüm registration senaryoları başarılı ({len(results)})")
    
    def test_all_login_scenarios(self):
        """
        YAML'daki tüm login senaryolarını çalıştır
        """
        scenarios = self.scenario_loader.get_login_scenarios()
        
        # None check
        if scenarios is None:
            scenarios = []
        
        assert len(scenarios) > 0, "YAML'da login senaryosu bulunamadı"
        
        print(f"\n🎯 {len(scenarios)} login senaryosu bulundu\n")
        
        # Her senaryo için test çalıştır
        results = []
        for scenario in scenarios:
            scenario_name = scenario['name']
            print(f"\n{'*'*70}")
            print(f"📋 Senaryo çalıştırılıyor: {scenario_name}")
            print(f"{'*'*70}")
            
            # YAML Method Executor'u kullan
            result = self.executor.execute_scenario(scenario_name)
            results.append(result)
            
            # Sonucu assert et
            assert result['success'], \
                f"Senaryo başarısız: {scenario_name}\nHata: {result['message']}"
        
        print(f"\n✅ Tüm login senaryoları başarılı ({len(results)})")
    
    def test_all_chat_scenarios(self):
        """
        YAML'daki tüm chat senaryolarını çalıştır
        """
        scenarios = self.scenario_loader.get_chat_scenarios()
        
        # None check
        if scenarios is None:
            scenarios = []
        
        if len(scenarios) == 0:
            print("⚠️  Chat senaryosu bulunamadı - test atlanıyor")
            return
        
        print(f"\n🎯 {len(scenarios)} chat senaryosu bulundu\n")
        
        # Her senaryo için test çalıştır
        results = []
        for scenario in scenarios:
            scenario_name = scenario['name']
            print(f"\n{'*'*70}")
            print(f"📋 Senaryo çalıştırılıyor: {scenario_name}")
            print(f"{'*'*70}")
            
            # YAML Method Executor'u kullan
            result = self.executor.execute_scenario(scenario_name)
            results.append(result)
            
            # Sonucu assert et
            assert result['success'], \
                f"Senaryo başarısız: {scenario_name}\nHata: {result['message']}"
        
        print(f"\n✅ Tüm chat senaryoları başarılı ({len(results)})")
    
    @pytest.mark.parametrize("scenario_name", [
        "successful_registration",
        "registration_with_custom_data"
    ])
    def test_registration_scenarios_parametrized(self, scenario_name):
        """
        Registration senaryolarını parametreli test ile çalıştır
        Her senaryo ayrı test olarak görünür
        """
        print(f"\n{'='*70}")
        print(f"🧪 Parametreli Test: {scenario_name}")
        print(f"{'='*70}\n")
        
        result = self.executor.execute_scenario(scenario_name)
        
        assert result['success'], \
            f"Senaryo başarısız: {scenario_name}\nHata: {result['message']}"
    
    @pytest.mark.parametrize("scenario_name", [
        "successful_login",
        "login_with_config_credentials"
    ])
    def test_login_scenarios_parametrized(self, scenario_name):
        """
        Login senaryolarını parametreli test ile çalıştır
        Her senaryo ayrı test olarak görünür
        """
        print(f"\n{'='*70}")
        print(f"🧪 Parametreli Test: {scenario_name}")
        print(f"{'='*70}\n")
        
        result = self.executor.execute_scenario(scenario_name)
        
        assert result['success'], \
            f"Senaryo başarısız: {scenario_name}\nHata: {result['message']}"
    
    def test_yaml_scenario_info(self):
        """YAML runner'ın bilgilerini göster"""
        print("\n" + "="*70)
        print("📚 YAML METHOD RUNNER HAKKINDA")
        print("="*70)
        
        all_scenarios = (
            self.scenario_loader.get_registration_scenarios() +
            self.scenario_loader.get_login_scenarios()
        )
        
        print(f"\n✓ Toplam Senaryo: {len(all_scenarios)}")
        print(f"✓ Registration: {len(self.scenario_loader.get_registration_scenarios())}")
        print(f"✓ Login: {len(self.scenario_loader.get_login_scenarios())}")
        
        print(f"\n📋 Senaryo Listesi:")
        for i, scenario in enumerate(all_scenarios, 1):
            enabled = "✅" if scenario.get('enabled', True) else "❌"
            page = scenario.get('page', 'N/A')
            method = scenario.get('method', 'N/A')
            print(f"   {i}. {enabled} {scenario['name']}")
            print(f"      Page: {page} | Method: {method}")
        
        print("\n" + "="*70)
        assert True


class TestYamlScenariosByMethod:
    """
    Metoda göre ayrılmış test class (Direct method calling)
    Her senaryo için ayrı browser session açılır
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup"""
        self.browser = get_browser()
        self.page = get_page(self.browser)
        self.scenario_loader = load_test_scenarios()
        self.executor = YamlMethodExecutor(self.page, self.scenario_loader)
        yield
        close_browser(self.browser)
    
    def test_successful_registration(self):
        """YAML Senaryo: Başarılı Kayıt"""
        result = self.executor.execute_scenario("successful_registration")
        assert result['success'], result['message']
    
    def test_registration_with_custom_data(self):
        """YAML Senaryo: Özel Verilerle Kayıt"""
        result = self.executor.execute_scenario("registration_with_custom_data")
        assert result['success'], result['message']
    
    def test_successful_login(self):
        """YAML Senaryo: Başarılı Giriş"""
        result = self.executor.execute_scenario("successful_login")
        assert result['success'], result['message']
    
    def test_login_with_config_credentials(self):
        """YAML Senaryo: Config Verilerle Giriş"""
        result = self.executor.execute_scenario("login_with_config_credentials")
        assert result['success'], result['message']


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])

    
    def test_all_registration_scenarios(self):
        """
        YAML'daki tüm registration senaryolarını çalıştır
        """
        scenarios = self.scenario_loader.get_registration_scenarios()
        
        # None check
        if scenarios is None:
            scenarios = []
        
        assert len(scenarios) > 0, "YAML'da registration senaryosu bulunamadı"
        
        print(f"\n🎯 {len(scenarios)} registration senaryosu bulundu\n")
        
        # Her senaryo için test çalıştır
        results = []
        for scenario in scenarios:
            scenario_name = scenario['name']
            print(f"\n{'*'*70}")
            print(f"📋 Senaryo çalıştırılıyor: {scenario_name}")
            print(f"{'*'*70}")
            
            # YAML Method Executor'u kullan
            result = self.executor.execute_scenario(scenario_name)
            results.append(result)
            
            # Sonucu assert et
            assert result['success'], \
                f"Senaryo başarısız: {scenario_name}\nHata: {result['message']}"
        
        print(f"\n✅ Tüm registration senaryoları başarılı ({len(results)})")
    
    def test_all_login_scenarios(self):
        """
        YAML'daki tüm login senaryolarını çalıştır
        """
        scenarios = self.scenario_loader.get_login_scenarios()
        
        # None check
        if scenarios is None:
            scenarios = []
        
        assert len(scenarios) > 0, "YAML'da login senaryosu bulunamadı"
        
        print(f"\n🎯 {len(scenarios)} login senaryosu bulundu\n")
        
        # Her senaryo için test çalıştır
        results = []
        for scenario in scenarios:
            scenario_name = scenario['name']
            print(f"\n{'*'*70}")
            print(f"📋 Senaryo çalıştırılıyor: {scenario_name}")
            print(f"{'*'*70}")
            
            # YAML Method Executor'u kullan
            result = self.executor.execute_scenario(scenario_name)
            results.append(result)
            
            # Sonucu assert et
            assert result['success'], \
                f"Senaryo başarısız: {scenario_name}\nHata: {result['message']}"
        
        print(f"\n✅ Tüm login senaryoları başarılı ({len(results)})")
    
    def test_all_chat_scenarios(self):
        """
        YAML'daki tüm chat senaryolarını çalıştır
        """
        scenarios = self.scenario_loader.get_chat_scenarios()
        
        # None check
        if scenarios is None:
            scenarios = []
        
        if len(scenarios) == 0:
            print("⚠️  Chat senaryosu bulunamadı - test atlanıyor")
            return
        
        print(f"\n🎯 {len(scenarios)} chat senaryosu bulundu\n")
        
        # Her senaryo için test çalıştır
        results = []
        for scenario in scenarios:
            scenario_name = scenario['name']
            print(f"\n{'*'*70}")
            print(f"📋 Senaryo çalıştırılıyor: {scenario_name}")
            print(f"{'*'*70}")
            
            # YAML Method Executor'u kullan
            result = self.executor.execute_scenario(scenario_name)
            results.append(result)
            
            # Sonucu assert et
            assert result['success'], \
                f"Senaryo başarısız: {scenario_name}\nHata: {result['message']}"
        
        print(f"\n✅ Tüm chat senaryoları başarılı ({len(results)})")
    
    @pytest.mark.parametrize("scenario_name", [
        "successful_registration",
        "registration_with_custom_data"
    ])
    def test_registration_scenarios_parametrized(self, scenario_name):
        """
        Registration senaryolarını parametreli test ile çalıştır
        Her senaryo ayrı test olarak görünür
        """
        print(f"\n{'='*70}")
        print(f"🧪 Parametreli Test: {scenario_name}")
        print(f"{'='*70}\n")
        
        result = self.executor.execute_scenario(scenario_name)
        
        assert result['success'], \
            f"Senaryo başarısız: {scenario_name}\nHata: {result['message']}"
    
    @pytest.mark.parametrize("scenario_name", [
        "successful_login",
        "login_with_config_credentials"
    ])
    def test_login_scenarios_parametrized(self, scenario_name):
        """
        Login senaryolarını parametreli test ile çalıştır
        Her senaryo ayrı test olarak görünür
        """
        print(f"\n{'='*70}")
        print(f"🧪 Parametreli Test: {scenario_name}")
        print(f"{'='*70}\n")
        
        result = self.executor.execute_scenario(scenario_name)
        
        assert result['success'], \
            f"Senaryo başarısız: {scenario_name}\nHata: {result['message']}"
    
    def test_yaml_scenario_info(self):
        """YAML runner'ın bilgilerini göster"""
        print("\n" + "="*70)
        print("📚 YAML METHOD RUNNER HAKKINDA")
        print("="*70)
        
        all_scenarios = (
            self.scenario_loader.get_registration_scenarios() +
            self.scenario_loader.get_login_scenarios()
        )
        
        print(f"\n✓ Toplam Senaryo: {len(all_scenarios)}")
        print(f"✓ Registration: {len(self.scenario_loader.get_registration_scenarios())}")
        print(f"✓ Login: {len(self.scenario_loader.get_login_scenarios())}")
        
        print(f"\n📋 Senaryo Listesi:")
        for i, scenario in enumerate(all_scenarios, 1):
            enabled = "✅" if scenario.get('enabled', True) else "❌"
            page = scenario.get('page', 'N/A')
            method = scenario.get('method', 'N/A')
            print(f"   {i}. {enabled} {scenario['name']}")
            print(f"      Page: {page} | Method: {method}")
        
        print("\n" + "="*70)
        assert True


class TestYamlScenariosByMethod:
    """
    Metoda göre ayrılmış test class (Direct method calling)
    Her senaryo için ayrı browser session açılır
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup"""
        self.driver = get_chrome_driver()
        self.driver.implicitly_wait(config.IMPLICIT_WAIT)
        self.scenario_loader = load_test_scenarios()
        self.executor = YamlMethodExecutor(self.driver, self.scenario_loader)
        yield
        self.driver.quit()
    
    def test_successful_registration(self):
        """YAML Senaryo: Başarılı Kayıt"""
        result = self.executor.execute_scenario("successful_registration")
        assert result['success'], result['message']
    
    def test_registration_with_custom_data(self):
        """YAML Senaryo: Özel Verilerle Kayıt"""
        result = self.executor.execute_scenario("registration_with_custom_data")
        assert result['success'], result['message']
    
    def test_successful_login(self):
        """YAML Senaryo: Başarılı Giriş"""
        result = self.executor.execute_scenario("successful_login")
        assert result['success'], result['message']
    
    def test_login_with_config_credentials(self):
        """YAML Senaryo: Config Verilerle Giriş"""
        result = self.executor.execute_scenario("login_with_config_credentials")
        assert result['success'], result['message']


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
