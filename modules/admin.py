import streamlit as st
from modules.db import get_setting, update_setting
from modules.auth import check_permission

def render_admin_panel(user_role):
    if not check_permission('admin'):
        st.error("عذراً، لا تملك صلاحية الوصول لهذه الصفحة.")
        return

    st.header("⚙️ إدارة إعدادات النظام")
    
    with st.form("admin_settings"):
        col1, col2 = st.columns(2)
        with col1:
            m_temp = st.number_input("معامل التأجير المؤقت", value=float(get_setting('mult_temp', 0.85)))
            m_long = st.number_input("معامل الاستثمار طويل الأجل", value=float(get_setting('mult_long', 1.60)))
        with col2:
            cost = st.number_input("تكلفة البناء (ريال/م²)", value=float(get_setting('const_cost', 3500)))
            discount = st.number_input("معدل الخصم DCF %", value=float(get_setting('discount_rate', 0.10)))

        if st.form_submit_button("💾 حفظ الإعدادات وتحديث النظام"):
            update_setting('mult_temp', m_temp)
            update_setting('mult_long', m_long)
            update_setting('const_cost', cost)
            update_setting('discount_rate', discount)
            st.success("✅ تم تحديث الإعدادات بنجاح")
