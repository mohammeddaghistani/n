import streamlit as st
from fpdf import FPDF
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from datetime import datetime
import os

# دالة معالجة النصوص العربية لـ PDF
def ar(text):
    if not text: return ""
    reshaped_text = reshape(str(text))
    bidi_text = get_display(reshaped_text)
    return bidi_text

class ProfessionalPDF(FPDF):
    def header(self):
        # إضافة شعار أو عنوان في رأس الصفحة
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, ar("تقرير التقييم العقاري المهني"), ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} / {{nb}}', align='C')

def generate_pdf(data):
    pdf = ProfessionalPDF()
    pdf.add_page()
    
    # ملاحظة: يجب توفر ملف خط يدعم العربية مثل (Arial.ttf) في مجلد fonts
    # إذا لم يتوفر، سيستخدم الخط الافتراضي (قد لا يظهر العربي بشكل صحيح بدون خط مخصص)
    try:
        pdf.add_font('ArabicFont', '', 'fonts/Arial.ttf', uni=True)
        pdf.set_font('ArabicFont', '', 12)
    except:
        pdf.set_font('Arial', '', 12)

    # --- القسم الأول: معلومات التقرير ---
    pdf.set_fill_color(30, 58, 138) # لون أزرق (نفس القالب)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, ar("١. المعلومات الأساسية"), ln=True, fill=True, align='R')
    pdf.set_text_color(0, 0, 0)
    
    pdf.ln(5)
    pdf.cell(0, 10, ar(f"رقم التقرير: {data.get('valuation_number', 'VAL-2026-001')}"), ln=True, align='R')
    pdf.cell(0, 10, ar(f"تاريخ التقييم: {data.get('deal_date', datetime.now().date())}"), ln=True, align='R')
    
    # --- القسم الثاني: وصف العقار ---
    pdf.ln(10)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, ar("٢. وصف العقار"), ln=True, fill=True, align='R')
    pdf.set_text_color(0, 0, 0)
    
    pdf.ln(5)
    pdf.cell(0, 10, ar(f"الموقع: {data.get('location', 'غير محدد')}"), ln=True, align='R')
    pdf.cell(0, 10, ar(f"المساحة: {data.get('area', 0)} م²"), ln=True, align='R')
    pdf.cell(0, 10, ar(f"الإحداثيات: {data.get('latitude', 0)}, {data.get('longitude', 0)}"), ln=True, align='R')

    # --- القسم الثالث: النتائج المالية ---
    pdf.ln(10)
    pdf.set_draw_color(251, 191, 36) # لون ذهبي (نفس القالب)
    pdf.set_line_width(1)
    pdf.rect(10, pdf.get_y(), 190, 30)
    
    pdf.set_y(pdf.get_y() + 5)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, ar(f"القيمة الإيجارية المقدرة: {data.get('price', 0)} ريال سعودي"), ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1', errors='ignore')

def render_report_module():
    st.markdown("### 📄 إصدار تقارير التقييم")
    
    # جلب آخر بيانات تم التعامل معها من الجلسة
    if 'site_info' not in st.session_state:
        st.info("💡 لا توجد بيانات حالية لإصدار تقرير. قم بإجراء عملية تقييم أولاً.")
        return

    data = st.session_state.site_info

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.success("✅ البيانات جاهزة للتصدير")
        with st.expander("🔍 استعراض بيانات التقرير قبل الطباعة"):
            st.write(data)
            
    with col2:
        # زر تحميل التقرير
        pdf_bytes = generate_pdf(data)
        st.download_button(
            label="📥 تحميل التقرير (PDF)",
            data=pdf_bytes,
            file_name=f"Report_{data.get('location', 'Property')}.pdf",
            mime="application/pdf",
            width="stretch" # التزاماً بالتحديث الجديد بدلاً من use_container_width
        )

    # عرض القالب HTML (للمعاينة فقط)
    st.divider()
    st.markdown("#### 🖼️ معاينة تصميم التقرير")
    # هنا نقوم بعرض القالب الذي أرسلته بشكل تفاعلي
    st.components.v1.html(open("report_template.html", "r", encoding="utf-8").read(), height=600, scrolling=True)
