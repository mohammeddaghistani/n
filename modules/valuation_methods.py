import pandas as pd
import numpy as np
import streamlit as st

class ValuationEngine:
    """محرك التقييم المعتمد على المعايير الدولية IVS"""
    
    @staticmethod
    def sales_comparison(area, price_per_m2, adjustments):
        """أسلوب السوق: مقارنة المبيعات [cite: 734]"""
        total_adj = sum(adjustments.values()) / 100
        adjusted_price = price_per_m2 * (1 + total_adj)
        return adjusted_price * area

    @staticmethod
    def residual_method(gdv, const_cost, developer_profit=0.20):
        """أسلوب الدخل: طريقة القيمة المتبقية [cite: 862, 1369]"""
        # المعادلة: قيمة الأرض = القيمة الإجمالية للتطوير - التكاليف (1 + الربح)
        total_costs = const_cost * (1 + developer_profit)
        land_value = gdv - total_costs
        return max(0, land_value)

    @staticmethod
    def dcf_valuation(annual_income, rate, years):
        """أسلوب الدخل: التدفقات النقدية المخصومة [cite: 791, 1570]"""
        # المعادلة: PV = Sum(Income / (1+r)^t)
        pv = sum([annual_income / ((1 + rate) ** t) for t in range(1, int(years) + 1)])
        return pv

def render_valuation_ui():
    st.title("🕋 محرك التقييم العقاري - مكة المكرمة")
    engine = ValuationEngine()
    
    method = st.segmented_control(
        "اختر منهجية التقييم المعتمدة",
        ["مقارنة المبيعات", "القيمة المتبقية", "التدفقات النقدية (DCF)"],
        default="مقارنة المبيعات"
    )

    with st.container(border=True):
        if method == "مقارنة المبيعات":
            c1, c2 = st.columns(2)
            area = c1.number_input("المساحة (م²)", value=1000.0)
            base_p = c2.number_input("سعر المتر المرجعي (ريال)", value=5000.0)
            
            st.markdown("##### ⚖️ معاملات التسوية (Adjustments)")
            adj_loc = st.slider("ميزة الموقع %", -20, 20, 0)
            adj_view = st.slider("الإطلالة والواجهة %", -10, 10, 0)
            
            result = engine.sales_comparison(area, base_p, {'loc': adj_loc, 'view': adj_view})
            st.metric("القيمة التقديرية السوقية", f"{result:,.2f} ريال")

        elif method == "القيمة المتبقية":
            # تطبيق مثال الأراضي 3 من الدليل [cite: 1376]
            gdv = st.number_input("القيمة الإجمالية للتطوير المتوقعة (GDV)", value=10000000.0)
            c_cost = st.number_input("إجمالي تكاليف الإنشاء والرسوم", value=6000000.0)
            profit = st.select_slider("نسبة ربح المطور", options=[0.15, 0.20, 0.25], value=0.20)
            
            land_val = engine.residual_method(gdv, c_cost, profit)
            st.metric("قيمة الأرض المتبقية", f"{land_val:,.2f} ريال")
