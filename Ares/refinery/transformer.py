# 檔案位置： Ares/refinery/transformer.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

class FeatureTransformer:
    """
    負責將乾淨的數據轉換為模型可用的矩陣 (Transformation)。
    職責：標準化 (Scaling)、切分 X/y、Reshape。
    """

    @staticmethod
    def to_dataframe(data, columns=None) -> pd.DataFrame:
        """將爬蟲抓到的 list of dicts 轉為 DataFrame"""
        return pd.DataFrame(data, columns=columns)

    @staticmethod
    def split_X_y(df: pd.DataFrame, target_col: str):
        """
        將 DataFrame 拆解為特徵矩陣 (X) 和 目標向量 (y)。
        回傳: (X, y)
        """
        if target_col not in df.columns:
            print(f"⚠️ [Transformer] 警告：目標欄位 '{target_col}' 不存在，將回傳整個矩陣與 None。")
            return df.values, None
            
        y = df[target_col].values
        X = df.drop(columns=[target_col]).values
        return X, y

    @staticmethod
    def scale_features(X: np.ndarray, method='minmax'):
        """
        數值標準化 (Normalization)。
        - KNN, SVM 對此非常敏感，必須做。
        - Tree-based 模型 (Decision Tree) 通常不需要，但做了也無妨。
        """
        if method == 'minmax':
            scaler = MinMaxScaler()
            return scaler.fit_transform(X)
        elif method == 'standard':
            scaler = StandardScaler()
            return scaler.fit_transform(X)
        return X

    @staticmethod
    def reshape_array(data: np.ndarray, shape: tuple):
        """
        安全的 Reshape，防止維度對不上時程式崩潰。
        """
        try:
            return data.reshape(shape)
        except ValueError as e:
            print(f"❌ [Transformer Error] Reshape failed: {e}")
            print(f"   -> 目前形狀: {data.shape}, 目標形狀: {shape}")
            return data