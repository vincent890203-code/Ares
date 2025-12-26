import sys
import os
import importlib
import inspect
import pkgutil

# 確保能讀取到專案根目錄
sys.path.append(os.getcwd())

def get_module_members(module_obj, module_name):
    """提取模組內的 Class 與 Function"""
    members = []
    
    try:
        # 取得所有屬性
        for name, obj in inspect.getmembers(module_obj):
            if name.startswith("__"): continue

            # 判斷是否為 Class
            if inspect.isclass(obj):
                # 關鍵過濾：只顯示定義在該模組內的 Class (排除 import 進來的 pandas/sklearn)
                if obj.__module__ == module_name:
                    # 嘗試抓取 method
                    methods = [n for n, v in inspect.getmembers(obj, inspect.isfunction) if not n.startswith("__")]
                    members.append(f"   🏗️  [Class] {name}")
                    if methods:
                        members.append(f"       └── methods: {methods}")

            # 判斷是否為 Function
            elif inspect.isfunction(obj):
                if obj.__module__ == module_name:
                    members.append(f"   ⚡  [Func]  {name}()")
    except Exception as e:
        members.append(f"   ⚠️  (分析錯誤: {e})")
        
    return members

def recursive_scan(base_package="Ares"):
    print(f"🚀 ARES ARSENAL DEEP SCAN: {base_package}")
    print("=" * 60)
    
    # 遍歷目錄
    base_path = os.path.join(os.getcwd(), base_package)
    if not os.path.exists(base_path):
        print(f"❌ 找不到路徑: {base_path}")
        return

    # 使用 os.walk 進行地毯式搜索
    for root, dirs, files in os.walk(base_path):
        # 忽略 __pycache__ 和 .git 等雜訊
        if "__pycache__" in root or ".git" in root:
            continue
            
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                # 1. 計算模組路徑 (例如: Ares\brain\cortex.py -> Ares.brain.cortex)
                rel_path = os.path.relpath(os.path.join(root, file), os.getcwd())
                module_name = rel_path.replace(os.sep, ".").replace(".py", "")
                
                print(f"\n📦 {module_name}")
                
                # 2. 動態載入模組
                try:
                    mod = importlib.import_module(module_name)
                    members = get_module_members(mod, module_name)
                    
                    if members:
                        for m in members:
                            print(m)
                    else:
                        print("   (無主要定義 / 純腳本)")
                        
                except Exception as e:
                    print(f"   ❌ Load Error: {e}")

    print("\n" + "=" * 60)
    print("✅ 掃描完成")

if __name__ == "__main__":
    recursive_scan("Ares")