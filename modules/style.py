import streamlit as st

def apply_makkah_theme():
    """تنسيق RTL كامل ودعم شاشات الجوال"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        direction: rtl;
        text-align: right;
        font-family: 'Tajawal', sans-serif;
    }
    
    /* جعل الحاويات متجاوبة على الجوال */
    @media (max-width: 768px) {
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
        }
    }

    /* تصميم كروت النتائج */
    .metric-card {
        background-color: #ffffff;
        border-right: 5px solid #1E3A8A;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
