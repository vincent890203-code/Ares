import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock

# ==========================================
# 1. 給 Refinery 用的假資料
# ==========================================
@pytest.fixture
def dirty_df():
    """
    這是一個「集大成」的髒資料 DataFrame，包含：
    1. 醜陋的欄位名稱 (前後空白)
    2. 重複的列 (ID=1)
    3. 缺失值 (NaN)
    4. 髒亂的文字 (前後空白)
    """
    return pd.DataFrame({
        '  ID ': [1, 1, 2, 3],        # 欄位有空白，且 ID=1 重複
        'Val ': [10, 10, np.nan, 20], # 數值有 NaN
        'Text': ['  A  ', '  A  ', 'B', None] # 文字有空白也有 None
    })

# ==========================================
# 2. 給 Spider 用的假元件
# ==========================================
@pytest.fixture
def mock_element():
    """
    回傳一個模擬的 Selenium WebElement。
    預設它有文字，且屬性 href 也有值。
    """
    element = MagicMock()
    element.text = "  Mock Text  "
    # 設定當呼叫 get_attribute('href') 時的回傳值
    element.get_attribute.side_effect = lambda attr: "http://mock.com" if attr == "href" else None
    return element