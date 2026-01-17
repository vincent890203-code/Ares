# playground_research.py
from Ares.departments.Research.scout import PubMedScout
from Ares.departments.Research.editor import ResearchEditor
import time

def test_research_pipeline():
    print("Ares Research Pipeline 啟動...")
    
    # 1. 初始化部門
    scout = PubMedScout(headless=True)
    editor = ResearchEditor()
    
    try:
        # 2. 派出偵查兵 (Hunt)
        query = "LLM in healthcare"
        print(f"正在搜尋: {query} ...")
        papers = scout.search(query, limit=3)
        print(f"成功捕獲 {len(papers)} 篇論文！開始進行 AI 審稿...\n")
        
        # 3. 總編輯審閱 (Analyze)
        for i, paper in enumerate(papers, 1):
            print(f"--- 論文 {i} 分析中 ---")
            print(f"標題: {paper['title']}")
            
            # 調試資訊：檢查論文資料
            snippet = paper.get('snippet', '')
            print(f"[調試] 摘要長度: {len(snippet)} 字元")
            print(f"[調試] 摘要預覽: {snippet[:100] if snippet else '無摘要'}...")
            
            # 呼叫 Editor 進行分析
            insight = editor.review(paper)
            
            # 顯示結果 (模擬未來的日報格式)
            print(f"評分: {insight.get('score')}/10")
            print(f"懶人包: {insight.get('tldr')}")
            print(f"創新點: {insight.get('innovation')}")
            print(f"點評: {insight.get('recommendation')}")
            
            # 如果有錯誤，顯示錯誤訊息
            if 'error' in insight:
                print(f"[錯誤] {insight.get('error')}")
            
            print("-" * 50 + "\n")
            
            # 避免 API Rate Limit (雖然 Gemini 限制很寬，但好習慣要有)
            time.sleep(1)

    except Exception as e:
        print(f"流程發生錯誤: {e}")
    finally:
        scout.close()
        print("任務結束")

if __name__ == "__main__":
    test_research_pipeline()