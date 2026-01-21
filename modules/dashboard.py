import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

def render_dashboard(user_role):
    st.markdown("## 📊 لوحة المؤشرات الإحصائية")
    
    conn = sqlite3.connect('data/system.db')
    df = pd.read_sql_query("SELECT * FROM deals", conn)
    conn.close()

    if df.empty:
        st.info("لا توجد بيانات حالية لعرضها.")
        return

    # مؤشرات سريعة
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الصفقات", len(df))
    c2.metric("متوسط المساحة", f"{df['area'].mean():.0f} م²")
    c3.metric("أحدث إضافة", str(df['deal_date'].max()))

    # رسوم بيانية
    col_a, col_b = st.columns(2)
    with col_a:
        fig1 = px.pie(df, names='property_type', title="توزيع أنواع العقارات", hole=0.4)
        st.plotly_chart(fig1, use_container_width=True)
    with col_b:
        fig2 = px.bar(df, x='deal_date', y='area', title="المساحات المضافة زمنياً")
        st.plotly_chart(fig2, use_container_width=True)
