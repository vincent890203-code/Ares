# Ares: End-to-End Biomedical Data Intelligence Agent

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-Private-red.svg)
![Coverage](https://img.shields.io/badge/coverage-50%25-yellowgreen.svg)

> **"From Raw Data to Actionable Insights."**

**Ares** 是一個高度模組化、可容器化部署的全端數據智慧系統。它不僅是一個生醫分析工具，更是資深工程師的個人軍火庫，整合了**隱匿爬蟲 (Spider)**、**數據提煉工廠 (Refinery)** 與 **自動化機器學習大腦 (Brain)**。

---

## 核心模組 (Core Modules)

### **Spider (情報搜集)**
負責底層資料獲取，採用混合解析技術。
- **Hybrid Parsing**: 整合 `Selenium` (動態交互) 與 `BeautifulSoup` (靜態解析)，兼顧速度與靈活性。
- **Tactical Actions**: 封裝 `safe_click`, `safe_type`, `nuclear_scroll` 等戰術動作，內建 `WebDriverWait` 顯式等待，解決網頁加載不同步問題。
- **Robustness**: 內建 `@retry` 裝飾器，自動處理網路波動與暫時性連線錯誤。

### **Refinery (資料提煉)**
負責將非結構化數據轉換為模型可用的特徵矩陣。
- **BioCleaner**: 專針對生醫資料設計，處理化學式亂碼、缺失值填充與字串正規化。
- **FeatureTransformer**: 提供自動化特徵工程，包含 One-Hot Encoding、標準化 Scaling 與矩陣維度重塑。

### **Brain (決策核心)**
具備自動化機器學習 (AutoML) 能力的決策中心。
- **Auto-Selection**: 給定任務類型（分類/回歸），自動對比多種模型（SVM, KNN, LR, RF, MLP），挑選最佳解。
- **Memory System**: 具備模型註冊機制 (`Registry`)，自動儲存表現最優異的模型參數與權重。
- **Modular Weapons**: 採用工廠模式與繼承結構，易於擴充 `XGBoost` 或 `PyTorch` 等新演算法。

---

## 專案架構 (Project Structure)
```
Ares-Project/
│
├── .github/
│   └── workflows/           
│       └── tests.yml
│
├── Ares/                    
│   ├── __init__.py
│   ├── cli.py               # [Entry] 統一指令列入口
│   ├── spider/              
│   │   ├── __init__.py
│   │   ├── core.py          # Driver setup, Retry logic
│   │   ├── actions.py       # Tactical Actions (Scroll, Safe Click)
│   │   └── extraction.py    # Parsing logic
│   │
│   ├── refinery/            
│   │   ├── __init__.py
│   │   ├── cleaner.py       # Data cleaning logic
│   │   └── transformer.py   # Feature engineering
│   │
│   └── brain/               
│       ├── __init__.py
│       ├── cortex.py        # AutoML Orchestrator
│       ├── registry.py      # Model Version Control
│       └── weapons/         # Algorithm Factory (SVM, LR, KNN...)
│   
├── tests/                  
│   ├── __init__.py
│   ├── test_spider.py
│   └── test_refinery.py
│
├── notebooks/               
│   └── experiment_v1.ipynb
│
├── .gitignore               
├── README.md                
├── requirements.txt         
├── setup.py                 
└── Dockerfile               
```

---
## Usage Example(End-to-end Workflow)

```
import pandas as pd
from Ares.spider.core import setup_driver
from Ares.refinery.cleaner import BioCleaner
from Ares.refinery.transformer import FeatureTransformer
from Ares.brain.cortex import ML_Brain

# ==========================================
# Phase 1: Hunt (資料搜集層)
# ==========================================
# 啟動具備錯誤重試與戰術動作支援的瀏覽器
driver = setup_driver(headless=True)
# [範例邏輯]：模擬從網頁抓取後的生醫原始數據
raw_data = pd.DataFrame([
    {"Drug": "Aspirin", "MW": 180.16, "Toxicity": 0},
    {"Drug": "Tylenol", "MW": 151.16, "Toxicity": 1},
    {"Drug": "Unknown", "MW": None,   "Toxicity": 0}
])
driver.quit()

# ==========================================
# Phase 2: Refine (資料提煉層)
# ==========================================
# 1. 執行生醫專用清洗邏輯
cleaner = BioCleaner()
df = cleaner.clean_column_names(raw_data)
df = cleaner.drop_missing(df)

# 2. 自動化特徵工程
transformer = FeatureTransformer()
# 自動分離特徵 (X) 與標籤 (y)，並進行數值標準化
X, y = transformer.split_X_y(df.drop(columns=['drug']), target_col='toxicity')
X_scaled = transformer.scale_features(X)

# ==========================================
# Phase 3: Think (大腦決策層)
# ==========================================
brain = ML_Brain()

# 使用核心指令：solve_mission
# 系統將自動判斷：是否存在高效能舊模型 (Memory Recall) 或需啟動新一輪 AutoML 訓練
best_model = brain.solve_mission(
    X_train=X_scaled, y_train=y, 
    X_test=X_scaled, y_test=y,
    task_type='classification',
    label_map={0: 'Safe', 1: 'Toxic'},
    threshold=0.85  # 設定效能滿意度門檻
)

if best_model:
    print(f"✅ Mission Success. Optimal Model: {best_model.model_name}")
```
---

## 架構設計 (Architecture Design)

本專案採用 **模組化 (Modularity)** 與 **物件導向 (OOP)** 設計原則，確保高內聚、低耦合：

* **單一職責原則 (SRP)**：Spider 只管抓、Refinery 只管洗、Brain 只管算。
* **介面隔離 (Interface Segregation)**: 透過 `Ares/__init__.py` 扁平化命名空間，外部呼叫只需 `from Ares import ...`，隱藏內部複雜實作。
* **可擴充性 (Scalability)**: 新增模型只需繼承 `BaseClassifier`，無需修改 Brain 的核心邏輯。

---

## 核心設計亮點 (Technical Highlights)

End-to-End Pipeline: 實現了從原始數據輸入到產出決策的完整閉環。

AutoML Integration: 在 brain 模組中隱藏了模型選擇的複雜度，實現「任務驅動」的設計模式。

High Testability: 透過模組解耦，使核心清洗與動作邏輯達成 100% 的測試覆蓋。

---

## Roadmap

[x] Phase 1: 爬蟲動作封裝與 Retry 機制。

[x] Phase 2: 模組化數據清洗工廠 (BioCleaner) 達 100% 覆蓋率。

[x] Phase 3: 基礎 AutoML 大腦與模型註冊機制。

[x] Phase 4: GitHub Actions CI/CD 自動化測試建置 (修正 Linux 大小寫路徑問題)。

[ ] Phase 5: 整合深度學習 (PyTorch) 進行複雜毒性預測。

[ ] Phase 6: 開發 FastAPI 接口將 Ares 部署為雲端數據 Service。

---

## 開發者指南 (Installation)

本專案採用 開放模式安裝 (Editable Mode)，修改程式碼後無需重新安裝。

請確保已安裝 `Anaconda` 與 `Python 3.x`。

```bash
# 1. 克隆專案
git clone [https://github.com/vincent890203-code/Ares.git](https://github.com/vincent890203-code/Ares.git)
cd Ares

# 2. 安裝依賴與套件 (確保路徑指向您的 Ares 資料夾)
pip install -r requirements.txt
pip install -e .

# 3. 執行測試並查看報告
pytest --cov=Ares
```

---

## 🚀 Quick Start (Docker Mode)

Ares 已經完全容器化，您可以無需安裝任何 Python 環境，直接透過 Docker 執行：

```bash
# 1. 建置映像檔
docker build -t ares-app:clean .

# 2. 執行分類任務 (自動化建模)
docker run --rm ares-app:clean --task classification --data breast_cancer

# 3. 執行自定義腳本 (例如爬蟲測試)
docker run --rm --entrypoint python ares-app:clean tests/spider_test.py
---

License: Private use only

Author: Yuan-Chen Kuo (vincent890203@gmail.com)