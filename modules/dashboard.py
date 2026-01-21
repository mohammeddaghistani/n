import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

def get_dashboard_data():
    """جلب البيانات من قاعدة البيانات لتحليلها"""
    try:
        conn = sqlite3.connect('data/system.db')
        # جلب البيانات من جدول deals الذي أنشأناه سابقاً
        df = pd.read_sql_query("SELECT * FROM deals", conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

def render_dashboard(user_role):
    st.markdown("## 📊 لوحة المؤشرات الإحصائية")
    
    df = get_dashboard_data()
    
    if df.empty:
        st.warning("⚠️ لا توجد بيانات متاحة حالياً. قم بإضافة عقارات من صفحة التقييم أولاً.")
        return

    # --- القسم الأول: المؤشرات السريعة (Metrics) ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("إجمالي العقارات", len(df), delta="محدث")
    with col2:
        st.metric("متوسط المساحات", f"{df['area'].mean():.1f} م²")
    with col3:
        total_types = df['property_type'].nunique()
        st.metric("تنوع الاستخدامات", total_types)
    with col4:
        st.metric("أحدث إضافة", df['deal_date'].max() if not df['deal_date'].isnull().all() else "N/A")

    st.divider()

    # --- القسم الثاني: الرسوم البيانية ---
    row2_col1, row2_col2 = st.columns([1, 1])

    with row2_col1:
        st.markdown("#### 🏗️ توزيع العقارات حسب النوع")
        # رسم بياني دائري (Pie Chart)
        fig_pie = px.pie(df, names='property_type', hole=0.4, 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

    with row2_col2:
        st.markdown("#### 📈 مقارنة المساحات لكل موقع")
        # رسم بياني أعمدة (Bar Chart)
        fig_bar = px.bar(df, x='location', y='area', color='property_type',
                         labels={'location': 'الموقع', 'area': 'المساحة'},
                         color_discrete_sequence=px.colors.qualitative.Set2)
        fig_bar.update_layout(margin=dict(t=20, b=0, l=0, r=0), height=300)
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- القسم الثالث: جدول البيانات الأخير ---
    st.markdown("#### 📋 آخر المواقع المضافة")
    # عرض آخر 5 صفوف بتنسيق جميل
    st.dataframe(df[['location', 'property_type', 'area', 'deal_date']].tail(5), 
                 use_container_width=True, hide_index=True)
