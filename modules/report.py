import streamlit as st
from fpdf import FPDF
from arabic_reshaper import reshape
from bidi.algorithm import get_display

def fix_ar(text):
    if not text: return ""
    return get_display(reshape(str(text)))

def render_report_module(user_role):
    st.header("📑 تصدير التقارير الرسمية")
    
    if 'site_info' not in st.session_state:
        st.warning("يرجى إجراء عملية تقييم أولاً لتتمكن من إصدار تقرير.")
        return

    data = st.session_state.site_info
    
    if st.button("📥 تحميل التقرير كـ PDF"):
        pdf = FPDF()
        pdf.add_page()
        # ملاحظة: يجب توفير خط يدعم العربية في مجلد assets/Arial.ttf
        try:
            pdf.add_font('ArialAR', '', 'assets/Arial.ttf', uni=True)
            pdf.set_font('ArialAR', '', 16)
        except:
            pdf.set_font('Arial', '', 12)

        pdf.cell(0, 10, fix_ar("تقرير تقييم عقاري رسمي"), ln=True, align='C')
        pdf.ln(10)
        pdf.cell(0, 10, fix_ar(f"الموقع: {data['location']}"), ln=True, align='R')
        pdf.cell(0, 10, fix_ar(f"المساحة: {data['area']} م٢"), ln=True, align='R')
        
        pdf_output = pdf.output(dest='S').encode('latin-1', errors='ignore')
        st.download_button("تأكيد تحميل الملف", pdf_output, "report.pdf", "application/pdf")
