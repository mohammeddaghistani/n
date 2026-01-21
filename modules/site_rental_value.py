import folium
from streamlit_folium import st_folium

def render_makkah_map():
    st.markdown("### 📍 تحديد الموقع الجغرافي (منطقة مكة)")
    # إحداثيات مكة المكرمة
    m = folium.Map(location=[21.3891, 39.8579], zoom_start=13)
    
    # إضافة أحياء مكة كطبقة معلوماتية
    makkah_neighborhoods = ["العزيزية", "الشوقية", "البطحاء", "الرصيفة", "الشرائع"]
    
    map_data = st_folium(m, height=400, width="100%", key="makkah_map")
    
    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lng = map_data["last_clicked"]["lng"]
        st.success(f"تم التقاط الإحداثيات لموقع مكة: {lat:.5f}, {lng:.5f}")
