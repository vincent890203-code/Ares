import os
from setuptools import setup, find_packages

# === 1. 設定專案資訊 (請修改這裡) ===
PACKAGE_NAME = "ares"
VERSION = "0.1.0"
AUTHOR = "Yuan-Chen Kuo"
AUTHOR_EMAIL = "vincent890203@gmail.com" 
DESCRIPTION = "An automated, modularized ML pipeline for biomedical data mining."

# === 2. 自動讀取 requirements.txt 的魔法函式 ===
# 這樣您就不需要手動在 setup.py 裡重複寫一遍依賴套件
def parse_requirements(filename):
    """讀取 requirements.txt 並回傳依賴清單"""
    if not os.path.exists(filename):
        return []
    
    with open(filename, encoding='utf-8') as f:
        # 過濾掉空行和註解 (# 開頭)
        return [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith("#")
        ]

# === 3. 主設定 ===
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    
    # 自動尋找所有包含 __init__.py 的資料夾 (也就是 ares, ares.spider...)
    packages=find_packages(),
    
    # 自動讀取依賴
    install_requires=parse_requirements("requirements.txt"),
    
    # 指定 Python 版本
    python_requires=">=3.9",
    
    # 這是為了讓別人知道這個套件的分類 (PyPI Trove Classifiers)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)