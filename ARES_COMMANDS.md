# Ares 系統指令大全

## 📋 主要指令（main.py）

### 1. 財務模組 (Finance)
```bash
# 處理銀行帳單 CSV 檔案
python main.py finance --file <檔案路徑> [--output <輸出路徑>]

# 範例
python main.py finance --file raw_bank_statement.csv
python main.py finance --file raw_bank_statement.csv --output tagged_statement.csv
```

### 2. 研究模組 (Research)
```bash
# 搜尋並分析論文
python main.py research --query "<搜尋關鍵字>" [--limit <數量>] [--output <輸出檔案>]

# 範例
python main.py research --query "LLM in healthcare" --limit 5
python main.py research --query "machine learning" --limit 10 --output my_report.md
```

### 3. 執行所有模組 (All)
```bash
# 執行所有流程（Good Morning Routine）
python main.py all
```

---

## 🧠 大腦記憶庫指令

### 4. 測試知識庫 (Test Brain)
```bash
# 測試 KnowledgeBase 的基本功能
python test_brain.py
```

### 5. 驗證大腦記憶庫 (Verify Brain)
```bash
# 驗證過濾和搜索功能
python verify_brain.py [<搜尋關鍵字>]

# 範例
python verify_brain.py
python verify_brain.py "LLM in healthcare"
python verify_brain.py "線蟲神經"
```

### 6. 清除大腦記憶庫 (Clear Database)
```bash
# 清除所有已存儲的論文記憶（需要確認）
python clear_brain_db.py
```

---

## 🤖 ML 大腦指令（cli.py）

### 7. 分類任務 (Classification)
```bash
# 執行分類任務
python -m Ares.cli --task classification [--data <資料集>] [--threshold <門檻>] [--memory <路徑>]

# 範例
python -m Ares.cli --task classification --data breast_cancer --threshold 0.85
```

### 8. 回歸任務 (Regression)
```bash
# 執行回歸任務
python -m Ares.cli --task regression [--data <資料集>] [--threshold <門檻>] [--memory <路徑>]

# 範例
python -m Ares.cli --task regression --data diabetes --threshold 0.80
```

**可用資料集：**
- `breast_cancer` (分類)
- `diabetes` (回歸)

---

## 🛠️ 工具指令

### 9. 建立測試資料 (Setup Data)
```bash
# 產生模擬銀行帳單 CSV 檔案
python setup_data.py
```

---

## 📊 指令參數說明

### Finance 模組參數
- `--file` (必填): 輸入的銀行 CSV 檔案路徑
- `--output` (選填): 輸出的 CSV 檔案路徑（預設：`tagged_<原檔名>`）

### Research 模組參數
- `--query` (必填): 搜尋關鍵字
- `--limit` (選填): 要處理的論文數量上限（預設：5）
- `--output` (選填): 輸出日報檔案路徑（預設：`Research_Daily_<日期>.md`）

### ML Brain 參數
- `--task` (必填): 任務類型（`classification` 或 `regression`）
- `--data` (選填): 資料集名稱（預設：`breast_cancer`）
- `--threshold` (選填): 模型召回門檻（預設：0.85）
- `--memory` (選填): 記憶檔案夾路徑（預設：`./brain_memory/`）

---

## 🎯 常用工作流程

### 每日研究報告
```bash
# 1. 搜尋並分析論文（自動存入大腦記憶庫）
python main.py research --query "LLM in healthcare" --limit 5

# 2. 驗證存入的論文
python verify_brain.py "LLM in healthcare"
```

### 財務分析
```bash
# 1. 產生測試資料（如果需要）
python setup_data.py

# 2. 處理銀行帳單
python main.py finance --file raw_bank_statement.csv
```

### 完整流程
```bash
# 執行所有模組
python main.py all
```

---

## 📝 注意事項

1. **環境變數**：確保 `.env` 檔案中包含必要的 API 金鑰：
   - `GEMINI_API_KEY` (用於研究模組的 AI 分析)
   - `GOOGLE_API_KEY` (用於向量資料庫嵌入)

2. **資料庫清除**：`clear_brain_db.py` 會永久刪除所有論文記憶，請謹慎使用

3. **論文分析**：只有成功分析的論文（score > 0 且無錯誤）才會存入大腦記憶庫

4. **瀏覽器模式**：研究模組預設使用無頭模式（headless=True），可在程式碼中修改

---

## 🔍 疑難排解

### 如果研究模組失敗
- 檢查網路連線（需要訪問 PubMed）
- 確認 Selenium WebDriver 已正確安裝
- 檢查 `.env` 檔案中的 `GEMINI_API_KEY`

### 如果大腦記憶庫異常
- 執行 `python clear_brain_db.py` 清除資料庫
- 檢查 `ares_knowledge_store` 目錄權限

### 如果財務模組失敗
- 確認 CSV 檔案格式正確（需包含 Date, Description, Amount 欄位）
- 檢查檔案路徑是否正確
