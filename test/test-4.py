# 你看！現在可以直接從 Ares 拿東西，不用打 Ares.spider.core...
from Ares import setup_driver, BioCleaner, ML_Brain

print("成功匯入 setup_driver")
print("成功匯入 BioCleaner")
print("成功匯入 ML_Brain")

# 測試一下是不是真的能用
try:
    cleaner = BioCleaner()
    print("Ares 系統架構正常！")
except Exception as e:
    print(f"出錯了: {e}")