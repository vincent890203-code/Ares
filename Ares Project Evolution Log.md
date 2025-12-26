# 🛡️ Ares System: Full Development History

> **Project Goal**: Building an End-to-End Biomedical Data Intelligence Agent.  
> **Current Version**: v1.0.0 (Intelligence Phase)  
> **Timeline**: 2025-12-18 to 2025-12-26
> **Author**: Yuan Chen Kuo
---

## 📅 Part 1: Version History (版本演進)
### 🚀 Phase 4: Production & Deployment (生產部署與整合)

**v1.1.0 - The Arsenal Integration** (Bonus: 2025/12/26)
* **核心目標**: 驗證 Spider/Refinery/Brain 三部門的協同作戰能力 (End-to-End)。
* **主要變動**:
    * **[Feature] Spider Reinforcement**: 在 `actions.py` 新增 `smart_scroll` (應對 Lazy Loading) 與參數自適應偵錯。
    * **[Test] Full Pipeline Verification**: 建立 `full_pipeline_test.py`，模擬從 PubChem 爬取到 QSAR 建模的完整流程。
    * **[Tool] Introspection**: 開發 `inspect_ares.py`，實現對自身模組架構的動態盤點。

**v1.0.0 - Containerization (Docker)** (Day 5: 2025/12/26)
* **核心目標**: 實現「環境即代碼 (Infrastructure as Code)」，解決跨平台相依性問題。
* **主要變動**:
    * **[Infra] Docker Support**: 撰寫 `Dockerfile`，建立輕量級 Python 執行環境 (`ares-app:clean`)。
    * **[CLI] Unified Interface**: 建立 `cli.py`，支援透過指令列 `python -m Ares.cli --task classification` 直接調度大腦。
    * **[UX] Professional Logging**: 優化日誌系統，過濾 `FutureWarning` 與 `ConvergenceWarning`，提供清晰的任務報告。

**v0.6.0 - Stress Testing** (Day 4: 2025/12/25)
* **核心目標**: 測試系統在大規模運算下的穩定性與記憶體管理。
* **主要變動**:
    * **[Refine] Registry Optimization**: 優化模型儲存機制，確保在大量訓練迭代下不會發生 I/O 衝突。
    * **[Fix] Parallel Processing**: 修正 Windows 環境下 Joblib 多工處理的鎖定問題。
### 🧠 Phase 3: Intelligence (賦予智慧)
**v0.5.0 - The AutoML Upgrade** (Day 3: 2025/12/25)
* **核心目標**: 讓 Ares 從「只會用預設參數」進化為「懂得自我優化」。
* **主要變動**:
    * **[New] Hyperparameter Tuning**: 在 `BaseAlgorithm` 實作 `optimize()`，整合 `GridSearchCV` 與 Cross-Validation。
    * **[New] Dynamic Parameter Grid**: 所有武器 (`Weapons`) 新增 `get_default_param_grid()` 方法，定義可調參數空間。
    * **[Update] Smart Cortex**: 更新 `think_and_train` 邏輯，自動偵測武器能力並決定是否啟動 Grid Search。
    * **[Fix] Stability**: 修復 `scoring_metric` 變數定義錯誤與 KNN 參數拼字錯誤 (`weights`)。

### 🏗️ Phase 2: Architecture (架構重構)
**v0.4.0 - The MVC Refactoring** (Day 2: 2025/12/24)
* **核心目標**: 解決 `Brain` 模組職責過重問題，導入 **MVC 設計模式**。
* **主要變動**:
    * **[New] Model Registry**: 建立 `registry.py` (View/Store)，專門負責檔案 I/O、模型掃描與版本管理，實現 **單一職責原則 (SRP)**。
    * **[Refactor] Cortex Decoupling**: 將 `cortex.py` (Controller) 中的檔案操作代碼移除，使其專注於 Recall/Train 決策。
    * **[Update] Serialization Protocol**: 放棄儲存原始模型物件，改為儲存 **Payload Dictionary** (含 `feature_names`)，防止特徵錯位造成的 Silent Failure。
    * **[Test] Integration Testing**: 新增 `test_integration_v2.py`，驗證重構後的系統生命週期。

### ⚙️ Phase 1: Infrastructure (基礎設施)
**v0.3.0 - The Engineering Foundation** (Day 1: 2025/12/23)
* **核心目標**: 將散亂的腳本轉型為標準 Python Package，建立 CI/CD。
* **主要變動**:
    * **[Structure] Package Skeleton**: 建立 `Ares/` 根目錄與三大子模組 (`spider`, `refinery`, `brain`)。
    * **[Config] Setup Configuration**: 配置 `setup.py` 支援 Editable Install (`pip install -e .`)。
    * **[CI/CD] Automated Testing**: 建立 GitHub Actions (`tests.yml`) 與 `pytest` 環境。
    * **[Feature] Robust Spider**: 實作 `Retry Decorator` 與 `Hybrid Parsing` (Selenium+BS4)。

