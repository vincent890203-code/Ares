from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def get_text(driver, by, value, timeout=5, default="Not Found"):
    """安全抓取文字"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element.text.strip()
    except:
        return default

def get_attribute(driver, by, value, attr_name, timeout=5):
    """抓取屬性"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element.get_attribute(attr_name)
    except:
        return None
    
def extract_list_by_pattern(items, pattern):
    """從清單中過濾符合正則表達式的項目"""
    results = []
    for item in items:
        # 嘗試取得 .text，如果沒有就直接轉字串
        text = item.text.strip() if hasattr(item, 'text') else str(item).strip()
        
        if re.search(pattern, text):
            results.append(text)
    return results