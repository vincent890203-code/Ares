import sys
import os
import time
from selenium.webdriver.common.by import By

# 確保 Python 找得到 Ares 套件
sys.path.append(os.getcwd())

# 從您的 core.py 載入武器
from Ares.spider.core import setup_driver, retry

# --- 測試 1: 驗證 Retry 機制 (模擬網路不穩) ---
print("\n🔥 [Test 1] Testing Retry Mechanism (韌性測試)...")

# 故意製造一個會失敗的函數
class NetworkFlake:
    def __init__(self):
        self.attempts = 0

    @retry(times=3, delay=1)  # 使用您的裝飾器
    def unstable_request(self):
        self.attempts += 1
        print(f"   -> 嘗試連線第 {self.attempts} 次...")
        if self.attempts < 3:
            raise ConnectionError("模擬網路斷線！")
        print("   -> ✅ 第三次連線成功！")
        return "Success"

try:
    tester = NetworkFlake()
    tester.unstable_request()
    print("✅ Retry 機制運作正常：它救回了失敗的請求。")
except Exception as e:
    print(f"❌ Retry 機制失效: {e}")

# --- 測試 2: 驗證反偵測瀏覽器 (真實連線) ---
print("\n🔥 [Test 2] Testing Stealth Browser (隱匿測試)...")

# 使用您的 setup_driver 啟動瀏覽器
# 我們先設 headless=False 讓您親眼看到瀏覽器跳出來 (更有感)
driver = setup_driver(headless=False, off_screen=False, load_images=True)

try:
    target_url = "https://www.google.com"
    print(f"   -> 正在前往: {target_url}")
    driver.get(target_url)
    
    # 檢查是否成功拿到標題
    title = driver.title
    print(f"   -> 網站標題: {title}")
    
    if "Google" in title:
        print("✅ 瀏覽器偽裝成功！成功存取目標網站。")
    else:
        print("⚠️ 警告：標題不如預期，可能被重導向。")
        
    time.sleep(2) # 停兩秒讓您看一下

except Exception as e:
    print(f"❌ 瀏覽器測試失敗: {e}")

finally:
    driver.quit()
    print("🛑 測試結束，瀏覽器已關閉。")