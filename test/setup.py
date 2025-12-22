from setuptools import setup, find_packages

setup(
    name="ares",           # 套件名稱 (pip install 時用的名字)
    version="0.1.0",               # 版本號
    author="Yuan-Chen Kuo",            # 名字
    description="A personalized web scraping toolkit aiming for Google-level quality.",
    packages=find_packages(),      # 自動尋找含有 __init__.py 的資料夾
    install_requires=[             # 自動安裝依賴套件
        "selenium>=4.10.0",
        "webdriver-manager",
        "beautifulsoup4"
    ],
    python_requires=">=3.8",       # 限制 Python 版本
)