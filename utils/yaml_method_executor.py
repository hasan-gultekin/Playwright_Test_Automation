"""
YAML Method Executor - YAML'da belirtilen page metodlarını dinamik olarak çalıştırır (Playwright uyumlu)
"""

import sys
import os
import time
import importlib
import re
from typing import Dict, Any, Optional

# Proje kök dizinini Python path'e ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.yaml_helper import YamlScenarioLoader
from playwright.sync_api import Page
import config


def camel_to_snake(name: str) -> str:
    """CamelCase'i snake_case'e çevir: RegistrationPage -> registration_page"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class YamlMethodExecutor:
    """
    YAML'da belirtilen page class metodlarını dinamik olarak çalıştırır
    
    YAML Yapısı:
    - name: "scenario_name"
      page: "RegistrationPage"        # Page class adı
      method: "execute_successful_registration_flow"  # Çalıştırılacak metod
      params:
        email: "user@test.com"
        password: "Pass123"
    """
    
    def __init__(self, page: Page, scenario_loader: YamlScenarioLoader):
        """
        Executor'ı başlat
        
        Args:
            page: Playwright Page instance
            scenario_loader: YAML Scenario Loader
        """
        self.page = page
        self.scenario_loader = scenario_loader
        self.page_instances = {}  # Page instances cache
    
    def execute_scenario(self, scenario_name: str) -> Dict[str, Any]:
        """
        YAML senaryosunu execute et
        
        Args:
            scenario_name: Senaryo adı
            
        Returns:
            dict: Sonuçlar
        """
        try:
            # Senaryo getir
            try:
                scenario = self.scenario_loader.get_scenario_by_name(scenario_name)
            except ValueError as e:
                return {
                    "success": False,
                    "scenario": scenario_name,
                    "message": str(e)
                }
            
            # Scenario None check
            if scenario is None:
                return {
                    "success": False,
                    "scenario": scenario_name,
                    "message": f"Senaryo bulunamadı: {scenario_name}"
                }
            
            print(f"\n{'='*70}")
            print(f"🧪 Senaryo: {scenario.get('name')}")
            print(f"📝 Açıklama: {scenario.get('description')}")
            print(f"{'='*70}\n")
            
            # Senaryo parametrelerini al
            page_name = scenario.get('page')
            method_name = scenario.get('method')
            params = scenario.get('params', {})
            wait_time = scenario.get('wait_time', 2)
            
            if not page_name or not method_name:
                return {
                    "success": False,
                    "scenario": scenario_name,
                    "message": "YAML'da 'page' ve 'method' belirtilmesi zorunludur"
                }
            
            print(f"📌 METOD ÇALIŞTIRILIYYOR:")
            print(f"   Page: {page_name}")
            print(f"   Method: {method_name}\n")
            
            # Parametreleri işle (dinamik değerler)
            processed_params = self._process_params(params)
            print(f"📦 Parametreler:")
            for key, value in processed_params.items():
                if "password" not in key.lower():
                    print(f"   {key}: {value}")
                else:
                    print(f"   {key}: {'*' * 8}")
            print()
            
            # Page instance'ı al
            page_instance = self._get_page_instance(page_name)
            
            if page_instance is None:
                return {
                    "success": False,
                    "scenario": scenario_name,
                    "message": f"Page sınıfı bulunamadı: {page_name}"
                }
            
            # Metod var mı kontrol et
            if not hasattr(page_instance, method_name):
                # Debug: Tüm metodları listele
                available_methods = [m for m in dir(page_instance) if not m.startswith('_')]
                print(f"❌ Metod '{method_name}' bulunamadı!")
                print(f"   Mevcut metodlar: {', '.join(available_methods)}")
                return {
                    "success": False,
                    "scenario": scenario_name,
                    "message": f"Metod bulunamadı: {page_name}.{method_name}(). Mevcut: {', '.join(available_methods[:5])}"
                }
            
            # Metodu çağır
            method = getattr(page_instance, method_name)
            result = method(**processed_params)
            
            # Bekleme
            print(f"\n⏳ {wait_time} saniye bekleniyor...")
            time.sleep(wait_time)
            
            # Sonuç kontrol et
            if isinstance(result, dict):
                success = result.get('success', False)
            elif isinstance(result, bool):
                success = result
            else:
                success = result is not None
            
            if not success:
                print(f"\n❌ Metod başarısız oldu")
                return {
                    "success": False,
                    "scenario": scenario_name,
                    "message": f"Metod başarısız: {result}",
                    "method_result": result
                }
            
            print(f"\n{'='*70}")
            print(f"✅ SENARYO BAŞARILI: {scenario_name}")
            print(f"{'='*70}\n")
            
            return {
                "success": True,
                "scenario": scenario_name,
                "message": f"Senaryo başarılı: {scenario_name}",
                "page": page_name,
                "method": method_name,
                "method_result": result if isinstance(result, dict) else {"status": "ok"}
            }
            
        except Exception as e:
            error_msg = f"Senaryo execution hatası: {str(e)}"
            print(f"\n❌ {error_msg}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "scenario": scenario_name,
                "message": error_msg,
                "exception": str(e)
            }
    
    def _get_page_instance(self, page_name: str):
        """
        Page instance'ını al (cached)
        
        Args:
            page_name: Page sınıf adı (CamelCase: RegistrationPage)
            
        Returns:
            Page instance veya None
        """
        # Cache'de var mı kontrol et
        if page_name in self.page_instances:
            return self.page_instances[page_name]
        
        try:
            # CamelCase'i snake_case'e çevir
            module_name = camel_to_snake(page_name)
            
            # Page modülünü dinamik olarak import et
            page_module = importlib.import_module(f"pages.{module_name}")
            
            # Sınıfı bul (CamelCase ile)
            page_class = getattr(page_module, page_name)
            
            # Instance oluştur (Page parametresi ile)
            instance = page_class(self.page)
            
            # Cache'e kaydet
            self.page_instances[page_name] = instance
            
            print(f"✓ Page instance oluşturuldu: {page_name} (pages.{module_name})\n")
            
            return instance
            
        except ImportError as e:
            print(f"❌ Page modülü bulunamadı: {page_name}")
            print(f"   Aranılan: pages.{camel_to_snake(page_name)}")
            print(f"   Hata: {str(e)}")
            return None
        except AttributeError as e:
            print(f"❌ Page sınıfı bulunamadı: {page_name}")
            print(f"   Hata: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Page instance oluşturma hatası: {str(e)}")
            return None
    
    def _process_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parametreleri işle (dinamik değerler, config referansları, sayfa sabitlerini)
        
        Args:
            params: Parametreler
            
        Returns:
            İşlenmiş parametreler
        """
        # None check
        if params is None:
            return {}
        
        processed = {}
        
        for key, value in params.items():
            if isinstance(value, str):
                # Dinamik parametreleri işle
                value = self.scenario_loader.process_dynamic_values(value)
                
                # Config referanslarını işle ({{config.BASE_URL}} gibi)
                if isinstance(value, str) and value.startswith("{{config.") and value.endswith("}}"):
                    config_key = value[9:-2]  # "BASE_URL" kısmını al
                    value = getattr(config, config_key, value)
                
                # Sayfa sabitleri referanslarını işle ({{ChatPage.MESSAGE_TO_DOCTOR1}} gibi)
                if isinstance(value, str) and value.startswith("{{") and "." in value and value.endswith("}}"):
                    inner = value[2:-2]  # "ChatPage.MESSAGE_TO_DOCTOR1"
                    if "." in inner:
                        page_name, const_name = inner.split(".", 1)
                        try:
                            # Sayfa modülünü dinamik olarak yükle
                            page_module = __import__(f"pages.{camel_to_snake(page_name)}", fromlist=[page_name])
                            # Sayfa sınıfını al
                            page_class = getattr(page_module, page_name, None)
                            if page_class:
                                # Sınıf sabitini al
                                resolved_value = getattr(page_class, const_name, None)
                                if resolved_value is not None:
                                    value = resolved_value
                                else:
                                    print(f"⚠️ Sabit bulunamadı: {page_name}.{const_name}")
                            else:
                                print(f"⚠️ Sayfa sınıfı bulunamadı: {page_name}")
                        except (ImportError, AttributeError) as e:
                            print(f"⚠️ Referans çözülemedi: {{{{ {page_name}.{const_name} }}}} ({str(e)})")
            
            processed[key] = value
        
        return processed
    
    def get_all_scenarios(self) -> Dict[str, list]:
        """Tüm senaryoları kategoriye göre döndür"""
        return {
            "registration": self.scenario_loader.get_registration_scenarios(),
            "login": self.scenario_loader.get_login_scenarios()
        }


