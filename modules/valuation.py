import numpy as np

class MakkahValuationEngine:
    """تطبيق المعادلات العلمية الواردة في دليل تقييم العقارات البلدية"""
    
    @staticmethod
    def market_approach(area, unit_price, adjustments):
        """أسلوب السوق: مقارنة المبيعات مع التسويات"""
        # adjustments عبارة عن قاموس للنسب المئوية (+ أو -)
        total_adjustment = sum(adjustments.values()) / 100
        final_unit_price = unit_price * (1 + total_adjustment)
        return final_unit_price * area

    @staticmethod
    def income_approach_dcf(annual_income, discount_rate, term_years):
        """أسلوب الدخل: التدفقات النقدية المخصومة DCF"""
        # PV = Sum(CF / (1+r)^t)
        pv = sum([annual_income / ((1 + discount_rate) ** t) for t in range(1, int(term_years) + 1)])
        return pv

    @staticmethod
    def residual_method(gdv, development_costs, developer_profit=0.20):
        """طريقة القيمة المتبقية للمشروعات الكبرى"""
        # قيمة الأرض = القيمة الإجمالية للتطوير - (التكاليف + الأرباح)
        return gdv - (development_costs * (1 + developer_profit))
