# playground.py
import os
from Ares.departments.finance.tagger import TransactionTagger

def test_brain():
    print("🧠 初始化大腦中 (Connecting to Gemini)...")
    
    try:
        # 1. 實例化標記器
        tagger = TransactionTagger()
        
        # 2. 準備測試題目
        test_cases = [
            "全聯福利中心-信義店",
            "Uber EATS",
            "台灣高鐵",
            "薪資轉帳-台積電",
            "星巴克咖啡"
        ]
        
        print(f"📋 準備測試 {len(test_cases)} 筆交易...\n")

        # 3. 逐一測試
        for desc in test_cases:
            tag = tagger.predict_category(desc)
            print(f"🔹 交易: {desc:<15} => 🏷️  類別: {tag}")
            
        print("\n✅ API 連線與推論成功！")

    except Exception as e:
        print(f"\n❌ 發生錯誤: {e}")
        print("💡 請檢查 .env 檔案是否設定正確，或 API Key 是否有效。")

if __name__ == "__main__":
    test_brain()