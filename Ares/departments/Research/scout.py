"""
研究偵察器模組

此模組提供研究與情報搜集的核心功能。
"""

from typing import List, Dict
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

from Ares.spider.core import setup_driver


class ResearchScout:
    """
    研究偵察器 - 負責研究與情報搜集任務。
    
    此類別將被實作用於執行各種研究與情報搜集操作。
    """
    
    def __init__(self):
        """初始化研究偵察器。"""
        pass


class PubMedScout:
    """
    PubMed 偵察器 - 從 PubMed 資料庫搜尋並提取研究論文資訊。
    
    此類別使用 Selenium 自動化瀏覽器操作，從 PubMed 網站搜尋論文，
    並提取標題、連結與摘要資訊。
    """
    
    def __init__(self, headless: bool = True):
        """
        初始化 PubMed 偵察器。
        
        Args:
            headless: 是否使用無頭模式執行瀏覽器。預設為 True。
        """
        self.driver = None
        self.headless = headless
        try:
            self.driver = setup_driver(headless=headless)
        except Exception as e:
            raise RuntimeError(f"無法初始化瀏覽器驅動程式：{str(e)}") from e
    
    def search(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        在 PubMed 上搜尋論文並提取結果。
        
        Args:
            query: 搜尋關鍵字。
            limit: 要提取的結果數量上限。預設為 5。
            
        Returns:
            List[Dict[str, str]]: 包含論文資訊的字典列表，每個字典包含：
                - 'title': 論文標題
                - 'link': 論文連結
                - 'snippet': 摘要片段（如果可見）
                
        Raises:
            RuntimeError: 當搜尋過程發生錯誤時。
        """
        if not self.driver:
            raise RuntimeError("瀏覽器驅動程式未初始化")
        
        results = []
        
        try:
            # 步驟 1: 前往 PubMed 首頁
            print(f"正在前往 PubMed 網站...")
            self.driver.get("https://pubmed.ncbi.nlm.nih.gov/")
            time.sleep(2)  # 等待頁面載入
            
            # 確認頁面已載入
            page_title = self.driver.title
            print(f"頁面標題：{page_title}")
            
            # 步驟 2: 找到搜尋框並輸入查詢（使用多種選擇器策略）
            print(f"正在尋找搜尋框並輸入關鍵字：{query}")
            search_box = None
            
            # 嘗試多種可能的搜尋框選擇器
            selectors = [
                (By.ID, "id_term"),
                (By.NAME, "term"),
                (By.CSS_SELECTOR, "input[name='term']"),
                (By.CSS_SELECTOR, "input[id='id_term']"),
                (By.CSS_SELECTOR, "input[type='search']"),
                (By.CSS_SELECTOR, "input[placeholder*='Search']"),
                (By.CSS_SELECTOR, "#search-input"),
            ]
            
            for by, value in selectors:
                try:
                    search_box = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((by, value))
                    )
                    print(f"成功找到搜尋框（使用選擇器：{by}={value}）")
                    break
                except TimeoutException:
                    continue
            
            if not search_box:
                # 如果所有選擇器都失敗，截圖並拋出錯誤
                self.driver.save_screenshot('debug_error.png')
                raise RuntimeError("無法找到搜尋框，已儲存截圖至 debug_error.png")
            
            search_box.clear()
            search_box.send_keys(query)
            time.sleep(1)
            
            # 步驟 3: 點擊搜尋按鈕或按 Enter
            print("正在執行搜尋...")
            try:
                # 嘗試找到搜尋按鈕
                search_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.search-btn, input[type='submit'], button[type='submit']"))
                )
                search_button.click()
            except TimeoutException:
                # 如果找不到按鈕，嘗試按 Enter
                search_box.send_keys(Keys.RETURN)
            
            # 步驟 4: 等待結果載入
            print("等待搜尋結果載入...")
            try:
                # 嘗試多種可能的結果選擇器
                WebDriverWait(self.driver, 15).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".results-article")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "article.full-docsum")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".docsum-content")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#search-results"))
                    )
                )
            except TimeoutException:
                # 如果找不到特定元素，至少等待頁面載入
                time.sleep(3)
            time.sleep(2)  # 額外等待確保內容完全載入
            
            # 步驟 5: 解析結果頁面
            print(f"正在提取前 {limit} 筆結果...")
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # 尋找結果項目（PubMed 的結果通常包含在特定類別中）
            result_items = soup.find_all('article', class_='full-docsum', limit=limit)
            
            if not result_items:
                # 嘗試其他可能的選擇器
                result_items = soup.find_all('div', class_='docsum-content', limit=limit)
            
            for item in result_items:
                try:
                    # 提取標題
                    title_elem = item.find('a', class_='docsum-title')
                    if not title_elem:
                        title_elem = item.find('a', href=True)
                    
                    title = title_elem.get_text(strip=True) if title_elem else "無標題"
                    
                    # 提取連結
                    if title_elem and title_elem.get('href'):
                        link = title_elem['href']
                        if not link.startswith('http'):
                            link = f"https://pubmed.ncbi.nlm.nih.gov{link}"
                    else:
                        link = ""
                    
                    # 提取摘要片段
                    snippet_elem = item.find('div', class_='full-view-snippet')
                    if not snippet_elem:
                        snippet_elem = item.find('p', class_='docsum-snippet')
                    if not snippet_elem:
                        snippet_elem = item.find('div', class_='snippet')
                    
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else "無摘要"
                    
                    results.append({
                        'title': title,
                        'link': link,
                        'snippet': snippet
                    })
                    
                except Exception as e:
                    print(f"警告：提取結果時發生錯誤：{str(e)}")
                    continue
            
            print(f"成功提取 {len(results)} 筆結果")
            return results
            
        except TimeoutException as e:
            # 儲存截圖以便調試
            try:
                self.driver.save_screenshot('debug_error.png')
                print("已儲存錯誤截圖至 debug_error.png")
            except Exception as screenshot_error:
                print(f"無法儲存截圖：{screenshot_error}")
            raise RuntimeError(f"搜尋超時：{str(e)}") from e
        except Exception as e:
            # 儲存截圖以便調試
            try:
                self.driver.save_screenshot('debug_error.png')
                print("已儲存錯誤截圖至 debug_error.png")
            except Exception as screenshot_error:
                print(f"無法儲存截圖：{screenshot_error}")
            raise RuntimeError(f"搜尋過程發生錯誤：{str(e)}") from e
    
    def close(self):
        """
        關閉瀏覽器驅動程式。
        
        此方法應在完成所有操作後呼叫，以釋放資源。
        """
        if self.driver:
            try:
                self.driver.quit()
                print("瀏覽器已關閉")
            except Exception as e:
                print(f"關閉瀏覽器時發生錯誤：{str(e)}")
            finally:
                self.driver = None
    
    def __enter__(self):
        """支援 context manager 的進入方法。"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """支援 context manager 的退出方法，確保瀏覽器關閉。"""
        self.close()
