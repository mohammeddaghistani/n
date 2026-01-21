import streamlit as st

def apply_custom_style():
    rtl_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [data-testid="stAppViewContainer"], .main {
            direction: RTL;
            text-align: right;
            font-family: 'Cairo', sans-serif;
        }
        [data-testid="stSidebar"] { direction: RTL; }
        .stTabs [data-baseweb="tab-list"] { direction: RTL; gap: 10px; }
        .stButton button { width: 100%; border-radius: 10px; }
        /* تحسين شكل الكروت في لوحة التحكم */
        .dashboard-card {
            background: #ffffff; padding: 20px; border-radius: 15px;
            border: 1px solid #e6e9ef; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 20px; text-align: center;
        }
    </style>
    """
    st.markdown(rtl_css, unsafe_allow_html=True)
