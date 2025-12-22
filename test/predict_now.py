import joblib
import pandas as pd
import numpy as np

# 假設這是明天，來了一批新藥物 (New Data)
new_drugs = [
    [0.1, 0.9], # 藥物 A 的特徵 (假設已標準化)
    [0.8, 0.1], # 藥物 B 的特徵
]

# 1. 載入記憶 (Load Model)
# 注意：請把下面的檔名換成你 brain_memory 資料夾裡實際產生的那個檔名
model_path = "./brain_memory/best_SVM_20251222_1637.pkl" 

print(f"🧠 正在喚醒記憶: {model_path} ...")
loaded_model = joblib.load(model_path)

# 2. 直接預測 (Inference)
print("⚡ 開始預測新藥物...")

# 因為我們存的是整個 Weapon 物件，所以可以直接用 predict
# 注意：這裡傳入 DataFrame 或是 Numpy 都可以，因為我們剛剛升級了 _validate_input
predictions = loaded_model.predict(pd.DataFrame(new_drugs))

print("\n--- 預測結果 ---")
for i, result in enumerate(predictions.predictions):
    label = predictions.prediction_labels[i]
    print(f"藥物 {i+1}: 預測為 [{label}]")