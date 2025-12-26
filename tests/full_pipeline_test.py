import sys
import os
import time
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 路徑設定
sys.path.append(os.getcwd())

# ==========================================================
# 1. 調度 Ares 軍火庫 (Arsenal Import)
# 根據您的盤點結果，精準引入現有模組
# ==========================================================

# [Spider]
from Ares.spider.core import setup_driver, retry
from Ares.spider.actions import safe_click, safe_type, nuclear_scroll
from Ares.spider.extraction import get_text

# [Refinery]
from Ares.refinery.cleaner import BioCleaner
from Ares.refinery.transformer import FeatureTransformer

# [Brain]
from Ares.brain.cortex import ML_Brain

# ==========================================================
# 2. 定義任務特化機器人 (Mission Specific Bot)
# 這是為了 PubChem 任務設計的策略，不汙染 Ares 核心
# ==========================================================

class PubChemMissionBot:
    def __init__(self, driver):
        self.driver = driver

    @retry(times=3)
    def scout_compound(self, compound_name):
        print(f"   -> 🕵️ [Spider Action] 鎖定目標: {compound_name}")
        
        # 1. 前往戰場
        self.driver.get("https://pubchem.ncbi.nlm.nih.gov/")
        
        # 2. 執行戰術動作
        # 修正：將 (By.TAG_NAME, "input") 拆開成兩個參數 By.TAG_NAME 和 "input"
        safe_type(self.driver, By.TAG_NAME, "input", compound_name + Keys.RETURN)
        
        # 3. 點擊結果
        # 修正：同樣拆開 Tuple
        safe_click(self.driver, By.CSS_SELECTOR, ".result-container a")
        
        # 4. 等待並解析
        time.sleep(3) 
        
        data = {'Name': compound_name}
        try:
            mw_xpath = "//div[contains(text(), 'Molecular Weight')]/following-sibling::div"
            logp_xpath = "//div[contains(text(), 'XLogP3')]/following-sibling::div"
            
            # 修正：get_text 也需要拆開 Tuple
            data['molecular_weight'] = get_text(self.driver, By.XPATH, mw_xpath)
            data['xlogp'] = get_text(self.driver, By.XPATH, logp_xpath)
            
            print(f"      ✅ 獲取情報: {data}")
            return data
        except Exception as e:
            print(f"      ⚠️ 情報獲取失敗: {e}")
            return None

# ==========================================================
# 3. 全端管線整合測試 (End-to-End Pipeline)
# ==========================================================

def run_full_pipeline_simulation():
    print("\n🚀 [ARES SYSTEM] FULL PIPELINE TEST INITIATED")
    print("==============================================")

    # --- PHASE 1: SPIDER (情報搜集) ---
    print("\n🕷️ [Phase 1] 啟動 Spider 部門...")
    
    # 測試樣本 (刻意包含差異大的藥物以利分類)
    targets = ["Aspirin", "Ibuprofen", "Caffeine", "Morphine", "Dopamine", "Penicillin"]
    
    # 啟動核心驅動 (Headless 模式模擬伺服器運行)
    driver = setup_driver(headless=True, off_screen=True, load_images=False)
    bot = PubChemMissionBot(driver)
    
    raw_data = []
    try:
        for target in targets:
            result = bot.scout_compound(target)
            if result:
                raw_data.append(result)
            time.sleep(1)
    finally:
        driver.quit()
        print("   -> 瀏覽器已回收。")

    if not raw_data:
        print("❌ 任務失敗：無數據。")
        return

    # --- PHASE 2: REFINERY (數據提煉) ---
    print("\n🧪 [Phase 2] 啟動 Refinery 部門...")
    
    # 轉為 DataFrame
    df = pd.DataFrame(raw_data)
    print("   -> 原始數據:\n", df.head(3))
    
    # 2.1 呼叫 BioCleaner (清洗)
    cleaner = BioCleaner()
    # 根據您的盤點，BioCleaner 有 clean_column_names 和 drop_missing
    df = cleaner.clean_column_names(df) 
    
    # 模擬數據類型轉換 (Refinery 通常也處理這個，這裡手動轉以便示範 transformer)
    df['molecular_weight'] = pd.to_numeric(df['molecular_weight'], errors='coerce')
    df['xlogp'] = pd.to_numeric(df['xlogp'], errors='coerce')
    
    df = cleaner.drop_missing(df)
    print(f"   -> 清洗後數據量: {len(df)}")

    # 2.2 產生合成標籤 (為了讓 Brain 有東西學)
    # 規則：MW < 400 且 LogP < 3 為 "高類藥性 (1)"
    df['target_class'] = ((df['molecular_weight'] < 400) & (df['xlogp'] < 3)).astype(int)

    # 2.3 呼叫 FeatureTransformer (轉換)
    transformer = FeatureTransformer()
    # 假設 split_X_y 幫我們切分特徵與標籤
    # 根據盤點，split_X_y 應該在 transformer 裡
    target_col = 'target_class'
    feature_cols = ['molecular_weight', 'xlogp']
    
    X = df[feature_cols]
    y = df[target_col]
    
    # 使用 FeatureTransformer 進行縮放 (Scale)
    # 這裡演示我們調用了 scale_features 方法
    X_scaled = transformer.scale_features(X)
    print("   -> 特徵已標準化 (Scaled)。準備傳輸至 Cortex。")

    # --- PHASE 3: BRAIN (決策中樞) ---
    print("\n🧠 [Phase 3] 啟動 Brain Cortex (中控室)...")
    
    # 實例化大腦
    brain = ML_Brain()
    
    # 呼叫 solve_mission (這是盤點出的核心方法)
    # 這會自動觸發 AutoML 機制，調用 Weapons 裡的 LogisticRegression/SVM/KNN
    print("   -> 發送任務指令: solve_mission (Classification)")
    
    try:
        # 假設 solve_mission 接受 X, y 和任務類型
        # 它內部會去呼叫 Weapons 資料夾裡的槍
        best_model = brain.solve_mission(X_scaled, y, task_type="classification")
        
        print("\n✅ [ARES SYSTEM] MISSION ACCOMPLISHED")
        print("   -> 全流程驗證成功：Spider -> Refinery -> Brain")
        print("   -> 資料流與模組接口運作正常。")
        
    except Exception as e:
        print(f"❌ Brain 運算發生錯誤 (可能是數據量太少導致 CV 失敗): {e}")
        print("   (建議：增加 targets 列表的藥物數量以滿足 Cross-Validation 需求)")

if __name__ == "__main__":
    run_full_pipeline_simulation()