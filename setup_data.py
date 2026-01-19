# setup_data.py
import pandas as pd

def create_mock_csv():
    print("📊 正在產生模擬銀行帳單...")
    
    data = {
        'Date': [
            '2024-01-01', '2024-01-02', '2024-01-05', 
            '2024-01-10', '2024-01-15', '2024-01-20', 
            '2024-01-25', '2024-01-28'
        ],
        'Description': [
            '7-11 信義門市',          # 預期: 雜支/食
            'Uber EATS',             # 預期: 食
            '台灣高鐵',               # 預期: 行
            '薪資轉帳-台積電',        # 預期: 薪資
            'World Gym 台北俱樂部',   # 預期: 樂/育
            'Netflix 月費',           # 預期: 樂
            '全聯福利中心',           # 預期: 食/雜支
            '富邦人壽保費'            # 預期: 保險/投資
        ],
        'Amount': [
            -155, -350, -1490, 
            85000, -1288, -270, 
            -890, -3500
        ]
    }
    
    df = pd.DataFrame(data)
    # 存成 utf-8-sig 確保 Excel 打開不會亂碼
    filename = 'raw_bank_statement.csv'
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    print(f"✅ 檔案已建立: {filename}")
    print("👉 現在你可以執行: python main.py finance --file raw_bank_statement.csv")

if __name__ == "__main__":
    create_mock_csv()