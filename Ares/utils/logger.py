import logging
import sys
from datetime import datetime
import warnings
import os

# 1. 忽略 Scikit-learn 常見的語法警告 (FutureWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

# 2. 忽略模型未收斂的警告 (ConvergenceWarning)
# 這在壓力測試或隨機數據中很常見，不影響功能
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)

# 3. 選填：禁止部分底層庫輸出雜訊
os.environ['PYTHONWARNINGS'] = 'ignore'

# 定義顏色 (ANSI Escape Codes)
class LogColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def setup_ares_logger(name="ARES"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 避免重複添加 Handler
    if not logger.handlers:
        # 1. 終端機彩色輸出
        c_handler = logging.StreamHandler(sys.stdout)
        c_format = logging.Formatter(
            f"{LogColors.BLUE}[%(asctime)s]{LogColors.ENDC} %(levelname)s: %(message)s",
            datefmt="%H:%M:%S"
        )
        c_handler.setFormatter(c_format)
        logger.addHandler(c_handler)

        # 2. 檔案紀錄 (用於壓力測試分析)
        f_handler = logging.FileHandler("ares_operation.log", encoding='utf-8')
        f_format = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s: %(message)s")
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)

    return logger

# 實例化全域 logger
ares_logger = setup_ares_logger()