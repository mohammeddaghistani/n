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
        st.warning("لا توجد بيانات حالية. قم بإضافة تقييمات من صفحة التقييم.")
        return

    # صف المؤشرات
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("إجمالي المواقع", len(df))
    with c2: st.metric("متوسط المساحات", f"{df['area'].mean():.0f} م²")
    with c3: st.metric("أحدث إضافة في مكة", df['neighborhood'].iloc[-1])

    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        fig1 = px.pie(df, names='neighborhood', title="توزيع المواقع حسب أحياء مكة")
        st.plotly_chart(fig1, use_container_width=True)
    with col_b:
        fig2 = px.bar(df, x='neighborhood', y='price', title="إجمالي القيم حسب الحي")
        st.plotly_chart(fig2, use_container_width=True)
