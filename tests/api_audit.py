import sys
import os
import inspect
import importlib

# 確保能讀取到 Ares 套件
sys.path.append(os.getcwd())

def audit_function(module_name, func_name, func_obj):
    """偵訊函式的參數結構"""
    try:
        sig = inspect.signature(func_obj)
        params = []
        for name, param in sig.parameters.items():
            # 標註是否有預設值
            default = f"={param.default}" if param.default is not inspect.Parameter.empty else ""
            params.append(f"{name}{default}")
        
        return f"   ⚡ {func_name}({', '.join(params)})"
    except Exception as e:
        return f"   ❌ 無法分析 {func_name}: {e}"

def audit_class(module_name, class_name, class_obj):
    """偵訊類別的方法"""
    results = [f"   🏗️  class {class_name}"]
    try:
        # 獲取所有公開方法
        methods = inspect.getmembers(class_obj, predicate=inspect.isfunction)
        for m_name, m_obj in methods:
            if not m_name.startswith("__"):
                results.append(f"      └── {audit_function(module_name, m_name, m_obj)}")
        return "\n".join(results)
    except Exception as e:
        return f"   ❌ 無ability分析類別 {class_name}: {e}"

def run_audit():
    print("🛡️  ARES API 接口自動偵察系統")
    print("=" * 60)

    # 定義要掃描的重點目標 (根據 Evolution Log 與盤點圖)
    targets = {
        "Spider": ["Ares.spider.core", "Ares.spider.actions", "Ares.spider.extraction"],
        "Refinery": ["Ares.refinery.cleaner", "Ares.refinery.transformer"],
        "Brain": ["Ares.brain.cortex", "Ares.brain.registry"]
    }

    for sector, modules in targets.items():
        print(f"\n📡 [偵查部門: {sector}]")
        for mod_path in modules:
            try:
                mod = importlib.import_module(mod_path)
                print(f" 📦 {mod_path}")
                
                # 遍歷模組內所有成員
                for name, obj in inspect.getmembers(mod):
                    if name.startswith("__"): continue
                    
                    # 判斷是否為該模組內定義的成員 (排除 import)
                    if hasattr(obj, '__module__') and obj.__module__ == mod_path:
                        if inspect.isfunction(obj):
                            print(audit_function(mod_path, name, obj))
                        elif inspect.isclass(obj):
                            print(audit_class(mod_path, name, obj))
                            
            except Exception as e:
                print(f" ❌ 無法載入模組 {mod_path}: {e}")

    print("\n" + "=" * 60)
    print("✅ 偵察完成。請將上方結果截圖或複製給我。")

if __name__ == "__main__":
    run_audit()