import streamlit as st
from streamlit_option_menu import option_menu
from modules.style import apply_custom_style
from modules.db import init_db
from modules.auth import authenticate
from modules.valuation import render_valuation_ui
from modules.dashboard import render_dashboard
from modules.report import render_report_tab

st.set_page_config(page_title="نظام HMMC العقاري المطور", layout="wide")
init_db()
apply_custom_style()

# التحقق من نوع الجهاز للجوال
is_mobile = st.context.headers.get("User-Agent", "").lower().find("mobile") != -1

if 'authenticated' not in st.session_state:
    st.header("🔐 نظام التقييم العقاري البلدي")
    # منطق تسجيل الدخول المحدث
    with st.form("login"):
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.form_submit_button("دخول"):
            user = authenticate(u, p)
            if user:
                st.session_state.authenticated = True
                st.rerun()
else:
    # القائمة الجانبية الاحترافية
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=100)
        selected = option_menu(
            "قائمة النظام",
            ["لوحة التحكم", "محرك التقييم", "إصدار التقارير", "الإعدادات"],
            icons=['grid', 'calculator', 'file-text', 'gear'],
            menu_icon="cast", default_index=0,
        )

    if selected == "لوحة التحكم":
        render_dashboard("admin")
    elif selected == "محرك التقييم":
        from modules.site_rental_value import render_makkah_map # دمج الخريطة
        render_makkah_map()
        render_valuation_ui()
    elif selected == "إصدار التقارير":
        render_report_tab()
