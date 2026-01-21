import streamlit as st
from streamlit_folium import st_folium
import folium
from datetime import datetime
from streamlit_option_menu import option_menu  # للمنشورات الاحترافية

# استيراد موديولات النظام
from modules.db import init_db, ensure_settings, add_deal
from modules.auth import login_required, logout
from modules.dashboard import render_dashboard
from modules.style import apply_custom_style, get_custom_css
from modules.admin import render_admin_panel
from modules.site_rental_value import SiteRentalValuation

# ضبط إعدادات الصفحة لتكون احترافية
st.set_page_config(
    page_title="HMMC | نظام التقييم العقاري",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# دالة كشف الجهاز مع دعم التنسيق للجوال
def detect_device_type():
    try:
        ua = st.context.headers.get("User-Agent", "").lower()
    except:
        ua = ""
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad']
    is_mobile = any(k in ua for k in mobile_keywords)
    st.session_state['is_mobile'] = is_mobile
    return is_mobile

# --- CSS إضافي لضمان التوافق التام مع الجوال ---
def apply_mobile_optimization():
    mobile_css = """
    <style>
        /* تحسين التبويبات للجوال */
        .stTabs [data-baseweb="tab-list"] {
            gap: 5px;
            overflow-x: auto;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px;
            font-size: 14px;
        }
        /* جعل الخريطة مرنة */
        iframe { width: 100% !important; border-radius: 15px; }
        /* تحسين شكل الكروت */
        .stMetric { background: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
    </style>
    """
    st.markdown(mobile_css, unsafe_allow_html=True)

class ProfessionalValuation(SiteRentalValuation):
    def render_enhanced_valuation(self):
        # استخدام أيقونات داخل التبويبات
        tab1, tab2, tab3 = st.tabs(["📍 الموقع الجغرافي", "💰 حساب التقييم", "📊 التقارير النهائية"])
        
        with tab1:
            st.markdown("### 🗺️ تحديد موقع العقار على الخريطة")
            is_mobile = st.session_state.get('is_mobile', False)
            
            # تقسيم الشاشة: خريطة بالأعلى أو الجانب حسب الجهاز
            if is_mobile:
                self.render_map_section()
                self.render_inputs_section()
            else:
                col1, col2 = st.columns([2, 1])
                with col1: self.render_map_section()
                with col2: self.render_inputs_section()

    def render_map_section(self):
        st.info("💡 انقر على الخريطة لتحديد الموقع بدقة")
        m = folium.Map(location=[24.7136, 46.6753], zoom_start=12)
        m.add_child(folium.LatLngPopup())
        
        # التقاط البيانات من الخريطة
        map_output = st_folium(m, height=350, width="100%")
        
        if map_output and map_output.get("last_clicked"):
            lat = map_output["last_clicked"]["lat"]
            lng = map_output["last_clicked"]["lng"]
            st.session_state.current_lat = lat
            st.session_state.current_lng = lng
            st.success(f"📍 تم تحديد الإحداثيات: {lat:.4f}, {lng:.4f}")

    def render_inputs_section(self):
        with st.container(border=True):
            st.markdown("#### 📝 بيانات العقار")
            site_name = st.text_input("اسم الموقع / العقار")
            site_area = st.number_input("المساحة الإجمالية (م²)", min_value=1.0)
            
            # تم استبدال use_container_width بـ width='stretch' حسب التحديث الجديد
            if st.button("💾 حفظ البيانات الآن", width="stretch", type="primary"):
                if 'current_lat' in st.session_state:
                    deal_data = {
                        'property_type': 'تجاري',
                        'location': site_name,
                        'area': site_area,
                        'price': 0.0,
                        'deal_date': datetime.now().date(),
                        'latitude': st.session_state.current_lat,
                        'longitude': st.session_state.current_lng,
                        'activity_type': 'تأجير',
                        'notes': 'إضافة عبر النظام المطور'
                    }
                    did = add_deal(deal_data)
                    st.balloons()
                    st.success(f"تم الحفظ بنجاح! رقم المرجع: {did}")
                else:
                    st.error("⚠️ يرجى النقر على الخريطة أولاً")

def main():
    is_mobile = detect_device_type()
    apply_mobile_optimization()
    
    if not st.session_state.get('authenticated'):
        # هنا يمكنك استدعاء صفحة تسجيل الدخول الخاصة بك
        st.title("🏗️ نظام HMMC العقاري")
        if st.button("تسجيل الدخول تجريبياً", width="stretch"):
            st.session_state.authenticated = True
            st.rerun()
    else:
        # القائمة الجانبية الاحترافية باستخدام أيقونات
        with st.sidebar:
            st.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=100)
            selected = option_menu(
                "القائمة الرئيسية",
                ["لوحة التحكم", "التقييم العقاري", "الإدارة", "خروج"],
                icons=['house', 'map', 'gear', 'door-open'],
                menu_icon="cast",
                default_index=0,
            )

        if selected == "لوحة التحكم":
            render_dashboard(st.session_state.get('user_role', 'admin'))
        elif selected == "التقييم العقاري":
            valuator = ProfessionalValuation()
            valuator.render_enhanced_valuation()
        elif selected == "الإدارة":
            render_admin_panel(st.session_state.get('user_role', 'admin'))
        elif selected == "خروج":
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    init_db()
    ensure_settings()
    main()
