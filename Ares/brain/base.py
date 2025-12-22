# 檔案位置： Ares/brain/base.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from sklearn.metrics import classification_report, confusion_matrix, mean_squared_error, r2_score

# 設定繪圖風格 (這是你原本的設定)
plt.style.use('seaborn-v0_8')
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Microsoft JhengHei', 'SimHei'] 
plt.rcParams['axes.unicode_minus'] = False

@dataclass
class ClassificationResult:
    """分類任務的報告"""
    predictions: np.ndarray
    probabilities: np.ndarray
    prediction_labels: list
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@dataclass
class RegressionResult:
    """回歸任務的報告"""
    predictions: np.ndarray
    actuals: np.ndarray = None 
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class BaseAlgorithm(ABC):
    def __init__(self, model_name):
        self.model = None
        self.model_name = model_name
        self.feature_names_ = None

# 檔案位置： Ares/brain/base.py 裡面的 BaseAlgorithm 類別下

    def _validate_input(self, X, is_training=False):
        """共用的輸入檢查守門員 (已升級：支援 Numpy Array)"""
        
        # 1. 自動容錯：如果是 Numpy Array，直接轉成 DataFrame
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)

        # 2. 經過轉換後，如果還不是 DataFrame 就真的報錯
        if not isinstance(X, pd.DataFrame):
            raise TypeError(f"❌ {self.model_name}: 請輸入 pd.DataFrame 格式")
        
        # 3. 訓練模式：記錄特徵名稱 (如果是 Numpy 轉來的，欄位名會是 0, 1, 2...)
        if is_training:
            self.feature_names_ = list(X.columns)
            return X
        
        # 4. 預測模式：檢查模型是否已訓練
        if self.feature_names_ is None:
            raise Exception("❌ 模型尚未訓練")
        
        # 5. 預測模式：欄位對齊檢查
        # 如果輸入的是 Numpy (欄位名是 0, 1...)，通常長度對了就行，這裡做個寬容處理
        missing = set(self.feature_names_) - set(X.columns)
        if missing:
            # 只有當缺失的欄位不是 "數字索引" 時才報錯，避免太嚴格
            if not all(isinstance(col, int) for col in missing):
                 raise ValueError(f"❌ 缺少欄位: {missing}")
            
        return X[self.feature_names_]

    @abstractmethod
    def fit(self, X, y): pass

class BaseClassifier(BaseAlgorithm):
    def __init__(self, model_name, label_map):
        super().__init__(model_name)
        self.label_map = label_map

    def predict(self, X) -> ClassificationResult:
        X_val = self._validate_input(X)
        preds = self.model.predict(X_val)
        
        if hasattr(self.model, "predict_proba"):
            probs = np.max(self.model.predict_proba(X_val), axis=1)
        else:
            probs = np.zeros_like(preds, dtype=float)
            
        labels = [self.label_map.get(p, str(p)) for p in preds]
        return ClassificationResult(preds, probs, labels)

    def evaluate(self, X_test, y_test):
        res = self.predict(X_test)
        print(f"\n=== {self.model_name} 分類報告 ===")
        print(classification_report(y_test, res.predictions))
        
        cm = confusion_matrix(y_test, res.predictions)
        plt.figure(figsize=(5, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'{self.model_name} Confusion Matrix')
        plt.show()

class BaseRegressor(BaseAlgorithm):
    def __init__(self, model_name):
        super().__init__(model_name)

    def predict(self, X) -> RegressionResult:
        X_val = self._validate_input(X)
        preds = self.model.predict(X_val)
        return RegressionResult(predictions=preds)

    def evaluate(self, X_test, y_test):
        res = self.predict(X_test)
        mse = mean_squared_error(y_test, res.predictions)
        r2 = r2_score(y_test, res.predictions)
        
        print(f"\n=== {self.model_name} 回歸報告 ===")
        print(f"📉 MSE: {mse:.4f}")
        print(f"📊 R2 Score: {r2:.4f}")
        
        plt.figure(figsize=(6, 5))
        plt.scatter(y_test, res.predictions, alpha=0.6, color='teal')
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        plt.xlabel("True Values")
        plt.ylabel("Predictions")
        plt.title(f"{self.model_name}: Actual vs Predicted")
        plt.show()