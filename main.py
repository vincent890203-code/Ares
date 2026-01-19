"""
Ares 系統 CLI 入口點

提供統一的命令列介面來執行 Ares 系統的各個模組。
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from Ares.departments.finance.manager import FinancePipeline
from Ares.departments.Research.manager import ResearchPipeline
from Ares.brain.chat import AresChatbot


def run_finance(file_path: str, output_path: str = None):
    """
    執行財務流程。
    
    Args:
        file_path: 輸入的銀行 CSV 檔案路徑。
        output_path: 輸出的 CSV 檔案路徑。如果為 None，則自動生成。
    """
    print("=" * 60)
    print("[$] Ares Finance Module - 財務數據處理流程")
    print("=" * 60)
    
    if output_path is None:
        # 自動生成輸出檔名
        input_file = Path(file_path)
        output_path = input_file.parent / f"tagged_{input_file.name}"
    
    try:
        pipeline = FinancePipeline()
        result_df = pipeline.run_pipeline(file_path, str(output_path))
        print(f"\n[OK] 財務流程執行完成！")
        print(f"   輸出檔案：{output_path}")
        print(f"   處理記錄數：{len(result_df)} 筆")
    except Exception as e:
        print(f"\n[ERROR] 財務流程執行失敗：{str(e)}")
        sys.exit(1)


def run_research(query: str, limit: int = 5, output_file: str = None):
    """
    執行研究流程。
    
    Args:
        query: 搜尋關鍵字。
        limit: 要處理的論文數量上限。
        output_file: 輸出日報檔案路徑。如果為 None，則自動生成。
    """
    print("=" * 60)
    print("[*] Ares Research Module - 研究論文分析流程")
    print("=" * 60)
    
    if output_file is None:
        # 自動生成輸出檔名
        today = datetime.now().strftime("%Y-%m-%d")
        output_file = f"Research_Daily_{today}.md"
    
    try:
        pipeline = ResearchPipeline(headless=True)
        pipeline.run_daily_brief(
            query=query,
            limit=limit,
            output_file=output_file
        )
        print(f"\n[OK] 研究流程執行完成！")
        print(f"   輸出檔案：{output_file}")
    except Exception as e:
        print(f"\n[ERROR] 研究流程執行失敗：{str(e)}")
        sys.exit(1)


def run_chat(query: str, tag: str = None):
    """
    執行聊天功能。
    
    Args:
        query: 用戶的問題。
        tag: 可選的分類標籤過濾器。
    """
    print("=" * 60)
    print("🤖 Ares Chatbot - 智能問答系統")
    print("=" * 60)
    
    try:
        # 初始化聊天機器人
        print("\n[初始化] 正在啟動 Ares 聊天機器人...")
        bot = AresChatbot()
        
        # 顯示思考訊息
        print("\n🤖 Ares 思考中... (正在檢索大腦記憶)")
        if tag:
            print(f"   過濾條件：{tag}")
        print()
        
        # 調用聊天機器人
        response = bot.chat(query, filter_tag=tag)
        
        # 美化輸出回答
        print("=" * 60)
        print("💬 Ares 的回答：")
        print("=" * 60)
        print()
        print(response)
        print()
        print("=" * 60)
        
    except ValueError as e:
        # API 金鑰相關錯誤
        print(f"\n[ERROR] 初始化失敗：{str(e)}")
        print("\n提示：")
        print("  1. 請確認 .env 檔案中存在 GEMINI_API_KEY")
        print("  2. 確認 API 金鑰格式正確")
        sys.exit(1)
    except Exception as e:
        # 其他錯誤
        print(f"\n[ERROR] 聊天功能執行失敗：{str(e)}")
        print(f"\n錯誤類型：{type(e).__name__}")
        import traceback
        print(f"\n詳細錯誤資訊：")
        traceback.print_exc()
        sys.exit(1)


def run_all():
    """
    執行所有流程（模擬「早安」例行程序）。
    
    自動檢查並執行財務和研究流程。
    """
    print("=" * 60)
    print("[*] Ares System - Good Morning Routine")
    print("執行所有模組的完整流程")
    print("=" * 60)
    
    # 步驟 1: 財務流程（檢查是否有預設檔案）
    print("\n[1/2] 財務模組...")
    default_finance_file = "raw_bank_statement.csv"
    
    if Path(default_finance_file).exists():
        print(f"發現財務資料檔案：{default_finance_file}")
        try:
            run_finance(default_finance_file)
        except Exception as e:
            print(f"[!] 財務流程執行失敗：{str(e)}")
            print("    繼續執行研究流程...")
    else:
        print(f"[!] 未找到預設財務檔案：{default_finance_file}")
        print("    如需執行財務流程，請使用：")
        print("    python main.py finance --file <path>")
        print("    或執行: python setup_data.py 建立測試資料")
    
    # 步驟 2: 研究流程
    print("\n[2/2] 研究模組...")
    try:
        run_research(query="LLM in healthcare", limit=3)
        print("\n[OK] 所有流程執行完成！")
    except Exception as e:
        print(f"\n[ERROR] 研究流程執行失敗：{str(e)}")
        sys.exit(1)


def main():
    """主函數：解析命令列參數並執行對應的流程。"""
    parser = argparse.ArgumentParser(
        description="Ares System CLI - 統一的命令列介面",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  # 執行財務流程
  python main.py finance --file bank_statement.csv
  
  # 執行研究流程
  python main.py research --query "machine learning" --limit 5
  
  # 與 Ares 聊天
  python main.py chat "什麼是深度學習？"
  python main.py chat "生成式AI的應用" --tag "LLM in healthcare"
  
  # 執行所有流程
  python main.py all
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用的命令')
    
    # 財務流程子命令
    finance_parser = subparsers.add_parser(
        'finance',
        help='執行財務數據處理流程'
    )
    finance_parser.add_argument(
        '--file',
        type=str,
        required=True,
        help='輸入的銀行 CSV 檔案路徑'
    )
    finance_parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='輸出的 CSV 檔案路徑（可選，預設為 tagged_<原檔名>）'
    )
    
    # 研究流程子命令
    research_parser = subparsers.add_parser(
        'research',
        help='執行研究論文分析流程'
    )
    research_parser.add_argument(
        '--query',
        type=str,
        required=True,
        help='搜尋關鍵字'
    )
    research_parser.add_argument(
        '--limit',
        type=int,
        default=5,
        help='要處理的論文數量上限（預設：5）'
    )
    research_parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='輸出日報檔案路徑（可選，預設為 Research_Daily_<日期>.md）'
    )
    
    # 聊天子命令
    chat_parser = subparsers.add_parser(
        'chat',
        help='與 Ares 聊天機器人對話'
    )
    chat_parser.add_argument(
        'query',
        type=str,
        help='要詢問的問題'
    )
    chat_parser.add_argument(
        '--tag',
        type=str,
        default=None,
        help='可選的分類標籤過濾器（例如："LLM in healthcare"）'
    )
    
    # 執行所有流程子命令
    all_parser = subparsers.add_parser(
        'all',
        help='執行所有流程（模擬 Good Morning 例行程序）'
    )
    
    args = parser.parse_args()
    
    # 執行對應的命令
    if args.command == 'finance':
        run_finance(args.file, args.output)
    elif args.command == 'research':
        run_research(args.query, args.limit, args.output)
    elif args.command == 'chat':
        run_chat(args.query, args.tag)
    elif args.command == 'all':
        run_all()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
