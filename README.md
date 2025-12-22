# Ares: End-to-End Biomedical Data Intelligence Agent

> **"From Raw Data to Actionable Insights."**

**Ares** 是一個模組化的全端數據智慧系統，專為生醫資料科學專案設計。它整合了**自動化爬蟲 (Spider)**、**資料清洗工廠 (Refinery)** 與 **自動化機器學習大腦 (Brain)**，實現從網頁數據擷取到模型預測的端到端 (End-to-End) 流程。

---

## 核心模組 (Core Modules)

###  **Spider (情報搜集軍團)**
負責底層資料獲取，採用混合解析技術。
- **Hybrid Parsing**: 整合 `Selenium` (動態交互) 與 `BeautifulSoup` (靜態解析)，兼顧速度與靈活性。
- **Tactical Actions**: 封裝 `safe_click`, `nuclear_scroll` 等戰術動作，內建顯式等待 (Smart Wait)，解決網頁加載不同步問題。
- **Robustness**: 內建裝飾器 (Decorators) 處理錯誤重試 (Retry) 機制。

###  **Refinery (資料提煉軍團)**
負責將非結構化數據轉換為模型可用的特徵矩陣。
- **BioCleaner**: 專針對生醫資料設計的清洗器（處理化學式亂碼、缺失值填充、字串正規化）。
- **FeatureTransformer**: 自動化特徵工程（One-Hot Encoding, 標準化 Scaling, Numpy Reshape）。

###  **Brain (決策核心軍團)**
具備自動化機器學習 (AutoML) 能力的決策中心。
- **Auto-Selection**: 給定任務類型（分類/回歸），自動派出多種模型（SVM, KNN, LR, RF）進行比武，挑選最佳解。
- **Memory System**: 自動儲存表現最好的模型與參數。
- **Modular Weapons**: 採用工廠模式與繼承結構 (`BaseAlgorithm`)，易於擴充新演算法 (如 XGBoost, PyTorch)。

---
## 專案架構 (Project Structure)
```
Ares-Project/
│
├── .github/
│   └── workflows/           # 未來放 CI/CD (GitHub Actions)
│       └── tests.yml
│
├── ares/                    # [主程式包] 所有的核心程式碼都在這
│   ├── __init__.py          # 讓 ares 變成一個 package (就是您之前設定 __all__ 的地方)
│   ├── spider/              # [情報官]
│   │   ├── __init__.py
│   │   ├── core.py          # Driver setup, retry logic
│   │   └── actions.py       # Specific scrolling/clicking
│   │
│   ├── refinery/            # [煉金術師]
│   │   ├── __init__.py
│   │   ├── cleaner.py       # Data cleaning logic
│   │   └── transformer.py   # Feature engineering
│   │
│   └── brain/               # [大腦]
│       ├── __init__.py
│       ├── cortex.py        # Model logic (Wrapper Class)
│       └── registry.py      # [新增] 用來管理模型版本的 (Model Registry)
│
├── tests/                   # [測試區] 這是身價 60k+ 的關鍵
│   ├── __init__.py
│   ├── test_spider.py
│   └── test_refinery.py
│
├── notebooks/               # [實驗區] 把您的 Jupyter Notebook 都丟進來，不要汙染根目錄
│   └── experiment_v1.ipynb
│
├── .gitignore               # 忽略垃圾檔案 (__pycache__, .env)
├── README.md                # 門面 (等下處理)
├── requirements.txt         # 依賴套件 (pip freeze > requirements.txt)
├── setup.py                 # [關鍵] 讓別人可以用 pip install 安裝您的工具
└── Dockerfile               # [關鍵] 容器化設定 (明天處理)
```

---
## Usage Example(End-to-end Workflow)

```
import pandas as pd
from Ares import setup_driver, BioCleaner, FeatureTransformer, ML_Brain

# ==========================================
# Phase 1: Hunt (Data Acquisition)
# ==========================================
# 使用封裝好的 setup_driver 啟動瀏覽器
driver = setup_driver()
# driver.get("[https://target-website.com](https://target-website.com)")
# ... (省略爬蟲過程) ...

# 假設我們已經抓到了以下生醫資料：
raw_data = pd.DataFrame([
    {"Drug": "Aspirin", "MW": 180.16, "Toxicity": 0},
    {"Drug": "Tylenol", "MW": 151.16, "Toxicity": 1},
    {"Drug": "Unknown", "MW": None,   "Toxicity": 0}
])
driver.quit() # 任務完成，關閉瀏覽器

# ==========================================
# Phase 2: Refine (Data Processing)
# ==========================================
# 1. Cleaning
cleaner = BioCleaner()
df = cleaner.clean_column_names(raw_data)
df = cleaner.drop_missing(df)

# 2. Transformation
transformer = FeatureTransformer()
# 自動切分特徵 (X) 與 目標 (y)
X, y = transformer.split_X_y(df.drop(columns=['drug']), target_col='toxicity')
# 數值標準化
X_scaled = transformer.scale_features(X)

# ==========================================
# Phase 3: Think (Agent Decision)
# ==========================================
brain = ML_Brain()

# 使用 Agent 核心指令：solve_mission
# 它會自動判斷： "我有沒有處理過類似數據？"
# -> 有且表現好：直接使用舊模型 (Recall)
# -> 沒有或表現差：自動啟動 AutoML 訓練 (Train)
best_model = brain.solve_mission(
    X_train=X_scaled, y_train=y, 
    X_test=X_scaled, y_test=y,
    task_type='classification',
    label_map={0: 'Safe', 1: 'Toxic'},
    threshold=0.85  # 滿意度門檻
)

# 查看結果
if best_model:
    print(f"Mission Success. Best Model: {best_model.model_name}")
```
---

## 架構設計 (Architecture Design)

本專案採用 **模組化 (Modularity)** 與 **物件導向 (OOP)** 設計原則，確保高內聚、低耦合：

* **單一職責原則 (SRP)**：Spider 只管抓、Refinery 只管洗、Brain 只管算。
* **介面隔離 (Interface Segregation)**: 透過 `Ares/__init__.py` 扁平化命名空間，外部呼叫只需 `from Ares import ...`，隱藏內部複雜實作。
* **可擴充性 (Scalability)**: 新增模型只需繼承 `BaseClassifier`，無需修改 Brain 的核心邏輯。

---

## Roadmap

[x] Phase 1: Infrastructure - Selenium/BS4 hybrid spider encapsulation.

[x] Phase 2: Robustness - Retry mechanism and error handling.

[x] Phase 3: Brain Module - AutoML system implementation.

[x] Phase 4: Agent Evolution - Memory recall mechanism (solve_mission) and continuous learning.

[ ] Phase 5: Deep Learning - Integrate PyTorch neural networks for complex toxicity prediction (DeepTox 2.0).

[ ] Phase 6: Deployment - Wrap Ares as a FastAPI service.
---

## 安裝方式 (Installation)

此套件採 **開放模式安裝 (Editable Mode)**，修改程式碼後無需重新安裝，適合開發階段。

請確保已安裝 `Anaconda` 與 `Python 3.x`。

```bash
# 請在 Anaconda (base) 或虛擬環境下執行：
# 注意：請將路徑替換為你的實際專案路徑
python -m pip install -e "C:\Users\USER\Desktop\Ares"
```

---

License:
Private use only