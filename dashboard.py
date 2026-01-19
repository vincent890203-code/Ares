"""
Ares Intelligence System - Web Dashboard

使用 Streamlit 構建的 Ares 系統 Web 介面
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from Ares.brain.chat import AresChatbot
import os
from pathlib import Path

# 頁面配置
st.set_page_config(
    page_title="Ares Intelligence System",
    layout="wide"
)

# 側邊欄導航
st.sidebar.title("Ares Command Center 🛡️")
page = st.sidebar.radio(
    "導航選單",
    ["💬 戰略對話 (Chat)", "💰 財務監控 (Finance)", "🔬 研究情報 (Research)"]
)

# 初始化 session_state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# 標籤頁 1: 戰略對話 (Chat)
if page == "💬 戰略對話 (Chat)":
    st.title("💬 戰略對話 (Chat)")
    st.markdown("---")
    
    # 初始化聊天機器人（只初始化一次）
    if st.session_state.chatbot is None:
        try:
            with st.spinner("正在啟動 Ares 聊天機器人..."):
                st.session_state.chatbot = AresChatbot()
            st.success("✅ Ares 已就緒")
        except Exception as e:
            st.error(f"❌ 初始化失敗：{str(e)}")
            st.session_state.chatbot = None
    
    # 顯示聊天歷史
    if st.session_state.chatbot:
        # 顯示歷史訊息
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                with st.chat_message("user"):
                    st.write(message['content'])
            else:
                with st.chat_message("assistant"):
                    st.write(message['content'])
        
        # 用戶輸入
        user_query = st.chat_input("輸入您的問題...")
        
        if user_query:
            # 顯示用戶訊息
            with st.chat_message("user"):
                st.write(user_query)
            
            # 保存用戶訊息到歷史
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_query
            })
            
            # 獲取 AI 回應
            try:
                with st.chat_message("assistant"):
                    with st.spinner("Ares 思考中..."):
                        response = st.session_state.chatbot.chat(user_query)
                        st.write(response)
                    
                    # 保存 AI 回應到歷史
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response
                    })
            except Exception as e:
                st.error(f"❌ 發生錯誤：{str(e)}")
    else:
        st.warning("⚠️ 聊天機器人尚未初始化，請檢查 API 金鑰設定。")

# 標籤頁 2: 財務監控 (Finance)
elif page == "💰 財務監控 (Finance)":
    st.title("💰 財務監控 (Finance)")
    st.markdown("---")
    
    # 尋找財務數據文件
    data_file = None
    root_path = Path(".")
    
    # 搜尋包含 'tagged' 的 CSV 文件
    csv_files = list(root_path.glob("*tagged*.csv"))
    if csv_files:
        data_file = csv_files[0]  # 使用第一個找到的文件
    
    if data_file and data_file.exists():
        try:
            # 讀取數據
            df = pd.read_csv(data_file)
            
            # 檢查是否有 Category 欄位
            if 'Category' in df.columns:
                st.subheader("📊 支出分類統計")
                
                # 計算分類統計
                category_counts = df['Category'].value_counts()
                
                # 創建餅圖
                fig = px.pie(
                    values=category_counts.values,
                    names=category_counts.index,
                    title="支出分類分布圖"
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
                
                # 顯示統計摘要
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("總交易數", len(df))
                with col2:
                    st.metric("分類數", len(category_counts))
                with col3:
                    if 'Amount' in df.columns:
                        total_amount = df['Amount'].sum()
                        st.metric("總金額", f"${total_amount:,.2f}")
                
                st.markdown("---")
                st.subheader("📋 原始數據")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("⚠️ 數據文件中沒有找到 'Category' 欄位")
                st.dataframe(df, use_container_width=True)
                
        except Exception as e:
            st.error(f"❌ 讀取數據文件時發生錯誤：{str(e)}")
    else:
        st.warning("⚠️ 尚未執行財務模組 (No data found)")
        st.info("💡 提示：請先執行 `python main.py finance --file <your_file.csv>` 來生成財務數據")

# 標籤頁 3: 研究情報 (Research)
elif page == "🔬 研究情報 (Research)":
    st.title("🔬 研究情報 (Research)")
    st.markdown("---")
    st.info("Research Dashboard coming soon...")
    
    # 未來可以在這裡添加研究相關的可視化
    # 例如：論文分析結果、知識庫統計等
