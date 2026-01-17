"""
研究編輯器模組

此模組提供論文審查與分析功能，使用 AI 評估研究論文的品質與創新點。
"""

import os
import json
import re
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


class ResearchEditor:
    """
    研究編輯器 - 使用 AI 審查與分析研究論文。
    
    此類別使用 Google Gemini AI 模型來分析論文標題與摘要，
    提供評分、摘要、創新點與閱讀建議。
    """
    
    def __init__(self):
        """
        初始化研究編輯器。
        
        載入環境變數並設定 LangChain Google Gemini API。如果缺少 API 金鑰，將拋出錯誤。
        
        Raises:
            ValueError: 如果環境變數中缺少 GEMINI_API_KEY。
        """
        # 載入環境變數
        load_dotenv()
        
        # 從環境變數取得 API 金鑰
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError('錯誤：環境變數中缺少 GEMINI_API_KEY，請在 .env 檔案中設定。')
        
        # 初始化 LangChain Google Gemini 模型（使用 gemini-flash-latest，temperature=0.2 以確保穩定性）
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-flash-latest",
            temperature=0.2,
            google_api_key=api_key
        )
    
    def review(self, paper: Dict[str, str]) -> Dict[str, Any]:
        """
        審查研究論文並提供分析結果。
        
        分析論文的標題與摘要，提供評分、摘要、創新點與閱讀建議。
        
        Args:
            paper: 包含論文資訊的字典，必須包含 'title' 和 'snippet' 鍵。
            
        Returns:
            Dict[str, any]: 包含以下鍵的字典：
                - 'score': 評分（1-10 的整數）
                - 'tldr': 一句話摘要（繁體中文）
                - 'innovation': 關鍵創新點（繁體中文）
                - 'recommendation': 閱讀建議（繁體中文）
                如果解析失敗，會包含 'error' 鍵。
        """
        # 驗證輸入
        if not isinstance(paper, dict):
            return self._get_default_response("輸入格式錯誤：必須是字典")
        
        title = paper.get('title', '').strip()
        snippet = paper.get('snippet', '').strip()
        
        # 處理摘要太短或為空的情況
        if not title:
            return self._get_default_response("論文標題為空")
        
        if not snippet or len(snippet) < 10:
            return self._get_default_response("論文摘要太短或為空，無法進行分析")
        
        # 構建提示詞
        prompt = f"""你是一位資深生醫研究員。請分析以下研究論文：

標題：{title}

摘要：{snippet}

請提供以下分析（使用繁體中文）：
1. 評分（1-10 分，10 分為最高）
2. 一句話摘要
3. 關鍵創新點
4. 閱讀建議（簡短說明為何值得閱讀或應該跳過）

**重要**：請嚴格以 JSON 格式回覆，不要使用 markdown 程式碼區塊（不要使用 ```json 或 ```）。
直接回覆純 JSON 字串，格式如下：
{{
    "score": <1-10 的整數>,
    "tldr": "<一句話摘要>",
    "innovation": "<關鍵創新點>",
    "recommendation": "<閱讀建議>"
}}"""
        
        try:
            # 呼叫 LLM
            response = self.llm.invoke(prompt)
            
            # 取得回應內容（處理多種可能的回應格式）
            if isinstance(response, list):
                # 如果回應是列表，取第一個元素
                first_item = response[0] if response else None
                if first_item is not None:
                    response_text = first_item.content if hasattr(first_item, 'content') else str(first_item)
                else:
                    response_text = ""
            elif hasattr(response, 'content'):
                response_text = response.content
            else:
                response_text = str(response)
            
            # 確保是字串類型
            if not isinstance(response_text, str):
                response_text = str(response_text)
            
            # 清理回應文字（移除可能的 markdown 格式）
            response_text = self._clean_json_response(response_text)
            
            # 調試：如果解析失敗，記錄原始回應（僅在開發時使用）
            if not response_text or response_text.strip() == "":
                return self._get_default_response("AI 回應為空")
            
            # 解析 JSON
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError as json_err:
                # 嘗試修復常見的 JSON 格式問題
                fixed_text = self._fix_json_format(response_text)
                try:
                    result = json.loads(fixed_text)
                except json.JSONDecodeError:
                    # 如果修復後仍然失敗，返回詳細錯誤
                    error_msg = f"JSON 解析失敗：{str(json_err)}。原始回應前 200 字元：{response_text[:200]}"
                    return self._get_default_response(error_msg)
            
            # 驗證結果格式
            if not isinstance(result, dict):
                return self._get_default_response("AI 回傳格式錯誤：不是字典")
            
            # 確保必要欄位存在
            required_keys = ['score', 'tldr', 'innovation', 'recommendation']
            for key in required_keys:
                if key not in result:
                    result[key] = "未提供"
            
            # 驗證 score 範圍
            if 'score' in result:
                try:
                    score = int(result['score'])
                    if score < 1:
                        result['score'] = 1
                    elif score > 10:
                        result['score'] = 10
                    else:
                        result['score'] = score
                except (ValueError, TypeError):
                    result['score'] = 5  # 預設值
            
            return result
            
        except json.JSONDecodeError as e:
            return self._get_default_response(f"JSON 解析失敗：{str(e)}")
        except Exception as e:
            return self._get_default_response(f"審查過程發生錯誤：{str(e)}")
    
    def _clean_json_response(self, text: str) -> str:
        """
        清理 AI 回應中的 JSON 字串，移除 markdown 格式。
        
        Args:
            text: 原始回應文字。
            
        Returns:
            str: 清理後的 JSON 字串。
        """
        # 確保輸入是字串類型
        if not isinstance(text, str):
            text = str(text)
        
        # 如果為空，返回空字串
        if not text:
            return "{}"
        
        try:
            # 移除 markdown 程式碼區塊標記
            text = re.sub(r'```json\s*', '', text)
            text = re.sub(r'```\s*', '', text)
            
            # 移除前後空白
            text = text.strip()
            
            # 如果文字以 { 開頭，找到最後一個 } 的位置
            start_idx = text.find('{')
            end_idx = text.rfind('}')
            
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                text = text[start_idx:end_idx + 1]
            
            return text
        except Exception as e:
            # 如果正則處理失敗，返回原始文字的字串表示
            return str(text)
    
    def _fix_json_format(self, text: str) -> str:
        """
        修復常見的 JSON 格式問題。
        
        Args:
            text: 可能有格式問題的 JSON 字串。
            
        Returns:
            str: 修復後的 JSON 字串。
        """
        if not isinstance(text, str):
            text = str(text)
        
        text = text.strip()
        
        # 修復 1: 移除開頭可能的 BOM 或特殊字元
        if text and text[0] not in ['{', '[']:
            # 找到第一個 { 或 [
            start_idx = max(text.find('{'), text.find('['))
            if start_idx > 0:
                text = text[start_idx:]
        
        # 修復 2: 將單引號改為雙引號（僅在 key 和值中）
        # 使用更智能的方法：逐字元解析並替換（簡化版）
        # 先處理鍵名：將 'key': 改為 "key":
        text = re.sub(r"'([^']+)'(\s*):", r'"\1"\2:', text)
        
        # 修復 3: 處理值中的單引號字串（但要注意避免替換字串內容中的單引號）
        # 這個比較複雜，我們使用簡單的替換：將 : 'value' 改為 : "value"
        # 但只替換不在雙引號內的單引號字串值
        def replace_single_quoted_values(match):
            # 匹配 : 'value' 或 , 'value' 的格式
            prefix = match.group(1)  # : 或 ,
            content = match.group(2)  # 值內容
            return f'{prefix}"{content}"'
        
        # 只替換簡單的單引號值（不在複雜嵌套中）
        text = re.sub(r'(:\s*|\,\s*)\'([^\']+)\'(\s*[,\}])', replace_single_quoted_values, text)
        
        # 修復 4: 提取完整的 JSON 物件（如果有多餘內容）
        start_idx = text.find('{')
        if start_idx != -1:
            # 計算大括號的層級，找到匹配的結束位置
            depth = 0
            in_string = False
            escape_next = False
            
            for i in range(start_idx, len(text)):
                char = text[i]
                
                if escape_next:
                    escape_next = False
                    continue
                
                if char == '\\':
                    escape_next = True
                    continue
                
                if char == '"':
                    in_string = not in_string
                    continue
                
                if not in_string:
                    if char == '{':
                        depth += 1
                    elif char == '}':
                        depth -= 1
                        if depth == 0:
                            return text[start_idx:i+1]
        
        return text
    
    def _get_default_response(self, error_message: str) -> Dict[str, any]:
        """
        取得預設回應字典（當發生錯誤時使用）。
        
        Args:
            error_message: 錯誤訊息。
            
        Returns:
            Dict[str, any]: 預設回應字典。
        """
        return {
            'score': 0,
            'tldr': '無法分析',
            'innovation': '無法分析',
            'recommendation': '無法提供建議',
            'error': error_message
        }
