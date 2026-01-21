import streamlit as st
from streamlit_option_menu import option_menu
from modules.style import apply_custom_style
from modules.db import init_db, ensure_settings
from modules.auth import authenticate, logout
from modules.dashboard import render_dashboard
from modules.site_rental_value import SiteRentalValuation
from modules.report import render_report_module
from modules.admin import render_admin_panel

# إعداد الصفحة الأساسي
st.set_page_config(
    page_title="lمبادرة محمد داغستاني لدعم قرارات اللجان لتقدير القيمة الإيجارية للمواقع الاستثمارية ",
    page_icon="🕋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة قاعدة البيانات والتنسيق
init_db()
ensure_settings()
apply_custom_style()

# دالة كشف الجوال
def is_mobile():
    try:
        ua = st.context.headers.get("User-Agent", "").lower()
        return any(x in ua for x in ["mobile", "android", "iphone", "ipad"])
    except:
        return False

st.session_state['is_mobile'] = is_mobile()

# نظام تسجيل الدخول
if 'authenticated' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🏗️ نظام HMMC للتقييم العقاري</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>منطقة مكة المكرمة</p>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                u = st.text_input("اسم المستخدم", placeholder="admin")
                p = st.text_input("كلمة المرور", type="password", placeholder="admin123")
                if st.form_submit_button("تسجيل الدخول", use_container_width=True):
                    user = authenticate(u, p)
                    if user:
                        st.session_state.update({
                            "authenticated": True, 
                            "user_role": user['role'], 
                            "user_name": user['name']
                        })
                        st.rerun()
                    else:
                        st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
else:
    # القائمة الجانبية الاحترافية
    with st.sidebar:
        st.markdown(f"### مرحباً، {st.session_state.user_name} 👋")
        st.info(f"الصلاحية: {st.session_state.user_role}")
        
        menu_options = ["الرئيسية", "تقييم جديد", "التقارير", "الإدارة", "خروج"]
        menu_icons = ['house', 'map', 'file-earmark-pdf', 'gear', 'box-arrow-right']
        
        # حجب الإدارة عن غير المسؤولين
        if st.session_state.user_role != 'admin':
            menu_options.remove("الإدارة")
            menu_icons.remove("gear")

        selected = option_menu(
            "القائمة الرئيسية",
            menu_options,
            icons=menu_icons,
            menu_icon="cast",
            default_index=0,
        )

    # توجيه الصفحات
    if selected == "الرئيسية":
        render_dashboard(st.session_state.user_role)
    elif selected == "تقييم جديد":
        valuator = SiteRentalValuation()
        valuator.render_enhanced_valuation()
    elif selected == "التقارير":
        render_report_module(st.session_state.user_role)
    elif selected == "الإدارة":
        render_admin_panel(st.session_state.user_role)
    elif selected == "خروج":
        logout()
        st.rerun()
