import streamlit as st
import folium
from streamlit_folium import st_folium
from modules.db import add_deal
from datetime import datetime

class SiteRentalValuation:
    def __init__(self):
        # قائمة أحياء مكة المكرمة الرئيسية
        self.makkah_neighborhoods = [
            "العزيزية", "الشوقية", "البطحاء", "الرصيفة", "الشرائع", 
            "جبل النور", "العوالي", "بطحاء قريش", "المسفلة", "المنصور"
        ]

    def render_valuation(self):
        st.markdown("### 🗺️ تحديد الموقع والتقييم الإيجاري")
        
        tab1, tab2 = st.tabs(["📍 الخريطة (مكة)", "📝 بيانات التقييم"])
        
        with tab1:
            st.info("انقر على الموقع في مكة المكرمة لتحديد الإحداثيات")
            # إحداثيات مكة المكرمة الافتراضية
            m = folium.Map(location=[21.3891, 39.8579], zoom_start=12)
            m.add_child(folium.LatLngPopup())
            map_data = st_folium(m, height=400, width="100%")
            
            if map_data and map_data.get("last_clicked"):
                st.session_state.lat = map_data["last_clicked"]["lat"]
                st.session_state.lng = map_data["last_clicked"]["lng"]
                st.success(f"تم التحديد: {st.session_state.lat:.4f}, {st.session_state.lng:.4f}")

        with tab2:
            with st.form("valuation_form"):
                col1, col2 = st.columns(2)
                with col1:
                    neigh = st.selectbox("حي العقار (مكة)", self.makkah_neighborhoods)
                    area = st.number_input("المساحة (م²)", min_value=1.0)
                with col2:
                    p_type = st.selectbox("نوع العقار", ["تجاري", "سكني", "استثماري"])
                    base_price = st.number_input("سعر المتر التقديري", value=500.0)
                
                if st.form_submit_button("💾 حفظ وإصدار التقييم"):
                    if 'lat' in st.session_state:
                        deal_data = {
                            'property_type': p_type, 'location': "مكة المكرمة",
                            'neighborhood': neigh, 'area': area, 'price': base_price * area,
                            'deal_date': datetime.now().date(), 'latitude': st.session_state.lat,
                            'longitude': st.session_state.lng, 'activity_type': 'إيجار بلدي', 'notes': ''
                        }
                        did = add_deal(deal_data)
                        st.session_state.site_info = deal_data
                        st.success(f"✅ تم الحفظ بنجاح! رقم المرجع: {did}")
                    else:
                        st.error("⚠️ يرجى تحديد الموقع على الخريطة أولاً")
