from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from functools import wraps
import time

def setup_driver(headless=False, off_screen=True, load_images=True):
    """通用瀏覽器啟動器"""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--start-maximized")
    
    if off_screen:
        options.add_argument("--window-position=-10000,0")
    if headless:
        options.add_argument("--headless=new")
    if not load_images:
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def retry(times=3, delay=2):
    """重試裝飾器"""
    def decorator(func): 
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[Retry {i+1}/{times}] {func.__name__} 發生錯誤: {e}")
                    time.sleep(delay)
            print(f"{func.__name__} 最終失敗")
            return None
        return wrapper
    return decorator