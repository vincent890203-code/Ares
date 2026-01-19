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
            response_text = None
            
            # 情況 1: 回應是字典格式 {'type': 'text', 'text': '...'}
            if isinstance(response, dict):
                if 'text' in response:
                    response_text = response['text']
                elif 'content' in response:
                    response_text = response['content']
                else:
                    # 如果字典中沒有 text 或 content，嘗試轉為字串並提取 JSON
                    response_str = str(response)
                    # 檢查是否是字典的字符串表示，嘗試提取內部的 text 值
                    if "'text'" in response_str or '"text"' in response_str:
                        # 使用正則提取 text 字段的值
                        match = re.search(r'["\']text["\']\s*:\s*["\']([^"\']+)["\']', response_str)
                        if match:
                            response_text = match.group(1)
                        else:
                            response_text = response_str
                    else:
                        response_text = response_str
            # 情況 2: 回應是列表
            elif isinstance(response, list):
                # 如果回應是列表，取第一個元素
                first_item = response[0] if response else None
                if first_item is not None:
                    # 檢查第一個元素是否為字典
                    if isinstance(first_item, dict):
                        response_text = first_item.get('text') or first_item.get('content')
                        if not response_text:
                            response_text = str(first_item)
                    elif hasattr(first_item, 'content'):
                        content = first_item.content
                        # 如果 content 是字典，提取 text
                        if isinstance(content, dict):
                            response_text = content.get('text') or str(content)
                        else:
                            response_text = content
                    else:
                        response_text = str(first_item)
                else:
                    response_text = ""
            # 情況 3: 回應有 content 屬性
            elif hasattr(response, 'content'):
                content = response.content
                # 如果 content 是字典，提取 text
                if isinstance(content, dict):
                    response_text = content.get('text') or str(content)
                else:
                    response_text = content
            # 情況 4: 回應是字符串（可能是字典的字符串表示）
            elif isinstance(response, str):
                # 檢查是否是字典的字符串表示
                if response.strip().startswith('{') or response.strip().startswith("{"):
                    # 嘗試解析為字典
                    try:
                        parsed = eval(response)  # 小心使用 eval，但在這裡是安全的
                        if isinstance(parsed, dict) and 'text' in parsed:
                            response_text = parsed['text']
                        else:
                            response_text = response
                    except:
                        # 如果解析失敗，嘗試用正則提取
                        match = re.search(r'["\']text["\']\s*:\s*["\']([^"\']+)["\']', response)
                        if match:
                            response_text = match.group(1)
                        else:
                            response_text = response
                else:
                    response_text = response
            # 情況 5: 其他格式，轉為字串
            else:
                response_text = str(response)
            
            # 確保是字串類型
            if not isinstance(response_text, str):
                response_text = str(response_text)
            
            # 特殊處理：如果 response_text 看起來像是字典的字符串表示，嘗試提取 text 字段
            if response_text.strip().startswith("{'type':") or response_text.strip().startswith('{"type":') or "'text'" in response_text or '"text"' in response_text:
                try:
                    # 首先嘗試用 ast.literal_eval 安全地解析 Python 字面量
                    import ast
                    parsed_dict = ast.literal_eval(response_text)
                    if isinstance(parsed_dict, dict) and 'text' in parsed_dict:
                        response_text = parsed_dict['text']
                        # 確保提取的是字串
                        if not isinstance(response_text, str):
                            response_text = str(response_text)
                except (ValueError, SyntaxError):
                    # 如果 ast.literal_eval 失敗，使用正則提取
                    # 優先匹配雙引號格式 "text": "{...}"
                    # 匹配 "text": "..." 或 'text': '...'，支持多行和嵌套 JSON
                    # 先嘗試匹配雙引號格式（更常見）
                    pattern1 = r'["\']text["\']\s*:\s*"((?:[^"\\]|\\.|\\n)*)"'
                    text_match = re.search(pattern1, response_text, re.DOTALL)
                    
                    if not text_match:
                        # 嘗試匹配單引號格式
                        pattern2 = r'["\']text["\']\s*:\s*\'((?:[^\'\\]|\\.|\\n)*)\''
                        text_match = re.search(pattern2, response_text, re.DOTALL)
                    
                    if not text_match:
                        # 嘗試更寬鬆的模式：匹配到第一個引號到最後一個引號之間的所有內容
                        # 這用於處理嵌套的 JSON 字串
                        pattern3 = r'["\']text["\']\s*:\s*["\']((?:[^"\']|\\["\']|\\n)+?)["\']'
                        text_match = re.search(pattern3, response_text, re.DOTALL)
                    
                    if text_match:
                        response_text = text_match.group(1)
                        # 移除可能的轉義字符
                        response_text = response_text.replace('\\n', '\n').replace("\\'", "'").replace('\\"', '"')
                    else:
                        # 如果正則也失敗，嘗試直接查找 JSON 對象（以 { 開頭的部分）
                        json_start = response_text.find('{"')
                        if json_start == -1:
                            json_start = response_text.find("{'")
                        if json_start != -1:
                            # 找到最後一個 } 的位置
                            json_end = response_text.rfind('}')
                            if json_end > json_start:
                                response_text = response_text[json_start:json_end+1]
            
            # 清理回應文字（移除可能的 markdown 格式）
            response_text = self._clean_json_response(response_text)
            
            # 調試：如果解析失敗，記錄原始回應（僅在開發時使用）
            if not response_text or response_text.strip() == "":
                return self._get_default_response("AI 回應為空")
            
            # 如果 response_text 仍然包含 Python 字典格式（如 {'type': 'text', 'text': '...'}），再次嘗試提取
            if (response_text.strip().startswith("{'") or response_text.strip().startswith('{"')) and ('"text"' in response_text or "'text'" in response_text):
                # 檢查是否包含嵌套的 JSON（text 字段的值是 JSON 字串）
                try:
                    import ast
                    parsed = ast.literal_eval(response_text)
                    if isinstance(parsed, dict) and 'text' in parsed:
                        inner_text = parsed['text']
                        if isinstance(inner_text, str) and (inner_text.strip().startswith('{') or inner_text.strip().startswith('[')):
                            response_text = inner_text
                except:
                    # 使用正則提取內部的 JSON
                    # 尋找 "text": "{" 或 'text': '{' 後面的內容
                    pattern = r'["\']text["\']\s*:\s*["\']?(\{.*\})["\']?'
                    match = re.search(pattern, response_text, re.DOTALL)
                    if match:
                        potential_json = match.group(1)
                        # 嘗試找到完整的 JSON 對象
                        brace_count = 0
                        json_end = -1
                        for i, char in enumerate(potential_json):
                            if char == '{':
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    json_end = i + 1
                                    break
                        if json_end > 0:
                            response_text = potential_json[:json_end]
            
            # 解析 JSON
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError as json_err:
                # 嘗試修復常見的 JSON 格式問題
                fixed_text = self._fix_json_format(response_text)
                try:
                    result = json.loads(fixed_text)
                except json.JSONDecodeError as json_err2:
                    # 如果修復後仍然失敗，嘗試更激進的修復
                    # 提取第一個完整的 JSON 對象
                    json_start = fixed_text.find('{')
                    if json_start != -1:
                        # 找到匹配的結束括號
                        brace_count = 0
                        json_end = -1
                        for i in range(json_start, len(fixed_text)):
                            if fixed_text[i] == '{':
                                brace_count += 1
                            elif fixed_text[i] == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    json_end = i + 1
                                    break
                        if json_end > json_start:
                            try:
                                result = json.loads(fixed_text[json_start:json_end])
                            except:
                                # 如果還是失敗，返回詳細錯誤
                                error_msg = f"JSON 解析失敗：{str(json_err2)}。原始回應前 300 字元：{response_text[:300]}"
                                return self._get_default_response(error_msg)
                    else:
                        # 如果修復後仍然失敗，返回詳細錯誤
                        error_msg = f"JSON 解析失敗：{str(json_err2)}。原始回應前 300 字元：{response_text[:300]}"
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
