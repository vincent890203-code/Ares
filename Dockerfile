# 使用官方 Python 輕量版作為基底
FROM python:3.9-slim

# 安裝 Chrome 與相關依賴
# 修正說明：改用 gpg --dearmor 取代已廢棄的 apt-key，並將金鑰存入 keyrings
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl \
    && mkdir -p /etc/apt/keyrings \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製專案檔案
COPY . .

# 安裝相依套件並以可編輯模式安裝 Ares
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .
# 加裝 pytest (為了確保容器內也能跑測試)
RUN pip install pytest pytest-cov

# 設定執行入口：改用 pytest 來執行，這樣跟 GitHub CI 行為一致
CMD ["pytest", "tests/full_pipeline_test.py"]