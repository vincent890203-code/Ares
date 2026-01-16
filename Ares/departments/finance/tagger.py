"""
交易標籤器模組

此模組使用 Google Gemini AI 來為銀行交易描述自動分類標籤。
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


class TransactionTagger:
    """
    交易標籤器 - 使用 AI 為銀行交易描述自動分類。
    
    此類別使用 Google Gemini AI 模型來分析交易描述並將其分類到預定義的類別中。
    支援的分類標籤：食、衣、住、行、育、樂、薪資、投資、雜支。
    """
    
    # 支援的交易分類標籤
    CATEGORIES = ['食', '衣', '住', '行', '育', '樂', '薪資', '投資', '雜支']
    
    def __init__(self):
        """
        初始化交易標籤器。
        
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
        
        # 初始化 LangChain Google Gemini 模型（使用 gemini-flash-latest，速度較快且成本較低）
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-flash-latest",
            temperature=0,
            google_api_key=api_key
        )
    
    def predict_category(self, description: str) -> str:
        """
        預測交易描述的分類標籤。
        
        使用 AI 模型分析交易描述，並將其分類到預定義的類別中。
        輸出僅包含標籤名稱，不包含其他文字。
        
        Args:
            description: 銀行交易描述文字。
            
        Returns:
            str: 分類標籤名稱（食、衣、住、行、育、樂、薪資、投資、雜支 其中之一）。
            
        Raises:
            Exception: 當 API 呼叫失敗時拋出異常。
        """
        prompt = f"""請將以下銀行交易描述分類到以下其中一個類別：{', '.join(self.CATEGORIES)}

交易描述：{description}

請只回覆標籤名稱，不要包含任何其他文字或說明。"""

        try:
            response = self.llm.invoke(prompt)

            # 檢查回傳結果的型別
            if isinstance(response, list):
                # 取清單第一個元素
                first_resp = response[0] if response else None
                category = getattr(first_resp, 'content', str(first_resp)).strip() if first_resp is not None else ''
            elif hasattr(response, 'content'):
                category = str(response.content).strip()
            else:
                # 回傳字串或未知型別
                category = str(response).strip()

            # 驗證回傳的標籤是否在有效類別中
            if category in self.CATEGORIES:
                return category
            else:
                return '雜支'

        except Exception as e:
            raise Exception(f'AI 分類失敗：{str(e)}') from e
