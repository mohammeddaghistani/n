import streamlit as st
from fpdf import FPDF
from arabic_reshaper import reshape
from bidi.algorithm import get_display

def fix_ar(text):
    if not text: return ""
    return get_display(reshape(str(text)))

def render_report_module(user_role):
    st.header("📄 تصدير تقرير التقييم (PDF)")
    
    if 'site_info' not in st.session_state:
        st.info("يرجى إجراء تقييم أولاً لتوليد التقرير")
        return

    data = st.session_state.site_info
    
    if st.button("📥 تحميل التقرير"):
        pdf = FPDF()
        pdf.add_page()
        # ملاحظة: يجب توفر خط Arial.ttf في مجلد assets
        try:
            pdf.add_font('Tajawal', '', 'assets/Tajawal.ttf', uni=True)
            pdf.set_font('Tajawal', '', 16)
        except:
            pdf.set_font('Arial', '', 12)

        pdf.cell(0, 10, fix_ar("تقرير تقييم موقع عقاري - مكة المكرمة"), ln=True, align='C')
        pdf.ln(10)
        pdf.cell(0, 10, fix_ar(f"الحي: {data['neighborhood']}"), ln=True, align='R')
        pdf.cell(0, 10, fix_ar(f"المساحة: {data['area']} م²"), ln=True, align='R')
        pdf.cell(0, 10, fix_ar(f"القيمة التقديرية: {data['price']:,} ريال"), ln=True, align='R')
        
        output = pdf.output(dest='S').encode('latin-1', errors='ignore')
        st.download_button("تأكيد التحميل", output, "Report_Makkah.pdf", "application/pdf")
