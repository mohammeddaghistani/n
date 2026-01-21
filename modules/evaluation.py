import streamlit as st
from datetime import datetime
from modules.db import add_deal

def render_evaluation_module(user_role):
    st.header("📑 نظام التقييم العقاري")
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            loc = st.text_input("📍 عنوان الموقع")
            area = st.number_input("📐 المساحة (م²)", min_value=1.0)
        with col2:
            p_type = st.selectbox("🏠 النوع", ["تجاري", "سكني", "صناعي"])
            act = st.selectbox("💼 نوع النشاط", ["تأجير بلدي", "استثمار", "فعاليات"])

        notes = st.text_area("📝 ملاحظات إضافية")
        
        if st.button("🚀 تنفيذ وحفظ التقييم", type="primary"):
            deal_data = {
                'property_type': p_type, 'location': loc, 'area': area,
                'price': 0.0, 'deal_date': datetime.now().date(),
                'activity_type': act, 'notes': notes
            }
            res_id = add_deal(deal_data)
            st.session_state.site_info = deal_data
            st.success(f"✅ تم الحفظ بنجاح بالرقم المرجعي: {res_id}")
