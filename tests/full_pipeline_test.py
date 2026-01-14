import sys
import os
import time
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. 環境初始化
is_ci = os.environ.get('GITHUB_ACTIONS') == 'true'
sys.path.append(os.getcwd())

# 2. 引入 Ares 核心架構
from Ares.spider.core import setup_driver
from Ares.spider.actions import safe_type, safe_click, nuclear_scroll
from Ares.spider.extraction import get_text
from Ares.refinery.cleaner import BioCleaner
from Ares.refinery.transformer import FeatureTransformer
from Ares.brain.cortex import ML_Brain
import warnings
from sklearn.exceptions import ConvergenceWarning

# 忽略不必要的 sklearn 內部警告
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

def test_ares_full_pipeline():
    print(f"🚀 [ARES] 啟動全端整合演習 (模式: {'CI' if is_ci else '本地'})")
    print("=" * 60)

    # --- PHASE 1: SPIDER (僅抓取分子量 MW) ---
    print("\n🕷️ [Phase 1] Spider 偵察任務開始...")
    driver = setup_driver(headless=is_ci, off_screen=True) 
    
    scraped_data = []
    # 增加更多樣本以確保模型有足夠數據進行訓練與驗證
    targets = ["Aspirin", "Ibuprofen", "Caffeine", "Nicotine", "Dopamine", "Morphine", "Atropine", "Penicillin", "Quinine", "Cocaine"]
    
    try:
        for drug in targets:
            print(f"\n🔍 正在搜尋目標: {drug}")
            driver.get("https://pubchem.ncbi.nlm.nih.gov/")
            
            # A. 搜尋動作
            safe_type(driver, By.TAG_NAME, "input", drug + Keys.RETURN)
            
            # B. 精準點擊
            highlight_selector = "a[data-ga-action='content-link'] span.pc-highlight"
            time.sleep(2) 
            try:
                safe_click(driver, By.CSS_SELECTOR, highlight_selector)
            except:
                safe_click(driver, By.CSS_SELECTOR, "a[data-ga-action='content-link']")
    
            # C. 驗證跳轉
            try:
                WebDriverWait(driver, 15).until(lambda d: "/compound/" in d.current_url)
                print(f"   ✅ 成功進入詳細頁: {driver.current_url}")
            except:
                print(f"   ❌ 跳轉失敗，跳過此項")
                continue

            # D. 核彈捲動
            nuclear_scroll(driver, times=2, wait=1.5)
            
            # E. 數據擷取 (暫時只抓 MW)
            mw = get_text(driver, By.XPATH, "//div[contains(text(), 'Molecular Weight')]/following-sibling::div")
            
            if mw != "Not Found":
                scraped_data.append({"drug": drug, "mw": mw})
                print(f"   ✨ 數據獵取成功: MW={mw}")
            
    finally:
        driver.quit()

    # --- PHASE 2: REFINERY (提煉單一特徵) ---
    print("\n🧪 [Phase 2] Refinery 提煉任務開始...")
    if not scraped_data:
        print("❌ 錯誤：未獲取數據，終止。")
        return

    df_raw = pd.DataFrame(scraped_data)
    cleaner = BioCleaner()
    df_clean = cleaner.clean_column_names(df_raw) #
    
    # 數值提煉：正規表達式提取數字
    df_clean['mw'] = pd.to_numeric(df_clean['mw'].str.extract(r'(\d+\.?\d*)')[0], errors='coerce')
    df_clean = cleaner.drop_missing(df_clean)
    
    # 手動建立標籤 (Labeling)
    # 規則：MW < 200 視為 "類藥 (1)"
    df_clean['is_druglike'] = (df_clean['mw'] < 200).astype(int)
    
    transformer = FeatureTransformer()
    # 將 mw 轉為矩陣格式進行轉換
    X, y = transformer.split_X_y(df_clean[['mw', 'is_druglike']], target_col='is_druglike')
    X_scaled = transformer.scale_features(X) 
    print(f"   ✅ 提煉完成。樣本數: {len(df_clean)}")

    # --- PHASE 3: BRAIN (建模修正版) ---
    print("\n🧠 [Phase 3] Brain 建模任務開始...")
    brain = ML_Brain()
    try:
        # 修正：根據 image_883f5b.png，必須加入 label_map 參數
        # 定義 0 與 1 對應的語義
        custom_label_map = {0: "Safe (低活性)", 1: "Active (高活性)"}
        
        # 呼叫 solve_mission
        brain.solve_mission(
            X_train=X_scaled, y_train=y, 
            X_test=X_scaled, y_test=y, 
            task_type='classification',
            label_map=custom_label_map # 補上缺失的關鍵參數
        )
        print("\n" + "=" * 60)
        print("🎉 [SUCCESS] Ares 全端管線驗證完成 (單特徵穩定版)！")
    except Exception as e:
        print(f"❌ 建模失敗: {e}")

if __name__ == "__main__":
    test_ares_full_pipeline()