import os
from setuptools import setup, find_packages

# === 1. 設定專案資訊 ===
PACKAGE_NAME = "ares-system" # 套件在 pip list 顯示的名稱
VERSION = "0.5.0"
AUTHOR = "Yuan-Chen Kuo"
AUTHOR_EMAIL = "vincent890203@gmail.com" 
DESCRIPTION = "An automated, modularized ML pipeline for biomedical data mining."

# === 2. 自動讀取 requirements.txt ===
def parse_requirements(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, encoding='utf-8') as f:
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
    
    # 【關鍵修正】：顯式指定包含大寫 Ares 的所有子套件
    # 這樣可以避免 find_packages() 在某些環境下抓不到大寫資料夾的問題
    packages=find_packages(include=["Ares", "Ares.*"]),
    
    install_requires=parse_requirements("requirements.txt"),
    python_requires=">=3.9",

# 讓系統生成一個名為 'ares' 的可執行檔
    entry_points={
        'console_scripts': [
            'ares=Ares.cli:main', 
        ],
    },


    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)