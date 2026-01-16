"""
財務數據載入器模組

此模組處理從各種來源載入財務數據。
"""

import os
from pathlib import Path
from typing import Union

import pandas as pd


class FinanceLoader:
    """
    財務載入器 - 處理財務數據的載入。
    
    此類別將被實作用於從各種來源載入財務數據，例如檔案、API 或資料庫。
    """
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        從 CSV 檔案載入財務數據。
        
        Args:
            file_path: 要載入的 CSV 檔案路徑。
            
        Returns:
            pd.DataFrame: 載入的財務數據，以 pandas DataFrame 形式返回。
            
        Raises:
            FileNotFoundError: 如果指定的檔案不存在。
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        df = pd.read_csv(file_path)
        print(f'Data loaded successfully from {file_path}')
        
        return df


class BankLoader:
    """
    銀行載入器 - 處理銀行 CSV 檔案的載入，並具備編碼偵測功能。
    
    此類別專門處理銀行 CSV 檔案的載入，特別是來自台灣銀行的檔案，
    這些檔案經常使用混合編碼（UTF-8 和 Big5/CP950）。
    """
    
    def load_csv(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        使用自動編碼偵測載入銀行 CSV 檔案。
        
        首先嘗試使用 UTF-8 編碼讀取 CSV 檔案，如果失敗則回退到
        Big5/CP950 編碼。這處理了台灣銀行 CSV 檔案可能使用任一編碼的常見情況。
        
        Args:
            file_path: 要載入的 CSV 檔案路徑。可以是字串或 Path 物件。
            
        Returns:
            pd.DataFrame: 包含載入數據的原始 pandas DataFrame。
            
        Raises:
            FileNotFoundError: 如果指定的檔案不存在。
            UnicodeDecodeError: 如果檔案無法使用 UTF-8 或 Big5/CP950 編碼解碼。
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # 首先嘗試 UTF-8（最常見的現代編碼）
        try:
            df = pd.read_csv(path, encoding='utf-8')
        except UnicodeDecodeError:
            # 回退到 Big5/CP950 用於台灣銀行檔案
            try:
                df = pd.read_csv(path, encoding='big5')
            except UnicodeDecodeError:
                # 嘗試 CP950 作為替代方案（Windows Big5 變體）
                df = pd.read_csv(path, encoding='cp950')
        
        return df
