"""
研究日報發布器模組

此模組提供研究日報的格式化與發布功能，將論文分析結果整理成易讀的 Markdown 格式。
"""

from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path


class ResearchPublisher:
    """
    研究日報發布器 - 將論文分析結果格式化為 Markdown 日報。
    
    此類別負責將多篇論文的分析結果整理成結構化的 Markdown 文件，
    包含目錄、評分、摘要、創新點與閱讀建議。
    """
    
    def publish(self, papers: List[Dict[str, Any]], filename: str) -> None:
        """
        發布研究日報到 Markdown 文件。
        
        將論文列表格式化為結構化的 Markdown 文件，包含標題、目錄和每篇論文的詳細分析。
        
        Args:
            papers: 論文列表，每個字典應包含：
                - 'title': 論文標題
                - 'link': 論文連結
                - 'analysis': 分析結果字典（包含 score, tldr, innovation, recommendation）
            filename: 輸出檔案路徑（.md 檔案）。
            
        Raises:
            IOError: 當檔案寫入失敗時。
        """
        # 取得當前日期
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # 構建 Markdown 內容
        markdown_content = []
        
        # 1. 標題
        markdown_content.append(f"# Ares Research Daily Brief\nDate: {current_date}\n")
        
        # 2. 目錄 (Table of Contents)
        if papers:
            markdown_content.append("## Table of Contents\n")
            for i, paper in enumerate(papers, 1):
                title = paper.get('title', f'Paper {i}')
                # 創建錨點連結（Markdown 標題自動生成錨點）
                anchor = title.lower().replace(' ', '-').replace(':', '').replace('.', '')
                anchor = ''.join(c for c in anchor if c.isalnum() or c == '-')
                # 移除多餘的連字號
                anchor = '-'.join(filter(None, anchor.split('-')))
                markdown_content.append(f"{i}. [{title}](#{anchor})")
            markdown_content.append("")  # 空行
        
        # 3. 論文內容
        markdown_content.append("---\n")
        for i, paper in enumerate(papers, 1):
            title = paper.get('title', f'Paper {i}')
            link = paper.get('link', '')
            analysis = paper.get('analysis', {})
            
            # 如果 analysis 是空字典，嘗試從 paper 中直接取得（向後兼容）
            if not analysis:
                analysis = {
                    'score': paper.get('score', 0),
                    'tldr': paper.get('tldr', '無法分析'),
                    'innovation': paper.get('innovation', '無法分析'),
                    'recommendation': paper.get('recommendation', '無法提供建議')
                }
            
            # 論文標題（Markdown 標題會自動生成錨點）
            markdown_content.append(f"\n## {title}\n")
            
            # 評分
            score = analysis.get('score', 0)
            markdown_content.append(f"**Score**: {score}/10\n")
            
            # TL;DR
            tldr = analysis.get('tldr', '無法分析')
            markdown_content.append(f"**TL;DR**: {tldr}\n")
            
            # 創新點
            innovation = analysis.get('innovation', '無法分析')
            markdown_content.append(f"**Innovation**: {innovation}\n")
            
            # 閱讀建議
            recommendation = analysis.get('recommendation', '無法提供建議')
            markdown_content.append(f"**Recommendation**: {recommendation}\n")
            
            # 如果有錯誤信息，顯示出來
            if 'error' in analysis:
                error_msg = analysis.get('error', '未知錯誤')
                markdown_content.append(f"\n*[!] 分析錯誤：{error_msg}*\n")
            
            # 論文連結
            if link:
                markdown_content.append(f"[Read Full Paper]({link})\n")
            else:
                markdown_content.append("*Link not available*\n")
            
            # 分隔線（最後一篇論文後不加）
            if i < len(papers):
                markdown_content.append("\n---\n")
        
        # 4. 組合所有內容
        full_content = "\n".join(markdown_content)
        
        # 5. 寫入檔案
        try:
            output_path = Path(filename)
            # 確保目錄存在
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            print(f"[OK] 日報已成功發布至：{output_path.absolute()}")
            
        except IOError as e:
            raise IOError(f"無法寫入檔案 {filename}：{str(e)}") from e
        except Exception as e:
            raise IOError(f"發布日報時發生錯誤：{str(e)}") from e
