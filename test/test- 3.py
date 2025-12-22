from Ares.refinery import BioCleaner, FeatureTransformer

# 1. 假設爬蟲抓回來的原始資料 (List of Dicts)
raw_data = [
    {"Drug Name": " Aspirin ", "MW": 180.16, "Toxicity": 0},
    {"Drug Name": "Tylenol", "MW": 151.16, "Toxicity": 1},
    {"Drug Name": "Tylenol", "MW": 151.16, "Toxicity": 1}, # 重複資料
    {"Drug Name": "Unknown", "MW": None, "Toxicity": 0},   # 缺失值
]

# --- 階段一：轉換格式 & 清洗 (Cleaning) ---
# 先轉成 DF
df = FeatureTransformer.to_dataframe(raw_data)

# 開始清洗流程
cleaner = BioCleaner()
df = cleaner.clean_column_names(df)      # "Drug Name" -> "drug_name"
df = cleaner.remove_duplicates(df)       # 移除重複的 Tylenol
df = cleaner.drop_missing(df)            # 移除 Unknown

print("清洗後的資料：")
print(df)

# --- 階段二：特徵工程 (Transformation) ---
transformer = FeatureTransformer()

# 準備切分 (假設我們要預測 toxicity，不使用 drug_name)
# 先把非數值欄位拿掉 (這裡簡單示範)
df_numeric = df.drop(columns=['drug_name'])

X, y = transformer.split_X_y(df_numeric, target_col='toxicity')

# 標準化 X
X_scaled = transformer.scale_features(X, method='standard')

print(f"\n準備好的訓練矩陣 X shape: {X_scaled.shape}")
print(f"準備好的目標向量 y shape: {y.shape}")

# 接下來就可以把 X_scaled, y 丟給 Brain 去訓練了！