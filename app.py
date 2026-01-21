import streamlit as st
from streamlit_option_menu import option_menu
from modules.db import init_db
from modules.style import apply_custom_style
from modules.auth import authenticate, logout
from modules.dashboard import render_dashboard
from modules.site_rental_value import SiteRentalValuation
from modules.report import render_report_module
from modules.admin import render_admin_panel

# 1. إعداد الصفحة الأولي
st.set_page_config(page_title="HMMC Makkah", layout="wide")
init_db()
apply_custom_style()

# 2. كشف نوع الجهاز
def is_mobile():
    try:
        ua = st.context.headers.get("User-Agent", "").lower()
        return any(x in ua for x in ["mobile", "android", "iphone"])
    except: return False

# 3. نظام تسجيل الدخول
if 'authenticated' not in st.session_state:
    st.title("🏗️ نظام التقييم العقاري - مكة المكرمة")
    with st.form("login"):
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.form_submit_button("دخول"):
            user = authenticate(u, p)
            if user:
                st.session_state.update({"authenticated": True, "user_role": user['role'], "user_name": user['name']})
                st.rerun()
            else: st.error("بيانات الدخول غير صحيحة")
else:
    # 4. القائمة الجانبية الاحترافية
    with st.sidebar:
        st.markdown(f"### مرحباً: {st.session_state.user_name}")
        choice = option_menu(
            "قائمة النظام",
            ["الرئيسية", "تقييم جديد", "التقارير", "الإدارة", "خروج"],
            icons=['house', 'map', 'file-earmark-pdf', 'gear', 'box-arrow-right'],
            menu_icon="cast", default_index=0
        )

    # 5. توجيه الصفحات
    if choice == "الرئيسية": render_dashboard(st.session_state.user_role)
    elif choice == "تقييم جديد": 
        val = SiteRentalValuation()
        val.render_valuation()
    elif choice == "التقارير": render_report_module(st.session_state.user_role)
    elif choice == "الإدارة": render_admin_panel(st.session_state.user_role)
    elif choice == "خروج": logout()
