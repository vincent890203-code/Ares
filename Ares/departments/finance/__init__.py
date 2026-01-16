"""
財務部門模組

此模組提供財務數據管理功能。
"""

from .loader import FinanceLoader
from .cleaner import FinanceCleaner


class FinanceManager:
    """
    財務管理器 - 協調財務數據操作。
    
    此類別協調數據載入與清洗操作，用於財務數據處理流程。
    """
    
    def __init__(self):
        """初始化財務管理器，包含載入器與清洗器元件。"""
        self.loader = FinanceLoader()
        self.cleaner = FinanceCleaner()
    
    def process(self, *args, **kwargs):
        """
        透過完整流程處理財務數據。
        
        此方法將被實作以協調財務數據集的載入與清洗操作。
        """
        raise NotImplementedError("FinanceManager.process() 將於後續實作")


__all__ = ["FinanceManager", "FinanceLoader", "FinanceCleaner"]
