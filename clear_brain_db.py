"""
清除大腦記憶庫（向量資料庫）的腳本
用於刪除所有已存儲的論文記憶
"""
from Ares.brain import KnowledgeBase

def clear_brain_database():
    """
    使用 KnowledgeBase 的 clear 方法清除所有論文記憶
    """
    try:
        kb = KnowledgeBase()
        success = kb.clear()
        if success:
            print(f"✅ 已成功清除大腦記憶庫")
            print(f"   所有已存儲的論文記憶已刪除")
        return success
    except Exception as e:
        print(f"❌ 清除失敗：{str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧠 清除大腦記憶庫（Hippocampus）")
    print("=" * 60)
    print()
    
    confirm = input("確定要刪除所有論文記憶嗎？(yes/no): ").strip().lower()
    
    if confirm in ['yes', 'y']:
        clear_brain_database()
    else:
        print("❌ 操作已取消")
