"""
Generic YAML Method Test Runner - Runs page methods specified in YAML (Playwright compatible)

Usage:
  py -m pytest tests/test_runner.py -v -s
"""

import pytest
import sys
import os

# Add project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_helper import get_browser, get_page, close_browser
from utils.yaml_helper import load_test_scenarios
from utils.yaml_method_executor import YamlMethodExecutor
import config


class TestYamlMethods:
    """
    Generic test class that runs page methods specified in YAML
    
    YAML Structure:
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
        
        # Initialize YAML loader - automatically load all YAMLs in the scenarios/ folder
        self.scenario_loader = load_test_scenarios()
        
        # If scenarios are empty, warn
        if not self.scenario_loader.scenarios:
            print("\n⚠️  YAML Scenario Warning:")
            print("   Scenarios not loaded or empty. Please check YAML files in the scenarios/ folder.")
            print("   Expected files: TC_001_registration.yaml, TC_002_login.yaml, etc.")
        
        # Initialize method executor
        self.executor = YamlMethodExecutor(self.page, self.scenario_loader)
        
        yield
        # Close the browser after the test
        close_browser(self.browser)
    
    def test_all_registration_scenarios(self):
        """
        Runs all registration scenarios in YAML
        """
        scenarios = self.scenario_loader.get_registration_scenarios()
        
        # None check
        if scenarios is None:
            scenarios = []
        
        assert len(scenarios) > 0, "No registration scenarios found in YAML"
        
        print(f"\n🎯 {len(scenarios)} registration scenarios found\n")
        
        # Run test for each scenario
        results = []
        for scenario in scenarios:
            scenario_name = scenario['name']
            print(f"\n{'*'*70}")
            print(f"📋 Running scenario: {scenario_name}")
            print(f"{'*'*70}")
            
            # Use YAML Method Executor
            result = self.executor.execute_scenario(scenario_name)
            results.append(result)
            
            # Assert the result
            assert result['success'], \
                f"Scenario failed: {scenario_name}\nError: {result['message']}"
        
        print(f"\n✅ All registration scenarios passed ({len(results)})")
    
    def test_all_login_scenarios(self):
        """
        Runs all login scenarios in YAML
        """
        scenarios = self.scenario_loader.get_login_scenarios()
        
        # None check
        if scenarios is None:
            scenarios = []
        
        assert len(scenarios) > 0, "No login scenarios found in YAML"
        
        print(f"\n🎯 {len(scenarios)} login scenarios found\n")
        
        # Run test for each scenario
        results = []
        for scenario in scenarios:
            scenario_name = scenario['name']
            print(f"\n{'*'*70}")
            print(f"📋 Running scenario: {scenario_name}")
            print(f"{'*'*70}")
            
            # Use YAML Method Executor
            result = self.executor.execute_scenario(scenario_name)
            results.append(result)
            
            # Assert the result
            assert result['success'], \
                f"Scenario failed: {scenario_name}\nError: {result['message']}"
        
        print(f"\n✅ All login scenarios passed ({len(results)})")
    
    def test_all_chat_scenarios(self):
        """
        Runs all chat scenarios in YAML
        """
        scenarios = self.scenario_loader.get_chat_scenarios()
        
        # None check
        if scenarios is None:
            scenarios = []
        
        if len(scenarios) == 0:
            print("⚠️  No chat scenarios found - skipping test")
            return
        
        print(f"\n🎯 {len(scenarios)} chat scenarios found\n")
        
        # Run test for each scenario
        results = []
        for scenario in scenarios:
            scenario_name = scenario['name']
            print(f"\n{'*'*70}")
            print(f"📋 Running scenario: {scenario_name}")
            print(f"{'*'*70}")
            
            # Use YAML Method Executor
            result = self.executor.execute_scenario(scenario_name)
            results.append(result)
            
            # Assert the result
            assert result['success'], \
                f"Scenario failed: {scenario_name}\nError: {result['message']}"
        
        print(f"\n✅ All chat scenarios passed ({len(results)})")
    
    @pytest.mark.parametrize("scenario_name", [
        "successful_registration",
        "registration_with_custom_data"
    ])
    def test_registration_scenarios_parametrized(self, scenario_name):
        """
       Runs registration scenarios with parameterized tests
        Each scenario appears as a separate test
        """
        print(f"\n{'='*70}")
        print(f"🧪 Parameterized Test: {scenario_name}")
        print(f"{'='*70}\n")
        
        result = self.executor.execute_scenario(scenario_name)
        
        assert result['success'], \
            f"Scenario failed: {scenario_name}\nError: {result['message']}"
    
    @pytest.mark.parametrize("scenario_name", [
        "successful_login",
        "login_with_config_credentials"
    ])
    def test_login_scenarios_parametrized(self, scenario_name):
        """
        Runs login scenarios with parameterized tests
        Each scenario appears as a separate test
        """
        print(f"\n{'='*70}")
        print(f"🧪 Parameterized Test: {scenario_name}")
        print(f"{'='*70}\n")
        
        result = self.executor.execute_scenario(scenario_name)
        
        assert result['success'], \
            f"Scenario failed: {scenario_name}\nError: {result['message']}"
    
    def test_yaml_scenario_info(self):
        """Show information about the YAML runner"""
        print("\n" + "="*70)
        print("📚 ABOUT YAML METHOD RUNNER")
        print("="*70)
        
        all_scenarios = (
            self.scenario_loader.get_registration_scenarios() +
            self.scenario_loader.get_login_scenarios()
        )
        
        print(f"\n✓ Total Scenarios: {len(all_scenarios)}")
        print(f"✓ Registration: {len(self.scenario_loader.get_registration_scenarios())}")
        print(f"✓ Login: {len(self.scenario_loader.get_login_scenarios())}")
        
        print(f"\n📋 Scenario List:")
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
    Test class separated by method (Direct method calling)
    Each scenario opens a separate browser session
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
        """YAML Scenario: Successful Registration"""
        result = self.executor.execute_scenario("successful_registration")
        assert result['success'], result['message']
    
    def test_registration_with_custom_data(self):
        """YAML Scenario: Registration with Custom Data"""
        result = self.executor.execute_scenario("registration_with_custom_data")
        assert result['success'], result['message']
    
    def test_successful_login(self):
        """YAML Scenario: Successful Login"""
        result = self.executor.execute_scenario("successful_login")
        assert result['success'], result['message']
    
    def test_login_with_config_credentials(self):
        """YAML Scenario: Login with Config Credentials"""
        result = self.executor.execute_scenario("login_with_config_credentials")
        assert result['success'], result['message']


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])

    
    def test_all_registration_scenarios(self):
        """
        Runs all registration scenarios from YAML
        """
        scenarios = self.scenario_loader.get_registration_scenarios()
        
        # None check
        if scenarios is None:
            scenarios = []
        
        assert len(scenarios) > 0, "No registration scenarios found in YAML"
        
        print(f"\n🎯 {len(scenarios)} registration scenarios found\n")
        
        # Run test for each scenario
        results = []
        for scenario in scenarios:
            scenario_name = scenario['name']
            print(f"\n{'*'*70}")
            print(f"📋 Scenario running: {scenario_name}")
            print(f"{'*'*70}")
            
            # Use YAML Method Executor
            result = self.executor.execute_scenario(scenario_name)
            results.append(result)
            
            # Assert the result
            assert result['success'], \
                f"Scenario failed: {scenario_name}\nError: {result['message']}"
        
        print(f"\n✅ All registration scenarios passed ({len(results)})")
    
    def test_all_login_scenarios(self):
        """
        Runs all login scenarios from YAML
        """
        scenarios = self.scenario_loader.get_login_scenarios()
        
        # None check
        if scenarios is None:
            scenarios = []
        
        assert len(scenarios) > 0, "No login scenarios found in YAML"
        
        print(f"\n🎯 {len(scenarios)} login scenarios found\n")
        
        # Run test for each scenario
        results = []
        for scenario in scenarios:
            scenario_name = scenario['name']
            print(f"\n{'*'*70}")
            print(f"📋 Scenario running: {scenario_name}")
            print(f"{'*'*70}")
            
            # Use YAML Method Executor
            result = self.executor.execute_scenario(scenario_name)
            results.append(result)
            
            # Assert the result
            assert result['success'], \
                f"Scenario failed: {scenario_name}\nError: {result['message']}"
        
        print(f"\n✅ All login scenarios passed ({len(results)})")
    
    def test_all_chat_scenarios(self):
        """
        Runs all chat scenarios from YAML
        """
        scenarios = self.scenario_loader.get_chat_scenarios()
        
        # None check
        if scenarios is None:
            scenarios = []
        
        if len(scenarios) == 0:
            print("⚠️  No chat scenarios found - skipping test")
            return
        
        print(f"\n🎯 {len(scenarios)} chat scenarios found\n")
        
        # Run test for each scenario
        results = []
        for scenario in scenarios:
            scenario_name = scenario['name']
            print(f"\n{'*'*70}")
            print(f"📋 Scenario running: {scenario_name}")
            print(f"{'*'*70}")
            
            # Use YAML Method Executor
            result = self.executor.execute_scenario(scenario_name)
            results.append(result)
            
            # Assert the result
            assert result['success'], \
                f"Scenario failed: {scenario_name}\nError: {result['message']}"
        
        print(f"\n✅ All chat scenarios passed ({len(results)})")
    
    @pytest.mark.parametrize("scenario_name", [
        "successful_registration",
        "registration_with_custom_data"
    ])
    def test_registration_scenarios_parametrized(self, scenario_name):
        """
        Runs registration scenarios with parameterized test
        Each scenario appears as a separate test
        """
        print(f"\n{'='*70}")
        print(f"🧪 Parameterized Test: {scenario_name}")
        print(f"{'='*70}\n")
        
        result = self.executor.execute_scenario(scenario_name)
        
        assert result['success'], \
            f"Scenario failed: {scenario_name}\nError: {result['message']}"
    
    @pytest.mark.parametrize("scenario_name", [
        "successful_login",
        "login_with_config_credentials"
    ])
    def test_login_scenarios_parametrized(self, scenario_name):
        """
        Runs login scenarios with parameterized test
        Each scenario appears as a separate test
        """
        print(f"\n{'='*70}")
        print(f"🧪 Parameterized Test: {scenario_name}")
        print(f"{'='*70}\n")
        
        result = self.executor.execute_scenario(scenario_name)
        
        assert result['success'], \
            f"Scenario failed: {scenario_name}\nError: {result['message']}"
    
    def test_yaml_scenario_info(self):
        """Shows information about the YAML runner"""
        print("\n" + "="*70)
        print("📚 ABOUT YAML METHOD RUNNER")
        print("="*70)
        
        all_scenarios = (
            self.scenario_loader.get_registration_scenarios() +
            self.scenario_loader.get_login_scenarios()
        )
        
        print(f"\n✓ Total Scenarios: {len(all_scenarios)}")
        print(f"✓ Registration: {len(self.scenario_loader.get_registration_scenarios())}")
        print(f"✓ Login: {len(self.scenario_loader.get_login_scenarios())}")
        
        print(f"\n📋 Scenario List:")
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
    Test class separated by method (Direct method calling)
    Each scenario opens a separate browser session
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
        """YAML Scenario: Successful Registration"""
        result = self.executor.execute_scenario("successful_registration")
        assert result['success'], result['message']
    
    def test_registration_with_custom_data(self):
        """YAML Scenario: Registration with Custom Data"""
        result = self.executor.execute_scenario("registration_with_custom_data")
        assert result['success'], result['message']
    
    def test_successful_login(self):
        """YAML Scenario: Successful Login"""
        result = self.executor.execute_scenario("successful_login")
        assert result['success'], result['message']
    
    def test_login_with_config_credentials(self):
        """YAML Scenario: Login with Config Credentials"""
        result = self.executor.execute_scenario("login_with_config_credentials")
        assert result['success'], result['message']


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
