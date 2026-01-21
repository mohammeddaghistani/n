import streamlit as st

def apply_custom_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    :root {
        --primary: #1E3A8A;
        --secondary: #FBBF24;
        --bg: #F8FAFC;
    }

    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
        background-color: var(--bg);
    }

    /* كروت التقييم العصرية */
    .valuation-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border-right: 8px solid var(--primary);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    /* تحسين القوائم والجوال */
    [data-testid="stSidebar"] { direction: rtl; }
    @media (max-width: 768px) {
        .stMetric { background: white; padding: 15px; border-radius: 15px; }
    }

    /* أزرار مخصصة */
    .stButton>button {
        border-radius: 12px;
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        border: none;
        transition: 0.3s;
        height: 3.5em;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
