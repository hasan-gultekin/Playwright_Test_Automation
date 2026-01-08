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
                          - None ise: scenarios/ klasöründen senaryoları toplar
                          - Dosya adı ise: scenarios/ klasöründen arar
                          - Tam yol ise: direkt açar
        """
        self.yaml_file_path = yaml_file_path
        self.scenarios = {}
        self.load_scenarios()
    
    def _find_yaml_file(self, yaml_file_path):
        """YAML dosyasını bulur"""
        if yaml_file_path is None:
            return None
        
        # Eğer dosya zaten varsa, direkt döndür
        if os.path.exists(yaml_file_path):
            return os.path.abspath(yaml_file_path)
        
        # Eğer tam yol değilse scenarios/ klasöründe ara
        if not os.path.isabs(yaml_file_path):
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # scenarios/ klasöründe ara
            scenarios_path = os.path.join(project_root, yaml_file_path)
            if os.path.exists(scenarios_path):
                return os.path.abspath(scenarios_path)
            
            # Sadece dosya adı ise, scenarios/ içinde ara
            if not yaml_file_path.startswith("scenarios"):
                scenarios_path = os.path.join(project_root, "scenarios", yaml_file_path)
                if os.path.exists(scenarios_path):
                    return os.path.abspath(scenarios_path)
        
        return None  # Bulunamıyorsa None döndür
    
    def load_scenarios(self):
        """YAML dosyasını yükle ve parse et"""
        try:
            # Dosya bulma işlemini yap
            yaml_file = self._find_yaml_file(self.yaml_file_path)
            
            # Belirli bir dosya varsa, onu yükle
            if yaml_file and os.path.exists(yaml_file):
                print(f"🔍 Yüklenen YAML: {yaml_file}")
                self._load_yaml_file(yaml_file)
                return
            
            # Eğer None veya bulunamadıysa, scenarios/ klasöründeki tüm YAML'ları topla
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            scenarios_dir = os.path.join(project_root, "scenarios")
            
            if os.path.exists(scenarios_dir):
                print(f"🔍 Senaryo dosyaları aranıyor: {scenarios_dir}")
                self._load_all_yaml_in_directory(scenarios_dir)
            else:
                print(f"❌ Senaryo klasörü bulunamadı: {scenarios_dir}")
                self.scenarios = {}
                
        except Exception as e:
            print(f"❌ YAML dosyası yükleme hatası: {str(e)}")
            import traceback
            traceback.print_exc()
            self.scenarios = {}
    
    def _load_yaml_file(self, yaml_file_path):
        """Tek bir YAML dosyasını yükle"""
        try:
            with open(yaml_file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            if data is None:
                print(f"⚠ YAML dosyası boş: {yaml_file_path}")
                return
            
            # test_scenarios anahtarını ara
            if 'test_scenarios' in data:
                self.scenarios.update(data['test_scenarios'])
                enabled_count = len(self._get_all_enabled_scenarios())
                print(f"✓ YAML yüklendi: {os.path.basename(yaml_file_path)} ({enabled_count} senaryo)")
            elif 'scenarios' in data:
                # Alternatif format: scenarios
                scenarios_data = data['scenarios']
                if isinstance(scenarios_data, list):
                    # Kategori belirlemek için scenario'ların ilk harfine bak
                    for scenario in scenarios_data:
                        self.scenarios.setdefault('default', []).append(scenario)
                    print(f"✓ YAML yüklendi: {os.path.basename(yaml_file_path)}")
        except Exception as e:
            print(f"❌ YAML parse hatası ({yaml_file_path}): {str(e)}")
    
    def _load_all_yaml_in_directory(self, directory):
        """Klasördeki tüm YAML dosyalarını yükle"""
        try:
            yaml_files = [f for f in os.listdir(directory) if f.endswith('.yaml')]
            
            if not yaml_files:
                print(f"⚠ {directory} klasöründe YAML dosyası bulunamadı")
                return
            
            print(f"📂 Bulundu {len(yaml_files)} YAML dosyası")
            
            for yaml_file in sorted(yaml_files):
                yaml_path = os.path.join(directory, yaml_file)
                self._load_yaml_file(yaml_path)
                
        except Exception as e:
            print(f"❌ Klasör okuma hatası: {str(e)}")
    
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
