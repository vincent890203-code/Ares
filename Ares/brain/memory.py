"""
RAG-based Long-Term Memory (Hippocampus) 模組
使用向量資料庫實現語義搜索功能
"""
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

# 載入環境變數
load_dotenv()


class KnowledgeBase:
    """
    知識庫類別，負責論文記憶與語義搜索
    使用 Chroma 向量資料庫和 Google Generative AI Embeddings
    """
    
    def __init__(self):
        """
        初始化知識庫
        - 設定 Google Generative AI Embeddings
        - 初始化 Chroma 向量資料庫
        - 持久化目錄：./ares_knowledge_store（與 ML 記憶路徑分離）
        - Collection 名稱：ares_research_archive
        """
        # 初始化嵌入模型
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        
        # 初始化向量資料庫
        # persist_directory 設為 ./ares_knowledge_store（與 brain_memory/ 分離）
        # collection_name 設為 ares_research_archive
        self.persist_directory = "./ares_knowledge_store"
        self.vector_db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name="ares_research_archive"
        )
    
    def memorize(self, papers: list, tag: str = "general"):
        """
        將論文列表存入向量資料庫
        
        Args:
            papers: 論文字典列表，每個字典應包含：
                - Title: 論文標題
                - TLDR: 論文摘要
                - Innovation: 創新點
                - Link: 論文連結
                - Score: 評分
                - Date: 日期
            tag: 分類標籤，用於標記論文類別（如 "AI", "Biology", "PM"）。預設為 "general"。
        """
        documents = []
        
        for paper in papers:
            # 組合 page_content：Title + TLDR + Innovation
            page_content = f"{paper.get('Title', '')}\n\n{paper.get('TLDR', '')}\n\n{paper.get('Innovation', '')}"
            
            # 設定 metadata：Title, Link, Score, Date, category
            metadata = {
                'Title': paper.get('Title', ''),
                'Link': paper.get('Link', ''),
                'Score': paper.get('Score', ''),
                'Date': paper.get('Date', ''),
                'category': tag
            }
            
            # 建立 Document 對象
            doc = Document(page_content=page_content, metadata=metadata)
            documents.append(doc)
        
        # 存入向量資料庫
        self.vector_db.add_documents(documents)
        print(f"🧠 [Hippocampus] stored {len(documents)} papers with tag '{tag}'")
    
    def recall(self, query: str, k=3, filter_tag: str = None):
        """
        從向量資料庫中進行語義搜索，召回最相關的論文
        
        Args:
            query: 查詢字串
            k: 返回最相關的 k 篇論文（預設為 3）
            filter_tag: 分類標籤過濾器。如果提供，只搜索該標籤的論文（如 "AI", "Biology", "PM"）。
                        如果為 None，則搜索整個知識庫（跨領域搜索）。預設為 None。
        
        Returns:
            最相關的 k 個 Document 對象列表
        """
        # 根據 filter_tag 決定是否使用過濾器
        if filter_tag is not None:
            # 使用分類標籤過濾器進行搜索
            results = self.vector_db.similarity_search(
                query, 
                k=k, 
                filter={"category": filter_tag}
            )
        else:
            # 搜索整個知識庫（跨領域搜索）
            results = self.vector_db.similarity_search(query, k=k)
        
        return results
    
    def clear(self):
        """
        清除所有已存儲的論文記憶
        
        警告：此操作不可逆，將刪除所有已存儲的論文資料
        """
        try:
            # 方法 1: 嘗試使用 Chroma 的 reset_collection 方法（推薦）
            # 這會刪除集合並重新創建一個空的
            if hasattr(self.vector_db, 'reset_collection'):
                try:
                    self.vector_db.reset_collection()
                    print(f"🧠 [Hippocampus] 已清除所有論文記憶（使用 reset_collection）")
                    return True
                except Exception as reset_error:
                    print(f"⚠️  [Hippocampus] reset_collection 失敗，嘗試其他方法：{str(reset_error)}")
            
            # 方法 2: 嘗試使用 delete_collection，然後重新創建
            if hasattr(self.vector_db, 'delete_collection'):
                try:
                    self.vector_db.delete_collection()
                    # 重新初始化空的資料庫
                    self.vector_db = Chroma(
                        persist_directory=self.persist_directory,
                        embedding_function=self.embeddings,
                        collection_name="ares_research_archive"
                    )
                    print(f"🧠 [Hippocampus] 已清除所有論文記憶（使用 delete_collection）")
                    return True
                except Exception as delete_error:
                    print(f"⚠️  [Hippocampus] delete_collection 失敗，嘗試手動刪除：{str(delete_error)}")
            
            # 方法 3: 如果 API 方法都失敗，手動刪除目錄並重新初始化
            # 注意：這需要先確保沒有其他連接在使用資料庫
            try:
                db_path = Path(self.persist_directory)
                if db_path.exists():
                    # 先嘗試關閉連接
                    if hasattr(self.vector_db, '_client'):
                        try:
                            self.vector_db._client = None
                        except:
                            pass
                    
                    # 刪除目錄
                    shutil.rmtree(db_path)
                    print(f"🧠 [Hippocampus] 已清除所有論文記憶（手動刪除目錄）")
                    
                    # 重新初始化空的資料庫
                    self.vector_db = Chroma(
                        persist_directory=self.persist_directory,
                        embedding_function=self.embeddings,
                        collection_name="ares_research_archive"
                    )
                    return True
                else:
                    print(f"ℹ️  [Hippocampus] 資料庫不存在，無需清除")
                    return True
            except Exception as manual_error:
                print(f"❌ [Hippocampus] 手動清除失敗：{str(manual_error)}")
                return False
                
        except Exception as e:
            print(f"❌ [Hippocampus] 清除資料庫時發生錯誤：{str(e)}")
            import traceback
            print(f"   詳細錯誤：{traceback.format_exc()}")
            return False
