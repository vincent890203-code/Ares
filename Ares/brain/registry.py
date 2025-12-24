import os
import glob
import joblib

class ModelRegistry:
    def __init__(self, memory_path):
        self.memory_path = memory_path
        if not os.path.exists(memory_path):
            os.makedirs(memory_path)

    def load_all_models(self):
        """
        掃描並載入所有記憶中的模型。
        回傳一個產生器 (Generator)，每次 yield (model_name, model_core)。
        
        Why Generator? 
        如果記憶資料夾有 100 個模型，一次全部讀進 RAM 會爆炸。
        用 yield 一次讀一個，測完就丟，節省記憶體。
        """
        # 抓取所有可能的檔案格式 (相容舊版 .pkl)
        files = glob.glob(os.path.join(self.memory_path, "*.joblib")) + \
                glob.glob(os.path.join(self.memory_path, "*.pkl"))

        if not files:
            print("   [Registry] Memory is empty.")
            return

        print(f"   [Registry] Found {len(files)} memory files. Scanning...")

        for path in files:
            try:
                content = joblib.load(path)
                
                # 相容性處理：判斷是新版字典還是舊版物件
                if isinstance(content, dict) and 'model' in content:
                    # 新版格式 (BaseAlgorithm.save 產生的 payload)
                    model_core = content['model']
                    name = content.get('meta', {}).get('name', 'Unknown')
                else:
                    # 舊版格式 (直接存模型物件)
                    model_core = content
                    name = os.path.basename(path)
                
                yield name, model_core

            except Exception as e:
                print(f"   [Registry] Corrupted memory file '{os.path.basename(path)}': {e}")

    def clear_memory(self):
        """清空所有記憶 (慎用)"""
        files = glob.glob(os.path.join(self.memory_path, "*"))
        for f in files:
            try:
                os.remove(f)
                print(f"   [Registry] Deleted: {f}")
            except Exception as e:
                print(f"   [Registry] Failed to delete {f}: {e}")