import argparse
import pandas as pd
from sklearn.datasets import load_breast_cancer, load_diabetes
from sklearn.model_selection import train_test_split
from Ares.brain.cortex import ML_Brain
from Ares.utils.logger import ares_logger

def main():
    parser = argparse.ArgumentParser(description="🛡️ Ares Biomedical Intelligence System CLI")
    
    # 定義指令
    parser.add_argument("--task", type=str, choices=['classification', 'regression'], required=True, 
                        help="執行任務類型：分類或回歸")
    parser.add_argument("--data", type=str, default="breast_cancer", 
                        help="資料集名稱 (目前支援 breast_cancer 或 diabetes)")
    parser.add_argument("--threshold", type=float, default=0.85, 
                        help="模型召回門檻 (預設 0.85)")
    parser.add_argument("--memory", type=str, default="./brain_memory/", 
                        help="記憶檔案夾路徑")

    args = parser.parse_args()

    ares_logger.info(f"🚀 Ares CLI 啟動中... 執行任務: {args.task}")

    # 1. 載入資料 (模擬流程，未來可串接 spider)
    if args.data == "breast_cancer":
        data = load_breast_cancer()
        X = pd.DataFrame(data.data, columns=data.feature_names)
        y = data.target
        label_map = {0: 'Malignant', 1: 'Benign'}
    elif args.data == "diabetes":
        data = load_diabetes()
        X = pd.DataFrame(data.data, columns=data.feature_names)
        y = data.target
        label_map = None
    else:
        ares_logger.error(f"❌ 不支援的資料集: {args.data}")
        return

    # 2. 切分資料
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. 喚醒大腦
    brain = ML_Brain(memory_path=args.memory)

    # 4. 執行任務
    try:
        winner = brain.solve_mission(
            X_train, y_train, X_test, y_test,
            task_type=args.task,
            label_map=label_map,
            threshold=args.threshold
        )
        
        if winner:
            ares_logger.info(f"🏆 任務達成！最強武器: {winner.model_name}")
        else:
            ares_logger.warning("⚠️ 任務結束，但未能找到合適的模型。")
            
    except Exception as e:
        ares_logger.error(f"💥 運行時發生系統崩潰: {e}")

if __name__ == "__main__":
    main()