import pandas as pd
from pathlib import Path
from tabulate import tabulate
from Ares.departments.finance.manager import FinancePipeline

def test_full_pipeline():
    print("🚀 啟動 Ares 財務自動化流水線...")
    
    # 1. 建立一個模擬的銀行 CSV (更真實一點)
    dummy_file = "raw_bank_statement.csv"
    output_file = "tagged_statement.csv"
    
    # 模擬常見欄位
    df_mock = pd.DataFrame({
        'Date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-05'],
        'Description': ['7-11 信義門市', '台灣大車隊', '富邦股利發放', 'World Gym'],
        'Amount': [-150, -350, 5000, -1200]
    })
    df_mock.to_csv(dummy_file, index=False, encoding='utf-8')
    
    try:
        # 2. 初始化流水線
        pipeline = FinancePipeline()
        
        # 3. 執行任務 (這時候你會看到進度條跑動！)
        print(f"\n📂 讀取檔案: {dummy_file}")
        result_df = pipeline.run_pipeline(dummy_file, output_file)
        
        # 4. 展示成果
        print("\n✅ 處理完成！預覽結果：")
        print("-" * 50)
        df_display = result_df[['Date', 'Description', 'Category', 'Amount']]
        print(tabulate(df_display, headers='keys', tablefmt='simple', showindex=False))
        print("-" * 50)
        print(f"💾 檔案已儲存至: {output_file}")

    except Exception as e:
        print(f"❌ 流水線發生錯誤: {e}")
    finally:
        # 清理測試用的原始檔 (保留結果檔讓你檢查)
        if Path(dummy_file).exists():
            Path(dummy_file).unlink()

if __name__ == "__main__":
    test_full_pipeline()