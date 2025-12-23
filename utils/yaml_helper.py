"""
YAML Dosyası Yönetimi - Test Senaryolarını Yükle
"""

import yaml
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

# Proje kök dizinini Python path'e ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class YamlScenarioLoader:
    """YAML dosyasından test senaryolarını yükler ve işler"""
    
    def __init__(self, yaml_file_path=None):
        """
        YamlScenarioLoader'ı başlat
        
        Args:
            yaml_file_path: YAML dosyasının yolu 
                          - None ise: proje kök/test_scenarios.yaml kullanır
                          - Dosya adı ise: scenarios/ klasöründen arar
                          - Tam yol ise: direkt açar
        """
        if yaml_file_path is None:
            # Varsayılan: proje kök/test_scenarios.yaml
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            yaml_file_path = os.path.join(project_root, "test_scenarios.yaml")
        else:
            # Eğer tam yol değilse dosya arama yap
            if not os.path.isabs(yaml_file_path) and not os.path.exists(yaml_file_path):
                # scenarios/ klasöründe ara (sadece dosya adı ise)
                if not yaml_file_path.startswith("scenarios/"):
                    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    scenarios_path = os.path.join(project_root, "scenarios", yaml_file_path)
                    if os.path.exists(scenarios_path):
                        yaml_file_path = scenarios_path
        
        self.yaml_file_path = yaml_file_path
        self.scenarios = {}
        self.load_scenarios()
    
    def load_scenarios(self):
        """YAML dosyasını yükle ve parse et"""
        try:
            if not os.path.exists(self.yaml_file_path):
                print(f"❌ YAML dosyası bulunamadı: {self.yaml_file_path}")
                self.scenarios = {}
                return
            
            print(f"🔍 Yüklenen YAML: {self.yaml_file_path}")
            
            with open(self.yaml_file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            if data is None:
                print("⚠ YAML dosyası boş veya parse hatası")
                self.scenarios = {}
                return
            
            if 'test_scenarios' in data:
                self.scenarios = data['test_scenarios']
                if self.scenarios is None:
                    self.scenarios = {}
                else:
                    print(f"✓ YAML dosyası yüklendi: {self.yaml_file_path}")
                    enabled_count = len(self._get_all_enabled_scenarios())
                    print(f"✓ Yüklenen senaryolar: {enabled_count} test")
            else:
                print("⚠ YAML dosyasında test_scenarios anahtarı bulunamadı")
                self.scenarios = {}
                
        except Exception as e:
            print(f"❌ YAML dosyası yükleme hatası: {str(e)}")
            import traceback
            traceback.print_exc()
            self.scenarios = {}
    
    def get_registration_scenarios(self) -> List[Dict[str, Any]]:
        """
        Kayıt (registration) senaryolarını döndür
        
        Returns:
            Liste: Registration test senaryoları
        """
        if not self.scenarios or 'registration' not in self.scenarios:
            return []
        
        scenarios = self.scenarios.get('registration')
        if scenarios is None:
            return []
        
        return [s for s in scenarios if s.get('enabled', True)]
    
    def get_login_scenarios(self) -> List[Dict[str, Any]]:
        """
        Giriş (login) senaryolarını döndür
        
        Returns:
            Liste: Login test senaryoları
        """
        if not self.scenarios or 'login' not in self.scenarios:
            return []
        
        scenarios = self.scenarios.get('login')
        if scenarios is None:
            return []
        
        return [s for s in scenarios if s.get('enabled', True)]

    def get_chat_scenarios(self) -> List[Dict[str, Any]]:
        """
        Chat senaryolarını döndür
        
        Returns:
            Liste: Chat test senaryoları
        """
        if not self.scenarios or 'chat' not in self.scenarios:
            return []
        
        scenarios = self.scenarios.get('chat')
        if scenarios is None:
            return []
        
        return [s for s in scenarios if s.get('enabled', True)]
    
    def get_scenario_by_name(self, scenario_name: str) -> Dict[str, Any]:
        """
        İsme göre senaryo döndür
        
        Args:
            scenario_name: Senaryo ismi
            
        Returns:
            dict: Senaryo bilgisi
        """
        # Scenarios None veya boş kontrol
        if not self.scenarios:
            raise ValueError(f"Senaryolar yüklenmemiş veya boş")
        
        for category in self.scenarios.values():
            if isinstance(category, list):
                for scenario in category:
                    if scenario.get('name') == scenario_name:
                        return scenario
        
        raise ValueError(f"Senaryo bulunamadı: {scenario_name}")
    
    def _get_all_enabled_scenarios(self) -> List[Dict[str, Any]]:
        """Aktif olan tüm senaryoları döndür (private)"""
        all_scenarios = []
        if not self.scenarios:
            return all_scenarios
        try:
            for category in self.scenarios.values():
                if isinstance(category, list):
                    all_scenarios.extend([s for s in category if s.get('enabled', True)])
        except Exception as e:
            print(f"⚠ Senaryo döngü hatası: {str(e)}")
            return []
        return all_scenarios
    
    def get_all_enabled_scenarios(self) -> List[Dict[str, Any]]:
        """
        Aktif olan tüm senaryoları döndür
        
        Returns:
            Liste: Tüm etkin senaryolar
        """
        return self._get_all_enabled_scenarios()
    
    def get_scenario_steps(self, scenario_name: str) -> List[Dict[str, Any]]:
        """
        Senaryo adımlarını döndür
        
        Args:
            scenario_name: Senaryo ismi
            
        Returns:
            liste: Adım listesi
        """
        scenario = self.get_scenario_by_name(scenario_name)
        return scenario.get('steps', [])
    
    def get_scenario_assertions(self, scenario_name: str) -> List[Dict[str, Any]]:
        """
        Senaryo assertions'larını döndür
        
        Args:
            scenario_name: Senaryo ismi
            
        Returns:
            liste: Assertion listesi
        """
        scenario = self.get_scenario_by_name(scenario_name)
        return scenario.get('assertions', [])
    
    def process_dynamic_values(self, value: Any) -> Any:
        """
        Dinamik değerleri işle (örn: {{timestamp}})
        
        Args:
            value: İşlenecek değer
            
        Returns:
            İşlenmiş değer
        """
        if isinstance(value, str):
            if '{{timestamp}}' in value:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
                return value.replace('{{timestamp}}', timestamp)
            
            if '{{date}}' in value:
                date_str = datetime.now().strftime("%Y%m%d")
                return value.replace('{{date}}', date_str)
            
            if '{{random}}' in value:
                import random
                rand_num = str(random.randint(10000, 99999))
                return value.replace('{{random}}', rand_num)
        
        return value
    
    def get_step_parameters(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adımın parametrelerini al (dinamik değerler işlenmiş halde)
        
        Args:
            step: Adım bilgisi
            
        Returns:
            dict: İşlenmiş parametreler
        """
        parameters = {}
        
        for key, value in step.items():
            if key != 'action':
                parameters[key] = self.process_dynamic_values(value)
        
        return parameters
    
    def print_scenario_summary(self, scenario_name: str):
        """
        Senaryo özetini yazdır
        
        Args:
            scenario_name: Senaryo ismi
        """
        scenario = self.get_scenario_by_name(scenario_name)
        
        print("\n" + "="*50)
        print(f"📋 Senaryo: {scenario.get('name')}")
        print(f"📝 Açıklama: {scenario.get('description')}")
        print(f"✓ Aktif: {scenario.get('enabled', True)}")
        
        steps = scenario.get('steps', [])
        print(f"\n📌 Adımlar ({len(steps)}):")
        for i, step in enumerate(steps, 1):
            print(f"  {i}. {step.get('action', 'unknown')}")
        
        assertions = scenario.get('assertions', [])
        print(f"\n✔️ Doğrulamalar ({len(assertions)}):")
        for i, assertion in enumerate(assertions, 1):
            print(f"  {i}. {assertion.get('type', 'unknown')}")
        
        print("="*50 + "\n")


def load_test_scenarios(yaml_file_path=None) -> YamlScenarioLoader:
    """
    YAML dosyasından test senaryolarını yükle (helper function)
    
    Args:
        yaml_file_path: YAML dosyasının yolu
        
    Returns:
        YamlScenarioLoader: Loader nesnesi
    """
    return YamlScenarioLoader(yaml_file_path)


if __name__ == "__main__":
    # Test amaçlı kullanım
    loader = load_test_scenarios()
    
    print("\n" + "="*50)
    print("📚 KAYIT SENARYOLARı")
    print("="*50)
    for scenario in loader.get_registration_scenarios():
        loader.print_scenario_summary(scenario['name'])
    
    print("\n" + "="*50)
    print("📚 GİRİŞ SENARYOLARı")
    print("="*50)
    for scenario in loader.get_login_scenarios():
        loader.print_scenario_summary(scenario['name'])
