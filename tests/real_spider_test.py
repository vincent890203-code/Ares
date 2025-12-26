import sys
import os
import time
import inspect
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 路徑設定
sys.path.append(os.getcwd())

# 引入軍火庫
from Ares.spider.core import setup_driver
# 引入我們一直「猜錯」的動作庫
from Ares.spider.actions import safe_type, safe_click
# 引入解析庫
from Ares.spider.extraction import get_text

def inspect_and_call(func, func_name, *args):
    """
    這是一個「萬能轉接頭」。
    它會檢查函式需要幾個參數，並嘗試自動適配。
    """
    sig = inspect.signature(func)
    params = list(sig.parameters.keys())
    print(f"   🔍 [偵錯] {func_name} 的真實定義是: {params}")
    
    try:
        # 嘗試直接呼叫 (假設我們猜對了)
        return func(*args)
    except TypeError as e:
        print(f"      ⚠️ 直接呼叫失敗: {e}")
        print("      🔄 嘗試自動參數適配 (Auto-Adapt)...")
        
        # 針對常見的 (driver, by, value) vs (driver, (by, value)) 差異進行修正
        # 情況 A: 我們傳了 4 個 (driver, by, val, text)，但它只要 3 個 (driver, locator, text)
        if len(args) == 4 and len(params) == 3:
            # 嘗試把中間兩個合併成 Tuple
            new_args = (args[0], (args[1], args[2]), args[3])
            return func(*new_args)
            
        # 情況 B: 我們傳了 3 個 (driver, locator, text)，但它要 4 個 (driver, by, val, text)
        elif len(args) == 3 and len(params) == 4:
            # 嘗試把中間那個 Tuple 拆開
            driver, locator, text = args
            new_args = (driver, locator[0], locator[1], text)
            return func(*new_args)
            
        # 情況 C (針對 get_text/safe_click): 參數數量不含 text
        elif len(args) == 3 and len(params) == 2: # 傳了 (driver, by, val) 但只要 (driver, locator)
             new_args = (args[0], (args[1], args[2]))
             return func(*new_args)
             
        raise e # 如果都救不回來，再報錯

def run_real_spider_mission():
    print("🔥 [ARES SPIDER] 啟動實戰偵錯任務...")
    print("========================================")
    
    # 1. 啟動瀏覽器 (開啟 headless=False 讓您親眼看到它在動)
    driver = setup_driver(headless=False, off_screen=False, load_images=True)
    
    target_drug = "Aspirin"
    
    try:
        # --- 步驟 1: 前往 PubChem ---
        print("\n1️⃣ 前往戰場 (PubChem)...")
        driver.get("https://pubchem.ncbi.nlm.nih.gov/")
        time.sleep(3) # 等待載入
        
        # --- 步驟 2: 輸入關鍵字 ---
        print(f"\n2️⃣ 執行動作: 輸入 '{target_drug}'...")
        # 這裡我們傳入最詳細的參數 (4個)，交給 inspect_and_call 去適配
        inspect_and_call(
            safe_type, "safe_type", 
            driver, By.TAG_NAME, "input", target_drug + Keys.RETURN
        )
        
        # --- 步驟 3: 點擊結果 ---
        print("\n3️⃣ 執行動作: 點擊搜尋結果...")
        time.sleep(2)
        # 這裡我們傳入拆開的參數 (3個)
        inspect_and_call(
            safe_click, "safe_click",
            driver, By.CSS_SELECTOR, ".result-container a"
        )
        
        # --- 步驟 4: 抓取數據 ---
        print("\n4️⃣ 執行解析: 抓取化學性質...")
        time.sleep(4) # 確保頁面跳轉完成
        
        # 定義 XPATH
        mw_xpath = "//div[contains(text(), 'Molecular Weight')]/following-sibling::div"
        logp_xpath = "//div[contains(text(), 'XLogP3')]/following-sibling::div"
        
        # 嘗試抓取
        print("   -> 正在抓取 Molecular Weight...")
        mw = inspect_and_call(get_text, "get_text", driver, By.XPATH, mw_xpath)
        
        print("   -> 正在抓取 XLogP...")
        logp = inspect_and_call(get_text, "get_text", driver, By.XPATH, logp_xpath)
        
        print("\n" + "="*40)
        print(f"✅ 任務成功！Ares 爬蟲運作正常")
        print(f"💊 藥物名稱: {target_drug}")
        print(f"⚖️ 分子量 (MW): {mw}")
        print(f"💧 親脂性 (LogP): {logp}")
        print("="*40)
        
        if mw and logp:
            print("\n🎉 證明：您的 Spider 模組功能是正常的，可以串接 Refinery 了。")
        else:
            print("\n⚠️ 警告：動作成功但數據為空，請檢查 XPATH 是否過期。")

    except Exception as e:
        print(f"\n❌ 任務崩潰: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\n🛑 關閉瀏覽器...")
        driver.quit()

if __name__ == "__main__":
    run_real_spider_mission()