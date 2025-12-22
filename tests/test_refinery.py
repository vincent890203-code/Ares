import pytest
import pandas as pd
import numpy as np
from Ares.refinery.cleaner import BioCleaner, clean_text_basic

# === 測試獨立函式 (這個沒變) ===
def test_clean_text_basic():
    assert clean_text_basic("  ABC  ") == "ABC"
    assert clean_text_basic(None) == ""

# === 測試 BioCleaner (使用 conftest 的 dirty_df) ===

def test_drop_missing(dirty_df):
    """注意：dirty_df 會自動從 conftest 傳進來"""
    # 原本 dirty_df 有 4 筆，其中 2 筆有 NaN (Val, Text 欄位)
    cleaned = BioCleaner.drop_missing(dirty_df)
    
    # 預期只剩下 2 筆 (ID 1 和 1) - 因為這兩列沒有 NaN
    # (原本的假資料 ID 1 雖然重複，但資料是完整的，ID 2, 3 都有缺)
    assert len(cleaned) == 2

def test_fill_missing(dirty_df):
    """測試填補功能"""
    filled = BioCleaner.fill_missing(dirty_df, value=0)
    
    # 檢查原本是 NaN 的地方 (第 2 列的 Val)
    assert filled.iloc[2]['Val '] == 0
    # 確保資料筆數沒變
    assert len(filled) == 4

def test_remove_duplicates(dirty_df):
    """測試移除重複"""
    # 我們的 dirty_df 前兩筆完全一樣 (ID=1)
    deduped = BioCleaner.remove_duplicates(dirty_df)
    
    # 應該少一筆
    assert len(deduped) == 3

def test_clean_column_names(dirty_df):
    """測試欄位清洗"""
    # 原本是 '  ID ', 'Val ', 'Text'
    cleaned = BioCleaner.clean_column_names(dirty_df)
    
    cols = cleaned.columns.tolist()
    assert 'id' in cols
    assert 'val' in cols
    assert '  ID ' not in cols