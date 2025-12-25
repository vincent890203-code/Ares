import numpy as np
import pandas as pd
import time
from Ares.brain.cortex import ML_Brain
from Ares.utils.logger import ares_logger

def run_stress_test(n_samples=1000000):
    ares_logger.info(f"🔥 Starting Stress Test with {n_samples} samples...")
    
    # 1. 生成巨量虛擬生醫數據 (30 個特徵)
    X = pd.DataFrame(np.random.rand(n_samples, 30), columns=[f"feature_{i}" for i in range(30)])
    y = np.random.randint(0, 2, n_samples)
    
    # 切分出一小部分做測試
    X_train, X_test = X[:int(n_samples*0.8)], X[int(n_samples*0.8):]
    y_train, y_test = y[:int(n_samples*0.8)], y[int(n_samples*0.8):]
    
    brain = ML_Brain()
    
    start_time = time.time()
    # 執行任務
    brain.solve_mission(X_train, y_train, X_test, y_test, task_type='classification', label_map={0:'Safe', 1:'Toxic'})
    
    end_time = time.time()
    ares_logger.info(f"✅ Stress Test Completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    run_stress_test(1000000) # 挑戰一百萬筆