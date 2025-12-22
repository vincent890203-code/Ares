import pandas as pd
from Ares import setup_driver, BioCleaner, FeatureTransformer, ML_Brain
# 注意：這裡假設你 extraction.py 裡有一個 parse_table 函式，如果沒有需自行實作
from Ares.spider.extraction import get_text 

def mission_start():
    print("[Mission Start] Ares System Online.")

    # ==========================================
    # Step 1: 蒐集 (Hunt) - Spider 
    # ==========================================
    print("\n--- Phase 1: Spider Corps ---")
    driver = setup_driver()
    
    # 這裡填入你要爬的真實網址
    target_url = "https://example.com/drug-data" 
    print(f"Targeting: {target_url}")
    
    try:
        driver.get(target_url)
        
        # 這裡模擬抓取過程 (需根據實際網頁結構修改 extraction)
        # 假設我們抓到了頁面原始碼，並解析成 DataFrame
        # raw_data = extraction.parse_table(driver.driver.page_source)
        
        # 為了讓程式現在能跑，我這裡還是先模擬回傳資料
        # 等你實際寫好針對特定網站的 extraction 規則後，把下面這行換掉
        raw_data = pd.DataFrame([
            {"Drug": "Aspirin", "MW": 180.16, "Toxicity": 0},
            {"Drug": "Tylenol", "MW": 151.16, "Toxicity": 1},
            {"Drug": "Unknown", "MW": None,   "Toxicity": 0}
        ])
        print(f"Data acquired: {len(raw_data)} rows.")

    finally:
        driver.quit() # 記得關閉瀏覽器

    # ==========================================
    # Step 2: 提煉 (Refine) - Refinery Corps
    # ==========================================
    print("\n--- Phase 2: Refinery Corps ---")
    
    # 實例化清洗器 (這是新版 OOP 的寫法)
    cleaner = BioCleaner()
    transformer = FeatureTransformer()

    # 清洗
    df = cleaner.clean_column_names(raw_data)
    df = cleaner.drop_missing(df)
    
    # 轉換 (準備 X, y)
    # 假設目標欄位是 'toxicity'，其餘是特徵
    target_col = 'toxicity'
    X, y = transformer.split_X_y(df.drop(columns=['drug']), target_col=target_col)
    
    # 標準化 (對 SVM/KNN 很重要)
    X_scaled = transformer.scale_features(X)

    # ==========================================
    # Step 3: 思考 (Think) - Brain Corps
    # ==========================================
    print("\n--- Phase 3: Brain Corps ---")
    
    brain = ML_Brain()
    
    # 使用我們剛寫好的「智慧決策」接口
    # 這裡為了演示，train 和 test 用同一份數據
    best_model = brain.solve_mission(
        X_train=X_scaled, y_train=y, 
        X_test=X_scaled, y_test=y, 
        task_type='classification', 
        label_map={0: 'Safe', 1: 'Toxic'},
        threshold=0.85 # 設定滿意門檻
    )
    
    print("\n[Mission Complete] Ares has evolved.")

if __name__ == "__main__":
    mission_start()