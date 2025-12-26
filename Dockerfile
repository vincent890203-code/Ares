# 1. 基底映像檔：使用官方 Python 3.9 的輕量版 (slim)
# 這就像是我們去買了一台已經灌好 Python 的乾淨電腦
FROM python:3.9-slim

# 2. 設定工作目錄
# 在容器裡面建立一個叫 /app 的資料夾，並切換進去
WORKDIR /app

# 3. 複製檔案
# 把您電腦目前目錄下的所有東西 (除了 .dockerignore 寫的) 複製到容器的 /app
COPY . /app

# 4. 安裝依賴與專案
# 執行 pip install . 會讀取 setup.py，自動安裝 numpy, pandas, scikit-learn 等套件
# --no-cache-dir 可以讓做出來的映像檔比較小
RUN pip install --no-cache-dir .

# 5. 設定進入點 (Entrypoint)
# 這讓容器變身為一個執行檔。當容器啟動時，直接執行 'ares' 指令
ENTRYPOINT ["ares"]

# 6. 預設參數
# 如果使用者啟動容器時沒給參數，預設執行 --help
CMD ["--help"]