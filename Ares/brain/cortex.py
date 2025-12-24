import os
import glob
import joblib
from datetime import datetime
import pandas as pd
import numpy as np
from .registry import ModelRegistry

# 評分工具
from sklearn.metrics import r2_score, accuracy_score 

# 從武器庫匯入
from .weapons import (
    LinearRegressionWeapon, PolynomialRegressionWeapon, DecisionTreeRegressorWeapon, SVRWeapon,
    LogisticRegressionWeapon, SVMClassifierWeapon, KNNClassifierWeapon
)

class ML_Brain:
    def __init__(self, memory_path="./brain_memory/"):

        # 初始化 Registry，把路徑交給它管
        self.registry = ModelRegistry(memory_path)

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
        [修正後的讀取邏輯]
        不再自己 glob 檔案，而是呼叫 self.registry.load_all_models()
        """
        best_score = -float('inf')
        best_model_payload = None

        # 關鍵差異：這裡改用 registry 的產生器，不再報錯找不到 memory_path
        for name, model_core in self.registry.load_all_models():
            try:
                # 這裡拿到的 model_core 是 sklearn 原生模型 (因為 base.py save 的是原生模型)
                preds = model_core.predict(X_test)

                if task_type == 'classification':
                    score = accuracy_score(y_test, preds)
                else:
                    score = r2_score(y_test, preds)
                
                print(f"      - Checking [{name}]... Score: {score:.4f}")

                if score > best_score:
                    best_score = score
                    best_model_payload = model_core

            except Exception as e:
                print(f"      - Error checking [{name}]: {e}")

        if best_model_payload and best_score >= threshold:
            print(f"   -> Found valid memory! Score {best_score:.4f}")
            return best_model_payload
        
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
            scoring_metric = 'r2'

        elif task_type == 'classification':
            if label_map is None:
                raise ValueError("[Error] Classification task requires label_map.")
            # 每次都要重新建立新的實例，避免汙染
            candidates = [factory(label_map) for factory in self.classifier_factories]
            metric_name = "Accuracy"
            scoring_metric = 'accuracy'
        else:
            raise ValueError("[Error] Unknown task type.")

        # 訓練迴圈
        for weapon in candidates:
            print(f"   - Training weapon: {weapon.model_name} ...", end=" ")
            try:
                # ==========================================
                # Day 3 新功能：超參數調優 (Hyperparameter Tuning)
                # ==========================================
                # 1. 取得該武器的參數網格
                param_grid = getattr(weapon, 'get_default_param_grid', lambda: {})()
                
                # 2. 決定策略：有網格就 Optimize，沒網格就 Fit
                if param_grid:
                    # cv=3 代表做 3 折交叉驗證 (為了速度先設 3，正式可設 5)
                    weapon.optimize(X_train, y_train, param_grid, cv=3, scoring=scoring_metric)
                else:
                    print(f"     (No param grid found, using default fit)")
                    weapon.fit(X_train, y_train)

                # 3. 驗證 (使用獨立的測試集)
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
            best_model.save(self.registry.memory_path)
            return best_model
        else:
            print("[Ares Training] All models failed.")
            return None