import streamlit as st
import folium
from streamlit_folium import st_folium
from modules.db import init_db, ensure_settings, add_deal
from modules.style import apply_makkah_theme
from modules.valuation import MakkahValuationEngine

# الإعدادات
st.set_page_config(page_title="HMMC - نظام تقييم مكة", layout="wide")
init_db()
ensure_settings()
apply_makkah_theme()

# دالة كشف الجوال
def is_mobile():
    ua = st.context.headers.get("User-Agent", "").lower()
    return any(x in ua for x in ["mobile", "android", "iphone"])

st.title("🕋 نظام التقييم العقاري البلدي - منطقة مكة")

# التقسيم الرئيسي
col_map, col_inputs = st.columns([2, 1] if not is_mobile() else [1, 1])

with col_map:
    st.subheader("📍 تحديد الموقع (مكة وأحياؤها)")
    # مكة المكرمة
    m = folium.Map(location=[21.3891, 39.8579], zoom_start=12)
    m.add_child(folium.LatLngPopup())
    map_data = st_folium(m, height=450, width="100%", key="makkah_map")

with col_inputs:
    with st.form("valuation_form"):
        st.subheader("💰 مدخلات التقييم")
        neighborhood = st.selectbox("الحي", ["العزيزية", "الشوقية", "بطحاء قريش", "الشرائع", "الرصيفة"])
        area = st.number_input("المساحة (م²)", min_value=1.0, value=500.0)
        
        # اختيار نوع العقد بناءً على اللائحة
        lease_type = st.selectbox("نوع التصرف", ["تأجير مؤقت (فعاليات)", "استثمار طويل الأجل", "تأجير مباشر"])
        
        base_price = st.number_input("سعر المتر المرجعي", value=1500.0)
        
        if st.form_submit_button("🚀 تنفيذ التقييم العلمي"):
            engine = MakkahValuationEngine()
            # تطبيق أسلوب السوق افتراضياً
            final_val = engine.market_approach(area, base_price, {"location": 5, "view": 2})
            
            st.session_state.last_result = final_val
            st.success(f"القيمة التقديرية: {final_val:,.2f} ريال")
            
            # حفظ في DB
            add_deal({
                'property_type': 'تجاري', 'location': 'مكة', 'neighborhood': neighborhood,
                'area': area, 'price': final_val, 'deal_date': '2026-01-21',
                'activity_type': lease_type, 'notes': 'تقييم آلي'
            })
