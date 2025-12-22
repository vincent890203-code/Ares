from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from .core import retry  # 從同一資料夾的 core 引用 retry

@retry(times=3)
def safe_click(driver, by, value, timeout=10):
    """安全點擊"""
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.5) 
    element.click()

def safe_type(driver, by, value, text, timeout=10):
    """模擬真人輸入"""
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )
    element.clear()
    for char in str(text):
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))

def nuclear_scroll(driver, times=3, wait=1.5):
    """核彈級捲動"""
    js_scroll_all = """
        window.scrollTo(0, document.body.scrollHeight);
        var elements = document.querySelectorAll('*');
        for (var i = 0; i < elements.length; i++) {
            if (elements[i].scrollHeight > elements[i].clientHeight) {
                elements[i].scrollTop = elements[i].scrollHeight;
            }
        }
    """
    for _ in range(times):
        driver.execute_script(js_scroll_all)
        time.sleep(wait)