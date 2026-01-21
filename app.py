import streamlit as st
from streamlit_option_menu import option_menu
from modules.style import apply_custom_style
from modules.db import init_db
from modules.auth import authenticate, logout
from modules.dashboard import render_dashboard
from modules.evaluation import render_evaluation_module
from modules.admin import render_admin_panel
from modules.report import render_report_module

# الإعدادات الأولية
st.set_page_config(page_title="HMMC System", layout="wide")
init_db()
apply_custom_style()

if 'authenticated' not in st.session_state:
    st.title("🏗️ نظام HMMC للتقييم")
    with st.form("login_form"):
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.form_submit_button("دخول"):
            user = authenticate(u, p)
            if user:
                st.session_state.update({"authenticated": True, "user_role": user['role'], "user_name": user['name']})
                st.rerun()
            else:
                st.error("خطأ في البيانات")
else:
    with st.sidebar:
        st.write(f"مرحباً: {st.session_state.user_name}")
        choice = option_menu("القائمة", ["الرئيسية", "التقييم", "التقارير", "الإدارة", "خروج"], 
                             icons=['house', 'map', 'file-pdf', 'gear', 'box-arrow-right'])
    
    if choice == "الرئيسية": render_dashboard(st.session_state.user_role)
    elif choice == "التقييم": render_evaluation_module(st.session_state.user_role)
    elif choice == "التقارير": render_report_module(st.session_state.user_role)
    elif choice == "الإدارة": render_admin_panel(st.session_state.user_role)
    elif choice == "خروج": logout()
