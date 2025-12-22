import pandas as pd
import numpy as np
import re

class BioCleaner:
    """
    負責生醫數據的清洗工作 (Cleaning)。
    職責：處理缺失值、去除重複、處理異常格式。
    """

    @staticmethod
    def drop_missing(df: pd.DataFrame) -> pd.DataFrame:
        """直接丟棄含有 NaN 的列"""
        initial_len = len(df)
        df_clean = df.dropna()
        dropped_count = initial_len - len(df_clean)
        if dropped_count > 0:
            print(f"🧹 [Cleaner] 已移除 {dropped_count} 筆含有缺失值的資料。")
        return df_clean

    @staticmethod
    def fill_missing(df: pd.DataFrame, value=0) -> pd.DataFrame:
        """填充缺失值 (例如實驗數據若無數值則補 0)"""
        print(f"🧹 [Cleaner] 將所有缺失值填充為: {value}")
        return df.fillna(value)

    @staticmethod
    def remove_duplicates(df: pd.DataFrame, subset=None) -> pd.DataFrame:
        """去除重複的資料 (爬蟲常會抓到重複項目)"""
        initial_len = len(df)
        df_clean = df.drop_duplicates(subset=subset)
        diff = initial_len - len(df_clean)
        if diff > 0:
            print(f"🧹 [Cleaner] 發現並移除了 {diff} 筆重複資料。")
        return df_clean

    @staticmethod
    def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """
        標準化欄位名稱：
        1. 移除前後空白
        2. 將空格轉為底線
        3. 轉小寫
        例如: " Drug Toxicity " -> "drug_toxicity"
        """
        df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
        return df

# ===  這是為了相容舊程式碼的獨立函式 (放在 Class 外面) ===
def clean_text_basic(text):
    """
    基礎文字清洗：去除前後空白、換行符號
    """
    if not text:
        return ""
    # 轉成字串 -> 去除前後空白 -> 去除換行
    text = str(text).strip()
    text = text.replace('\n', '').replace('\r', '')
    return text