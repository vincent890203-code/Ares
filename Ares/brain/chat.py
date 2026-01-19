"""
Ares 聊天機器人模組

整合大腦記憶庫（Hippocampus）與 LLM，實現基於知識庫的問答功能
"""
import os
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from Ares.brain.memory import KnowledgeBase

# 載入環境變數
load_dotenv()


class AresChatbot:
    """
    Ares 聊天機器人 - 整合長期記憶與 LLM 的智能助手
    
    使用向量資料庫檢索相關論文，並結合 LLM 生成回答
    """
    
    def __init__(self):
        """
        初始化聊天機器人
        
        - 初始化大腦記憶庫（KnowledgeBase）作為長期記憶
        - 初始化 LLM（ChatGoogleGenerativeAI）作為語音輸出
        
        Raises:
            ValueError: 如果環境變數中缺少 GEMINI_API_KEY。
        """
        # 載入環境變數
        load_dotenv()
        
        # 從環境變數取得 API 金鑰
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError('錯誤：環境變數中缺少 GEMINI_API_KEY，請在 .env 檔案中設定。')
        
        # 大腦記憶庫（長期記憶）
        self.brain = KnowledgeBase()
        
        # LLM（語音輸出）
        # 使用 gemini-flash-latest，與其他模組保持一致
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-flash-latest",
            temperature=0.7,
            google_api_key=api_key
        )
    
    def chat(self, user_query: str, filter_tag: str = None):
        """
        與用戶對話，基於知識庫回答問題
        
        Args:
            user_query: 用戶的問題
            filter_tag: 可選的分類標籤過濾器，用於限制搜索範圍
        
        Returns:
            str: LLM 生成的回答（繁體中文）
        """
        # 步驟 1: Recall - 從記憶庫中檢索相關論文
        memories = self.brain.recall(user_query, k=3, filter_tag=filter_tag)
        
        # 步驟 2: Context Construction - 構建上下文
        if not memories:
            # 如果沒有找到任何記憶，返回提示訊息
            return "我腦中沒有相關記憶，請先派我去 Research 抓取資料。"
        
        # 將檢索到的文件內容組合成上下文字串，並保存引用資訊
        context_parts = []
        references = []  # 用於保存引用資訊
        
        for i, doc in enumerate(memories, 1):
            title = doc.metadata.get('Title', '未知標題')
            link = doc.metadata.get('Link', '')
            content = doc.page_content
            # 將內容分段，以便後續標註具體段落
            content_lines = content.split('\n')
            context_parts.append(f"[論文 {i}] {title}\n{content}")
            
            # 保存引用資訊
            references.append({
                'id': i,
                'title': title,
                'link': link,
                'content': content,
                'content_lines': content_lines
            })
        
        context_str = "\n\n".join(context_parts)
        
        # 步驟 3: Prompting - 創建提示詞
        prompt = f"""請根據以下檢索到的論文內容直接回答用戶的問題。

**回答格式要求：**
1. 直接回答問題，不要自我介紹或開場白
2. 回答開頭應該是「根據記憶庫中的資料」或「根據檢索到的論文」
3. 回答中的每一個結論或事實都必須使用引用格式 [論文編號]，例如 [1]、[2] 等
4. 如果某個結論來自多篇論文，請使用 [1,2] 的格式
5. 請務必使用繁體中文回答，避免使用簡體中文或英文
6. 如果答案不在上下文中，請明確說明「根據記憶庫中的資料，我無法找到相關資訊」

上下文內容（來自記憶庫）：
{context_str}

問題：{user_query}

請直接回答問題（不要說「我是 Ares」或類似開場白）："""
        
        # 步驟 4: Generate - 調用 LLM 生成回答
        try:
            response = self.llm.invoke(prompt)
            
            # 提取回應內容（只提取純文字，完全忽略技術細節）
            response_text = None
            
            # 情況 1: 回應是列表格式 [{'type': 'text', 'text': '...', 'extras': {...}}]
            # 這是最常見的格式，優先處理
            if isinstance(response, list) and len(response) > 0:
                # 遍歷列表，尋找包含 'text' 的字典
                for item in response:
                    if isinstance(item, dict):
                        # 只提取 'text' 欄位，完全忽略 'extras'、'type' 等其他欄位
                        text_value = item.get('text')
                        if text_value is not None:
                            # 如果 text_value 是字符串，直接使用（這是我們想要的）
                            if isinstance(text_value, str):
                                response_text = text_value
                                break
                            # 如果 text_value 是其他類型，轉為字符串
                            elif text_value:
                                response_text = str(text_value)
                                break
                    # 如果列表元素有 content 或 text 屬性
                    elif hasattr(item, 'content'):
                        content = item.content
                        # 如果 content 是字符串，直接使用
                        if isinstance(content, str):
                            response_text = content
                            break
                        # 如果 content 是列表，遞迴處理
                        elif isinstance(content, list) and len(content) > 0:
                            for sub_item in content:
                                if isinstance(sub_item, dict) and 'text' in sub_item:
                                    response_text = sub_item['text']
                                    break
                            if response_text:
                                break
                    elif hasattr(item, 'text'):
                        text_attr = item.text
                        if isinstance(text_attr, str):
                            response_text = text_attr
                            break
                
                # 如果列表處理後仍沒有找到文字，嘗試第一個元素的其他屬性
                if not response_text and len(response) > 0:
                    first_item = response[0]
                    if hasattr(first_item, 'content'):
                        content = first_item.content
                        if isinstance(content, str):
                            response_text = content
                        elif isinstance(content, list) and len(content) > 0:
                            for sub_item in content:
                                if isinstance(sub_item, dict) and 'text' in sub_item:
                                    response_text = sub_item['text']
                                    break
                    elif hasattr(first_item, 'text'):
                        response_text = first_item.text
                    # 最後手段：轉為字符串（但這不應該發生）
                    if not response_text:
                        response_text = "無法解析回應格式"
            
            # 情況 2: 回應有 content 屬性
            elif hasattr(response, 'content'):
                content = response.content
                # 如果 content 是列表，遞迴處理
                if isinstance(content, list) and len(content) > 0:
                    for item in content:
                        if isinstance(item, dict) and 'text' in item:
                            response_text = item['text']
                            break
                        elif isinstance(item, str):
                            response_text = item
                            break
                # 如果 content 是字典，提取 text
                elif isinstance(content, dict):
                    response_text = content.get('text')
                # 如果 content 是字符串，直接使用
                elif isinstance(content, str):
                    response_text = content
                else:
                    response_text = str(content)
            
            # 情況 3: 回應有 text 屬性
            elif hasattr(response, 'text'):
                response_text = response.text
            
            # 情況 4: 回應是字典格式
            elif isinstance(response, dict):
                # 只提取 'text' 欄位，忽略其他所有欄位（包括 'extras'）
                response_text = response.get('text') or response.get('content')
            
            # 情況 5: 回應是字串
            elif isinstance(response, str):
                response_text = response
            
            # 情況 6: 其他格式，轉為字串
            else:
                response_text = str(response)
            
            # 確保是字串類型
            if not isinstance(response_text, str):
                response_text = str(response_text)
            
            # 特殊處理：如果 response_text 看起來像是字典的字符串表示，嘗試提取 text 字段
            # 這處理類似 {'type': 'text', 'text': '...', 'extras': {...}} 的格式
            # 但首先檢查是否包含 'extras'，如果包含則說明可能是整個字典的字符串表示
            if response_text and (
                "'extras'" in response_text or 
                '"extras"' in response_text or
                response_text.strip().startswith("{'type':") or 
                response_text.strip().startswith('{"type":') or 
                ("'text'" in response_text and "'extras'" in response_text) or
                ('"text"' in response_text and '"extras"' in response_text)
            ):
                try:
                    import ast
                    # 嘗試解析為 Python 字典
                    parsed_dict = ast.literal_eval(response_text)
                    if isinstance(parsed_dict, dict) and 'text' in parsed_dict:
                        response_text = parsed_dict['text']
                        if not isinstance(response_text, str):
                            response_text = str(response_text)
                except (ValueError, SyntaxError):
                    # 如果 ast.literal_eval 失敗，使用正則提取
                    import re
                    # 優先匹配雙引號格式 "text": "..."
                    pattern1 = r'["\']text["\']\s*:\s*"((?:[^"\\]|\\.|\\n)*)"'
                    text_match = re.search(pattern1, response_text, re.DOTALL)
                    
                    if not text_match:
                        # 嘗試匹配單引號格式
                        pattern2 = r'["\']text["\']\s*:\s*\'((?:[^\'\\]|\\.|\\n)*)\''
                        text_match = re.search(pattern2, response_text, re.DOTALL)
                    
                    if not text_match:
                        # 嘗試更寬鬆的模式（匹配到第一個 'extras' 或結尾）
                        pattern3 = r'["\']text["\']\s*:\s*["\']((?:[^"\']|\\["\']|\\n)+?)(?:["\']\s*,\s*["\']extras["\']|["\']\s*[,}])'
                        text_match = re.search(pattern3, response_text, re.DOTALL)
                    
                    if text_match:
                        response_text = text_match.group(1)
                        # 移除可能的轉義字符
                        response_text = response_text.replace('\\n', '\n').replace("\\'", "'").replace('\\"', '"')
            
            # 清理回應文字（移除多餘的空白和格式）
            if response_text:
                response_text = response_text.strip()
                
                # 移除或替換不想要的開場白
                unwanted_prefixes = [
                    "我是 Ares，",
                    "我是 Ares ",
                    "Ares 是",
                    "根據我的理解，",
                    "作為一位先進的 AI 研究助理，",
                    "作為 AI 研究助理，",
                ]
                
                for prefix in unwanted_prefixes:
                    if response_text.startswith(prefix):
                        response_text = response_text[len(prefix):].strip()
                        break
                
                # 如果回答開頭不是「根據記憶庫」或「根據檢索」，添加前綴
                if not response_text.startswith(("根據記憶庫", "根據檢索", "根據以下", "記憶庫中的資料")):
                    # 檢查是否包含「根據」開頭的句子，如果沒有則添加
                    if not re.match(r'^根據', response_text):
                        response_text = "根據記憶庫中的資料，" + response_text
            
            # 最終檢查：確保 response_text 不包含技術細節（如 'extras'、'signature' 等）
            if response_text and (
                "'extras'" in response_text or 
                '"extras"' in response_text or
                "'signature'" in response_text or
                '"signature"' in response_text or
                response_text.startswith("[{") or
                response_text.startswith("[{'")
            ):
                # 如果仍然包含技術細節，嘗試最後一次提取
                import re
                # 嘗試提取最長的純文字段落（不包含字典結構）
                # 匹配從 'text': '...' 到 'extras' 或結尾的內容
                pattern = r'["\']text["\']\s*:\s*["\']((?:[^"\']|\\["\']|\\n)+?)(?:["\']\s*,\s*["\']extras["\']|["\']\s*[,}])'
                text_match = re.search(pattern, response_text, re.DOTALL)
                if text_match:
                    response_text = text_match.group(1)
                    response_text = response_text.replace('\\n', '\n').replace("\\'", "'").replace('\\"', '"').strip()
                else:
                    # 如果無法提取，返回錯誤訊息
                    response_text = "抱歉，無法解析回應格式。"
            
            # 如果回應為空，返回預設訊息
            if not response_text or len(response_text) == 0:
                response_text = "抱歉，我無法生成回答。"
            
            # 步驟 5: 添加參考文獻部分
            # 解析回答中的引用（如 [1], [2], [1,2] 等）
            import re
            citation_pattern = r'\[(\d+(?:,\d+)*)\]'
            citations_found = set()
            citation_positions = {}  # 記錄每個引用在回答中的位置
            
            for match in re.finditer(citation_pattern, response_text):
                # 提取引用編號（如 "1", "2", "1,2"）
                citation_ids = match.group(1).split(',')
                citation_start = match.start()
                citation_end = match.end()
                
                # 找到引用前的句子（最多前 200 字元）
                context_start = max(0, citation_start - 200)
                context_text = response_text[context_start:citation_end]
                
                for cid in citation_ids:
                    try:
                        ref_id = int(cid.strip())
                        citations_found.add(ref_id)
                        if ref_id not in citation_positions:
                            citation_positions[ref_id] = []
                        citation_positions[ref_id].append(context_text)
                    except ValueError:
                        pass
            
            # 生成參考文獻部分
            if citations_found and references:
                response_text += "\n\n" + "=" * 60 + "\n"
                response_text += "📚 參考文獻與來源段落\n"
                response_text += "=" * 60 + "\n\n"
                
                for ref_id in sorted(citations_found):
                    if 1 <= ref_id <= len(references):
                        ref = references[ref_id - 1]  # 引用編號從 1 開始
                        response_text += f"[{ref_id}] {ref['title']}\n"
                        if ref['link']:
                            response_text += f"   連結：{ref['link']}\n"
                        
                        # 找到回答中與此引用相關的內容
                        if ref_id in citation_positions:
                            # 從回答的上下文中提取關鍵詞，在論文中找到相關段落
                            contexts = citation_positions[ref_id]
                            # 提取關鍵詞（簡單策略：取上下文中的名詞和動詞）
                            keywords = []
                            for ctx in contexts:
                                # 移除引用標記，提取關鍵詞
                                ctx_clean = re.sub(r'\[\d+(?:,\d+)*\]', '', ctx)
                                # 提取中文詞彙（2-4 字）
                                chinese_words = re.findall(r'[\u4e00-\u9fff]{2,4}', ctx_clean)
                                keywords.extend(chinese_words[:5])  # 每個上下文最多 5 個關鍵詞
                            
                            # 在論文中找到包含關鍵詞的段落
                            relevant_paragraphs = []
                            content_lines = ref['content_lines']
                            
                            for line in content_lines:
                                if any(keyword in line for keyword in keywords[:3]):  # 只檢查前 3 個關鍵詞
                                    if len(line.strip()) > 20:  # 只保留有意義的段落
                                        relevant_paragraphs.append(line.strip())
                                        if len(relevant_paragraphs) >= 2:  # 最多顯示 2 個段落
                                            break
                            
                            if relevant_paragraphs:
                                response_text += "   相關段落：\n"
                                for para in relevant_paragraphs:
                                    # 限制段落長度
                                    if len(para) > 300:
                                        para = para[:300] + "..."
                                    response_text += f"   • {para}\n"
                            else:
                                # 如果找不到相關段落，顯示論文的前 200 字作為預覽
                                content_preview = ref['content'][:200]
                                if len(ref['content']) > 200:
                                    content_preview += "..."
                                response_text += f"   相關段落：{content_preview}\n"
                        else:
                            # 如果沒有找到引用位置，顯示論文的前 200 字
                            content_preview = ref['content'][:200]
                            if len(ref['content']) > 200:
                                content_preview += "..."
                            response_text += f"   相關段落：{content_preview}\n"
                        
                        response_text += "\n"
            
            return response_text
            
        except Exception as e:
            # 錯誤處理
            error_msg = f"生成回答時發生錯誤：{str(e)}"
            print(f"[警告] {error_msg}")
            return f"抱歉，處理您的問題時發生錯誤：{str(e)}"
