def test_sanity():
    """
    一個最基本的測試，確保 1+1=2。
    這只是用來測試 CI 流程是否正常運作。
    """
    assert 1 + 1 == 2

def test_import():
    """
    測試是否能成功 import 您的套件。
    如果有依賴沒裝好，這一步就會報錯。
    """
    try:
        import Ares
    except ImportError:
        assert False, "Ares package could not be imported"