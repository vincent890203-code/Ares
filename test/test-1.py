# ==========================================
# 1. 裝備武器 (Import Arsenal)
# ==========================================
# 因為你在 __init__.py 做了很好的封裝，所以可以直接從 Ares 引入所有功能
from Ares import (
    setup_driver,       # 啟動器
    safe_click,         # 戰術：安全點擊
    safe_type,          # 戰術：安全輸入 (這次沒用到，但可以備著)
    nuclear_scroll,     # 戰術：核彈捲動
    get_text,           # 提取：抓文字
    clean_text_basic    # 後勤：清洗資料
)
from selenium.webdriver.common.by import By
import time

# ==========================================
# 2. 部署戰場 (Deploy)
# ==========================================
print("Ares 系統啟動中...")

# 啟動瀏覽器
# headless=False: 讓你看得到瀏覽器畫面 (除錯用)
# off_screen=False: 讓視窗出現在螢幕上
driver = setup_driver(headless=True, off_screen=False)

try:
    target_url = "https://www.ptt.cc/bbs/Gossiping/index.html"
    print(f"鎖定目標: {target_url}")
    driver.get(target_url)

    # ==========================================
    # 3. 突破防線 (Breach Defenses)
    # ==========================================
    # PTT 會問「是否滿 18 歲」，我們要點擊 "yes" 按鈕
    # 按鈕的 name 屬性是 'yes'
    print(" 偵測到年齡驗證，正在嘗試突破...")
    
    # 使用你的 Ares 專屬函式：安全點擊
    # 它會自動等待按鈕出現、捲動到按鈕位置、然後點擊
    safe_click(driver, By.NAME, "yes")
    
    print("成功進入版面！")

    # ==========================================
    # 4. 戰術捲動 (Tactical Scroll)
    # ==========================================
    # 為了抓多一點資料，我們往下捲動幾次
    print("執行核彈級捲動...")
    nuclear_scroll(driver, times=2, wait=1)

    # ==========================================
    # 5. 獲取戰利品 (Looting)
    # ==========================================
    print("開始提取情報...")
    
    # 尋找所有文章標題區塊 (CSS Selector: div.r-ent)
    posts = driver.find_elements(By.CSS_SELECTOR, "div.r-ent")

    data_list = []

    for post in posts:
        # 在每個區塊內，分別尋找「標題」、「作者」、「日期」
        # 注意：這裡我們傳入 post (WebElement) 而不是 driver，縮小搜尋範圍
        # 但因為我們的 get_text 設計是傳入 driver，這裡我們先用簡單的方式示範
        
        # 為了示範 get_text 的威力，我們換個方式：
        # 我們直接抓出標題的元素
        try:
            # 這是原本 Selenium 的寫法，容易報錯
            title_elm = post.find_element(By.CSS_SELECTOR, "div.title a")
            raw_title = title_elm.text
            link = title_elm.get_attribute("href")
            
            # 使用你的 Utils 進行清洗
            clean_title = clean_text_basic(raw_title)
            
            print(f"   [發現] {clean_title}")
            print(f"      -> 連結: {link}")
            
        except:
            continue # 略過被刪除的文章

except Exception as e:
    print(f"任務發生意外: {e}")

finally:
    # ==========================================
    # 6. 撤退 (Retreat)
    # ==========================================
    print("任務結束，3秒後關閉武器...")
    time.sleep(3)
    driver.quit()