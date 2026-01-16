"""
財務流程管理器模組

此模組提供完整的財務數據處理流程，整合資料載入、AI 分類與結果輸出。
"""

import pandas as pd
from tqdm import tqdm
from typing import Optional

from .loader import BankLoader
from .tagger import TransactionTagger


class FinancePipeline:
    """
    財務處理流程 - 整合資料載入、AI 分類與結果輸出的完整流程。
    
    此類別提供端對端的財務數據處理功能，從讀取銀行 CSV 檔案開始，
    使用 AI 自動分類每筆交易，最後輸出包含分類結果的 CSV 檔案。
    """
    
    def __init__(self):
        """
        初始化財務處理流程。
        
        建立資料載入器與 AI 標籤器實例，準備進行資料處理。
        """
        self.loader = BankLoader()
        self.tagger = TransactionTagger()
    
    def run_pipeline(self, file_path: str, output_path: str) -> pd.DataFrame:
        """
        執行完整的財務數據處理流程。
        
        從指定的檔案路徑讀取銀行交易資料，使用 AI 為每筆交易自動分類，
        並將結果儲存到輸出路徑。處理過程會顯示進度條以便追蹤。
        
        Args:
            file_path: 輸入的銀行 CSV 檔案路徑。
            output_path: 輸出結果的 CSV 檔案路徑。
            
        Returns:
            pd.DataFrame: 包含分類結果的處理後 DataFrame。
            
        Raises:
            FileNotFoundError: 如果輸入檔案不存在。
            ValueError: 如果 DataFrame 中缺少必要的描述欄位。
            Exception: 當資料處理或檔案寫入過程中發生錯誤時。
        """
        try:
            # 步驟 1: 載入資料
            print(f"正在載入資料：{file_path}")
            df = self.loader.load_csv(file_path)
            print(f"成功載入 {len(df)} 筆交易記錄")
            
            # 步驟 2: 檢查必要的欄位是否存在
            description_column = None
            if "Description" in df.columns:
                description_column = "Description"
            elif "摘要" in df.columns:
                description_column = "摘要"
            else:
                raise ValueError(
                    "錯誤：DataFrame 中缺少必要的描述欄位。"
                    "請確認資料包含 'Description' 或 '摘要' 欄位。"
                )
            
            print(f"使用欄位 '{description_column}' 作為交易描述")
            
            # 步驟 3: 使用 AI 為每筆交易分類
            print("開始進行 AI 分類...")
            categories = []
            
            # 使用 tqdm 建立進度條，遍歷每一列資料
            for idx, row in tqdm(df.iterrows(), total=len(df), desc="分類進度"):
                try:
                    # 取得交易描述
                    description = str(row[description_column])
                    
                    # 如果描述為空或 NaN，設為預設值
                    if pd.isna(description) or description.strip() == "":
                        category = "雜支"
                    else:
                        # 呼叫 AI 標籤器進行分類
                        category = self.tagger.predict_category(description)
                    
                    categories.append(category)
                    
                except Exception as e:
                    # 如果單筆分類失敗，使用預設值並記錄警告
                    print(f"警告：第 {idx + 1} 筆交易分類失敗：{str(e)}，使用預設值 '雜支'")
                    categories.append("雜支")
            
            # 步驟 4: 將分類結果加入 DataFrame
            df["Category"] = categories
            print(f"分類完成！共處理 {len(df)} 筆交易")
            
            # 步驟 5: 儲存結果到 CSV 檔案
            print(f"正在儲存結果到：{output_path}")
            df.to_csv(
                output_path,
                index=False,
                encoding='utf-8-sig'  # 使用 utf-8-sig 避免 Excel 中文亂碼
            )
            print("結果已成功儲存！")
            
            return df
            
        except FileNotFoundError as e:
            raise FileNotFoundError(f"檔案載入失敗：{str(e)}") from e
        except ValueError as e:
            raise ValueError(f"資料驗證失敗：{str(e)}") from e
        except Exception as e:
            raise Exception(f"處理流程執行失敗：{str(e)}") from e
