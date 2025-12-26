# 使用官方 Python 輕量版作為基底
FROM python:3.9-slim

# 安裝 Chrome 與相關依賴（這是執行 Spider 必備的）
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製專案檔案
COPY . .

# 安裝相依套件並以可編輯模式安裝 Ares
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

# 設定執行入口：預設執行全端整合測試
CMD ["python", "tests/full_pipeline_test.py"]