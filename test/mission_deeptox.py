import pandas as pd
import numpy as np

# 🌟 這一行就是模組化的威力！直接從 Ares 叫出三大軍團
from Ares import setup_driver, BioCleaner, FeatureTransformer, ML_Brain

def run_mission():
    print("==========================================")
    print("🚀 Ares Mission: DeepTox Protocol Started")
    print("==========================================\n")

    # ==========================================
    # 🕵️‍♂️ Phase 1: 情報搜集 (Hunt)
    # ==========================================
    print("--- [Phase 1] Spider Corps: Hunting Data ---")
    
    # 備註：在真實情況下，這裡會呼叫 driver 去爬網頁
    # driver = setup_driver()
    # driver.get("https://some-bio-database.com")
    # raw_data = ... (爬蟲邏輯)
    
    print("   (模擬：正在從目標網站抓取藥物分子資料...)")
    
    # 這裡我們模擬爬蟲抓回來的一些「髒」數據
    # 包含：多餘空白、缺失值 (None)、重複資料
    mock_raw_data = [
        {"Drug Name": " Aspirin ", "MolWt": 180.16, "LogP": 1.19, "Toxicity": 0},
        {"Drug Name": "Tylenol",   "MolWt": 151.16, "LogP": 0.46, "Toxicity": 1},
        {"Drug Name": " Advil ",   "MolWt": 206.29, "LogP": 3.50, "Toxicity": 1},
        {"Drug Name": "Caffeine",  "MolWt": 194.19, "LogP": -0.07, "Toxicity": 0},
        {"Drug Name": "UnknownX",  "MolWt": None,   "LogP": 1.20,  "Toxicity": 1}, # 缺失值
        {"Drug Name": "Tylenol",   "MolWt": 151.16, "LogP": 0.46, "Toxicity": 1}, # 重複資料
        {"Drug Name": "Water",     "MolWt": 18.01,  "LogP": -1.38, "Toxicity": 0},
        {"Drug Name": "Cyanide",   "MolWt": 26.02,  "LogP": -0.25, "Toxicity": 1},
    ]
    
    # 先轉成 DataFrame 方便看
    df_raw = FeatureTransformer.to_dataframe(mock_raw_data)
    print(f"   -> 抓取完成，原始資料共 {len(df_raw)} 筆。")

    # ==========================================
    # 🏭 Phase 2: 資料提煉 (Refine)
    # ==========================================
    print("\n--- [Phase 2] Refinery Corps: Processing Data ---")
    
    cleaner = BioCleaner()
    transformer = FeatureTransformer()

    # 1. 衛生清潔 (Cleaning)
    print("   -> 正在標準化欄位名稱...")
    df = cleaner.clean_column_names(df_raw) # "Drug Name" -> "drug_name"
    
    print("   -> 正在移除重複與缺失值...")
    df = cleaner.remove_duplicates(df)
    df = cleaner.drop_missing(df)
    
    print(f"   -> 清洗完畢，剩餘有效資料: {len(df)} 筆。")
    print(df) # 印出來看看

    # 2. 轉換成數學矩陣 (Transformation)
    print("\n   -> 正在進行特徵矩陣轉換 (X, y)...")
    
    # 設定我們不想放入訓練的欄位 (例如藥名)
    df_features = df.drop(columns=['drug_name'])
    
    # 自動切分 X (特徵) 與 y (目標)
    X, y = transformer.split_X_y(df_features, target_col='toxicity')
    
    # 數值標準化 (這對 SVM 和 KNN 很重要！)
    X_scaled = transformer.scale_features(X, method='minmax')
    
    print(f"   -> 轉換完成。特徵矩陣 X shape: {X_scaled.shape}")

    # ==========================================
    # 🧠 Phase 3: 大腦決策 (Think)
    # ==========================================
    print("\n--- [Phase 3] The Brain: AutoML Training ---")
    
    brain = ML_Brain()
    
    # 告訴大腦：這是一個「分類任務」，標籤 0=安全, 1=有毒
    # 大腦會自動派出 LogisticRegression, SVM, KNN 上場亂鬥
    best_model = brain.think_and_train(
        X_train=X_scaled, 
        y_train=y, 
        X_test=X_scaled, # 演示用，實際應該要切分 train/test
        y_test=y,
        task_type='classification',
        label_map={0: 'Safe (無毒)', 1: 'Toxic (有毒)'}
    )

    if best_model:
        print("\n==========================================")
        print(f"🎉 任務成功！最強模型 [{best_model.model_name}] 已存入記憶庫。")
        print("==========================================")
        
        # 讓冠軍模型畫圖給你看
        # best_model.evaluate(X_scaled, y) # 如果你在 Jupyter 裡可以打開這行
    else:
        print("⚠️ 任務失敗，大腦未能訓練出有效模型。")

if __name__ == "__main__":
    run_mission()   