import os
import shutil
import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

# 引用您的核心模組
from Ares.brain.cortex import ML_Brain

def run_system_check():
    print("========================================")
    print("🤖 Ares System Integration Test (v2.0)")
    print("========================================")

    # 1. 環境清理 (確保測試是乾淨的)
    memory_path = "./brain_memory_test/"
    if os.path.exists(memory_path):
        shutil.rmtree(memory_path)
    os.makedirs(memory_path)
    print(f"1. [Environment] Created clean test memory: {memory_path}")

    # 2. 準備數據
    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("2. [Data] Breast Cancer dataset loaded.")

    # 3. 初始化大腦
    # 注意：我們傳入測試用的路徑，避免汙染您原本的 brain_memory
    brain = ML_Brain(memory_path=memory_path)
    print("3. [System] Brain & Registry initialized.")

    # 4. 第一輪測試：強制訓練 (Training Phase)
    print("\n--- Phase A: First Run (Training) ---")
    model_v1 = brain.solve_mission(
        X_train, y_train, X_test, y_test,
        task_type='classification',
        label_map={0: 'Malignant', 1: 'Benign'},
        threshold=0.85
    )
    
    # 驗證 A：是否有產生檔案？
    saved_files = os.listdir(memory_path)
    if len(saved_files) > 0:
        print(f"✅ [Check] File saved successfully: {saved_files[0]}")
    else:
        print("❌ [Check] No file saved! (Check base.py save logic)")
        return

    # 5. 第二輪測試：強制回憶 (Recall Phase)
    print("\n--- Phase B: Second Run (Recall) ---")
    # 我們重新初始化一個 brain，模擬「隔天重新開機」的情境
    brain_new = ML_Brain(memory_path=memory_path)
    
    model_v2 = brain_new.solve_mission(
        X_train, y_train, X_test, y_test,
        task_type='classification',
        label_map={0: 'Malignant', 1: 'Benign'},
        threshold=0.85
    )

    # 驗證 B：是否真的是讀取舊檔案？
    # 如果是回憶成功的，控制台應該會印出 "Using existing model"
    # 我們這裡檢查 model_v2 是否能預測
    try:
        sample_pred = model_v2.predict(X_test.iloc[0:5])
        print(f"✅ [Check] Recalled model prediction test: Passed")
        print(f"   Predictions: {sample_pred}")
    except Exception as e:
        print(f"❌ [Check] Recalled model failed to predict: {e}")
        return

    print("\n========================================")
    print("🎉 SYSTEM STATUS: GREEN (Stable)")
    print("   Registry, Cortex, and Base are compatible.")
    print("========================================")

if __name__ == "__main__":
    run_system_check()