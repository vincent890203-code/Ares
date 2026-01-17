# playground_research.py
from Ares.departments.Research.manager import ResearchPipeline
from datetime import datetime

def run_mission():
    print("Ares 生醫情報網啟動...")
    
    # 今天的日期作為檔名
    today = datetime.now().strftime("%Y-%m-%d")
    report_file = f"Research_Daily_{today}.md"
    
    pipeline = ResearchPipeline()
    
    try:
        # 一行指令完成：偵查 -> 分析 -> 出刊
        pipeline.run_daily_brief(
            query="LLM in healthcare", 
            limit=3, 
            output_file=report_file
        )
        
        print(f"\n日報已發行！請查看檔案: {report_file}")
        
    except Exception as e:
        print(f"任務失敗: {e}")

if __name__ == "__main__":
    run_mission()