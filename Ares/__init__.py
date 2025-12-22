# === 1. 設定捷徑：直接從子部門拿出好用的工具 ===

# 從 Spider 拿工具
from .spider.core import setup_driver, retry
from .spider.actions import safe_click, safe_type, nuclear_scroll
from .spider.extraction import get_text, get_attribute, extract_list_by_pattern

# 從 Refinery 拿工具 (使用新的 Class 名稱)
from .refinery.cleaner import BioCleaner, clean_text_basic
from .refinery.transformer import FeatureTransformer

# 從 Brain 拿工具
from .brain.cortex import ML_Brain

# === 2. 設定 __all__ (告訴 Python 'from Ares import *' 包含什麼) ===
__all__ = [
    # Spider 工具
    "setup_driver", 
    "retry",
    "safe_click", 
    "safe_type", 
    "nuclear_scroll",
    "get_text", 
    "get_attribute",
    "extract_list_by_pattern",
    
    # Refinery 工具
    "BioCleaner",
    "clean_text_basic",
    "FeatureTransformer",

    # Brain 工具
    "ML_Brain"
]
