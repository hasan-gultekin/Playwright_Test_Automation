"""
Specific YAML Test Runner - Belirtilen YAML dosyasındaki senaryoları çalıştırır (Playwright)
"""

import sys
import os
import argparse
import time

# Proje kök dizinini Python path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.driver_helper import get_browser, get_page, close_browser
from utils.yaml_helper import YamlScenarioLoader
from utils.yaml_method_executor import YamlMethodExecutor
import config


def run_yaml_scenarios(yaml_file_path):
    """
    Belirtilen YAML dosyasındaki tüm senaryoları çalıştır
    
    Args:
        yaml_file_path: YAML dosyasının yolu
    """
    
    print("\n" + "="*80)
    print(f"🚀 YAML TEST RUNNER - {os.path.basename(yaml_file_path)}")
    print("="*80 + "\n")
    
    # YAML Yükle
    try:
        loader = YamlScenarioLoader(yaml_file_path)
    except Exception as e:
        print(f"❌ YAML yükleme hatası: {str(e)}")
        return False
    
    # Scenario yoksa çık
    if not loader.scenarios:
        print("❌ YAML'da senaryo bulunamadı!")
        return False
    
    # Tüm senaryoları al
    all_scenarios = loader._get_all_enabled_scenarios()
    if not all_scenarios:
        print("❌ Aktif senaryo bulunamadı!")
        return False
    
    print(f"📊 Toplam Senaryo: {len(all_scenarios)}")
    print(f"📝 Senaryo Kategorileri:\n")
    
    # Kategoriye göre göster
    categories = {}
    for scenario in all_scenarios:
        page = scenario.get('page', 'Unknown')
        if page not in categories:
            categories[page] = []
        categories[page].append(scenario)
    
    for page, scenarios_list in categories.items():
        print(f"  📦 {page} ({len(scenarios_list)} senaryo)")
        for scenario in scenarios_list:
            print(f"     • {scenario.get('name')}")
            print(f"       └─ {scenario.get('description')}")
    
    print()
    
    print("\n" + "="*80 + "\n")
    
    # Browser başlat
    browser = None
    page = None
    passed = 0
    failed = 0
    results = []
    
    try:
        browser = get_browser()
        page = get_page(browser)
        
        # Executor oluştur
        executor = YamlMethodExecutor(page, loader)
        
        # Her senaryo için test çalıştır
        for scenario in all_scenarios:
            scenario_name = scenario['name']
            
            print(f"\n{'▶'*40}")
            print(f"🧪 Senaryo: {scenario_name}")
            print(f"{'▶'*40}\n")
            
            try:
                # Senaryo çalıştır
                result = executor.execute_scenario(scenario_name)
                
                if result['success']:
                    print(f"✅ BAŞARILI: {scenario_name}\n")
                    passed += 1
                else:
                    print(f"❌ BAŞARISIZ: {scenario_name}")
                    print(f"   Hata: {result['message']}\n")
                    failed += 1
                
                results.append({
                    'name': scenario_name,
                    'status': 'PASSED' if result['success'] else 'FAILED',
                    'message': result.get('message', '')
                })
                
            except Exception as e:
                print(f"❌ EXCEPTION: {scenario_name}")
                print(f"   Hata: {str(e)}\n")
                failed += 1
                results.append({
                    'name': scenario_name,
                    'status': 'ERROR',
                    'message': str(e)
                })
        
    finally:
        if page:
            page.close()
        if browser:
            close_browser(browser)
    
    # Özet Yazdır
    print("\n" + "="*80)
    print("📊 TEST ÖZETI")
    print("="*80)
    print(f"✅ Başarılı: {passed}")
    print(f"❌ Başarısız: {failed}")
    print(f"📋 Toplam: {passed + failed}")
    
    if results:
        print("\n" + "-"*80)
        print("Detaylı Sonuçlar:")
        print("-"*80)
        for result in results:
            status_icon = "✅" if result['status'] == 'PASSED' else "❌"
            print(f"\n{status_icon} {result['name']}")
            print(f"   Status: {result['status']}")
            if result['message']:
                print(f"   Mesaj: {result['message']}")
    
    print("\n" + "="*80 + "\n")
    
    return failed == 0


def main():
    parser = argparse.ArgumentParser(
        description='Belirtilen YAML dosyasındaki senaryoları çalıştırır (Playwright)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python run_specific_yaml.py scenarios/TC_002_login_scenarios.yaml
  python run_specific_yaml.py login_scenarios.yaml
  python run_specific_yaml.py /absolute/path/to/scenarios.yaml
        """
    )
    
    parser.add_argument(
        'yaml_file',
        help='Çalıştırılacak YAML dosyasının yolu veya adı'
    )
    
    args = parser.parse_args()
    yaml_file = args.yaml_file
    
    # Dosya var mı kontrol et
    if not os.path.exists(yaml_file):
        # scenarios/ klasöründe ara
        scenarios_dir = os.path.join(os.path.dirname(__file__), "scenarios")
        alt_path = os.path.join(scenarios_dir, yaml_file)
        
        if os.path.exists(alt_path):
            yaml_file = alt_path
        else:
            print(f"❌ Dosya bulunamadı: {yaml_file}")
            print(f"   Arandığı yerler:")
            print(f"   1. {yaml_file}")
            print(f"   2. {alt_path}")
            sys.exit(1)
    
    # Testleri çalıştır
    success = run_yaml_scenarios(yaml_file)
    
    # Exit code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
