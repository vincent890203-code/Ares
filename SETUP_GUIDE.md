# Ares 套件環境啟動指南

## 快速啟動（如果已安裝）

```bash
# 1. 進入專案目錄
cd C:\Users\USER\Desktop\Ares

# 2. 確保環境變數已載入（如果有 .env 檔案）
# 確保 GEMINI_API_KEY 等變數已設定

# 3. 直接使用
python playground_research.py
# 或
python playground-2.py
```

## 完整安裝步驟（首次使用或重新安裝）

### Windows PowerShell

```powershell
# 1. 進入專案目錄
cd C:\Users\USER\Desktop\Ares

# 2. 安裝所有依賴套件
pip install -r requirements.txt

# 3. 以可編輯模式安裝 Ares 套件（重要！）
pip install -e .

# 4. 驗證安裝
python -c "from Ares.departments.Research.editor import ResearchEditor; print('✓ 安裝成功')"
```

### 設定環境變數（.env 檔案）

在專案根目錄創建 `.env` 檔案：

```env
GEMINI_API_KEY=your_api_key_here
```

## 使用方式

```python
# 匯入模組
from Ares.departments.Research.scout import PubMedScout
from Ares.departments.Research.editor import ResearchEditor
from Ares.departments.finance.manager import FinancePipeline

# 或使用 CLI（如果已安裝）
ares --help
```

## 常見問題

### 問題 1: ModuleNotFoundError
```bash
# 解決：重新安裝套件
pip install -e .
```

### 問題 2: 缺少依賴套件
```bash
# 解決：重新安裝依賴
pip install -r requirements.txt
```

### 問題 3: 環境變數未載入
```bash
# 確保 .env 檔案存在於專案根目錄
# 或在程式碼中使用 load_dotenv()
```