def execute_yaml_scenario(page: Page, scenario_name: str, yaml_file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Helper function - YAML senaryosu execute et
    
    Args:
        page: Playwright Page instance
        scenario_name: Senaryo adı
        yaml_file_path: YAML dosyası yolu (optional)
        
    Returns:
        dict: Sonuçlar
    """
    # None check
    if page is None:
        return {
            "success": False,
            "scenario": scenario_name,
            "message": "Page None - browser başlatılmamış"
        }
    
    if scenario_name is None or scenario_name == "":
        return {
            "success": False,
            "message": "Senaryo adı boş veya None"
        }
    
    try:
        # Loader'ı yükle
        print(f"\n🔧 YamlScenarioLoader oluşturuluyor...")
        loader = YamlScenarioLoader(yaml_file_path)
        print(f"✓ Loader oluşturuldu")
        
        # Loader'ın scenarios'ı kontrolü
        print(f"📊 Scenarios Type: {type(loader.scenarios)}")
        print(f"📊 Scenarios Length: {len(loader.scenarios) if loader.scenarios else 0}")
        
        if loader.scenarios is None:
            return {
                "success": False,
                "scenario": scenario_name,
                "message": "YAML scenarios None - loader başarısız"
            }
        
        if not loader.scenarios:
            return {
                "success": False,
                "scenario": scenario_name,
                "message": "YAML senaryoları boş - lütfen YAML dosyasını kontrol edin"
            }
        
        # Executor oluştur
        print(f"🔧 YamlMethodExecutor oluşturuluyor...")
        executor = YamlMethodExecutor(page, loader)
        print(f"✓ Executor oluşturuldu")
        
        # Senaryo çalıştır
        return executor.execute_scenario(scenario_name)
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Execute hatası: {error_msg}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "scenario": scenario_name,
            "message": f"Execute hatası: {error_msg}",
            "exception": error_msg
        }


if __name__ == "__main__":
    # Test amaçlı kullanım
    print("✓ YAML Method Executor module yüklendi")
    print("✓ YAML'da belirtilen page metodlarını dinamik olarak çalıştırır")
    print("\nKullanım:")
    print("  executor = YamlMethodExecutor(driver, scenario_loader)")
    print("  result = executor.execute_scenario('successful_login')")
