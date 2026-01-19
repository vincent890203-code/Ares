"""
驗證大腦記憶庫（Hippocampus）功能測試腳本

測試目標：
1. 測試 1：使用 filter_tag 過濾特定類別，確認 Category 欄位正確
2. 測試 2：跨領域搜索，顯示所有論文（不限類別）
"""
from Ares.brain import KnowledgeBase


def verify_brain(test_query: str = "LLM in healthcare"):
    """
    驗證大腦記憶庫的過濾和搜索功能
    
    Args:
        test_query: 測試用的搜尋關鍵字（應對應之前存入資料庫時使用的標籤）
    """
    print("=" * 70)
    print("🧠 驗證大腦記憶庫（Hippocampus）功能")
    print("=" * 70)
    
    # 初始化知識庫
    print("\n[初始化] 載入知識庫...")
    kb = KnowledgeBase()
    
    # ==========================================
    # 測試 1：使用 filter_tag 過濾特定類別
    # ==========================================
    print(f"\n{'='*70}")
    print(f"📋 測試 1：過濾特定類別（Category = '{test_query}'）")
    print(f"{'='*70}")
    
    query_text = "deep learning"  # 任意查詢文字，用於語義搜索
    results_filtered = kb.recall(query_text, k=10, filter_tag=test_query)
    
    print(f"\n查詢：「{query_text}」")
    print(f"過濾條件：Category = '{test_query}'")
    print(f"\n找到 {len(results_filtered)} 篇論文：\n")
    
    if results_filtered:
        for i, doc in enumerate(results_filtered, 1):
            category = doc.metadata.get('category', 'N/A')
            title = doc.metadata.get('Title', 'N/A')
            score = doc.metadata.get('Score', 'N/A')
            link = doc.metadata.get('Link', 'N/A')
            
            print(f"--- 論文 {i} ---")
            print(f"標題: {title}")
            print(f"Category: {category}")
            print(f"評分: {score}")
            print(f"連結: {link}")
            
            # 驗證 Category 是否正確
            if category == test_query:
                print(f"✅ Category 驗證通過")
            else:
                print(f"❌ Category 驗證失敗：期望 '{test_query}'，實際為 '{category}'")
            
            print()
    else:
        print(f"⚠️  未找到任何論文")
        print(f"   提示：請確認資料庫中是否有使用標籤 '{test_query}' 存儲的論文")
    
    # ==========================================
    # 測試 2：跨領域搜索（不限類別）
    # ==========================================
    print(f"\n{'='*70}")
    print(f"🌐 測試 2：跨領域搜索（不限 Category）")
    print(f"{'='*70}")
    
    results_all = kb.recall(query_text, k=10, filter_tag=None)
    
    print(f"\n查詢：「{query_text}」")
    print(f"過濾條件：無（顯示所有類別）")
    print(f"\n找到 {len(results_all)} 篇論文：\n")
    
    if results_all:
        # 統計不同類別的數量
        category_count = {}
        for doc in results_all:
            category = doc.metadata.get('category', 'unknown')
            category_count[category] = category_count.get(category, 0) + 1
        
        print(f"📊 類別統計：")
        for cat, count in category_count.items():
            print(f"   - {cat}: {count} 篇")
        print()
        
        # 顯示所有論文
        for i, doc in enumerate(results_all, 1):
            category = doc.metadata.get('category', 'N/A')
            title = doc.metadata.get('Title', 'N/A')
            score = doc.metadata.get('Score', 'N/A')
            link = doc.metadata.get('Link', 'N/A')
            
            print(f"--- 論文 {i} ---")
            print(f"標題: {title}")
            print(f"Category: {category}")
            print(f"評分: {score}")
            print(f"連結: {link}")
            print()
    else:
        print(f"⚠️  未找到任何論文")
        print(f"   提示：請確認資料庫中是否有存儲任何論文")
    
    # ==========================================
    # 測試結果總結
    # ==========================================
    print(f"\n{'='*70}")
    print(f"📊 測試結果總結")
    print(f"{'='*70}")
    
    print(f"\n✅ 測試 1（過濾 '{test_query}'）：{len(results_filtered)} 篇論文")
    
    # 驗證測試 1 的 Category 是否都正確
    if results_filtered:
        all_correct = all(
            doc.metadata.get('category') == test_query 
            for doc in results_filtered
        )
        if all_correct:
            print(f"   ✅ 所有論文的 Category 欄位都正確")
        else:
            print(f"   ❌ 部分論文的 Category 欄位不正確")
    else:
        print(f"   ⚠️  未找到任何論文，無法驗證")
    
    print(f"\n✅ 測試 2（跨領域搜索）：{len(results_all)} 篇論文")
    
    # 比較兩個測試的結果
    if results_filtered and results_all:
        print(f"\n📈 比較分析：")
        print(f"   - 過濾搜索結果：{len(results_filtered)} 篇（僅 '{test_query}' 類別）")
        print(f"   - 跨領域搜索結果：{len(results_all)} 篇（所有類別）")
        
        if len(results_all) >= len(results_filtered):
            print(f"   ✅ 跨領域搜索的結果數量 >= 過濾搜索（符合預期）")
        else:
            print(f"   ⚠️  跨領域搜索的結果數量 < 過濾搜索（異常）")


if __name__ == "__main__":
    import sys
    
    # 允許從命令列指定測試關鍵字
    if len(sys.argv) > 1:
        test_query = sys.argv[1]
        print(f"使用指定的測試關鍵字：{test_query}\n")
    else:
        test_query = "LLM in healthcare"
        print(f"使用預設測試關鍵字：{test_query}")
        print(f"（可通過命令列參數指定，例如：python verify_brain.py \"線蟲神經\"）\n")
    
    verify_brain(test_query=test_query)
