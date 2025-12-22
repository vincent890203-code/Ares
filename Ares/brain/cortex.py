import os
import glob
import joblib
from datetime import datetime
import pandas as pd
import numpy as np

# 評分工具
from sklearn.metrics import r2_score, accuracy_score 

# 從武器庫匯入
from .weapons import (
    LinearRegressionWeapon, PolynomialRegressionWeapon, DecisionTreeRegressorWeapon, SVRWeapon,
    LogisticRegressionWeapon, SVMClassifierWeapon, KNNClassifierWeapon
)

class ML_Brain:
    def __init__(self, memory_path="./brain_memory/"):
        self.memory_path = memory_path
        if not os.path.exists(memory_path):
            os.makedirs(memory_path)
        
        # 定義回歸武器 (可以直接實例化)
        self.regressors = [
            LinearRegressionWeapon(),
            PolynomialRegressionWeapon(degree=2),
            DecisionTreeRegressorWeapon(max_depth=5),
            SVRWeapon()
        ]
        
        # 定義分類武器工廠 (需要 label_map 才能實例化)
        self.classifier_factories = [
            lambda map: LogisticRegressionWeapon(label_map=map),
            lambda map: SVMClassifierWeapon(label_map=map),
            lambda map: KNNClassifierWeapon(label_map=map, k=5)
        ]

    def solve_mission(self, X_train, y_train, X_test, y_test, task_type='classification', label_map=None, threshold=0.85):
        """
        [Agent 對外唯一接口]
        Ares 的高級決策流程：
        1. 先嘗試回憶 (Recall)
        2. 若回憶失敗或分數過低，則啟動訓練 (Train)
        """
        print(f"\n[Ares Brain] Processing {task_type} mission...")

        # 1. 嘗試回憶
        best_old_model = self._recall_memory(X_test, y_test, task_type, threshold)

        if best_old_model:
            print(f"[Ares Brain] Memory Recall Success: Using existing model.")
            return best_old_model
        
        # 2. 回憶失敗，開始訓練
        print(f"[Ares Brain] Memory Recall Failed (or score too low). Starting AutoML training...")
        return self.think_and_train(X_train, y_train, X_test, y_test, task_type, label_map)

    def _recall_memory(self, X_test, y_test, task_type, threshold):
        """
        [內部功能] 搜尋記憶庫，讓每個舊模型出來跑測試數據
        """
        pkl_files = glob.glob(f"{self.memory_path}*.pkl")
        if not pkl_files:
            print("   -> Memory is empty.")
            return None

        best_score = -float('inf')
        best_model = None

        print("   -> Scanning memory files...")

        for pkl_path in pkl_files:
            try:
                # 載入模型
                model = joblib.load(pkl_path)
                model_name = os.path.basename(pkl_path)

                # 讓舊模型跑新數據
                res = model.predict(X_test)

                # 計算分數
                if task_type == 'classification':
                    score = accuracy_score(y_test, res.predictions)
                else:
                    score = r2_score(y_test, res.predictions)
                
                print(f"      - Checking [{model_name}]... Score: {score:.4f}")

                # 記錄最強的舊模型
                if score > best_score:
                    best_score = score
                    best_model = model

            except Exception as e:
                # 通常是欄位不符 (Schema Mismatch)
                print(f"      - Skipping [{os.path.basename(pkl_path)}]: Incompatible data schema.")

        # 決策：是否採用
        if best_model and best_score >= threshold:
            print(f"   -> Found valid memory! Score {best_score:.4f} >= Threshold {threshold}")
            return best_model
        
        return None

    def think_and_train(self, X_train, y_train, X_test, y_test, task_type='regression', label_map=None):
        """
        [內部功能] 執行 AutoML 訓練流程
        """
        print(f"\n[Ares Training] Starting model selection...")
        
        best_score = -float('inf')
        best_model = None
        
        # 準備武器
        if task_type == 'regression':
            candidates = self.regressors
            metric_name = "R2 Score"
        elif task_type == 'classification':
            if label_map is None:
                raise ValueError("[Error] Classification task requires label_map.")
            candidates = [factory(label_map) for factory in self.classifier_factories]
            metric_name = "Accuracy"
        else:
            raise ValueError("[Error] Unknown task type.")

        # 訓練迴圈
        for weapon in candidates:
            print(f"   - Training weapon: {weapon.model_name} ...", end=" ")
            try:
                weapon.fit(X_train, y_train)
                res = weapon.predict(X_test)
                
                if task_type == 'regression':
                    score = r2_score(y_test, res.predictions)
                else:
                    score = accuracy_score(y_test, res.predictions)
                
                print(f"-> {metric_name}: {score:.4f}")
                
                if score > best_score:
                    best_score = score
                    best_model = weapon
            except Exception as e:
                print(f"Failed. Reason: {e}")

        # 結算
        if best_model:
            print(f"[Ares Training] Winner: [{best_model.model_name}] with Score: {best_score:.4f}")
            self._memorize(best_model)
            return best_model
        else:
            print("[Ares Training] All models failed.")
            return None

    def _memorize(self, model):
        """
        [內部功能] 將模型存檔
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.memory_path}best_{model.model_name}_{timestamp}.pkl"
        joblib.dump(model, filename)
        print(f"[Ares Memory] Model saved to: {filename}")