import pandas as pd
import numpy as np
from Ares import ML_Brain, FeatureTransformer

# === 模擬資料生成器 ===
def get_data(difficulty='easy'):
    """
    easy: 簡單規律，舊模型應該能解
    hard: 規律改變，舊模型會失敗 -> 強制重練
    """
    np.random.seed(42)
    # 產生 100 筆資料，2 個特徵
    X = np.random.rand(100, 2)
    
    if difficulty == 'easy':
        # 簡單規則：特徵1 > 0.5 就是有毒
        y = (X[:, 0] > 0.5).astype(int)
    else:
        # 困難規則：特徵1 + 特徵2 > 1 才是有毒 (邏輯變了!)
        y = ((X[:, 0] + X[:, 1]) > 1.0).astype(int)
        
    return pd.DataFrame(X, columns=['f1', 'f2']), y

# === 測試腳本 ===
def main():
    brain = ML_Brain()
    
    print("======== 第一回合：初次見面 (Create Memory) ========")
    X1, y1 = get_data(difficulty='easy')
    
    # 第一次跑，記憶庫可能是空的，或是舊的不適用，它應該會訓練
    # 注意：我們改用 solve_mission
    model_v1 = brain.solve_mission(
        X1, y1, X1, y1, 
        task_type='classification',
        label_map={0: 'Safe', 1: 'Toxic'}
    )

    print("\n======== 第二回合：遇到類似問題 (Use Memory) ========")
    # 我們生成一樣規律的資料 ('easy')
    X2, y2 = get_data(difficulty='easy')
    
    # 這次它應該要發現 "欸！我以前學過！" 然後直接用舊的，不應該看到 "訓練武器..."
    model_v2 = brain.solve_mission(
        X2, y2, X2, y2, 
        task_type='classification',
        label_map={0: 'Safe', 1: 'Toxic'},
        threshold=0.9 # 門檻設高一點測試
    )

    print("\n======== 第三回合：世界變了 (Retrain) ========")
    # 規律變成了 'hard'，舊模型的準確率會大幅下降
    X3, y3 = get_data(difficulty='hard')
    
    # 它應該會試著用舊的回憶，發現分數很爛，然後被迫重新訓練
    model_v3 = brain.solve_mission(
        X3, y3, X3, y3, 
        task_type='classification',
        label_map={0: 'Safe', 1: 'Toxic'}
    )

if __name__ == "__main__":
    main()