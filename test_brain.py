"""
測試 KnowledgeBase (Hippocampus) 模組
"""
from Ares.brain import KnowledgeBase


def test_hippocampus():
    """
    測試知識庫的記憶與回憶功能
    """
    print("=" * 50)
    print("🧠 測試 Hippocampus (KnowledgeBase)")
    print("=" * 50)
    
    # 初始化知識庫
    print("\n[1] 初始化 KnowledgeBase...")
    kb = KnowledgeBase()
    
    # 創建虛擬數據
    # 格式：title, link, analysis={tldr, innovation, score}
    print("\n[2] 準備測試數據...")
    dummy_data = [
        {
            'title': 'Deep Learning for Drug Discovery',
            'link': 'https://example.com/paper1',
            'analysis': {
                'tldr': 'This paper presents a novel deep learning approach for predicting drug-target interactions using graph neural networks.',
                'innovation': 'First to use GNN for multi-target drug discovery with 95% accuracy improvement.',
                'score': 9.5
            }
        },
        {
            'title': 'Transformer Models in Bioinformatics',
            'link': 'https://example.com/paper2',
            'analysis': {
                'tldr': 'We adapt transformer architectures for protein sequence analysis, achieving state-of-the-art results on benchmark datasets.',
                'innovation': 'Novel attention mechanism specifically designed for biological sequences with interpretability features.',
                'score': 9.2
            }
        }
    ]
    
    # 轉換數據格式以符合 memorize 的期望格式
    papers = []
    for item in dummy_data:
        paper = {
            'Title': item['title'],
            'Link': item['link'],
            'TLDR': item['analysis']['tldr'],
            'Innovation': item['analysis']['innovation'],
            'Score': item['analysis']['score'],
            'Date': '2026-01-17'  # 添加日期欄位
        }
        papers.append(paper)
    
    # 調用 memorize
    print("\n[3] 存入知識庫...")
    kb.memorize(papers)
    
    # 調用 recall 進行查詢
    print("\n[4] 執行語義搜索...")
    query = "deep learning drug discovery"
    results = kb.recall(query, k=2)
    
    # 打印召回結果
    print(f"\n[5] 查詢：'{query}'")
    print(f"找到 {len(results)} 篇相關論文：\n")
    
    for i, doc in enumerate(results, 1):
        print(f"--- 論文 {i} ---")
        print(f"標題: {doc.metadata.get('Title', 'N/A')}")
        print(f"連結: {doc.metadata.get('Link', 'N/A')}")
        print(f"評分: {doc.metadata.get('Score', 'N/A')}")
        print(f"內容預覽:\n{doc.page_content[:200]}...")
        print()


if __name__ == "__main__":
    test_hippocampus()