**v0.2.0 - The Concept (Ares Genesis)** (2025/12/22)
* **核心目標**: 構思模組化設計，確立 Spider/Refinery/Brain 三位一體的概念。
* **特點**: 初步將 Jupyter Notebook 中的功能封裝為函式，但尚未形成物件導向架構。

**v0.1.0 - Proof of Concept (Project "DeepTox")** (2025/12/18)
* **核心目標**: 驗證「網頁爬蟲 + 機器學習」的可行性。
* **特點**: 單一腳本 (Monolithic Script)，硬編碼 (Hard-coded) 變數，無測試，難以維護。這是一切的起點。

## 💡 Summary
Ares 專案已完成從實驗腳本到 **生產級容器應用 (Production Container)** 的轉變。
目前版本 (**v1.1.0**) 具備完整的 **爬蟲反偵測**、**自動化清洗** 與 **AutoML 建模** 能力，並可透過 Docker 在任何環境中一鍵部署。

---

## 🧩 Part 2: Module Features & Specifications (模組特性詳解)

### 🕷️ 1. Spider Module (The Hunter)
> **負責**: Data Acquisition (資料獲取)

* **Hybrid Parsing (混合解析)**:
    * 結合 `Selenium` (處理動態 JS 渲染) 與 `BeautifulSoup` (快速靜態解析)，平衡效能與兼容性。
* **Resilience System (韌性系統)**:
    * 實作 **Decorator Pattern (`@retry`)**，遇網路波動自動重試，實現指數退避 (Exponential Backoff)。
* **Headless Operations**:
    * 支援無頭模式 (Headless Mode)，適合在 Docker 容器或雲端伺服器 (CI/CD) 中執行。

### 🏭 2. Refinery Module (The Processor)
> **負責**: Data Cleaning & Transformation (資料清洗與轉換)

* **Pipeline Architecture**:
    * 將清洗步驟 (`BioCleaner`) 與轉換步驟 (`FeatureTransformer`) 分離，支援類似 sklearn Pipeline 的串接。
* **Type Safety & Validation**:
    * 內建 Pandas DataFrame 的 schema 檢查，確保進入模型的資料格式正確。
* **Domain Specific**:
    * 針對生醫資料特性（如缺失的 MW 分子量、Toxicity 標籤清洗）內建專用邏輯。

### 🧠 3. Brain Module (The Decision Maker)
> **負責**: AutoML, Model Management & Inference (決策、管理與推論)

#### **A. Controller: Cortex (`cortex.py`)**
* **Agent Logic**: 實現「回憶優先，訓練在後 (Recall-First, Train-Later)」的高級決策邏輯。
* **AutoML Orchestrator**: 自動協調資料流，根據任務類型 (Classification/Regression) 選擇適當的評分指標 (`Accuracy`/`R2`)。
* **Hyperparameter Tuning**: 自動偵測武器能力，動態切換 `GridSearch` 或 `Simple Fit`。

#### **B. Store: Registry (`registry.py`)**
* **Lifecycle Management**: 負責模型的掃描 (Scanning)、載入 (Loading) 與清理。
* **Lazy Loading**: 使用 Python Generator (`yield`) 逐一載入模型，避免一次性讀取大量模型導致記憶體溢出 (OOM)。
* **Version Control**: 透過 Timestamp 與 Metadata 管理模型版本。

#### **C. Model: Weapons (`weapons/*.py`) & Base (`base.py`)**
* **Polymorphism (多型)**: 所有武器皆繼承自 `BaseAlgorithm`，保證介面一致 (`train`, `predict`, `save`, `optimize`)。
* **Encapsulation (封裝)**: 將 `sklearn` 的複雜度封裝在 `SklearnModelWrapper` 內部，對外提供統一 API。
* **Smart Serialization**: 實作 **Payload Protocol**，存檔時一併記錄 `feature_names`，載入時自動驗證欄位順序，杜絕 Silent Failure。
* **Factory Pattern**: 透過 `__init__.py` 與工廠列表動態生成模型實例。

---

### 💡 Summary
從 **v0.1 DeepTox** 的混亂腳本，到 **v0.5 Ares** 的自動化智慧系統，這個專案見證了：
1.  **程式碼品質**的提升 (Linting, Modularization)。
2.  **架構思維**的建立 (MVC, OOP, Design Patterns)。
3.  **工程紀律**的實踐 (Testing, Git, CI/CD)。