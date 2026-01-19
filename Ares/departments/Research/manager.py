"""
研究流程管理器模組

此模組提供完整的研究論文處理流程，整合論文搜尋、AI 分析與日報生成。
"""

import time
from datetime import datetime
from typing import List, Dict, Any

from .scout import PubMedScout
from .editor import ResearchEditor
from .daily_brief import ResearchPublisher
from Ares.brain import KnowledgeBase


class ResearchPipeline:
    """
    研究處理流程 - 整合論文搜尋、AI 分析與日報生成的完整流程。
    
    此類別提供端對端的研究論文處理功能，從 PubMed 搜尋論文開始，
    使用 AI 分析每篇論文，最後生成格式化的 Markdown 日報。
    """
    
    def __init__(self, headless: bool = True):
        """
        初始化研究處理流程。
        
        建立偵察兵、編輯器、發布器與大腦記憶庫實例，準備進行論文處理。
        
        Args:
            headless: 是否使用無頭模式執行瀏覽器。預設為 True。
        """
        self.scout = PubMedScout(headless=headless)
        self.editor = ResearchEditor()
        self.publisher = ResearchPublisher()
        self.brain = KnowledgeBase()
    
    def run_daily_brief(
        self, 
        query: str, 
        limit: int = 5, 
        output_file: str = "daily_brief.md",
        save_to_brain: bool = True
    ) -> None:
        """
        執行完整的日報生成流程。
        
        從 PubMed 搜尋論文，使用 AI 分析每篇論文，並生成格式化的 Markdown 日報。
        
        Args:
            query: 搜尋關鍵字。
            limit: 要處理的論文數量上限。預設為 5。
            output_file: 輸出日報檔案路徑。預設為 "daily_brief.md"。
            save_to_brain: 是否將論文存入大腦記憶庫。預設為 True。
            
        Raises:
            RuntimeError: 當流程執行過程中發生錯誤時。
        """
        try:
            # 步驟 1: Scout 搜尋論文
            print(f"正在搜尋論文：{query} ...")
            papers = self.scout.search(query, limit=limit)
            print(f"成功找到 {len(papers)} 篇論文\n")
            
            if not papers:
                print("未找到任何論文，無法生成日報")
                return
            
            # 步驟 2: Editor 審查每篇論文
            print("開始進行 AI 審查...")
            papers_with_analysis: List[Dict[str, Any]] = []
            
            for i, paper in enumerate(papers, 1):
                try:
                    print(f"正在分析論文 {i}/{len(papers)}: {paper.get('title', '無標題')[:50]}...")
                    
                    # 調試資訊：檢查論文資料
                    snippet = paper.get('snippet', '')
                    snippet_len = len(snippet) if snippet else 0
                    if snippet_len < 10:
                        print(f"  [!] 警告：摘要長度僅 {snippet_len} 字元，可能無法分析")
                    
                    # 呼叫 Editor 進行分析
                    analysis = self.editor.review(paper)
                    
                    # 將分析結果添加到論文字典中
                    paper_with_analysis = paper.copy()
                    paper_with_analysis['analysis'] = analysis
                    papers_with_analysis.append(paper_with_analysis)
                    
                    # 顯示分析結果摘要
                    score = analysis.get('score', 0)
                    if score == 0 and 'error' in analysis:
                        error_msg = analysis.get('error', '未知錯誤')
                        print(f"  [X] 分析失敗：{error_msg}")
                        # 如果錯誤包含 JSON 解析問題，顯示前 100 字元以便調試
                        if 'JSON' in error_msg or 'json' in error_msg:
                            print(f"     [調試] 錯誤詳情已記錄在日報中")
                    else:
                        print(f"  [OK] 分析完成，評分：{score}/10")
                        
                except Exception as e:
                    print(f"  [X] 分析失敗：{str(e)}")
                    # 即使分析失敗，也將論文加入列表（使用預設分析結果）
                    paper_with_analysis = paper.copy()
                    paper_with_analysis['analysis'] = {
                        'score': 0,
                        'tldr': '分析失敗',
                        'innovation': '無法分析',
                        'recommendation': '無法提供建議',
                        'error': str(e)
                    }
                    papers_with_analysis.append(paper_with_analysis)
            
            print(f"\n完成 {len(papers_with_analysis)} 篇論文的分析\n")
            
            # 步驟 3: 將論文存入大腦記憶庫（僅存入成功分析的論文）
            if save_to_brain:
                # 過濾出成功分析的論文（沒有 error 且 score > 0）
                papers_for_memory = []
                skipped_count = 0
                
                for paper in papers_with_analysis:
                    analysis = paper.get('analysis', {})
                    
                    # 檢查是否分析成功：沒有 error 且 score > 0
                    has_error = 'error' in analysis
                    score = analysis.get('score', 0)
                    is_valid = not has_error and score > 0
                    
                    if is_valid:
                        paper_dict = {
                            'Title': paper.get('title', ''),
                            'Link': paper.get('link', ''),
                            'TLDR': analysis.get('tldr', ''),
                            'Innovation': analysis.get('innovation', ''),
                            'Score': analysis.get('score', 0),
                            'Date': datetime.now().strftime('%Y-%m-%d')
                        }
                        papers_for_memory.append(paper_dict)
                    else:
                        skipped_count += 1
                        error_reason = analysis.get('error', '評分為 0')
                        print(f"  [跳過] 論文「{paper.get('title', '無標題')[:50]}...」未存入資料庫（原因：{error_reason}）")
                
                # 只有成功分析的論文才存入資料庫
                if papers_for_memory:
                    self.brain.memorize(papers_for_memory, tag=query)
                    print(f"✅ {len(papers_for_memory)} 篇論文已存入大腦記憶庫（標籤：{query}）")
                    if skipped_count > 0:
                        print(f"   ⚠️  {skipped_count} 篇論文因分析失敗未存入資料庫（僅生成報告）")
                else:
                    print(f"⚠️  沒有成功分析的論文，跳過存入資料庫（僅生成報告）")
                print()
            
            # 步驟 4: Publisher 保存報告
            print(f"正在生成日報：{output_file} ...")
            self.publisher.publish(papers_with_analysis, output_file)
            print("日報生成完成！")
            
        except Exception as e:
            raise RuntimeError(f"日報生成流程發生錯誤：{str(e)}") from e
        finally:
            # 確保 Scout 關閉瀏覽器
            try:
                self.scout.close()
                print("瀏覽器已關閉")
            except Exception as e:
                print(f"關閉瀏覽器時發生錯誤：{str(e)}")
    
    def __enter__(self):
        """支援 context manager 的進入方法。"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """支援 context manager 的退出方法，確保瀏覽器關閉。"""
        try:
            self.scout.close()
        except Exception:
            pass
