import pytest
from unittest.mock import MagicMock, patch
from selenium.webdriver.common.by import By

# 確保路徑大小寫正確 (Ares)
from Ares.spider.core import setup_driver
from Ares.spider.actions import safe_click, safe_type, nuclear_scroll

# ==========================================
# 1. 測試 Actions: safe_click
# ==========================================

@patch('Ares.spider.actions.WebDriverWait')
def test_safe_click_success(mock_wait):
    # 模擬 Driver 和 Element
    mock_driver = MagicMock()
    mock_element = MagicMock()
    
    # 模擬 WebDriverWait(...).until(...) 回傳我們的假元素
    mock_wait.return_value.until.return_value = mock_element
    
    # 執行：傳入正確的 3 個參數 (driver, by, value)
    safe_click(mock_driver, By.ID, "login_btn")
    
    # 驗證：
    # 1. 是否有呼叫 scrollIntoView 腳本
    mock_driver.execute_script.assert_called()
    # 2. 元素最終是否有被點擊
    mock_element.click.assert_called_once()

# ==========================================
# 2. 測試 Actions: safe_type
# ==========================================

@patch('Ares.spider.actions.WebDriverWait')
def test_safe_type_success(mock_wait):
    mock_driver = MagicMock()
    mock_element = MagicMock()
    mock_wait.return_value.until.return_value = mock_element
    
    # 執行：傳入正確的 4 個參數 (driver, by, value, text)
    test_text = "Ares123"
    safe_type(mock_driver, By.NAME, "username", test_text)
    
    # 驗證：
    # 1. 是否有先清空輸入框
    mock_element.clear.assert_called_once()
    # 2. 檢查 send_keys 被呼叫的次數是否等於字串長度 (因為您是用 for 迴圈逐字輸入)
    assert mock_element.send_keys.call_count == len(test_text)

# ==========================================
# 3. 測試 Actions: nuclear_scroll
# ==========================================

def test_nuclear_scroll():
    mock_driver = MagicMock()
    
    # 執行：捲動 2 次
    nuclear_scroll(mock_driver, times=2, wait=0.1)
    
    # 驗證 execute_script 是否被呼叫了 2 次
    assert mock_driver.execute_script.call_count == 2

# ==========================================
# 4. 測試 Core: setup_driver (Mock 掉重裝瀏覽器的過程)
# ==========================================

@patch('Ares.spider.core.webdriver.Chrome')
@patch('Ares.spider.core.Service')
@patch('Ares.spider.core.ChromeDriverManager')
def test_setup_driver_logic(mock_manager, mock_service, mock_chrome):
    driver = setup_driver(headless=True)
    assert driver is not None
    mock_chrome.assert_called_once()