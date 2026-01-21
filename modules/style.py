import streamlit as st

def apply_custom_style():
    """تطبيق الإعدادات العامة وتنسيق RTL"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* ضبط القائمة الجانبية */
    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }

    /* تحسين العرض للجوال */
    @media (max-width: 768px) {
        .stColumns { flex-direction: column !important; }
        .stMetric { margin-bottom: 15px; }
    }

    /* كروت لوحة التحكم */
    .dashboard-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-right: 5px solid #1E3A8A;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    /* أزرار عريضة ومتجاوبة */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

def get_custom_css():
    return "/* CSS Base */"
