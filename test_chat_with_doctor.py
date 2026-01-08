"""
TC_003_chat_with_doctor.yaml - Doktorla sohbet testi
"""
import sys
import os

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.driver_helper import get_browser, get_page, close_browser
from utils.yaml_helper import YamlScenarioLoader
from utils.yaml_method_executor import YamlMethodExecutor
import time

print("\n" + "="*70)
print("🎯 TC_003_chat_with_doctor.yaml TESİ BAŞLADI")
print("="*70 + "\n")

try:
    # 1. YAML dosyasını yükle
    print("1️⃣ YAML dosyası yükleniyor...")
    scenario_file = "scenarios/TC_003_chat_with_doctor.yaml"
    loader = YamlScenarioLoader(scenario_file)
    
    # 2. Browser'ı başlat
    print("\n2️⃣ Browser başlatılıyor...")
    browser = get_browser()
    print("   ✓ Browser başlatıldı")
    
    # 3. Page oluştur
    print("\n3️⃣ Page oluşturuluyor...")
    page = get_page(browser)
    print("   ✓ Page oluşturuldu")
    
    # 4. Executor'u başlat
    print("\n4️⃣ YAML Method Executor başlatılıyor...")
    executor = YamlMethodExecutor(page, loader)
    print("   ✓ Executor başlatıldı")
    
    # 5. Chat senaryolarını al
    print("\n5️⃣ Chat senaryoları alınıyor...")
    chat_scenarios = loader.get_chat_scenarios()
    print(f"   ✓ {len(chat_scenarios)} chat senaryosu bulundu:")
    for scenario in chat_scenarios:
        print(f"     - {scenario['name']}: {scenario['description']}")
    
    # 6. Senaryoları çalıştır
    print("\n6️⃣ Senaryolar çalıştırılıyor...\n")
    
    results = []
    for scenario in chat_scenarios:
        scenario_name = scenario['name']
        print("\n" + "*"*70)
        print(f"📋 Senaryo: {scenario_name}")
        print(f"   Açıklama: {scenario['description']}")
        print("*"*70)
        
        try:
            result = executor.execute_scenario(scenario_name)
            results.append({
                'name': scenario_name,
                'success': result.get('success'),
                'message': result.get('message')
            })
            
            if result.get('success'):
                print(f"\n   ✅ BAŞARILI: {result.get('message')}")
            else:
                print(f"\n   ❌ BAŞARISIZ: {result.get('message')}")
            
            # Senaryo sonrası bekle
            wait_time = scenario.get('wait_time', 5)
            print(f"\n   ⏳ {wait_time} saniye bekleniyor...")
            time.sleep(wait_time)
            
        except Exception as e:
            print(f"\n   ❌ HATA: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append({
                'name': scenario_name,
                'success': False,
                'message': str(e)
            })
    
    # 7. Sonuçları özet
    print("\n" + "="*70)
    print("📊 TEST SONUÇLARI")
    print("="*70)
    
    successful = len([r for r in results if r['success']])
    total = len(results)
    
    for result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {result['name']}: {result['message']}")
    
    print(f"\nToplam: {successful}/{total} test başarılı")
    
    if successful == total:
        print("\n🎉 TÜM TESTLER BAŞARILI!")
    else:
        print(f"\n⚠️  {total - successful} test başarısız!")
    
    print("\n" + "="*70)
    
except Exception as e:
    print(f"\n❌ GENEL HATA: {str(e)}")
    import traceback
    traceback.print_exc()

finally:
    # 8. Browser'ı kapat
    print("\n7️⃣ Browser kapatılıyor...")
    try:
        close_browser(browser)
        print("   ✓ Browser kapatıldı")
    except:
        pass
    
    print("\n" + "="*70)
    print("✅ TEST SONA ERDI")
    print("="*70 + "\n")
